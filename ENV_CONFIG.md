# Environment Configuration Guide

This document explains how to configure environment variables for the Health Check Dashboard.

## Backend Configuration

Create a `.env` file in the `backend/` directory:

```env
# Server Configuration
PORT=8000
ENV=development

# CORS Configuration
FRONTEND_URL=http://localhost:5173

# Optional: Production API URL
# FRONTEND_URL=https://yourdomain.com
```

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Server port |
| `ENV` | `development` | Environment (development/production) |
| `FRONTEND_URL` | Optional | Additional CORS origin for frontend |

### Usage

**Development:**
```bash
python main.py
```

**Production:**
```bash
ENV=production PORT=8000 uvicorn main:app --host 0.0.0.0
```

## Frontend Configuration

Create a `.env.local` file in the `frontend/` directory:

```env
# API Configuration
VITE_API_URL=http://localhost:8000
```

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://localhost:8000` | Backend API URL |

### Usage Examples

**Local Development:**
```env
VITE_API_URL=http://localhost:8000
```

**Development Backend (Different Machine):**
```env
VITE_API_URL=http://192.168.1.100:8000
```

**Production:**
```env
VITE_API_URL=https://api.yourdomain.com
```

**Render/Railway Deployment:**
```env
VITE_API_URL=https://your-backend-service.onrender.com
```

## Deployment Configurations

### Local Full Stack

**Backend `.env`:**
```env
PORT=8000
ENV=development
FRONTEND_URL=http://localhost:5173
```

**Frontend `.env.local`:**
```env
VITE_API_URL=http://localhost:8000
```

### Render + Vercel

**Backend (Render) `.env`:**
```env
PORT=8000
ENV=production
FRONTEND_URL=https://your-frontend.vercel.app
```

**Frontend (Vercel) Environment Variable:**
```
VITE_API_URL=https://your-backend.onrender.com
```

### Railway + Netlify

**Backend (Railway) `.env`:**
```env
PORT=8000
ENV=production
FRONTEND_URL=https://your-frontend.netlify.app
```

**Frontend (Netlify) Environment Variable:**
```
VITE_API_URL=https://your-backend-railway-url.up.railway.app
```

### Self-hosted (Docker Compose)

**Backend `backend/.env`:**
```env
PORT=8000
ENV=production
FRONTEND_URL=https://yourdomain.com
```

**Frontend `frontend/.env.local`:**
```env
VITE_API_URL=https://api.yourdomain.com
```

## Docker Deployment

### Using Docker Compose

Create `docker-compose.yml` in project root:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    environment:
      PORT: 8000
      ENV: production
      FRONTEND_URL: http://localhost:3000
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      args:
        VITE_API_URL: http://localhost:8000
    ports:
      - "3000:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Run with:
```bash
docker-compose up
```

## CI/CD Configuration

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          # Deploy to Render/Railway
          echo "Deploying backend..."
      
      - name: Deploy Frontend
        env:
          VITE_API_URL: https://api.yourdomain.com
        run: |
          cd frontend
          npm install
          npm run build
          # Deploy to Vercel/Netlify
          echo "Deploying frontend..."
```

## Security Best Practices

1. **Never commit `.env` files to git**
   - Add `*.env*` to `.gitignore`
   - Use platform-specific secret management

2. **Use environment-specific URLs**
   - Development: `http://localhost:*`
   - Production: HTTPS only

3. **Rotate secrets regularly**
   - Update API URLs when changing deployment platforms
   - Use API keys where applicable

4. **Validate environment variables**
   - Check configuration before deployment
   - Verify CORS origins match frontend URL

## Troubleshooting

### Backend Cannot Connect to Frontend

**Error**: CORS error in browser console

**Solution:**
1. Verify `FRONTEND_URL` in backend `.env`
2. Ensure frontend is running at that URL
3. Check browser console for exact URL

### Frontend Cannot Connect to Backend

**Error**: "Network Error" or "Cannot reach API"

**Solution:**
1. Verify `VITE_API_URL` in `.env.local`
2. Check backend is running at that URL
3. Test: `curl http://your-backend-url/health`

### Environment Variables Not Applied

**Solution:**
1. Restart development server after changing `.env`
2. For Docker: rebuild image with `--no-cache`
3. Clear environment cache: `npm cache clean --force`

## .gitignore Configuration

Add to project `.gitignore`:

```
# Environment variables
.env
.env.local
.env.*.local
.env.production

# Backend
backend/.env

# Frontend
frontend/.env.local
frontend/.env.*.local
```

## Platform-Specific Guides

### Vercel Environment Variables

1. Go to Project Settings → Environment Variables
2. Add variable: `VITE_API_URL`
3. Set value: `https://your-api.com`
4. Apply to all environments or specific ones
5. Redeploy

### Render Environment Variables

1. Go to Environment → Environment Variables
2. Add key: `FRONTEND_URL`
3. Add value: `https://your-frontend.com`
4. Redeploy

### Railway Environment Variables

1. Go to Service → Variables
2. Add raw environment variables
3. Deploy

## Support

For environment-related issues, check:
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- Main: `README.md`
