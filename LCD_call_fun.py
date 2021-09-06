# Distributed with a free-will license.
#
#This is basic functions for the LCD display 
import time
import smbus
import LCD_Fun as LCD

LCD.LCD_init()   # Initialize the LCD
while True:
	instr = raw_input(" Input Text for display >")
	LCD.LCD_clear()
	if len(instr) <= 20:
		LCD.LCD_print(instr)
	else:
		LCD.LCD_print(instr[:20])
		

