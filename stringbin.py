#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""バイナリな文字列を扱います"""

def strbinBE2int(strbin):

    summation = 0;
    for c in strbin:
        summation <<= 8
        summation += ord(c)
    return summation

def strbinLE2int(strbin):
    return strbinBE2int(strbin[::-1])

def int2strbinLE(num,length):
    strbin = ""
    for _ in range(0, length):
        strbin += chr(num & 0xff)
        num >>= 8

    return strbin

def int2strbinBE(num,length):
    return int2strbinLE(num,length)[::-1]
