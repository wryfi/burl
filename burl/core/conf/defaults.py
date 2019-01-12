import os

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
HASHID_ALPHABET = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789'
DEFAULT_REDIRECT_URL = 'https://masterofallscience.com/meme/S02E08/331081.jpg?b64lines=IE9oLiBPaCwgbXkgZ29kLiBIb3cgZGlkIEkgZ2V0IGhlcmU_IEhlbGxvPyE='
BURL_BLACKLIST = ['admin', 'api']

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
        'USER': 'burl',
        'PASSWORD': utils.get_env('BURL_POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 5432
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
