# OpenClaw Nexus - Log Analyzer API

This project exposes a FastAPI service to analyze logs using the existing LogAnalyzer.

API
- POST /analyze: Upload a log file (multipart/form-data, field name: file). Returns JSON with:
  - counts: map from log line to frequency
  - top_messages: list of up to 3 most frequent lines

Run locally
- Install: pip install -r requirements.txt
- Run: uvicorn app:app --reload --port 8000
- Test quickly:
  - Use curl or a HTTP client to post a log file to http://localhost:8000/analyze

Tests
- Pytest tests/test_api.py validate the API behavior.
