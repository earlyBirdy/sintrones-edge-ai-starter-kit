# Basic anomaly detection
def detect_anomaly(data):
    return data['temperature'] > 75 or data['vibration'] > 0.15
