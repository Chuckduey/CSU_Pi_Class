# boot.py -- run on boot-up
import pycom
import network
from network import WLAN
from machine import *
i2cexp_addrs = range(0x38,0x3f)
# Turn off blinking light make red for not conneced to network
pycom.heartbeat(False)
pycom.rgbled(0x110000)
# Find all the I2C Expanders and write them to FF
i2c = I2C(0, I2C.MASTER, baudrate=100000)
devs = i2c.scan()
for dev in devs:
    if dev in i2cexp_addrs:
        i2c.writeto(dev,0xff)
        print(dev)

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'DueyNet':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'DueyNet3295'), timeout=5000)
        print('WLAN connection succeeded!')
        pycom.rgbled(0x1100)
# Make Telnet and FTP more secure Change the password
server = network.Server()
server.deinit() # disable the server
# enable the server again with new settings
server.init(login=('Chiller', 'Fr@nken'), timeout=600)
