import re
from typing import Dict

from .actions import (
    check_disk,
    check_memory,
    check_uptime,
    check_ports,
    analyze_logs as analyze_logs_action,
    help_text as help_text_action,
)


def route_message(message: str) -> Dict[str, str]:
    # Normalize input to a safe, lowercase string and strip punctuation
    s = (message or "").lower().strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    print("DEBUG NL:", s)

    # Help
    if not s or "help" in s:
        return {"response": help_text_action()}

    # Disk keywords
    if any(kw in s for kw in ["disk", "storage", "space"]):
        data = check_disk()
        return {
            "response": f"Disk usage: {data['used_gb']} GB used of {data['total_gb']} GB ({data['percent_used']}% used).",
        }
    # Memory keywords
    if any(kw in s for kw in ["memory", "ram"]):
        data = check_memory()
        return {
            "response": f"Memory usage: {data['used_mb']} MB / {data['total_mb']} MB ({data['percent_used']}% used).",
        }
    # Uptime keywords
    if any(kw in s for kw in ["uptime", "running", "server running"]):
        data = check_uptime()
        return {"response": f"Uptime: {data['uptime']}"}
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
    if any(kw in s for kw in ["system health", "health", "status"]):
        d = check_disk()
        m = check_memory()
        u = check_uptime()
        resp = f"System Health: Disk {d['percent_used']}% used, Memory {m['percent_used']}% used, Uptime {u['uptime']}."
        return {"response": resp}
    # Fallback message
    return {"response": "I didn’t understand. Try: check disk, check memory, system health, analyze logs"}
