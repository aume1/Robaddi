from picamera import PiCamera
from time import sleep

camera = PiCamera()
#camera.resolution = (1920, 1080)
camera.resolution = (1640, 1232)
camera.zoom = (0,0,0,0)

camera.start_preview()
sleep(30)
camera.stop_preview()

#camera length = 1.57
#total length = 15.4
print(15.4-1.57)
