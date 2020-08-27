import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

'''GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18,1/1200)
# pwm = GPIO.PWM(1.5)
pwm.start(100)
# pwm.start(50)
# time.sleep(100)
while True:
	pass
	for i in range(50,100):
		pwm.ChangeDutyCycle(i)
		print(i)
		time.sleep(.1)'''

class Motor(object):
    '''fpin = -1
    bpin = -1
    speed = 0.0
    frequency = 0
    fpwm = None
    bpwm = None
    invert = False'''
    
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
    '''pin = -1
    pwm = None
    min_val = -1
    max_val = -1
    frequency = 50'''
    
    def __init__(self, pin, min_value = 2.2, max_value = 11.8, frequency=50):
        self.pin = pin
        self.frequency = frequency
        self.min_val = min_value
        self.max_val = max_value
        
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, frequency)
        
    def set_angle(self, angle):
        pwm_angle = (angle/180.0) * (self.max_value-self.min_value)/2.0
        pwm_angle += (self.max_value + self.min_value)/2
        self.pwm.ChangeDutyCycle(pwm_angle)
    
if __name__ == "__main__":
    #motor = Motor(12,13)
    servo = Servo(18)
    while True:
        for i in range(-90, 90):
        servo.set_angle(i)
        time.sleep(0.01)