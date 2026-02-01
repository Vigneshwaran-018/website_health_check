"""
Attacker vs Defender Analysis Module
Provides two perspectives on security findings: attacker exploitation view vs defender remediation view.
"""

from typing import Dict, List, Any


# Mapping of issues to attack types
ATTACK_MAPPINGS = {
    "Content-Security-Policy": {
        "attack_type": "XSS (Cross-Site Scripting)",
        "exploit_description": "Attacker can inject malicious JavaScript that will execute in victim's browser",
        "impact": "Steal session tokens, redirect users, deface website",
        "likelihood": "High"
    },
    "X-Frame-Options": {
        "attack_type": "Clickjacking",
        "exploit_description": "Attacker can frame the website in a hidden overlay to trick users into clicking malicious content",
        "impact": "Perform unauthorized actions on behalf of user",
        "likelihood": "Medium-High"
    },
    "Strict-Transport-Security": {
        "attack_type": "Man-in-the-Middle (MITM)",
        "exploit_description": "Attacker can downgrade HTTPS to HTTP or intercept unencrypted traffic on first visit",
        "impact": "Intercept credentials, sensitive data, or inject malware",
        "likelihood": "Medium"
    },
    "X-Content-Type-Options": {
        "attack_type": "MIME Sniffing",
        "exploit_description": "Browser may interpret files as executable scripts even if they're supposed to be images/documents",
        "impact": "Execute arbitrary code, XSS attacks",
        "likelihood": "Low-Medium"
    },
}

# Dangerous port exploit mappings
PORT_EXPLOITS = {
    21: {
        "attack_type": "FTP Credential Compromise",
        "exploit": "FTP transmits credentials in plaintext. Attacker can intercept or brute-force",
        "impact": "Full file system access, malware upload, website defacement"
    },
    22: {
        "attack_type": "SSH Brute Force / Key Compromise",
        "exploit": "Attacker attempts password cracking or uses leaked keys to gain shell access",
        "impact": "Server takeover, data exfiltration, malware installation"
    },
    23: {
        "attack_type": "Telnet Protocol Exploitation",
        "exploit": "Telnet uses no encryption. Credentials and commands visible in plaintext",
        "impact": "Server takeover, privilege escalation"
    },
    445: {
        "attack_type": "SMB/Windows Share Exploitation",
        "exploit": "Attacker attempts to access shared resources, exploit SMB vulnerabilities (EternalBlue, etc.)",
        "impact": "Lateral movement, ransomware deployment, data theft"
    },
    3306: {
        "attack_type": "MySQL Database Takeover",
        "exploit": "Exposed MySQL with weak credentials or no authentication",
        "impact": "Full database access, customer data theft, SQL injection amplification"
    },
    5432: {
        "attack_type": "PostgreSQL Database Takeover",
        "exploit": "Exposed PostgreSQL instance allows unauthenticated or weak-auth access",
        "impact": "Full database access, data exfiltration, privilege escalation"
    },
    27017: {
        "attack_type": "MongoDB Ransomware/Data Theft",
        "exploit": "MongoDB defaults often have no authentication. Attacker wipes or exfiltrates data",
        "impact": "Complete data loss or breach, business disruption"
    },
    3389: {
        "attack_type": "RDP Brute Force / Exploitation",
        "exploit": "Attacker attempts to crack RDP credentials or exploit RDP vulnerabilities",
        "impact": "Direct server access, ransomware, lateral movement"
    },
    5900: {
        "attack_type": "VNC Unauthorized Access",
        "exploit": "VNC with weak/no authentication allows remote desktop takeover",
        "impact": "Full server control, malware installation, data theft"
    },
}

SSL_ATTACKS = {
    "missing_ssl": {
        "attack_type": "HTTP Downgrade / Man-in-the-Middle",
        "exploit": "No HSTS means browsers accept HTTP. Attacker intercepts traffic",
        "impact": "Steal authentication tokens, redirect to phishing sites, inject malware"
    },
    "expired_ssl": {
        "attack_type": "SSL Certificate Spoofing",
        "exploit": "Expired certificate may be trusted by older clients or misconfigurations",
        "impact": "MITM attacks, data interception, malware injection"
    }
}


def generate_attacker_view(
    ssl_data: Dict[str, Any],
    headers_data: Dict[str, Any],
    ports_data: Dict[str, Any],
    risk_score: float
) -> Dict[str, Any]:
    """
    Generate attacker perspective on security findings.
    Highlights exploitation possibilities and attack vectors.
    
    Args:
        ssl_data: SSL/TLS check results
        headers_data: Security headers check results
        ports_data: Open ports check results
        risk_score: Overall risk score
    
    Returns:
        Attacker-perspective analysis with attack vectors and exploitation paths
    """
    
    # Defensive defaults
    ssl_data = ssl_data or {}
    headers_data = headers_data or {}
    ports_data = ports_data or {}
    try:
        risk_score = float(risk_score or 0)
    except Exception:
        risk_score = 0.0

    attack_vectors = []
    exploitation_paths = []
    
    # SSL/TLS vulnerabilities
    if not ssl_data.get('is_valid', False):
        attack_vectors.append({
            "severity": "CRITICAL",
            "attack_type": SSL_ATTACKS["missing_ssl"]["attack_type"],
            "description": SSL_ATTACKS["missing_ssl"]["exploit"],
            "impact": SSL_ATTACKS["missing_ssl"]["impact"],
            "ease_of_exploitation": "Easy"
        })
        exploitation_paths.append("Setup malicious WiFi hotspot → intercept credentials → compromise user account")
    
    try:
        expires_in_days = int(ssl_data.get('expires_in_days', 365) or 365)
    except Exception:
        expires_in_days = 365
    if 0 < expires_in_days < 30:
        attack_vectors.append({
            "severity": "HIGH",
            "attack_type": "SSL Certificate Expiration",
            "description": f"Certificate expires in {expires_in_days} days. Attacker can replace with spoofed cert.",
            "impact": "Temporary window for successful MITM attacks",
            "ease_of_exploitation": "Medium"
        })
    
    # Missing security headers - normalize input
    missing_headers = headers_data.get('missing_headers') or headers_data.get('missing') or []
    if not isinstance(missing_headers, list):
        missing_headers = []
    header_exploits = {}

    for header in missing_headers:
        header_name = header.get('name') if isinstance(header, dict) else (str(header) if header else '')
        header_name = header_name or ''
        if header_name in ATTACK_MAPPINGS:
            mapping = ATTACK_MAPPINGS[header_name]
            header_exploits[header_name] = mapping
            
            attack_vectors.append({
                "severity": "HIGH",
                "attack_type": mapping.get("attack_type"),
                "description": mapping.get("exploit_description"),
                "impact": mapping.get("impact"),
                "ease_of_exploitation": "Medium" if mapping.get("likelihood") == "High" else "Hard"
            })
    
    # Add exploitation path for XSS if CSP missing
    if header_exploits.get("Content-Security-Policy"):
        exploitation_paths.append("Inject XSS payload in comment/input field → steal admin session token → takeover account")
    
    # Add exploitation path for clickjacking if X-Frame-Options missing
    if header_exploits.get("X-Frame-Options"):
        exploitation_paths.append("Create fake login form overlay → trick user into entering credentials → harvest credentials")
    
    # Open ports vulnerabilities - normalize
    open_ports = ports_data.get('open_ports') or ports_data.get('ports') or []
    if not isinstance(open_ports, list):
        open_ports = []
    dangerous_ports_found = []
    
    for port_info in open_ports:
        try:
            port = port_info.get('port') if isinstance(port_info, dict) else int(port_info)
        except Exception:
            continue
        if port in PORT_EXPLOITS:
            exploit = PORT_EXPLOITS[port]
            dangerous_ports_found.append(port)
            
            attack_vectors.append({
                "severity": "CRITICAL",
                "attack_type": exploit.get("attack_type"),
                "description": exploit.get("exploit"),
                "impact": exploit.get("impact"),
                "ease_of_exploitation": "Easy" if port in [27017, 3306, 5432] else "Medium"
            })
    
    if dangerous_ports_found:
        ports_str = ", ".join(map(str, dangerous_ports_found))
        exploitation_paths.append(f"Scan for common credentials on ports {ports_str} → gain direct system/database access")
    
    # Calculate overall attacker attractiveness safely
    try:
        attacker_score = len(attack_vectors) * 20 + (float(risk_score) / 5)
    except Exception:
        attacker_score = len(attack_vectors) * 20
    attacker_score = min(100, attacker_score)
    
    return {
        "perspective": "attacker",
        "attacker_attractiveness_score": round(attacker_score, 2),
        "attack_vectors": sorted(attack_vectors, key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2}.get(x["severity"], 3)),
        "exploitation_paths": exploitation_paths,
        "recommended_targets": [t for t in [
            "Database ports (3306, 5432, 27017)" if any(p in dangerous_ports_found for p in [3306, 5432, 27017]) else None,
            "Admin/management ports (22, 3389)" if any(p in dangerous_ports_found for p in [22, 3389]) else None,
            "XSS injection points" if header_exploits.get("Content-Security-Policy") else None,
        ] if t],
        "summary": f"This site presents {len(attack_vectors)} significant attack vectors. Overall difficulty: {'Easy' if attacker_score > 70 else 'Medium' if attacker_score > 40 else 'Hard'}"
    }


def generate_defender_view(
    ssl_data: Dict[str, Any],
    headers_data: Dict[str, Any],
    ports_data: Dict[str, Any],
    risk_score: float,
    site_context: str = "marketing"
) -> Dict[str, Any]:
    """
    Generate defender perspective on security findings.
    Prioritized fixes and impact reduction strategy.
    
    Args:
        ssl_data: SSL/TLS check results
        headers_data: Security headers check results
        ports_data: Open ports check results
        risk_score: Overall risk score
        site_context: Site context for prioritization
    
    Returns:
        Defender-perspective remediation plan with prioritized fixes
    """
    
    # Defensive defaults and normalization
    ssl_data = ssl_data or {}
    headers_data = headers_data or {}
    ports_data = ports_data or {}
    try:
        risk_score = float(risk_score or 0)
    except Exception:
        risk_score = 0.0

    fixes = []
    impact_reductions = []
    quick_wins = []
    
    # Priority order based on context
    context_priorities = {
        "authentication": ["SSL/TLS", "CSP", "Ports"],
        "ecommerce": ["SSL/TLS", "CSP", "Ports"],
        "marketing": ["SSL/TLS", "CSP"],
        "internal": ["Ports", "SSL/TLS"],
    }
    
    priority_order = context_priorities.get(site_context, ["SSL/TLS", "CSP", "Ports"])
    
    # SSL/TLS fixes
    if not ssl_data.get('is_valid', False):
        fixes.append({
            "priority": 1,
            "category": "SSL/TLS",
            "issue": "Missing or invalid SSL certificate",
            "fix": "Obtain SSL certificate from Let's Encrypt (free) or commercial CA",
            "effort": "Low (30 mins)",
            "impact_reduction": "Eliminates MITM attacks, increases user trust",
            "tools": ["Let's Encrypt", "Certbot", "AWS Certificate Manager"]
        })
        impact_reductions.append(f"Fixes SSL/TLS: Risk score would improve by ~40 points")
    else:
        try:
            expires_in_days = int(ssl_data.get('expires_in_days', 365) or 365)
        except Exception:
            expires_in_days = 365
        if 0 < expires_in_days < 30:
            quick_wins.append({
                "action": "Renew SSL certificate",
                "timeline": "Within 30 days",
                "effort": "Very Low (10 mins)"
            })
    
    # Security headers fixes
    missing_headers = headers_data.get('missing_headers') or headers_data.get('missing') or []
    if not isinstance(missing_headers, list):
        missing_headers = []
    header_priority_map = {h: i for i, h in enumerate([
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options"
    ])}
    
    for idx, header in enumerate(missing_headers):
        header_name = header.get('name') if isinstance(header, dict) else (str(header) if header else '')
        header_name = header_name or ''
        header_priority = header_priority_map.get(header_name, 5)

        fixes.append({
            "priority": 2 + header_priority,
            "category": "Security Headers",
            "header": header_name,
            "issue": f"Missing {header_name}",
            "fix": f"Add '{header_name}' header to all HTTP responses",
            "effort": "Low (10-20 mins)",
            "impact_reduction": f"Eliminates {ATTACK_MAPPINGS.get(header_name, {}).get('attack_type', 'various attacks')}",
            "config_example": get_header_config_snippet(header_name)
        })
    
    if missing_headers:
        reduction_count = len(missing_headers) * 5
        impact_reductions.append(f"Fixes all headers: Risk score would improve by ~{reduction_count} points")
    
    # Open ports fixes
    open_ports = ports_data.get('open_ports') or ports_data.get('ports') or []
    if not isinstance(open_ports, list):
        open_ports = []
    for port_info in open_ports:
        try:
            port = port_info.get('port') if isinstance(port_info, dict) else int(port_info)
        except Exception:
            continue
        if port in PORT_EXPLOITS:
            exploit = PORT_EXPLOITS[port]
            
            fixes.append({
                "priority": 2,
                "category": "Open Ports",
                "port": port,
                "issue": f"Dangerous port {port} ({exploit.get('attack_type','') .split()[0]}) is exposed",
                "fix": f"Close port {port} or restrict with firewall rules (allowlist specific IPs)",
                "effort": "Low (5-15 mins)",
                "impact_reduction": "Removes direct attack vector",
                "firewall_commands": get_firewall_rules(port)
            })
    
    if open_ports:
        dangerous = [p for p in open_ports if (isinstance(p, dict) and p.get('port') in PORT_EXPLOITS) or (isinstance(p, int) and p in PORT_EXPLOITS)]
        if dangerous:
            impact_reductions.append(f"Closes {len(dangerous)} dangerous ports: Risk score would improve by ~{len(dangerous) * 3} points")
    
    # Quick wins (high impact, low effort)
    if not ssl_data.get('is_valid', False) and len(missing_headers) == 0 and len(open_ports) == 0:
        quick_wins.append({
            "action": "Site is already well-configured!",
            "timeline": "Maintain current state",
            "effort": "Monitor regularly"
        })
    
    return {
        "perspective": "defender",
        "prioritized_fixes": sorted(fixes, key=lambda x: x["priority"]),
        "quick_wins": quick_wins,
        "estimated_improvements": impact_reductions,
        "remediation_plan": {
            "phase_1": "SSL/TLS certificate (if missing)",
            "phase_2": "Security headers",
            "phase_3": "Open ports closure",
            "estimated_total_time": "30-60 minutes for full remediation"
        },
        "summary": f"Implement {len(fixes)} fixes to reach excellent security. Most critical: {fixes[0]['category'] if fixes else 'None'}"
    }


def get_header_config_snippet(header_name: str) -> str:
    """Generate configuration snippet for adding header."""
    snippets = {
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' https://trusted.cdn; style-src 'self' 'unsafe-inline'",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "X-Frame-Options": "SAMEORIGIN",
        "X-Content-Type-Options": "nosniff"
    }
    return snippets.get(header_name, "")


def get_firewall_rules(port: int) -> Dict[str, str]:
    """Generate firewall rules to close a port."""
    return {
        "iptables": f"sudo iptables -A INPUT -p tcp --dport {port} -j DROP",
        "firewalld": f"sudo firewall-cmd --permanent --remove-port={port}/tcp",
        "ufw": f"sudo ufw deny {port}",
        "windows": f"netsh advfirewall firewall add rule name=\"Block Port {port}\" dir=in action=block protocol=tcp localport={port}"
    }
