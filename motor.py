import RPi.GPIO as GPIO
import time

class Motor(object):
    def __init__(self, forward_pin, backward_pin, speed=0.0, frequency=1000, invert=False):
        self.fpin = forward_pin
        self.bpin = backward_pin
        self.speed = speed
        self.frequency = frequency
        self.invert = invert
        
        GPIO.setup(forward_pin, GPIO.OUT)
        GPIO.setup(backward_pin, GPIO.OUT)
        self.fpwm = GPIO.PWM(forward_pin, frequency)
        self.bpwm = GPIO.PWM(backward_pin, frequency)
        
        self.set(speed)
        
    
    def set(self, speed):
        if speed > 1:
            speed = 1
        elif speed < -1:
            speed = -1
        
        self.speed = speed
        
        if self.speed == 0.0:
            self.fpwm.ChangeDutyCycle(0)
            self.bpwm.ChangeDutyCycle(0)
        if self.invert ^ (self.speed > 0): # speed is positive
            self.fpwm.ChangeDutyCycle(speed*100)
            self.bpwm.ChangeDutyCycle(0)
        else: # speed is negative
            self.fpwm.ChangeDutyCycle(0)
            self.bpwm.ChangeDutyCycle(speed*100)
    
    def set_inverted(self, invert):
        self.invert = invert
    
