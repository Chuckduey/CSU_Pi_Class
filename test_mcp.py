import time 
import botbook_mcp3002 as mcp # 

def readPotentiometer(): 
   global potentiometer 
   potentiometer = mcp.readAnalog() # 

def main(): 
   while True: # 
     readPotentiometer() # 
     print("The current potentiometer value is %i " % potentiometer) # 
     ime.sleep( 0.5) # s 

if __name__ = = "__main__": 
  main()

