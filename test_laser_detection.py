import cv2
import numpy as np
import time
import imutils
from helpers import control_laser_status
from configs import laser_pin
import RPi.GPIO as GPIO
import requests, json
from collections import Counter

GPIO.setmode(GPIO.BCM)
GPIO.setup(laser_pin, GPIO.OUT)

control_laser_status("on")
cap = cv2.VideoCapture(0)

angle = 20

requests.post("http://127.0.0.1:5001/control",
            data=json.dumps({"id": 0, "angle": angle}),
            headers = {'content-type':'application/json'})

pts = []
def adjust_laser(location, angle):
    print("angle= " + str(angle))
    if location == 0:
        angle = angle + 1
    if angle < 20:
        return 20
    if angle > 60:
        return 60
        
    if location > 50:
        angle = angle + 1
    if location < 40:
        angle = angle - 1
    requests.post("http://127.0.0.1:5001/control",
            data=json.dumps({"id": 0, "angle": angle}),
            headers = {'content-type':'application/json'})
    return angle

samples = []

while (1):

    # Take each frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



    lower_red = np.array([0, 0, 255])
    upper_red = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
#     print(maxLoc)
    cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('Track Laser', frame)
#     angle = adjust_laser(maxLoc, angle)
    if len(samples) < 10:
        samples.append(maxLoc[1])
    else:
        c = Counter(samples)
        most_common = c.most_common(1)
        if most_common != 0:
            print(most_common[0][0])
        samples = []
        angle = adjust_laser(most_common[0][0], angle)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


