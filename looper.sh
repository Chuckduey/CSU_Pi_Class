#!/bin/bash
#gpio mode 4 out  
echo 4 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio4/direction
echo 22 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio22/direction
while true; do  
#    gpio -g write 4 1
    echo 1 > /sys/class/gpio/gpio4/value
    sleep 0.5
#    gpio -g write  4 0
    echo 0 > /sys/class/gpio/gpio4/value
    sleep 0.5
done  
