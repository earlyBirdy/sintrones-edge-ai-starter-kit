#!/usr/bin/env python3
"""Generate a small ONNX model via PyTorch.
Requires: pip install torch
Output: models/defect_detector.onnx
"""
from pathlib import Path
import torch
import torch.nn as nn

class DummyDefectDetector(nn.Module):
    def __init__(self):
        super().__init__()
        # Very small MLP: 10 -> 6 to match [x,y,w,h,score,cls]
        self.fc = nn.Linear(10, 6)

    def forward(self, x):
        # Clamp score to 0..1 and class to non-negative
        y = self.fc(x)
        y[..., 4] = torch.sigmoid(y[..., 4])   # score
        y[..., 5] = torch.relu(y[..., 5])      # cls id-ish
        return y

if __name__ == "__main__":
    model = DummyDefectDetector().eval()
    dummy = torch.randn(1, 10)
    out = Path("models") / "defect_detector.onnx"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(
        model, dummy, out,
        input_names=["input"], output_names=["detections"],
        dynamic_axes={"input": {0: "batch"}, "detections": {0: "batch"}},
        opset_version=11
    )
    print("✅ Wrote", out.resolve())
