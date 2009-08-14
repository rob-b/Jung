from django import template
from django.utils.safestring import mark_safe
from datetime import date
from calendar import Calendar
from calendar import day_abbr
from schedule.utils import TaskCalendar
register = template.Library()


class Day(object):

    def __init__(self, day, weekday, month, year):
        self.day = day
        self.weekday = weekday
        self.month = month
        self.year = year
        self.tasks = []

        self._today = date.today()
        self._valid = bool(day)
        if day == 0:
            self._target = date.today()
            self.day_name = u''
        else:
            self._target = date(year, month, day)
            self.day_name = day_abbr[weekday]


    def __repr__(self):
        return u'<Day: %s>' % self._target.strftime('%d/%m/%Y')

    @property
    def today(self):
        return self._today == self._target

    @property
    def past(self):
        return self._today > self._target

    @property
    def future(self):
        return self._today < self._target

    @property
    def valid(self):
        return self._valid


def process_week(week, month, year):
    return [Day(*list(day) + [month, year]) for day in week]

def check_tasks(day_list, tasks):
    for day in day_list:
        if day.valid and day.day in tasks:
            day.tasks = tasks[day.day]
    return day_list


@register.inclusion_tag('schedule/task_calendar.html')
def calendar(tasks, date_obj=date.today()):
    month, year = date_obj.month, date_obj.year
    tasks = tasks

    dates = Calendar()
    weeks = [process_week(week, month, year) for week in
             dates.monthdays2calendar(year, month)]
    weeks = [check_tasks(week, tasks) for week in weeks]
    return {
        'weeks': weeks,
        'date_obj': date_obj,
    }
