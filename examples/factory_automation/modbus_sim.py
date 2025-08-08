# Keep read_sensor(), and ADD:
import time, random

def read_sensor():
    return {
        "temperature": round(random.uniform(65, 85), 2),
        "vibration": round(random.uniform(0.01, 0.2), 3)
    }

def run_simulation(interval=2):
    while True:
        print("[MODBUS] Sensor Reading:", read_sensor())
        time.sleep(interval)

if __name__ == "__main__":
    run_simulation()
