#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import time, csv
from csv import writer
from datetime import datetime
import numpy as np
import statusLEDs, Relais
import os

def measure(scaleRatio=-1, averageOfXValues = 20, limit = 15, date_time = "def.csv"): 
    try:
        GPIO.setmode(GPIO.BCM)
        hx711 = HX711(dout_pin=5,pd_sck_pin=6, gain_channel_A=64,select_channel='A')

        path = (os.path.dirname(__file__) + "/Data/" + date_time)
        print(path)
        f = open(path, mode='w+',encoding="utf-8", newline="")
        f_csv_writer = writer(f,delimiter=",")
        f_csv_writer.writerow("row_index, row_time, outputvalue, force")
        print("Values are saved to: ", path)

        hx711.reset()   #Zuruecksetzen
        time.sleep(1)
        hx711.zero()    #Offset eliminieren
        hx711.set_scale_ratio(scaleRatio)
        
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
            print("Output: ", outputvalue, " Force: ", force)

            #Erstelle Inhalt der naechsten Reihe:
            row_time = datetime.now().strftime("%H/%M/%S")
			print(rwo_time)
            row_content = row_index, row_time, outputvalue, force
            row_index +=1
            print(row_content)
            #Schreibe die naeste Reihe:
            f_csv_writer.writerow(row_content)

            #Pruefe Warping Bedingung:
            if force>limit:
                nowarping = False
                return True        
                            
    except (KeyboardInterrupt, SystemExit): #Programm kann mit Ctrl + C angehalten werden
        print("Pfiat di Gott! :D")

    finally:
        f.close() # Schliesse Daten.txt
        GPIO.cleanup()