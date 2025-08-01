# Factory Automation Example
# Reads sensor data and applies basic inference or alerts

def read_sensor():
    # Simulated Modbus or GPIO reading
    return {"temp": 78.3, "vibration": 0.08}

def process_data(sensor_data):
    if sensor_data["temp"] > 75:
        return "Warning: High temperature detected"
    return "System normal"

if __name__ == "__main__":
    sensor_data = read_sensor()
    status = process_data(sensor_data)
    print(status)
