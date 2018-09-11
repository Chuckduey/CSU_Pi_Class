import picamera
import time

camera = picamera.PiCamera()

camera.start_preview(fullscreen=False,window = (100,20,1280,1024))
time.sleep(10)
camera.stop_preview()
