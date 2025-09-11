import os, glob

def list_rules(rule_dir="recipes/rules"):
    os.makedirs(rule_dir, exist_ok=True)
    return [{"rule_file":p} for p in glob.glob(os.path.join(rule_dir,"*.yaml"))]
