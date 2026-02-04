# Gold Trader - Docker Setup Guide

##  Overview

This guide explains how to set up and run the Gold Trader application using Docker. The Docker setup includes:

- **Frontend**: React + Vite application (served via Nginx)
- **Backend**: Django + Django REST Framework application
- **Database**: PostgreSQL
- **Cache**: Redis (for Django Channels/WebSockets)

## Quick Start

### Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)

### Environment Setup

1. Copy the environment file:
   ```bash
   cp .env.example.docker .env
   ```

2. Edit the `.env` file if needed (default values should work for development)

### Development Mode

For development with hot-reloading:

```bash
# Build and start all services in development mode
docker-compose -f docker-compose.dev.yml up --build

# Or run in detached mode
docker-compose -f docker-compose.dev.yml up -d --build
```

Access the applications:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/
- **Backend Admin**: http://localhost:8000/admin/

### Production Mode

For production-like environment:

```bash
# Build and start all services in production mode
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

Access the applications:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Backend Admin**: http://localhost:8000/admin/

## Service Details

### Frontend (Development)
- **Port**: 5173
- **Technology**: Vite + React + TypeScript + Tailwind CSS
- **Features**: Hot-reloading, development server
- **Dockerfile**: `frontend/Dockerfile.dev`

### Frontend (Production)
- **Port**: 3000
- **Technology**: Nginx serving built React app
- **Features**: Optimized for production, gzip compression, SPA routing
- **Dockerfile**: `frontend/Dockerfile`

### Backend (Development)
- **Port**: 8000
- **Technology**: Django development server
- **Features**: Auto-reload on code changes, debug mode
- **Dockerfile**: `backend/Dockerfile.dev`

### Backend (Production)
- **Port**: 8000
- **Technology**: Gunicorn + Uvicorn workers
- **Features**: Multiple workers, production-ready
- **Dockerfile**: `backend/Dockerfile`

### PostgreSQL
- **Port**: 5432
- **Database**: `gold_trader`
- **User**: `postgres`
- **Password**: `postgres_password` (change in production)
- **Data**: Persisted in Docker volume

### Redis
- **Port**: 6379
- **Purpose**: Django Channels, session storage, caching
- **Data**: Persisted in Docker volume with AOF enabled

## Common Commands

### Building Images

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend
```

### Starting/Stopping Services

```bash
# Start all services
docker-compose up

# Start all services in detached mode
docker-compose up -d

# Stop all services
docker-compose down

# Stop services and remove volumes
docker-compose down -v

# Restart specific service
docker-compose restart backend
```

### Viewing Logs

```bash
# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs backend
docker-compose logs postgres

# Follow logs in real-time
docker-compose logs -f backend
```

### Running Commands in Containers

```bash
# Access backend container shell
docker-compose exec backend bash

# Run Django management commands
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser

# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d gold_trader

# Access Redis CLI
docker-compose exec redis redis-cli
```

## Environment Variables

### Backend Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Django debug mode | `True` |
| `SECRET_KEY` | Django secret key | `django-insecure-dev-secret-key` |
| `DB_NAME` | PostgreSQL database name | `gold_trader` |
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `postgres_password` |
| `DB_HOST` | PostgreSQL host | `postgres` |
| `DB_PORT` | PostgreSQL port | `5432` |
| `REDIS_HOST` | Redis host | `redis` |
| `REDIS_PORT` | Redis port | `6379` |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:3000` |

### Frontend Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `http://localhost:8000/api` |

## Production Deployment

### Security Considerations

1. **Change Default Secrets**: Update `SECRET_KEY` and database passwords
2. **Disable Debug**: Set `DEBUG=False` in production
3. **Use HTTPS**: Configure SSL certificates
4. **Database Security**: Use strong passwords and restrict access
5. **Environment Variables**: Use secure methods to manage secrets

### Scaling

To scale services:

```bash
# Scale backend to 3 instances
docker-compose up -d --scale backend=3

# Scale frontend to 2 instances (behind load balancer)
docker-compose up -d --scale frontend=2
```

### Volume Management

Data is persisted in Docker volumes:
- `postgres_data`: PostgreSQL data
- `redis_data`: Redis data
- `backend_media`: Django media files
- `backend_static`: Django static files

## Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 3000, 5432, 6379, and 8000 are available
2. **Database Connection**: Check PostgreSQL is running and credentials are correct
3. **Redis Connection**: Verify Redis container is healthy
4. **Permission Issues**: Ensure proper file permissions in mounted volumes

### Health Checks

Both PostgreSQL and Redis containers include health checks:

```bash
# Check container health
docker-compose ps

# Check specific container
docker inspect gold-trader-postgres
```

### Rebuilding

If you make changes to Dockerfiles or dependencies:

```bash
# Force rebuild without cache
docker-compose build --no-cache

# Rebuild and restart
docker-compose up -d --build
```

## Development Workflow

### Making Changes

1. **Frontend Changes**: Code changes are automatically reflected due to hot-reloading
2. **Backend Changes**: Django dev server automatically reloads on code changes
3. **Database Changes**: Use Django migrations:
   ```bash
   docker-compose exec backend python manage.py makemigrations
   docker-compose exec backend python manage.py migrate
   ```

### Testing

```bash
# Run backend tests
docker-compose exec backend python manage.py test

# Access test database
docker-compose exec backend python manage.py dbshell
```

### Database Management

```bash
# Create database backup
docker-compose exec postgres pg_dump -U postgres gold_trader > backup.sql

# Restore database
docker-compose exec -i postgres psql -U postgres gold_trader < backup.sql

# Access database directly
docker-compose exec postgres psql -U postgres -d gold_trader
```

## Support

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Ensure all prerequisites are installed
4. Check port availability
5. Review environment variable configuration

---

*Last updated: February 4, 2026*