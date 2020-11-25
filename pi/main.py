# necessary imports
import socket
import logging
import threading
import time
import RPi.GPIO as GPIO
import camera_stream

# setup the pins to use the BCM mode and disable GPIO warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

message = ""
distance = 0.0
speed = 0
ultra_trig = 22 # ultrasonic trigger pin number
ultra_echo = 23 # ultrasonic echo pin number

# Drive pin setups
GPIO.setup(18, GPIO.OUT) # setup the forward drive motor (pin 18)
fpwm = GPIO.PWM(18, 50)
fpwm.start(0)
GPIO.setup(17, GPIO.OUT) # setup the backward drive motor (pin 17)
bpwm = GPIO.PWM(17, 50)
bpwm.start(0)

# Servo setup
GPIO.setup(24, GPIO.OUT) # setup the servo motor (pin 24)
servo = GPIO.PWM(24, 50)
angle = 150
servo.start(angle/18 + 2)
        
        
# main thread (interpreting messages, driving, steering)
def thread_function(name):
    global message, distance, speed, angle
    time.sleep(2)
    while True:
        print(distance)
        if message:
            if message in ('w', 'W') and speed < 100:
                speed += 10
            elif message in ('s', 'S') and speed > -100:
                speed -= 10
            elif message in ('d', 'D') and angle > 125:
                angle -= 2.5
            elif message in ('a', 'A') and angle < 175:
                angle += 2.5
        drive(speed)
        steer(angle)
        message = ""
        time.sleep(0.1)


# ultrasonic sensor thread
def ultrasonic_distance(name):
    global ultra_trig, ultra_echo, distance
    GPIO.setup(ultra_trig, GPIO.OUT)
    GPIO.setup(ultra_echo, GPIO.IN)
    GPIO.output(ultra_trig, 0)

    MAX_PULSE = 23200.0/58.0

    while True:
        GPIO.output(ultra_trig, 1)
        time.sleep(0.001*0.01)
        GPIO.output(ultra_trig, 0)
        
        t1 = 0
        t2 = 0
        while GPIO.input(ultra_echo) == 0:
            pass
        t1 = int(round(time.time() * 1000*1000))
        while GPIO.input(ultra_echo) == 1:
            pass
        t2 = int(round(time.time() * 1000*1000))
        width = ((t2 - t1)*343/2)/(1000*1000)
        
        distance = width
        
        time.sleep(0.06)
    

# UPD thread (message handling)
def UDP_Thread(name):
    global message
    UDP_IP = socket.gethostbyname('raspberrypi.local')
    UDP_PORT = 5005
    print("IP: {}:{}".format(UDP_IP, UDP_PORT))

    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        message = data.decode('utf-8')
        print("received message: %s" % data)


# drive the robot with a given speed
def drive(speed):
    global distance, fpwm, bpwm
    print('driving with speed {} and distance {}'.format(speed, distance))
    if distance < 0.2 and speed > 0:
        speed = 0
    elif distance < 0.4:
        speed /= 2

    if speed > 0:
        fpwm.ChangeDutyCycle(speed)
        bpwm.ChangeDutyCycle(0)
    elif speed < 0:
        fpwm.ChangeDutyCycle(0)
        bpwm.ChangeDutyCycle(abs(speed))
    else:
        fpwm.ChangeDutyCycle(0)
        bpwm.ChangeDutyCycle(0)
        #print('not driving!')


# steer the robot with a given angle
def steer(angle):
    global servo
    if angle < 125:
        angle = 125
    elif angle > 175:
        angle = 175
    duty = angle / 18 + 2
    servo.ChangeDutyCycle(duty)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    
    x = threading.Thread(target=thread_function, args=(1,)) # start main thread
    x.start()
    comms = threading.Thread(target=UDP_Thread, args=(2,)) # start communication thread
    comms.start()
    
    ultra = threading.Thread(target=ultrasonic_distance, args=(3,)) # start ultrasonic thread
    ultra.start()

    cam = threading.Thread(target=camera_stream.Camera.camera_server, args=(4,)) # start camera thread
    cam.start()
    
    print('threads started')

    
