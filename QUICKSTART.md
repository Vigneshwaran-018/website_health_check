# Quick Start Guide

Get the Health Check Dashboard running in 5 minutes.

## Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check Node version (need 16+)
node --version
npm --version
```

## Start Backend

```bash
cd backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Install and run
pip install -r requirements.txt
python main.py
```

✅ Backend running at: **http://localhost:8000**

**Test it:**
```bash
curl http://localhost:8000/health
```

## Start Frontend

**In a new terminal:**

```bash
cd frontend

# Install dependencies
npm install

# Create config
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

## Test Scan

1. Open browser to **http://localhost:5173**
2. Enter a website URL (e.g., `google.com`)
3. Click "Scan Now"
4. Wait 10-30 seconds for results

## File Structure Created

```
health_check_dashboard/
├── backend/
│   ├── main.py                 (FastAPI app - 350 lines)
│   ├── scanners/
│   │   ├── ssl_check.py        (SSL validation - 90 lines)
│   │   ├── headers_check.py    (Headers check - 70 lines)
│   │   ├── ports_check.py      (Port scanning - 90 lines)
│   │   └── risk_score.py       (Risk calculation - 120 lines)
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/         (10 React components)
│   │   ├── services/
│   │   │   └── api.js          (API client - 100 lines)
│   │   ├── config.js           (Configuration - 50 lines)
│   │   ├── App.jsx             (Main app - 300 lines)
│   │   └── index.css           (Styles)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
│
├── README.md                   (Main documentation)
├── ENV_CONFIG.md               (Environment setup)
├── DEPLOYMENT.md               (Deployment guide)
└── .gitignore
```

## What Each Component Does

### Backend Modules

**main.py**
- FastAPI server with 3 endpoints
- `/scan?url=...` - Full security audit
- `/scan/quick?url=...` - Quick metrics
- `/health` - Deployment check

**ssl_check.py**
- Validates SSL/TLS certificates
- Checks expiration dates
- Identifies protocol & cipher

**headers_check.py**
- Scans for 4 critical security headers
- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options

**ports_check.py**
- Scans ports 1-1024 in parallel
- Identifies running services
- Flags dangerous ports

**risk_score.py**
- Calculates 0-100 score
- Deducts points for issues
- Provides improvement recommendations

### Frontend Components

| Component | Purpose |
|-----------|---------|
| `Header.jsx` | Navigation bar |
| `URLInput.jsx` | URL input form |
| `RiskScoreCard.jsx` | Donut chart with score |
| `SSLStatusCard.jsx` | SSL info display |
| `SecurityHeadersCard.jsx` | Headers status |
| `OpenPortsCard.jsx` | Ports list |
| `DeductionsTable.jsx` | Score breakdown |
| `LoadingSpinner.jsx` | Loading state |
| `ErrorDisplay.jsx` | Error messages |
| `Footer.jsx` | Footer info |

## Key Features Implemented

✅ **SSL/TLS Validation**
- Checks certificate validity
- Monitors expiration (warns <30 days)
- Identifies protocol version & cipher

✅ **Security Headers Check**
- Detects 4 critical headers
- Shows which ones are missing
- Provides recommendations

✅ **Port Scanning**
- Scans common ports (1-1024)
- Identifies services (SSH, HTTP, etc.)
- Flags dangerous ports (FTP, Telnet, etc.)

✅ **Risk Scoring**
- 0-100 scale
- Detailed deduction breakdown
- Color-coded risk levels (Low/Medium/High/Critical)

✅ **Responsive Dashboard**
- Works on desktop & mobile
- Real-time loading states
- Executive-style presentation

## Environment Variables

### Backend
Create `backend/.env`:
```env
PORT=8000
ENV=development
FRONTEND_URL=http://localhost:5173
```

### Frontend
Create `frontend/.env.local`:
```env
VITE_API_URL=http://localhost:8000
```

## Common Commands

```bash
# Backend
cd backend
python main.py              # Run dev server
python -m pytest           # Run tests (if added)

# Frontend
cd frontend
npm run dev                # Dev server
npm run build              # Production build
npm run preview            # Preview production build
npm install <package>      # Add dependency
```

## API Examples

### Scan Website
```bash
curl "http://localhost:8000/scan?url=example.com"
```

### Quick Scan
```bash
curl "http://localhost:8000/scan/quick?url=example.com"
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

### API Docs
Open: **http://localhost:8000/docs**

## Troubleshooting

### Port 8000 already in use?
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

### Cannot connect backend from frontend?
1. Check `VITE_API_URL` in `frontend/.env.local`
2. Restart frontend dev server
3. Check browser console for errors

### Scan takes very long?
- Normal! Port scanning takes time (10-30 seconds)
- Timeout is set to 1 second per port
- Can be optimized for production

### Module not found errors?
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Next Steps

1. **Read full docs**: Check `README.md` for details
2. **Deploy backend**: See `DEPLOYMENT.md` → Render/Railway section
3. **Deploy frontend**: See `DEPLOYMENT.md` → Vercel section
4. **Customize**: Modify components in `frontend/src/components/`
5. **Add features**: Extend scanner modules as needed

## Important Reminders

⚠️ **Authorization Required**
- Only scan websites you own or have permission to scan
- Unauthorized scanning may be illegal
- Always respect terms of service

🔒 **Security**
- Never commit `.env` files
- Use HTTPS in production
- Enable CORS only for trusted domains
- Consider rate limiting

📈 **Monitoring**
- Check backend logs regularly
- Monitor API response times
- Track error rates
- Use platform-specific dashboards

---

**You're ready to go!** 🚀

For detailed documentation:
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
- Deployment: `DEPLOYMENT.md`
- Environment: `ENV_CONFIG.md`
