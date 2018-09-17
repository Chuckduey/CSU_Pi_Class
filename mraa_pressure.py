# Distributed with a free-will license.

# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# MPL3115A2
# This code is designed to work with the MPL3115A2_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/products
#
# TK code added by Chuck Duey
import time
from Tkinter import *
import mraa
import smbus
import time
# MPL3115A2 Address mpl_addr
mpl_addr = 0x60
update = 3000
# Get I2C bus
bus = mraa.I2c(0)
bus.address(mpl_addr)
def get_data():
     # MPL3115A2 address, mpl_addr(0x60)
     # Select control register, 0x26(38)
     #		0xB9(185)	Active mode, OSR = 128, Altimeter mode
     bus.writeReg(0x26, 0xB9)
     # MPL3115A2 address, mpl_addr(96)
     # Select data configuration register, 0x13(19)
     #		0x07(07)	Data ready event enabled for altitude, pressure, temperature
     bus.writeReg(0x13, 0x07)
     # MPL3115A2 address, mpl_addr(96)
     # Select control register, 0x26(38)
     #		0xB9(185)	Active mode, OSR = 128, Altimeter mode
     bus.writeReg(0x26, 0xB9)

     time.sleep(1)

     # MPL3115A2 address, mpl_addr(96)
     # Read data back from 0x00(00), 6 bytes
     # status, tHeight MSB1, tHeight MSB, tHeight LSB, temp MSB, temp LSB
     data = bus.read(6)
#     print str(data)
     # Convert the data to 20-bits
     tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
     temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
     altitude = 3.28084*(tHeight / 16.0)
     cTemp = temp / 16.0
     fTemp = cTemp * 1.8 + 32

     # MPL3115A2 address, mpl_addr(96)
     # Select control register, 0x26(38)
     #		0x39(57)	Active mode, OSR = 128, Barometer mode
     bus.writeReg(0x26, 0x39)

     time.sleep(1)

     # MPL3115A2 address, mpl_addr(96)
     # Read data back from 0x00(00), 4 bytes
     # status, pres MSB1, pres MSB, pres LSB
     data = bus.read(4)

     # Convert the data to 20-bits
     pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
     pressure = (pres / 4.0) / 100.0

     # Output data to screen
     pressure = round(pressure,2)
     altitude = round(altitude,1)
     cTemp = round(cTemp,1)
     fTemp = round(fTemp,1)
     return([pressure, altitude, cTemp, fTemp])

def meas_disp():
     global clock,clock1
     out = get_data()    # Get data Pressure, Alt, Temp C and Temp F
     clock.config(text="Pressure = "+str(out[0]) + "mb  Altitude = "+str(out[1]) + " Feet")
     clock1.config(text="Temperature ="+str(out[2]) + "'C  Temperature = "+str(out[3]) + "'F")
     clock.after(update,meas_disp)
# Define Tk root
root = Tk ()
root.title("Pressure/Temp")
clock = Label(root, font=('times', 20, 'bold'),bg='green')
clock.pack(fill=BOTH, expand=1)
out = get_data()
clock.config(text="Pressure = "+str(out[0]) + "mb  Altitude = "+str(out[1]) + " Feet")
clock1 = Label(root, font=('times', 20, 'bold'), bg="green")
clock1.pack(fill=BOTH, expand=1)
clock1.config(text="Temperature ="+str(out[2]) + "'C  Temperature = "+str(out[3]) + "'F")
clock.after(update,meas_disp)

root.mainloop( )
# Clean up IO ports return to normal


