#!/usr/bin/env python3
import argparse, time, json, uuid, pathlib, os, sys
import numpy as np
import cv2
import paho.mqtt.client as mqtt

MQTT_HOST, MQTT_PORT = "localhost", 1883
TOPIC_DET = "factory/vision/detections"

def preprocess_bgr(img, size=(640,640)):
    ih, iw = img.shape[:2]
    scale = min(size[0]/ih, size[1]/iw)
    nh, nw = int(ih*scale), int(iw*scale)
    resized = cv2.resize(img, (nw, nh))
    canvas = np.full((size[0], size[1], 3), 114, dtype=np.uint8)
    canvas[:nh, :nw] = resized
    blob = canvas[:, :, ::-1].transpose(2,0,1)[None].astype(np.float32)/255.0
    return blob, scale

def dummy_postprocess(outputs, scale, conf_th=0.5):
    out = outputs[0] if isinstance(outputs, (list, tuple)) else outputs
    dets = []
    if out is None: return dets
    out = np.array(out)
    for row in out:
        if row.shape[-1] < 6: continue
        x,y,w,h,score,cls = row[:6]
        if score < conf_th: continue
        dets.append({
            "cls": str(int(cls)), "score": float(score),
            "bbox": [float(x/scale), float(y/scale), float(w/scale), float(h/scale)]
        })
    return dets

def ensure_model(path):
    if path and os.path.exists(path):
        return path
    print(f"[vision] WARNING: model not found at {path!r}. Running in MOCK mode (synthetic detections).", file=sys.stderr)
    return None

def main():
    ap = argparse.ArgumentParser()
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--camera", type=int, help="OpenCV camera index")
    src.add_argument("--video", type=str, help="Video file path")
    ap.add_argument("--model", required=False, default="models/defect_detector.onnx", help="ONNX model path")
    ap.add_argument("--name", default="lineA-cam01", help="Source camera name")
    ap.add_argument("--media-dir", default="data/media/lineA-cam01", help="Where to store event frames")
    ap.add_argument("--conf", type=float, default=0.5, help="Confidence threshold")
    ap.add_argument("--fps-limit", type=float, default=0.0, help="Max FPS (0 = unlimited)")
    args = ap.parse_args()

    media_dir = pathlib.Path(args.media_dir); media_dir.mkdir(parents=True, exist_ok=True)
    model_path = ensure_model(args.model)

    sess = None; input_name = None
    if model_path:
        try:
            import onnxruntime as ort
            sess = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
            input_name = sess.get_inputs()[0].name
        except Exception as e:
            print("[vision] WARNING: onnxruntime failed, falling back to MOCK. Error:", e, file=sys.stderr)

    cli = mqtt.Client(); cli.connect(MQTT_HOST, MQTT_PORT, 60); cli.loop_start()

    cap = cv2.VideoCapture(args.camera if args.camera is not None else args.video)
    if not cap.isOpened():
        raise RuntimeError("Unable to open camera/video source")

    try:
        last = time.time()
        while True:
            ok, frame = cap.read()
            if not ok: break
            blob, scale = preprocess_bgr(frame)

            if sess is not None and input_name is not None:
                outputs = sess.run(None, {input_name: blob})
                dets = dummy_postprocess(outputs, scale, conf_th=args.conf)
            else:
                dets = [{"cls":"mock_defect","score":0.85,"bbox":[100,120,80,60]}] if int(time.time()) % 5 == 0 else []

            frame_id = f"f_{uuid.uuid4().hex[:8]}"
            img_path = ""
            if dets:
                img_path = str((media_dir / f"{frame_id}.jpg").resolve())
                cv2.imwrite(img_path, frame)

            payload = {
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "source": args.name,
                "frame_id": frame_id,
                "detections": dets,
                "image_path": f"file://{img_path}" if img_path else ""
            }
            cli.publish(TOPIC_DET, json.dumps(payload), qos=0)

            if args.fps_limit > 0:
                dt = time.time() - last
                min_dt = 1.0/args.fps_limit
                if dt < min_dt:
                    time.sleep(min_dt - dt)
                last = time.time()
    except KeyboardInterrupt:
        pass
    finally:
        cap.release(); cli.loop_stop()

if __name__ == "__main__":
    main()
