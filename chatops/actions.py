def help_text() -> str:
    return (
        "Available commands: check disk, check memory, check uptime, check ports, analyze logs, help"
    )


def check_disk():
    # Simple placeholder values
    return {"total_gb": 500, "used_gb": 230, "percent_used": 46}


def check_memory():
    return {"total_mb": 32768, "used_mb": 10240, "percent_used": 31}


def check_uptime():
    return {"uptime": "3 days, 4 hours"}


def check_ports():
    return [
        {"port": 22, "service": "ssh", "open": True},
        {"port": 80, "service": "http", "open": True},
        {"port": 443, "service": "https", "open": True},
    ]


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

