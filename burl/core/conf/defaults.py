import os

from burl.core import utils

DEBUG = False
ALLOWED_HOSTS = ['*']

SETTINGS_MODULE = os.path.dirname(os.path.abspath(__file__))
CORE_MODULE = os.path.dirname(SETTINGS_MODULE)
MODULE_ROOT = os.path.dirname(CORE_MODULE)
BASE_DIR = MODULE_ROOT
PROJECT_ROOT = os.path.dirname(MODULE_ROOT)

HOME = utils.get_env('HOME')
SECRET_KEY = utils.get_env('BURL_SECRET_KEY')
HASHID_ALPHABET = utils.get_env('BURL_HASHID_ALPHABET', 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789')
BURL_BLACKLIST = ['admin', 'api', 'static', 'media']
ROUGH_COUNT_MIN = 1000

ROOT_URLCONF = 'burl.core.urls.root'

AUTH_USER_MODEL = 'core.BurlUser'
DEFAULT_REDIRECT_URL = utils.get_env('DEFAULT_REDIRECT_URL', 'http://wryfi.net')

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'burl.core',
    'burl.redirects',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'django.contrib.admin',
    'django_filters'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'NAME': utils.get_env('BURL_POSTGRES_DB', 'burl'),
        'USER': utils.get_env('BURL_POSTGRES_USER', 'burl'),
        'PASSWORD': utils.get_env('BURL_POSTGRES_PASSWORD'),
        'HOST': utils.get_env('BURL_POSTGRES_HOST', '127.0.0.1'),
        'PORT': int(utils.get_env('BURL_POSTGRES_PORT', 5432))
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

TIMEZONE = utils.get_env('BURL_TIMEZONE', 'America/Los_Angeles')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = utils.get_env('BURL_MEDIA_ROOT', os.path.join(HOME, 'var', 'burl', 'media'))
STATIC_ROOT = utils.get_env('BURL_STATIC_ROOT', os.path.join(HOME, 'share', 'burl', 'static'))

LOG_DIR = utils.get_env('BURL_LOG_DIR', utils.get_log_dir())

BURL_LOG_LEVEL = utils.get_env('BURL_LOG_LEVEL', 'WARNING')
APP_LOG_LEVEL = utils.get_env('BURL_APP_LOG_LEVEL', 'INFO')


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
          'level': BURL_LOG_LEVEL,
          'class': 'logging.handlers.RotatingFileHandler',
          'filename': os.path.join(LOG_DIR, 'burl.log'),
          'maxBytes': 1024 * 1024 * 5,  # 5MiB
          'backupCount': 5,
          'formatter': 'verbose'
      },
      'console': {
          'class': 'logging.StreamHandler',
          'formatter': 'verbose',
          'level': BURL_LOG_LEVEL
      }
    },
    'loggers': {
      '': {
          'handlers': ['console'],
          'level': APP_LOG_LEVEL,
      },
      'burl': {
          'handlers': ['console'],
          'level': BURL_LOG_LEVEL,
      },
    }
}

API_PAGE_SIZE = int(utils.get_env('BURL_API_PAGE_SIZE', 100))

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': API_PAGE_SIZE,
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

CORS_ORIGIN_ALLOW_ALL = True

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/api/v1/swagger'
LOGOUT_URL = '/accounts/logout/'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'token': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}

SENDGRID_API_KEY = utils.get_env('BURL_SENDGRID_API_KEY', 1)

if SENDGRID_API_KEY == 1 or SENDGRID_API_KEY == '':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

