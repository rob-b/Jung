from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from hostel.decorators import rendered
from schedule.models import Task, Occurrence
from schedule.forms import TaskForm
from schedule.utils import week_starting
from schedule.decorators import args_to_datetime
from datetime import datetime
from workers.models import Employee
from collections import defaultdict
from itertools import groupby


@rendered
@args_to_datetime
def user_schedule(request, username, dt):
    """All tasks scheduled for this month for a given employee"""
    user = get_object_or_404(User, username=username)
    tasks = Occurrence.objects.for_user(user).month(dt.month).group_by_day()
    return 'schedule/user_schedule.html', {
        'owner': user,
        'tasks': tasks,
        'date_obj': dt,
    }

@rendered
def schedule_list(request):
    """Overview of the number tasks each employee has"""
    object_list = Employee.objects.select_related().all()
    return 'schedule/schedule_list.html', {
        'object_list': object_list,
    }

@login_required
@rendered
def task_add(request):
    """Create a new task and assign it to an employee"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.user = form.cleaned_data.get('user', request.user)
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

@login_required
@rendered
def task_detail(request, project, slug):
    """details on a task"""
    task = get_object_or_404(Task, slug=slug, project__slug=project)
    return 'schedule/task_detail.html', {
        'task': task,
    }


@rendered
def user_task_list(request, username):
    """All pending tasks for a given employee"""
    user = get_object_or_404(Employee, user__username=username)
    dt = datetime.now()
    tasks = Task.objects.before(dt).for_user(user)
    return 'schedule/user_task_list.html', {
        'object_list': tasks,
        'profile': user,
    }

def sort_global_schedule(events):
    """build a dict of users as the key and a list of their tasks as the
    value"""
    field = lambda x: x.task.user
    schedule = defaultdict(list)
    for user, occurrence in groupby(events, field):
        schedule[user.get_profile()] += list(occurrence)
    return dict(schedule)

@rendered
@args_to_datetime
def weekly_schedule(request, username=None, dt=None):
    """All tasks scheduled for this week for a given employee"""
    dt = dt or datetime.now()
    week = week_starting(dt)
    if username is None:
        events = Occurrence.objects.week_of(dt)
        schedule = sort_global_schedule(events)
    else:
        user = get_object_or_404(Employee, user__username=username)
        events = Occurrence.objects.week_of(dt).for_user(user)
        schedule = {user: events}

    user_week = {}
    field = lambda x: x.start_time.day
    for user, occs in schedule.items():
        event_days = [(day, list(occs)) for day, occs in groupby(occs, field)]
        event_days = dict(event_days)

        w = []
        for day in week:
            w.append([day, event_days.get(day.day, [])])
        user_week[user] = w
    return 'schedule/schedule_weekly.html', {
        'object_list': user_week,
        'week': week,
        'dt': week[0],
    }
