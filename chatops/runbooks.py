import subprocess
from typing import Dict, Optional, List

RUNBOOKS: Dict[str, dict] = {
    "clear_tmp": {
        "description": "Delete files in /tmp older than 1 day",
        "command": ["find", "/tmp", "-maxdepth", "1", "-mtime", "+1", "-delete"],
        "preview": "find /tmp -maxdepth 1 -mtime +1 -delete",
    },
    "disk_breakdown": {
        "description": "Show disk usage of top-level directories",
        "command": ["du", "-sh", "--exclude=/proc", "--exclude=/sys", "--exclude=/dev", "/*"],
        "preview": "du -sh /* (excludes /proc /sys /dev)",
    },
    "large_logs": {
        "description": "List log files over 50MB in /var/log",
        "command": ["find", "/var/log", "-type", "f", "-size", "+50M", "-exec", "ls", "-lh", "{}", ";"],
        "preview": "find /var/log -type f -size +50M",
    },
    "listening_services": {
        "description": "List all listening services with PIDs",
        "command": ["ss", "-tlnp"],
        "preview": "ss -tlnp",
    },
}

_pending: Optional[str] = None


def list_runbooks() -> List[dict]:
    return [
        {"name": k, "description": v["description"], "preview": v["preview"]}
        for k, v in RUNBOOKS.items()
    ]


def request_runbook(name: str) -> dict:
    global _pending
    rb = RUNBOOKS.get(name)
    if not rb:
        available = ", ".join(RUNBOOKS.keys())
        return {
            "status": "error",
            "message": f"Unknown runbook '{name}'. Available: {available}",
        }
    _pending = name
    return {
        "status": "confirm",
        "message": (
            f"Runbook: {rb['description']}\n"
            f"Command: {rb['preview']}\n\n"
            f"Reply 'confirm {name}' to execute, or 'cancel' to abort."
        ),
    }


def confirm_runbook(name: str) -> dict:
    global _pending
    if _pending != name:
        return {
            "status": "error",
            "message": f"No pending confirmation for '{name}'. Use 'run {name}' first.",
        }
    rb = RUNBOOKS.get(name)
    if not rb:
        return {"status": "error", "message": f"Unknown runbook '{name}'."}
    _pending = None
    try:
        result = subprocess.run(
            rb["command"], capture_output=True, text=True, timeout=15
        )
        output = (result.stdout or result.stderr or "(no output)").strip()
        return {"status": "ok", "output": output[:1500]}
    except subprocess.TimeoutExpired:
        return {"status": "error", "message": "Runbook timed out after 15 seconds."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def cancel_runbook() -> dict:
    global _pending
    _pending = None
    return {"status": "ok", "message": "Cancelled."}
