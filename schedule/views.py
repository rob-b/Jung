from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from hostel.decorators import rendered
from models import Task, TaskType, Occurrence
from utils import TaskCalendar
from datetime import date
from calendar import Calendar
from workers.models import Employee

@rendered
def user_task_list(request, username, month=None, year=None):
    if month is None and year is None:
        now = date.today()
        month, year = now.month, now.year
    user = get_object_or_404(User, username=username)
    tasks = Occurrence.objects.for_user(user).group_by_day()
    return 'schedule/user_task_list.html', {
        'tasks': tasks,
        'date_obj': date(year, month, 1)
    }

@rendered
def task_list(request):
    object_list = Employee.objects.select_related().all()
    return 'schedule/task_list.html', {
        'object_list': object_list,
    }
