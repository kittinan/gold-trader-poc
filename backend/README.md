# Backend API Server

Gold Trader Backend API Server - Django REST Framework + Django Channels

## Technology Stack
- Django 5.2+ (Web Framework)
- Django REST Framework (API)
- Django Channels (WebSocket support)
- PostgreSQL (Database)
- Redis (WebSocket message broker)
- JWT Authentication (SimpleJWT)
- Gunicorn/Daphne (Production servers)

## Features
- ✅ RESTful API architecture
- ✅ JWT Authentication
- ✅ WebSocket support for real-time updates
- ✅ User management with custom User model
- ✅ Gold price tracking
- ✅ Transaction management
- ✅ Wallet system
- ✅ CORS support for frontend integration
- ✅ Admin panel for content management

## Quick Start

See [SETUP.md](SETUP.md) for detailed installation instructions.

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## API Base URL
- Development: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`

## Current Structure
```
backend/
├── gold_trader/       # Django project configuration
│   ├── __init__.py
│   ├── settings.py    # Django settings (with DRF & Channels)
│   ├── urls.py        # Main URL routing
│   ├── asgi.py        # ASGI config (WebSocket support)
│   └── wsgi.py        # WSGI config
├── core/              # Main application
│   ├── admin.py       # Admin configuration
│   ├── apps.py
│   ├── consumers.py   # WebSocket consumers
│   ├── models.py      # Database models
│   ├── routing.py     # WebSocket routing
│   ├── serializers.py # DRF serializers
│   ├── urls.py        # API URL routing
│   └── views.py       # API viewsets
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
├── SETUP.md           # Detailed setup guide
└── manage.py          # Django management script
```

## Main Models
- **User**: Extended user model with email authentication
- **GoldPrice**: Historical gold price tracking
- **Transaction**: Buy/sell transactions
- **Wallet**: User wallet with cash balance and gold holdings

## API Endpoints
- `/api/auth/token/` - JWT token authentication
- `/api/users/` - User management
- `/api/gold-prices/` - Gold price data
- `/api/transactions/` - Transaction management
- `/api/wallets/` - Wallet information

## Development Status
✅ Milestone 1 Complete:
- Django project setup
- Core models created
- DRF ViewSets configured
- JWT authentication
- Basic WebSocket consumers
- Admin panel configured

See [SETUP.md](SETUP.md) for complete documentation.