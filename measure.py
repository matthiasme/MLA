#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import time, csv
from datetime import datetime
import numpy as np
import statusLEDs, Relais

def measure(scaleRatio=-1, averageOfXValues = 20, limit = 15, date_time = "def.csv"): 
	try:
		GPIO.setmode(GPIO.BCM)
		hx711 = HX711(dout_pin=5,pd_sck_pin=6,
						gain_channel_A=64,select_channel='A')
		
		hx711.reset()   #Zurücksetzen
		time.sleep(1)
		hx711.zero()    #Offset eliminieren
		hx711.set_scale_ratio(scaleRatio)

		#Erstelle eine neue csv-datei:
		f = open("Data/" + date_time, "w+")
		f_csv_writer = csv.writer(f,delimiter=",")
		print("Values are saved to: " + date_time)
		
		#measurement:
		print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
		print('Current value measured is: ')
		row_index = 0
		nowarping = True

		while nowarping:
			#Messe Werte:
			statusLEDs.lightLed("no_warping")
			outputvalue = hx711.get_weight_mean(averageOfXValues)
			force = round((outputvalue+27776.8/186245)*9.81 , 2)
			print("Output: " + outputvalue, "\t Force: " + force)

			#Erstelle Inhalt der naechsten Reihe:
			row_time = datetime.now().strftime("%H/%M/%S")
			row_content = [row_index, row_time, outputvalue, force]
			row_index +=1

			#Schreibe die naeste Reihe:
			f_csv_writer.writerow(row_content)

			#Pruefe Warping Bedingung:
			if force>limit:
				nowarping = False
				return True		
							
	except (KeyboardInterrupt, SystemExit): #Programm kann mit Ctrl + C angehalten werden
		print("Pfiat di Gott! :D")
		f.close() 
		GPIO.cleanup()

	finally:
		f.close() # Schliesse Daten.txt
		GPIO.cleanup()