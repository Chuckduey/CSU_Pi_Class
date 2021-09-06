#!/usr/bin/python3
import os
import sys
import subprocess

for k in range(1):
    outstr = ''
    for i in range(254):
       ip="192.168.5.%d" %(i)
       #print(ip)
       rep = os.system('fping -t 100 -q -c 1 ' + ip + ' > /dev/null 2>&1')
       if rep == 0:
           # arp list
           p = subprocess.Popen(['arp', '-n'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
           out, err = p.communicate()
           
           try:
              arp = [x for x in out.split('\n') if ip in x][0]
              #print(arp)
           except:
               #print(out)
               #print("\n")
               arp  = "None  None Not:Found"
    # this will print out the interface name
           outstr += " Host Up "+ip+" MAC = " + ' '.join(arp.split()).split()[2] + "\n"
      #     print("Host Up ",ip)
    os.system('clear')
    print(outstr)
