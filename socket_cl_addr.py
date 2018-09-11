#!/usr/bin/python           # This is socket_client.py file

import socket               # Import socket module
import sys

try:
     mys = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
except mys.error:
     print("Failed to generate socket")
     sys.exit()
port = 4321 
#addr = "127.0.0.1"
addr = raw_input('Enter address ')
if len(addr) < 8:
    addr = "127.0.0.1"
try:
   ainfo = socket.getaddrinfo(addr,port)
   mys.connect(ainfo[0][4])
except mys.error:
   print"failed to connect"
   sys.exit()
data = raw_input('Enter Data ')
mys.sendall(data)
mys.close()
