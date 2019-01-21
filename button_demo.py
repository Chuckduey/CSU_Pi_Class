#
# Added Tkinter interface Chuck Duey 8/20/2015
# Dual LED 9/24/2016 Chuck Duey
# Import the modules
import RPi.GPIO as GPIO
import time
from Tkinter import *

# Define our statics
ON = 1
OFF = 0
# Define our pin usage:
button1 = 25 
button2 = 13
led1 = 4
led2 = 23
# Set blink rate for global in ms and blank state
led_blink_rate = 600
led_state = OFF

#Set up the GPIO ports
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)

def led_blink():
     global led_state,led_blink_rate,led1,led2
     if led_state == ON:
          led_state = OFF
     else:
          led_state = ON
     GPIO.output(led1,led_state)
     GPIO.output(led2,1-led_state)
     clock.after(led_blink_rate/2,led_blink)

def blinkChange(channel):
     global led_blink_rate,clock
     if channel == button1:
          if led_blink_rate > 50:
              led_blink_rate -= 50
     if channel == button2:
          if led_blink_rate < 2000:
              led_blink_rate += 100
     clock.config(text="LED Blink Rate = "+str(led_blink_rate))
# Define Tk root
root = Tk ()
root.title("Button Demo")
clock = Label(root, font=('times', 20, 'bold'),bg='green')
clock.pack(fill=BOTH, expand=1)
clock.config(text="LED Blink Rate = "+str(led_blink_rate))

# Main 
# Set up events
GPIO.add_event_detect(button1, GPIO.RISING, callback=blinkChange, bouncetime=300)
GPIO.add_event_detect(button2, GPIO.RISING, callback=blinkChange, bouncetime=300)
clock.after(led_blink_rate,led_blink)
# Start main loop
root.mainloop( )
# Clean up IO ports return to normal
GPIO.cleanup()
