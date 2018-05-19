#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import stringbin

import rcs620s

COMMAND_TIMEOUT = 250

# serial port
SERIAL_PORT_NAME = "/dev/ttyAMA0" #raspberrypiの場合
SERIAL_PORT_NAME = "COM3" #windowsの場合

def printBalance(card_name, balance):
    u""" 残高を表示する """
    print("%s %uyen" % (card_name, balance))

def hexdmp(strhex,delimiter) :
    u""" 文字列（中身はバイナリ）をHEXダンプする """
    result = ""
    for c in strhex :
        result += c.encode('hex')
        result += delimiter

    if ( 0<len(delimiter) ) :
        # 最後に付けてしまっているdelimiterを取る
        result = result[:-len(delimiter)]

    return result

if __name__ == '__main__':

    rcs620sObj = rcs620s.Rcs620s()

    ret = rcs620sObj.initDevice(SERIAL_PORT_NAME)

    if (ret!="") :
        # 初期化失敗→エラーを吐いて終了
        print(ret)
        sys.exit(1)

    rcs620s.timeout = COMMAND_TIMEOUT

    # Suica領域
    if(rcs620sObj.polling("\x00\x03")):
        print(hexdmp(rcs620sObj.idm,":"))
        # Suica PASMO etc
        # http://jennychan.web.fc2.com/format/suica.html
        buf = rcs620sObj.readBlock("\x8B\x00", 0, 1)
        if(buf is not None) :
            balance = stringbin.strbinLE2int(buf[11:13])
            printBalance("SUICA", balance)

    # 共通領域
    if(rcs620sObj.polling("\xFE\x00")):
        print(hexdmp(rcs620sObj.idm,":"))
        # nanaco
        buf = rcs620sObj.readBlock("\x97\x55", 0, 1)
        if(buf is not None) :
            balance = stringbin.strbinLE2int(buf[0:4])
            printBalance("nanaco", balance)

        # waon
        buf = rcs620sObj.readBlock("\x17\x68", 0, 1)
        if(buf is not None) :
            balance = stringbin.strbinLE2int(buf[0:2])
            printBalance("WAON", balance)

        # Edy
        buf = rcs620sObj.readBlock("\x17\x13", 0, 1)
        if(buf is not None) :
            balance = stringbin.strbinLE2int(buf[0:4])
            printBalance("Edy", balance)

    rcs620sObj.rfOff()
