from .common import *

# =======================================================================
# SECURITY SETTINGS
# =======================================================================
SECRET_KEY = 'z-c0r=jq#%kx3myqw6%qh_126x*vi#8^clm-r6=6-4wy+$03%s'
JWT_SECRET = 'secret'
DEBUG = True

# List of hosts allowed to access the app
ALLOWED_HOSTS = ['localhost', '127.0.0.1',]
CORS_ORIGIN_WHITELIST = (
    # API origins
    'localhost:8000',
    '127.0.0.1:8000',
    # Client origins
    'localhost:8080',
    '127.0.0.1:8080',
)
CORS_ALLOW_METHODS = (
        'GET',
        'POST',
        'PUT',
        'PATCH',
        'DELETE',
        'OPTIONS'
    )
# =======================================================================
# APPLICATIONS
# On application start-up, Django looks for migrations files for each app
# =======================================================================
DJANGO_APPS += [
    # Not likely to need anything here. New apps should be added in common.py
]

EXTERNAL_APPS += [
    # Dev Tools: Any tools needed only for development purposes
    'corsheaders',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS

MIDDLEWARE += [
    # Dev middlewares ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# =======================================================================
# MEDIA MANAGEMENT
# Static files and template management
# https://docs.djangoproject.com/en/1.11/howto/static-files/
# =======================================================================
TEMPLATES += [
   # Dev settings here
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATICFILES_DIRS += [
    os.path.join(APP_ROOT, "static"),
]

# =======================================================================
# DATABASE SETTINGS
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# =======================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'idea_pool_dev',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'xotomajor',
        'PASSWORD': 'admin',
    },
    'test': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'idea_pool_test',
        'HOST': 'localhost',
        'PORT': '5432',
        'PASSWORD': '',
    },
}

# =======================================================================
# AUTHENTICATION
# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
# =======================================================================
AUTH_PASSWORD_VALIDATORS += [
    # Custom auth for local testing
]

# =======================================================================
# THIRD-PARTY INTEGRATION SETTINGS
# For settings specific to third-party modules and apis.
# The credentials below are NOT FOR PRODUCTION. Overwrite them by editing
# your dev.py
# =======================================================================
JWT_EXP_DELTA = datetime.timedelta(seconds=600)
JWT_ALGORITHM = 'HS256'
JWT_REFRESH_EXP_DELTA = datetime.timedelta(days=7)

JWT_AUTH = {
    'JWT_SECRET_KEY': SECRET_KEY,
    'JWT_ALLOW_REFRESH': True,
    'JWT_AUTH_HEADER_PREFIX': 'JWT',

    'JWT_ENCODE_HANDLER': 'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER': 'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

    'JWT_RESPONSE_PAYLOAD_HANDLER': 'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_GET_USER_SECRET_KEY': None,
    'JWT_PUBLIC_KEY': None,
    'JWT_PRIVATE_KEY': None,
    'JWT_ALGORITHM': 'HS256',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LEEWAY': 0,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=6000),
    'JWT_AUDIENCE': None,
    'JWT_ISSUER': None,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_COOKIE': None,
}

# =======================================================================
# LOGGING SETTINGS
# =======================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'root': {
    #     'level': 'WARNING',
    #     'handlers': ['console'],
    # },
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        # Print logs to file
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(dirname(APP_ROOT), 'logs', 'debug.log'),
            'formatter': 'standard',
        },
        # Print logs to console
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
