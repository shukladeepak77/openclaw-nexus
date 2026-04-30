import re
from collections import Counter

class LogAnalyzer:
    LEVELS = ("ERROR", "WARNING", "INFO")

    def __init__(self, path: str = None, text: str = None):
        self.path = path
        self.text = text
        self._entries = []  # list of (level, message)

    def _parse_line(self, line: str):
        for level in self.LEVELS:
            if level in line:
                idx = line.index(level)
                after = line[idx + len(level):].strip()
                if after.startswith("-"):
                    after = after[1:].lstrip()
                if after.startswith(":"):
                    after = after[1:].lstrip()
                return level, after
        return None

    def _load_entries(self):
        if self._entries:
            return
        if self.path:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = self._parse_line(line.strip())
                    if parsed:
                        self._entries.append(parsed)
        elif self.text:
            for line in self.text.splitlines():
                parsed = self._parse_line(line.strip())
                if parsed:
                    self._entries.append(parsed)

    @property
    def counts(self) -> dict:
        self._load_entries()
        c = Counter([lvl for lvl, _ in self._entries])
        return {lvl: c.get(lvl, 0) for lvl in self.LEVELS}

    def top_messages(self, limit: int = 5):
        self._load_entries()
        msgs = Counter([msg for _lvl, msg in self._entries])
        return msgs.most_common(limit)

    def generate_report(self, report_path: str = "log_report.txt", top_limit: int = 5) -> str:
        counts = self.counts
        top = self.top_messages(top_limit)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("Log Analysis Report\n")
            f.write("==================\n\n")
            f.write("Counts by level:\n")
            for lvl in self.LEVELS:
                f.write(f"{lvl}: {counts[lvl]}\n")
            f.write("\nTop messages:\n")
            for msg, cnt in top:
                f.write(f"{cnt}x - {msg}\n")
        return report_path
