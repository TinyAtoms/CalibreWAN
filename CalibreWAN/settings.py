"""
Django settings for CalibreWAN project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
import sys
# section to use .env to seperate sensitive settings in a seperate file that shouldn't go in git
from django.utils.translation import ugettext_lazy as _

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = bool(int(os.environ["DEBUG"]))
ACCOUNT_ALLOW_SIGNUPS= bool(int(os.environ["ACCOUNT_ALLOW_SIGNUPS"]))
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")


ACCOUNT_ADAPTER = 'CalibreWAN.adapter.CustomAccountAdapter'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'dal',  # autocomplete
    'dal_select2',  # autocomplete
    # 'debug_toolbar',  # debug
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django.contrib.sites",  # everything from here till the last allauth is for oAuth2
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.microsoft',
    "library",
    'api.apps.ApiConfig',
]

SITE_ID = 1 # changed from 2

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',  # debug
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', # security
    'django.contrib.auth.middleware.AuthenticationMiddleware', # auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware', #translation
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # security
    'csp.middleware.CSPMiddleware', # security
]

if DEBUG:  # the REALLY hacky way to show debug toolbar
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda x: True,
    }

ROOT_URLCONF = 'CalibreWAN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',  # for alauth
            ],
        },
    },
]

WSGI_APPLICATION = 'CalibreWAN.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "Persistent" / 'db.sqlite3',
    },
    'calibre': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "UserLibrary" / "metadata.db",
    }
}
DATABASE_ROUTERS = ["CalibreWAN.db_routers.CalibreRouter", "CalibreWAN.db_routers.DjangoRouter"]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

# auth backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_MAX_EMAIL_ADDRESSES = 3
ACCOUNT_SIGNUP_REDIRECT_URL = "/"
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = False  # the behaviour that irritates me
LOGIN_REDIRECT_URL = "/"
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (
    BASE_DIR / "locale",
)

LANGUAGES = (
    ('en-us', _('English')),
    ('nl', _('Dutch')),
)
LANGUAGE_CODE = 'en-us' 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# CSP stuff

# default source as self
CSP_DEFAULT_SRC = ("'self'", )
  
# style from our domain and bootstrapcdn
CSP_STYLE_SRC = ("'self'",
    "cdnjs.cloudflare.com",
    "cdn.datatables.net",
    "use.fontawesome.com",
    "fonts.googleapis.com",
    "cdn.jsdelivr.net"
    )
  
# scripts from our domain and other domains
CSP_SCRIPT_SRC = ("'self'",
    "cdnjs.cloudflare.com",
    "cdn.datatables.net",
    "cdn.jsdelivr.net",
    )

CSP_IMG_SRC = ("'self'",
    "www.google-analytics.com",
    "raw.githubusercontent.com",
    "googleads.g.doubleclick.net")
  
# loading manifest, workers, frames, etc
CSP_FONT_SRC = ("'self'",
                "use.fontawesome.com",
                "fonts.googleapis.com",
                "fonts.gstatic.com" 
                )
                
CSP_CONNECT_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'self'", )
CSP_BASE_URI = ("'self'", )
CSP_FRAME_ANCESTORS = ("'self'", )
CSP_INCLUDE_NONCE_IN = ('script-src', )
CSP_MANIFEST_SRC = ("'self'", )
CSP_WORKER_SRC = ("'self'", )
CSP_MEDIA_SRC = ("'self'", )
CSP_FORM_ACTION = ("'self'", "github.com", "accounts.google.com")

# SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "Strict"
# SESSION_COOKIE_SAMESITE = "Strict"
