#!/usr/bin/python3
import time
import math
import re
import tkinter as tk
import serial
port = "/dev/ttyACM0"
screen_height = 450
screen_width = 450
center_x = screen_width/2
center_y = screen_height/2
sin_30 = 100
cos_30 = 173
rad=4
min_mag=0.1
q1=str.encode("AFF0000"+"\r\n")
q2=str.encode("A00FF00"+"\r\n")
q3=str.encode("A0000FF"+"\r\n")
q4=str.encode("AFFFF00"+"\r\n")
q5=str.encode("AFFFFFF"+"\r\n")
ser = serial.Serial(port=port, baudrate=9600)
ser.write(q1)
cur_led=q1
time.sleep(1)
# Define Tk root
root = tk.Tk()
canvas = tk.Canvas(root, width=screen_width, height=screen_height, borderwidth=0, highlightthickness=0, bg="#27272d")
canvas.grid()
def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle
def drawcircle(canv,x,y,rad):
    # changed this to return the ID
    return canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill='yellow')
def led_update(new_led):
    global cur_led
    if (new_led != cur_led):
        cur_led = new_led
        ser.write(new_led)

canvas.create_circle(center_x, center_y, 223, fill="#2f2f34", outline="#7d7d81", width=3)
for r in range(200,0,-25):
    canvas.create_circle(center_x, center_y, r, fill="#2f2f34", outline="#7d7d81")
canvas.create_line(0,center_y,screen_width,center_y,fill="#7d7d81")
canvas.create_line(center_x,0,center_x,screen_height,fill="#7d7d81")
canvas.create_line(center_x-cos_30,center_y-sin_30,center_x+cos_30,center_y+sin_30,fill="#7d7d81")
canvas.create_line(center_x-sin_30,center_y-cos_30,center_x+sin_30,center_y+cos_30,fill="#7d7d81")
canvas.create_line(center_x-cos_30,center_y+sin_30,center_x+cos_30,center_y-sin_30,fill="#7d7d81")
canvas.create_line(center_x-sin_30,center_y+cos_30,center_x+sin_30,center_y-cos_30,fill="#7d7d81")
root.wm_title("Polar Plot")
circ1=drawcircle(canvas,100,100,rad)
mag_block=canvas.create_text(15,10,fill="white",font="Times 15",text="Mag = 1.2", anchor="w")
ph_block=canvas.create_text(328,10,fill="white",font="Times 15",text="Phase = 180.0", anchor="w")
x = 10
y = 10
# Start main loop
root.geometry('%dx%d+%d+%d' % (screen_width, screen_height,0,-5))
while True:
    ser_in = ser.readline()
    out_vec = re.findall(r"[-+]?\d*\.\d+|\d+",ser_in.decode("utf-8"))
    if len(out_vec) > 3:
         x = float(out_vec[1])*150/9.8
         y = float(out_vec[0])*150/9.8
    mag = math.sqrt(x*x + y*y)/150.0
    out_str = "Mag = " + str(round(mag,2))
    canvas.itemconfigure(mag_block,text=out_str)
    out_str = "Phase = " + str(round(math.degrees(math.atan2(-y,x)),1))
    canvas.itemconfigure(ph_block,text=out_str)
    canvas.coords(circ1,center_x+x+rad,center_y+y+rad,center_x+x-rad,center_y+y-rad)
    canvas.update()
    if mag < min_mag:
        led_update(q5)
    else:
      led_update(q1)
root.mainloop( )
