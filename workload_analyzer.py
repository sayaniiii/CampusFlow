import numpy as np
from collections import defaultdict

class WorkloadAnalyzer:
    def __init__(self, assignments): self.assignments = assignments
    @staticmethod
    def _level(score):
        if score >= 50: return 'HIGH'
        if score >= 25: return 'MEDIUM'
        return 'LOW'
    def daily_scores(self):
        grouped = defaultdict(list)
        for a in self.assignments: grouped[a.deadline].append(a)
        result = {}
        for day, tasks in sorted(grouped.items()):
            scores = np.array([t.workload_score() for t in tasks], dtype=float)
            hours = np.array([t.hours for t in tasks], dtype=float)
            total = float(np.sum(scores))
            result[day] = {'score': total, 'hours': float(np.sum(hours)), 'level': self._level(total)}
        return result
    def weekly_average(self):
        values = np.array([v['score'] for v in self.daily_scores().values()], dtype=float)
        return float(np.mean(values)) if values.size else 0.0
    def peak_day(self):
        scores = self.daily_scores()
        return max(scores, key=lambda d: scores[d]['score']) if scores else 'N/A'
