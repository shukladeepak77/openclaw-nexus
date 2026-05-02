class IncidentAnalyzer:
    """Phase 1 AI Incident Triage - rule-based placeholder.

    Inputs:
      - service: service name
      - environment: environment (prod, staging, etc.)
      - logs: string containing log content

    Output (via analyze):
      - severity: LOW | MEDIUM | HIGH
      - root_cause: string
      - impact: string
      - suggested_actions: list[str]
    """

    def __init__(self, service: str, environment: str, logs: str):
        self.service = service
        self.environment = environment
        self.logs = logs or ""

    def _count(self, keyword: str) -> int:
        return self.logs.upper().count(keyword.upper())

    def analyze(self) -> dict:
        log = self.logs or ""
        logu = log.upper()

        error_count = self._count("ERROR")
        warning_count = self._count("WARNING")

        # Severity logic
        if error_count > 5:
            severity = "HIGH"
        elif warning_count > 0 or "TIMEOUT" in logu:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # Root cause & patterns
        if "DB" in logu:
            root_cause = "Database connection/query issue detected (DB pattern)"
        elif "TIMEOUT" in logu:
            root_cause = "Network timeout detected"
        elif "AUTH" in logu:
            root_cause = "Authentication failure detected"
        else:
            root_cause = "Unclear root cause; requires deeper log analysis"

        # Impact
        if severity == "HIGH":
            impact = "Critical impact on service availability"
        elif severity == "MEDIUM":
            impact = "Degraded service; user impact possible"
        else:
            impact = "Low impact; monitoring advised"

        # Suggested actions
        suggested_actions = []
        if error_count > 5:
            suggested_actions.append("Investigate failures")
        if warning_count > 0:
            suggested_actions.append("Check system health")
        if "DB" in logu:
            suggested_actions.append("Inspect database connectivity/queries")
        if "TIMEOUT" in logu:
            suggested_actions.append("Review network latency and timeouts")
        if "AUTH" in logu:
            suggested_actions.append("Audit authentication flow and credentials")
        if not suggested_actions:
            suggested_actions.append("Gather more logs for triage")

        return {
            "severity": severity,
            "root_cause": root_cause,
            "impact": impact,
            "suggested_actions": suggested_actions,
        }

