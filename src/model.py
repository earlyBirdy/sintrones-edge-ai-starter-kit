# Dummy model for demonstration
def detect_anomaly(sensor_data):
    return sensor_data.get("temperature", 0) > 75 or sensor_data.get("vibration", 0) > 0.15
