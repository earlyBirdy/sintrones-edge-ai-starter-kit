import os
from logger import frame_logger
import numpy as np

def test_save_frame_with_metadata(tmp_path):
    img = (np.ones((100, 100, 3)) * 255).astype(np.uint8)
    meta = {"test": "value"}
    frame_logger.save_frame_with_metadata(img, meta, output_dir=tmp_path)
    files = os.listdir(tmp_path)
    assert any(f.endswith(".jpg") for f in files)
    assert any(f.endswith(".json") for f in files)