# Phase 4: Production Ready 🏭

## เป้าหมาย
ทำให้ Gold Trader POC พร้อม deploy ขึ้น production ได้จริง

---

## 📋 Task Breakdown

### Task 1: Docker Setup (คุณฐาน - Backend)

| ไฟล์ | รายละเอียด |
|------|------------|
| `backend/Dockerfile` | Multi-stage build สำหรับ Django |
| `backend/.dockerignore` | Exclude venv, __pycache__, etc. |
| `.env.example` | Template สำหรับ environment variables |

**Dockerfile features:**
- Python 3.12 slim base
- Poetry/pip for dependencies
- Gunicorn as WSGI server
- Non-root user for security

---

### Task 2: Docker Setup (คุณอาร์ต - Frontend)

| ไฟล์ | รายละเอียด |
|------|------------|
| `frontend/Dockerfile` | Multi-stage build (build + nginx serve) |
| `frontend/.dockerignore` | Exclude node_modules, dist, etc. |
| `frontend/nginx.conf` | Nginx config สำหรับ SPA routing |

**Dockerfile features:**
- Node 22 for build stage
- Nginx alpine for serving
- Gzip compression
- SPA fallback routing

---

### Task 3: Docker Compose (คุณฐาน)

| ไฟล์ | รายละเอียด |
|------|------------|
| `docker-compose.yml` | Development environment |
| `docker-compose.prod.yml` | Production environment |

**Services:**
```yaml
services:
  db:        # PostgreSQL
  redis:     # For Channels layer
  backend:   # Django + Gunicorn + Daphne (WebSocket)
  frontend:  # React served by Nginx
  nginx:     # Reverse proxy (prod only)
```

**Development:**
- Hot reload enabled
- Volume mounts for code
- Exposed ports for debugging

**Production:**
- No volume mounts
- Internal network only
- Nginx as single entry point

---

### Task 4: Environment Configs

| Environment | Config |
|-------------|--------|
| `.env.example` | Template with all required vars |
| `backend/gold_trader/settings/base.py` | Shared settings |
| `backend/gold_trader/settings/dev.py` | Development overrides |
| `backend/gold_trader/settings/prod.py` | Production overrides |

**Variables:**
```
# Database
DATABASE_URL=postgres://user:pass@db:5432/gold_trader

# Django
SECRET_KEY=your-secret-key
DEBUG=false
ALLOWED_HOSTS=example.com

# Redis
REDIS_URL=redis://redis:6379/0

# Frontend
VITE_API_URL=https://api.example.com
VITE_WS_URL=wss://api.example.com/ws
```

---

### Task 5: Nginx Reverse Proxy (Prod)

| ไฟล์ | รายละเอียด |
|------|------------|
| `nginx/nginx.conf` | Main nginx config |
| `nginx/conf.d/default.conf` | Server block |

**Routing:**
```
/api/*     → backend:8000
/ws/*      → backend:8000 (WebSocket upgrade)
/admin/*   → backend:8000
/*         → frontend:80
```

**Features:**
- Gzip compression
- Security headers
- WebSocket upgrade handling
- Static file caching

---

### Task 6: E2E Tests in CI

| ไฟล์ | รายละเอียด |
|------|------------|
| `.github/workflows/ci.yml` | อัปเดต e2e-test job |
| `e2e/playwright.config.ts` | อัปเดต baseURL |

**CI Flow:**
1. Build Docker images
2. Start docker-compose (backend + frontend + db)
3. Wait for services ready
4. Run Playwright tests
5. Upload test artifacts
6. Cleanup

---

## ⏰ Timeline

| Task | ผู้รับผิดชอบ | ระยะเวลา |
|------|-------------|----------|
| 1. Backend Dockerfile | คุณฐาน | 30 นาที |
| 2. Frontend Dockerfile | คุณอาร์ต | 30 นาที |
| 3. Docker Compose | คุณฐาน | 45 นาที |
| 4. Environment Configs | คุณฐาน | 30 นาที |
| 5. Nginx Reverse Proxy | คุณฐาน | 30 นาที |
| 6. E2E Tests in CI | คุณละเอียด | 45 นาที |

**รวม: ~3.5 ชั่วโมง** (ทำ parallel ได้)

---

## 🔄 Workflow

```
[คุณอาร์ต]              [คุณฐาน]
     │                      │
     ▼                      ▼
Frontend Dockerfile    Backend Dockerfile
     │                      │
     │                      ▼
     │              Docker Compose (dev)
     │                      │
     └──────────┬───────────┘
                │
                ▼
         Integration Test (local)
                │
                ▼
        Docker Compose (prod)
                │
                ▼
           Nginx Config
                │
                ▼
    [คุณละเอียด] E2E in CI
                │
                ▼
            ✅ Done
```

---

## 📝 Commit Strategy

1. `feat: add Docker setup for backend`
2. `feat: add Docker setup for frontend`
3. `feat: add docker-compose for development`
4. `feat: add production docker-compose with nginx`
5. `feat: add environment configuration`
6. `ci: enable E2E tests with Docker`

**กฎ:** Commit local ก่อน รอ review แล้วค่อย push

---

## ✅ Definition of Done

- [ ] `docker-compose up` ทำงานได้ (dev)
- [ ] `docker-compose -f docker-compose.prod.yml up` ทำงานได้
- [ ] Frontend เข้าถึง Backend ผ่าน Nginx ได้
- [ ] WebSocket ทำงานผ่าน Nginx ได้
- [ ] E2E tests ผ่านใน CI
- [ ] `.env.example` มีครบทุก variables ที่จำเป็น
- [ ] README อัปเดตวิธี run ด้วย Docker

---

ราชา review แผนนี้ก่อนครับ หากอนุมัติจะให้ทีมเริ่มทำงานครับ 🙏
