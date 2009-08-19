from calendar import HTMLCalendar, month_name
from datetime import date

class TaskCalendar(HTMLCalendar):
    """
    This calendar returns complete HTML pages.
    """

    def __init__(self, tasks, firstweekday=0):
        super(TaskCalendar, self).__init__(firstweekday)
        self.tasks = tasks

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(TaskCalendar, self).formatmonth(year, month)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            today = date.today()
            target = date(self.year, self.month, day)
            if today == target:
                cssclass += " today"
            elif today > target:
                cssclass += " history"
            if day in self.tasks:
                content = ', '.join([task.task.title for task in self.tasks[day]])
            else:
                content = ''
            return '<td class="%s"><h4>%d</h4> %s</td>' % (cssclass, day, content)
        return '<td class="noday">&nbsp;</td>'


