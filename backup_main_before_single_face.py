#! /usr/bin/python

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import RPi.GPIO as GPIO
import pigpio
from time import sleep
from multiprocessing import Process, Manager

from helpers import adjust_cam_position, search_for_face, prepare_to_move
from movement_control import MovementControl
from configs import dc_m_1, dc_m_2, camera_servo_pin, image_width,face_detect_status_led

camera_servo = pigpio.pi()
camera_servo.set_mode(camera_servo_pin, pigpio.OUTPUT)
camera_servo.set_PWM_frequency(camera_servo_pin, 50)

m = MovementControl(dc_m_1, dc_m_2)

GPIO.setup(face_detect_status_led, GPIO.OUT)
GPIO.output(face_detect_status_led, False)

current_name = "unknown"
encodingsP = "encodings.pickle"

print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

vs = VideoStream(src=0,framerate=10).start()
time.sleep(2.0)

fps = FPS().start()

current_angle = 1500
direction = 1
timer_since_last_face = 0
moving_timer = time.time()
face_detected = False
search_pause = 2
face_timer = time.time()
camera_servo.set_servo_pulsewidth(camera_servo_pin, current_angle)

def dc_motor_control_process(q, motor):
    moving = False
    while True:
        try:
            command = q.get(block=False)
            if command == "start":
                moving = True
                motor.start()
            if command == "stop":
                moving = False
        except:
            if moving:
                motor.keep_straight(100)
            
        
    return

m_q = Manager().Queue()

m_process = Process(target=dc_motor_control_process, args=(m_q,m))

all_processes = [m_process]
for p in all_processes:
    p.start()

while True:
    
    frame = vs.read()
    frame = imutils.resize(frame, width=image_width)
    boxes = face_recognition.face_locations(frame)

    if boxes:
        print(boxes)
        face_detected = True
        m.stop()
        GPIO.output(face_detect_status_led, True)
        new_angle = adjust_cam_position(boxes, current_angle, image_width)
#         print(new_angle - current_angle)
#         print(current_angle)
        if new_angle - current_angle == 0:
            rotation_time = prepare_to_move(new_angle, m)
            new_angle = 1500
            m_q.put("start")
#           
#                 m.stop()
        current_angle = new_angle
        face_timer = time.time()
    else:
        GPIO.output(face_detect_status_led, False)
        if time.time() - face_timer > search_pause:
            (current_angle, direction) = search_for_face(current_angle, direction)
            face_detected = False
    camera_servo.set_servo_pulsewidth(camera_servo_pin, current_angle)

    encodings = face_recognition.face_encodings(frame, boxes)
    names = []
    
    person_to_check = "Mustapha"

    for encoding in encodings:

        matches = face_recognition.compare_faces(data["encodings"],
            encoding)
        name = "Unknown"
        # print(matches)

        if True in matches:

            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
            # print(counts)
            name = max(counts, key=counts.get)

            if current_name != name:
                current_name = name
                print(current_name)

        names.append(name)

    for ((top, right, bottom, left), name) in zip(boxes, names):
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)

    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    fps.update()

m_q.put("stop")
    
for p in all_processes:
    p.terminate()
#     print(p)
#     p.join()
#     print(p)
fps.stop()
m.destroy()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
