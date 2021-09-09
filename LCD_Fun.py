#!/usr/bin/python3
# Distributed with a free-will license.
#
#This is basic functions for the LCD display 
import time
import smbus
LCD_Addr = 0x3E
# Get I2C bus
bus0 = smbus.SMBus(0)

def LCD_home():
        buf = [0x00,0x02];
        bus0.write_i2c_block_data(LCD_Addr,0,buf)  #Set to Home


def LCD_print(str):
	buf1=[0x00,0x80]
	bus0.write_i2c_block_data(LCD_Addr,0,buf1)
	bus0.write_i2c_block_data(LCD_Addr,0x40,[ord(c) for c in str])

def LCD_init():

   init1 = [0x00,0x38]
   init2 = [0x00, 0x39, 0x14,0x74,0x54,0x6f,0x0c,0x01]
   # 2 lines 8 bit 3.3V Version
   bus0.write_i2c_block_data(LCD_Addr,0,init1)
   bus0.write_i2c_block_data(LCD_Addr,0,init2)


def LCD_clear():
        buf = [0x00,0x01];
        bus0.write_i2c_block_data(LCD_Addr,0,buf)  #Clear LCD



