# ADD THIS instead of the top-level while True loop
import paho.mqtt.client as mqtt
import time, json, random

def run_simulation(broker="localhost", port=1883, topic="factory/sensor", interval=3):
    client = mqtt.Client()
    client.connect(broker, port, 60)
    while True:
        data = {
            "temperature": round(random.uniform(65, 85), 2),
            "vibration": round(random.uniform(0.01, 0.2), 3)
        }
        client.publish(topic, json.dumps(data))
        print("[MQTT] Published:", data)
        time.sleep(interval)

if __name__ == "__main__":
    run_simulation()
