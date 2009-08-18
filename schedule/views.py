from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from hostel.decorators import rendered
from models import Task, TaskType, Occurrence
from forms import TaskForm
from utils import TaskCalendar
from datetime import date, datetime
from calendar import Calendar
from workers.models import Employee
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


@rendered
@parse_args
def user_schedule(request, username, month=None, year=None):
    # if month is None or year is None:
    #     now = date.today()
    # month = now.month if month is None else int(month)
    # year = now.year if year is None else int(year)

    user = get_object_or_404(User, username=username)
    tasks = Occurrence.objects.for_user(user).month(month).group_by_day()
    return 'schedule/user_schedule.html', {
        'owner': user,
        'tasks': tasks,
        'date_obj': date(year, month, 1)
    }

@rendered
def schedule_list(request):
    object_list = Employee.objects.select_related().all()
    return 'schedule/schedule_list.html', {
        'object_list': object_list,
    }

@login_required
@rendered
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            user = form.cleaned_data.get('user', request.user)
            task.user = user
            task.task_type = form.cleaned_data['task_type']
            task.save()
            task.add_occurrences(form.cleaned_data['start_time'],
                                 form.cleaned_data['end_time'],
                                 byweekday=range(5),
                                 count=form.cleaned_data['count'])
            dest = reverse('schedule_user_schedule',
                           args=[request.user.username])
            return HttpResponseRedirect(dest)
    else:
        form = TaskForm()
    return 'schedule/task_add.html', {
        'form': form,
    }

@rendered
def user_task_list(request, username):
    user = get_object_or_404(Employee, user__username=username)
    dt = datetime.now()
    tasks = Task.objects.before(dt).for_user(user)
    return 'schedule/user_task_list.html', {
        'object_list': tasks,
        'profile': user,
    }
