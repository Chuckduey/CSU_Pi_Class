import socket
import sys
import math
from machine import *
import time
import re

Bcoef = 3950.001
To = 298.15
Ro = 10000
Vref = 1.1
ncodes=4096
HOST, PORT = '', 80
web_response = """\
HTTP/1.1 200 OK

"""
web_header = "<html><body><center> <font color='blue'> <h1>Franken Chiller Sensors</h1><br>\n"
# Intital Realy word
relay_word = 0xffff
relay1 = 0x3a
relay2 = 0x3c
# Initialize ADC
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


def send_web(string_data):
        try:
           client_connection.sendall(string_data.encode('utf8'))
        except:
           client_connection.close()
           print("Web Exception")

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print( 'Serving HTTP on port %s ...' % PORT)

while True:
    i2c.writeto(relay1,relay_word & 0xff)
    i2c.writeto(relay2,relay_word>>8 & 0xff)
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    #print(request)
    request_dec = request.decode()
    headers_alone = request_dec.split('\r\n')
    for txt in headers_alone:
        print(txt)
    if (headers_alone[0].find('POST') > -1):
        print('Found Post Request')
        pos=request_dec.find('Relay_Word=0x')
        try:
            relay_word=int(request_dec[pos+11:],16)
        except:
            print('Conversion poblem')
    if (headers_alone[0].find('GET') > -1) | (headers_alone[0].find('POST') > -1):
        print("Got GET request")
        send_web(web_response)
        send_web(web_header)
        send_web('<h3>ADC channel 0 = ' + str(adc0.value()) + '  ADC channel 1 = ' + str(adc1.value())+ ' <br>\n')
        send_web('ADC channel 2 = ' + str(adc2.value()) + '  ADC channel 3 = ' + str(adc3.value())+ ' <br>\n')
        send_web('ADC channel 4 = ' + str(adc4.value()) + '  ADC channel 5 = ' + str(adc5.value())+ ' <br>\n')
        send_web('ADC channel 6 = ' + str(adc6.value()) + '  ADC channel 7 = ' + str(adc7.value())+ ' <br></h3>\n')
        temp1 = therm_to_temp(adc0.value(),adc1.value())
        temp2 = therm_to_temp(adc0.value(),adc2.value())
        temp3 = therm_to_temp(adc0.value(),adc3.value())
        temp4 = code_to_temp(adc4.value())
        send_web('<br><br><h2>Temp 1 = ' + str(temp1)+ "'C  Temp 2 = " + str(temp2) + "'C <br>\n")
        send_web('Temp 3 = ' + str(temp3) + "'C  Temp 4 = " + str(temp4) + "'C <br><br></h2>\n")
        send_web('Relay Word = ' + hex(relay_word))
        send_web('<form method="post">\n')
        send_web('<p>Relay Word:<input type="text" name="Relay_Word" size="20"/></p>\n')
        send_web('<p><input type="submit" value="Update"/>')
        send_web('<input type="submit" name="logout" value="Logout"></p></form>\n')
    client_connection.close()
