from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^jung/', include('jung.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
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

from workers import models
from django.contrib import databrowse
databrowse.site.register(models.Employee)
databrowse.site.register(models.Skill)
urlpatterns += patterns('',
    (r'^databrowse/(.*)', databrowse.site.root),
)
