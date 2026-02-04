# Gold Trader Backend - Setup Guide

## Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Redis (for Django Channels)
- Node.js (for frontend)

## Installation

### 1. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or using uv (faster):
```bash
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` file with your configuration:
- Set `DB_PASSWORD` to your PostgreSQL password
- Update `SECRET_KEY` with a secure random string
- Configure other settings as needed

### 4. Setup PostgreSQL Database

#### Create Database (requires PostgreSQL running)

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE gold_trader;
CREATE USER gold_trader WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gold_trader TO gold_trader;
\q
```

#### Or if using postgres user:

```bash
createdb gold_trader
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`
Admin panel: `http://localhost:8000/admin/`

## API Endpoints

### Authentication
- `POST /api/auth/token/` - Obtain JWT token
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Users
- `GET /api/users/` - List users
- `POST /api/users/` - Register new user
- `GET /api/users/me/` - Get current user profile
- `GET /api/users/{id}/` - Get user details

### Gold Prices
- `GET /api/gold-prices/` - List gold prices
- `GET /api/gold-prices/latest/` - Get latest gold price

### Transactions
- `GET /api/transactions/` - List user transactions
- `POST /api/transactions/` - Create new transaction
- `GET /api/transactions/{id}/` - Get transaction details

### Wallets
- `GET /api/wallets/` - List wallets
- `GET /api/wallets/my_wallet/` - Get current user's wallet

## Running with Django Channels (WebSocket)

For production with WebSocket support, you need:

1. Redis server running:
```bash
redis-server
```

2. Run Daphne (ASGI server):
```bash
daphne gold_trader.asgi:application -b 0.0.0.0 -p 8000
```

Or use Gunicorn with worker class:
```bash
gunicorn gold_trader.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## Project Structure

```
backend/
├── gold_trader/           # Project settings
│   ├── asgi.py           # ASGI config (for Channels)
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI config
├── core/                 # Main application
│   ├── admin.py          # Admin configuration
│   ├── apps.py           # App configuration
│   ├── consumers.py      # WebSocket consumers
│   ├── models.py         # Database models
│   ├── routing.py        # WebSocket routing
│   ├── serializers.py    # DRF serializers
│   ├── urls.py           # App URL routing
│   └── views.py          # API views
├── .env.example          # Environment variables template
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Common Commands

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Start shell
python manage.py shell

# Database operations
python manage.py dbshell
```

## Troubleshooting

### PostgreSQL Connection Issues
- Ensure PostgreSQL is running: `sudo systemctl status postgresql`
- Check credentials in `.env` file
- Verify database exists: `psql -U postgres -l`

### Redis Connection Issues
- Ensure Redis is running: `redis-cli ping` (should return PONG)
- Check Redis settings in `settings.py`

### Module Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use strong database passwords
- Configure CORS properly for production
- Enable HTTPS in production
