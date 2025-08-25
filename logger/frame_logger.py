import os
import cv2
import json
from datetime import datetime

def save_frame_with_metadata(image, metadata, output_dir="logs"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    img_path = os.path.join(output_dir, f"{timestamp}.jpg")
    meta_path = os.path.join(output_dir, f"{timestamp}.json")
    cv2.imwrite(img_path, image)
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)