#!/usr/bin/python3
import picamera
import time

camera = picamera.PiCamera()

camera.start_preview(fullscreen=True,rotation=90)
time.sleep(30)
camera.stop_preview()
