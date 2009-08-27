from django.db import models
from datetime import date, timedelta, time, datetime
from itertools import groupby
from collections import defaultdict
from hostel.managers import QuerySet, QSManager


class OccurrenceManager(QuerySet):

    def for_user(self, user):
        return self.filter(task__user=user)

    def month(self, month):
        return self.filter(start_time__month=month)

    def week_of(self, dt):
        try:
            dt = dt.date()
        except AttributeError:
            pass
        dt = dt + timedelta(days=-dt.weekday())
        td = dt + timedelta(days=6)
        dt = datetime.combine(dt, time(0))
        td = datetime.combine(td, time(0))
        return self.filter(end_time__gt=dt,
                           start_time__lt=td).distinct()

    def group_by_day(self):
        field = lambda x: x.start_time.day
        days = defaultdict(list)
        for day, occurrence in groupby(self, field):
            days[day] += list(occurrence)

        # return a standard dict purely because there are places where django
        # doesn't handle defaultdict well i.e. templates
        return dict(days)


class TaskQuerySet(QuerySet):

    def for_user(self, user):
        return self.filter(user=user)

    def before(self, dt):
        return self.filter(occurrence__start_time__lt=dt).distinct()

    def after(self, dt):
        return self.filter(occurrence__start_time__gt=dt).distinct()

    def week_of(self, monday):
        try:
            monday = monday.date()
        except AttributeError:
            pass
        monday = monday + timedelta(days=-monday.weekday())
        sunday = monday + timedelta(days=6)
        monday = datetime.combine(monday, time(0))
        sunday = datetime.combine(sunday, time(0))
        return self.filter(occurrence__end_time__gt=monday,
                           occurrence__start_time__lt=sunday).distinct()


class TaskRelatedManager(QSManager):

    def __init__(self, qs_class=TaskQuerySet):
        """Ensure that related managers use the correct class"""
        super(TaskRelatedManager, self).__init__(qs_class)

