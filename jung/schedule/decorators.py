from datetime import datetime, time, date
from functools import wraps

def args_to_datetime(f):
    @wraps(f)
    def wrapper(request, username=None, day=None, month=None, year=None):
        day = int(day) if day is not None else datetime.now().day
        try:
            dt = datetime.strptime(month, '%b')
        except (ValueError, TypeError):
            month = datetime.now().month
        else:
            month = dt.month
        try:
            dt = datetime.strptime(year, '%Y')
        except (ValueError, TypeError):
            year = datetime.now().year
        else:
            year = dt.year
        dt = datetime.combine(date(year, month, day), time(0))
        return f(request, username, dt)
    return wrapper
