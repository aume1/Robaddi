import RPi.GPIO as GPIO
import time
from Motor import Motor
from Servo import Servo

class Robot(object):
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.drive = Motor(18, 12)
		#self.steer = Servo(0)
		self.speed = 0.0

	def run(self):
		#print("running motor at {} speed".format(self.speed))
		self.drive.set(self.speed)
		if self.speed > 100:
			self.speed = 0
		else:
			self.speed += 1

	def cleanup(self):
		self.drive.cleanup()
