from flask import Flask, request
import requests
import consumer
import random 
import threading 
import json
import time

app = Flask(__name__)

# 1st resources 
data_pool = []

# 2nd resources
back_data = []

threads = list()

@app.route('/order2', methods=['POST'])
def answer():
    global data_pool
    global back_data

    res = request.get_json()
   
    back_data.append(res["data"])
    print("data has been received from Cons")
    if back_data[0] == "steady":
        payload = {"data" : "bang"}
    back_data.pop(0)
    post = requests.post("http://26.249.68.98:5000/distribution", json = payload)
    print(payload, "data has been sended to Pro")
    return "data has been sended to Pro"
    

# payload = {"data": "ready"}

@app.route('/order', methods=['POST'])
def send():
    res = request.get_json()
    data_pool.append(res["data"])
    print(res, "data has been received from Pro")
    return "data has been received from Pro"


def send_to_consumer(index_eater):
    global data_pool
    global back_data
    
    while True:
        if (len(data_pool) == 0):
            time.sleep(1)
            # print(data_pool, "data pool")
            continue
        
        payload = {"data" : data_pool[0]}
        data_pool.pop(0)
        post = requests.post("http://26.249.68.98:7000/consumer", json = payload)
        print(payload, "data has been sended to Cons")
                
  

# python app.py

if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=6000, use_reloader=False)
    
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, host="0.0.0.0", port=6000, use_reloader=False))

    threads = list()
    threads.append(flask_thread)
    for index in range(4):
        iterable = [index]
        print("Main    : create and start thread.", index)
        x = threading.Thread(target=send_to_consumer, args=(iterable))
        threads.append(x)
    
    for index, thread in enumerate(threads):
        print("Main    : before joining thread.", index)
        thread.start()
        print("Main    : thread done", index)
