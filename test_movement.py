from movement_control import MovementControl
from configs import dc_m_1, dc_m_2, camera_servo_pin, image_width,face_detect_status_led
import time
from mpu6050_control import Mpu6050Control

from pynput import keyboard

mpu = Mpu6050Control()
m = MovementControl(dc_m_1, dc_m_2, mpu)

break_program = False
def on_press(key):
    global break_program
    if key == keyboard.Key.end:
        print ('end pressed')
        break_program = True
        m.stop()
        m.destroy()
        return False

m.calibrate()
start = time.time()
duration = 0.8
# m.start(100)
with keyboard.Listener(on_press=on_press) as listener:
    while break_program == False:
        while True:
#             angle = mpu.get_drift(0.1)
#             print(angle)
#             if angle > 0:
#                 m.steer(100, "left", abs(angle) / 0.2)
#             else:
#                 m.steer(100, "right", abs(angle) / 0.9)
            m.keep_straight(100)
        listener.join()

# while time.time() - start < 1:
#     print(mpu.get_drift(0.1))
#     m.steer(0, "left", 100)
# m.steer(100, "left", 100)
# print(mpu.get_drift(duration))
# m.stop()
# 
# m.steer(0, "right", 100)
# print(mpu.get_drift(duration))
# for _ in range(5):
#     m.start(100)
#     print(mpu.get_drift(duration))
# m.stop()
# m.destroy()