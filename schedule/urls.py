from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('schedule.views',

    url(r'^$',
        'task_list',
        {'user_id': 1},
        name='schedule_task_list'),
)
