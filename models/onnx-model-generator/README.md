# ONNX Model Generator (Ready-to-Run)

Two ways to create a tiny, runnable ONNX model for your pipeline tests.

## Option A — Pure ONNX (no PyTorch needed)
```bash
python generate_dummy_onnx_with_onnx.py
# -> writes models/defect_detector.onnx
```

## Option B — PyTorch → ONNX
```bash
pip install torch  # if not already installed
python generate_dummy_onnx_with_torch.py
# -> writes models/defect_detector.onnx
```

## Quick test (mock-capable camera script)
```bash
pip install onnxruntime opencv-python paho-mqtt
python camera_infer_mock_fallback.py --camera 0
# or:
python camera_infer_mock_fallback.py --video path/to/sample.mp4
# or force a real model:
python camera_infer_mock_fallback.py --model models/defect_detector.onnx --camera 0
```
