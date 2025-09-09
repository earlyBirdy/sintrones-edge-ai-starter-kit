import os
import time

def log_training_progress(metrics):
    log_dir = os.path.join("logs", "training")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    log_path = os.path.join(log_dir, f"train_{timestamp}.log")
    with open(log_path, "w") as f:
        for key, val in metrics.items():
            f.write(f"{key}: {val}\n")