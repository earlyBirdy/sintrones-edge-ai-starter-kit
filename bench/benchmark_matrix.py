def run_matrix():
    return [
        {"engine":"onnxruntime","size":"640","fps":28,"latency_ms":35},
        {"engine":"openvino","size":"640","fps":34,"latency_ms":29},
        {"engine":"tensorrt","size":"640","fps":55,"latency_ms":12},
    ]
