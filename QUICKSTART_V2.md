# Health Check Dashboard v2.0 - QUICK START GUIDE

## What's New in v2.0?

The dashboard now features advanced security intelligence with two powerful perspectives:

### 🛡️ Defender View
- **What it shows:** How to fix issues effectively
- **Best for:** Security teams focused on remediation
- **Includes:** Fix snippets, timelines, prioritized steps

### ⚔️ Attacker View  
- **What it shows:** Exploitation opportunities and risk surface
- **Best for:** Understanding your attack surface
- **Includes:** Attack vectors, exploit paths, severity assessment

---

## Getting Started

### 1. **Choose Your Site Context**
Before scanning, tell us what type of site you're testing:

- 📢 **Marketing Site** - Public content, general audience
- 🔐 **Authentication** - Login systems, user accounts  
- 🛒 **E-commerce** - Payments, customer data
- 🏢 **Internal** - Corporate systems, employee access

**Why?** Different site types need different security standards. Missing CSP on e-commerce is critical; missing on marketing is moderate.

### 2. **Toggle Your Analysis Mode**
Switch between perspectives to understand your security from both angles:

- **Defender mode (Blue):** Focus on fixes and improvements
- **Attacker mode (Red):** Focus on vulnerabilities and risks

### 3. **Scan Your Site**
Enter your domain - the dashboard will scan for:
- ✓ SSL/TLS certificate validity
- ✓ Security headers (CSP, HSTS, X-Frame-Options, etc.)
- ✓ Exposed ports and services

---

## Understanding Your Results

### The Security Pulse
The central animation shows your security status at a glance:

- **Green pulse** = Low risk (80+) ✅
- **Yellow pulse** = Medium risk (60-79) 🟡
- **Orange pulse** = High risk (40-59) ⚠️
- **Red pulse** = Critical (0-39) 🚨

The **fragments orbiting the core** represent active security issues.

### The Risk Score
Calculated based on your site context:

```
E-commerce site missing CSP = -30 points (CRITICAL)
Marketing site missing CSP = -10 points (MEDIUM)
Internal site missing CSP = -5 points (LOW)
```

### The Drift Timeline
See how your security has changed:

- 📈 **Improved** - Good news! You've made progress
- 📉 **Regressed** - New issues detected
- ➡️ **Stable** - No changes since last scan

---

## Using Advanced Features

### Actionable Fixes

Get exact configuration for your platform:

**Nginx:**
```nginx
add_header Content-Security-Policy "default-src 'self';" always;
```

**Apache:**
```apache
Header always set Content-Security-Policy "default-src 'self';"
```

**Express:**
```javascript
app.use(helmet()); // Automatically adds headers
```

**Django:**
```python
# settings.py
SECURE_HSTS_SECONDS = 31536000
```

### Attack Analysis (Attacker View)

See what attackers could exploit:
- XSS injection points
- Clickjacking opportunities  
- MITM attack windows
- Database exposure risks

### Executive Summary (Technical Layer)

Get business impact in simple terms:
- Overall risk assessment
- Compliance implications
- Customer trust implications
- Estimated cost of NOT fixing

---

## Key Metrics Explained

### Missing Headers
Each missing security header has different impact by context:

| Header | E-commerce | Authentication | Marketing | Internal |
|--------|-----------|-----------------|-----------|----------|
| CSP    | CRITICAL ⚠️ | CRITICAL ⚠️ | HIGH ⚠️ | LOW |
| HSTS   | CRITICAL ⚠️ | CRITICAL ⚠️ | HIGH ⚠️ | MEDIUM |
| X-Frame | HIGH ⚠️ | HIGH ⚠️ | MEDIUM | LOW |

### Open Ports

Most dangerous ports:
- **Port 3306** (MySQL) - Database exposed 🚨
- **Port 5432** (PostgreSQL) - Database exposed 🚨
- **Port 27017** (MongoDB) - Database exposed 🚨
- **Port 22** (SSH) - Admin access exposed ⚠️
- **Port 21** (FTP) - Unencrypted file access ⚠️

---

## Recommended Workflow

### For Developers
1. Scan with **e-commerce** context
2. Switch to **Defender view** (Blue)
3. Copy the fix snippets for your platform
4. Implement the fixes in priority order
5. Rescan to track improvements

### For Security Teams
1. Scan with **authentication** context
2. Toggle to **Attacker view** (Red)
3. Review exploitation paths
4. Document findings for remediation
5. Create tickets for each issue

### For Executives
1. Scan your site
2. Check the **executive summary** layer
3. Review business impact section
4. Understand ROI of security improvements
5. Approve remediation budget

---

## Color Language

The dashboard uses colors semantically:

### By Context
- 🔴 **Red** = Attacker perspective, threats
- 🔵 **Blue** = Defender perspective, solutions
- 🟣 **Purple** = Neutral/system information

### By Risk
- 🟢 **Green** = Secure, low risk (80+)
- 🟡 **Yellow** = Caution, medium risk (60-79)
- 🟠 **Orange** = Warning, high risk (40-59)
- 🔴 **Red** = Danger, critical risk (0-39)

---

## Tips & Best Practices

### ✅ DO:
- Scan sites you own or have permission to test
- Review both Defender AND Attacker views
- Set the correct site context for accurate scoring
- Implement high-priority fixes first
- Rescan regularly to track drift

### ❌ DON'T:
- Scan sites without authorization
- Assume all issues have equal priority
- Ignore context-specific recommendations
- Leave exposed database ports open
- Forget to enable security headers in production

---

## Getting Help

### Common Questions

**Q: Why does my score change between scans?**
A: Score can change if new ports opened, headers changed, or SSL cert expires.

**Q: Can I scan internal sites?**
A: Yes! Select "Internal" context for corp systems. Different scoring rules apply.

**Q: Which fix should I implement first?**
A: Check the Defender view - fixes are prioritized by impact and effort.

**Q: What's the difference between the two modes?**
A: Attacker mode = understand risks. Defender mode = understand fixes.

---

## API Integration (For Developers)

### Advanced Scan
```bash
curl "http://localhost:8000/scan/advanced?url=example.com&context=ecommerce&mode=both"
```

### Executive Summary
```bash
curl "http://localhost:8000/scan/layers?url=example.com&layer=executive"
```

### Standard Scan (Backward Compatible)
```bash
curl "http://localhost:8000/scan?url=example.com"
```

---

**For detailed technical documentation, see [IMPLEMENTATION_SUMMARY_V2.md](./IMPLEMENTATION_SUMMARY_V2.md)**

**Version:** 2.0.0  
**Last Updated:** January 2026
