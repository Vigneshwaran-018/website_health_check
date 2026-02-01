# Implementation Guide - Health Check Dashboard

Complete technical reference for understanding and extending the Health Check Dashboard.

## Table of Contents

1. [Backend Architecture](#backend-architecture)
2. [Frontend Architecture](#frontend-architecture)
3. [Scanner Modules Deep Dive](#scanner-modules-deep-dive)
4. [Component System](#component-system)
5. [API Specifications](#api-specifications)
6. [Extending the Project](#extending-the-project)

---

## Backend Architecture

### Application Flow

```
Request: GET /scan?url=example.com
    ↓
main.py validate_url()
    ↓ (parallel execution)
    ├── ssl_check.check_ssl()
    ├── headers_check.check_headers()
    └── ports_check.check_ports()
    ↓
risk_score.calculate_risk_score()
    ↓
Response: JSON with all results
```

### Main Application (main.py)

**Key Components:**

1. **FastAPI Initialization**
   ```python
   app = FastAPI(...)
   app.add_middleware(CORSMiddleware, ...)
   ```

2. **URL Validation**
   - Regex pattern matching for domain format
   - Prevents malformed input
   - Normalizes URLs (removes protocol)

3. **Endpoints**
   - `GET /` - API info
   - `GET /health` - Health check
   - `GET /scan` - Full scan (60s timeout)
   - `GET /scan/quick` - Quick scan (20s timeout)

4. **Error Handling**
   - HTTPException for client errors
   - Generic error messages for security
   - Comprehensive logging

### CORS Configuration

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    # Add production URLs here
]
```

**Customization:**
- Add frontend URLs to prevent CORS errors
- Use environment variable `FRONTEND_URL` for production
- Restrict to trusted domains only

---

## Frontend Architecture

### Component Hierarchy

```
App
├── Header
├── URLInput
├── LoadingSpinner (conditional)
├── ErrorDisplay (conditional)
├── Results Layout (conditional)
│   ├── Summary Header
│   ├── Grid Container
│   │   ├── RiskScoreCard
│   │   ├── SSLStatusCard
│   │   └── OpenPortsCard
│   ├── SecurityHeadersCard
│   ├── DeductionsTable
│   └── Recommendations
└── Footer
```

### State Management

```javascript
const [scanResults, setScanResults] = useState(null)
const [isLoading, setIsLoading] = useState(false)
const [error, setError] = useState(null)
const [lastScannedUrl, setLastScannedUrl] = useState(null)
```

### Data Flow

1. User enters URL in URLInput
2. URLInput calls `handleScan(url)`
3. `handleScan` calls `apiService.scanWebsite(url)`
4. API service makes request to backend
5. Results update React state
6. Components re-render with new data

---

## Scanner Modules Deep Dive

### SSL Check Module

**File**: `backend/scanners/ssl_check.py`

**Function**: `check_ssl(url: str) -> Dict[str, Any]`

**Process:**
1. Extract hostname from URL
2. Create SSL context with certificate validation
3. Connect to server on port 443
4. Get peer certificate information
5. Extract issued to, issued by, expiration
6. Calculate days until expiration
7. Determine validity status

**Return Structure:**
```python
{
    "is_valid": bool,
    "issued_to": str,
    "issued_by": str,
    "expires_in_days": int,
    "warning": str | None,
    "protocol_version": str,
    "cipher": str
}
```

**Error Cases:**
- SSLError → Invalid certificate
- Timeout → Connection timeout
- Any other exception → Unexpected error

### Headers Check Module

**File**: `backend/scanners/headers_check.py`

**Function**: `check_headers(url: str) -> Dict[str, Any]`

**Process:**
1. Ensure URL has protocol (add https:// if needed)
2. Make GET request with timeout
3. Extract headers from response
4. Check for each required header
5. Categorize into present/missing
6. Calculate coverage percentage

**Required Headers:**
- `Content-Security-Policy`
- `Strict-Transport-Security`
- `X-Frame-Options`
- `X-Content-Type-Options`

**Return Structure:**
```python
{
    "present_headers": List[Dict],  # {name, value, description}
    "missing_headers": List[Dict],  # {name, description}
    "headers_score": float,         # 0-100
    "missing_count": int,
    "all_headers": Dict             # Complete response headers
}
```

### Port Scanning Module

**File**: `backend/scanners/ports_check.py`

**Function**: `check_ports(url: str, max_port: int = 1024) -> Dict[str, Any]`

**Process:**
1. Extract hostname
2. Verify hostname is resolvable (DNS lookup)
3. Create thread pool for parallel scanning
4. For each port 1-1024:
   - Try to connect via socket
   - 1-second timeout per port
   - If connection succeeds, port is open
5. Identify service by port number
6. Sort and return results

**Thread Implementation:**
```python
for port in range(1, max_port + 1):
    thread = threading.Thread(
        target=check_port,
        args=(hostname, port, open_ports)
    )
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join(timeout=2)  # Overall timeout
```

**Service Mapping:**
- Port 21 → FTP
- Port 22 → SSH
- Port 443 → HTTPS
- Port 3306 → MySQL
- etc. (see COMMON_PORTS dict)

**Return Structure:**
```python
{
    "open_ports": List[Dict],  # {port, status, service}
    "total_scanned": int,
    "ports_open_count": int,
    "hostname": str
}
```

### Risk Score Module

**File**: `backend/scanners/risk_score.py`

**Function**: `calculate_risk_score(ssl_data, headers_data, ports_data) -> Dict`

**Scoring Algorithm:**

```
Start: 100 points

SSL/TLS Deductions:
- Invalid cert: -40
- Certificate expiring <30 days: -10

Security Headers Deductions:
- Missing header: -5 per header (max -20)

Open Ports Deductions:
- Dangerous port (SSH, MySQL, etc.): -3 per port
- Standard port: -2 per port

Final: score = max(0, min(100, 100 - total_deductions))
```

**Risk Levels:**
- 80-100: Low Risk (Green)
- 60-79: Medium Risk (Yellow)
- 40-59: High Risk (Orange)
- 0-39: Critical Risk (Red)

**Return Structure:**
```python
{
    "score": int,                      # 0-100
    "risk_level": str,                 # Low/Medium/High/Critical
    "risk_color": str,                 # green/yellow/orange/red
    "deductions": List[Dict],          # {category, issue, deduction}
    "total_deductions": int,
    "breakdown": {                     # Score by category
        "ssl_score": int,
        "headers_score": int,
        "ports_score": int
    }
}
```

---

## Component System

### Card Components

**Pattern:** Each card is self-contained with its own styling

**RiskScoreCard**
- Uses Recharts PieChart for visualization
- Donut chart showing score/remaining
- Risk color coding
- Contextual message based on score

**SSLStatusCard**
- Displays certificate information
- Status color (red/yellow/green)
- Warning indicators
- All certificate details

**SecurityHeadersCard**
- Lists present headers (green background)
- Lists missing headers (red background)
- Expandable headers to show values
- Coverage percentage

**OpenPortsCard**
- Sortable port list
- Service identification
- Danger level coloring
- Grouped display

### State Update Pattern

```javascript
// 1. Set loading
setIsLoading(true)
setError(null)

// 2. Call API
const result = await apiService.scanWebsite(url)

// 3. Handle success/error
if (result.success) {
  setScanResults(result.data)
} else {
  setError(result.error)
}

// 4. Clear loading
setIsLoading(false)
```

---

## API Specifications

### Request Format

```
GET /scan?url=example.com HTTP/1.1
Host: api.example.com
Content-Type: application/json
```

### Response Format (Success)

```json
HTTP/1.1 200 OK
Content-Type: application/json

{
  "url": "example.com",
  "scan_timestamp": "2024-01-31T10:30:00.000Z",
  "ssl": { ... },
  "headers": { ... },
  "ports": { ... },
  "risk_score": { ... },
  "summary": { ... }
}
```

### Response Format (Error)

```json
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "detail": "Invalid URL format"
}
```

### Error Status Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request (invalid URL) |
| 500 | Server error (scan failed) |
| 408 | Request timeout (scan took too long) |

---

## Extending the Project

### Adding New Scanners

1. **Create Module**
   ```python
   # backend/scanners/new_check.py
   def check_new_thing(url: str) -> Dict[str, Any]:
       try:
           # Your implementation
           return {
               "status": "success",
               "data": {...}
           }
       except Exception as e:
           return {
               "status": "error",
               "error": str(e)
           }
   ```

2. **Import in main.py**
   ```python
   from scanners import check_new_thing
   ```

3. **Add to scan endpoint**
   ```python
   new_result = check_new_thing(normalized_url)
   ```

4. **Add to response**
   ```python
   return {
       ...existing fields...,
       "new_check": new_result
   }
   ```

### Adding Frontend Components

1. **Create Component**
   ```jsx
   // frontend/src/components/NewCard.jsx
   export default function NewCard({ data }) {
       if (!data) return null
       return (
           <div className="rounded-lg shadow-md p-6 bg-white">
               {/* Your component */}
           </div>
       )
   }
   ```

2. **Add to App.jsx**
   ```jsx
   import NewCard from './components/NewCard'
   
   // In results section:
   <NewCard data={scanResults.new_check} />
   ```

### Customizing Styling

**Tailwind Colors:** Edit `frontend/tailwind.config.js`

```javascript
theme: {
  extend: {
    colors: {
      primary: { ... },
      custom: "#your-color"
    }
  }
}
```

**Global Styles:** Edit `frontend/src/index.css`

### Performance Optimization

**Backend:**
- Increase port scanning range: modify `max_port` parameter
- Add caching for repeated scans
- Implement rate limiting

**Frontend:**
- Use `React.memo()` for expensive components
- Implement pagination for large port lists
- Add result caching

### Adding Authentication

**Backend:**
```python
from fastapi.security import HTTPBearer
from fastapi import Depends

security = HTTPBearer()

@app.get("/scan")
async def scan_website(credentials: HTTPAuthCredentials = Depends(security)):
    # Verify token
    # Then proceed with scan
```

**Frontend:**
```javascript
// Add token to API headers
apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
```

---

## Database Integration (Optional)

### Adding Result Storage

```python
# backend/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./scan_results.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# In main.py
db: Session = Depends(get_db)

@app.get("/scan")
async def scan_website(url: str, db: Session = Depends(get_db)):
    # ... perform scan ...
    
    # Save result
    result = ScanResult(url=url, score=risk_score_result['score'])
    db.add(result)
    db.commit()
```

---

## Testing

### Backend Tests

```python
# backend/test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_scan_invalid_url():
    response = client.get("/scan?url=invalid@@url")
    assert response.status_code == 400

def test_scan_valid_url():
    response = client.get("/scan?url=google.com")
    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert "risk_score" in data
```

### Frontend Tests

```javascript
// frontend/src/components/__tests__/URLInput.test.jsx
import { render, screen, fireEvent } from '@testing-library/react'
import URLInput from '../URLInput'

describe('URLInput', () => {
  test('renders input field', () => {
    render(<URLInput onScan={() => {}} isLoading={false} />)
    expect(screen.getByPlaceholderText(/example.com/)).toBeInTheDocument()
  })
})
```

---

## Monitoring & Debugging

### Backend Debugging

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Add debug endpoints
@app.get("/debug/config")
async def debug_config():
    return {
        "cors_origins": ALLOWED_ORIGINS,
        "env": os.getenv("ENV")
    }
```

### Frontend Debugging

```javascript
// Enable verbose logging
const logger = {
    log: (msg, data) => console.log(`[APP] ${msg}`, data),
    error: (msg, err) => console.error(`[ERROR] ${msg}`, err)
}

// Use React DevTools browser extension
```

---

## Production Checklist

- [ ] Environment variables configured
- [ ] HTTPS/SSL enabled
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Error logging enabled
- [ ] Performance monitoring active
- [ ] Database backups scheduled
- [ ] Security headers added
- [ ] Input validation complete
- [ ] Documentation updated

---

## Troubleshooting

### Common Issues

**Issue**: Scan returns 0 open ports
- **Solution**: Normal! Most ports are closed for security
- **Check**: Try known-open port using `nc -zv hostname port`

**Issue**: Headers check returns error
- **Solution**: HTTPS required, add error handling
- **Check**: Verify URL is HTTPS accessible

**Issue**: Slow performance
- **Solution**: Port scanning is I/O bound
- **Optimize**: Reduce port range, add caching

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)
- [Python SSL Module](https://docs.python.org/3/library/ssl.html)
- [MDN: HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

---

**Version**: 1.0.0 | Last Updated: January 31, 2024
