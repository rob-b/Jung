from django import forms
from django.utils.translation import ugettext_lazy as _
from models import Occurrence
from datetime import datetime
from dateutil.relativedelta import relativedelta

def office_hours(date_obj):
    am = date_obj.replace(hour=8, minute=59, second=59)
    pm = am.replace(hour=18, minute=0, second=1)
    return am < date_obj < pm


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

    def save(self, commit=True):
        # start, end = self.cleaned_data['start_time'], self.cleaned_data['end_time']
        # diff = relativedelta(end, start)
        # if diff.days:
        #     count = diff.days
        #     assert False, "we must add %d occurrences" % count
        return super(OccurrenceForm, self).save(commit)


    class Meta:
        model = Occurrence

