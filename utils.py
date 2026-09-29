from datetime import datetime

def choose(prompt, valid):
    valid = set(valid)
    while True:
        try:
            x = int(input(prompt))
            if x in valid: return x
        except ValueError: pass
        print('Enter a valid option.')

def input_int(prompt, low=None, high=None):
    while True:
        try:
            x = int(input(prompt))
            if (low is None or x >= low) and (high is None or x <= high): return x
        except ValueError: pass
        print('Enter a valid integer.')

def input_float(prompt, low=None):
    while True:
        try:
            x = float(input(prompt))
            if low is None or x >= low: return x
        except ValueError: pass
        print('Enter a valid number.')

def input_date(prompt):
    while True:
        x = input(prompt).strip()
        try: datetime.strptime(x, '%Y-%m-%d'); return x
        except ValueError: print('Use YYYY-MM-DD.')

def print_table(headers, rows):
    widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row): widths[i] = max(widths[i], len(str(cell)))
    print(' | '.join(str(h).ljust(widths[i]) for i, h in enumerate(headers)))
    print('-+-'.join('-' * w for w in widths))
    for row in rows: print(' | '.join(str(c).ljust(widths[i]) for i, c in enumerate(row)))
