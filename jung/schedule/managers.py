from django.db import models
from django.db import connection
from datetime import date, timedelta, time, datetime
from itertools import groupby, chain
from collections import defaultdict
from hostel.managers import QuerySet


class OccurrenceManager(QuerySet):

    def for_user(self, user):
        """Return all occurrences for `user`"""
        return self.filter(task__user=user)

    def month(self, month):
        return self.filter(start_time__month=month)

    def week_of(self, dt):
        """All occurences that occur during the week that features `dt`"""
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

    def conflicted(self):
        """Return all occurrences that overlap with another occurrence.

        bear in mind that most occurence will overlap and so this is only useful
        when filtered with something else"""

        sql = """SELECT DISTINCT  o1.id
        FROM schedule_occurrence o1, schedule_occurrence o2
        WHERE (o2.start_time BETWEEN o1.start_time AND o1.end_time
        OR o2.end_time BETWEEN o1.start_time AND o1.end_time)
        AND o1.id <> o2.id"""
        cursor = connection.cursor()
        cursor.execute(sql)
        ids = chain(*cursor.fetchall())
        return self.filter(id__in=ids).extra(select={'conflict': 1})

    def pristine(self):
        """Return all occurrences that do not overlap with any other"""
        return self.exclude(
            id__in=self.conflicted().values_list('id', flat=True)
        ).extra(select={'conflict': 0})

    def get_query_set(self):
        qs = self.pristine() | self.conflicted()
        return qs.order_by(self.model._meta.ordering)


class TaskManager(QuerySet):

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
