from imutils.video import VideoStream
from imutils.video import FPS
import cv2
import face_recognition
import imutils
import pickle
import numpy as np
import json
import time
import RPi.GPIO as GPIO
import requests
from time import sleep
from multiprocessing import Process, Manager
from Queue import Empty
from mpu6050_control import Mpu6050Control
from speech_recogniser import SpeechRecogniser

from helpers import search_for_face, prepare_to_move, prepare_to_move_non_middle, check_for_name, \
     play_animation, end_animation, control_camera, control_laser_platform, control_laser_status, laser_sweep
from movement_control import MovementControl
from configs import dc_m_1, dc_m_2, image_width, people_all, camera_servo_id, \
     trigger_pin, echo_pin, laser_pin, lower_red, upper_red

GPIO.setmode(GPIO.BCM)
GPIO.setup(laser_pin, GPIO.OUT)

encodingsP = "encodings.pickle"
desired_name = ""
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(encodingsP, "rb").read())

vs = VideoStream(src=0,framerate=10).start()
time.sleep(2.0)

fps = FPS().start()

current_angle = 90

direction = 1
timer_since_last_face = 0
moving_timer = time.time()
search_pause = 2
face_timer = time.time()
face_found = False
initial_find = True
confirm_face_default = 3

def dc_motor_control_process(q_m, q_s, s, l):
    mpu = Mpu6050Control()
    motor = MovementControl(dc_m_1, dc_m_2, trigger_pin, echo_pin, mpu)
    motor.calibrate(2, 90)
    
    while True:
        try:
            command = q_m.get(block=False)
            if isinstance(command, str):
                if command == "end":
                    motor.stop()
                    motor.destroy()
                    
            print("motors received command: {}".format(command))
            value = command[0]
            direction = command[1]
            if s.value == 1 or s.value == 2:
                continue
            elif s.value == 0:
                with l:
                    s.value = 1
            elif s.value == 3:
                s.value = 4

            if direction == "right" or direction == "left":
                motor.steer_by_angle(100, direction, value)
                motor.stop()
            if s.value == 1:
                time.sleep(1)
                motor.move(100)
                while True:
                    if motor.keep_straight(100) == -1000:
                        wrong_counter = 0
                        motor.stop()
                        time.sleep(0.1)
                        for _ in range(5):
                            if not motor.verify_ditance_at_rest():
                                wrong_counter += 1
                        if wrong_counter < 3:
                            motor.move(100)
                            print("false dist warning")
                            continue
                        else:
                            q_s.put("arrived")
                            print("arrived")
                            with l:
                                s.value = 2
                            break
                time.sleep(0.5)
        except Empty as e:
            motor.stop()
            pass


def voice_listener_process(q_m, q_s, q_l ):
    s = SpeechRecogniser()
    while True:
        text_read1 = s.start_listening(1)
        if text_read1:
            if "rob" in text_read1:
                q_l.put("listen_active")
                text_read2 = s.start_listening(3)
                q_l.put("stop")
                if text_read2:
                    text_read = text_read1 + text_read2
                else:
                    text_read = text_read1
                if text_read:
                    if "start" in text_read:
                        m_q.put("start")
                    elif "stop" in text_read:
                        m_q.put("stop")
                    elif "find" in text_read:
                        name_found = check_for_name(text_read, people_all)
                        if name_found:
                            q_s.put(name_found)
                    elif "exit" in text_read or "quit" in text_read:
                            q_s.put("exit")



def light_controller_process(q_l):
    while True:
        try:
            command = q_l.get(block=False)
            if command == "stop":
                end_animation()
            else:
                play_animation(command)
        except Empty as e:
            pass
        
def laser_controller_process(q_laser):
    while True:
        try:
            command = q_laser.get(block=False)
            control_laser_status(command)
#             laser_sweep()
        
        except Empty as e:
            pass

# motor queue        
m_q = Manager().Queue()
# voice listener queue
s_q = Manager().Queue()
# light controller queue
l_q = Manager().Queue()
# laser controller queue
laser_q = Manager().Queue()

# status 0: not started, 1: moving, 2: arrived
status = Manager().Value("i", 0)
lock =  Manager().Lock()

m_process = Process(target=dc_motor_control_process, args=(m_q, s_q, status, lock))
s_process = Process(target=voice_listener_process, args=(m_q, s_q, l_q))
l_process = Process(target=light_controller_process, args=(l_q,))
laser_process = Process(target=laser_controller_process, args=(laser_q,))

all_processes = [
                 m_process,
                 s_process,
                 l_process,
                 laser_process                
                 ]
for p in all_processes:
    p.start()
l_q.put("stop")
laser_q.put("off")

desired_name = "Abdullah"
confirm_face = confirm_face_default
time.sleep(9)
while True:
    stop = False
    try:
        n = s_q.get(block=False)
        if n:
            if n == "arrived":
                continue
            elif n == "exit":
                print("Ending the execution")
                stop = True
            else:
                desired_name = n
                laser_q.put("off")
                l_q.put("search")
                current_angle = 90
                with lock:
                    status.value = 0
                print("desired name changed to {}".format(desired_name))
    except:
        pass   
      
    frame = vs.read()
    frame = imutils.resize(frame, width=image_width)
    if status.value != 3 and status.value != 1:
        face_found = False
        boxes = face_recognition.face_locations(frame)
        
        encodings = face_recognition.face_encodings(frame, boxes)
#         face_found = False
        box_index = 0
        matching_box_count = 0
               
        for encoding_index, encoding in enumerate(encodings):

            matches = face_recognition.compare_faces(data["encodings"],
                encoding)


            if True in matches:

                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                name = max(counts, key=counts.get)
                if name == desired_name:
                    if counts[name] > matching_box_count:
                        box_index = encoding_index
                        face_found = True
    if face_found:
        if status.value == 0:
            confirm_face -= 1
            print('confirm face: '+str(confirm_face))
            if confirm_face > 0:
                cv2.imshow("Facial Recognition is Running", frame)
                key = cv2.waitKey(1) & 0xFF
                continue
        with lock:
            if status.value == 2:
                l_q.put("found")
                print("lighting up")
                laser_q.put("on")
                status.value = 3
                time.sleep(2)
        if status.value == 4:                
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_red, upper_red)
            (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
            cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)
            

        (top, right, bottom, left) = boxes[box_index]
        cv2.rectangle(frame, (left, top), (right, bottom),
            (0, 255, 225), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, desired_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
            .8, (0, 255, 255), 2)
        rotation = prepare_to_move_non_middle(current_angle, boxes[box_index], image_width)
        print(rotation)
        current_angle = 90
        if status.value == 0 or status.value == 3:
            control_camera(current_angle)
            print(rotation)
            m_q.put(rotation)

        face_timer = time.time()
#         time.sleep(5)
    else:
        (current_angle, direction) = search_for_face(current_angle, direction)
        if desired_name:
            confirm_face = confirm_face_default
            control_camera(current_angle)
#             time.sleep(1)

    
    cv2.imshow("Facial Recognition is Running", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or stop:
        control_camera(90)
        break

    fps.update()

m_q.put("end")
while not m_q.empty():
    m_q.get()
    sleep(1)
for p in all_processes:
    p.terminate()

fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()
end_animation()
