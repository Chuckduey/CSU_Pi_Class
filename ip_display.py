#
# Dipslays the IP address,  Host name and Gateway
import os
import socket
import time
from Tkinter import *
host = "None"
ipaddr = "None"
gateway = "None"
update = 3000

#
def update_ip():
     global clock
     gw = os.popen("ip -4 route show default").read().split()
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.connect((gw[2], 0))
     ipaddr = s.getsockname()[0]
     gateway = gw[2]
     host = socket.gethostname()
     s.close()
     clock.config(text="Host name = "+host+"\nIp Address = "+ ipaddr + "\nGateway =" + gateway, anchor="w")
     clock.after(update,update_ip)
     
def update_ip_nl():
     global clock
     gw = os.popen("ip -4 route show default").read().split()
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.connect((gw[2], 0))
     ipaddr = s.getsockname()[0]
     gateway = gw[2]
     host = socket.gethostname()
     s.close()
     clock.config(text="Host Name = "+host+"\nIp Address = "+ ipaddr + "\nGateway =" + gateway, anchor="w")

root = Tk ()
root.title("IP Adresses")
clock = Label(root, font=('times', 20, 'bold'),bg='green')
clock.pack(fill=BOTH, expand=1)
clock.config(text="Host name = "+host+"\nIp Address = "+ ipaddr + "\nGateway =" + gateway, anchor="w")
b=Button(root, text="Refresh", anchor=S, command=update_ip_nl)
b.pack()
#time.sleep(5)
# Main 
clock.after(update,update_ip)

# Start main loop
root.mainloop( )
