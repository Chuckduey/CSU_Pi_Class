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
button1 = 23
button2 = 24
led1 = 25
led2 = 26
# Set blink rate for global in ms and blank state
led_pwm = 50
led_state = OFF

#Set up the GPIO ports
GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(led1, GPIO.OUT)
GPIO.setup(led2, GPIO.OUT)
led1_pwm = GPIO.PWM(led1,400)
led2_pwm = GPIO.PWM(led2,400)
led1_pwm.start(led_pwm)
led2_pwm.start(led_pwm)

def pwmChange(channel):
     global led_pwm,clock
     if channel == button1:
          if led_pwm > 0:
              led_pwm -= 5
     if channel == button2:
          if led_pwm < 100:
              led_pwm += 5
     led1_pwm.ChangeDutyCycle(led_pwm)
     led2_pwm.ChangeDutyCycle(100-led_pwm)
     clock.config(text="  LED PWM% = "+str(led_pwm))
# Define Tk root
root = Tk ()
root.title("PWM LED")
clock = Label(root, font=('times', 20, 'bold'),bg='green')
clock.pack(fill=BOTH, expand=1)
clock.config(text="  LED PWM% = "+str(led_pwm))

# Main 
# Set up events
GPIO.add_event_detect(button1, GPIO.RISING, callback=pwmChange, bouncetime=300)
GPIO.add_event_detect(button2, GPIO.RISING, callback=pwmChange, bouncetime=300)
# Start main loop
root.mainloop( )
# Clean up IO ports return to normal
GPIO.cleanup()
