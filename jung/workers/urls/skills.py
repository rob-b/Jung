from django.conf.urls.defaults import *

urlpatterns = patterns('workers.views',
    url(r'^$', 'skill_list', name='workers_skill_list'),
    url(r'^(?P<skill>[-\w]+)/$',
        'skill_detail',
        name='workers_skill_detail'),
)
