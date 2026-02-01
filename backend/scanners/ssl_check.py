"""
SSL/TLS Certificate Validation Module
Checks SSL certificate validity and expiration for a given URL.
"""

import ssl
import socket
from datetime import datetime
from typing import Dict, Any


def check_ssl(url: str) -> Dict[str, Any]:
    """
    Check SSL/TLS certificate status for a website.
    
    Args:
        url: Website URL (domain name without protocol)
    
    Returns:
        Dictionary with SSL status information
    """
    try:
        # Extract hostname from URL if it includes protocol
        hostname = url.replace("http://", "").replace("https://", "").split('/')[0]
        
        # Create SSL context
        context = ssl.create_default_context()
        
        # Connect to the server
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                # Get certificate information
                subject = dict(x[0] for x in cert['subject'])
                issued_to = subject.get('commonName', 'Unknown')
                
                # Check expiration date
                expiry_str = cert['notAfter']
                expiry_date = datetime.strptime(expiry_str, '%b %d %H:%M:%S %Y %Z')
                expires_in_days = (expiry_date - datetime.now()).days
                
                # Get issuer
                issuer = dict(x[0] for x in cert['issuer'])
                issued_by = issuer.get('organizationName', 'Unknown')
                
                is_valid = True
                warning = None
                
                # Check if certificate is expired
                if expires_in_days <= 0:
                    is_valid = False
                    warning = "Certificate has expired"
                elif expires_in_days < 30:
                    warning = f"Certificate expires in {expires_in_days} days"
                
                return {
                    "is_valid": is_valid,
                    "issued_to": issued_to,
                    "issued_by": issued_by,
                    "expires_in_days": expires_in_days,
                    "warning": warning,
                    "protocol_version": ssock.version(),
                    "cipher": ssock.cipher()[0]
                }
    
    except ssl.SSLError as e:
        return {
            "is_valid": False,
            "error": f"SSL Certificate Error: {str(e)}",
            "issued_to": "Unknown",
            "issued_by": "Unknown",
            "expires_in_days": -1,
            "warning": "Invalid SSL certificate",
            "protocol_version": None,
            "cipher": None
        }
    
    except socket.timeout:
        return {
            "is_valid": False,
            "error": "Connection timeout",
            "issued_to": "Unknown",
            "issued_by": "Unknown",
            "expires_in_days": -1,
            "warning": "Unable to verify SSL",
            "protocol_version": None,
            "cipher": None
        }
    
    except Exception as e:
        return {
            "is_valid": False,
            "error": f"Unexpected error: {str(e)}",
            "issued_to": "Unknown",
            "issued_by": "Unknown",
            "expires_in_days": -1,
            "warning": "SSL check failed",
            "protocol_version": None,
            "cipher": None
        }
