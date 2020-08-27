import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

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
        
class Servo(object):
    def __init__(self, pin, min_value = 2.2, max_value = 11.8, frequency=50):
        self.pin = pin
        self.frequency = frequency
        self.min_value = min_value
        self.max_value = max_value
        
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, frequency)
	self.pwm.start(0)

    def set(self, angle):
	self.set_angle(angle)
    def set_angle(self, angle):
        pwm_angle = (angle/180.0) * (self.max_value-self.min_value)/2.0
        pwm_angle += (self.max_value + self.min_value)/2
        self.pwm.ChangeDutyCycle(pwm_angle)
    
if __name__ == "__main__":
    #motor = Motor(12,13)
    servo = Servo(18)
    while True:
        for i in range(-180, 180):
            servo.set(i)
	    time.sleep(0.02)
