#!/bin/bash
#gpio mode 4 out  
mraa-gpio set 7 output
while true; do  
#    gpio -g write 4 1
    mraa-gpio set 7 1
    sleep 0.5
#    gpio -g write  4 0
    mraa-gpio set 7 0
    sleep 0.5
done  
