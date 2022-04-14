import logging
import os
from datetime import timedelta

from burl.core import utils
from burl.core.conf import config

# NOTE: attempt to group related settings together

# situational awareness settings
SETTINGS_MODULE = os.path.dirname(os.path.abspath(__file__))
CORE_MODULE = os.path.dirname(SETTINGS_MODULE)
MODULE_ROOT = os.path.dirname(CORE_MODULE)
BASE_DIR = MODULE_ROOT
PROJECT_ROOT = os.path.dirname(MODULE_ROOT)
HOME = utils.get_env("HOME")

# general application settings
DEBUG = config.get_bool("app.debug")
HASHID_ALPHABET = config.get_string("app.hashid_alphabet")
BURL_BLACKLIST = config.get_list("app.burl_blacklist")
ROUGH_COUNT_MIN = config.get_int("admin.rough_count_min")

# security related settings
AUTH_USER_MODEL = "core.BurlUser"
SECRET_KEY = config.get_string("security.secret_key")
ALLOWED_HOSTS = config.get_list("security.allowed_hosts")
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = config.get_bool("security.cors.allow_all_origins")
CORS_ALLOWED_ORIGINS = config.get_list("security.cors.allowed_origins")
CORS_ALLOWED_ORIGIN_REGEXES = config.get_list("security.cors.allowed_origin_regexes")
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=config.get_int("security.jwt.access_lifetime")
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=config.get_int("security.jwt.refresh_lifetime")
    ),
}

# localization related settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = config.get_string("app.time_zone")
USE_I18N = True
USE_L10N = True
USE_TZ = True

# http related settings
WSGI_APPLICATION = "burl.core.wsgi.application"
USE_X_FORWARDED_HOST = config.get_bool("http.use_x_forwarded_host")
SECURE_PROXY_SSL_HEADER = (
    config.get("http.secure_proxy_ssl_header_name"),
    config.get("http.secure_proxy_ssl_header_value"),
)

# URLs and URL configurations
ROOT_URLCONF = "burl.core.urls.root"
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGIN_REDIRECT_URL = "/api/v2/swagger/"
STATIC_URL = "/static/"
DEFAULT_REDIRECT_URL = config.get("app.default_redirect_url")

# file resources
MEDIA_ROOT = config.get("app.media_root")
STATIC_ROOT = config.get("app.static_root")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# rest framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": config.get_int("api.page_size"),
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "token": {"type": "apiKey", "in": "header", "name": "Authorization"},
    },
}

# email settings
SENDGRID_API_KEY = config.get("mail.sendgrid_api_key")
if SENDGRID_API_KEY == 1 or SENDGRID_API_KEY == "":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
DEFAULT_FROM_EMAIL = config.get("mail.default_from_email")

# high-level logging configuration (see more detailed configs below)
LOG_DIR = config.get("logging.log_dir")
LOG_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}
BURL_LOG_LEVEL = LOG_LEVELS.get(config.get("logging.burl.level"), logging.WARN)
APP_LOG_LEVEL = LOG_LEVELS.get(config.get("logging.app.level"), logging.WARN)

# database configuration
DATABASES = {
    "default": {
        "ENGINE": config.get_string("db.default.engine"),
        "NAME": config.get_string("db.default.name"),
        "USER": config.get_string("db.default.user"),
        "PASSWORD": config.get_string("db.default.password"),
        "HOST": config.get_string("db.default.host"),
        "PORT": config.get_int("db.default.port"),
    },
}

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

try:
    import django_extensions

    INSTALLED_APPS.append("django_extensions")
except ImportError:
    pass

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
