from django.conf.urls.defaults import *

urlpatterns = patterns('policy.views',
    url(r'^$',
       'project_list',
       name='policy_project_list'),

    url(r'^(?P<slug>[-\w]+)/$',
        'project_detail',
        name='policy_project_detail'),
)

