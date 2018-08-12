"""
Idea Pool settings

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
from os.path import dirname

# Build paths inside the project like this: os.path.join(SETTINGS_DIR, ...)
# SETTINGS_DIR: written/written/settings/
SETTINGS_DIR = dirname(os.path.abspath(__file__))

# APP_ROOT: idea_pool/idea_pool
APP_ROOT = dirname(SETTINGS_DIR)

# Project Dir: idea_pool/manage.py
PROJECT_DIR = dirname(APP_ROOT)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# =======================================================================
# SECURITY SETTINGS
# =======================================================================
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1',]

# =======================================================================
# APPLICATIONS
# On application start-up, Django looks for migrations files for each app
# =======================================================================
DJANGO_APPS = [
    # Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Blog
    'accounts',
    # 'blog',
    # 'core',
]

EXTERNAL_APPS = [
    # Tools
    'rest_framework',
    'django_extensions',
    'rest_framework_extensions'
]
INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =======================================================================
# MEDIA MANAGEMENT
# Static files and template management
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# =======================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(APP_ROOT, 'templates')]
        ,
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(APP_ROOT, 'assets')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(APP_ROOT, 'uploads')

STATICFILES_DIRS = [
    # '/var/www/static/',
]

# =======================================================================
# CONFIGURATION SETTINGS
# =======================================================================
ROOT_URLCONF = 'idea_pool.urls'
WSGI_APPLICATION = 'idea_pool.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# =======================================================================
# DATABASE SETTINGS
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# =======================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('WRITTEN_DB_NAME'),
        'HOST': os.getenv('WRITTEN_DB_HOST'),
        'PORT': os.getenv('WRITTEN_DB_PORT'),
        'USER': os.getenv('WRITTEN_DB_USER'),
        'PASSWORD': os.getenv('WRITTEN_DB_PASSWORD'),
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('WRITTEN_TEST_DB_NAME'),
        'HOST': os.getenv('WRITTEN_TEST_DB_HOST'),
        'PORT': os.getenv('WRITTEN_TEST_DB_PORT'),
        'USER': os.getenv('WRITTEN_TEST_DB_USER'),
        'PASSWORD': os.getenv('WRITTEN_TEST_DB_PASSWORD'),
    },
}

# =======================================================================
# AUTHENTICATION
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
# =======================================================================
AUTH_USER_MODEL = 'accounts.User'

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

# =======================================================================
# THIRD-PARTY INTEGRATION SETTINGS
# For settings specific to third-party modules and apis.
# The credentials below are NOT FOR PRODUCTION. Overwrite them by editing
# your dev.py
# =======================================================================


# =======================================================================
# LOGGING SETTINGS
# https://docs.djangoproject.com/en/1.11/topics/logging
# =======================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(dirname(SETTINGS_DIR), 'logs', 'idea_pool.log'),
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}
