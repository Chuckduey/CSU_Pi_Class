#!/bin/bash
gpio mode 4 out  
while true; do  
    gpio -g write 4 1
    sleep 0.5
    gpio -g write  4 0
    sleep 0.5
done  
