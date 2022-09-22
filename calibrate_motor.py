from movement_control import *
from multiprocessing import Process, Manager
from collections import OrderedDict

from configs import *
import time
import json
import copy
from mpu6050_control import Mpu6050Control
mpu = Mpu6050Control()
time.sleep(1)

file_name = ""
def get_time(slope, intercept, angle):
    
    return (angle - intercept) / float(slope)

m = MovementControl(dc_m_1, dc_m_2, trigger_pin, echo_pin, mpu)
m.calibrate_mpu()

def main():
    global file_name
    decision = raw_input("[C]alibrate or use [E]xisting calibration? ")
    file_name = raw_input("Enter surface name: ")
    if decision == "E":
        with open(file_name + ".json", "r") as f:
            sd = json.load(f)
            
        while True:
            angle = int(raw_input("angle: "))
            d = raw_input("direction: ")
            sorted_keys = copy.deepcopy(list(sd[d].keys()))
            for k_index, k in enumerate(sorted_keys):
                sorted_keys[k_index] = float(k) 
            sorted_keys.sort()
            old_s = 0
            if angle < sorted_keys[0]:
                old_s = sorted_keys[0]
            else:
                for s in sorted_keys:
                    if angle > s:
                        old_s = s
                        continue
                    break
            print(old_s)
            t = get_time(int(sd[d][str(old_s)]["slope"]), int(sd[d][str(old_s)]["intercept"]), angle)
            m.steer(0,d,100)
            time.sleep(t)
            m.stop()
    elif decision == "C":
        return
    else:
        exit()
        
main()

def mpu_operations(q, m):
    values = OrderedDict()
    while True:
        try:
            command = q.get(block=True)
            if command == "end":
                times = []
                angles = []
                for v in values:
                    times.append(v)
                    angles.append(round(values[v],1))
                q.put((times, angles, d))
                values = OrderedDict()
                continue
                    
            t = command[0]
            r = command[1]
            r_all = command[2]
            d = command[3]
#             extra_time = m.check_for_movement()
            angle = m.get_real_time_angle()
            if r == 1:
                values[t] = angle
            else:
                values[t] = values[t] + angle
            if r == r_all:
                values[t] = values[t] / r
                print("(" + str(t) + "," + str(values[t]) + ")")
                
                
                
        except Exception as e:
            print(e)
            pass

queue = Manager().Queue()
p = Process(target=mpu_operations, args=(queue, mpu))
p.start()


max_attempts = 2
times = [0.05, 0.06, 0.07, 0.08]
times_extra = [0.05] * 5

for t_index, t in enumerate(times_extra):
    times_extra[t_index] = t * t_index + 0.1
times = times + times_extra
lines = {}
for direction in ["right","left"]:
    for repeat in range(1,max_attempts):
        print("repeat: "+ str(repeat))
        for i in times:
            queue.put((i, repeat, max_attempts - 1, direction))
            time.sleep(1)
            m.steer(0,"right",100)
            time.sleep(i)
            m.stop()
            time.sleep(2)
    queue.put("end")
    while True:
        command = queue.get(block=True)
       
        times, angles, d = command
        lines[d] = OrderedDict()

        for t_index, t in enumerate(times):
            if t_index == len(times) - 1:
                break
            slope = (angles[t_index + 1] - angles[t_index]) / (times[t_index + 1] - t)
            lines[d][angles[t_index]] = {"slope": slope}
            lines[d][angles[t_index]]["intercept"] = angles[t_index] - slope * t
        with open(file_name + ".json", "w") as f:
            json.dump(lines, f)
        break


while True:
    
    angle = input("angle: ")
    d = input("direction: ")
    old_s = 0
    if angle < list(lines[d].keys())[0]:
        old_s = list(lines[d].keys())[0]
    else:
        for s in lines[d]:
            if angle > s:
                old_s = s
                continue
            break
    print(old_s)
    t = get_time(lines[d][old_s]["slope"], lines[d][old_s]["intercept"], angle)    
    m.steer(0,"right",100)
    time.sleep(t)
    m.stop()

p.terminate()



   

