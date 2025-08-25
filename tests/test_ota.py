from ota import model_switcher

def test_model_path_default():
    path = model_switcher.get_model_path_from_ota()
    assert isinstance(path, str)
    assert path.endswith(".onnx")