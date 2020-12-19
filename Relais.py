#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import statusLEDs

'''
Schalte Relais (NC) je nach Status
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

'''
Probiere den Drucker aus/einzuschalten je nach Status 
(warping oder kein Warping)
'''
def statusDrucker(status):
	try:
		if status == "warping":
			drucker_aus(channel)
		elif status == "no_warping":
			drucker_ein(channel)
		else:
			statusLEDs.lightLed("err")
			
	#Wenn das Programm beendet wird, raeume auf		
	except KeyboardInterrupt:
		GPIO.cleanup()
		pass
	

	
