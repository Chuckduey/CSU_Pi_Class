import socket
import sys
# Define socket to be used for web page  80 is a normal web socket, but may be used for other things in the system.
HOST, PORT = '', 80

# Define the standard web response for a web page
web_response = """\
HTTP/1.1 200 OK

"""
web_line = '<html><h1>Hello World</h1></html>\n'
# Open up a socket server port
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print( 'Serving HTTP on port %s ...' % PORT)
while True:
	# open socket
    client_connection, client_address = listen_socket.accept()
# wait for response
    request = client_connection.recv(1024)
    print(request)
    try:
       client_connection.sendall(web_response.encode('utf8'))
       client_connection.sendall(web_line.encode('utf8'))
    except:
       client_connection.close()
       print("Web Exception")
    client_connection.close()
