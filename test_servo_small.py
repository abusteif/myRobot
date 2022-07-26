import requests, time, json

print(requests.post("http://127.0.0.1:5001/control",
                data=json.dumps({"id": 7, "angle": 0}),
                headers = {'content-type':'application/json'}))
state = True

# while True:
#     num2 = 3 if state else 4
#     num1 = 4 if state else 3
#     for i in range(10):
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": num1, "angle": 95 - i}),
#                         headers = {'content-type':'application/json'}))
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": num2, "angle": 85 + i}),
#                         headers = {'content-type':'application/json'}))
#         time.sleep(0.5)
#     state = not state

# while True:
#     for i in range(90):
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 0, "angle": 30 + i}),
#                         headers = {'content-type':'application/json'}))
#         time.sleep(0.1)
#     for i in range(90):
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 0, "angle": 110 - i}),
#                         headers = {'content-type':'application/json'}))
#         time.sleep(0.1)
#         
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 3, "angle": 60 + i}),
#                         headers = {'content-type':'application/json'}))
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 4, "angle": 120 - i}),
#                         headers = {'content-type':'application/json'}))
#         time.sleep(0.1)
#     for i in range(60):
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 0, "angle": 110 - i}),
#                         headers = {'content-type':'application/json'}))
#         
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 3, "angle": 120 - i}),
#                         headers = {'content-type':'application/json'}))
#         print(requests.post("http://127.0.0.1:5001/control",
#                         data=json.dumps({"id": 4, "angle": 60 + i}),
#                         headers = {'content-type':'application/json'}))
#         time.sleep(0.1)
        
