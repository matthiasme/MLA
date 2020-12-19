#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

'''
Schalte Relais test
'''

channel = 18
	
#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


#Schalte Drucker aus
def drucker_aus(pin):
	GPIO.output(pin, GPIO.HIGH)

#Schalte Drucker ein	
def drucker_ein(pin):
	GPIO.output(pin, GPIO.LOW)

try:
	for x in range(0,2):
		drucker_aus(channel)
		time.sleep(30)  
		drucker_ein(channel)
		time.sleep(30)   
		x+=1
except KeyboardInterrupt:
	GPIO.cleanup()
	pass

finally:
	GPIO.cleanup()
	pass
