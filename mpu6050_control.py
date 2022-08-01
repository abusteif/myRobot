from mpu6050 import mpu6050
import time

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
        begin = time.time()

        while time.time()- begin < duration:
            start = time.time()
            data = self.mpu.get_gyro_data()
            end = time.time() - start
            d += (data["x"] - self.calibration["x"]) * end
        return d

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
            
        return time.time() - start
