from flask import Flask, request
import board
import neopixel
import time
import threading
from threading import Thread
import queue

from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.solid import Solid

from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.color import *
from adafruit_led_animation.sequence import AnimationSequence

app = Flask(__name__)
pixel_pin = board.D21
   
pixel_num = 12
q = queue.Queue()

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

def listener(q):
    start_time = 0
    duration = 0
    while True:
        try:
            if q.empty():
                if animation and time.time() - start_time < duration: 
                    animation.animate()
                else:
                    pixels.fill((0,0,0))
                    pixels.show()                    
                    
            else:
                data = q.get()
                animation = data['animation']
                duration = data["duration"]
                start_time = time.time()
               
        except:
            pass

            
thread = Thread(target=listener, args=((q,)))
thread.start()

@app.route('/')
def initialize():
    return "ok"

@app.route('/animation', methods = ['POST'])
def change_animation():
    data = request.get_json()
    if not data:
        q.put({"animation": None})
        return "stopping"
    style = data.get('style')
    color = data.get('color')
    spacing = int(data.get('spacing', 0))
    speed = float(data.get('speed', 0))
    size = int(data.get('size', 0))
    period = int(data.get('period',0))
    tail_length = int(data.get('tail_length',0))
    bounce = data.get('bounce',0)
    num_sparkles = int(data.get('num_sparkles',0))
    duration = int(data.get('duration', 1000))

    if style == "chase":
        animation = {"animation": Chase(pixels, speed=speed, color=color, size=size, spacing=spacing)}
    if style == "rainbow_chase":
        animation = {"animation": RainbowChase(pixels, speed=speed, size=size, spacing=spacing)}
    if style == "rainbow":
        animation = {"animation": Rainbow(pixels, speed=speed, period=period)}
    if style == "pulse":
        animation = {"animation": Pulse(pixels, speed=speed, color=color, period=period)}
    if style == "comet":
        animation = {"animation": Comet(pixels, speed=speed, color=color, tail_length=tail_length, bounce=bounce)}
    if style == "rainbow_comet":
        animation = {"animation": RainbowComet(pixels, speed=speed, tail_length=tail_length, bounce=bounce)}
    if style == "rainbow_sparkle":
        animation = {"animation": RainbowSparkle(pixels, speed=speed, num_sparkles=num_sparkles)}
    
    if style == "solid":
        animation = {"animation": Solid(pixels, color=color)}
    animation["duration"] = duration
    q.put(animation)
    return "ok"

@app.route('/solid',methods = ['POST'])
def solid():
    global stop
    stop = True
    data = request.get_json()
    color = data.get('color')
    pixels.fill(color)
    pixels.show()
    return "i"
    
@app.route('/stop',methods = ['GET'])
def stop():
#     global stop
#     stop = True
    q.put({"animation": None})
    return "ok"


# def login():
#    if request.method == 'POST':
#       user = request.form['nm']
#       return redirect(url_for('success',name = user))
#    else:
#       user = request.args.get('nm')
#       return redirect(url_for('success',name = user))

app.run(debug=True)