import random
def run_matrix(sizes=("320","480","640","960"), engines=("onnxruntime","openvino","tensorrt")):
    rows=[]
    for s in sizes:
        for e in engines:
            base={"onnxruntime":25,"openvino":32,"tensorrt":55}[e]
            jitter=random.uniform(-3,3)
            fps=max(5.0, base + jitter - (int(s)/640)*5)
            latency=max(5.0, 1000.0/max(1.0,fps))
            rows.append({"engine":e,"size":s,"fps":round(fps,1),"latency_ms":round(latency,1)})
    return rows
