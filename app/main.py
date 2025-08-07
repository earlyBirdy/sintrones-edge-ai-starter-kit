# main.py
"""
Main entry point for Sintrones Edge AI Starter Kit
Includes runtime hooks for factory/city/vehicle applications
"""

import argparse
from src import edge_runtime
from dashboard import app_factory

def run_app(mode="factory"):
    print(f"[INFO] Launching Edge AI Kit in '{mode}' mode")

    if mode == "factory":
        edge_runtime.start_factory_monitor()
    elif mode == "dashboard":
        app_factory.launch_dashboard()
    elif mode == "test":
        print("[INFO] Running in test mode")
    else:
        print("[ERROR] Unsupported mode:", mode)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sintrones Edge AI Kit")
    parser.add_argument("--mode", default="factory", help="Mode: factory | dashboard | test")
    args = parser.parse_args()

    run_app(mode=args.mode)
