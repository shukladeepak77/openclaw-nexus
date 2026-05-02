from monitor_logs import analyze_logs_chunk, parse_args, run_once
import os



def test_analyze_chunk_high(monkeypatch):
    class Resp:
        def __init__(self, json_data):
            self._json = json_data
        def json(self):
            return self._json
        def raise_for_status(self):
            pass

    def fake_post(url, json, timeout):
        return Resp({"severity": "HIGH", "root_cause": "DB", "impact": "Critical", "suggested_actions": ["Investigate"]})

    import monitor_logs
    monkeypatch.setattr(monitor_logs, 'requests', type('R', (), {'post': fake_post}))
    data = analyze_logs_chunk("ERROR: test failed\nDB error occurred")
    assert data["severity"] == "HIGH"


def test_analyze_chunk_low(monkeypatch):
    class Resp:
        def __init__(self, json_data):
            self._json = json_data
        def json(self):
            return self._json
        def raise_for_status(self):
            pass

    def fake_post(url, json, timeout):
        return Resp({"severity": "LOW", "root_cause": "None", "impact": "Low", "suggested_actions": []})

    import monitor_logs
    monkeypatch.setattr(monitor_logs, 'requests', type('R', (), {'post': fake_post}))
    data = analyze_logs_chunk("INFO: all good")
    assert data["severity"] == "LOW"


def test_parse_args_defaults():
    args = parse_args(["sample.log"])
    assert args.log_file == "sample.log"
    assert args.api_url == "http://localhost:8001/incident/analyze"
    assert args.interval == 30
    assert args.service == "log-monitor"
    assert args.environment == "prod"


def test_run_once_high(monkeypatch, tmp_path):
    # Create a small temp log file
    log_file = tmp_path / "sample.log"
    log_file.write_text("ERROR: failed\nDB issue detected")

    class Resp:
        def __init__(self, json_data):
            self._json = json_data
        def json(self):
            return self._json
        def raise_for_status(self):
            pass

    def fake_post(url, json, timeout):
        return Resp({"severity": "HIGH", "root_cause": "DB", "impact": "Critical", "suggested_actions": ["Investigate"]})

    import monitor_logs
    monkeypatch.setattr(monitor_logs, 'requests', type('R', (), {'post': fake_post}))

    data, new_pos = run_once(str(log_file), 0, "http://localhost:8001/incident/analyze", "log-monitor", "prod")
    assert isinstance(data, dict)
    assert data.get("severity") == "HIGH"
    assert new_pos > 0
