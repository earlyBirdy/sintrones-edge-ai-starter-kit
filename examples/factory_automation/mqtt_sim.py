# Simulated MQTT publisher
import paho.mqtt.client as mqtt
import time
import random
import json

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    payload = {
        "temperature": round(random.uniform(65, 85), 2),
        "vibration": round(random.uniform(0.01, 0.2), 3)
    }
    client.publish("factory/sensor", json.dumps(payload))
    print("Published:", payload)
    time.sleep(3)
