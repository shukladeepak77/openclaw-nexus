import asyncio
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import tempfile
import os
import pathlib

from log_analyzer.analyzer import LogAnalyzer
from kundli.analyzer import KundliAnalyzer
from incident.analyzer import IncidentAnalyzer
from chatops.router import route_message
from chatops.db import (
    init_db, save_message, get_history, clear_history,
    get_alerts, ack_alert, unacked_count, get_metric_history, add_alert,
)
from chatops.config import load_config, save_config
from chatops.runbooks import list_runbooks


# ── Background health check ───────────────────────────────────────────────────

def _health_check_sync():
    from chatops.actions import check_disk, check_memory, check_cpu
    from chatops.config import alert_status_from_config
    from chatops.db import add_metric

    for fn, metric in [(check_disk, "disk"), (check_memory, "memory"), (check_cpu, "cpu")]:
        try:
            data = fn()
            pct = data["percent_used"]
            add_metric(metric, pct)
            status = alert_status_from_config(pct, metric)
            if status != "OK":
                add_alert(f"{metric.capitalize()} {status}: {pct:.1f}% used", status)
        except Exception:
            pass


async def _health_check_loop():
    loop = asyncio.get_event_loop()
    while True:
        try:
            cfg = load_config()
            interval = int(cfg.get("health_check_interval", 60))
        except Exception:
            interval = 60
        try:
            await loop.run_in_executor(None, _health_check_sync)
        except Exception:
            pass
        await asyncio.sleep(interval)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(_health_check_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)


# ── Request models ─────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    message: str


class KundliRequest(BaseModel):
    dob: str
    time: str
    place: str
    gender: Optional[str] = None


class IncidentRequest(BaseModel):
    service: str
    environment: str
    logs: str


class ConfigUpdate(BaseModel):
    disk_warning: Optional[float] = None
    disk_critical: Optional[float] = None
    memory_warning: Optional[float] = None
    memory_critical: Optional[float] = None
    cpu_warning: Optional[float] = None
    cpu_critical: Optional[float] = None
    health_check_interval: Optional[int] = None


# ── ChatOps routes ─────────────────────────────────────────────────────────────

@app.get("/chatops", response_class=HTMLResponse)
async def chatops_page():
    path = pathlib.Path("chatops/static/chatops.html")
    if path.exists():
        return HTMLResponse(path.read_text(encoding="utf-8"))
    return HTMLResponse("<html><body><h1>ChatOps</h1></body></html>")


@app.post("/chatops/message")
def chatops_message(msg: ChatMessage):
    save_message("user", msg.message)
    result = route_message(msg.message)
    save_message("bot", result.get("response", ""))
    return result


@app.get("/chatops/history")
def get_chat_history(limit: int = 50):
    return {"history": get_history(limit)}


@app.delete("/chatops/history")
def clear_chat_history():
    clear_history()
    return {"status": "ok"}


@app.get("/chatops/alerts")
def get_alerts_endpoint(limit: int = 50, unacked_only: bool = False):
    alerts = get_alerts(limit=limit, unacked_only=unacked_only)
    count = unacked_count()
    return {"alerts": alerts, "unacked_count": count}


@app.post("/chatops/alerts/{alert_id}/ack")
def ack_alert_endpoint(alert_id: int):
    ack_alert(alert_id)
    return {"status": "ok", "unacked_count": unacked_count()}


@app.get("/chatops/metrics/history")
def metrics_history_endpoint(metric: str = "disk", limit: int = 60):
    return {"metric": metric, "data": get_metric_history(metric, limit)}


@app.get("/chatops/config")
def get_config_endpoint():
    return load_config()


@app.put("/chatops/config")
def update_config_endpoint(updates: ConfigUpdate):
    data = {k: v for k, v in updates.model_dump().items() if v is not None}
    return save_config(data)


@app.get("/chatops/runbooks")
def get_runbooks_endpoint():
    return {"runbooks": list_runbooks()}


# ── Existing analyzer routes ───────────────────────────────────────────────────

@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)):
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
        tmp.write(content)
        temp_path = tmp.name
    try:
        analyzer = LogAnalyzer(temp_path)
        counts = analyzer.counts
        top_messages = analyzer.top_messages(3)
        total_lines = sum(counts.values()) if isinstance(counts, dict) else 0
        error_count = sum(c for line, c in counts.items() if "ERROR" in str(line).upper())
        warning_count = sum(c for line, c in counts.items() if "WARNING" in str(line).upper())
        risk_level = "HIGH" if error_count > 5 else ("MEDIUM" if warning_count > 3 else "LOW")
        suggestions = []
        if error_count > 5:
            suggestions.append("Investigate failures")
        if warning_count > 3:
            suggestions.append("Check system health")
        return {
            "counts": counts,
            "top_messages": top_messages,
            "total_lines": total_lines,
            "error_count": error_count,
            "warning_count": warning_count,
            "risk_level": risk_level,
            "suggestions": suggestions,
        }
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass


@app.post("/kundli/analyze")
async def kundli_analyze(req: KundliRequest):
    analyzer = KundliAnalyzer(req.dob, req.time, req.place, req.gender)
    return analyzer.analyze()


@app.post("/incident/analyze")
async def incident_analyze(req: IncidentRequest):
    analyzer = IncidentAnalyzer(req.service, req.environment, req.logs)
    return analyzer.analyze()
