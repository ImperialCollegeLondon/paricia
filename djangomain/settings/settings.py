########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

"""Django settings for djangomain project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import re
from datetime import timedelta
from pathlib import Path

from django_bootstrap5.core import BOOTSTRAP5_DEFAULTS

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800
FILE_UPLOAD_MAX_MEMORY_SIZE = 27000000

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = str(Path(__file__).resolve().parent.parent.parent)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "mj7(ja+=@-xxx&(t)_2um%y^khe17txt&^_ydw0d168%+so#yd"

# SECURITY WARNING: don't run with debug turned on in production!

# DEBUG = False
DEBUG = True
ALLOWED_HOSTS = ["*"]
# ALLOWED_HOSTS = ['127.0.0.1', ]

# DEBUG = False
# ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    "station.apps.StationConfig",
    "sensor.apps.SensorConfig",
    "variable.apps.VariableConfig",
    "formatting.apps.FormattingConfig",
    "measurement",
    "importing.apps.ImportingConfig",
    "django_bootstrap5",
    "django_extensions",
    "django_filters",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "huey.contrib.djhuey",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
    "management",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_plotly_dash.apps.DjangoPlotlyDashConfig",
    "guardian",
    "django_tables2",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_plotly_dash.middleware.BaseMiddleware",
    "djangomain.middleware.TimezoneMiddleware",
]

ROOT_URLCONF = "djangomain.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "djangomain.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": "db",
        "PORT": "5432",
    },
    "huey": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "huey",
        "FILE": os.path.join(BASE_DIR, "data", "huey.db"),
    },
}

if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES["default"]["HOST"] = "127.0.0.1"

HUEY = {
    "huey_class": "huey.SqliteHuey",
    "name": DATABASES["huey"]["NAME"],
    "immediate": False,
    "consumer": {"workers": 2},
    "connection": {
        "filename": DATABASES["huey"]["FILE"],
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa E501
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [  # Extra static directories
    os.path.join(BASE_DIR, "static"),
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "data/media")

INTERNAL_IPS = ("127.0.0.1",)


########################################################################

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

########################################################################
# Requerido para enviar mensajes de correo a través de servidor SMTP
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "10.1.1.18"
EMAIL_PORT = 25
#
#########################################################################

#########################################################################
#
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # this is default
    "guardian.backends.ObjectPermissionBackend",
)

ANONYMOUS_USER_NAME = "AnonymousUser"

#
#########################################################################

# Fixtures for tests
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent.parent)
FIXTURE_DIRS = [os.path.join(PROJECT_ROOT, "utilities/data")]

# Custom User model
AUTH_USER_MODEL = "management.User"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

REST_AUTH_SERIALIZERS = {
    "USER_DETAILS_SERIALIZER": "management.serializers.UserSerializer",
}


ACCESS_TOKEN_LIFETIME_IN_SECONDS = 2 * 60 * 60  # 2 hours

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=ACCESS_TOKEN_LIFETIME_IN_SECONDS),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3650),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

LOGIN_URL = "auth:login"
LOGIN_REDIRECT_URL = "home"

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap5.html"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

X_FRAME_OPTIONS = "SAMEORIGIN"

javascript_url = BOOTSTRAP5_DEFAULTS["javascript_url"]["url"]

if not (match := re.search("@\\d+\\.\\d+\\.\\d+/", javascript_url)):
    raise ValueError("Unable to determine Bootstrap 5 javascript version.")

javascript_version = javascript_url[slice(*match.span())]

BOOTSTRAP5 = dict(
    css_url=dict(
        url=f"https://cdn.jsdelivr.net/npm/bootswatch{javascript_version}dist/flatly/bootstrap.min.css",
        integrity="sha384-Gn6TIhloBHiLpI1VM8qQG+H8QQhHXqsiUlMLS4uhr9gqQzFsOhMTo0lSTMbOrLoI",
        crossorigin="anonymous",
    )
)

# Staticfiles finders for locating dash app assets and related files
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django_plotly_dash.finders.DashAssetFinder",
    "django_plotly_dash.finders.DashComponentFinder",
    "django_plotly_dash.finders.DashAppDirectoryFinder",
]

# Plotly components containing static content that should
# be handled by the Django staticfiles infrastructure

PLOTLY_COMPONENTS = [
    # Common components (ie within dash itself) are automatically added
    # django-plotly-dash components
    "dpd_components"
]
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
