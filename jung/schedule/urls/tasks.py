from django.conf.urls.defaults import *

urlpatterns = patterns('schedule.views',

    url('^create/$',
        'task_add',
        name='schedule_task_add'),

    url(r'^(?P<project>[-\w]+)/(?P<slug>[-\w]+)/$',
        'task_detail', name='schedule_task_detail'),

    url(r'^(?P<username>[-\w]+)/$',
        'user_task_list', name='schedule_user_task_list'),
)

