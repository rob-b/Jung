from django.db import models
from django.utils.translation import ugettext_lazy as _
from hostel.models import MarkdownField
from django_extensions.db.fields import AutoSlugField
from dateutil import rrule
from managers import OccurrenceManager


class Task(models.Model):

    """once upon a time there was a user named Alice...

    Alice clicks through to her calendar and sees a list of the next 30
    days. some of these days are marked to indicate a particular project that
    Alice should be working on on. Some days are fully dedicated to one
    particular project, others are split across two or more projects.

    Alice can also book other users to work on particular projects. on a day
    when the second user Bob is available Alice can select a project, and
    optionally a time slot, to schedule Bob to work on that project.

    But how are tasks related to projects? When a project is created a default
    "work on project x" task type is created to complement it. When Alice, or Bob,
    schedules a fellow user to work on a particular project it will by default
    create an task associated with the default task type of that project. Of
    course, Alice would also be able to create a custom task if she should so
    choose.
    """

    title = models.CharField(_('Title'), max_length=100)
    slug = AutoSlugField(_('Slug'), populate_from='title', editable=True)
    body = MarkdownField(_('Body'), blank=True)
    author = models.ForeignKey('auth.user', verbose_name=_('Author'),
                              related_name='tasks_created')
    user = models.ForeignKey('auth.user', verbose_name=_('User'))
    task_type = models.ForeignKey('schedule.TaskType',
                                   verbose_name=_('Task type'))


    def __unicode__(self):
        return self.title

    def add_occurrences(self, start_time, end_time, **rrule_params):
        '''
        Add one or more occurences to the task using a comparable API to
        ``dateutil.rrule``.

        If ``rrule_params`` does not contain a ``freq``, one will be defaulted
        to ``rrule.DAILY``.

        Because ``rrule.rrule`` returns an iterator that can essentially be
        unbounded, we need to slightly alter the expected behavior here in order
        to enforce a finite number of occurrence creation.

        If both ``count`` and ``until`` entries are missing from ``rrule_params``,
        only a single ``Occurrence`` instance will be created using the exact
        ``start_time`` and ``end_time`` values.
        '''
        rrule_params.setdefault('freq', rrule.DAILY)

        if 'count' not in rrule_params and 'until' not in rrule_params:
            self.occurrence_set.create(start_time=start_time, end_time=end_time)
        else:
            delta = end_time - start_time
            for ev in rrule.rrule(dtstart=start_time, **rrule_params):
                self.occurrence_set.create(start_time=ev, end_time=ev + delta)


class TaskType(models.Model):
    title = models.CharField(_('Title'), max_length=100, unique=True)


class Occurrence(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    task = models.ForeignKey('schedule.Task', verbose_name=_('task'))
    objects = OccurrenceManager.as_manager()

    def __unicode__(self):
        return u'%s at %s' % (self.task.title, self.start_time)
