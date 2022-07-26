import RPi.GPIO as GPIO
import time

class DCMotor:
    def __init__(self, dc_m):
        self.enable = dc_m["en"]
        self.dir_a = dc_m["dir_a"]
        self.dir_b = dc_m["dir_b"]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.enable, GPIO.OUT)
        GPIO.setup(self.dir_a, GPIO.OUT)
        GPIO.setup(self.dir_b, GPIO.OUT)
        GPIO.output(self.enable, False)
        GPIO.output(self.dir_a, False)
        GPIO.output(self.dir_b, False)

        self.pwm = GPIO.PWM(self.enable, 100)
        self.pwm.start(0)

    def move(self, forward, speed):
        GPIO.output(self.dir_a, forward)
        GPIO.output(self.dir_b, not forward)
        self.pwm.ChangeDutyCycle(speed)
        
    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        
    def destroy(self):
        self.pwm.stop()
        GPIO.cleanup()
if __name__ == "__main__":
    m1 = DCMotor(18, 23, 24)
    m2 = DCMotor(25, 8, 7)

    while True:
        dir1 = input("Direction 1 - f/b: ")
        speed1 = input("Speed 1: ")
        dir2 = input("Direction 2 - f/b: ")
        speed2 = input("Speed 2: ")
        
        dir1 = dir1 == "f"
        dir2 = dir2 == "f"
        
        m1.move(dir1, int(speed1))
        m2.move(dir2, int(speed2))

        time.sleep(5)
        m1.stop()
        m2.stop()
        
    m1.destroy()
    m2.destroy()
