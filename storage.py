import json
from pathlib import Path
from models import Student, Course, Event, Assignment

class DataStore:
    def __init__(self, filename): self.path = Path(filename)
    def exists(self): return self.path.exists()
    def save(self, student, courses, events, assignments):
        data = {
            'student': {'name': student.name},
            'courses': [c.__dict__ for c in courses],
            'events': [e.__dict__ for e in events],
            'assignments': [a.to_dict() for a in assignments]
        }
        self.path.write_text(json.dumps(data, indent=4), encoding='utf-8')
    def load(self):
        data = json.loads(self.path.read_text(encoding='utf-8'))
        return (Student(**data['student']),
                [Course(**x) for x in data['courses']],
                [Event(**x) for x in data['events']],
                [Assignment(**x) for x in data['assignments']])
