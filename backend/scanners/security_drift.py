"""
Security Drift & Change Tracking Module
Tracks security changes over time and reports improvements/regressions.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


SCAN_HISTORY_FILE = "/tmp/security_scan_history.json"  # In-memory file-based storage


class ScanHistoryTracker:
    """Lightweight security drift tracker."""
    
    def __init__(self, history_file: str = SCAN_HISTORY_FILE):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load scan history from file."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_history(self) -> None:
        """Save scan history to file."""
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            pass  # Silently fail if unable to save
    
    def record_scan(self, url: str, scan_data: Dict[str, Any]) -> None:
        """Record a security scan result."""
        if url not in self.history:
            self.history[url] = []
        
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "risk_score": scan_data.get("risk_score", {}).get("score", 0),
            "risk_level": scan_data.get("risk_score", {}).get("risk_level", "UNKNOWN"),
            "ssl_valid": scan_data.get("ssl", {}).get("is_valid", False),
            "missing_headers_count": scan_data.get("headers", {}).get("missing_count", 0),
            "open_ports_count": scan_data.get("ports", {}).get("ports_open_count", 0),
            "missing_headers": [h.get('name') for h in scan_data.get("headers", {}).get("missing_headers", [])],
            "open_ports": [p.get('port') for p in scan_data.get("ports", {}).get("open_ports", [])]
        }
        
        self.history[url].append(record)
        self._save_history()
    
    def get_scan_history(self, url: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get scan history for a URL."""
        if url in self.history:
            return self.history[url][-limit:]
        return []
    
    def calculate_drift(self, url: str) -> Dict[str, Any]:
        """Calculate security drift for a URL."""
        history = self.get_scan_history(url, limit=None)
        
        if len(history) < 2:
            return {
                "has_history": len(history) > 0,
                "scans_recorded": len(history),
                "drift_detected": False,
                "summary": "Need at least 2 scans to detect drift"
            }
        
        # Compare latest vs previous scan
        latest = history[-1]
        previous = history[-2]
        
        # Calculate changes
        score_change = latest["risk_score"] - previous["risk_score"]
        score_direction = "improved" if score_change > 0 else "regressed" if score_change < 0 else "unchanged"
        
        headers_change = previous["missing_headers_count"] - latest["missing_headers_count"]
        ports_change = previous["open_ports_count"] - latest["open_ports_count"]
        ssl_change = "fixed" if not previous["ssl_valid"] and latest["ssl_valid"] else "broken" if previous["ssl_valid"] and not latest["ssl_valid"] else "no change"
        
        # Detect drift
        drift_detected = (
            abs(score_change) > 5 or
            headers_change != 0 or
            ports_change != 0 or
            ssl_change != "no change"
        )
        
        # Newly introduced risks
        new_risks = []
        if ssl_change == "broken":
            new_risks.append("SSL certificate became invalid")
        
        if headers_change < 0:  # More headers missing now
            new_headers_missing = set(latest["missing_headers"]) - set(previous["missing_headers"])
            if new_headers_missing:
                new_risks.append(f"New missing headers: {', '.join(new_headers_missing)}")
        
        if ports_change < 0:  # More ports open now
            new_ports = set(latest["open_ports"]) - set(previous["open_ports"])
            if new_ports:
                new_risks.append(f"New open ports: {', '.join(map(str, new_ports))}")
        
        # Improvements
        improvements = []
        if ssl_change == "fixed":
            improvements.append("SSL certificate issue resolved")
        
        if headers_change > 0:  # Fewer headers missing
            fixed_headers = set(previous["missing_headers"]) - set(latest["missing_headers"])
            if fixed_headers:
                improvements.append(f"Added security headers: {', '.join(fixed_headers)}")
        
        if ports_change > 0:  # Fewer ports open
            closed_ports = set(previous["open_ports"]) - set(latest["open_ports"])
            if closed_ports:
                improvements.append(f"Closed ports: {', '.join(map(str, closed_ports))}")
        
        return {
            "has_history": True,
            "scans_recorded": len(history),
            "drift_detected": drift_detected,
            "latest_timestamp": latest["timestamp"],
            "previous_timestamp": previous["timestamp"],
            "risk_score_change": {
                "previous": previous["risk_score"],
                "latest": latest["risk_score"],
                "delta": score_change,
                "direction": score_direction
            },
            "component_changes": {
                "ssl": ssl_change,
                "missing_headers": {
                    "previous": previous["missing_headers_count"],
                    "latest": latest["missing_headers_count"],
                    "delta": headers_change
                },
                "open_ports": {
                    "previous": previous["open_ports_count"],
                    "latest": latest["open_ports_count"],
                    "delta": ports_change
                }
            },
            "new_risks": new_risks,
            "improvements": improvements,
            "summary": f"Risk {score_direction} by {abs(score_change):.1f} points. {len(improvements)} improvements, {len(new_risks)} new issues."
        }


def generate_delta_summary(url: str, latest_scan: Dict[str, Any], tracker: Optional[ScanHistoryTracker] = None) -> Dict[str, Any]:
    """
    Generate delta summary comparing current scan to historical baseline.
    
    Args:
        url: Website URL
        latest_scan: Current scan data
        tracker: ScanHistoryTracker instance (creates new if None)
    
    Returns:
        Delta summary with changes and trends
    """
    
    if tracker is None:
        tracker = ScanHistoryTracker()
    
    # Record the latest scan
    tracker.record_scan(url, latest_scan)
    
    # Calculate drift
    drift = tracker.calculate_drift(url)
    
    if not drift.get("has_history"):
        return {
            "status": "baseline",
            "message": "First scan recorded. Future scans will show changes.",
            "drift": drift
        }
    
    return {
        "status": "tracked",
        "drift": drift,
        "trend": {
            "direction": drift["risk_score_change"]["direction"],
            "severity": "critical" if abs(drift["risk_score_change"]["delta"]) > 20 else "significant" if abs(drift["risk_score_change"]["delta"]) > 10 else "minor",
            "alerts": drift["new_risks"],
            "celebrations": drift["improvements"]
        },
        "recommendations": _generate_delta_recommendations(drift),
        "timeline": {
            "baseline_timestamp": drift.get("previous_timestamp"),
            "latest_timestamp": drift.get("latest_timestamp"),
            "scans_recorded": drift.get("scans_recorded")
        }
    }


def _generate_delta_recommendations(drift: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on drift analysis."""
    recommendations = []
    
    if drift.get("drift_detected"):
        if len(drift.get("new_risks", [])) > 0:
            recommendations.append("⚠️ Security regression detected. Address new risks immediately.")
        
        if len(drift.get("improvements", [])) > 0:
            recommendations.append("✅ Keep up the security improvements!")
        
        score_change = drift.get("risk_score_change", {}).get("delta", 0)
        if score_change < -20:
            recommendations.append("🚨 Critical regression: Score dropped significantly. Review recent infrastructure changes.")
        elif score_change < -5:
            recommendations.append("⚡ Notable regression: Score decreased. Investigate configuration changes.")
    else:
        recommendations.append("✓ Security posture is stable. Continue monitoring.")
    
    return recommendations


def get_security_timeline(url: str, tracker: Optional[ScanHistoryTracker] = None) -> List[Dict[str, Any]]:
    """
    Get security timeline for visualization.
    
    Args:
        url: Website URL
        tracker: ScanHistoryTracker instance
    
    Returns:
        Timeline data suitable for charting
    """
    
    if tracker is None:
        tracker = ScanHistoryTracker()
    
    history = tracker.get_scan_history(url, limit=None)
    
    timeline = []
    for scan in history:
        timeline.append({
            "timestamp": scan["timestamp"],
            "risk_score": scan["risk_score"],
            "risk_level": scan["risk_level"],
            "ssl_status": "🔐" if scan["ssl_valid"] else "🔓",
            "headers_missing": scan["missing_headers_count"],
            "ports_open": scan["open_ports_count"]
        })
    
    return timeline
