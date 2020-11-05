from Robot import Robot
import RPi.GPIO as GPIO
import time

try:
	if __name__ == "__main__":
		robot = Robot()
		while True:
			robot.run()
			time.sleep(0.05)
except KeyboardInterrupt:
	print("Keyboard interrupt. Exiting.")
finally:
	robot.cleanup()
	GPIO.cleanup()
