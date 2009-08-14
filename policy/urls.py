from django.conf.urls.defaults import *

urlpatterns = patterns('policy.views',
    url(r'^$',
       'project_list',
       name='policy_project_list'),
)

