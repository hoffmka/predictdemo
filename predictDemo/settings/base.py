"""Base settings shared by all environments"""

# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l9dulfp$k8hw0uvbrwefh8mi8b_syipuh5*ec2zz$z%amz6mz$'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

from django.conf.locale.de import formats as de_formats
#de_formats.DATETIME_FORMAT = "d b Y H:i:s"
de_formats.DATE_FORMAT = "d.m.Y"

# Application definition

INSTALLED_APPS = [
    # my apps
    'apps.accounts',
    'apps.dashtest',
    'apps.patients',
    'apps.predictions',
    'apps.trials',
    'apps.dbviews', # Standard and user defined views
    'apps.udv_destiny', # user defined views for destiny trial
    'apps.shiny', # embeds shiny apps

    #third party apps
    'rolepermissions', # role-permission --> https://django-role-permissions.readthedocs.io/en/stable/index.html
    'django_plotly_dash.apps.DjangoPlotlyDashConfig', # for implementation dash apps in django --> https://django-plotly-dash.readthedocs.io/en/latest/index.html
    'bootstrap4',
 #   'channels',
 #   'dpd_static_support',
    'lazysignup', # guest accounts --> https://django-lazysignup.readthedocs.io/en/latest/index.html
    'django_filters', # Filter and Search app
    'django_tables2', # Django tables with filtering and order feature by default
    'docs',

    # django apps
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/


#==============================================================================
# Project URLS and media settings
#==============================================================================

ROOT_URLCONF = 'predictDemo.urls'

LOGIN_URL='accounts:login'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_REDIRECT_URL = 'home'

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = os.path.join(PROJECT_DIR,'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

#PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
#STATIC_ROOT = os.path.join(PROJECT_DIR, 'collectstatic')

#==============================================================================
# Templates
#==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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


#==============================================================================
# Middleware
#==============================================================================


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    #'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    #'django_plotly_dash.middleware.BaseMiddleware',
    #'django_plotly_dash.middleware.ExternalRedirectionMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


#==============================================================================
# Auth / security
#==============================================================================


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
  'django.contrib.auth.backends.ModelBackend',
  'lazysignup.backends.LazySignupBackend',
)

#==============================================================================
# Miscellaneous project settings
#==============================================================================

#==============================================================================
# Third party app settings
#==============================================================================

# for role permissions
#-----------------------

ROLEPERMISSIONS_MODULE = 'predictDemo.roles.base'
ROLEPERMISSIONS_REGISTER_ADMIN = True
ROLEPERMISSIONS_REDIRECT_TO_LOGIN = True

# for django-plotly-dash
#-----------------------
ASGI_APPLICATION = 'predictDemo.routing.application'

# Caching - demo uses redis as this is present due to channels use

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.25.69.150:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient"
        },
        "KEY_PREFIX": "dpd-demo"
    }
}

# Channels config, to use channel layers

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('10.25.69.150', 6379),],
        },
    },
}

# Staticfiles finders for locating dash app assets and related files

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'djangobower.finders.BowerFinder',

    #'django_plotly_dash.finders.DashAssetFinder',
    #'django_plotly_dash.finders.DashComponentFinder',
    #'django_plotly_dash.finders.DashAppDirectoryFinder',
]

# Plotly components containing static content that should
# be handled by the Django staticfiles infrastructure

# PLOTLY_COMPONENTS = [
#    'dash_core_components',
#    'dash_html_components',
    #'dash_bootstrap_components',
#    'dash_renderer',
    #'dpd_components',
    #'dpd_static_support',
#]

# PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
#    "ws_route" :   "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
#    "http_route" : "dpd/views",

    # Flag controlling existince of http poke endpoint
#    "http_poke_enabled" : True,

    # Insert data for the demo when migrating
#    "insert_demo_migrations" : False,

    # Timeout for caching of initial arguments in seconds
#    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
#    "view_decorator": None,

    # Flag to control location of initial argument storage
#    "cache_arguments": True,

    # Flag controlling local serving of assets
#    "serve_locally": True,
#} """

DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

# Settings for sphinx documentation that will be used by 'django-docs'
DOCS_ROOT = os.path.join(BASE_DIR, '../docs/build/html')
#Docs access level (public by default). Possible values:
#public - (default) docs are visible to everyone
#login_required - docs are visible only to authenticated users
#staff - docs are visible only to staff users (user.is_staff == True)
#superuser - docs are visible only to superusers (user.is_superuser == True)
DOCS_ACCESS = 'login_required'