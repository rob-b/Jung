from django.test import TestCase
from django.contrib.auth.models import User
from models import Event, EventType, Occurrence
from datetime import datetime
import dateutil
from dateutil.relativedelta import relativedelta
from dateutil import rrule

class ScheduleTest(TestCase):

    def test_user_schedule(self):
        alice = User.objects.create_user('alice', 'alice@example.com', 'pass')
        bob = User.objects.create_user('bob', 'bob@example.com', 'pass')

        et = EventType.objects.create(title='some-project')
        event = Event.objects.create(
            title='Event #1',
            author=alice,
            user=bob,
            event_type=et,
        )
        start = datetime.now()
        end = start + relativedelta(days=+1)
        event.add_occurrences(start, end, count=3,)
        import ipdb; ipdb.set_trace();
        assert False
