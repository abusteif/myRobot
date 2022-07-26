import requests, time, json
from adafruit_led_animation.color import *

# print(requests.get("http://127.0.0.1:5000/"))

# print(requests.get("http://127.0.0.1:5000/start"))
body_chase = {
    "style": "chase",
    "color" : RED,
    "size": 3,
    "spacing": 10,
    "speed": 0.1,
    }
body_rainbow = {
    "style": "rainbow",
    "speed": 0.1,
    "period": 9,

    }

for _ in range(2):
    print(requests.post("http://127.0.0.1:5000/animation", data=json.dumps(body_chase),
                            headers = {'content-type':'application/json'}))
    time.sleep(2)
    print(requests.post("http://127.0.0.1:5000/animation", data=json.dumps(body_rainbow),
                        headers = {'content-type':'application/json'}))
    time.sleep(2)
    print(requests.post("http://127.0.0.1:5000/animation", data=json.dumps({"style":"solid", "color": BLUE}),
                        headers = {'content-type':'application/json'}))
    time.sleep(2)
print(requests.post("http://127.0.0.1:5000/animation", data=None))
print(requests.get("http://127.0.0.1:5000/stop"))
