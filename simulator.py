import numpy as np
from workload_analyzer import WorkloadAnalyzer

class WhatIfSimulator:
    def __init__(self, assignments): self.assignments = assignments
    def analyze(self, assignments=None):
        daily = WorkloadAnalyzer(assignments if assignments is not None else self.assignments).daily_scores()
        values = np.array([v['score'] for v in daily.values()], dtype=float)
        if not values.size: return {'average': 0.0, 'peak': 0.0, 'peak_day': 'N/A'}
        return {'average': float(np.mean(values)), 'peak': float(np.max(values)), 'peak_day': max(daily, key=lambda d: daily[d]['score'])}
