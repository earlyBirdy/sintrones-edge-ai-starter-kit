# src/edge_runtime.py

import time
import threading
from examples.factory_automation import factory_monitor
from examples import mqtt_sim, modbus_sim

def start_factory_monitor():
    print("[INFO] Starting factory monitor...")

    # Start simulated MQTT and Modbus publishers
    threading.Thread(target=mqtt_sim.run_simulation, daemon=True).start()
    threading.Thread(target=modbus_sim.run_simulation, daemon=True).start()

    # Start the main factory monitor loop
    try:
        factory_monitor.run_monitor()
    except KeyboardInterrupt:
        print("[INFO] Factory monitor stopped.")
    except Exception as e:
        print("[ERROR] Factory monitor failed:", str(e))

