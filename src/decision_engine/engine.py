#!/usr/bin/env python3
"""Decision Engine Stub
Evaluates events and returns an action decision.
Replace with rules/ML hybrid as needed.
"""
from typing import Dict, Any

DEFAULT_THRESHOLD = 0.8  # placeholder

def evaluate(event: Dict[str, Any]) -> Dict[str, Any]:
    """Return a simple pass/alert decision based on a score field in event."""
    score = float(event.get("score", 0.0))
    if score >= DEFAULT_THRESHOLD:
        return {"action": "alert", "reason": f"score {score} >= {DEFAULT_THRESHOLD}"}
    return {"action": "pass", "reason": f"score {score} < {DEFAULT_THRESHOLD}"}
