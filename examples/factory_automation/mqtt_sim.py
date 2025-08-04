import paho.mqtt.client as mqtt
import time
import json
import random

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    data = {
        "temperature": round(random.uniform(65, 85), 2),
        "vibration": round(random.uniform(0.01, 0.2), 3)
    }
    client.publish("factory/sensor", json.dumps(data))
    print("Published:", data)
    time.sleep(3)
