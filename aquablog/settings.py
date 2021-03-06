"""Settings for Zinnia Aquablog"""
import os
PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

gettext = lambda s: s

DEBUG = True

DATABASES = {'default':
             {'ENGINE': 'django.db.backends.sqlite3',
              'NAME': os.path.join(os.path.dirname(__file__), 'aquablog.db')}
             }

TIME_ZONE = 'Europe/Paris'

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

AUTH_PROFILE_MODULE = 'aquablog.UserProfile'

SECRET_KEY = 'jo-1rzm(%sf)3#n+fb7h955yu$3(pt63abhi12_t7e^^5q8dyw'

ACCOUNT_ACTIVATION_DAYS = 7

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'andrey.galimshyn@gmail.com'
EMAIL_HOST_PASSWORD = '1Heckfyjdf'
EMAIL_USE_TLS = True

USE_TZ = True
USE_I18N = True
USE_L10N = True

SITE_ID = 1

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', gettext('English')),
)

'''
    ('fr', gettext('French')),
    ('de', gettext('German')),
    ('es', gettext('Spanish')),
    ('it', gettext('Italian')),
    ('nl', gettext('Dutch')),
    ('hu', gettext('Hungarian')),
    ('cs', gettext('Czech')),
    ('sk', gettext('Slovak')),
    ('ru', gettext('Russian')),
    ('pl', gettext('Polish')),
    ('eu', gettext('Basque')),
    ('ca', gettext('Catalan')),
    ('tr', gettext('Turkish')),
    ('hr_HR', gettext('Croatian')),
    ('pt_BR', gettext('Brazilian Portuguese')),
    ('fi_FI', gettext('Finnish (Finland)')),
    ('zh_CN', gettext('Simplified Chinese')),
'''

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'aquablog.urls'
TEMPLATE_DIRS = (
    'D:/Projects/tech_forum/aquablog/aquablog/templates'
)
LOGIN_REDIRECT_URL = '/blog/'
LOGIN_URL = 'http://127.0.0.1:8000/login'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'zinnia.context_processors.version',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sitemaps',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'registration',
    'mptt',
    'zinnia',
    'tagging',
    'django_xmlrpc',
    'aquablog',
)

from zinnia.xmlrpc import ZINNIA_XMLRPC_METHODS
XMLRPC_METHODS = ZINNIA_XMLRPC_METHODS
