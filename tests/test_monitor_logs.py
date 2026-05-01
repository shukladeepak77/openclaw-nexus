from monitor_logs import analyze_logs_chunk


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

