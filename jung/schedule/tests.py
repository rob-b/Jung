from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import Task, TaskType, Occurrence
from policy.models import Project
from datetime import datetime, date, timedelta, time
import dateutil
from dateutil.relativedelta import relativedelta
from dateutil import rrule
from forms import OccurrenceForm, TaskForm

class ScheduleTest(TestCase):

    def setUp(self):
        self.project = Project.objects.create(
            description = 'A nice test project',
            status = Project.ACTIVE,
            name = 'Test Project',
        )
        self.alice = User.objects.create_user('alice', 'alice@example.com', 'pass')
        self.bob = User.objects.create_user('bob', 'bob@example.com', 'pass')
        self.et = TaskType.objects.create(title='some-project')
        self.task = Task.objects.create(
            title='Task #1',
            author=self.alice,
            user=self.bob,
            task_type=self.et,
            project=self.project,
        )

    def tearDown(self):
        User.objects.all().delete()
        Task.objects.all().delete()
        TaskType.objects.all().delete()

    def test_user_schedule(self):
        start = datetime.now()
        end = start + relativedelta(days=+1)
        self.task.add_occurrences(start, end, count=3,)
        task2 = Task.objects.create(
            title='The second task',
            author=self.alice,
            user=self.bob,
            task_type=self.et,
            project=self.project,
        )
        dest = reverse('schedule_schedule_list')
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
        data = {
            'title': 'Write some tests',
            'day': '01/04/2005',
            'start_time': 2,
            'end_time': 2,
            'user': self.alice.pk,
            'project': self.project.pk,
            'status': Project.ACTIVE,
            'task_type': self.et.pk,
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
        task.author = self.alice
        task.save()
        task.add_occurrences(form.cleaned_data['start_time'],
                             form.cleaned_data['end_time'],
                             count=form.cleaned_data['count'])
        self.assertEqual(Occurrence.objects.count(), 3)

    def test_week_of_method(self):

        # set the start to the begining of the week minus 1 day.
        start = date.today()
        start = start + timedelta(days=-(start.weekday() - 1))
        end = start + relativedelta(days=+1)

        # set the task to occur 5 times, this should be 4 times this week
        self.task.add_occurrences(start, end, count=5,)

        dt = date.today()
        self.assert_(Task.objects.week_of(dt),
                     "There should be a task available for this week")

        # now go back a week and there should be no tasks
        dt = date.today()
        offset = dt.weekday() + 7
        dt = dt + timedelta(days=-offset)
        self.assertFalse(Task.objects.week_of(dt))

        # now create a task occurrence a week ago and voila...
        end = dt + relativedelta(days=+1)
        self.task.add_occurrences(dt, end, count=2)
        self.assert_(Task.objects.week_of(dt))

    def test_conflicts(self):
        """Double bookings should be flagged"""

        # add 3 occurences of a task starting today
        start = datetime.combine(date.today(), time(10))
        end = start + relativedelta(hours=+4)
        self.task.add_occurrences(start, end, count=3,)

        task_2 = Task.objects.create(
            title='Secodary task',
            author=self.alice,
            user=self.bob,
            task_type=self.et,
            project=self.project,
        )
        task_2.add_occurrences(start, end)

        # there should be two occurences that are not conflicted
        self.assertEqual(2, Occurrence.objects.pristine().count())

        # and another two that are conflicted
        self.assertEqual(2, Occurrence.objects.conflicted().count())

        # the conflicted occurences are from different tasks
        first, second = Occurrence.objects.conflicted()
        self.assertNotEqual(first.task.pk, second.task.pk)

        # the pristine occurences are from the same tasks
        first, second = Occurrence.objects.pristine()
        self.assertEqual(first.task.pk, second.task.pk)

    def test_one_day_at_a_time(self):
        """Can not specifiy an end time for tomorrow"""

