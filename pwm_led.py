import RPi.GPIO as GPIO
import time

led = 12
duty = 50.0
#Set up the GPIO ports
GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)
led_pwm = GPIO.PWM(led,400)
led_pwm.start(duty)
step = 1.0
while True:
     duty += step
     if duty < 0:
        step = 1.0
        duty = 0
     if duty > 100:
        step = -1.0
        duty = 100
     led_pwm.ChangeDutyCycle(duty)
     time.sleep(.03)
GPIO.cleanup()

