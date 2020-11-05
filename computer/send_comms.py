#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 16:39:33 2020

@author: cameron
"""

import socket
#from tkinter import *
from tkinter import Tk, Label, Button, Radiobutton, IntVar, W
#from tkinter import *
import sys

import cv2
import numpy as np
import urllib

import threading
from PIL import ImageTk, Image

#import keyboard
import math



root = Tk()
#ip = socket.gethostbyname('raspberrypi.local')
ip = '192.168.43.244'

def color(b,g,r):
    b = 0 if b < 0 else 255 if b > 255 else b
    g = 0 if g < 0 else 255 if g > 255 else g
    r = 0 if r < 0 else 255 if r > 255 else r
    return [b,g,r]

def camera_server():
    
    stream=urllib.request.urlopen('http://' + ip + ':8000/stream.mjpg')
    #stream = urllib.urlopen('http://localhost:8080/frame.mjpg')
    bytes = b''
    cont = True
    while cont:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            i = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            hsv = cv2.cvtColor(i, cv2.COLOR_BGR2HSV)

            #B = cv2.getTrackbarPos("B", "Trackbars")
            #G = cv2.getTrackbarPos("G", "Trackbars")
            #R = cv2.getTrackbarPos("R", "Trackbars")
        
            #green = np.uint8([[[B, G, R]]])
            #hsvGreen = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
            tol = 30
            
            
            
            lowerBlack = np.uint8(color(0,0,0))
            tol = 30
            upperBlack = np.uint8(color(tol,tol,tol))
            
            #lowerLimit = np.uint8([hsvGreen[0][0][0]-tol,100,100])
            #upperLimit = np.uint8([hsvGreen[0][0][0]+tol,255,255])
        
            #mask = cv2.inRange(hsv, lowerLimit, upperLimit)
            #colormask = cv2.inRange(hsv, lowerLimit, upperLimit)
            blackmask = cv2.inRange(i, lowerBlack, upperBlack)
            
            
            #white = 255 * np.ones(image.shape, image.dtype)
            #white = 255*np.ones(image.shape)
            #result = cv2.bitwise_and(image  , image , mask=colormask)
            blackresult = cv2.bitwise_and(i, i, mask=blackmask)
            
            
            gray = cv2.cvtColor(blackresult, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 0, 255, 0)
            contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                #cv2.drawContours(i, contours, -1, (0,255,0), 3)
                
                areas = [cv2.contourArea(c) for c in contours]
                max_index = np.argmax(areas)
                cnt=contours[max_index]
                x,y,w,h = cv2.boundingRect(cnt)
                cv2.rectangle(i,(x,y),(x+w,y+h),(0,255,255),2)
                cx = int(x+(w/2))
                cy = int(y+(h/2))
                #cv2.circle(i, (cx, cy), 2, (255,0,0), 2)
                #cv2.circle(i, (160, 120), 1, (0,0,255), 2)
                
                angle = 80*(160-(cx))/416*2
                #print('Angle: {:2.2f}'.format(angle))
                
                '''print("Absolute angle off:  {}".format(80*math.sqrt((640/2-x+w/2)**2 + (480/2-y+h/2)**2)/416))
                print("Angle off of centre: {}, {}".format(
                    80*(640/2-(x+w/2))/416,
                    80*(480/2-(y+h/2))/416
                ))'''
                
        
            #cv2.imshow("frame", image)
            cv2.putText(i, 'Angle offset: {:2.2f}'.format(angle),
                        (10,10), cv2.FONT_HERSHEY_COMPLEX, 0.4, (255, 0, 0), 1)
            cv2.imshow('Live Camera', i)
            if cv2.waitKey(1) == 27:
                cont = False
                stream.close()
                #cv2.destroyAllWindows()
                

cam = threading.Thread(name='camera_server', target=camera_server)
#comms = threading.Thread(name='comms', target=send_signals)

cam.start()
#comms.start()

print('program')

UDP_IP = ip#socket.gethostbyname("raspberrypi.local")
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s:%s" % (UDP_IP, UDP_PORT))
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


    
def button_click():
    udp_message(MESSAGE)
    
    
    
def close(event):
    root.withdraw() # if you want to bring it back
    sys.exit() # if you want to exit the entire thing

def WASD(event):
    string = str.encode(event.char)
    print(string)
    udp_message(string)
    
    
def unWASD(event):
    string = str.encode('un' + event.char)
    print(string)
    udp_message(string)
    
def stop(event):
    udp_message('Stop')

root.geometry('500x400')
a = Label(root, text="Click in this box to drive the robot!")
#b = Button(root, text="button", command=button_click)
#b.pack()
a.pack()

#var = IntVar()
#b1 = Radiobutton(root, text="Driver Control", variable=var, value=1)
#b2 = Radiobutton(root, text="Object following", variable=var, value=2)

#b1.select()
#b2.pack(anchor = W)
#b1.pack(anchor = W)


root.bind('<Escape>', close)
for key in ('W', 'w', 'A', 'a', 'S', 's', 'D', 'd'):
    root.bind(key, WASD)

root.bind('p', lambda x: udp_message(b'Stop'))


def udp_message(message):
    sock.sendto(message, (UDP_IP, UDP_PORT))

def shift(event):
    print('shift')
    udp_message(b'shift')

root.mainloop()