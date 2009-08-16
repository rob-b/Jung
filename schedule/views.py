from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from hostel.decorators import rendered
from models import Task, TaskType, Occurrence
from forms import TaskForm
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

@rendered
def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            task.user = request.user
            task.task_type = form.cleaned_data['task_type']
            task.save()
            task.add_occurrences(form.cleaned_data['start_time'],
                                 form.cleaned_data['end_time'],
                                 byweekday=range(5),
                                 count=form.cleaned_data['count'])
            dest = reverse('schedule_user_task_list',
                           args=[request.user.username])
            return HttpResponseRedirect(dest)
    else:
        form = TaskForm()
    return 'schedule/task_add.html', {
        'form': form,
    }
