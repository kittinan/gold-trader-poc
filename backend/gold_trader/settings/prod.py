"""
Production settings for Gold Trader project.
Use with: DJANGO_SETTINGS_MODULE=gold_trader.settings.prod python manage.py runserver
IMPORTANT: All sensitive values must come from environment variables.
"""

from .base import *  # noqa: F401, F403

from decouple import config, Csv


# =============================================================================
# Debug Mode
# =============================================================================
DEBUG = False

# SECRET_KEY must be set in environment!
SECRET_KEY = config('SECRET_KEY')

# ALLOWED_HOSTS must be set in environment!
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# =============================================================================
# Database Configuration
# =============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'CONN_MAX_AGE': 600,  # Persistent connections
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}


# =============================================================================
# Redis / Channels Configuration
# =============================================================================
REDIS_PASSWORD = config('REDIS_PASSWORD', default='')
redis_hosts = f"{config('REDIS_HOST')}:{config('REDIS_PORT')}"
if REDIS_PASSWORD:
    redis_hosts = f":{REDIS_PASSWORD}@{redis_hosts}"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [redis_hosts],
        },
    },
}


# =============================================================================
# CORS Configuration (Production - strict)
# =============================================================================
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())


# =============================================================================
# Security Settings
# =============================================================================
# SSL Redirect (uncomment if SSL is enabled)
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Cookie Security (uncomment if SSL is enabled)
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# HSTS (uncomment if SSL is enabled)
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Other Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# =============================================================================
# Email Configuration
# =============================================================================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@goldtrader.com')


# =============================================================================
# Logging Configuration
# =============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/app/logs/django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gold_trader': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# =============================================================================
# Static Files (Whitenoise for serving)
# =============================================================================
# In production, static files are served by nginx
# This is fallback if nginx is not configured correctly
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# =============================================================================
# Session Configuration
# =============================================================================
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week


# =============================================================================
# Performance Settings
# =============================================================================
CONN_MAX_AGE = 600  # Reuse database connections
