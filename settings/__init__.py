# Django settings for jung project.
import os
PROJECT_DIR = os.path.dirname(os.path.realpath(os.path.join(__file__, '..')))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_DIR, 'jung.db')
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# media paths and urls
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'assets')
ATTACHMENT_ROOT = os.path.join(PROJECT_DIR, 'attachments')
MEDIA_URL = '/assets/'
ATTACHMENT_URL = '/attachments/'
ADMIN_MEDIA_PREFIX = '/media/'

# thumbnail settings
# THUMBNAIL_BASEDIR =  ATTACHMENT_ROOT
THUMBNAIL_SUBDIR = 'thumbnails'
THUMBNAIL_DEBUG = DEBUG

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(w#zdo)sh^1q3bn)0d-%(0!xg@eag=lc!@q+=bp%ulo#3-l&ys'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'hostel.context_processors.attachment_url',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# account settings
AUTH_PROFILE_MODULE = 'workers.employee'
ACCOUNT_ACTIVATION_DAYS = 3
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/employees/'

ROOT_URLCONF = 'jung.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'templates', 'hostel'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.databrowse',
    'hostel',
    'workers',
    'sorl.thumbnail',
    'typogrify',
    'django_extensions',
    'contacts',
    'compress',
    'registration',
    'schedule',
)



try:
    from settings.local import *
    from settings.compress import *
except ImportError:
    pass
