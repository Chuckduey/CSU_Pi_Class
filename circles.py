#
import time
import math
import Tkinter as tk
screen_height = 400
screen_width = 400
center_x = screen_width/2
center_y = screen_height/2
sin_30 = 100
cos_30 = 173
rad=5
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

canvas.create_circle(center_x, center_y, 197, fill="#2f2f34", outline="#7d7d81", width=3)
for r in range(175,0,-25):
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
ph_block=canvas.create_text(282,10,fill="white",font="Times 15",text="Phase = 180.0", anchor="w")

# Start main loop
for m in range (10,200,10):
  for d in range (361):
    x = m*math.cos(math.radians(d))
    y = m*math.sin(math.radians(d))
    mag = math.sqrt(x*x + y*y)
    out_str = "Mag = " + str(round(mag,2))
    canvas.itemconfigure(mag_block,text=out_str)
    out_str = "Phase = " + str(round(math.degrees(math.atan2(-y,x)),1))
    canvas.itemconfigure(ph_block,text=out_str)
    canvas.coords(circ1,center_x+x+rad,center_y+y+rad,center_x+x-rad,center_y+y-rad)
    canvas.update()
    time.sleep(0.01)
root.mainloop( )
