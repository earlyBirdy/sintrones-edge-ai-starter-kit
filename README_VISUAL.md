# Visual Inspection Add-on

Drop these files into your repo to enable smart factory visual QA.

**Files**
- `examples/vision_inspection/camera_infer.py` – camera/video → ONNX inference → MQTT detections
- `models/` – put `defect_detector.onnx` here
- `src/decision_engine/rules.py` – adds `defects_per_frame` rule
- `src/decision_engine/policies.example.visual.yaml` – merge into your `policies.yaml`

**Requirements to add**
```
opencv-python
onnxruntime
paho-mqtt
```

**Run**
```bash
# Publish detections from camera or video
python examples/vision_inspection/camera_infer.py --model models/defect_detector.onnx --camera 0

# Collector should already be running to write JSONL
python -m src.cli collect --config configs/config.yaml

# Batch to Parquet
python -m src.cli batch --config configs/config.yaml
```
