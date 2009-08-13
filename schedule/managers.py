from django.db import models
from itertools import groupby
from collections import defaultdict
from hostel.managers import QuerySet


class OccurrenceManager(QuerySet):

    def for_user(self, user):
        return self.filter(task__user=user)

    def group_by_day(self):
        field = lambda x: x.start_time.day
        days = defaultdict(list)
        for day, occurrence in groupby(self, field):
            days[day] += list(occurrence)

        # return a standard dict purely because there are places where django
        # doesn't handle defaultdict well i.e. templates
        return dict(days)
