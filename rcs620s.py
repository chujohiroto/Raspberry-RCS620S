#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""RC-S620/S sample library for Python https://qiita.com/rukihena/items/476d48e1e8d8fc6b98bf#_reference-e396793bfda9cc109c2c """

from __future__ import print_function

import time
import serial
import stringbin

class Rcs620s:

    __RCS620S_MAX_CARD_RESPONSE_LEN = 254
    __RCS620S_MAX_RW_RESPONSE_LEN = 265

    __RCS620S_DEFAULT_TIMEOUT = 1000

    __ser = None    # シリアルオブジェクト

    idm = None  # IDm：polling で設定される。8バイト文字列。
    pmm = None  # PMm：polling で設定される。8バイト文字列。

    def __init__(self):
        self.__timeout = self.__RCS620S_DEFAULT_TIMEOUT


    def gettimeout(self):
        return self.__timeout

    def settimeout(self, value):
        self.__timeout = value
        self.__ser.timeout(value/1000.0)

    def initDevice(self, portName):

        try:
            self.__ser = serial.Serial(port=portName, baudrate=115200, timeout=self.__timeout/1000.0)
        except serial.serialutil.SerialException:
            return "can't open serial port"

        response = self.__rwCommand("\xd4\x32\x02\x00\x00\x00")
        if (response != "\xd5\x33" ) :
            return "can't open RC-S620/S"

        # RFConfiguration (max retries)
        response = self.__rwCommand("\xd4\x32\x05\x00\x00\x00")
        if (response != "\xd5\x33" ) :
            return "can't initialize RC-S620/S"

        # RFConfiguration (additional wait time = 24ms)
        response = self.__rwCommand("\xd4\x32\x81\xb7")
        if (response != "\xd5\x33" ) :
            return "can't initialize RC-S620/S"

        return ""

    def polling(self, systemCode) :
        # InListPassiveTarget
        buf = "\xd4\x4a\x01\x01\x00" + systemCode + "\x00\x0f"

        response = self.__rwCommand(buf)
        if (response is None):return False
        if (len(response) != 22) :return False
        if (not response.startswith("\xd5\x4b\x01\x01\x12\x01")) :return False

        self.idm = response[6:6+8]
        self.pmm = response[14:14+8]

        return True

    def cardCommand(self, command) :
        if (self.__timeout >= (0x10000 / 2)) :
            commandTimeout = 0xffff;
        else :
            commandTimeout = (self.__timeout * 2);
        # CommunicateThruEX
        buf = "\xd4\xa0"
        buf += stringbin.int2strbinLE(commandTimeout,2)
        buf += chr(len(command) + 1)
        buf += command

        buf = self.__rwCommand(buf)
        if (buf is None) :return None
        bufLen = len(buf)
        if (bufLen < 4) :return None
        if (not buf.startswith("\xd5\xa1\x00")) :return None
        if (bufLen != (3 + ord(buf[3]))) :return None

        return buf[4:]

    def rfOff(self) :
        # RFConfiguration (RF field)
        response = self.__rwCommand("\xd4\x32\x01\x00")
        if (response != "\xd5\x33" ) :
            return False

        return True

    def push(self, data) :
        # 未テストです

        dataLen = len(data)
        if (dataLen > 224) :
            return False

        # Push
        buf = "\xb0"+self.idm+chr(dataLen) + data

        buf = self.cardCommand(buf)
        if ( buf != "\xb1"+self.idm+chr(dataLen) ) :
            return False

        buf = "\xa4"+self.idm+"\x00"
        buf = self.cardCommand(buf)
        if ( buf != "\xa5"+self.idm+"\x00") :
            return False

        time.sleep(1000)

        return True

    def requestService(self, serviceCode):
        u""" サービスの存在確認 """
        buf = "\x02" + self.idm + "\x01" + serviceCode

        buf = self.cardCommand(buf)

        if (buf is None) : return False
        if (len(buf) != 12) : return False
        if (not buf.startswith("\x03" + self.idm)) : return False
        if (buf[10:] == "\xff\xff") : return False

        return True


    def readWithoutEncryption(self, serviceCode, blockNumber):
        u""" 暗号化なしで読む """
        buf = "\x06" + self.idm
        buf += "\x01" # サービス数
        buf += serviceCode
        buf += "\x01" # ブロック数(なぜか複数指定するとエラーが返る)
        buf += "\x80"
        buf += chr(blockNumber)

        buf = self.cardCommand(buf)

        if (buf is None) :
            return None
        if (len(buf) != 28) :
            return None
        if (not buf.startswith("\x07"+self.idm)) :
            return None

        return buf[12:]

    def readWithoutEncryption2(self, serviceCode, blockNumber, length):
        u""" 複数ブロックを暗号化なしで読む """
        res = ""
        for i in range(0, length):
            buf = self.readWithoutEncryption(serviceCode, blockNumber+i)
            if ( buf != None ) :
                res += buf
        return res


    def readBlock(self, serviceCode, blockNumber, length):
        u""" 存在確認してから読む """
        if(self.requestService(serviceCode)) :
            return self.readWithoutEncryption2(serviceCode, 0, length)
        else:
            return None

# ------------------------
# private
# ------------------------

    def __rwCommand(self, command):
        self.__flushSerial();

        commandLen = len(command)

        dcs = self.__calcDCS(command)

        # transmit the command
        req = "\x00\x00\xff"
        if (commandLen <= 255) :
            # normal frame
            req += chr(commandLen) + chr((-commandLen)&0xff)
            self.__writeSerial(req)
        else :
            # extended frame
            # 未テストです
            req += "\xff\xff"
            req += chr((commandLen >> 8) & 0xff)
            req += chr((commandLen >> 0) & 0xff)
            req += chr(self.calfDCS(req[2:]))
            self.__writeSerial(req);

        self.__writeSerial(command);
        req = chr(dcs)+"\x00"
        self.__writeSerial(req);

        # receive an ACK
        res = self.__readSerial(6);
        if (res != "\x00\x00\xff\x00\xff\x00") :
            self.__cancel()
            return None

        # receive a response
        res = self.__readSerial(5);
        if (res == None) :
            self.__cancel()
            return None
        elif ( not res.startswith("\x00\x00\xff") ) :
            return None

        if ((res[3] == "\xff") and (res[4] == "\xff")) :
            # 未テストです
            res = self.__readSerial(3)
            if (res == None or self.__calcDCS(res) != 0) :
                return None
            responseLen = (ord(res[5]) << 8) | (ord(res[6]) << 0)
        else :
            if (self.__calcDCS(res[3:]) != 0) :
                return None
            responseLen = ord(res[3])
        if (responseLen > self.__RCS620S_MAX_RW_RESPONSE_LEN) :
            return None

        response = self.__readSerial(responseLen)
        if (response == None) :
            self.__cancel()
            return None

        dcs = chr(self.__calcDCS(response))

        res = self.__readSerial(2)
        if (res == None or res[0] != dcs or res[1] != "\x00") :
            self.__cancel()
            return None

        return response

    def __cancel(self):
        # transmit an ACK
        self.__writeSerial("\x00\x00\xff\x00\xff\x00")
        time.sleep(0.001);
        self.__flushSerial();

    # DCS(チェックサム)を計算する
    def __calcDCS(self, data):

        checkSum = 0;
        for c in data:
            checkSum += ord(c)
        return -checkSum & 0xff

    def __writeSerial(self, data) :
        self.__ser.write(data);

    def __readSerial(self, length) :

        data = self.__ser.read(length)
        if ( len(data) == length ) :
            return data
        else :
            return None

    def __flushSerial(self) :
        self.__ser.flush()
