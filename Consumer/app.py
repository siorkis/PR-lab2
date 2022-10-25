from flask import Flask, request
import requests
import consumer
import random 
import threading 
import json
import time

app = Flask(__name__)

items_received = []


# payload = {
#       "producer_id": id[Consumer.counter],
#       "items": message[Consumer.counter]
#     }

@app.route('/consumer', methods=['POST'])
def answer():
    
    global items_received
    data = request.get_json()
    items_received.append(data["data"])
 
    print(data, "data has been received from Agr")
    return "data has been received from Agr"

def send_to_agregator(index_eater):
    global items_received

    while True:
        if (len(items_received) == 0):
            time.sleep(1)
            continue
        
        if items_received[0] == "ready":
            payload = {"data" : "steady"}
        post = requests.post("http://26.249.68.98:6000/order2", json = payload)
        if items_received:    
            items_received.pop(0)
 
        print(payload, "data has been sended to Agr")

        



if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=6000, use_reloader=False)
    
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, host="0.0.0.0", port=7000, use_reloader=False))

    threads = list()
    threads.append(flask_thread)
    for index in range(4):
        iterable = [index]
        print("Main    : create and start thread.", index)
        x = threading.Thread(target=send_to_agregator, args=(iterable))
        threads.append(x)
    
    for index, thread in enumerate(threads):
        print("Main    : before joining thread.", index)
        thread.start()
        print("Main    : thread done", index)
