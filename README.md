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

Kundli Insight API (Phase 1 Prototype)
- Endpoint: POST /kundli/analyze
- Input: JSON body with dob, time, place, and optional gender
- Output: JSON with placeholder insights: personality, career, challenges, guidance
- Example:
  curl -X POST http://localhost:8000/kundli/analyze \
       -H 'Content-Type: application/json' \
       -d '{"dob":"1990-01-01","time":"12:00","place":"New York","gender":"Male"}'

Tests
- Pytest tests/test_api.py validate the API behavior.
