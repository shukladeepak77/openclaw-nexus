from fastapi import FastAPI, UploadFile, File
import tempfile
import os
from log_analyzer.analyzer import LogAnalyzer

app = FastAPI()


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
        return {"counts": counts, "top_messages": top_messages}
    finally:
        try:
            os.remove(temp_path)
        except Exception:
            pass
