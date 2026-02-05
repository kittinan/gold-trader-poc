# Settings package for Gold Trader
# Default to dev settings if DJANGO_SETTINGS_MODULE is not explicitly set
# Use: DJANGO_SETTINGS_MODULE=gold_trader.settings.prod python manage.py runserver

import os

# If this file is imported directly (as gold_trader.settings), use dev by default
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'gold_trader.settings':
    from .dev import *  # noqa: F401, F403
else:
    # Allow importing base for extension
    pass
