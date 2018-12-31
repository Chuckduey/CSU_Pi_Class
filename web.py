import socket
import sys

# Define socket to be used for web page  80 is a normal wbsocket, but may be used for other things in the system.
HOST, PORT = '', 88

# Define the standar web response for a web page
web_response = """\
HTTP/1.1 200 OK

"""

# Title block for the web page
web_header = "<html><body><center> <font color='blue'> <h1>Thermo Sensor Reading</h1><br>\n"

# Function to send the data to the socket.  Will close the connection if there is an error
def send_web(string_data):
        try:
           client_connection.sendall(string_data.encode('utf8'))
        except:
           client_connection.close()
           print("Web Exception")

# Open up a socket server port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print( 'Serving HTTP on port %s ...' % PORT)

# Replace temp with an actual sensor.
temp = 25.5
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)
    request_dec = request.decode()
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
    if (headers_alone[0].find('GET') > -1) | (headers_alone[0].find('POST') > -1):
        print("Got GET request")
        temp = 25.5
        send_web(web_response)
        send_web(web_header)
        send_web('<h3>The temp is = ' + str(temp) + "'C and the time is now <br></h3>")
        send_web('<form method="post">\n')
        send_web('<input type="submit" name="logout" value="Logout"></form></p>\n')

    else:
        print("got unknown")
        print(request_dec)
    client_connection.close()