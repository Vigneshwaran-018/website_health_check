"""
Health Check Dashboard - FastAPI Backend
Security scanning application for websites

DISCLAIMER: This tool is designed for authorized security testing only.
Always obtain proper authorization before scanning any website.
Unauthorized network scanning may be illegal in your jurisdiction.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import re
from urllib.parse import urlparse

from scanners import check_ssl, check_headers, check_ports, calculate_risk_score


# Initialize FastAPI app
app = FastAPI(
    title="Health Check Dashboard API",
    description="Security scanning API for website health checks",
    version="1.0.0"
)

# Configure CORS for frontend communication
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
    "https://localhost:3000",
    "https://localhost:5173",
]

# Allow environment variable override for production
import os
if os.getenv("FRONTEND_URL"):
    ALLOWED_ORIGINS.append(os.getenv("FRONTEND_URL"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate and normalize the provided URL.
    
    Args:
        url: URL to validate
    
    Returns:
        Tuple of (is_valid, normalized_url or error_message)
    """
    if not url or len(url.strip()) == 0:
        return False, "URL cannot be empty"
    
    url = url.strip()
    
    # Basic URL pattern validation
    url_pattern = re.compile(
        r'^(?:(?:https?://)?(?:www\.)?)?'  # Optional protocol and www
        r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'  # Subdomains
        r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?'  # Domain
        r'(?:\.[a-zA-Z]{2,})?'  # TLD
        r'(?:[/?#].*)?$'  # Optional path, query, fragment
    )
    
    if not url_pattern.match(url):
        return False, "Invalid URL format"
    
    # Normalize URL (remove protocol if present for domain extraction)
    normalized = url.replace("http://", "").replace("https://", "").split('/')[0]
    
    if len(normalized) < 3:
        return False, "Domain name too short"
    
    return True, normalized


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Health Check Dashboard API",
        "version": "1.0.0",
        "endpoints": {
            "scan": "/scan?url=example.com",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring."""
    return {
        "status": "healthy",
        "service": "Health Check Dashboard API"
    }


@app.get("/scan")
async def scan_website(url: str = Query(..., min_length=3, max_length=500)) -> Dict[str, Any]:
    """
    Scan a website for security issues.
    
    DISCLAIMER: This endpoint should only be used to scan websites you own
    or have explicit permission to scan. Unauthorized scanning may be illegal.
    
    Args:
        url: Website URL to scan (e.g., example.com or https://example.com)
    
    Returns:
        Comprehensive security scan results
    
    Raises:
        HTTPException: If URL is invalid or scan fails
    """
    try:
        # Validate and normalize URL
        is_valid, result = validate_url(url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=result)
        
        normalized_url = result
        
        # Execute all security checks
        ssl_result = check_ssl(normalized_url)
        headers_result = check_headers(f"https://{normalized_url}")
        ports_result = check_ports(normalized_url)
        
        # Calculate risk score
        risk_score_result = calculate_risk_score(ssl_result, headers_result, ports_result)
        
        # Compile final response
        return {
            "url": normalized_url,
            "scan_timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "ssl": ssl_result,
            "headers": headers_result,
            "ports": ports_result,
            "risk_score": risk_score_result,
            "summary": {
                "overall_risk": risk_score_result['risk_level'],
                "risk_score": risk_score_result['score'],
                "ssl_valid": ssl_result.get('is_valid', False),
                "missing_headers_count": headers_result.get('missing_count', 0),
                "open_ports_count": ports_result.get('ports_open_count', 0)
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Scan failed: {str(e)}"
        )


@app.get("/scan/quick")
async def quick_scan(url: str = Query(..., min_length=3, max_length=500)) -> Dict[str, Any]:
    """
    Quick scan endpoint that returns only critical information.
    Useful for repeated checks on the same domain.
    
    Args:
        url: Website URL to scan
    
    Returns:
        Simplified scan results with key metrics only
    """
    try:
        # Validate and normalize URL
        is_valid, result = validate_url(url)
        if not is_valid:
            raise HTTPException(status_code=400, detail=result)
        
        normalized_url = result
        
        # Execute security checks
        ssl_result = check_ssl(normalized_url)
        headers_result = check_headers(f"https://{normalized_url}")
        ports_result = check_ports(normalized_url)
        risk_score_result = calculate_risk_score(ssl_result, headers_result, ports_result)
        
        return {
            "url": normalized_url,
            "score": risk_score_result['score'],
            "risk_level": risk_score_result['risk_level'],
            "ssl_valid": ssl_result.get('is_valid', False),
            "missing_headers": headers_result.get('missing_count', 0),
            "open_ports": ports_result.get('ports_open_count', 0)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Quick scan failed: {str(e)}"
        )


@app.get("/api/health-check")
async def api_health():
    """Alternative health endpoint for load balancers."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    
    # Get port from environment or default to 8000
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if os.getenv("ENV") == "development" else False
    )
