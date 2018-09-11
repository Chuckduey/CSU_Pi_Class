#!/usr/bin/python
 
from Tkinter import *
import Tkinter as tk
import spidev
import smbus
import time
import os
import math

# Thermistor constants
Bcoef = 3950.001
To = 298.15
Ro = 10000

eeprom_file="/proc/device-tree/hat/custom_0a"  # location of primary eeprom file
sensor_set=[]   # initialize sensor array
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)   # for ADC
spi1 = spidev.SpiDev()
spi1.open(0,1)  #for DAC

# Open I2C bus
i2cbus=smbus.SMBus(1)
relay1 = 0x39
relay2 = 0x3e
pwm1 = 0x20

# Initialize the relays and pwm
i2cbus.write_byte(relay1,0xff)
i2cbus.write_byte(relay2,0xff)
i2cbus.write_byte_data(pwm1,0x01,0x00)   # set blink state 0 to Low Z
i2cbus.write_byte_data(pwm1,0x03,0x00)   # Set to outputs
i2cbus.write_byte_data(pwm1,0x09,0xff)   # set blink state 1 to High Z
i2cbus.write_byte_data(pwm1,0x0e,0xf8)   # Set Duty Cycle to 8/15ths and O8 to 8/15ths
i2cbus.write_byte_data(pwm1,0x0f,0x03)   # turn on blink/pwm
i2cbus.write_byte_data(pwm1,0x10,0xff)   # Set to outputs 0 and 1 to off
i2cbus.write_byte_data(pwm1,0x11,0xff)   # Set to outputs 2 and 3 to off
i2cbus.write_byte_data(pwm1,0x12,0xff)   # Set to outputs 4 and 5 to off
i2cbus.write_byte_data(pwm1,0x13,0xff)   # Set to outputs 6 and 7 to off

class sensor_channel:
	def __init__(self,channel,offset=0,gain=1,units="bits",places=2):
		self.channel=channel
		self.offset=offset
		self.gain=gain
		self.units=units
		self.raw=0
		self.value=float(0.0)
		self.places=places
		self.string=str(self.value) + " " + units

	def update(self):
		raw_code=ReadChannel(self.channel)
		self.raw=raw_code
		self.value=round((raw_code+self.offset)/float(self.gain),self.places)
		if self.places == 0:
			self.value = int(self.value)
		self.string=str(self.value) + " " + self.units


class dac_channel:
	def __init__(self,channel,gain=1,enable=1,value=0):
		self.channel = channel
		self.gain = gain
		self.enable = enable
		self.value = value
		self.lownib = value & 0xf
		self.midnib = (value & 0xf0) >> 4
		self.highnib = (value % 0xf00) >> 8
		self.maxnib = self.channel * 8 + self.gain * 2 + self.enable
		self.byte1 = self.maxnib * 16 + self.highnib
		self.byte2 = self.midnib * 16 + self.lownib
	def update(self):
		self.maxnib = self.channel * 8 + self.gain * 2 + self.enable
		self.byte1 = self.maxnib * 16 + self.highnib
		self.byte2 = self.midnib * 16 + self.lownib
		out = spi1.xfer2([self.byte1,self.byte2])
		
	def set(self,value):
		self.value = value & 0xfff
		self.lownib = value & 0xf
		self.midnib = (value & 0xf0) >> 4
		self.highnib = (value & 0xf00) >> 8
		self.maxnib = self.channel * 8 + self.gain * 2 + self.enable
		self.byte1 = self.maxnib * 16 + self.highnib
		self.byte2 = self.midnib * 16 + self.lownib
		
	def enab(self):
		self.enable = 1
		self.lownib = self.value & 0xf
		self.midnib = (self.value & 0xf0) >> 4
		self.highnib = (self.value % 0xf00) >> 8
		self.maxnib = self.channel * 8 + self.gain * 2 + self.enable
		self.byte1 = self.maxnib * 16 + self.highnib
		self.byte2 = self.midnib * 16 + self.lownib

	def dis_enab(self):
		self.enable = 0
		self.lownib = self.value & 0xf
		self.midnib = (self.value & 0xf0) >> 4
		self.highnib = (self.value % 0xf00) >> 8
		self.maxnib = self.channel * 8 + self.gain * 2 + self.enable
		self.byte1 = self.maxnib * 16 + self.highnib
		self.byte2 = self.midnib * 16 + self.lownib
				
	def set_gain(self,ga):
		self.gain = ga & 0x1
		
# Function to read SPI data from MCP3208 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0,0])
  data = ((adc[1]&3) << 10) + (adc[2] << 2) + ((adc[3] & 0xc0) >> 6)
# + adc[2] << 1 + ((adc[3]&0xc0) >> 6)
  return data

def therm_to_temp(vr,vt):
       # vt is thermistor voltage in codes
       a = 0.001129148
       b = 0.000234125
       c = 8.76741e-08
       # vr is reference / 2 in codes
       if vt < 1:
            return(-273)
       res = Ro*(vr*2/float(vt) - 1.0)
#       tmp = 1/(1/To+1/Bcoef*math.log(res/Ro))
       tmp = 1/(a + b*math.log(res) + c*math.pow(math.log(res),3))
       return(tmp - 273.15) 
#       return(res/1000)

def tick():
    global time1,sensor_set
    # get the current local time from the PC
    for sensor in sensor_set:
	   sensor.update()

    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    clock1.config(text= sensor_set[0].string + "  " + sensor_set[1].string + "   " + str(round(therm_to_temp(sensor_set[0].raw,sensor_set[1].raw),1)))
    clock2.config(text= str(round(therm_to_temp(sensor_set[0].raw,sensor_set[2].raw),1))+ " 'C  " +str(round(therm_to_temp(sensor_set[0].raw,sensor_set[3].raw),1)) +" 'C")
    clock3.config(text= sensor_set[4].string + "  " + sensor_set[5].string)
    clock4.config(text= sensor_set[6].string + "  " + sensor_set[7].string)
    clock.config(text=time2)
    time1 = time2
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    clock.after(200, tick)
	
def tog_relay1(n):
    global rel_state1,buttons1
    r_mask=2**(n)
    if rel_state1&r_mask:
       rel_state1 = rel_state1 & ~r_mask
       i2cbus.write_byte(relay1,rel_state1)
       buttons1[7-n]["bg"]="red"
    else: 
       rel_state1 = rel_state1 | r_mask
       i2cbus.write_byte(relay1,rel_state1)
       buttons1[7-n]["bg"]="grey"

def tog_relay2(n):
    global rel_state2,buttons2
    r_mask=2**(n)
    if rel_state2&r_mask:
       rel_state2 = rel_state2 & ~r_mask
       i2cbus.write_byte(relay2,rel_state2)
       buttons2[7-n]["bg"]="red"
    else: 
       rel_state2 = rel_state2 | r_mask
       i2cbus.write_byte(relay2,rel_state2)
       buttons2[7-n]["bg"]="grey"
	   
def int_inc(n):
    global inten,inten_max,button3
    i = 7-n
    if inten_max & 2**i:
        inten_max = inten_max - 2**i 
        inten[i] = 0x0f
    else:
        inten[i] -= 1
        if inten[i] < 0:
           inten_max = inten_max + 2**i
           inten[i] = 0x0f
    i2cbus.write_byte_data(pwm1,0x09,255-inten_max)
    i2cbus.write_byte_data(pwm1,0x10,inten[1]*16+inten[0])
    i2cbus.write_byte_data(pwm1,0x11,inten[3]*16+inten[2])
    i2cbus.write_byte_data(pwm1,0x12,inten[5]*16+inten[4])
    i2cbus.write_byte_data(pwm1,0x13,inten[7]*16+inten[6])
    buttons3[i]["text"]=hex(15-inten[i] + 16*(2**i & inten_max)/2**i)[2:]

inten=[0x0f]*8     # Initialize array with Min intenisty
inten_max = 0x00    # set max intensities to zero
rel_state1=0xff
rel_state2=0xff

dac0 = dac_channel(0,1,1,28)     # Initialize the DACs set to default
dac0.update()
dac1 = dac_channel(1,1,1,254)
dac1.update()

if os.path.isfile(eeprom_file):
   fp = open(eeprom_file)
   lines = fp.readlines()
   for i in range(0, 8):
      line=lines[i+1].strip().split()
      sensor = sensor_channel(i,int(line[0]),float(line[1]),line[2],int(line[3]))
      sensor_set.append(sensor)
   fp.close()
else:
	print'The hardway!!!/n'
	sensor = sensor_channel(0,0,1,'Bits',0)
	sensor_set.append(sensor)
	sensor = sensor_channel(1,0,1,'Bits',0)
	sensor_set.append(sensor)
	sensor = sensor_channel(2,0,1,"'C",1)
	sensor_set.append(sensor)
	sensor = sensor_channel(3,0,1,"'C",1)
	sensor_set.append(sensor)
	sensor = sensor_channel(4,-1000,20,"'C",1)
	sensor_set.append(sensor)
	sensor = sensor_channel(5,-711,11.11,"'F",1)
	sensor_set.append(sensor)
	sensor = sensor_channel(6,-711,11.11,"'F",1)
	sensor_set.append(sensor)
#	sensor = sensor_channel(7,0,1,"CO ppb",0)
	sensor = sensor_channel(7,-711,11.11,"'F",1)
	sensor_set.append(sensor)
def dac_inc(channel,factor):
	global dac0, dac1, buttons4, buttons5
	if channel == 1:
		dac1.set(dac1.value+factor)
		dac1.update()
#		print dac1.value
		buttons5[2]["text"]=hex(dac1.highnib)[2:]
		buttons5[3]["text"]=hex(dac1.midnib)[2:]
		buttons5[4]["text"]=hex(dac1.lownib)[2:]
	else:
		dac0.set(dac0.value+factor)
		dac0.update()
#		print dac0.value
		buttons4[2]["text"]=hex(dac0.highnib)[2:]
		buttons4[3]["text"]=hex(dac0.midnib)[2:]
		buttons4[4]["text"]=hex(dac0.lownib)[2:]

def dac_ga(channel):
	global dac0, dac1, buttons4, buttons5
	if channel == 1:
		dac1.set_gain(dac1.gain+1)
		dac1.update()
		buttons5[1]["text"]="G=" + str(dac1.gain)
	else:
		dac0.set_gain(dac0.gain+1)
		dac0.update()
		buttons4[1]["text"]="G=" + str(dac0.gain)

def dac_ena(channel):
	global dac0, dac1, buttons4, buttons5
	if channel == 1:
		if dac1.enable:
			dac1.dis_enab()
			bcolor = "grey"
		else:
			dac1.enab()
			bcolor = "red"
		dac1.update()
		buttons5[0]["text"]=str(dac1.enable)
		for b in buttons5:
			b["bg"] = bcolor
	else:
		if dac0.enable:
			dac0.dis_enab()
			bcolor = "grey"
		else:
			dac0.enab()
			bcolor = "red"
		dac0.update()
		buttons4[0]["text"]=str(dac0.enable)
		for b in buttons4:
			b["bg"] = bcolor

root = Tk()
root.title("SKE ADC DAC Relay")
time1 = ''
frame = Frame(root, bd=2, width=300, height=400, bg="green")
frame.grid(column=0, row=0)
clock = Label(frame, font=('times', 14), bg="green")
clock.grid(row=1, column=0, columnspan=8)
clock1 = Label(frame, font=('times', 14), bg="green")
clock1.grid(row=2, column=0, columnspan=8)
clock2 = Label(frame, font=('times', 14), bg="green")
clock2.grid(row=3, column=0, columnspan=8)
clock3 = Label(frame, font=('times', 14), bg="green")
clock3.grid(row=4, column=0, columnspan=8)
clock4 = Label(frame, font=('times', 14), bg="green")
clock4.grid(row=5, column=0, columnspan=8)
buttons1=[]
buttons2=[]
buttons3=[]
buttons4=[]
buttons5=[]
frame.grid(column=0, row=7)
for i in range(8):
     button=Button(frame, bg="grey", text=str(7-i), command=lambda i=7-i: tog_relay1(i))
     button.grid(row=6, column=i)
     buttons1.append(button)
for i in range(8):
     button2=Button(frame, bg="grey", text=hex(7-i)[2:], command=lambda i=7-i: tog_relay2(i))
     button2.grid(row=7, column=i)
     buttons2.append(button2)
for i in range(8):
     button3=Button(frame, bg="grey", text=str(15-inten[i]), command=lambda i=7-i: int_inc(i))
     button3.grid(row=8, column=7-i)
     buttons3.append(button3)
button=Button(frame, bg="red", text=str(dac0.enable), command=lambda i=0: dac_ena(i))
button.grid(row=9, column=0)
buttons4.append(button)
button=Button(frame, bg="red", text=str(dac1.enable), command=lambda i=1: dac_ena(i))
button.grid(row=10, column=0)
buttons5.append(button)
 
button=Button(frame, bg="red", text="G=" + str(dac0.gain), command=lambda i=0: dac_ga(i))
button.grid(row=9, column=1, ipadx=6, columnspan=2)
buttons4.append(button)
button=Button(frame, bg="red", text="G=" + str(dac1.gain), command=lambda i=1: dac_ga(i))
button.grid(row=10, column=1, ipadx=6, columnspan=2)
buttons5.append(button)

button=Button(frame, bg="red", text=hex(dac0.highnib)[2:], command=lambda i=0: dac_inc(i,256))
button.grid(row=9, column=3)
buttons4.append(button)
button=Button(frame, bg="red", text=hex(dac1.highnib)[2:], command=lambda i=1: dac_inc(i,256))
button.grid(row=10, column=3)
buttons5.append(button)

button=Button(frame, bg="red", text=hex(dac0.midnib)[2:], command=lambda i=0: dac_inc(i,16))
button.grid(row=9, column=4)
buttons4.append(button)
button=Button(frame, bg="red", text=hex(dac1.midnib)[2:], command=lambda i=1: dac_inc(i,16))
button.grid(row=10, column=4)
buttons5.append(button)

button=Button(frame, bg="red", text=hex(dac0.lownib)[2:], command=lambda i=0: dac_inc(i,1))
button.grid(row=9, column=5)
buttons4.append(button)
button=Button(frame, bg="red", text=hex(dac1.lownib)[2:], command=lambda i=1: dac_inc(i,1))
button.grid(row=10, column=5)
buttons5.append(button)

rel_state1=0xff
rel_state2=0xff

tick()
root.mainloop( )
