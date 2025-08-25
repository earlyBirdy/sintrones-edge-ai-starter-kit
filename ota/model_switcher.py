# model_switcher.py - Reads OTA JSON to switch ONNX model path
import json

def get_model_path_from_ota(ota_config="ota/update_control.json"):
    with open(ota_config, 'r') as f:
        cfg = json.load(f)
    return cfg.get("onnx_model_path", "models/defect_detector.onnx")