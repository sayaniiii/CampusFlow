class StudyPlanner:
    def __init__(self, events): self.events = events
    @staticmethod
    def to_minutes(t):
        h, m = map(int, t.split(':')); return h * 60 + m
    @staticmethod
    def to_time(minutes): return f'{minutes // 60:02d}:{minutes % 60:02d}'
    def free_slots(self, date, start_hour=8, end_hour=20):
        events = sorted([(self.to_minutes(e.start), self.to_minutes(e.end)) for e in self.events if e.date == date])
        start, end, cursor = start_hour * 60, end_hour * 60, start_hour * 60
        free = []
        for a, b in events:
            if b <= start or a >= end: continue
            a, b = max(a, start), min(b, end)
            if a > cursor: free.append((self.to_time(cursor), self.to_time(a), a - cursor))
            cursor = max(cursor, b)
        if cursor < end: free.append((self.to_time(cursor), self.to_time(end), end - cursor))
        return free
    @staticmethod
    def best_slot(slots, required_minutes):
        suitable = [s for s in slots if s[2] >= required_minutes]
        return min(suitable, key=lambda s: s[2]) if suitable else None
