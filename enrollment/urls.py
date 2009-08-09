from django.conf.urls.defaults import *
from enrollment.forms import EnrollmentForm


urlpatterns = patterns('',
    url(r'^register/$',
       'registration.views.register',
       {'form_class': EnrollmentForm},
       name='registration_register'),
    (r'', include('registration.urls')),
)
