#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import sys


try:
     mys = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
except mys.error:
     print("Failed to generate socket")
     sys.exit()
port = 4321 
try:
   mys.bind(("", port))        # Bind to the port
except mys.error:
   print"failed to connect"
   sys.exit()

print "listing port 4321"
mys.listen(5)                 # Now wait for connection
while True:
   conn, addr = mys.accept()
   print 'Got connection from', addr
   data = conn.recv(200)
   print data
   conn.close()                # Close the connection
