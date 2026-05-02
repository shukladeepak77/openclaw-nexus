#!/usr/bin/env python3
"""Log monitoring agent to triage incidents via the /incident/analyze API (Phase 1).

Reads a log file, polls every 30 seconds for new content, and sends the latest
logs to the Incident Analyzer API. Prints results when severity is HIGH.
"""

import time
import argparse
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


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Monitor logs and triage incidents via /incident/analyze")
    parser.add_argument("log_file", help="Path to the log file to monitor")
    parser.add_argument("--api-url", dest="api_url", default="http://localhost:8001/incident/analyze", help="API URL to send logs to")
    parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds")
    parser.add_argument("--service", default="log-monitor", help="Service name for incident context")
    parser.add_argument("--environment", default="prod", help="Environment name for incident context")
    return parser.parse_args(argv)


def run_once(log_path: str, last_pos: int, api_url: str, service: str, environment: str):
    logs, new_pos = read_new_logs(log_path, last_pos)
    if logs.strip():
        result = analyze_logs_chunk(logs, service=service, environment=environment, api_url=api_url)
        return result, new_pos
    return None, new_pos


if __name__ == "__main__":
    args = parse_args()
    log_path = args.log_file
    last_pos = 0
    while True:
        res, last_pos = run_once(log_path, last_pos, args.api_url, args.service, args.environment)
        if isinstance(res, dict):
            print("Incident analysis result:")
            print(json.dumps(res, indent=2))
            if res.get("severity") == "HIGH":
                print("ALERT: HIGH severity detected from incident analyzer")
        else:
            print("No new logs in this interval.")
        time.sleep(args.interval)
