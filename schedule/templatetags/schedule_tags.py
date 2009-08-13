from django import template
from django.utils.safestring import mark_safe
from schedule.utils import TaskCalendar
register = template.Library()

@register.inclusion_tag('schedule/task_calendar.html', takes_context=True)
def calendar(context):
    month, year = context['month'], context['year']
    tasks = context['object_list']
    calendar = mark_safe(TaskCalendar(tasks).formatmonth(year, month))
    return {
        'calendar': calendar,
    }
