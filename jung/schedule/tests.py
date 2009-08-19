from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Task, TaskType, Occurrence
from datetime import datetime
import dateutil
from dateutil.relativedelta import relativedelta
from dateutil import rrule
from forms import OccurrenceForm, TaskForm

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

    def test_occurrence_form(self):
        """Times outside of work hours should produce errors in the form"""
        now = datetime.now()
        data = {
            'start_time': now.replace(hour=7)
        }
        form = OccurrenceForm(data)
        self.assertFalse(form.is_valid(), '7am starts are not allowed')
        self.assert_('start_time' in form.errors)
        self.assert_('Work hours are' in form.errors['start_time'][0])

        data = {
            'end_time': now.replace(hour=19)
        }
        form = OccurrenceForm(data)
        self.assertFalse(form.is_valid(), '7pm finishes are not allowed')
        self.assert_('end_time' in form.errors)
        self.assert_('Work hours are' in form.errors['end_time'][0])

        # just to ensure that it does not always return invalid
        data = {
            'end_time': now.replace(hour=14)
        }
        form = OccurrenceForm(data)
        self.assertFalse(form.is_valid())
        self.assertFalse('end_time' in form.errors)

        data = {
            'start_time': now.replace(hour=9)
        }
        form = OccurrenceForm(data)
        self.assertFalse(form.is_valid())
        self.assertFalse('start_time' in form.errors)

    def test_task_form(self):
        alice = User.objects.create_user('alice', 'alice@example.com', 'pass')
        data = {
            'title': 'Write some tests',
            'day': '01/04/2005',
            'start_time': 2,
            'end_time': 12,
            'user': alice.pk,
        }
        form = TaskForm(data)
        self.assertFalse(form.is_valid())

        data['start_time'] = 11
        data['count'] = 3
        form = TaskForm(data)
        self.assert_(form.is_valid())
        tt = TaskType.objects.create(title='why?')
        task = form.save(commit=False)
        task.task_type = tt
        task.author = alice
        task.save()
        task.add_occurrences(form.cleaned_data['start_time'],
                             form.cleaned_data['end_time'],
                             count=form.cleaned_data['count'])
        self.assertEqual(Occurrence.objects.count(), 3)
