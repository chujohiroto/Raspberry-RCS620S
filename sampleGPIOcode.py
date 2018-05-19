# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time

COUNT = 3
PIN1 = 11
PIN2 = 13
PIN3 = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN1,GPIO.OUT)
GPIO.setup(PIN2,GPIO.OUT)
GPIO.setup(PIN3,GPIO.OUT)

for _ in xrange(COUNT):
	GPIO.output(PIN1,True)
	GPIO.output(PIN2,False)
	time.sleep(0.5)
	GPIO.output(PIN2,True)
	GPIO.output(PIN3,False)
	time.sleep(0.5)
	GPIO.output(PIN1,False)
	GPIO.output(PIN3,True)
	time.sleep(0.5)
	GPIO.output(PIN2,False)
	GPIO.output(PIN1,True)
	time.sleep(0.5)

GPIO.cleanup()
