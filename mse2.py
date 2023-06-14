#===============================================================
#VERSION
#===============================================================
#00.00.............................Working test of concept
#01.00.............................Changed to move mouse 5 spaces left from current position for less disruption.
#===============================================================


import pyautogui as py
import time
import sys
#from datetime import datetime
#from playsound import playsound
import datetime
import playsound #1.2.2 version (latest version causes exception in code) to install: py -m pip install playsound==1.2.2

now = datetime.datetime.now().time() # time object
today6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)

# sound = r'C:\Windows\Media\Ring02.wav'
# endsound = r'C:\Windows\Media\Alarm10.wav'
# playsound.playsound(sound)

py.FAILSAFE = False
numMin = 1
x = 0

while(x<numMin):
    #time.sleep(5)
    time.sleep(60) #was 300
    now = datetime.datetime.now().time()
    postuple = py.position()
    print(now)
    print(postuple)

    time.sleep(60) #was 300
    now = datetime.datetime.now().time()
    postuple2 = py.position()
    print(now)
    print(postuple2)
    
    if postuple == postuple2:
        py.press("shift")
        print("Movement made at {}".format(datetime.datetime.now().time()))
    if datetime.datetime.now().time() >= today6pm:
        print('End')
        #exec(open("schedule.py").read())
        now = datetime.datetime.now().time() # time object
        today6pm = now.replace(hour=18, minute=0, second=0, microsecond=0)
        time.sleep(60*60*12)
