# From Website - http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
import time
while True:
	if(GPIO.input(23) ==1):
	  GPIO.output(25, GPIO.HIGH)
          print("Button 1 pressed")
	if(GPIO.input(24) == 0 ):
	  GPIO.output(26, GPIO.HIGH)
          print("Button 2 pressed")
	if(GPIO.input(23) == 0):
	  GPIO.output(25, GPIO.LOW)
	if(GPIO.input(24) == 1):
	  GPIO.output(26, GPIO.LOW)
GPIO.cleanup()



