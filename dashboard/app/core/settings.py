import os
import pytz
from pathlib import Path

from . import logger
from .config import setup

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-vix#(ofw!k(00xpq49ef($awagrgey@#n@ntp#-4zl&&#wk$xq"

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "admin_menu",
    "core.apps.MyAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Almaty"
USE_I18N = True
USE_TZ = True
ALMATY_TZ = pytz.timezone("Asia/Almaty")

# CELERY SETTINGS
CELERY_BROKER_URL = setup.CELERY_BROKER_URL
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True

# STATIC STORAGE SETTINGS
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_AUTOREFRESH = True
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "static/"
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGGING SETTINGS
LOGGING = logger.config

# ADMIN PANEL SETTINGS
ADMIN_STYLE = {
    "background": "whitesmoke",
    "primary-color": "#205280",
    "primary-text": "#d6d5d2",
    "secondary-color": "#3B75AD",
    "secondary-text": "white",
    "tertiary-color": "#F2F9FC",
    "tertiary-text": "black",
    "breadcrumb-color": "whitesmoke",
    "breadcrumb-text": "black",
    "focus-color": "#eaeaea",
    "focus-text": "#666",
    "primary-button": "#26904A",
    "primary-button-text": " white",
    "secondary-button": "#999",
    "secondary-button-text": "white",
    "link-color": "#4285AC",
    "link-color-hover": "lighten($link-color, 20%)",
    "logo-width": "auto",
    "logo-height": "60px",
}

GOSZAKUP_URL = "http://127.0.0.1:8000"
