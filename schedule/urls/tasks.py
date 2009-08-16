from django.conf.urls.defaults import *

urlpatterns = patterns('schedule.views',

    url('^create/$',
        'task_add',
        name='schedule_task_add'),
)

