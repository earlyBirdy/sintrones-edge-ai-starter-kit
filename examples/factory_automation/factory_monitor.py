# Create a monitor loop the runtime can call
import time
from . import modbus_sim
from src.model import detect_anomaly

def run_monitor(poll=2):
    print("[MONITOR] Starting factory monitor loop…")
    while True:
        data = modbus_sim.read_sensor()   # {"temperature":..,"vibration":..}
        bad = detect_anomaly(data)        # uses your model stub
        if bad:
            print(f"[ALERT] Anomaly: {data}")
        else:
            print(f"[OK] {data}")
        time.sleep(poll)

if __name__ == "__main__":
    run_monitor()
