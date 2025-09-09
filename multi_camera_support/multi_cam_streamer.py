import os

def get_mock_camera_feeds():
    base_dir = os.path.join("logs", "feeds")
    return [
        os.path.join(base_dir, "cam1_feed.jpg"),
        os.path.join(base_dir, "cam2_feed.jpg"),
        os.path.join(base_dir, "cam3_feed.jpg"),
    ]