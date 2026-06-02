#!/usr/bin/env python3
"""Write a local demo session status without invoking an AI coding client."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import time


parser = argparse.ArgumentParser()
parser.add_argument(
    "state", choices=["idle", "working", "waiting", "completed", "error"]
)
args = parser.parse_args()

path = Path.home() / ".ai-traffic-light" / "sessions" / "demo.json"
path.parent.mkdir(parents=True, exist_ok=True)
if args.state == "idle":
    path.unlink(missing_ok=True)
else:
    timestamp = int(time.time())
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
        created_at = existing.get("created_at") or existing.get("timestamp") or timestamp
    except (OSError, json.JSONDecodeError):
        created_at = timestamp
    path.write_text(
        json.dumps(
            {
                "client": "codebuddy",
                "state": args.state,
                "message": "Local demo",
                "timestamp": timestamp,
                "created_at": created_at,
            }
        ),
        encoding="utf-8",
    )
