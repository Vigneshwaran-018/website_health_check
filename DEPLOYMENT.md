# Deployment Guide

Complete step-by-step instructions for deploying the Health Check Dashboard.

## Table of Contents

1. [Backend Deployment](#backend-deployment)
2. [Frontend Deployment](#frontend-deployment)
3. [Full Stack Deployment](#full-stack-deployment)
4. [Post-Deployment](#post-deployment)

---

## Backend Deployment

### Option 1: Render.com (Recommended)

**Advantages:** Free tier available, easy integration, auto-deploys on git push

#### Steps:

1. **Prepare Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/health-check-dashboard.git
   git push -u origin main
   ```

2. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Configure:
     - **Name**: `health-check-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r backend/requirements.txt`
     - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
     - **Region**: Choose closest to users

4. **Set Environment Variables**
   - Go to Environment
   - Add variables:
     ```
     ENV=production
     FRONTEND_URL=https://your-frontend-url.vercel.app
     ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment (2-5 minutes)
   - Note the service URL (e.g., `https://health-check-api.onrender.com`)

### Option 2: Railway.app

**Advantages:** Good free tier, simple dashboard

#### Steps:

1. **Create Railway Account**
   - Go to https://railway.app
   - Connect GitHub

2. **Create Project**
   - New Project → Import from GitHub
   - Select repository

3. **Add Python Service**
   - Add Service → GitHub Repo
   - Select backend directory (or root with backend folder)

4. **Configure**
   - Variables:
     ```
     ENV=production
     FRONTEND_URL=https://your-frontend-url
     ```
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Deploy**
   - Auto-deploys on push
   - Get API URL from deployment logs

### Option 3: Self-Hosted (VPS)

#### Prerequisites:
- Linux server (Ubuntu 20.04+)
- SSH access
- Domain name (optional but recommended)

#### Steps:

1. **Connect to Server**
   ```bash
   ssh root@your-server-ip
   ```

2. **Install Dependencies**
   ```bash
   apt update && apt upgrade -y
   apt install python3 python3-pip python3-venv nginx supervisor -y
   ```

3. **Clone Repository**
   ```bash
   cd /var/www
   git clone https://github.com/yourusername/health-check-dashboard.git
   cd health-check-dashboard/backend
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/health-check.service
   ```

   Add:
   ```ini
   [Unit]
   Description=Health Check Dashboard API
   After=network.target

   [Service]
   Type=notify
   User=www-data
   WorkingDirectory=/var/www/health-check-dashboard/backend
   Environment="PATH=/var/www/health-check-dashboard/backend/venv/bin"
   ExecStart=/var/www/health-check-dashboard/backend/venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

6. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable health-check
   sudo systemctl start health-check
   ```

7. **Configure Nginx Reverse Proxy**
   ```bash
   sudo nano /etc/nginx/sites-available/health-check
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name api.yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/health-check /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **SSL Certificate (Let's Encrypt)**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d api.yourdomain.com
   ```

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

**Advantages:** Optimized for React/Vite, free tier, auto-deploys

#### Steps:

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Configure Environment**
   - Follow prompts
   - Link to GitHub repo
   - When asked about settings, press Enter to use defaults

4. **Add Environment Variable**
   - Go to Project Settings → Environment Variables
   - Add `VITE_API_URL` with value of your backend API URL
   - Redeploy

5. **Get URL**
   - Dashboard shows deployment URL
   - Frontend is live!

### Option 2: Netlify

**Advantages:** Good free tier, simple deployment

#### Steps:

1. **Push to GitHub**
   ```bash
   git push origin main
   ```

2. **Connect to Netlify**
   - Go to https://netlify.com
   - Click "Add new site" → "Import an existing project"
   - Select GitHub repository

3. **Configure Build**
   - Build command: `npm run build` (in frontend folder)
   - Publish directory: `frontend/dist`

4. **Set Environment Variable**
   - Site settings → Build & deploy → Environment
   - Add `VITE_API_URL=https://your-backend-url`

5. **Deploy**
   - Automatic deployment on push

### Option 3: Self-Hosted

#### Steps:

1. **Build Project**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Upload to Server**
   ```bash
   scp -r dist/* root@your-server-ip:/var/www/health-check
   ```

3. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/health-check-frontend
   ```

   Add:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       root /var/www/health-check;

       location / {
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass https://your-backend-api.com;
       }
   }
   ```

4. **Enable and Test**
   ```bash
   sudo ln -s /etc/nginx/sites-available/health-check-frontend /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

## Full Stack Deployment

### Docker Compose on VPS

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker $USER
   ```

2. **Create docker-compose.yml**
   ```yaml
   version: '3.8'

   services:
     backend:
       build:
         context: .
         dockerfile: backend/Dockerfile
       environment:
         ENV: production
         PORT: 8000
         FRONTEND_URL: https://yourdomain.com
       ports:
         - "8000:8000"
       restart: unless-stopped

     frontend:
       build:
         context: .
         dockerfile: frontend/Dockerfile
         args:
           VITE_API_URL: https://api.yourdomain.com
       ports:
         - "3000:80"
       depends_on:
         - backend
       restart: unless-stopped
   ```

3. **Deploy**
   ```bash
   docker-compose up -d
   ```

---

## Post-Deployment

### Verify Deployment

1. **Check Backend**
   ```bash
   curl https://your-backend-url/health
   ```
   Should return: `{"status": "healthy", "service": "Health Check Dashboard API"}`

2. **Check Frontend**
   - Open `https://your-frontend-url` in browser
   - Test with a scan

3. **Test Full Flow**
   - Enter URL in dashboard
   - Verify scan completes successfully

### Monitor

**Render:**
- Dashboard → Logs tab

**Railway:**
- Service → Logs

**Self-hosted:**
```bash
# Backend
journalctl -u health-check -f

# Nginx
sudo tail -f /var/log/nginx/access.log
```

### Scaling & Rate Limiting

**Add Rate Limiting (Backend)**

In `backend/main.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/scan")
@limiter.limit("10/minute")
async def scan_website(request: Request, url: str = Query(...)):
    # ... rest of endpoint
```

### SSL/HTTPS

**Render & Vercel:** Automatic SSL

**Self-hosted:**
```bash
# Using Let's Encrypt
sudo certbot --nginx -d yourdomain.com
# Auto-renews every 90 days
```

### Backups & Monitoring

- No database, so minimal backup needs
- Monitor error logs
- Set up alerts for downtime

---

## Troubleshooting Deployment

### Frontend shows "Cannot reach API"

**Solution:**
1. Verify `VITE_API_URL` environment variable
2. Check backend is deployed and responding
3. Verify CORS is configured in backend
4. Check browser console for exact error

### Backend returning 502/503

**Solution:**
1. Check service is running: `systemctl status health-check`
2. Check logs for errors
3. Verify port is not in use
4. Restart service: `systemctl restart health-check`

### Slow scans after deployment

**Solution:**
1. Normal (scans take 10-30 seconds)
2. If consistently slow, check server resources
3. Consider adding caching layer (Redis)

### Certificate errors

**Solution:**
1. Let's Encrypt auto-renewal: `sudo certbot renew`
2. Verify domain points to server
3. Check certificate expiry: `sudo certbot certificates`

---

## Maintenance Checklist

- [ ] SSL certificates auto-renewing
- [ ] Error logs monitored
- [ ] Backend and frontend URLs in sync
- [ ] Rate limiting enabled (production)
- [ ] CORS origins correct
- [ ] Environment variables set correctly
- [ ] Database backups (if added)
- [ ] Performance monitoring active

---

## Next Steps

1. Set up custom domain with DNS
2. Configure email alerts
3. Add uptime monitoring
4. Document your deployment
5. Create runbooks for common issues

For questions, refer to platform-specific documentation or contact support.
