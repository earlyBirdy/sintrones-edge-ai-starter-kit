import os, yaml

DEFAULT_STEPS=[{"op":"resize","params":{"w":640,"h":640}}, {"op":"infer","params":{"engine":"onnx"}}]

def export_pipeline(steps=DEFAULT_STEPS, out_path="recipes/pipeline.yaml"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path,"w") as f: yaml.safe_dump({"steps":steps}, f)
    return out_path
