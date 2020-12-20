#!/usr/bin/python3
from hx711 import HX711
import RPi.GPIO as GPIO
import time, csv, os
from csv import writer
from datetime import datetime
import numpy as np
import statusLEDs, Relais

def measure(scaleRatio=1, averageOfXValues = 20, limit = 15, path = "Data/def.csv"): 
    try:
        GPIO.setmode(GPIO.BCM)
        hx711 = HX711(dout_pin=5,pd_sck_pin=6, gain_channel_A=64,select_channel='A')
        print("Values are saved to: ", path)

        content = [["row tindex", "time", "outputvalue", "force"]]

        hx711.reset()   #Zuruecksetzen
        time.sleep(1)
        hx711.zero()    #Offset eliminieren
        hx711.set_scale_ratio(scaleRatio)
        
        #measurement:
        print("Now, I will read data in infinite loop. To exit press 'CTRL + C' two times ")
        print('Current value measured is: ')
        row_index = 0
        nowarping = True

        while nowarping:
            #Messe Werte:
            statusLEDs.lightLed("no_warping")
            outputvalue = hx711.get_weight_mean(averageOfXValues)
            force = round(((outputvalue-112.360606060606)/-197498.869696969696)*9.81 , 2)
            print("Output: ", outputvalue, " Force: ", force)

            #Erstelle Inhalt der naechsten Reihe:
            row_time = datetime.now().strftime("%H-%M-%S")
            row_content = np.asarray([row_index, row_time, outputvalue, force])
            content.append(row_content)
            np.savetxt(path, np.array(content), fmt='%s', delimiter=",", encoding ='utf-8')
            row_index +=1

            #Pruefe Warping Bedingung:
            if force>limit:
                nowarping = False
                return True        
                            
    except (KeyboardInterrupt, SystemExit): #Programm kann mit Ctrl + C angehalten werden
        print("Pfiat di Gott! :D")

    finally:
        GPIO.cleanup()
