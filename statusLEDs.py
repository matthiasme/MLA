#!/usr/bin/python3
from gpiozero import LED

#Erstelle zwei LED Objekte
green = LED("GPIO16")
red = LED("GPIO26")
#Achtung unterschied PINs und GPIO

#Schalte LEDs je nach Status des Druckers
def lightLed(status):
    if status == "warping":
        red.on()
        green.off()
    elif status == "no_warping":
        green.on()
        red.off()
    else:
        green.blink()
        red.blink()
        







