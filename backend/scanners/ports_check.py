"""
Port Scanning Module
Checks for open ports on the target website.
"""

import socket
import threading
from typing import Dict, List, Any


COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    587: "SMTP",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    5432: "PostgreSQL",
    5984: "CouchDB",
    6379: "Redis",
    8080: "HTTP Alt",
    8443: "HTTPS Alt",
    27017: "MongoDB",
}


def check_port(hostname: str, port: int, results: List[Dict]) -> None:
    """
    Check if a single port is open.
    
    Args:
        hostname: Target hostname
        port: Port number to check
        results: List to store results
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            results.append({
                "port": port,
                "status": "open",
                "service": service
            })
    except Exception:
        pass


def check_ports(url: str, max_port: int = 1024) -> Dict[str, Any]:
    """
    Check for open ports on the target website (1-1024).
    
    Args:
        url: Website URL (domain name without protocol)
        max_port: Maximum port to scan (default 1024)
    
    Returns:
        Dictionary with port scan results
    """
    try:
        # Extract hostname from URL
        hostname = url.replace("http://", "").replace("https://", "").split('/')[0]
        
        # Verify hostname is resolvable
        try:
            socket.gethostbyname(hostname)
        except socket.gaierror:
            return {
                "open_ports": [],
                "total_scanned": 0,
                "error": f"Unable to resolve hostname: {hostname}"
            }
        
        open_ports = []
        threads = []
        
        # Create threads for parallel scanning
        # Note: Limit threads to avoid overwhelming the system
        for port in range(1, min(max_port + 1, 1025)):
            thread = threading.Thread(
                target=check_port,
                args=(hostname, port, open_ports)
            )
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=2)
        
        # Sort open ports by port number
        open_ports.sort(key=lambda x: x['port'])
        
        return {
            "open_ports": open_ports,
            "total_scanned": max_port,
            "ports_open_count": len(open_ports),
            "hostname": hostname
        }
    
    except Exception as e:
        return {
            "open_ports": [],
            "total_scanned": 0,
            "error": f"Port scanning error: {str(e)}"
        }
