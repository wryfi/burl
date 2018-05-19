import os
from importlib.machinery import SourceFileLoader
import sys

from burl.core.utils import settings as utils

DEBUG = False
ALLOWED_HOSTS = []

SETTINGS_MODULE = os.path.dirname(os.path.abspath(__file__))
CORE_MODULE = os.path.dirname(SETTINGS_MODULE)
MODULE_ROOT = os.path.dirname(CORE_MODULE)
BASE_DIR = MODULE_ROOT
PROJECT_ROOT = os.path.dirname(MODULE_ROOT)

HOME = utils.get_env('HOME')
SECRET_KEY = utils.get_env('BURL_SECRET_KEY')
HASHID_SALT = utils.get_env('BURL_HASHID_SALT')
HASHID_ALPHABET = utils.get_env('BURL_HASHID_ALPHABET', 'abcdefghjkmnpqrstuvwxyz0123456789')
DEFAULT_REDIRECT_URL = utils.get_env('BURL_DEFAULT_REDIRECT', 'https://en.wikipedia.org/')
HASHID_BLACKLIST = ['admin', 'api']

ROOT_URLCONF = 'burl.core.urls.root'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'burl.core',
    'burl.redirects',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'burl.core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'burl',
        'USER': utils.get_env('BURL_POSTGRES_USER'),
        'PASSWORD': utils.get_env('BURL_POSTGRES_PASSWORD'),
        'HOST': utils.get_env('BURL_POSTGRES_HOST'),
        'PORT': utils.get_env('BURL_POSTGRES_PORT')
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(HOME, 'var', 'burl', 'media')
STATIC_ROOT = os.path.join(HOME, 'share', 'burl', 'static')

LOG_DIR = utils.get_log_dir()

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
      'verbose': {
          'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
          'datefmt' : "%d/%b/%Y %H:%M:%S"
      },
      'simple': {
          'format': '%(levelname)s %(message)s'
      },
    },
    'handlers': {
      'file': {
          'level': 'DEBUG',
          'class': 'logging.handlers.RotatingFileHandler',
          'filename': os.path.join(LOG_DIR, 'burl.log'),
          'maxBytes': 1024 * 1024 * 5,  # 5MiB
          'backupCount': 5,
          'formatter': 'verbose'
      },
    },
    'loggers': {
      'django': {
          'handlers': ['file'],
          'propagate': True,
          'level': 'DEBUG',
      },
      'burl': {
          'handlers': ['file'],
          'level': 'DEBUG',
      },
    }
}


module = sys.modules[__name__]

# override settings from the first configuration file we find
home = os.environ.get('HOME', '/tmp')
config_dirs = ['/etc/burl', os.path.join(home, '.config', 'burl'), os.path.join(home, 'etc', 'burl')]
for config_dir in config_dirs:
    config_file = os.path.join(config_dir, 'burlrc')
    if os.path.isfile(config_file):
        local_settings = SourceFileLoader('local_settings', config_file).load_module()
        for attr in dir(local_settings):
            if attr.isupper():
                setattr(module, attr, getattr(local_settings, attr))
