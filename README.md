# CampusFlow

A Python command-line project for college schedule and workload analysis.

## Run
```bash
pip install -r requirements.txt
python main.py
```

## Test
```bash
python -m unittest discover -s tests
```

## Structure
- `main.py` — CLI
- `models.py` — OOP data models
- `storage.py` — JSON persistence
- `schedule_manager.py` — conflict detection
- `workload_analyzer.py` — NumPy workload analysis
- `planner.py` — free-time algorithm
- `simulator.py` — what-if analysis
- `utils.py` — input validation/output
- `tests/` — tests

## Workload Formula
`workload = difficulty × estimated_hours × urgency`

This is a project-defined heuristic, not a medical or psychological measurement.
