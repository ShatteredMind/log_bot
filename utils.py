from datetime import datetime


def line_contains_date(line):
    try:
        datetime.strptime(line.split()[0], '%Y-%m-%d')
        return True
    except ValueError:
        return False
