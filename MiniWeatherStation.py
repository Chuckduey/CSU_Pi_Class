#!/usr/bin/python3

import json
import sys
import time
import datetime

# libraries
import sys

from sense_hat import SenseHat

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 10


sense = SenseHat()
sense.clear()		
print ('Press Ctrl-C to quit.')
worksheet = None
while True:

	# Attempt to get sensor reading.
	temp = sense.get_temperature()
	temp = round(temp, 1)
	humidity = sense.get_humidity()
	humidity = round(humidity, 1)
	pressure = sense.get_pressure()
	pressure = round(pressure, 1)
	
	# 8x8 RGB
	sense.clear()
	info = 'Temp=' + str(temp) + "'C  Hum=" + str(humidity) + '%  Pres=' + str(pressure) + 'mBar'
	sense.show_message(info, text_colour=[255, 0, 0])
	
	# Print
	print( "Temperature (C): ", temp)
	print( "Humidity: ", humidity)
	print( "Pressure: ", pressure, "\n")
	time.sleep(FREQUENCY_SECONDS)

