from mpu6050 import mpu6050
import time
mpu = mpu6050(0x68)
from movement_control import MovementControl
from configs import dc_m_1, dc_m_2, camera_servo_pin, image_width
import time
from mpu6050_control import Mpu6050Control
m = MovementControl(dc_m_1, dc_m_2, mpu)

time.sleep(2)
def get_smoothed_values(n_samples=10, calibration=None):
    """
    Get smoothed values from the sensor by sampling
    the sensor `n_samples` times and returning the mean.
    """
    result = {}
    for _ in range(n_samples):
        data = mpu.get_gyro_data()
        for k in data.keys():

            result[k] = result.get(k,0) + (data[k] / n_samples)

    if calibration:
        for k in calibration.keys():
            result[k] -= calibration[k]
    return result

def calibrate(threshold=50, n_samples=100):
    """
    Get calibration date for the sensor, by repeatedly measuring
    while the sensor is stable. The resulting calibration
    dictionary contains offsets for this sensor in its
    current position.
    """
    while True:
        v1 = get_smoothed_values(n_samples)
        v2 = get_smoothed_values(n_samples)
        # Check all consecutive measurements are within
        # the threshold. We use abs() so all calculated
        # differences are positive.
        if all(abs(v1[k] - v2[k]) < threshold for k in v1.keys()):
            return v1  # Calibrated.

def get_angle(duration, cal):
    d = 0
    begin = time.time()
    start = time.time()

    while time.time()- begin < duration:
        start = time.time()
        data = mpu.get_gyro_data() 
        end = time.time() - start
        d += (data["x"] - cal["x"]) * end
    return (float(d)/duration)

calibration = calibrate()

current_angle = 0
while True:
    m.steer(100,"right",100)
    new_angle = get_angle(0.5, calibration)
    if abs(new_angle) > 0.5: 
        current_angle += new_angle
        if abs(current_angle) > 720:
            current_angle = abs(current_angle) - 720
    print(current_angle/2)
# calibration = calibrate()
# count = 10
# d = 0
# start = time.time()
# elapsed = time.time()
# while True:
#     start = time.time()
#     data = get_smoothed_values(n_samples=1, calibration=calibration)
#     data = mpu.get_gyro_data() 
#     end = time.time() - start
#     print(end)
#     d += (data["x"] - calibration["x"]) * end
#     count -= 1
#     print(time.time() - elapsed)
#     if time.time() - elapsed > 0.5:
#         print(float(d)/(end))
#         elapsed = time.time()
#         d = 0

# 
#     if end:
#         print(float(d)/(end))
#         count = 20
#         d = 0



