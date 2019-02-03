import socket
import sys
import smbus
import time
import RPi.GPIO as GPIO
import LCD_Fun as LCD
from adcPythonC import *

# Define socket to be used for web page  80 is a normal web socket, but may be used for other things in the system.
HOST, PORT = '', 80

# Define the standard web response for a web page
# MPL3115A2 Address mpl_addr
mpl_addr = 0x60
update = 3000
GP2 = 4
GP3 = 22
GP4 = 23
GP5 = 7
GP6 = 19
GP7 = 18
GP8 = 25
GP9 = 13
GP10 = 26
GP11 = 16
adc_channel = 7 # Input pin for ADC Channel

buttons = [GP8,GP9,GP10,GP11]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
for button in buttons:
    GPIO.setup(button, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(GP2, GPIO.OUT)
GPIO.setup(GP3, GPIO.OUT)
# Open I2C bus
bus = smbus.SMBus(1)
relay = 0   # Set relay off

web_response = """\
HTTP/1.1 200 OK

"""

# Title block for the web page
web_header = '<html><body><head><meta http-equiv="refresh" content="10"></head><center> <font color="blue"> <h1>Project Board Readings</h1>\n'

# Function to send the data to the socket.  Will close the connection if there is an error
def send_web(string_data):
        try:
           client_connection.sendall(string_data.encode('utf8'))
        except:
           client_connection.close()
           print("Web Exception")
def get_data():
     bus.write_byte_data(mpl_addr, 0x26, 0xB9)
     bus.write_byte_data(mpl_addr, 0x13, 0x07)
     bus.write_byte_data(mpl_addr, 0x26, 0xB9)
     time.sleep(1)  # Must wait 1 second for conversion to complete
     data = bus.read_i2c_block_data(mpl_addr, 0x00, 6)
     tHeight = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
     temp = ((data[4] * 256) + (data[5] & 0xF0)) / 16
     altitude = 3.28084*(tHeight / 16.0)
     cTemp = temp / 16.0
     fTemp = cTemp * 1.8 + 32
     bus.write_byte_data(mpl_addr, 0x26, 0x39)
     time.sleep(1) # must wait 1 second for conversion to complete
     data = bus.read_i2c_block_data(mpl_addr, 0x00, 4)
     # Convert the data to 20-bits
     pres = ((data[1] * 65536) + (data[2] * 256) + (data[3] & 0xF0)) / 16
     pressure = (pres / 4.0) / 100.0
     pressure = round(pressure,2)
     altitude = round(altitude,1)
     cTemp = round(cTemp,1)
     fTemp = round(fTemp,1)
     return([pressure, altitude, cTemp, fTemp])

# Get I2C bus
bus = smbus.SMBus(1)
LCD.LCD_init()
# Open up a socket server port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print( 'Serving HTTP on port %s ...' % PORT)

while True:
    if(relay == 0):  # Note Low = on and High = off
        GPIO.output(GP2, GPIO.HIGH)
    if(relay  == 1 ):
        GPIO.output(GP2, GPIO.LOW)
# open socket
    client_connection, client_address = listen_socket.accept()
    LCD.LCD_clear()
    LCD.LCD_print(client_address[0])
    print 'Client Address = ',client_address[0]
# wait for response
    request = client_connection.recv(1024)
    print(request)
# Change response from bytes to regular text
    request_dec = request.decode()
# Look at the various lines coming back.  See if it is a GET or POST  If it is a POST look for our data
    headers_alone = request_dec.split('\r\n')
	# Find out what type of request it is POST = data coming back.  GET is a regular request.
    if (headers_alone[0].find('POST') > -1):
        print('Found Post Request')
        out_test = request_dec.find('logout=Logout')
        if out_test > 1:
            print('Exiting Program')
            send_web(web_response)
            send_web("<html><body><center> <font color='red'> <h1>Logging Out...Good Bye</h1><br>\n")
            client_connection.close()
            listen_socket.close()
            sys.exit()
        out_test = request_dec.find('On=on')
        if out_test > 1:
            relay = 1
            print("got On request")
            GPIO.output(GP2, GPIO.LOW)
        out_test = request_dec.find('Off=off')
        if out_test > 1:
            relay = 0
            print("Got off request")
            GPIO.output(GP2, GPIO.HIGH)
# For both post and get respond with standard HTTP OK and send Header
    if (headers_alone[0].find('GET') > -1) | (headers_alone[0].find('POST') > -1):
        print("Got GET request")
        out = get_data()
        tempa = round(100*(adcRead(adc_channel) * 3.3/4095.0 -0.5),2)
        send_web(web_response)
        send_web(web_header)
        send_web("<h3>MPL3115A2 Readings<br>")
        send_web("Pressure = "+str(out[0]) + "mb  Altitude = "+str(out[1]) + " Feet<br>")
        send_web("Temperature ="+str(out[2]) + "'C  Temperature = "+str(out[3]) + "'F<br></h3>")
        send_web("<h2>TMP36 Reading = "+str(tempa)+"'C  "+str(round(tempa*9/5.0 +32,2))+"'F </h2>")  
        send_web("<font color='black'><h2> Relay Status = ")
        if(relay == 0 ):
            send_web("<font color='red'> Off<br><font color='black'>")
        if(relay == 1 ):
            send_web("<font color='green'> On<br><font color='black'>")
        send_web("Button Status</h2><h3>")
        but_number = 1
        for button in buttons:
            if(GPIO.input(button) == 0):
                send_web(" Button "+str(but_number)+":<font color='green'> On  <font color='black'>")
            else:
                send_web(" Button "+str(but_number)+":<font color='blue'> Off  <font color='black'>")
            but_number += 1
        send_web('<br><br>Set Relay<br><form method="post">\n')
        send_web('<input type="submit" name="On" value="on">')
        send_web('<input type="submit" name="Off" value="off"></p>\n')
        send_web('<input type="submit" name="logout" value="Logout"></form></p>\n')
    else:
        print("got unknown")
        print(request_dec)
    client_connection.close()
