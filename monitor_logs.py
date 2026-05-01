#!/usr/bin/env python3
"""Log monitoring agent to triage incidents via the /incident/analyze API (Phase 1).

Reads a log file, polls every 30 seconds for new content, and sends the latest
logs to the Incident Analyzer API. Prints results when severity is HIGH.
"""

import time
from typing import Optional
import os
import json
try:
    import requests
except Exception:
    requests = None


def read_new_logs(path: str, last_pos: int) -> tuple[str, int]:
    if not os.path.exists(path):
        return "", last_pos
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(last_pos)
        data = f.read()
        last_pos = f.tell()
    return data, last_pos


def analyze_logs_chunk(log_text: str, service: str = "log-monitor", environment: str = "prod", api_url: str = "http://localhost:8000/incident/analyze"):
    if requests is None:
        return {"error": "requests module not available"}
    payload = {
        "service": service,
        "environment": environment,
        "logs": log_text,
    }
    try:
        resp = requests.post(api_url, json=payload, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def main(log_path: str):
    print(f"Starting Incident monitor for {log_path}. Polling every 30 seconds.")
    last_pos = 0
    while True:
        logs, last_pos = read_new_logs(log_path, last_pos)
        if logs.strip():
            print("New logs detected, analyzing...")
            result = analyze_logs_chunk(logs)
            print("Incident analysis result:")
            print(json.dumps(result, indent=2))
            if isinstance(result, dict) and result.get("severity") == "HIGH":
                print("ALERT: HIGH severity detected from incident analyzer")
        else:
            print("No new logs in this interval.")
        time.sleep(30)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "/var/log/syslog"
    main(path)

