# API Testing Guide - User System

## Environment Setup

```bash
cd /home/tun/.openclaw/workspace/gold-trader-poc/backend
source .venv/bin/activate
python manage.py runserver
```

## API Endpoints

### 1. Register User

**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "phone_number": "0812345678",
  "date_of_birth": "1990-01-01"
}
```

**Response (201 Created):**
```json
{
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "",
    "last_name": ""
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

---

### 2. Login

**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "email": "test@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "",
    "last_name": ""
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

---

### 3. Get Profile

**Endpoint:** `GET /api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "",
  "last_name": "",
  "phone_number": "0812345678",
  "date_of_birth": "1990-01-01",
  "balance": "0.00",
  "is_verified": false,
  "created_at": "2026-02-04T07:24:00Z",
  "updated_at": "2026-02-04T07:24:00Z"
}
```

---

### 4. Update Profile

**Endpoint:** `PATCH /api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "Test",
  "last_name": "User",
  "phone_number": "0898765432"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "phone_number": "0898765432",
  "date_of_birth": "1990-01-01",
  "balance": "0.00",
  "is_verified": false,
  "created_at": "2026-02-04T07:24:00Z",
  "updated_at": "2026-02-04T07:30:00Z"
}
```

---

### 5. Refresh Token

**Endpoint:** `POST /api/auth/token/refresh/`

**Request Body:**
```json
{
  "refresh": "<refresh_token>"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 6. Logout

**Endpoint:** `POST /api/auth/logout/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh": "<refresh_token>"
}
```

**Response (200 OK):**
```json
{
  "message": "Logout successful"
}
```

---

## cURL Examples

### Register:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'
```

### Login:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### Get Profile:
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## Error Responses

### 400 Bad Request - Validation Error
```json
{
  "password": ["Password fields didn't match."]
}
```

### 401 Unauthorized - Invalid Credentials
```json
{
  "error": "Invalid email or password"
}
```

### 401 Unauthorized - No Token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden - Invalid Token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid"
}
```

---

## Notes

- Access tokens expire in **1 hour**
- Refresh tokens expire in **7 days**
- Always store refresh tokens securely
- Use HTTPS in production
- Implement rate limiting in production
