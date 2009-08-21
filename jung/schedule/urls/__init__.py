from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('schedule.views',

    url(r'^$',
        'schedule_list',
        name='schedule_schedule_list'),

    url(r'^weekly/$', 'weekly_schedule', name='schedule_weekly'),
    url(r'^weekly/(?P<day>\w{2})/(?P<month>\w{3})/$', 'weekly_schedule', name='schedule_weekly'),
    url(r'^weekly/(?P<day>\w{2})/(?P<month>\w{3})/(?P<year>\w{4})/$', 'weekly_schedule', name='schedule_weekly'),

    url(r'^(?P<username>[-\w]+)/weekly/$', 'weekly_schedule',
        name='schedule_user_schedule_week'),

    url(r'^(?P<username>[-\w]+)/$',
        'user_schedule', name='schedule_user_schedule'),

    url(r'^(?P<username>[-\w]+)/(?P<month>\w{3})/$',
        'user_schedule', name='schedule_user_schedule_month'),
)
