"""
HTTP Security Headers Check Module
Verifies the presence of critical security headers.
"""

import requests
from typing import Dict, List, Any


REQUIRED_HEADERS = {
    "Content-Security-Policy": "Controls what resources can be loaded",
    "Strict-Transport-Security": "Forces HTTPS connections",
    "X-Frame-Options": "Prevents clickjacking attacks",
    "X-Content-Type-Options": "Prevents MIME type sniffing"
}


def check_headers(url: str) -> Dict[str, Any]:
    """
    Check for presence of critical HTTP security headers.
    
    Args:
        url: Complete URL of the website
    
    Returns:
        Dictionary with header check results
    """
    try:
        # Ensure URL has protocol
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Make request with timeout
        response = requests.get(url, timeout=5, allow_redirects=True)
        headers = response.headers
        
        missing_headers = []
        present_headers = []
        
        # Check each required header
        for header_name, description in REQUIRED_HEADERS.items():
            if header_name in headers:
                present_headers.append({
                    "name": header_name,
                    "value": headers[header_name],
                    "description": description
                })
            else:
                missing_headers.append({
                    "name": header_name,
                    "description": description
                })
        
        # Calculate score (percentage of headers present)
        headers_score = (len(present_headers) / len(REQUIRED_HEADERS)) * 100
        
        return {
            "present_headers": present_headers,
            "missing_headers": missing_headers,
            "headers_score": headers_score,
            "missing_count": len(missing_headers),
            "all_headers": dict(headers)
        }
    
    except requests.exceptions.Timeout:
        return {
            "present_headers": [],
            "missing_headers": [{"name": h, "description": REQUIRED_HEADERS[h]} for h in REQUIRED_HEADERS],
            "headers_score": 0,
            "missing_count": len(REQUIRED_HEADERS),
            "error": "Request timeout"
        }
    
    except requests.exceptions.ConnectionError:
        return {
            "present_headers": [],
            "missing_headers": [{"name": h, "description": REQUIRED_HEADERS[h]} for h in REQUIRED_HEADERS],
            "headers_score": 0,
            "missing_count": len(REQUIRED_HEADERS),
            "error": "Connection error"
        }
    
    except Exception as e:
        return {
            "present_headers": [],
            "missing_headers": [{"name": h, "description": REQUIRED_HEADERS[h]} for h in REQUIRED_HEADERS],
            "headers_score": 0,
            "missing_count": len(REQUIRED_HEADERS),
            "error": f"Error checking headers: {str(e)}"
        }
