# Backend - Health Check Dashboard API

FastAPI server for security scanning of websites. This backend performs comprehensive security audits including SSL/TLS validation, HTTP security header checks, and port scanning.

## Features

- **SSL/TLS Certificate Validation**: Verifies certificate validity and expiration
- **Security Headers Check**: Detects missing critical HTTP security headers
- **Port Scanning**: Identifies open ports on the target domain
- **Risk Scoring**: Calculates an overall security risk score (0-100)
- **CORS Support**: Configured for frontend integration

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

```bash
python main.py
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI) will be available at `http://localhost:8000/docs`

### Configuration

Environment variables:
- `PORT`: API port (default: 8000)
- `ENV`: Environment mode (`development` or `production`)
- `FRONTEND_URL`: Additional allowed CORS origin for production

Example `.env` file:
```
PORT=8000
ENV=development
FRONTEND_URL=https://yourdomain.com
```

## API Endpoints

### GET `/scan?url=example.com`
Performs a full security scan on the provided website.

**Query Parameters:**
- `url` (required): Website URL to scan (e.g., `example.com` or `https://example.com`)

**Response:**
```json
{
  "url": "example.com",
  "scan_timestamp": "2024-01-31T10:30:00",
  "ssl": {
    "is_valid": true,
    "issued_to": "example.com",
    "issued_by": "Let's Encrypt",
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
    "risk_level": "Medium"
  }
}
```

### GET `/scan/quick?url=example.com`
Quick scan returning only critical metrics.

### GET `/health`
Health check endpoint for deployment monitoring.

## Scanner Modules

### `scanners/ssl_check.py`
Validates SSL/TLS certificates, checks expiration, and verifies protocol versions.

### `scanners/headers_check.py`
Scans for the presence of critical security headers:
- Content-Security-Policy
- Strict-Transport-Security
- X-Frame-Options
- X-Content-Type-Options

### `scanners/ports_check.py`
Scans ports 1-1024 for open connections and identifies running services.

### `scanners/risk_score.py`
Calculates an overall security risk score (0-100) based on:
- SSL/TLS validity (up to -40 points)
- Missing security headers (-5 points each)
- Open ports (-2 to -3 points each)

## Deployment

### Render.com

1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in Render dashboard
6. Deploy

### Railway.app

1. Push code to GitHub or connect Railway to Git
2. Create new project on Railway
3. Add Python service
4. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

### Local Development with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t health-check-api .
docker run -p 8000:8000 health-check-api
```

## Important Notes

### Authorization
Always obtain proper authorization before scanning any website. Unauthorized network scanning may be illegal in your jurisdiction.

### Rate Limiting
Implement rate limiting in production to prevent abuse:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### CORS Configuration
Update `ALLOWED_ORIGINS` in `main.py` with your frontend URLs for production.

### Timeout Considerations
Scans may take 10-30 seconds depending on target responsiveness. Consider implementing request timeouts on the frontend.

## Troubleshooting

**Issue: SSL certificate verification fails**
- Some servers may have certificate issues. The scanner will report this as part of the security assessment.

**Issue: Port scanning is slow**
- Port scanning (1-1024) uses threading but respects 1-second timeouts per port. Large-scale scanning may require optimization.

**Issue: CORS errors in frontend**
- Ensure your frontend URL is added to `ALLOWED_ORIGINS` in `main.py`

## Development

To modify scanner behavior:

1. Update relevant module in `scanners/`
2. Test locally at `http://localhost:8000/docs`
3. Use Swagger UI to test endpoint changes

## License

This project is provided as-is for educational and authorized testing purposes.
