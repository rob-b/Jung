from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from models import Occurrence, Task, TaskType
from datetime import datetime, time, date, timedelta
from dateutil.relativedelta import relativedelta

def office_hours(dt):
    am = datetime.combine(dt.date(), time(9))
    pm = am.replace(hour=18, minute=0, second=1)
    return am <= dt <= pm


class OccurrenceForm(forms.ModelForm):

    def clean_start_time(self):
        """ensure start_time is within office hours

        round up/down to nearest hour"""
        start = self.cleaned_data['start_time']
        if not office_hours(start):
            msg = _('Invalid start time. Work hours are 09:00-18:00')
            raise forms.ValidationError(msg)
        return start.replace(minute=0, second=0)

    def clean_end_time(self):
        """ensure end_time is within office hours

        round up/down to nearest hour"""
        end = self.cleaned_data['end_time']
        if not office_hours(end):
            msg = _('Invalid end time. Work hours are 09:00-18:00')
            raise forms.ValidationError(msg)
        return end.replace(minute=0, second=0)

    def clean(self):
        super(OccurrenceForm, self).clean()
        data = self.cleaned_data
        start = data.get('start_time')
        end = data.get('end_time')
        if start and end:
            if data['end_time'] < data['start_time']:
                raise forms.ValidationError(_('The end cannot be before the start'))
        return data


    class Meta:
        model = Occurrence

INTERVAL = timedelta(hours=+1)
START = time(9)
DELTA = timedelta(hours=+8)
EMPTY_ENTRY = (0, '--------')

def timeslots(start=time(9), delta=timedelta(hours=+8),
              interval=INTERVAL):
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start)
    dtend = dtstart + delta
    options = [EMPTY_ENTRY]

    while dtstart <= dtend:
        options.append((dtstart.hour, dtstart.strftime('%H:%M')))
        dtstart += interval
    return options
timeslot_options = timeslots()

def duration(start=START, delta=DELTA, interval=INTERVAL):
    options = [(8, _('All day')),]
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start)
    dtend = dtstart + delta

    while dtstart < dtend:
        diff = relativedelta(dtend, dtstart)
        if diff.hours == 1:
            options.append((diff.hours, _('%d Hour') % diff.hours))
        else:
            options.append((diff.hours, _('%d Hours') % diff.hours))
        dtstart += interval
    options.append(EMPTY_ENTRY)
    return reversed(options)
duration_options= duration()


class TaskForm(forms.ModelForm):

    task_type = forms.ModelChoiceField(queryset=TaskType.objects.all())
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True),
                                  required=False,
                                  label=_('User'),
                                  help_text=_('Who this task will be'
                                              ' assigned to'))
    day = forms.DateField(widget=SelectDateWidget(), initial=date.today())
    start_time = forms.ChoiceField(label=_('Start time'),
                                   choices=timeslot_options,)
    end_time = forms.IntegerField(
        widget=forms.Select(choices=duration_options),
        label=_('Duration'),
    )
    count = forms.IntegerField(
        label=_('Occurrences'),
        initial=1,
        required=False,
        widget=forms.TextInput(attrs=dict(size=2, maxlength=2)),
        help_text=_('You can set how many (consecutive) days'
                    ' you want this task to occur on'),
    )

    def clean(self):
        data = self.cleaned_data
        day, start = data.get('day'), data.get('start_time'),
        end = data.get('end_time')
        if day and start and end:

            # first we validate the duration doesn't exceed working hours.
            # if it's acceptable we coerce start/end to datetime objects
            day = datetime.combine(day, time(0))
            start = day.replace(hour=int(start))
            end = start + relativedelta(hours=end)
            if not office_hours(end):
                msg = _("Work hours are 09:00-18:00. Please modify the duration")
                self._errors['end_time'] = forms.util.ErrorList([msg])
                del data['end_time']
                return data
            data['start_time'] = start
            data['end_time'] = end
            data['day'] = day
        return data

    def clean_day(self):
        day = self.cleaned_data.get('day')
        if day:
            dt = datetime.combine(day, time(0))
            if dt.weekday() in (5,6):
                keys = {
                    'date': dt.strftime('%B %d %Y'),
                    'day': dt.strftime('%A'),
                }
                msg = _('Work days are Mon-Fri. %(date)s is a %(day)s') % keys
                raise forms.ValidationError(msg)
        return day


    class Meta:
        model = Task
        exclude = 'slug', 'author', 'task_type'
