from dc_motor_control import *
from configs import *

d = DCMotor(dc_m_1)
while True:
    d.move( True,0)