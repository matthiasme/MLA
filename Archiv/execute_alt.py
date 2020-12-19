#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import statusLEDs
import statusRelaise
import time
import telegrambot

if __name__ == "__main__": 
	try:
		GPIO.setmode(GPIO.BCM)
		hx711 = HX711(dout_pin=5,pd_sck_pin=6,
						gain_channel_A=64,select_channel='A')
		
		#Offset eliminieren
		print("Bitte entfernen Sie alle Gewichte von der Waage.")
		time.sleep(5)
		hx711.reset()   #Before we start, reset the HX711 (not obligate)
		hx711.zero()
		
		#Scale Ratio setzen
		print("Bitte bekanntes Gewicht auflegen!")
		while True:
			try:
				value = float(input("Wie viel Gramm wiegt das Gewicht?"))
				measures = hx711.get_raw_data_mean()
			except TypeError:
				print("Ungueltige Eingabe! Bitte erneut versuchen.")
				continue
			else:
				break
		scaleRatio = (measures/value)*1.5
		scaleRatio = (measures/value)*1.5
		hx711.set_scale_ratio(scaleRatio)
		
		#Gewichte ausgeben und LEDs ansteuern
		print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
		input('Press Enter to begin reading')
		print('Current weight on the scale in grams is: ')
		while True:
			outputvalue = hx711.get_weight_mean(20)
			print(outputvalue, 'gr.')
			if outputvalue>200:
				statusLEDs.lightLed("warping")
				statusRelaise.statusDrucker("warping")
				
				userinput = input("Fehler erkannt! Druck Fortsetzen? (y / n)" )
				if userinput == "y":
					Print("Strom wird wieder eingeschaltet. Druck kann manuell fortgesetzt werden."
					statusRelaise.statusDrucker("no_warping")
			else:
				statusLEDs.lightLed("no_warping")
			
	except (KeyboardInterrupt, SystemExit):
		print("Pfiat di Gott! :D")

	finally:
		GPIO.cleanup()

