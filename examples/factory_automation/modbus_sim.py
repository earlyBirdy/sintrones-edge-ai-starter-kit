# Simulated Modbus sensor reading
import time
import random

def get_modbus_data():
    return {
        "temperature": round(random.uniform(65, 85), 2),
        "vibration": round(random.uniform(0.01, 0.2), 3)
    }

if __name__ == "__main__":
    while True:
        data = get_modbus_data()
        print("Modbus Data:", data)
        time.sleep(2)
