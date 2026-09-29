from dataclasses import dataclass

@dataclass
class Conflict:
    date: str
    event_a: object
    event_b: object
    overlap_minutes: int

class ScheduleManager:
    def __init__(self, events): self.events = events
    @staticmethod
    def _minutes(t):
        h, m = map(int, t.split(':')); return h * 60 + m
    def find_conflicts(self):
        grouped = {}
        for e in self.events: grouped.setdefault(e.date, []).append(e)
        conflicts = []
        for date, events in grouped.items():
            events = sorted(events, key=lambda e: self._minutes(e.start))
            for i in range(len(events)):
                for j in range(i + 1, len(events)):
                    a, b = events[i], events[j]
                    overlap = min(self._minutes(a.end), self._minutes(b.end)) - max(self._minutes(a.start), self._minutes(b.start))
                    if overlap > 0: conflicts.append(Conflict(date, a, b, overlap))
        return conflicts
