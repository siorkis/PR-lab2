from this import d
from flask import Flask, request
import threading
import producer
import sender
import json
import random
import time
import requests

app = Flask(__name__)
producers = [producer.Producer(i, "free", []) for i in range(1, 11)]
senders = [sender.Sender(i) for i in range(1, 5)]


def sendData():
    
    payload = {"data": "ready"}
    print(payload, "PAYLOAD")
    post = requests.post("http://26.249.68.98:6000/order", json = payload)
    print(payload, "data has been sended to Agr")
    
    # time.sleep(10)

@app.route('/distribution', methods=['POST'])
def send():    
    data = request.get_json()
    print(data, "DATA POST")

    print("data has been received from Agr")
    return "data has been received from Agr"

    
if __name__ == '__main__':
    # app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False)
    flask_thread = threading.Thread(target=lambda: app.run(debug=False, host="0.0.0.0", port=5000, use_reloader=False))

    threads = list()
    threads.append(flask_thread)
    for index in range(6):
        print("Main    : create and start thread.", index)
        x = threading.Thread(target=sendData, args=())
        threads.append(x)

    for index, thread in enumerate(threads):
        print("Main    : before joining thread.", index)
        thread.start()
        print("Main    : thread done", index)