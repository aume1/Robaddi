from Robot import Robot
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

trigger = 18
echo = 17

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trigger, 0)

MAX_PULSE = 23200.0/58.0

while True:
    GPIO.output(trigger, 1)
    time.sleep(0.001*0.01)
    GPIO.output(trigger, 0)
    
    t1 = 0
    t2 = 0
    while GPIO.input(echo) == 0:
        pass
    t1 = int(round(time.time() * 1000*1000))
    while GPIO.input(echo) == 1:
        pass
    t2 = int(round(time.time() * 1000*1000))
    width = ((t2 - t1)*343/2)/(1000*1000)
    
    print(width)
    
    time.sleep(0.06)
    