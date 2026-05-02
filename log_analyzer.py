from collections import Counter


class LogAnalyzer:
    """A minimal log analyzer that counts occurrences of each log line and
    extracts the top messages by frequency.
    
    This is a lightweight implementation intended to be used as the existing
    LogAnalyzer in this project for the FastAPI service.
    """

    def analyze(self, lines):
        # Normalize lines to strings and count occurrences
        counts = {}
        for line in lines:
            counts[line] = counts.get(line, 0) + 1

        # Top messages by frequency (best-effort, up to 3 items)
        top_messages = [line for line, _ in Counter(lines).most_common(3)]

        return {
            "counts": counts,
            "top_messages": top_messages,
        }

