# Health Check Dashboard for Websites

A comprehensive, security-focused web application that scans websites and displays an executive-style dashboard with security metrics.

**[🔒 Security First](#security-disclaimer) | [🚀 Quick Start](#quick-start) | [📊 Features](#features) | [🌐 Deployment](#deployment)**

## Features

✅ **SSL/TLS Certificate Validation**
- Certificate validity verification
- Expiration monitoring
- Protocol and cipher suite inspection

✅ **HTTP Security Headers Check**
- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options

✅ **Open Port Discovery**
- Scans ports 1-1024
- Service identification
- Risk level assessment

✅ **Risk Scoring System**
- Comprehensive 0-100 scoring
- Breakdown of security deductions
- Risk level categorization

✅ **Executive Dashboard**
- Real-time results visualization
- Interactive charts and cards
- Mobile-responsive design

## Security Disclaimer

⚠️ **IMPORTANT**: This tool is designed for authorized security testing only.

- **ONLY** scan websites you own or have explicit written permission to scan
- Unauthorized network scanning **MAY BE ILLEGAL** in your jurisdiction
- Users are solely responsible for legal compliance
- Always obtain proper authorization before use

## Quick Start

### Prerequisites

- **Backend**: Python 3.8+, pip
- **Frontend**: Node.js 16+, npm

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate
# Activate (macOS/Linux)
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python main.py
```

Backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Run dev server
npm run dev
```

Frontend will be available at `http://localhost:5173`

### 3. Test

Open browser to `http://localhost:5173` and enter a website URL to scan.

## Project Structure

```
health_check_dashboard/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── scanners/
│   │   ├── ssl_check.py        # SSL/TLS validation
│   │   ├── headers_check.py    # Security headers check
│   │   ├── ports_check.py      # Port scanning
│   │   ├── risk_score.py       # Risk calculation
│   │   └── __init__.py
│   ├── requirements.txt        # Python dependencies
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── services/           # API client
│   │   ├── App.jsx             # Main component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Global styles
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── README.md
│
└── README.md                   # This file
```

## API Endpoints

### `GET /scan?url=example.com`

Performs full security scan.

**Response:**
```json
{
  "url": "example.com",
  "scan_timestamp": "2024-01-31T10:30:00",
  "ssl": {
    "is_valid": true,
    "issued_to": "example.com",
    "expires_in_days": 89
  },
  "headers": {
    "present_headers": [...],
    "missing_headers": [...],
    "missing_count": 2
  },
  "ports": {
    "open_ports": [...],
    "ports_open_count": 2
  },
  "risk_score": {
    "score": 78,
    "risk_level": "Medium",
    "deductions": [...]
  }
}
```

### `GET /scan/quick?url=example.com`

Quick scan with only critical metrics.

### `GET /health`

Health check endpoint.

See [Backend README](backend/README.md) for full API documentation.

## Deployment

### Backend Deployment

#### Render.com

1. Push code to GitHub
2. Create Web Service on Render, connect repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables:
   - `FRONTEND_URL`: Your frontend URL
6. Deploy

#### Railway.app

1. Connect GitHub repository
2. Create Python service
3. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables
5. Deploy

#### Self-hosted (Docker)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment

#### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variable:
   - `VITE_API_URL`: Your backend API URL
4. Deploy (automatic on push)

```bash
# CLI deployment
npm install -g vercel
vercel
```

#### Netlify

1. Connect GitHub repository
2. Build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Set environment variables
4. Deploy

#### Self-hosted (Docker)

```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ARG VITE_API_URL
RUN VITE_API_URL=$VITE_API_URL npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Configuration

### Environment Variables

**Backend** (`.env` in backend directory):
```
PORT=8000
ENV=development
FRONTEND_URL=https://yourdomain.com
```

**Frontend** (`.env.local` in frontend directory):
```
VITE_API_URL=https://api.yourdomain.com
```

## Development

### Backend

- FastAPI with automatic API documentation at `/docs`
- Modular scanner architecture
- CORS support for frontend integration
- Comprehensive error handling

### Frontend

- React 18 with Hooks
- Vite for fast development
- Tailwind CSS for styling
- Recharts for visualizations
- Axios for API communication

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI (Python) |
| Backend Workers | requests, ssl, socket, threading |
| Frontend | React 18 + Vite |
| Styling | Tailwind CSS |
| Charts | Recharts |
| HTTP Client | Axios |
| Database | None (stateless) |

## Performance Considerations

- **Scans**: 10-30 seconds per website
- **Concurrent requests**: Limited by backend threading
- **Port scanning**: Parallel scanning with 1-second timeout per port
- **Rate limiting**: Recommended for production (implement in backend)

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

**SSL certificate verification fails:**
- Expected for some servers; reported as security issue
- Not a bug, part of security assessment

**Port scanning is slow:**
- Normal behavior; scanning 1024 ports with timeouts takes time
- Consider reducing scan scope in production

### Frontend Issues

**Cannot connect to backend:**
- Verify `VITE_API_URL` environment variable
- Ensure backend is running and accessible
- Check CORS configuration in backend

**Build fails:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Contributing

This is an educational project. Modifications welcome for learning purposes.

## License

Provided as-is for educational and authorized testing purposes.

## Support

For issues or questions:
1. Check the relevant README in backend/ or frontend/
2. Review API documentation at `http://localhost:8000/docs`
3. Verify environment variables are set correctly

---

**Remember**: Always obtain proper authorization before scanning any website. This tool is for educational and authorized security testing only.
