"""
Actionable Fix Engine
Provides structured fix snippets for every issue across different web servers and frameworks.
"""

from typing import Dict, List, Any


# Fix snippets for missing headers
HEADER_FIXES = {
    "Content-Security-Policy": {
        "description": "Restricts what resources can be loaded, preventing XSS attacks",
        "fixes": {
            "nginx": {
                "config": "add_header Content-Security-Policy \"default-src 'self'; script-src 'self' 'unsafe-inline' https://trusted.cdn; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'\" always;",
                "location": "In http or server block of /etc/nginx/nginx.conf",
                "restart": "sudo systemctl restart nginx"
            },
            "apache": {
                "config": "Header always set Content-Security-Policy \"default-src 'self'; script-src 'self' 'unsafe-inline' https://trusted.cdn; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self'; frame-ancestors 'self'; form-action 'self'; base-uri 'self'\"",
                "location": "In .htaccess or Apache config file",
                "restart": "sudo systemctl restart apache2"
            },
            "express": {
                "code": "const csp = require('helmet-csp');\napp.use(csp({\n  directives: {\n    defaultSrc: [\"'self'\"],\n    scriptSrc: [\"'self'\", \"'unsafe-inline'\", \"https://trusted.cdn\"],\n    styleSrc: [\"'self'\", \"'unsafe-inline'\"],\n    imgSrc: [\"'self'\", \"data:\", \"https:\"],\n    connectSrc: [\"'self'\"],\n  }\n}));",
                "package": "npm install helmet-csp",
                "restart": "Restart Node.js application"
            },
            "django": {
                "code": "# settings.py\nCSP_DEFAULT_SRC = (\"'self'\",)\nCSP_SCRIPT_SRC = (\"'self'\", \"'unsafe-inline'\", \"https://trusted.cdn\")\nCSP_STYLE_SRC = (\"'self'\", \"'unsafe-inline'\")\n# Install django-csp: pip install django-csp\n# Add 'csp.middleware.CSPMiddleware' to MIDDLEWARE",
                "package": "pip install django-csp",
                "restart": "Restart Django application"
            },
            "flask": {
                "code": "from flask_talisman import Talisman\nfrom flask import Flask\napp = Flask(__name__)\nTalisman(app, force_https=True, strict_transport_security=True, content_security_policy={\n    'default-src': \"'self'\",\n    'script-src': [\"'self'\", \"'unsafe-inline'\", \"https://trusted.cdn\"],\n    'style-src': [\"'self'\", \"'unsafe-inline'\"]\n})",
                "package": "pip install flask-talisman",
                "restart": "Restart Flask application"
            }
        }
    },
    "Strict-Transport-Security": {
        "description": "Forces HTTPS connections and prevents downgrade attacks",
        "fixes": {
            "nginx": {
                "config": "add_header Strict-Transport-Security \"max-age=31536000; includeSubDomains; preload\" always;",
                "location": "In http or server block of /etc/nginx/nginx.conf",
                "restart": "sudo systemctl restart nginx"
            },
            "apache": {
                "config": "Header always set Strict-Transport-Security \"max-age=31536000; includeSubDomains; preload\"",
                "location": "In .htaccess or Apache config file",
                "restart": "sudo systemctl restart apache2"
            },
            "express": {
                "code": "const helmet = require('helmet');\napp.use(helmet.hsts({\n  maxAge: 31536000,\n  includeSubDomains: true,\n  preload: true\n}));",
                "package": "npm install helmet",
                "restart": "Restart Node.js application"
            },
            "django": {
                "code": "# settings.py\nSECURE_HSTS_SECONDS = 31536000\nSECURE_HSTS_INCLUDE_SUBDOMAINS = True\nSECURE_HSTS_PRELOAD = True\nSECURE_SSL_REDIRECT = True",
                "package": "Built-in (add to settings.py)",
                "restart": "Restart Django application"
            },
            "flask": {
                "code": "from flask_talisman import Talisman\napp = Flask(__name__)\nTalisman(app, force_https=True, strict_transport_security=True, strict_transport_security_max_age=31536000)",
                "package": "pip install flask-talisman",
                "restart": "Restart Flask application"
            }
        }
    },
    "X-Frame-Options": {
        "description": "Prevents clickjacking attacks by controlling frame embedding",
        "fixes": {
            "nginx": {
                "config": "add_header X-Frame-Options \"SAMEORIGIN\" always;",
                "location": "In http or server block of /etc/nginx/nginx.conf",
                "restart": "sudo systemctl restart nginx"
            },
            "apache": {
                "config": "Header always set X-Frame-Options \"SAMEORIGIN\"",
                "location": "In .htaccess or Apache config file",
                "restart": "sudo systemctl restart apache2"
            },
            "express": {
                "code": "const helmet = require('helmet');\napp.use(helmet.frameguard({ action: 'sameorigin' }));",
                "package": "npm install helmet",
                "restart": "Restart Node.js application"
            },
            "django": {
                "code": "# settings.py\nX_FRAME_OPTIONS = 'SAMEORIGIN'",
                "package": "Built-in (add to settings.py)",
                "restart": "Restart Django application"
            },
            "flask": {
                "code": "from flask_talisman import Talisman\napp = Flask(__name__)\nTalisman(app, frame_options='SAMEORIGIN')",
                "package": "pip install flask-talisman",
                "restart": "Restart Flask application"
            }
        }
    },
    "X-Content-Type-Options": {
        "description": "Prevents MIME type sniffing attacks",
        "fixes": {
            "nginx": {
                "config": "add_header X-Content-Type-Options \"nosniff\" always;",
                "location": "In http or server block of /etc/nginx/nginx.conf",
                "restart": "sudo systemctl restart nginx"
            },
            "apache": {
                "config": "Header always set X-Content-Type-Options \"nosniff\"",
                "location": "In .htaccess or Apache config file",
                "restart": "sudo systemctl restart apache2"
            },
            "express": {
                "code": "const helmet = require('helmet');\napp.use(helmet.noSniff());",
                "package": "npm install helmet",
                "restart": "Restart Node.js application"
            },
            "django": {
                "code": "# settings.py\nSECURE_CONTENT_TYPE_NOSNIFF = True",
                "package": "Built-in (add to settings.py)",
                "restart": "Restart Django application"
            },
            "flask": {
                "code": "@app.after_request\ndef set_security_headers(response):\n    response.headers['X-Content-Type-Options'] = 'nosniff'\n    return response",
                "package": "Built-in",
                "restart": "Restart Flask application"
            }
        }
    }
}

# Port closure fixes
PORT_CLOSURE_FIXES = {
    21: {  # FTP
        "description": "FTP is insecure - use SFTP instead",
        "fixes": {
            "iptables": "sudo iptables -A INPUT -p tcp --dport 21 -j DROP && sudo iptables-save > /etc/iptables/rules.v4",
            "firewalld": "sudo firewall-cmd --permanent --remove-port=21/tcp && sudo firewall-cmd --reload",
            "ufw": "sudo ufw deny 21",
            "windows": "netsh advfirewall firewall add rule name=\"Block FTP\" dir=in action=block protocol=tcp localport=21",
            "alternative": "Enable SFTP (port 22) with SSH key authentication instead"
        }
    },
    22: {  # SSH
        "description": "SSH should be restricted to specific IPs",
        "fixes": {
            "iptables": "sudo iptables -A INPUT -p tcp --dport 22 -s YOUR_IP -j ACCEPT && sudo iptables -A INPUT -p tcp --dport 22 -j DROP",
            "firewalld": "sudo firewall-cmd --permanent --add-rich-rule='rule family=\"ipv4\" source address=\"YOUR_IP\" port protocol=\"tcp\" port=\"22\" accept' && sudo firewall-cmd --reload",
            "ufw": "sudo ufw allow from YOUR_IP to any port 22",
            "windows": "netsh advfirewall firewall add rule name=\"Allow SSH from IP\" dir=in action=allow protocol=tcp localport=22 remoteip=YOUR_IP",
            "additional": "Change default port 22 to non-standard port, disable password auth, use key-only SSH"
        }
    },
    3306: {  # MySQL
        "description": "Database should never be exposed to internet",
        "fixes": {
            "iptables": "sudo iptables -A INPUT -p tcp --dport 3306 -j DROP",
            "firewalld": "sudo firewall-cmd --permanent --remove-port=3306/tcp && sudo firewall-cmd --reload",
            "ufw": "sudo ufw deny 3306",
            "mysql_bind": "Edit /etc/mysql/mysql.conf.d/mysqld.cnf and set bind-address = 127.0.0.1",
            "windows": "netsh advfirewall firewall add rule name=\"Block MySQL\" dir=in action=block protocol=tcp localport=3306",
            "alternative": "Use cloud database service with VPC/subnet isolation instead of exposed port"
        }
    },
    5432: {  # PostgreSQL
        "description": "Database should never be exposed to internet",
        "fixes": {
            "iptables": "sudo iptables -A INPUT -p tcp --dport 5432 -j DROP",
            "firewalld": "sudo firewall-cmd --permanent --remove-port=5432/tcp && sudo firewall-cmd --reload",
            "ufw": "sudo ufw deny 5432",
            "postgresql_bind": "Edit /etc/postgresql/*/main/postgresql.conf and set listen_addresses = 'localhost'",
            "windows": "netsh advfirewall firewall add rule name=\"Block PostgreSQL\" dir=in action=block protocol=tcp localport=5432",
            "alternative": "Use cloud database service or set up SSH tunnel for remote access"
        }
    },
    27017: {  # MongoDB
        "description": "Database should never be exposed to internet (infamous for data breaches)",
        "fixes": {
            "iptables": "sudo iptables -A INPUT -p tcp --dport 27017 -j DROP",
            "firewalld": "sudo firewall-cmd --permanent --remove-port=27017/tcp && sudo firewall-cmd --reload",
            "ufw": "sudo ufw deny 27017",
            "mongodb_bind": "Edit /etc/mongod.conf and set net.bindIp: 127.0.0.1",
            "windows": "netsh advfirewall firewall add rule name=\"Block MongoDB\" dir=in action=block protocol=tcp localport=27017",
            "critical": "Ensure MongoDB authentication is enabled: use_auth: true in mongod.conf"
        }
    },
    3389: {  # RDP
        "description": "RDP should be restricted or disabled",
        "fixes": {
            "windows": "netsh advfirewall firewall add rule name=\"Block RDP\" dir=in action=block protocol=tcp localport=3389",
            "restrict": "Change RDP port, use VPN for access, disable if not needed",
            "additional": "Consider using Bastion hosts or VPN instead of exposing RDP directly"
        }
    }
}


def generate_fix_snippets(
    missing_headers: List[Dict[str, Any]],
    open_ports: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate structured fix snippets for all issues.
    
    Args:
        missing_headers: List of missing security headers
        open_ports: List of open ports
    
    Returns:
        Structured JSON with fixes for Nginx, Apache, and common frameworks
    """
    
    fixes = {
        "headers": [],
        "ports": [],
        "summary": {
            "total_issues": len(missing_headers) + len(open_ports),
            "header_issues": len(missing_headers),
            "port_issues": len(open_ports)
        }
    }
    
    # Generate header fixes
    for header in missing_headers:
        header_name = header.get('name', '')
        if header_name in HEADER_FIXES:
            header_fix = HEADER_FIXES[header_name]
            fixes["headers"].append({
                "header": header_name,
                "description": header_fix["description"],
                "fixes": header_fix["fixes"]
            })
    
    # Generate port closure fixes
    for port_info in open_ports:
        port = port_info['port']
        if port in PORT_CLOSURE_FIXES:
            port_fix = PORT_CLOSURE_FIXES[port]
            fixes["ports"].append({
                "port": port,
                "description": port_fix["description"],
                "fixes": port_fix["fixes"]
            })
    
    return fixes


def get_framework_specific_guidance(framework: str) -> Dict[str, str]:
    """
    Get framework-specific security guidance.
    
    Args:
        framework: Framework name (express, django, flask, etc.)
    
    Returns:
        Framework-specific guidance and best practices
    """
    
    guidance = {
        "express": {
            "security_package": "npm install helmet express-rate-limit express-validator",
            "basic_setup": """
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const app = require('express')();

// Apply security headers
app.use(helmet());

// Apply rate limiting
const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100 });
app.use(limiter);
            """,
            "additional_headers": "helmet automatically adds: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection"
        },
        "django": {
            "security_middleware": "Add 'django.middleware.security.SecurityMiddleware' to MIDDLEWARE",
            "basic_setup": """
# settings.py
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
            """,
            "csp_setup": "pip install django-csp and add 'csp.middleware.CSPMiddleware' to MIDDLEWARE"
        },
        "flask": {
            "security_package": "pip install flask-talisman flask-limiter",
            "basic_setup": """
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask import Flask

app = Flask(__name__)
Talisman(app, force_https=True)
limiter = Limiter(app, key_func=lambda: request.remote_addr)
            """,
            "additional": "flask-talisman automatically handles most security headers"
        },
        "nextjs": {
            "security_headers": "Add to next.config.js: async headers() { return [{ source: '/:path*', headers: [...] }] }",
            "packages": "npm install next-safe",
            "basic_setup": "Use next-safe package or configure headers in next.config.js"
        }
    }
    
    return guidance.get(framework, {"error": f"No guidance available for {framework}"})
