import numpy as np
search_animation_body = {
    "style": "chase",
    "color" : (255,0,0),
    "size": 3,
    "spacing": 10,
    "speed": 0.1
    }

found_animation_body = {
    "style": "rainbow",
    "speed": 0.1,
    "period": 9
    }

listen_passive_animation = {
    "style": "pulse",
    "speed": 0.1,
    "color": (0,255,0),
    "period": 2
    }

listen_active_animation = {
    "style": "rainbow_comet",
    "speed": 0.1,
    "tail_length": 4,
    "bounce": True
    }
animations_to_event_mapping = {
    "search": search_animation_body,
    "found":found_animation_body,
    "listen_active":listen_active_animation,
    "listen_passive":listen_passive_animation
    }
e_1 = 18
e_2 = 25

dir_a_1 = 24
dir_b_1 = 23

dir_a_2 = 7
dir_b_2 = 8

dc_m_1 = {
    "en": e_1,
    "dir_a": dir_a_1,
    "dir_b": dir_b_1,
    }
dc_m_2 = {
    "en": e_2,
    "dir_a": dir_a_2,
    "dir_b": dir_b_2,
    }

camera_servo_id = 7
platform_servo_id = 0
right_servo_id = 3
left_servo_id = 4

trigger_pin = 12
echo_pin = 27
laser_pin = 6

lower_red = np.array([0, 0, 255])
upper_red = np.array([255, 255, 255])
    
image_width = 400
people_all = [["Dad", "mohamad", "muhammad"], ["Mum", "ghinwa"], ["Jihad","jayjay", "jj"],
          ["Ahmad", "ahmed"], ["Ayda","sister", "ada"], ["Omar", "amilase", "amylase", "oma"],
          ["Khaled", "lurk","bourke", "look", "luck"], ["Mustapha", "boss", "mustafa"],
          ["Abdullah"], ["Malak", "angle"]]

NOT_STARTED = "NOT_STARTED"
SEARCHING = "SEARCHING"
FOUND = "FOUND"
ROTATED = "ROTATED"
ARRIVED = "ARRIVED"
ADJUSTED = "ADJUSTED"
AIMED = "AIMED"
