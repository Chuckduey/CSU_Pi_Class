# From Web page - http://www.rpiblog.com/2012/09/using-gpio-of-raspberry-pi-to-blink-led.html
import RPi.GPIO as GPIO
import time
out_pin1 = 4
out_pin2 = 23
# blinking function
def blink(pin):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(.3)
        GPIO.output(pin,GPIO.LOW)
        time.sleep(.31)
        return
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# set up GPIO output channel
GPIO.setup(out_pin1, GPIO.OUT)
GPIO.setup(out_pin2, GPIO.OUT)
# blink "out_pin" 20 times
for i in range(0,20):
        blink(out_pin1)
        blink(out_pin2)
GPIO.cleanup() 
