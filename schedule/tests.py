from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Task, TaskType, Occurrence
from datetime import datetime
import dateutil
from dateutil.relativedelta import relativedelta
from dateutil import rrule
from views import task_list

class ScheduleTest(TestCase):

    def test_user_schedule(self):
        alice = User.objects.create_user('alice', 'alice@example.com', 'pass')
        bob = User.objects.create_user('bob', 'bob@example.com', 'pass')

        et = TaskType.objects.create(title='some-project')
        task = Task.objects.create(
            title='Task #1',
            author=alice,
            user=bob,
            task_type=et,
        )
        start = datetime.now()
        end = start + relativedelta(days=+1)
        task.add_occurrences(start, end, count=3,)
        task2 = Task.objects.create(
            title='The second task',
            author=alice,
            user=bob,
            task_type=et,
        )
        dest = reverse('schedule_task_list')
        response = self.client.get(dest)
        import ipdb; ipdb.set_trace();
        assert False