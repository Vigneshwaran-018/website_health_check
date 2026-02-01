"""
Risk Score Calculation Module
Calculates an overall security risk score (0-100) based on various factors.
"""

from typing import Dict, Any


def calculate_risk_score(ssl_data: Dict[str, Any], 
                        headers_data: Dict[str, Any], 
                        ports_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate overall security risk score based on multiple factors.
    
    Scoring algorithm:
    - Start with 100 points
    - Deduct points for security issues
    - SSL/TLS issues: -30 to -40 points
    - Missing security headers: -5 to -25 points
    - Open ports: -2 to -3 points per port
    
    Args:
        ssl_data: SSL check results
        headers_data: Headers check results
        ports_data: Port scan results
    
    Returns:
        Dictionary with risk score and breakdown
    """
    score = 100
    deductions = []
    
    # SSL/TLS scoring
    ssl_deduction = 0
    if not ssl_data.get('is_valid', False):
        ssl_deduction = 40
        deductions.append({
            "category": "SSL/TLS",
            "issue": "Invalid or missing SSL certificate",
            "deduction": ssl_deduction
        })
    else:
        # Check expiration warning
        expires_in_days = ssl_data.get('expires_in_days', 365)
        if expires_in_days < 30 and expires_in_days > 0:
            ssl_deduction = 10
            deductions.append({
                "category": "SSL/TLS",
                "issue": f"Certificate expires in {expires_in_days} days",
                "deduction": ssl_deduction
            })
    
    score -= ssl_deduction
    
    # Security Headers scoring
    missing_headers = headers_data.get('missing_count', 0)
    headers_deduction = missing_headers * 5  # 5 points per missing header
    
    if headers_deduction > 0:
        deductions.append({
            "category": "Security Headers",
            "issue": f"{missing_headers} critical security headers missing",
            "deduction": headers_deduction
        })
    
    score -= headers_deduction
    
    # Open Ports scoring
    open_ports_count = ports_data.get('ports_open_count', 0)
    
    # Calculate port deduction (higher deduction for certain dangerous ports)
    open_ports = ports_data.get('open_ports', [])
    dangerous_ports = {21, 22, 23, 445, 3306, 5432, 27017}  # FTP, SSH, Telnet, SMB, MySQL, PostgreSQL, MongoDB
    
    ports_deduction = 0
    dangerous_open = []
    
    for port_info in open_ports:
        port = port_info['port']
        if port in dangerous_ports:
            ports_deduction += 3  # More severe penalty
            dangerous_open.append(port)
        else:
            ports_deduction += 2  # Standard penalty
    
    if ports_deduction > 0:
        issue = f"{open_ports_count} open port(s) detected"
        if dangerous_open:
            issue += f" including dangerous services: {', '.join(map(str, dangerous_open))}"
        
        deductions.append({
            "category": "Open Ports",
            "issue": issue,
            "deduction": ports_deduction
        })
    
    score -= ports_deduction
    
    # Ensure score stays within 0-100 range
    score = max(0, min(100, score))
    
    # Determine risk level
    if score >= 80:
        risk_level = "Low"
        risk_color = "green"
    elif score >= 60:
        risk_level = "Medium"
        risk_color = "yellow"
    elif score >= 40:
        risk_level = "High"
        risk_color = "orange"
    else:
        risk_level = "Critical"
        risk_color = "red"
    
    return {
        "score": score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "deductions": deductions,
        "total_deductions": 100 - score,
        "breakdown": {
            "ssl_score": 100 - ssl_deduction,
            "headers_score": max(0, 100 - headers_deduction),
            "ports_score": max(0, 100 - ports_deduction)
        }
    }
