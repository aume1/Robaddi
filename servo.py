import RPi.GPIO as GPIO
import time

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
