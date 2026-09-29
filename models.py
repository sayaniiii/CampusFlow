from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Student:
    name: str

@dataclass
class Course:
    code: str
    name: str

@dataclass
class Event:
    name: str
    event_type: str
    date: str
    start: str
    end: str
    course: Optional[str] = None

@dataclass
class Assignment:
    name: str
    course: str
    difficulty: int
    hours: float
    deadline: str

    def urgency(self, today=None):
        from datetime import date, datetime
        today = today or date.today()
        due = datetime.strptime(self.deadline, '%Y-%m-%d').date()
        days_left = (due - today).days
        if days_left <= 0: return 5
        if days_left <= 2: return 4
        if days_left <= 5: return 3
        if days_left <= 10: return 2
        return 1

    def workload_score(self, today=None):
        return self.difficulty * self.hours * self.urgency(today)

    def to_dict(self):
        return asdict(self)
