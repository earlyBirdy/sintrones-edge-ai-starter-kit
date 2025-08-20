#!/usr/bin/env python3
"""Generate a tiny ONNX model that always outputs one detection row.

Output:
  models/defect_detector.onnx

Requires:
  pip install onnx
"""
import numpy as np
import onnx
from onnx import helper, TensorProto, numpy_helper

def build_model():
    const_vals = np.array([[100.0, 120.0, 80.0, 60.0, 0.9, 1.0]], dtype=np.float32)
    const_tensor = numpy_helper.from_array(const_vals, name="const_detections")
    # Dummy input (unused) to satisfy code that feeds input images
    input_tensor = helper.make_tensor_value_info('input', TensorProto.FLOAT, ['N', 3, 640, 640])
    output_tensor = helper.make_tensor_value_info('detections', TensorProto.FLOAT, [1, 6])
    const_node = helper.make_node('Constant', inputs=[], outputs=['detections'], value=const_tensor)
    graph_def = helper.make_graph([const_node], 'DummyDetectionGraph', [input_tensor], [output_tensor], initializer=[])
    model_def = helper.make_model(graph_def, opset_imports=[helper.make_operatorsetid("", 11)])
    onnx.checker.check_model(model_def)
    return model_def

if __name__ == "__main__":
    model = build_model()
    out = Path("models") / "defect_detector.onnx"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(model.SerializeToString())
    print("Wrote", out.resolve())
