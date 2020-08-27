import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18,1/1200)
# pwm = GPIO.PWM(1.5)
pwm.start(100)
# pwm.start(50)
# time.sleep(100)
while True:
	pass
	'''for i in range(50,100):
		pwm.ChangeDutyCycle(i)
		print(i)
		time.sleep(.1)'''
