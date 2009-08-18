from datetime import datetime
from functools import wraps

def parse_args(f):
    @wraps(f)
    def wrapper(request, username, month=None, year=None):
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
        return f(request, username, month, year)
    return wrapper
