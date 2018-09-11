#!/usr/bin/python
 
from Tkinter import *
import Tkinter as tk
import spidev
import smbus
import time
import os
import math

# set up constants
mpl115a2_add = 0x60
convert_reg = 0x12
pressure_reg = 0x00
temp_reg = 0x02
a0_reg = 0x04
b1_reg = 0x06
b2_reg = 0x08
c12_reg = 0x0a
# globla coefficients
a0_coef = 0.0
b1_coef = 0.0
b2_coef = 0.0
c12_coef = 0.0

# open i2c bus 1
i2cbus=smbus.SMBus(1)

def read_2_bytes(addr,reg):
    b = i2cbus.read_i2c_block_data(addr,reg,2)
    res = (b[0] << 8) + b[1]
    if res > 32768:
        res = res - 65536
    return(res)

def read_10_bits(addr,reg):
    b = i2cbus.read_i2c_block_data(addr,reg,2)
    res = ((b[0] << 8) + b[1] )>> 6
    return(res)

def get_coef():
     global a0_coef, b1_coef, b2_coef, c12_coef
     a0_coef_i = read_2_bytes(mpl115a2_add,a0_reg)
     b1_coef_i = read_2_bytes(mpl115a2_add,b1_reg)
     b2_coef_i = read_2_bytes(mpl115a2_add,b2_reg)
     c12_coef_i = read_2_bytes(mpl115a2_add,c12_reg)
     a0_coef = a0_coef_i / 8.0
     b1_coef = b1_coef_i / 8192.0
     b2_coef = b2_coef_i / 16384.0
     c12_coef = c12_coef_i / 16777216.0

#     print a0_coef_i,a0_coef
#     print b1_coef_i,b1_coef
#     print b2_coef_i,b2_coef
#     print c12_coef_i,c12_coef

# Set up initial coefffficients

get_coef()
# Start conversion
i2cbus.write_byte_data(mpl115a2_add, convert_reg, 0x00)
time.sleep(.05)
p = read_10_bits(mpl115a2_add, pressure_reg)
t = read_10_bits(mpl115a2_add, temp_reg)
pres = a0_coef + ( b1_coef + c12_coef * t)*p + b2_coef*t
temp = (float(t) - 498.0) / (-5.35) + 25.0
pres = pres*65/1023.0 + 50.0
print 'pressure = ',pres,' KPa  Temp = ',temp," 'C"
