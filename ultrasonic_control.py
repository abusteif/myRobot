import RPi.GPIO as GPIO
import time
from configs import trigger_pin, echo_pin

class UltrasonicControl:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
    
    def get_distance(self):
        # set Trigger to HIGH
        GPIO.output(self.trigger_pin, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)
     
        start_time = time.time()
        beginning = start_time
        stop_time = time.time()
     
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
            if start_time - beginning > 0.08:
                print("error in distance")
                return 127
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()

        time_elapsed = stop_time - start_time
        distance = (time_elapsed * 34300) / 2
#         print("distance: " + str(distance))
    
        return distance
    
if __name__ == '__main__':
    u = UltrasonicControl(trigger_pin, echo_pin)
    try:
        while True:
            dist = u.get_distance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
