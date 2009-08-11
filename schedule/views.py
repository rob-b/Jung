from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from hostel.decorators import rendered
from models import Event, EventType, Occurrence
from datetime import datetime
from calendar import Calendar

@rendered
def event_list(request, user_id, month=None, year=None):
    if month is None and year is None:
        now = datetime.now()
        month, year = now.month, now.year
    user = get_object_or_404(User, id=user_id)
    events = Occurrence.objects.for_user(user).group_by_day()
    calendar = Calendar()
    dates = [dt for dt in calendar.itermonthdates(year, month) if dt.month ==
             month]
    return 'base.html', {
        'dates': dates,
    }

