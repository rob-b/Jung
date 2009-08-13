from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from hostel.decorators import rendered
from models import Task, TaskType, Occurrence
from utils import TaskCalendar
from datetime import datetime
from calendar import Calendar

@rendered
def task_list(request, user_id, month=None, year=None):
    if month is None and year is None:
        now = datetime.now()
        month, year = now.month, now.year
    user = get_object_or_404(User, id=user_id)
    tasks = Occurrence.objects.for_user(user).group_by_day()
    calendar = Calendar()
    # dates = [dt for dt in calendar.itermonthdates(year, month) if dt.month ==
             # month]
    dates = list(calendar.itermonthdates(year, month))
    matches = []
    for date in dates:
        if date.day in tasks:
            str = '**%s**' % date.day
        else:
            str = '%d' % date.day
        matches.append(str)
    calendar = TaskCalendar(tasks).formatmonth(year, month)
    return 'schedule/task_list.html', {
        'dates': dates,
        'object_list': tasks,
        'matches': matches,
        'calendar': calendar,
        'month': month,
        'year': year,
    }
