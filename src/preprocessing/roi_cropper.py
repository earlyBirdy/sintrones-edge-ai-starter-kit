
# Region of Interest Cropper
def crop_roi(frame, x=100, y=100, w=300, h=300):
    return frame[y:y+h, x:x+w]
