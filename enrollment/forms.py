from django import forms
from django.core.urlresolvers import resolve, Resolver404
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from urlparse import urlparse
from profiles import urls

class EnrollmentForm(RegistrationFormUniqueEmail):

    def clean_username(self):
        username = super(EnrollmentForm, self).clean_username()
        for pattern in urls.urlpatterns:
            if pattern.resolve(username+'/'):
                msg = _('This username is already taken. Please choose another')
                raise forms.ValidationError(msg)
        return username
