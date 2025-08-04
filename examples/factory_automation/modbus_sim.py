import time
import random

def read_sensor():
    return {
        "temperature": round(random.uniform(65, 85), 2),
        "vibration": round(random.uniform(0.01, 0.2), 3)
    }

if __name__ == "__main__":
    while True:
        print("Sensor Reading:", read_sensor())
        time.sleep(2)
