# File to test all 4 buttons.
import RPi.GPIO as GPIO
import time
GP2 = 4
GP3 = 22
GP4 = 23
GP5 = 7
GP6 = 19
GP7 = 18
GP8 = 12
GP9 = 13
GP10 = 26
GP11 = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(GP8, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GP9, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GP10, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GP11, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GP2, GPIO.OUT)
GPIO.setup(GP3, GPIO.OUT)

while True:
	if(GPIO.input(GP8) == 0):
	  GPIO.output(GP2, GPIO.LOW)
          print("Button 1 pressed")
	if(GPIO.input(GP9) == 0 ):
	  GPIO.output(GP2, GPIO.HIGH)
          print("Button 2 pressed")
	if(GPIO.input(GP10) == 0 ):
	  GPIO.output(GP3, GPIO.HIGH)
          print("Button 3 pressed")
	if(GPIO.input(GP11) == 0 ):
	  GPIO.output(GP3, GPIO.LOW)
          print("Button 4 pressed")
GPIO.cleanup()



