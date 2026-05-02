import shutil
import os
import re
import subprocess


def help_text() -> str:
    return (
        "Available commands: check disk, check memory, check uptime, check ports, analyze logs, help"
    )


def check_disk():
    # Real disk usage using shutil
    usage = shutil.disk_usage("/")
    total_gb = usage.total / (1024**3)
    used_gb = usage.used / (1024**3)
    free_gb = usage.free / (1024**3)
    percent_used = (usage.used / usage.total) * 100 if usage.total else 0
    return {
        "total_gb": round(total_gb, 2),
        "used_gb": round(used_gb, 2),
        "free_gb": round(free_gb, 2),
        "percent_used": round(percent_used, 2),
    }


def _read_meminfo():
    mem = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem["MemTotal_kB"] = int(line.split()[1])
                elif line.startswith("MemAvailable:"):
                    mem["MemAvailable_kB"] = int(line.split()[1])
                elif line.startswith("MemFree:"):
                    mem["MemFree_kB"] = int(line.split()[1])
    except Exception:
        pass
    return mem


def check_memory():
    mem = _read_meminfo()
    total_kb = mem.get("MemTotal_kB", 0)
    avail_kb = mem.get("MemAvailable_kB")
    if avail_kb is None:
        avail_kb = mem.get("MemFree_kB", 0)
    used_kb = max(total_kb - avail_kb, 0)
    total_mb = int(total_kb / 1024)
    used_mb = int(used_kb / 1024)
    available_mb = int(avail_kb / 1024) if avail_kb else 0
    percent_used = (used_kb / total_kb) * 100 if total_kb else 0
    return {
        "total_mb": total_mb,
        "used_mb": used_mb,
        "available_mb": available_mb,
        "percent_used": round(percent_used, 2),
    }


def check_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            seconds_str = f.readline().split()[0]
            seconds = float(seconds_str)
    except Exception:
        seconds = 0.0
    days = int(seconds // 86400)
    seconds -= days * 86400
    hours = int(seconds // 3600)
    seconds -= hours * 3600
    minutes = int(seconds // 60)
    seconds = int(seconds - minutes * 60)
    return {
        "uptime_days": days,
        "uptime_hours": hours,
        "uptime_minutes": minutes,
        "uptime_seconds": seconds,
    }


def check_ports():
    try:
        res = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, timeout=3)
        if res.returncode != 0:
            return []
        ports = []
        for line in res.stdout.splitlines():
            for token in line.split():
                if ":" in token:
                    port_s = token.rsplit(":", 1)[-1]
                    if port_s.isdigit():
                        ports.append({"port": int(port_s), "service": "unknown"})
        # unique ports
        seen = set()
        uniq = []
        for p in ports:
            if p["port"] not in seen:
                seen.add(p["port"])
                uniq.append(p)
        return uniq
    except Exception:
        return []


def analyze_logs(logs: str):
    up = (logs or "").upper()
    errors = up.count("ERROR")
    warnings = up.count("WARNING")
    severity = "HIGH" if errors > 3 else ("MEDIUM" if warnings > 0 else "LOW")
    root_cause = "Unclear root cause; requires deeper log analysis"
    if "DB" in up:
        root_cause = "Database connectivity issue"
    elif "TIMEOUT" in up:
        root_cause = "Network timeout detected"
    elif "AUTH" in up:
        root_cause = "Authentication failure detected"
    impact = "Critical" if severity == "HIGH" else ("Degraded" if severity == "MEDIUM" else "Low")
    suggested_actions = []
    if errors > 0:
        suggested_actions.append("Review error logs")
    if warnings > 0:
        suggested_actions.append("Check system health")
    if "DB" in up:
        suggested_actions.append("Inspect database connectivity/queries")
    if "TIMEOUT" in up:
        suggested_actions.append("Review network latency and timeouts")
    if "AUTH" in up:
        suggested_actions.append("Audit authentication flow and credentials")
    if not suggested_actions:
        suggested_actions.append("Monitor and collect more logs")
    return {
        "severity": severity,
        "root_cause": root_cause,
        "impact": impact,
        "suggested_actions": suggested_actions,
    }

def alert_status(percent: float) -> str:
    if percent >= 90:
        return "CRITICAL"
    if percent >= 80:
        return "WARNING"
    return "OK"
