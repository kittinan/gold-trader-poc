"""
Development settings for Gold Trader project.
Use with: DJANGO_SETTINGS_MODULE=gold_trader.settings.dev python manage.py runserver
"""

from .base import *  # noqa: F401, F403

import sys
from decouple import config, Csv


# =============================================================================
# Debug Mode
# =============================================================================
DEBUG = True

# Security warning: don't use this key in production!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-+mg3=j-tn3%!s^s^$y4ynxg^fg$r+lxm#cvv)r@u0v2exn^397')


# =============================================================================
# Allowed Hosts
# =============================================================================
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,backend,frontend', cast=Csv())


# =============================================================================
# Database Configuration
# =============================================================================
# Use SQLite for testing, PostgreSQL for dev
if 'test' in sys.argv or 'pytest' in sys.modules:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='gold_trader'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='postgres_password'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }


# =============================================================================
# Redis / Channels Configuration
# =============================================================================
if 'test' in sys.argv or 'pytest' in sys.modules:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [
                    (
                        config('REDIS_HOST', default='127.0.0.1'),
                        config('REDIS_PORT', default=6379, cast=int)
                    )
                ],
            },
        },
    }


# =============================================================================
# CORS Configuration (Development)
# =============================================================================
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!


# =============================================================================
# Email Configuration (Console backend for dev)
# =============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# =============================================================================
# Logging Configuration (Verbose for dev)
# =============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'gold_trader': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


# =============================================================================
# Debug Toolbar (optional, uncomment if installed)
# =============================================================================
# if 'debug_toolbar' in INSTALLED_APPS:
#     MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
#     INTERNAL_IPS = ['127.0.0.1', 'localhost']
