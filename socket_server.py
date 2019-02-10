#!/usr/bin/python           # This is socket_server.py file

import socket               # Import socket module
import sys


try:
     mys = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
except:
     print("Failed to generate socket")
     sys.exit()
port = 4321 
try:
   mys.bind(("", port))        # Bind to the port
except mys.error:
   print"failed to connect"
   sys.exit()

while True:
     print "listing port 4321"
     mys.listen(5)                 # Now wait for connection
     while True:
        conn, addr = mys.accept()
        print 'Got connection from', addr
        try:
           data = conn.recv(256)
           print data
        except:
            print "No Packets"
        conn.close()                # Close the connection
