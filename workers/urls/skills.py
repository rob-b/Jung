from django.conf.urls.defaults import *

urlpatterns = patterns('workers.views',
    url(r'^(?P<skill>[\s\w]+)/$',
        'skill_detail',
        name='workers_skill_detail'),
)
