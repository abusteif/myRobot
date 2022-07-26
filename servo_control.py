from flask import Flask, request
from adafruit_servokit import ServoKit
import time 
kit = ServoKit(channels=16)

app = Flask(__name__)

@app.route('/')
def initialize():
    return "ok"

@app.route('/angle',methods = ['GET'])
def set_angle():
    angle = request.args.get("angle")
    kit.servo[0].angle = int(angle)
    return "OK"

@app.route('/control', methods = ['POST'])
def control():
    data = request.get_json()
    servo_id = data.get('id')
    angle = data.get('angle')
    kit.servo[servo_id].angle = int(angle)
    return "ok"

  


app.run(debug=True, port=5001)
