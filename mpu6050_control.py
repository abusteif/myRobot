from mpu6050 import mpu6050
import time
import math
from collections import Counter

class Mpu6050Control:
    
    def __init__(self):
        self.mpu = mpu6050(0x68)
        self.calibration = None
    
    def get_smoothed_values(self, n_samples=10):

        result = {}
        for _ in range(n_samples):
            data = self.mpu.get_gyro_data()
            for k in data.keys():

                result[k] = result.get(k,0) + (data[k] / n_samples)

        if self.calibration:
            for k in self.calibration.keys():
                result[k] -= self.calibration[k]
        return result

    def calibrate(self, threshold=50, n_samples=100):
        while True:
            v1 = self.get_smoothed_values(n_samples)
            v2 = self.get_smoothed_values(n_samples)
            if all(abs(v1[k] - v2[k]) < threshold for k in v1.keys()):
                self.calibration = v1
                return

    def get_drift_by_duration(self, duration):
        if not self.calibration:
            return "Please calibrate first"
        d = 0
        begin = time.perf_counter()

        while time.perf_counter()- begin < duration:
            start = time.perf_counter()
            data = self.mpu.get_gyro_data()
            end = time.perf_counter() - start
            d += (data["x"] - self.calibration["x"]) * end
            
        return d
    
    def check_for_movement(self):
        begin = 0
        counter = 0
        angles = []
        while True:
            angle = self.mpu.get_gyro_data()["x"] - self.calibration["x"]
            print(angle)
            if abs(angle) >= 3:
                break
            
        old_angle = angle
        while abs(angle) > 2:
            angle = self.mpu.get_gyro_data()["x"] - self.calibration["x"]
            print(angle)
            if begin:
                continue 
            if angle - old_angle < -1:
                if angle - old_angle < -5:
                    begin = time.perf_counter()
                    continue
                if counter < 3:
                    counter += 1
                else:
                    print("We are stopping")
                    begin = time.perf_counter()
            else:
                counter = 0
              
            old_angle = angle

        return time.perf_counter() - begin
    
    def control_angle(self, angle, call_back, calibration_factor):
        if not self.calibration:
            return "Please calibrate first"
        d = 0
        begin = time.perf_counter()

        while True:
            start = time.perf_counter()
            data = self.mpu.get_gyro_data()
            end = time.perf_counter() - start
            d += (data["x"] - self.calibration["x"]) * end
            if d >= angle * calibration_factor :
                time_elapsed = time.perf_counter() - begin
                call_back()
                return time_elapsed

    def get_real_time_angle(self):
        if not self.calibration:
            return "Please calibrate first"
        d = 0
        begin = time.time()
        angles_values = []
        angles = []
        while True:
            start = time.time()
            while True:
                try:
                    data = self.mpu.get_gyro_data()
                    break
                except Exception as e:
                    print("error")
                    
                    print(e)
                
            
            end = time.time() - start
            if data["x"] > 0:
                angles_values.append((data["x"], end))
                angles.append(int(math.ceil(data["x"])))
            d += (data["x"] - self.calibration["x"]) * end
            
            if time.time() - begin > 3:
#                 print("\t" + str(d) + ")")
                return d
#                 data = Counter(angles)
#                 peak = max(angles, key=data.get)
#                 print("max: " + str(peak))
               
                break
            
    def get_time_by_angle(self, angle):
        if not self.calibration:
            return "Please calibrate first"
        d = 0
        start = time.time()
        while abs(d) < angle:
            b = time.time()
            data = self.mpu.get_gyro_data() 
            end = time.time() - b
            d += (data["x"] - self.calibration["x"]) * end
#             print(d)
        return time.time() - start
