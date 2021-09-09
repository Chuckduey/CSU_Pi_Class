#!/usr/bin/python3
import socket
import sys
import smbus
import time
import time
import board
import busio
import adafruit_sgp30
from sense_hat import SenseHat
from adafruit_pm25.i2c import PM25_I2C
import adafruit_scd30
import threading


station_alt = 5300 # Station altitude in feet for pressure correction
# Define socket to be used for web page  80 is a normal web socket, but may be used for other things in the system.
HOST, PORT = '', 1080
# I2C channel 1 primary I2C bus
channel = 1
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)  # Adafruit IO
bus = smbus.SMBus(channel) # Normal smbus

reset_pin = None

# Ozone Sensor constants
# mode
measure_mode_auto = 0x00

# const
mode_register = 0x03
read_ozone_data_register = 0x04
auto_read_data = 0x00 
AUTO_data_high_eight_bits = 0x09



# Ozone Sensor - 0x70 - 0x71 - 0x72 - 0x73 ( default )
address = 0x73

# variables
OCOUNT = 100
collect_number = 20 # numbers of read 1-100



# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
sgp30.set_iaq_baseline(0x8926, 0x8de2)
try:
   pm25 = PM25_I2C(i2c, reset_pin)
   found_pm25 = True
   print("Found Sensor")
except:
   found_pm25 = False
   print("Did not find PM25 Sensor")
try:
   scd = adafruit_scd30.SCD30(i2c)
   found_CO2 = True
   print("Found CO2 Sensor")
   co2_data =0.0
except:
   found_CO2 = False
   print("Did not find SCD30 CO2 Sensor")
try:
   bus.write_byte_data(address, mode_register, measure_mode_auto)
   found_OZ = True
   print("Found Ozone Sensor")
   oz_data = 0.0
except:
   found_OZ = False
   print("Did not find Ozone Sensor")

sense = SenseHat()
sense.clear()	

web_response = """\
HTTP/1.1 200 OK

"""

# Title block for the web page
web_header = '<html><body><head><meta http-equiv="refresh" content="10"></head><center> <font color="blue"> <h1>I2C Environmental Readings</h1>\n'

# Function to send the data to the socket.  Will close the connection if there is an error
def send_web(string_data):
        try:
           client_connection.sendall(string_data.encode('utf8'))
        except:
           client_connection.close()
           print("Web Exception")
def Data_engine():
     global aqdata,air_data,co2_data,oz_data
     while True: 
         tvoc = sgp30.TVOC
         eco2 = sgp30.eCO2
         cTemp = sense.get_temperature()
         fTemp = cTemp * 1.8 + 32
         pressure = round(sense.get_pressure() + station_alt/30,1)
         humidity = round(sense.get_humidity(),1)
         cTemp = round(cTemp,1)
         fTemp = round(fTemp,1)
         air_data = [pressure, humidity, cTemp, fTemp, eco2, tvoc]
         if found_pm25: 
               try:
                  aqdata = pm25.read()
               except:
                  print("Particle sensor problem")
         if found_CO2:
             if scd.data_available:
                   co2_data = round(scd.CO2,2)        
         if found_OZ:
             oz_data = round(read_ppb()*1000,1)
def read_ppb():
    global bus
    OzoneData = [0x00] * OCOUNT 


    # SetModes -> measure_mode_auto
    bus.write_byte_data(address, mode_register, measure_mode_auto)

    # ReadOzoneData
    for j in range(collect_number):
        # read active data in active mode
        try:
           bus.write_byte_data(address, read_ozone_data_register, auto_read_data)
           time.sleep(0.1);   
        # first request once
           bus.write_byte(address, AUTO_data_high_eight_bits)
           time.sleep(0.1)
        # then read 2 bytes from the sensor

           rxbuf = bus.read_i2c_block_data(address, AUTO_data_high_eight_bits, 2)
        except:
           rxbuf = [0,0]
           print("I2C Fail setting data to 0.0")
        
        # convert byte in a word
        O3_ppb = (rxbuf[0] << 8) + rxbuf[1]
        # send back the converted ppb to ppm
        OzoneData[j] = O3_ppb/1000

    # getAverageNum
    Ozone = 0
    for i in range(collect_number):
        Ozone = Ozone + OzoneData[i]
    # average
    Ozone_ppm = Ozone/collect_number

    # check if the result is valid or not
    if Ozone_ppm >= 0 or Ozone_ppm < 60:
        return Ozone_ppm
    else:
        return -1



# Open up a socket server port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print( 'Serving HTTP on port %s ...' % PORT)

try:
   threading._start_new_thread(Data_engine,())
except (KeyboardInterrupt, SystemExit):
   cleanup_stop_thread()
   sys.exit()
   
   
while True:

# open socket
    client_connection, client_address = listen_socket.accept()
  
    print ('Client Address = ',client_address[0])
# wait for response
    try:

        request = client_connection.recv(1024)
    except:
        request = "Null"
    print(request)
# Change response from bytes to regular text
    try:
        request_dec = request.decode()
    except:
        request_dec = "Bad Decode"
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

# For both post and get respond with standard HTTP OK and send Header
    if (headers_alone[0].find('GET') > -1) | (headers_alone[0].find('POST') > -1):
        print("Got GET request")
        # air_data = get_data()   # Data Engine will collect the data.
        send_web(web_response)
        send_web(web_header)
        send_web("<h3>Current Air Readings<br>")
        send_web("Pressure = "+str(air_data[0]) + " mBar Humidity = "+str(air_data[1]) + " %<br>")
        send_web("Temperature ="+str(air_data[2]) + "'C  Temperature = "+str(air_data[3]) + "'F<br></h3>")
        send_web("<h2>ECO2 = "+str(air_data[4])+" ppm  TVOC = "+str(air_data[5])+"ppb </h2>")
        if found_CO2:
           send_web("<h2>CO2 = "+str(co2_data)+" ppm</h2>")
        if found_OZ:
           send_web("<h2>Ozone = "+str(oz_data)+" ppb</h2>")
        if found_pm25: 
           try:
              aqdata = pm25.read()
           except:
              send_web("<h3>No PM25 Sensor</h3>")
           send_web("<h3>Concentration Units (standard)<br>")
           send_web("---------------------------------------<br>")
           send_web("PM 1.0: "+str(aqdata["pm10 standard"])+"   PM2.5: "+str(aqdata["pm25 standard"])+"   PM10: "+str(aqdata["pm100 standard"])+"<br>")
           send_web("Concentration Units (environmental)<br>")
           send_web("---------------------------------------<br>")
           send_web("PM 1.0: "+str(aqdata["pm10 env"])+"   PM2.5: "+str(aqdata["pm25 env"])+"   PM10: "+str(aqdata["pm100 env"])+"<br>")
           send_web("---------------------------------------<br>")
           send_web("Particles > 0.3um / 0.1L air: "+str(aqdata["particles 03um"])+"<br>")
           send_web("Particles > 0.5um / 0.1L air: "+str(aqdata["particles 05um"])+"<br>")
           send_web("Particles > 1.0um / 0.1L air: "+str(aqdata["particles 10um"])+"<br>")
           send_web("Particles > 2.5um / 0.1L air: "+str(aqdata["particles 25um"])+"<br>")
           send_web("Particles > 5.0um / 0.1L air: "+str(aqdata["particles 50um"])+"<br>")
           send_web("Particles > 10 um / 0.1L air: "+str(aqdata["particles 100um"])+"<br>")
           send_web("---------------------------------------</h3><br>")
        send_web('<br><br>Set Relay<br><form method="post">\n')
        send_web('<input type="submit" name="On" value="on">')
        send_web('<input type="submit" name="Off" value="off"></p>\n')
        send_web('<input type="submit" name="logout" value="Logout"></form></p>\n')
    else:
        print("got unknown")
        print(request_dec)
    client_connection.close()
