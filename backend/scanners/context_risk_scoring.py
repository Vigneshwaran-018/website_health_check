"""
Context-Aware Risk Scoring Module
Dynamically adjusts risk score weights based on site context (marketing, authentication, ecommerce, internal).
"""

from typing import Dict, Any, List
from enum import Enum


class SiteContext(str, Enum):
    """Enumeration of possible site contexts."""
    MARKETING = "marketing"
    AUTHENTICATION = "authentication"
    ECOMMERCE = "ecommerce"
    INTERNAL = "internal"


# Context-specific header criticality weights
HEADER_WEIGHTS = {
    "Content-Security-Policy": {
        "marketing": 0.4,      # Medium importance
        "authentication": 0.9, # Critical
        "ecommerce": 1.0,      # Critical
        "internal": 0.3,       # Low importance
    },
    "Strict-Transport-Security": {
        "marketing": 0.6,
        "authentication": 1.0,
        "ecommerce": 1.0,
        "internal": 0.5,
    },
    "X-Frame-Options": {
        "marketing": 0.5,
        "authentication": 0.9,
        "ecommerce": 0.9,
        "internal": 0.4,
    },
    "X-Content-Type-Options": {
        "marketing": 0.3,
        "authentication": 0.7,
        "ecommerce": 0.8,
        "internal": 0.3,
    },
}

# Context-specific port danger weights
DANGEROUS_PORTS = {
    21: {"name": "FTP", "base_danger": 1.0},
    22: {"name": "SSH", "base_danger": 0.7},
    23: {"name": "Telnet", "base_danger": 1.0},
    445: {"name": "SMB", "base_danger": 0.9},
    3306: {"name": "MySQL", "base_danger": 0.9},
    5432: {"name": "PostgreSQL", "base_danger": 0.9},
    27017: {"name": "MongoDB", "base_danger": 1.0},
    3389: {"name": "RDP", "base_danger": 0.8},
    5900: {"name": "VNC", "base_danger": 0.8},
}


def calculate_context_aware_risk(
    ssl_data: Dict[str, Any],
    headers_data: Dict[str, Any],
    ports_data: Dict[str, Any],
    site_context: str = "marketing",
    advanced: bool = False
) -> Dict[str, Any]:
    """
    Calculate risk score with context-aware weighting.
    
    Args:
        ssl_data: SSL/TLS check results
        headers_data: Security headers check results
        ports_data: Open ports check results
        site_context: Site context (marketing, authentication, ecommerce, internal)
    
    Returns:
        Dictionary with contextualized risk score, reasoning, and weighted factors
    """
    
    # Defensive defaults for missing inputs
    ssl_data = ssl_data or {}
    headers_data = headers_data or {}
    ports_data = ports_data or {}

    # Validate context
    try:
        context = SiteContext(site_context)
    except ValueError:
        context = SiteContext.MARKETING
    
    score = 100.0
    weighted_factors = []
    reasoning = []
    
    # ===== SSL/TLS SCORING =====
    ssl_deduction = 0
    ssl_reasoning = ""
    
    if not ssl_data.get('is_valid', False):
        # Critical for all contexts
        ssl_deduction = 40
        ssl_reasoning = f"Invalid or missing SSL certificate (critical for all site types)"
        reasoning.append(ssl_reasoning)
    else:
        # Ensure numeric expiry value
        try:
            expires_in_days = int(ssl_data.get('expires_in_days', 365) or 365)
        except Exception:
            expires_in_days = 365

        if 0 < expires_in_days < 30:
            ssl_deduction = 10
            ssl_reasoning = f"Certificate expires in {expires_in_days} days"
            reasoning.append(ssl_reasoning)
    
    if ssl_deduction > 0:
        weighted_factors.append({
            "category": "SSL/TLS",
            "weight": 1.0,  # No context adjustment for SSL
            "base_deduction": ssl_deduction,
            "adjusted_deduction": ssl_deduction,
            "reasoning": ssl_reasoning or "SSL/TLS configuration issues"
        })
    
    score -= ssl_deduction
    
    # ===== SECURITY HEADERS SCORING =====
    # Accept different shapes for headers_data and normalize
    missing_headers = headers_data.get('missing_headers') or headers_data.get('missing') or []
    if not isinstance(missing_headers, list):
        # If it's an integer (count), we can't reason about names; treat as empty list
        if isinstance(missing_headers, int):
            missing_headers = []
        else:
            missing_headers = []
    headers_deduction = 0
    headers_reasoning_list = []
    
    # Iterate safely - header may be a dict or a simple string
    for header in missing_headers:
        header_name = header.get('name') if isinstance(header, dict) else (str(header) if header else '')
        header_name = header_name or ''

        weight = HEADER_WEIGHTS.get(header_name, {}).get(context.value, 0.5)
        base_deduction = 5
        adjusted_deduction = base_deduction * (weight or 0.5)

        # Ensure numeric
        try:
            adjusted_deduction = float(adjusted_deduction)
        except Exception:
            adjusted_deduction = base_deduction * 0.5

        headers_deduction += adjusted_deduction

        context_label = context.value.upper()
        importance = "CRITICAL" if weight >= 0.8 else "HIGH" if weight >= 0.5 else "MEDIUM" if weight >= 0.3 else "LOW"

        headers_reasoning_list.append(
            f"Missing {header_name}: {importance} importance for {context_label} sites"
        )

        weighted_factors.append({
            "category": "Security Headers",
            "header": header_name,
            "weight": weight,
            "base_deduction": base_deduction,
            "adjusted_deduction": adjusted_deduction,
            "reasoning": f"{header_name} is {importance} for {context.value} sites"
        })
    
    if headers_deduction > 0:
        reasoning.extend(headers_reasoning_list[:3])  # Limit to 3 items
    
    score -= headers_deduction
    
    # ===== OPEN PORTS SCORING =====
    open_ports = ports_data.get('open_ports') or ports_data.get('ports') or []
    if not isinstance(open_ports, list):
        open_ports = []
    ports_deduction = 0
    ports_reasoning_list = []
    
    # Context-specific port danger multiplier
    port_danger_multipliers = {
        "marketing": 0.5,
        "authentication": 1.0,
        "ecommerce": 1.0,
        "internal": 0.3,
    }
    multiplier = port_danger_multipliers.get(context.value, 0.5)
    
    for port_info in open_ports:
        # port_info may be dict or simple int
        try:
            port = port_info.get('port') if isinstance(port_info, dict) else int(port_info)
        except Exception:
            # Skip invalid entries
            continue

        port_danger = DANGEROUS_PORTS.get(port, {}).get('base_danger', 1.5)
        port_name = DANGEROUS_PORTS.get(port, {}).get('name', f'Unknown (:{port})')

        base_deduction = port_danger * 3
        adjusted_deduction = base_deduction * (multiplier or 1.0)
        try:
            adjusted_deduction = float(adjusted_deduction)
        except Exception:
            adjusted_deduction = base_deduction

        ports_deduction += adjusted_deduction

        concern_text = "highly concerning" if adjusted_deduction > 2 else "concerning"
        ports_reasoning_list.append(
            f"Port {port} ({port_name}) open - {concern_text} for {context.value} sites"
        )

        weighted_factors.append({
            "category": "Open Ports",
            "port": port,
            "port_name": port_name,
            "weight": multiplier,
            "base_deduction": base_deduction,
            "adjusted_deduction": adjusted_deduction,
            "reasoning": f"Port {port} ({port_name}) exposure risk"
        })
    
    if ports_deduction > 0:
        reasoning.extend(ports_reasoning_list[:3])  # Limit to 3 items
    
    score -= ports_deduction
    
    # ===== ADVANCED ANALYSIS PENALTIES =====
    # When advanced mode is enabled, apply stricter penalties for dangerous combinations
    if advanced:
        try:
            missing_count = len(missing_headers)
        except Exception:
            missing_count = 0

        # Multiple missing headers => additional penalty
        if missing_count >= 2:
            combo_penalty = min(15, 5 * (missing_count - 1))
            score -= combo_penalty
            reasoning.append(f"Advanced penalty: {missing_count} missing headers increases attack surface")
            weighted_factors.append({
                "category": "Advanced Penalty",
                "issue": "Multiple missing headers",
                "adjusted_deduction": combo_penalty,
                "reasoning": "Stricter scoring applied in advanced analysis"
            })

        # Specific attack-chain detection: CSP + HSTS missing
        header_names = { (h.get('name') if isinstance(h, dict) else str(h)) for h in missing_headers }
        if ('Content-Security-Policy' in header_names) and ('Strict-Transport-Security' in header_names):
            chain_penalty = 10
            score -= chain_penalty
            reasoning.append("Advanced penalty: Missing CSP and HSTS - increased XSS+MITM chain risk")
            weighted_factors.append({
                "category": "Attack Chain",
                "issue": "CSP+HSTS missing",
                "adjusted_deduction": chain_penalty,
                "reasoning": "Detected header combination that enables attack chaining"
            })

        # Correlate open dangerous ports with missing headers
        try:
            dangerous_open_ports = [p for p in open_ports if (isinstance(p, dict) and p.get('port') in DANGEROUS_PORTS) or (isinstance(p, int) and p in DANGEROUS_PORTS)]
        except Exception:
            dangerous_open_ports = []

        if dangerous_open_ports and missing_count > 0:
            corr_penalty = min(20, 5 * len(dangerous_open_ports))
            score -= corr_penalty
            reasoning.append("Advanced penalty: Dangerous open ports combined with missing headers increase exploitation risk")
            weighted_factors.append({
                "category": "Advanced Correlation",
                "issue": "Ports + Headers",
                "adjusted_deduction": corr_penalty,
                "reasoning": "Correlated risk identified in advanced analysis"
            })

    # Ensure score stays within 0-100 range
    score = max(0, min(100, score))
    
    # Determine risk level
    if score >= 80:
        risk_level = "LOW"
        risk_color = "green"
    elif score >= 60:
        risk_level = "MEDIUM"
        risk_color = "yellow"
    elif score >= 40:
        risk_level = "HIGH"
        risk_color = "orange"
    else:
        risk_level = "CRITICAL"
        risk_color = "red"
    
    return {
        "score": round(score, 2),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "site_context": context.value,
        "why_score": {
            "summary": f"Risk score is {risk_level} for {context.value} site context",
            "factors": reasoning,
            "weighted_factors": weighted_factors
        },
        "deductions": weighted_factors
    }


def get_context_recommendations(
    context: str,
    missing_headers: List[Dict[str, Any]],
    open_ports: List[Dict[str, Any]],
    ssl_valid: bool
) -> List[Dict[str, str]]:
    """
    Generate context-specific security recommendations.
    
    Args:
        context: Site context
        missing_headers: List of missing security headers
        open_ports: List of open ports
        ssl_valid: Whether SSL is valid
    
    Returns:
        List of prioritized recommendations
    """
    recommendations = []
    
    # Context-specific priorities
    priorities = {
        "authentication": ["SSL/TLS", "CSP", "Ports"],
        "ecommerce": ["SSL/TLS", "CSP", "Headers", "Ports"],
        "marketing": ["SSL/TLS", "Headers", "Ports"],
        "internal": ["Ports", "SSL/TLS", "Headers"],
    }
    
    priority_list = priorities.get(context, ["SSL/TLS", "Headers", "Ports"])
    
    # SSL recommendations
    if not ssl_valid and "SSL/TLS" in priority_list:
        recommendations.append({
            "priority": "CRITICAL",
            "category": "SSL/TLS",
            "recommendation": "Obtain and install valid SSL certificate",
            "context_reason": "Essential for all website types, especially for user trust"
        })
    
    # Header recommendations based on context
    header_priorities = {
        "authentication": ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"],
        "ecommerce": ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"],
        "marketing": ["Content-Security-Policy", "Strict-Transport-Security"],
        "internal": ["X-Frame-Options", "X-Content-Type-Options"],
    }
    
    context_headers = header_priorities.get(context, [])
    for header in missing_headers:
        if header.get('name') in context_headers and "Headers" in priority_list:
            priority = "CRITICAL" if context_headers.index(header.get('name', '')) == 0 else "HIGH"
            recommendations.append({
                "priority": priority,
                "category": "Security Headers",
                "header": header.get('name'),
                "recommendation": f"Implement {header.get('name')}",
                "context_reason": f"Critical for {context} site protection"
            })
    
    # Port recommendations
    if open_ports and "Ports" in priority_list:
        dangerous_count = sum(1 for p in open_ports if p.get('port') in DANGEROUS_PORTS)
        if dangerous_count > 0:
            recommendations.append({
                "priority": "CRITICAL" if context != "internal" else "HIGH",
                "category": "Open Ports",
                "recommendation": f"Close {dangerous_count} dangerous port(s)",
                "context_reason": f"Exposed database/admin services detected"
            })
    
    return recommendations
