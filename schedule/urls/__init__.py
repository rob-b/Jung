from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('schedule.views',

    url(r'^$',
        'task_list',
        name='schedule_task_list'),
    url(r'^(?P<username>[-\w]+)/$',
        'user_task_list', name='schedule_user_task_list'),
)
