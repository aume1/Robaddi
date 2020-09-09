import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 100)
pwm.start(0)
speed = 0
while True:
	if speed <100:
		speed+=1
	else:
		speed = 0
	pwm.ChangeDutyCycle(speed)
	time.sleep(0.1)
