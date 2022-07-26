import RPi.GPIO as GPIO
# import pigpio
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)

while True:
    GPIO.output(6, False)
#     time.sleep(1)
#     GPIO.output(6, False)
#     time.sleep(1)
# canon_holder_servo_pin = 12
# right_canon_servo_pin = 24
# left_canon_servo_pin = 23

# servos = pigpio.pi()
# 
# servos.set_mode(canon_holder_servo_pin, pigpio.OUTPUT)
# servos.set_mode(right_canon_servo_pin, pigpio.OUTPUT)
# servos.set_mode(left_canon_servo_pin, pigpio.OUTPUT)

# servos.set_PWM_frequency(canon_holder_servo_pin, 50)
# servos.set_PWM_frequency(right_canon_servo_pin, 50)
# servos.set_PWM_frequency(left_canon_servo_pin, 50)
# 
# servos.set_servo_pulsewidth(canon_holder_servo_pin, 1500)
# servos.set_servo_pulsewidth(right_canon_servo_pin, 1400)
# servos.set_servo_pulsewidth(left_canon_servo_pin, 1600)

# sign = -1
# laser = False
# while True:
#     servos.set_servo_pulsewidth(canon_holder_servo_pin,1500)
# while True:
#     selection = input("selection: ")
#     angle = int(input("enter: "))
#     if selection == "right":
#         servos.set_servo_pulsewidth(right_canon_servo_pin, angle)
#     if selection == "left":
#         servos.set_servo_pulsewidth(left_canon_servo_pin, angle)
#     if selection == "center":
#         servos.set_servo_pulsewidth(canon_holder_servo_pin,angle)


#     servos.set_servo_pulsewidth(left_canon_servo_pin, 1500)
#     servos.set_servo_pulsewidth(right_canon_servo_pin, 1500)
#     for i in range(1500,1800,10):
#         servos.set_servo_pulsewidth(canon_holder_servo_pin,i)
#         time.sleep(0.1)
#     for i in range(1500,1800,-10):
#         servos.set_servo_pulsewidth(canon_holder_servo_pin,i)
#         time.sleep(0.1)


#     for i in range(2000):
#         if i % 10 == 0:
#             servos.set_servo_pulsewidth(canon_holder_servo_pin, 1600 + i/10)
#             laser = not laser
#             GPIO.output(6, laser)
# 
# 
#         servos.set_servo_pulsewidth(right_canon_servo_pin, 500 +  i)
#         servos.set_servo_pulsewidth(left_canon_servo_pin, 500 +  i)
#         time.sleep(0.005)
#     for i in range(2000):
#         if i % 10 == 0:
#             servos.set_servo_pulsewidth(canon_holder_servo_pin, 1800 - i/10)
#             laser = not laser
#             GPIO.output(6, laser)
# 
#         servos.set_servo_pulsewidth(right_canon_servo_pin, 2500 -  i)
#         servos.set_servo_pulsewidth(left_canon_servo_pin, 2500 -  i)
#         time.sleep(0.005)

    
    





