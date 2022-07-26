from movement_control import *
from configs import *
import time
from mpu6050_control import Mpu6050Control
mpu = Mpu6050Control()

m = MovementControl(dc_m_1, dc_m_2, trigger_pin, echo_pin, mpu)
keep_trying = 3

while keep_trying > 0: 
    try:
        m.calibrate(2, 90)
        break
    except Exception as e:
        print(e)
        keep_trying -= 1
        pass

while True:
    try:
        fun = input("Enter next move (move, stop, steer, angle, straight, calibrate): ")
        if fun == "move":
            speed = int(input("enter speed: "))
            duration = int(input("duration: "))
            m.move(speed)
            time.sleep(duration)
            m.stop()

        if fun == "steer":
            args = input("speed,direction,percentage: ").split(",")
            duration = int(input("duration: "))
            m.steer(int(args[0]), args[1], int(args[2]))
            time.sleep(duration)
            m.stop()

        if fun =="stop":
            m.stop()
        if fun == "calibrate":
            args = input("repeats,angle,max_time: ").split(",")
            args = [int(arg) for arg in args]
            m.calibrate(args[0], args[1], args[2])
            m.stop()
        if fun == "angle":
            args = input("speed,direction,angle: ").split(",")
            m.steer_by_angle(int(args[0]), args[1], int(args[2]))
            m.stop()
        if fun == "straight":
            speed = int(input("enter speed: "))
            duration = int(input("duration: "))
            m.move(speed)
            start_time = time.time()
            angle = 0
            while time.time() - start_time < duration:
                temp_angle = m.keep_straight(speed)
                if temp_angle == -1000:
                    break
                angle += temp_angle
            m.stop()
            

    except Exception as e:
        print(e)
        print("err")
        m.stop()
        m.destroy()
        
