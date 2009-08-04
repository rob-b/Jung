from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^$',
        'django.views.generic.simple.redirect_to',
        {'url': '/employees/'},
        name='worker_homepage'),
    (r'^employees/', include('workers.urls')),
)

from django.conf import settings
if settings.DEBUG:
    MEDIA_URL = settings.MEDIA_URL.strip('/')
    ATTACHMENT_URL = settings.ATTACHMENT_URL.strip('/')
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % MEDIA_URL, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT,
          'show_indexes': True}),
        (r'^%s(?P<path>.*)$' % ATTACHMENT_URL, 'django.views.static.serve',
         {'document_root': settings.ATTACHMENT_ROOT,
          'show_indexes': True}),
)
