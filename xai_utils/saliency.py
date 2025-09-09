import numpy as np
import cv2
import os

def save_saliency_map(image, output_path="logs/saliency_map.jpg"):
    """
    Dummy saliency map: grayscale + color overlay
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    heatmap = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    cv2.imwrite(output_path, heatmap)
    return output_path
