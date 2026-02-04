# Gold Trader Backend API

Backend REST API for Gold Trader Application built with Django REST Framework.

## Features

- ✅ Custom User Model with balance tracking
- ✅ JWT Authentication (access & refresh tokens)
- ✅ Token Blacklist for secure logout
- ✅ User Registration & Login
- ✅ User Profile Management
- ✅ Gold Price Tracking (models ready)
- ✅ Transaction Management (models ready)
- ✅ PostgreSQL Database
- ✅ CORS Enabled for Frontend Integration

## Tech Stack

- Django 5.2+
- Django REST Framework 3.14+
- Django REST Framework Simple JWT 5.3+
- PostgreSQL
- Python 3.12+

## Installation

### 1. Clone & Navigate
```bash
cd gold-trader-poc/backend
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Update `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=gold_trader
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### 5. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

API will be available at: `http://localhost:8000`

## API Documentation

See `API_GUIDE.md` for detailed API documentation including:

- Endpoint descriptions
- Request/response examples
- cURL examples
- Error handling

Quick Overview:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register new user |
| `/api/auth/login/` | POST | Login user |
| `/api/auth/logout/` | POST | Logout user |
| `/api/auth/token/refresh/` | POST | Refresh access token |
| `/api/auth/profile/` | GET | Get user profile |
| `/api/auth/profile/` | PATCH | Update user profile |
| `/api/auth/me/` | GET | Get current user |

## Project Structure

```
backend/
├── gold_trader/          # Project configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI config
├── core/                 # Core application
│   ├── models.py         # User, Transaction, GoldPrice, Wallet models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # API views
│   ├── urls.py           # App URL configuration
│   └── migrations/       # Database migrations
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── API_GUIDE.md          # API documentation
```

## Models

### User
- Extended Django AbstractUser
- Fields: email (unique), phone_number, date_of_birth, is_verified, balance
- Custom user manager
- Email as username

### Transaction
- Buy/Sell transactions
- Fields: user, transaction_type, gold_weight, gold_price_per_gram, total_amount, status
- Status: PENDING, COMPLETED, CANCELLED

### GoldPrice
- Historical gold prices
- Fields: price_per_gram, price_per_baht, currency, timestamp, source

### Wallet
- User wallet balance
- Fields: user, balance (cash), gold_holdings

## Authentication

- JWT-based authentication
- Access token lifetime: 1 hour
- Refresh token lifetime: 7 days
- Token rotation enabled
- Token blacklist after rotation

### Using JWT Tokens

Include in Authorization header:
```
Authorization: Bearer <access_token>
```

## Development

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Tests
```bash
python manage.py test
```

### Check for Issues
```bash
python manage.py check
```

## Production Deployment

### Security Checklist
- [ ] Set `DEBUG = False`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS
- [ ] Set secure database password
- [ ] Configure CORS properly
- [ ] Use environment variables
- [ ] Run `python manage.py collectstatic`

### Gunicorn (Production Server)
```bash
gunicorn gold_trader.wsgi:application --bind 0.0.0.0:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "gold_trader.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | `True` |
| `DB_NAME` | Database name | `gold_trader` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | Required |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:5173` |

## Frontend Integration

CORS is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://127.0.0.1:5173`

Include JWT token in API requests:
```javascript
const response = await fetch('http://localhost:8000/api/auth/profile/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
});
```

## Troubleshooting

### Database Connection Error
```
FATAL: password authentication failed
```
Check `.env` file for correct database credentials.

### Migration Issues
```bash
python manage.py migrate --fake-initial
```

### CORS Errors
Verify `CORS_ALLOWED_ORIGINS` in `.env` matches your frontend URL.

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.
