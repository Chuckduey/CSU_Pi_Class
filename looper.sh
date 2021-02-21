#!/bin/bash
gpio mode 7 out  
#mraa-gpio set 7 output
while true; do  
    gpio write 7 1
#   mraa-gpio set 7 1
    sleep 0.5
    gpio write  7 0
#   mraa-gpio set 7 0
    sleep 0.5
done  
