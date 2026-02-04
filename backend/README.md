# Backend API Server

Gold Trader Backend API Server

## Technology Stack
- Django REST Framework
- Django Channels (WebSocket)
- PostgreSQL
- Redis (Cache/Message Broker)
- JWT Authentication

## Development
This directory contains the Django backend API server for the Gold Trading platform.

Key responsibilities:
- API Development
- Database Management
- Real-time Trading Logic
- Authentication & Security
- Business Logic Implementation

## Structure
```
backend/
├── gold_trader/       # Django project
│   ├── __init__.py
│   ├── settings.py    # Django settings
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI application
├── apps/              # Django apps
│   ├── users/         # User management
│   ├── trading/       # Trading logic
│   ├── goldholdings/  # Gold holdings
│   └── deposits/      # Deposit system
├── requirements.txt   # Python dependencies
└── manage.py          # Django management script
```