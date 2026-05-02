from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from log_analyzer.analyzer import LogAnalyzer
from kundli.analyzer import KundliAnalyzer
from incident.analyzer import IncidentAnalyzer
from chatops.router import route_message
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
import pathlib

app = FastAPI()

@app.get("/chatops", response_class=HTMLResponse)
async def chatops_page():
    path = pathlib.Path("chatops/static/chatops.html")
    if path.exists():
        return HTMLResponse(path.read_text(encoding="utf-8"))
    return HTMLResponse("<html><body><h1>ChatOps</h1></body></html>")


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


@app.post("/analyze")
async def analyze_log(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    content = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".log") as tmp:
        tmp.write(content)
        temp_path = tmp.name
    try:
        analyzer = LogAnalyzer(temp_path)
        counts = analyzer.counts
        top_messages = analyzer.top_messages(3)

        # Extended health monitor metrics
        total_lines = sum(counts.values()) if isinstance(counts, dict) else 0
        error_count = 0
        warning_count = 0
        for line, c in counts.items():
            if isinstance(line, str):
                up = line.upper()
                if "ERROR" in up:
                    error_count += c
                if "WARNING" in up:
                    warning_count += c

        if error_count > 5:
            risk_level = "HIGH"
        elif warning_count > 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

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
    insights = analyzer.analyze()
    return insights


@app.post("/incident/analyze")
async def incident_analyze(req: IncidentRequest):
    analyzer = IncidentAnalyzer(req.service, req.environment, req.logs)
    result = analyzer.analyze()
    return result


@app.post("/chatops/message")
async def chatops_message(msg: ChatMessage):
    return route_message(msg.message)
