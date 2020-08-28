import RPi.GPIO as GPIO
import time
import folder.Motor as Motor
import folder.Servo as Servo

class Robot(object):
    def __init__(self):
        self.drive = Motor(12,13)
        self.steer = Servo(18)
        
        GPIO.setmode(GPIO.BCM)
        
    
    def run(self):
        for i in range(-180, 180):
            self.steer.set(i)
            time.sleep(0.02)
