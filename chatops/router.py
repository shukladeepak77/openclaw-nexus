import re
from typing import Dict

from .actions import (
    check_disk,
    check_memory,
    check_uptime,
    check_ports,
    analyze_logs as analyze_logs_action,
    help_text as help_text_action,
    alert_status,
)


def route_message(message: str) -> Dict[str, str]:
    # Normalize input to a safe, lowercase string and strip punctuation
    s = (message or "").lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)

    # Help
    if not s or "help" in s:
        return {"response": help_text_action()}

    # Disk keywords
    if any(kw in s for kw in ["disk", "storage", "space"]):
        data = check_disk()
        return {
            "response": f"Disk usage: {data['percent_used']:.2f}% used. Status: {alert_status(data['percent_used'])}",
        }
    # Memory keywords
    if any(kw in s for kw in ["memory", "ram"]):
        data = check_memory()
        return {
            "response": f"Memory usage: {data['percent_used']:.2f}% used. Status: {alert_status(data['percent_used'])}",
        }
    # Uptime keywords
    if any(kw in s for kw in ["uptime", "running", "server running"]):
        data = check_uptime()
        uptime_str = f"{data.get('uptime_days', 0)}d {data.get('uptime_hours', 0)}h {data.get('uptime_minutes', 0)}m"
        return {"response": f"Uptime: {uptime_str}"}
    # Ports keywords
    if any(kw in s for kw in ["port", "ports", "open ports"]):
        data = check_ports()
        ports = ", ".join([f"{p['port']}/{p['service']}" for p in data])
        return {"response": f"Open ports: {ports}"}
    # Analyze logs
    if "analyze logs" in s:
        logs = s.split("analyze logs", 1)[1].strip()
        if logs.startswith(":"):
            logs = logs[1:].strip()
        data = analyze_logs_action(logs)
        return {
            "response": f"Logs → Severity: {data.get('severity')}, Root: {data.get('root_cause')}, Guidance: {data.get('suggested_actions')}"
        }
    # System health (quick summary)
    if any(kw in s for kw in ["system health", "system usage", "health", "status"]):
        d = check_disk()
        m = check_memory()
        u = check_uptime()
        uptime_str = f"{u.get('uptime_days',0)}d {u.get('uptime_hours',0)}h {u.get('uptime_minutes',0)}m"
        disk_status = alert_status(d["percent_used"])
        memory_status = alert_status(m["percent_used"])
        if "CRITICAL" in (disk_status, memory_status):
            overall_status = "CRITICAL"
        elif "WARNING" in (disk_status, memory_status):
            overall_status = "WARNING"
        else:
            overall_status = "OK"
        resp = (
            f"System Health: overall_status: {overall_status}; "
            f"disk_status: {disk_status} ({d['percent_used']:.2f}% used); "
            f"memory_status: {memory_status} ({m['percent_used']:.2f}% used); "
            f"uptime: {uptime_str}"
        )
        return {
            "response": resp,
            "overall_status": overall_status,
            "disk_status": disk_status,
            "memory_status": memory_status,
            "uptime": uptime_str,
        }
    # Fallback message
    return {"response": "I didn’t understand. Try: check disk, check memory, system health, analyze logs"}
