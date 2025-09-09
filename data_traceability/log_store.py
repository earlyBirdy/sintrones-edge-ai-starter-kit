import os
import json
from datetime import datetime

def store_log(data):
    log_dir = os.path.join("logs", "inference")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{timestamp}_log.json")
    with open(log_file, "w") as f:
        json.dump(data, f, indent=4)