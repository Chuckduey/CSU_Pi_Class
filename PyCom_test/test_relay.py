# main.py -- put your code here!
import pycom
import time
from machine import *
i2c = I2C(0, I2C.MASTER, baudrate=100000)
while True:
    i2c.writeto(58,0x00)
    time.sleep(1)
    i2c.writeto(58,0x55)
    time.sleep(1)
    i2c.writeto(58,0xaa)
    time.sleep(1)
    i2c.writeto(58,0xff)
    time.sleep(1)
    i2c.writeto(60,0x00)
    time.sleep(1)
    i2c.writeto(60,0x55)
    time.sleep(1)
    i2c.writeto(60,0xaa)
    time.sleep(1)
    i2c.writeto(60,0xff)
    time.sleep(1)
