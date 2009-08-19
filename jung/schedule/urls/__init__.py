from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('schedule.views',

    url(r'^$',
        'schedule_list',
        name='schedule_schedule_list'),
    url(r'^(?P<username>[-\w]+)/$',
        'user_schedule', name='schedule_user_schedule'),
    url(r'^(?P<username>[-\w]+)/(?P<month>\w{3})/$',
        'user_schedule', name='schedule_user_schedule_month'),
)
