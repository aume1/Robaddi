import RPi.GPIO as GPIO
import time

class Motor(object):
    def __init__(self, forward_pin, backward_pin, speed=0.0, frequency=100, invert=False):
        print("Initalising motor in pins {} and {} with speed {} and frequency {}.".format(forward_pin, backward_pin, speed, frequency))
        self.fpin = forward_pin
        self.bpin = backward_pin
        self.speed = speed
        self.frequency = frequency
        self.invert = invert
        
        GPIO.setup(forward_pin, GPIO.OUT)
        self.fpwm = GPIO.PWM(forward_pin, frequency)
        self.fpwm.start(0)

        GPIO.setup(backward_pin, GPIO.OUT)
        self.bpwm = GPIO.PWM(backward_pin, frequency)
        self.bpwm.start(0)
        
        self.set(speed)
        
    
    def set(self, speed):
        print("setting speed to {}".format(speed))
        if speed > 1:
            speed = 1
        elif speed < -1:
            speed = -1
        
        self.speed = speed
        
        if int(self.speed) == 0:
            print('speed 0')
            self.fpwm.ChangeDutyCycle(0)
            self.bpwm.ChangeDutyCycle(0)
        elif self.invert ^ (self.speed > 0): # speed is positive
            print('speed positive')
            self.fpwm.ChangeDutyCycle(speed*100)
            self.bpwm.ChangeDutyCycle(0)
        else: # speed is negative
            print('speed negative')
            self.fpwm.ChangeDutyCycle(0)
            self.bpwm.ChangeDutyCycle(speed*100)
    
    def set_inverted(self, invert):
        self.invert = invert

    def cleanup(self):
        self.set(0)
