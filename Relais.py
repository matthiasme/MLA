#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import statusLEDs

'''
Schalte Relais (NC) je nach Status
'''

GPIO.setmode(GPIO.BCM)
gpio_no = 18
GPIO.setup(gpio_no, GPIO.OUT)

#Schalte Drucker aus
def drucker_aus(Klaus):
	GPIO.output(Klaus, GPIO.HIGH)

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
			drucker_aus(gpio_no)
		elif status == "no_warping":
			drucker_ein(gpio_no)
		else:
			statusLEDs.lightLed("err")
			
	#Wenn das Programm beendet wird, raeume auf		
	except KeyboardInterrupt:
		GPIO.cleanup()
		pass
	

	
