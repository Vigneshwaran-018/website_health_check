"""
Executive vs Technical Response Layers
Provides two interpretations of scan results: simplified executive summary and raw technical data.
"""

from typing import Dict, Any, List


def generate_executive_layer(scan_data: Dict[str, Any], risk_score: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate executive-friendly summary with business impact.
    
    Args:
        scan_data: Full scan results
        risk_score: Risk score data
    
    Returns:
        Executive summary with simplified language and business impact
    """
    
    risk_level = risk_score.get("risk_level", "UNKNOWN")
    risk_value = risk_score.get("score", 0)
    
    # Business impact mapping
    impact_mapping = {
        "CRITICAL": {
            "severity": "🚨 CRITICAL",
            "business_impact": "Your website is at immediate risk of compromise. Customer data, reputation, and revenue are in danger.",
            "urgency": "ADDRESS WITHIN 24 HOURS",
            "liability": "Potential legal/compliance violations. GDPR/CCPA fines possible.",
            "customer_trust": "⚠️ Severely compromised. Expect user churn and negative reviews.",
            "revenue_impact": "⬇️ High: Data breach costs, incident response, legal fees, customer compensation"
        },
        "HIGH": {
            "severity": "⚠️ HIGH",
            "business_impact": "Your website has significant security gaps. Attacks are likely to succeed.",
            "urgency": "ADDRESS WITHIN 1 WEEK",
            "liability": "Compliance risks. Regular audits recommended.",
            "customer_trust": "🟡 Moderately impacted. Users will question data safety.",
            "revenue_impact": "⬇️ Moderate: Increased support costs, potential breach cleanup"
        },
        "MEDIUM": {
            "severity": "🟡 MEDIUM",
            "business_impact": "Your website has room for improvement. Attack surface exists but is not critical.",
            "urgency": "PLAN IMPROVEMENTS IN 2-4 WEEKS",
            "liability": "Low risk but demonstrates due diligence if addressed.",
            "customer_trust": "🟢 Adequate. Most users feel reasonably safe.",
            "revenue_impact": "➡️ Minimal immediate impact but reduces long-term risk"
        },
        "LOW": {
            "severity": "✅ LOW",
            "business_impact": "Your website has strong security posture. Well-protected against common attacks.",
            "urgency": "MAINTAIN AND MONITOR",
            "liability": "✓ Demonstrates strong security governance.",
            "customer_trust": "🟢 Strong. Users have confidence in your security.",
            "revenue_impact": "⬆️ Positive: Builds brand trust, competitive advantage"
        }
    }
    
    impact = impact_mapping.get(risk_level, impact_mapping["MEDIUM"])
    
    # Issue count summary
    missing_headers = scan_data.get("headers", {}).get("missing_count", 0)
    open_ports = scan_data.get("ports", {}).get("ports_open_count", 0)
    ssl_valid = scan_data.get("ssl", {}).get("is_valid", False)
    
    issue_count = (0 if ssl_valid else 1) + missing_headers + open_ports
    
    # Create executive summary
    return {
        "security_grade": risk_level,
        "risk_percentage": 100 - risk_value,
        "executive_summary": {
            "headline": impact["severity"],
            "business_impact": impact["business_impact"],
            "urgency_level": impact["urgency"],
            "compliance_status": impact["liability"],
            "customer_trust_level": impact["customer_trust"],
            "financial_impact": impact["revenue_impact"]
        },
        "key_findings": {
            "total_issues": issue_count,
            "ssl_status": "✅ Secure" if ssl_valid else "❌ Exposed",
            "data_exposure": f"Missing {missing_headers} security headers" if missing_headers > 0 else "✅ Headers configured",
            "network_exposure": f"{open_ports} open port(s) detected" if open_ports > 0 else "✅ Ports secure"
        },
        "next_steps": _get_executive_next_steps(risk_level, ssl_valid, missing_headers, open_ports),
        "investment_case": {
            "cost_of_fixing": _get_fix_cost(ssl_valid, missing_headers, open_ports),
            "cost_of_not_fixing": _get_breach_cost(risk_value),
            "roi": "Immediate security improvement + long-term risk reduction"
        }
    }


def generate_technical_layer(scan_data: Dict[str, Any], risk_score: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate detailed technical response with raw data and metadata.
    
    Args:
        scan_data: Full scan results
        risk_score: Risk score data
    
    Returns:
        Technical layer with raw headers, metadata, and detailed analysis
    """
    
    return {
        "technical_summary": {
            "url": scan_data.get("url"),
            "scan_timestamp": scan_data.get("scan_timestamp"),
            "scan_version": "1.0",
            "methodology": "Automated security header and port scanning"
        },
        "risk_analysis": {
            "score": risk_score.get("score"),
            "risk_level": risk_score.get("risk_level"),
            "risk_color": risk_score.get("risk_color"),
            "weighted_factors": risk_score.get("why_score", {}).get("weighted_factors", []),
            "deductions": risk_score.get("deductions", [])
        },
        "ssl_tls_details": scan_data.get("ssl", {}),
        "security_headers": {
            "present": scan_data.get("headers", {}).get("present_headers", []),
            "missing": scan_data.get("headers", {}).get("missing_headers", []),
            "raw_headers": scan_data.get("headers", {}).get("all_headers", {})
        },
        "network_exposure": {
            "open_ports": scan_data.get("ports", {}).get("open_ports", []),
            "closed_ports_checked": scan_data.get("ports", {}).get("ports_checked", []),
            "port_scan_summary": {
                "total_scanned": scan_data.get("ports", {}).get("ports_checked", 0),
                "open_count": scan_data.get("ports", {}).get("ports_open_count", 0),
                "dangerous_count": len([p for p in scan_data.get("ports", {}).get("open_ports", []) if p.get('port') in [21, 22, 23, 445, 3306, 5432, 27017]])
            }
        },
        "metadata": {
            "scan_duration_ms": scan_data.get("scan_duration_ms", "N/A"),
            "backend_version": "1.0.0",
            "api_version": "1.0"
        },
        "raw_response": scan_data  # Full raw data included
    }


def _get_executive_next_steps(risk_level: str, ssl_valid: bool, missing_headers: int, open_ports: int) -> List[Dict[str, str]]:
    """Get prioritized next steps for executives."""
    
    steps = []
    
    if not ssl_valid:
        steps.append({
            "priority": "P0",
            "action": "Obtain SSL Certificate",
            "owner": "IT/DevOps",
            "timeline": "24-48 hours",
            "budget": "$0 (Let's Encrypt) or $100-1000 (commercial)"
        })
    
    if missing_headers > 0:
        steps.append({
            "priority": "P1",
            "action": f"Configure {missing_headers} Security Header(s)",
            "owner": "IT/Security",
            "timeline": "3-5 days",
            "budget": "$0 (dev time only)"
        })
    
    if open_ports > 0:
        steps.append({
            "priority": "P1",
            "action": f"Close/Restrict {open_ports} Exposed Port(s)",
            "owner": "Infrastructure",
            "timeline": "1-2 days",
            "budget": "$0 (configuration only)"
        })
    
    if not steps:
        steps.append({
            "priority": "P3",
            "action": "Maintain Current Security Posture",
            "owner": "Security Team",
            "timeline": "Ongoing",
            "budget": "Monitoring costs only"
        })
    
    return steps


def _get_fix_cost(ssl_valid: bool, missing_headers: int, open_ports: int) -> Dict[str, str]:
    """Estimate cost of fixing issues."""
    
    dev_hours = 0
    cert_cost = 0
    
    if not ssl_valid:
        dev_hours += 1
        cert_cost = 0  # Let's Encrypt
    
    if missing_headers > 0:
        dev_hours += (missing_headers * 0.5)  # ~30 min per header
    
    if open_ports > 0:
        dev_hours += (open_ports * 0.25)  # ~15 min per port closure
    
    hourly_rate = 75  # Average dev rate
    
    return {
        "developer_time": f"${dev_hours * hourly_rate:.0f} ({dev_hours:.1f} hours)",
        "certificate": f"${cert_cost}",
        "tools_and_services": "$0",
        "total_estimated": f"${(dev_hours * hourly_rate) + cert_cost:.0f}",
        "timeline": f"{max(1, int(dev_hours))} working day(s)"
    }


def _get_breach_cost(risk_score: float) -> Dict[str, str]:
    """Estimate potential breach costs based on risk score."""
    
    # Cost model based on risk score
    if risk_score >= 80:
        base_cost = 50000
        likelihood = "Very Low"
    elif risk_score >= 60:
        base_cost = 250000
        likelihood = "Low"
    elif risk_score >= 40:
        base_cost = 1000000
        likelihood = "Medium"
    else:
        base_cost = 3000000
        likelihood = "High"
    
    return {
        "average_breach_cost": f"${base_cost:,}",
        "likelihood_this_year": likelihood,
        "components": {
            "incident_response": "20%",
            "notification_costs": "25%",
            "legal_and_compliance": "15%",
            "remediation": "20%",
            "lost_revenue": "20%"
        },
        "note": "Based on 2024 IBMCOST industry averages"
    }


def merge_responses(executive_layer: Dict[str, Any], technical_layer: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge both response layers into a unified response.
    
    Args:
        executive_layer: Executive summary
        technical_layer: Technical details
    
    Returns:
        Combined response with both perspectives
    """
    
    return {
        "url": technical_layer.get("technical_summary", {}).get("url"),
        "scan_timestamp": technical_layer.get("technical_summary", {}).get("scan_timestamp"),
        "executive_view": executive_layer,
        "technical_view": technical_layer,
        "version": "2.0"  # New unified response version
    }
