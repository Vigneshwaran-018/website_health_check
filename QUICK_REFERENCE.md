# ⚡ QUICK COMMAND REFERENCE

Fast reference for common commands in the Health Check Dashboard.

---

## 🚀 GET STARTED (5 minutes)

### Terminal 1: Start Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
python main.py
```
**Result**: Backend at `http://localhost:8000`

### Terminal 2: Start Frontend
```bash
cd frontend
npm install
echo "VITE_API_URL=http://localhost:8000" > .env.local
npm run dev
```
**Result**: Frontend at `http://localhost:5173`

### Terminal 3: Test
```bash
# Open browser
http://localhost:5173

# Enter URL: google.com
# Click Scan
# Wait 10-30 seconds
# See results!
```

---

## 📚 DOCUMENTATION

| Command | Purpose |
|---------|---------|
| `cat QUICKSTART.md` | 5-minute setup |
| `cat README.md` | Project overview |
| `cat DEPLOYMENT.md` | Deploy to production |
| `cat ENV_CONFIG.md` | Environment setup |
| `cat IMPLEMENTATION_GUIDE.md` | How it works |

---

## 🔧 DEVELOPMENT

### Backend
```bash
# Run dev server
cd backend && python main.py

# View API docs
# Open: http://localhost:8000/docs

# Run tests (if added)
pytest

# Check code
pylint backend/main.py
```

### Frontend
```bash
# Dev server
cd frontend && npm run dev

# Build production
npm run build

# Preview build
npm run preview

# Add package
npm install <package-name>

# Lint code
npm run lint
```

---

## 🌐 API ENDPOINTS

### Local Testing
```bash
# Health check
curl http://localhost:8000/health

# Full scan
curl "http://localhost:8000/scan?url=google.com"

# Quick scan
curl "http://localhost:8000/scan/quick?url=google.com"

# API docs
http://localhost:8000/docs
```

### Production Testing
```bash
# Replace localhost with your domain
curl "https://your-api.com/health"
curl "https://your-api.com/scan?url=example.com"
```

---

## 🚀 DEPLOYMENT

### Backend (Render)
```bash
# 1. Create account at render.com
# 2. Create Web Service
# 3. Build: pip install -r backend/requirements.txt
# 4. Start: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
# 5. Environment: FRONTEND_URL=your-frontend-url
# 6. Deploy!
```

### Backend (Railway)
```bash
# 1. Create account at railway.app
# 2. Connect GitHub
# 3. Create service
# 4. Start: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
# 5. Deploy!
```

### Frontend (Vercel)
```bash
# Method 1: CLI
npm install -g vercel
cd frontend
vercel

# Method 2: Dashboard
# 1. Go to vercel.com
# 2. Import GitHub repo
# 3. Set VITE_API_URL env variable
# 4. Deploy!
```

### Frontend (Netlify)
```bash
# 1. Go to netlify.com
# 2. Import from GitHub
# 3. Build: npm run build
# 4. Publish: dist
# 5. Add VITE_API_URL env variable
# 6. Deploy!
```

---

## 📦 ENVIRONMENT SETUP

### Backend (.env)
```bash
# Create file: backend/.env
echo "PORT=8000" >> backend/.env
echo "ENV=development" >> backend/.env
echo "FRONTEND_URL=http://localhost:5173" >> backend/.env
```

### Frontend (.env.local)
```bash
# Create file: frontend/.env.local
echo "VITE_API_URL=http://localhost:8000" > frontend/.env.local
```

### Production Backend (.env)
```bash
PORT=8000
ENV=production
FRONTEND_URL=https://your-frontend.vercel.app
```

### Production Frontend (.env.local)
```bash
VITE_API_URL=https://your-backend.onrender.com
```

---

## 🔍 TROUBLESHOOTING

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Dependencies Missing
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Build Errors
```bash
# Backend
# Check Python version: python --version (need 3.8+)

# Frontend
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

### API Connection Error
```bash
# Check backend is running
curl http://localhost:8000/health

# Check VITE_API_URL
cat frontend/.env.local

# Check CORS
# Should include http://localhost:5173 or your frontend URL
```

---

## 📊 MONITORING

### Check Backend Health
```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy", ...}
```

### View Backend Logs
```bash
# Should show requests in console where python main.py runs
# Look for GET /scan requests
```

### View Frontend Console
```bash
# Open browser DevTools (F12)
# Click Console tab
# Look for network requests to /scan
```

### Performance Check
```bash
# Scan should take 10-30 seconds
# Port scanning is slow (normal!)
# Each port has 1-second timeout
```

---

## 🎯 USEFUL CURL COMMANDS

### Test Backend
```bash
# Health
curl http://localhost:8000/health

# API Info
curl http://localhost:8000/

# Full Scan
curl "http://localhost:8000/scan?url=google.com"

# Quick Scan
curl "http://localhost:8000/scan/quick?url=google.com"

# With Pretty JSON
curl "http://localhost:8000/scan?url=google.com" | jq
```

### Test from Different Machine
```bash
# Replace localhost with IP
curl "http://192.168.1.100:8000/health"

# Or use hostname
curl "http://mycomputer:8000/health"
```

---

## 🐳 DOCKER COMMANDS

### Build Docker Image
```bash
cd backend
docker build -t health-check-api .

cd frontend
docker build -t health-check-dashboard .
```

### Run Docker Container
```bash
# Backend
docker run -p 8000:8000 health-check-api

# Frontend
docker run -p 3000:80 health-check-dashboard
```

### Docker Compose
```bash
# In project root
docker-compose up

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

---

## 📁 FILE NAVIGATION

### Key Files to Check
```bash
# Backend API
cat backend/main.py

# Scanners
cat backend/scanners/ssl_check.py
cat backend/scanners/headers_check.py
cat backend/scanners/ports_check.py
cat backend/scanners/risk_score.py

# Frontend App
cat frontend/src/App.jsx

# Components
ls frontend/src/components/

# API Service
cat frontend/src/services/api.js
```

### Configuration Files
```bash
# Python
cat backend/requirements.txt

# Node
cat frontend/package.json

# Tailwind
cat frontend/tailwind.config.js

# Vite
cat frontend/vite.config.js
```

---

## 🔐 SECURITY CHECKS

### Verify No Hardcoded Secrets
```bash
# Should find nothing
grep -r "localhost" backend/main.py | grep -v "allowed_origins"
grep -r "hardcoded" backend/
grep -r "secret" backend/

# Frontend should only have .env reference
grep -r "http://localhost:8000" frontend/src/ | grep -v ".env"
```

### Check Git Ignore
```bash
# Should ignore env files
cat .gitignore | grep .env

# Verify
git status | grep .env  # Should be empty
```

---

## 🎓 LEARNING COMMANDS

### View Source Code
```bash
# Backend structure
tree backend/ -L 2

# Frontend structure
tree frontend/src/ -L 2

# All files
find . -type f -name "*.py" -o -name "*.jsx"
```

### Search Code
```bash
# Find all API endpoints
grep -r "@app.get" backend/

# Find all React components
grep -r "export default" frontend/src/components/

# Find imports
grep -r "import " frontend/src/
```

---

## 📝 GIT COMMANDS

### Initial Setup
```bash
cd ..  # Go to parent of health_check_dashboard
git clone <your-repo-url>
cd health_check_dashboard
```

### Push Changes
```bash
git add .
git commit -m "Your message"
git push origin main
```

### View Diff
```bash
git diff
git status
git log
```

---

## 💻 SYSTEM COMMANDS

### Check Versions
```bash
python --version        # Should be 3.8+
node --version         # Should be 16+
npm --version          # Should be 8+
pip --version          # Should be 21+
```

### Check Ports
```bash
# Windows
netstat -ano

# macOS/Linux
lsof -i -P -n | grep LISTEN
```

### Virtual Environments
```bash
# Create
python -m venv venv

# Activate - Windows
venv\Scripts\activate

# Activate - macOS/Linux
source venv/bin/activate

# Deactivate
deactivate
```

---

## 🚀 ONE-LINER COMMANDS

### Start Everything (3 commands, each in separate terminal)
```bash
# Terminal 1
cd backend && python -m venv venv && venv\Scripts\activate && pip install -r requirements.txt && python main.py

# Terminal 2
cd frontend && npm install && echo "VITE_API_URL=http://localhost:8000" > .env.local && npm run dev

# Terminal 3
echo "Open http://localhost:5173"
```

---

## 📖 HELP COMMANDS

### Get Quick Help
```bash
cat QUICKSTART.md              # 5-minute setup
cat README.md | head -50       # Project overview
grep -A 5 "Troubleshooting" README.md
```

### Open Documentation
```bash
# Linux/macOS
open README.md
code README.md

# Windows
start README.md
```

---

## ⏱️ TIMING REFERENCE

| Task | Time |
|------|------|
| Setup backend | 2 min |
| Setup frontend | 2 min |
| First scan | 20-30 sec |
| Full deployment | 30-60 min |
| Full documentation read | 30 min |

---

**Remember**: Always start with **QUICKSTART.md** for the full setup! 🚀

This is just a quick reference for common commands.
