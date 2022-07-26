from movement_control import MovementControl
from mpu6050_control import Mpu6050Control

from configs import dc_m_1, dc_m_2, camera_servo_pin, image_width,face_detect_status_led
mpu = Mpu6050Control()
m = MovementControl(dc_m_1, dc_m_2, mpu)
m.stop()
m.destroy()