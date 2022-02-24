import os
from datetime import timedelta

from burl.core import utils
from burl.core.conf import config

DEBUG = config.get("app.debug", bool)
ALLOWED_HOSTS = config.get("security.allowed_hosts", list)

SETTINGS_MODULE = os.path.dirname(os.path.abspath(__file__))
CORE_MODULE = os.path.dirname(SETTINGS_MODULE)
MODULE_ROOT = os.path.dirname(CORE_MODULE)
BASE_DIR = MODULE_ROOT
PROJECT_ROOT = os.path.dirname(MODULE_ROOT)

HOME = utils.get_env("HOME")
SECRET_KEY = config.get("security.secret_key", str)
HASHID_ALPHABET = config.get("app.hashid_alphabet", str)
BURL_BLACKLIST = config.get("app.burl_blacklist", list)
ROUGH_COUNT_MIN = config.get("admin.rough_count_min", int)

ROOT_URLCONF = "burl.core.urls.root"

AUTH_USER_MODEL = "core.BurlUser"
DEFAULT_REDIRECT_URL = config.get("app.default_redirect_url")

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "burl.core",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "django.contrib.admin",
    "django.contrib.sites",
    "django_filters",
    "django_burl",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "burl.core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config.get("db.default.engine", str),
        "NAME": config.get("db.default.name", str),
        "USER": config.get("db.default.user", str),
        "PASSWORD": config.get("db.default.password", str),
        "HOST": config.get("db.default.host", str),
        "PORT": config.get("db.default.port", int),
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIMEZONE = config.get("app.timezone")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = config.get("app.media_root")
STATIC_ROOT = config.get("app.static_root")

LOG_DIR = config.get("logging.log_dir")

BURL_LOG_LEVEL = config.get("logging.burl.level")
APP_LOG_LEVEL = config.get("logging.app.level")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {
            "level": BURL_LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "burl.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5MiB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "level": BURL_LOG_LEVEL,
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": APP_LOG_LEVEL,
        },
        "burl": {
            "handlers": ["console"],
            "level": BURL_LOG_LEVEL,
        },
    },
}

API_PAGE_SIZE = config.get("api.page_size")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": API_PAGE_SIZE,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/api/v1/swagger/"
LOGOUT_URL = "/accounts/logout/"

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "token": {"type": "apiKey", "in": "header", "name": "Authorization"},
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=600),
}

SENDGRID_API_KEY = config.get("security.sendgrid_api_key")

if SENDGRID_API_KEY == 1 or SENDGRID_API_KEY == "":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
