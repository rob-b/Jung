from django import forms
from django.core.urlresolvers import resolve, Resolver404
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from urlparse import urlparse

class EnrollmentForm(RegistrationFormUniqueEmail):

    def clean_username(self):
        username = super(EnrollmentForm, self).clean_username()
        try:
            resolve(urlparse('/' + username + '/')[2])
        except Resolver404:
            return username
        raise forms.ValidationError(_('This username is already taken. Please'
                                      ' choose another'))
