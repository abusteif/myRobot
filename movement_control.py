from dc_motor_control import DCMotor
import time
import statistics
from math import log
from ultrasonic_control import UltrasonicControl
import copy

class MovementControl:
    def __init__(self, dc_m_1, dc_m_2, ultrasonic_trig=None, ultrasonic_echo=None, mpu=None, min_distance=40):
        self.m_l = DCMotor(dc_m_1)
        self.m_r = DCMotor(dc_m_2)
        self.ultrasonic = UltrasonicControl(ultrasonic_trig, ultrasonic_echo)
        self.mpu = mpu
        self.calibrated = False
        self.calibrations = {}
        self.angle_sum = 0
        self.distance_check = False
        self.min_distance = min_distance
        
    def calibrate(self, repeats, max_time = 2):
        self.calibrate_mpu()
        try:
            self.calibrate_rotation(repeats, max_time)
            self.calibrated = True
        except Exception as e:
            print(e)
            self.stop()
        
    def calibrate_mpu(self):
        self.mpu.calibrate()

    def calibrate_rotation(self, repeats, max_time=2):
        
        times = {
            "left": {
                5:[],
                10:[],
                15:[],
                20:[],
                30:[],
                40:[],
                50:[],
                90:[],
                180:[]
                },
            "right":{
                5:[],
                10:[],
                15:[],
                20:[],
                30:[],
                40:[],
                50:[],
                90:[],
                180:[]
                }
            }
        avgs = copy.deepcopy(times)
        calibration = copy.deepcopy(times)
        for d in times:
            for angle in times[d]:
                counter = 0
                while counter < repeats:
                    self.steer(0, d, 100)
                    new_time = self.mpu.get_time_by_angle(angle)
                    self.stop()
                    if new_time > max_time:
                        counter -= 1
                        continue
                    times[d][angle].append(new_time)
                    counter += 1
                    
                    time.sleep(5)
        classifications = []
        
        for d in times:
            for angle in times[d]:
                avg = statistics.mean(times[d][angle])
                avgs[d][angle] = avg
                for t in times[d][angle]:
                    classifications.append(t/avg < 0.9)
                if classifications.count(True) > repeats / 2:
                    print("Repeat calibration")
                else:
                    print("Calibration successful")
                    calibration[d][angle] = avgs[d][angle] / angle
        
        self.calibrations = calibration
        print(calibration)
        return calibration
    
#     def calibrate_rotation(self, repeats, angle, max_time=2):
#         times = {"left": [], "right":[]}
#         calibration = {"left": 0, "right":0}
#         for d in times:
#             counter = 0
#             while counter < repeats:
#                 self.steer(0, d, 100)
#                 time.sleep(1)
#                 new_time = self.mpu.get_time_by_angle(angle)
#                 if new_time > max_time:
#                     counter -= 1
#                     continue
#                 times[d].append(new_time)
#                 counter += 1
#                 a = time.time()
#                 self.stop()
#                 time.sleep(1)
#         classifications = []
#         avgs = {"right":0, "left":0}
#         for dire in times:
#             avg = statistics.mean(times[dire])
#             avgs[dire] = avg
#             for t in times[dire]:
#                 classifications.append(t/avg < 0.9)
#             if classifications.count(True) > repeats / 2:
#                 print("Repeat calibration")
#             else:
#                 print("Calibration successful")
#                 calibration[dire] = avgs[dire] / angle
#         
#         self.calibrations = calibration
#         print(calibration)
#         return calibration          
        
    def steer(self, current_speed, direction, percentage):
        amount = int((100 - percentage) * current_speed * 0.01)
        
        if current_speed == 0:
            current_speed = percentage
            amount = 0

        if direction == "right":
            self.m_r.move(True, amount)
            self.m_l.move(True, current_speed)
        elif direction == "left":
            self.m_r.move(True, current_speed) 
            self.m_l.move(True, amount)
        elif direction == "straight":
            self.m_r.move(True, current_speed)
            self.m_l.move(True, current_speed)
    
    def steer_by_angle(self, current_speed, direction, angle):
        if not self.calibrated:
            print("Please calibrate first")
#         correction_factor = 0.00014881 * angle * angle - 0.021131 * angle + 1.73393
#         if correction_factor < 1 or angle > 70:
#             correction_factor = 1
#         print(correction_factor)
#         correction_factor = 0.95 if angle >= 45 else 1.2
#         correction_factor = 1
        temp = 0
        for a in self.calibrations[direction]:
            if angle >= a:
                temp = self.calibrations[direction][a]
                continue
            if angle <= a:
                print(a)
                duration = angle * (temp + self.calibrations[direction][a]) / 2
                break
                
#         duration = self.calibrations[direction] * angle * correction_factor
        start_time = time.time()
        while time.time() - start_time < duration:
            self.steer(current_speed, direction, 100)

            
    def move(self, speed):
        if not self.check_if_near_obstacle(speed):
            self.m_r.move(True, speed)
            self.m_l.move(True, speed)
            return True
        else:
            self.stop()
            return False
        
    def keep_straight(self, speed, ):
        angle = self.mpu.get_drift_by_duration(0.0001)
#         print("angle: {}".format(angle))
        if self.check_if_near_obstacle(speed):
            return -1000
        self.angle_sum += angle
#         print("angle sum: " + str(self.angle_sum))
        if self.angle_sum > 0.3:
            self.steer_by_angle(speed, "left", self.angle_sum)
        if self.angle_sum < -0.3:
            self.steer_by_angle(speed, "right", abs(self.angle_sum))
            
        if angle > 0:
            self.steer_by_angle(speed, "left", angle)
        else:
            self.steer_by_angle(speed, "right", abs(angle))
        return angle

        
    def stop(self):
        self.m_r.stop()
        self.m_l.stop()
    
    def destroy(self):
        self.m_r.destroy()
        self.m_l.destroy()

    def check_if_near_obstacle(self, speed):
        distance = self.ultrasonic.get_distance()
        status = distance < speed * self.min_distance/50
        if status:
            self.distance_check = not self.distance_check
            print(distance)
            return not self.distance_check
        self.distance_check = False
        return status
    
    def verify_ditance_at_rest(self):
        distance = self.ultrasonic.get_distance()
        return distance < self.min_distance




