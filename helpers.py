import time
import requests
import json
import RPi.GPIO as GPIO

from configs import animations_to_event_mapping, camera_servo_id, platform_servo_id, \
     right_servo_id, left_servo_id, laser_pin

def play_animation(animation):
    requests.post("http://127.0.0.1:5000/animation", data=json.dumps(animations_to_event_mapping[animation]),
    headers = {'content-type':'application/json'})

def end_animation():
    requests.post("http://127.0.0.1:5000/animation", data=None)

def control_camera(angle):
    requests.post("http://127.0.0.1:5001/control",
        data=json.dumps({"id": camera_servo_id, "angle": angle}),
        headers = {'content-type':'application/json'})
    

def control_laser_platform(angle):
    requests.post("http://127.0.0.1:5001/control",
        data=json.dumps({"id": platform_servo_id, "angle": angle}),
        headers = {'content-type':'application/json'})
    
def control_laser_canons(angle):
    requests.post("http://127.0.0.1:5001/control",
        data=json.dumps({"id": camera_servo_id, "angle": angle}),
        headers = {'content-type':'application/json'})    

def control_laser_status(status):
    if status == "on":
        GPIO.output(laser_pin, True)
    if status == "off":
        GPIO.output(laser_pin, False)
        
def control_laser_all(location, angle):
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
    control_laser_platform(angle)
    return angle

def laser_sweep():
    while True:
        for i in range(90):
            requests.post("http://127.0.0.1:5001/control",
                            data=json.dumps({"id": 0, "angle": 110 - i}),
                            headers = {'content-type':'application/json'})
            time.sleep(0.1)
            
#             print(requests.post("http://127.0.0.1:5001/control",
#                             data=json.dumps({"id": 3, "angle": 60 + i}),
#                             headers = {'content-type':'application/json'}))
#             print(requests.post("http://127.0.0.1:5001/control",
#                             data=json.dumps({"id": 4, "angle": 120 - i}),
#                             headers = {'content-type':'application/json'}))
#             time.sleep(0.1)
        for i in range(60):
            requests.post("http://127.0.0.1:5001/control",
                            data=json.dumps({"id": 0, "angle": 110 - i}),
                            headers = {'content-type':'application/json'})
            
#             print(requests.post("http://127.0.0.1:5001/control",
#                             data=json.dumps({"id": 3, "angle": 120 - i}),
#                             headers = {'content-type':'application/json'}))
#             print(requests.post("http://127.0.0.1:5001/control",
#                             data=json.dumps({"id": 4, "angle": 60 + i}),
#                             headers = {'content-type':'application/json'}))
            time.sleep(0.1)

def dist_from_mid(face_loc, image_width):
    return (face_loc[1] - face_loc[3]) / 2 + face_loc[3] - image_width / 2

def search_for_face(current_angle, direction):

    step_distance = 18
    new_angle = current_angle + direction * step_distance
    if new_angle <= 0:
        new_angle = 0
        direction = 1
    if new_angle >= 180:
        new_angle = 180
        direction = -1
    return (new_angle, direction)

def prepare_to_move(angle, m_c):
    speed = 0
    if angle > 90:
        direction = "left"
    elif angle < 90:
        direction = "right"
    else:
        direction = "straight"
        speed = 70
    if direction == "straight":
        return 0
    m_c.steer(speed, direction, 100)
    rotation_time = abs(angle - 90) * 1.0 / 90.0
    time.sleep(rotation_time)
    m_c.stop()
    return direction

def prepare_to_move_non_middle(angle, face_loc, image_width):
#     dist = dist_from_mid(face_loc, image_width)
#     dist = 0 if abs(dist) < 20 else dist
#     angle = angle - dist
#     if angle > 1510:
#         direction = "left"
#     elif angle < 1490:
#         direction = "right"
#     else:
#         direction = "straight"
#     angle = abs(angle - 1500) * 90 / 1000
#     return angle, direction
    dist = dist_from_mid(face_loc, image_width)
#     dist = 0 if abs(dist) < 20 else dist
#     angle = angle - dist
    dist_mapping = dist * 62 / image_width
    print("angle= " + str(angle))

    angle = angle - dist_mapping

    if angle > 92:
        direction = "left"
        angle = angle - 90
    elif angle < 88:
        direction = "right"
        angle = 90 - angle
    else:
        direction = "straight"
#     angle = abs(angle - 1500) * 100 / 1000 - 90
    print("dist= " + str(dist_mapping))

    return angle, direction

def check_for_name(text, name_list):
    for n in name_list:
        for name in n:
            if name.lower() in text:
                return n[0]
    return None
    
    
        