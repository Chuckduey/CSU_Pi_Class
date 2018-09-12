from twython import TwythonStreamer
#  Note the initkeys.py is not included.  
# For this program to run Twitter API keys are required.
execfile("initkeys.py")

hit_count = 0

class MyStreamer(TwythonStreamer):
     def on_success(self,data):
         global hit_count
         if 'text' in data:
             hit_count += 1
#             print " Hit Count = ",hit_count
         if hit_count >= 5:
             print("Raspberry Pi")
             hit_count = 0

stream = MyStreamer(c_k, c_s, a_t, a_s)
stream.statuses.filter(track="Raspberry Pi")

