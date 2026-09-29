from models import Assignment, Course, Event, Student
from storage import DataStore
from schedule_manager import ScheduleManager
from workload_analyzer import WorkloadAnalyzer
from planner import StudyPlanner
from simulator import WhatIfSimulator
from utils import choose, input_date, input_float, input_int, print_table

DATA_FILE = 'data.json'

def seed_data():
    student = Student('Student')
    courses = [Course('MAT1003','Engineering Mathematics'), Course('CSE1021','Problem Solving and Programming'), Course('ENG1004','Technical English')]
    events = [Event('MAT1003 Class','class','2026-10-05','09:00','10:00','MAT1003'), Event('CSE1021 Class','class','2026-10-05','10:00','11:00','CSE1021')]
    assignments = [Assignment('Math Assignment','MAT1003',4,3,'2026-10-07'), Assignment('Python Assignment','CSE1021',5,4,'2026-10-06')]
    return student, courses, events, assignments

def setup():
    store = DataStore(DATA_FILE)
    if not store.exists(): store.save(*seed_data())
    return store

def dashboard(store):
    student, courses, events, assignments = store.load(); a = WorkloadAnalyzer(assignments)
    print('\n=== CAMPUSFLOW DASHBOARD ===')
    print(f'Student: {student.name}\nCourses: {len(courses)} | Events: {len(events)} | Tasks: {len(assignments)}')
    for d, v in a.daily_scores().items(): print(f'{d}: score={v["score"]:.1f}, hours={v["hours"]:.1f}, level={v["level"]}')

def add_assignment(store):
    student,courses,events,assignments=store.load(); name=input('Assignment name: ').strip(); course=input('Course code: ').strip().upper(); difficulty=input_int('Difficulty (1-5): ',1,5); hours=input_float('Estimated hours: ',0.1); deadline=input_date('Deadline (YYYY-MM-DD): ')
    assignments.append(Assignment(name,course,difficulty,hours,deadline)); store.save(student,courses,events,assignments); print('Assignment added.')

def add_event(store):
    student,courses,events,assignments=store.load(); name=input('Event name: ').strip(); typ=input('Type (class/exam/other): ').strip().lower(); date=input_date('Date (YYYY-MM-DD): '); start=input('Start (HH:MM): '); end=input('End (HH:MM): '); course=input('Course code (optional): ').strip().upper() or None
    events.append(Event(name,typ,date,start,end,course)); store.save(student,courses,events,assignments); print('Event added.')

def conflicts(store):
    _,_,events,_=store.load(); found=ScheduleManager(events).find_conflicts()
    if not found: print('No schedule conflicts found.'); return
    print_table(['Date','Event A','Event B','Overlap'], [[c.date,c.event_a.name,c.event_b.name,c.overlap_minutes] for c in found])

def workload(store):
    _,_,_,assignments=store.load(); a=WorkloadAnalyzer(assignments); scores=a.daily_scores()
    if not scores: print('No assignments.'); return
    print_table(['Date','Score','Hours','Level'], [[d,f'{v["score"]:.1f}',f'{v["hours"]:.1f}',v['level']] for d,v in scores.items()]); print(f'Average: {a.weekly_average():.2f} | Peak day: {a.peak_day()}')

def planner(store):
    _,_,events,_=store.load(); p=StudyPlanner(events); date=input_date('Date (YYYY-MM-DD): '); slots=p.free_slots(date)
    print_table(['Start','End','Minutes'], slots) if slots else print('No free slots.')

def simulate(store):
    _,_,_,assignments=store.load(); s=WhatIfSimulator(assignments); name=input('New assignment: '); course=input('Course code: ').upper(); diff=input_int('Difficulty (1-5): ',1,5); hours=input_float('Hours: ',0.1); deadline=input_date('Deadline: '); new=Assignment(name,course,diff,hours,deadline); before=s.analyze(); after=s.analyze(assignments+[new]); print(f'Average: {before["average"]:.2f} -> {after["average"]:.2f}'); print(f'Peak: {before["peak"]:.2f} -> {after["peak"]:.2f}'); print('Saved data unchanged.')

def main():
    store=setup()
    while True:
        print('\n1 Dashboard\n2 Add assignment\n3 Add event\n4 Check conflicts\n5 Analyze workload\n6 Find study windows\n7 What-if simulation\n8 Exit')
        c=choose('Choose: ',range(1,9))
        if c==1: dashboard(store)
        elif c==2: add_assignment(store)
        elif c==3: add_event(store)
        elif c==4: conflicts(store)
        elif c==5: workload(store)
        elif c==6: planner(store)
        elif c==7: simulate(store)
        else: break

if __name__=='__main__': main()
