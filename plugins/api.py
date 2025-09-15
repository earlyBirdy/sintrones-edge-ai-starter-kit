from typing import Callable, Dict, List
REGISTRY: Dict[str, Callable] = {}

def register(name: str):
    def deco(fn: Callable):
        REGISTRY[name]=fn; return fn
    return deco

def available()->List[str]: return list(REGISTRY.keys())
