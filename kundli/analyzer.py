import hashlib


import hashlib


class KundliAnalyzer:
    """Phase 1 placeholder Kundli Insight engine (deterministic by time).

    Accepts dob, time, place, and optional gender. Produces deterministic,
    rule-based placeholder insights without real planetary positions.
    """

    def __init__(self, dob: str, time: str, place: str, gender: str | None = None):
        self.dob = dob
        self.time = time
        self.place = place
        self.gender = gender

    def _hour(self) -> int:
        try:
            hour = int(str(self.time).split(":")[0])
        except Exception:
            hour = 0
        return hour

    def analyze(self) -> dict:
        hour = self._hour()
        # Phase 1: determine profile by birth time window
        if 4 <= hour < 10:
            idx = 0  # morning
        elif 10 <= hour < 16:
            idx = 1  # afternoon
        elif 16 <= hour < 20:
            idx = 2  # evening
        else:
            idx = 3  # night

        profiles = [
            {
                "personality": "Morning profile: active and leadership-oriented.",
                "career": "Morning career path: roles that require initiative and direction.",
                "challenges": "Morning challenges: staying concise and focused.",
                "guidance": "Morning guidance: set priorities for the day.",
            },
            {
                "personality": "Afternoon profile: practical, grounded, work-focused.",
                "career": "Afternoon career path: practical tasks and steady execution.",
                "challenges": "Afternoon challenges: avoid creative block and fatigue.",
                "guidance": "Afternoon guidance: chunk work into clear milestones.",
            },
            {
                "personality": "Evening profile: relational, balanced, socially aware.",
                "career": "Evening career path: teamwork, collaboration, leadership.",
                "challenges": "Evening challenges: balance social with focus.",
                "guidance": "Evening guidance: nurture relationships and priorities.",
            },
            {
                "personality": "Night profile: introspective, spiritual, reflective.",
                "career": "Night career path: research, analysis, or solitary work.",
                "challenges": "Night challenges: avoid overthinking.",
                "guidance": "Night guidance: quiet reflection to plan tomorrow.",
            },
        ]

        return profiles[idx]
