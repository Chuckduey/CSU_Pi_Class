
import pycom
import time
import socket
import sys
import math
from machine import *
from network import WLAN
port = 4321
addr = '192.168.10.25'
# Thermistor constants
Bcoef = 3950.001
To = 298.15
Ro = 10000
Vref = 1.1
ncodes=4096

pycom.heartbeat(False)
pycom.rgbled(0x111100)
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'DueyNet':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'DueyNet3295'), timeout=5000)
        print('WLAN connection succeeded!')
time.sleep(10)
adc = ADC(0)
i2c = I2C(0, I2C.MASTER, baudrate=100000)
adc0 = adc.channel(pin='P13', attn=ADC.ATTN_11DB)
adc1 = adc.channel(pin='P14', attn=ADC.ATTN_11DB)
adc2 = adc.channel(pin='P15', attn=ADC.ATTN_11DB)
adc3 = adc.channel(pin='P16', attn=ADC.ATTN_11DB)
adc4 = adc.channel(pin='P17')
adc5 = adc.channel(pin='P18')
adc6 = adc.channel(pin='P19')
adc7 = adc.channel(pin='P20')
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
#       return(res/1000)`````````````````````````````
def code_to_temp(din):
    v=Vref*din/int(ncodes)
    return((v-.5)/.01)


while True:
    try:
         mys = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except mys:
         mys.close()
         print("Failed to generate socket")
         sys.exit()
    try:
         mys.connect(socket.getaddrinfo('192.168.10.25',4321)[0][4])
    except:
       mys.close()
       print("failed to connect")
       sys.exit()
#    i2c.writeto(58,0xaa)
#    out = i2c.readfrom(58,1)
    # print('out = ',out)
#    ref_res = adc0.value()
    temp1 = therm_to_temp(adc0.value(),adc1.value())
    temp2 = therm_to_temp(adc0.value(),adc2.value())
    temp3 = therm_to_temp(adc0.value(),adc3.value())
    temp4 = code_to_temp(adc4.value())
    temp5 = code_to_temp(adc5.value())
    temp6 = code_to_temp(adc6.value())
    temp7 = code_to_temp(adc7.value())

    print(temp1, temp2, temp3, temp4, temp5, temp6, temp7)
    strout = 'Therm1 = ' + str(temp1) + '\n' + 'Therm2 = ' + str(temp2) + '\n' + 'Therm3 = ' +  str(temp3) + '\n'
    strout = strout + 'Therm4 = ' + str(temp4) + '\n' + 'Therm5 = ' + str(temp5) + '\n' + 'Therm6 = ' +  str(temp6) + '\n' + 'Therm7 = ' +  str(temp7) + '\n'
    try:
        mys.sendall(bytes(strout, 'utf-8'))
    except:
        print("failed to send")
    mys.close()
    time.sleep(10)
