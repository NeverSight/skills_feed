---
name: "Python Security Scan"
description: "Comprehensive security vulnerability scanner for Python projects including Flask, Django, and FastAPI applications. Detects OWASP Top 10 vulnerabilities, injection flaws, insecure deserialization, authentication issues, hardcoded secrets, and framework-specific security problems. Audits dependencies for known CVEs and generates actionable security reports."
---

# Python Security Scan Skill

This skill enables comprehensive security scanning of Python projects based on OWASP guidelines, Python security best practices, and framework-specific vulnerabilities.

## When to Use This Skill

- Security audits of Python applications
- Code review for security vulnerabilities
- Pre-deployment security checks
- Dependency vulnerability assessment
- Detecting hardcoded secrets and credentials
- Framework-specific security reviews (Flask, Django, FastAPI)

## Supported Frameworks

This skill automatically detects and applies framework-specific checks for:

- **Flask** - Template injection, session security, CORS, extensions
- **Django** - ORM injection, CSRF, template security, settings
- **FastAPI** - Dependency injection, Pydantic validation, OAuth2
- **General Python** - Core language vulnerabilities applicable to all projects

## Scan Types

### 1. Quick Scan
Fast scan focusing on critical vulnerabilities:
- Hardcoded secrets, API keys, and credentials
- Dangerous function usage (`eval`, `exec`, `pickle.loads`)
- Command injection via `subprocess`, `os.system`
- SQL injection patterns
- Known vulnerable dependencies

### 2. Full Scan
Comprehensive security assessment covering:
- All OWASP Top 10:2025 categories
- Python-specific vulnerabilities
- Framework-specific security issues
- Injection vulnerabilities (SQL, NoSQL, Command, LDAP)
- Insecure deserialization
- Authentication and authorization flaws
- Cryptographic failures
- Security misconfigurations
- Dependency audit (CVE check)
- Environment variable and secrets exposure

### 3. Targeted Scan
Focus on specific vulnerability categories:
- `--injection` - SQL/NoSQL/Command/LDAP injection
- `--deserialization` - Pickle, YAML, JSON deserialization
- `--auth` - Authentication/authorization issues
- `--secrets` - Hardcoded credentials
- `--deps` - Dependency vulnerabilities
- `--crypto` - Cryptographic issues
- `--flask` - Flask-specific vulnerabilities
- `--django` - Django-specific vulnerabilities
- `--fastapi` - FastAPI-specific vulnerabilities

## Scan Procedure

### Step 1: Project Discovery
1. Identify project type and framework:
   - Check for `requirements.txt`, `Pipfile`, `pyproject.toml`, `setup.py`
   - Detect Flask (`from flask import`), Django (`django.conf`), FastAPI (`from fastapi import`)
2. Locate configuration files
3. Map the codebase structure

### Step 2: Framework Detection
```python
# Detection patterns
Flask: "from flask import", "Flask(__name__)"
Django: "django.conf.settings", "INSTALLED_APPS", "manage.py"
FastAPI: "from fastapi import", "FastAPI()"
```

### Step 3: Dependency Audit
Run the dependency audit script:
```bash
./scripts/dependency-audit.sh /path/to/project
```
Or manually:
```bash
pip-audit
# or
safety check
```

### Step 4: Secret Scanning
Scan for hardcoded secrets:
```bash
python scripts/secret-scanner.py /path/to/project
```

**Important: Environment File Handling**
- By default, real `.env` files are **SKIPPED** (`.env`, `.env.local`, `.env.production`, etc.)
- These files contain actual secrets and should not be in version control
- Only `.env.example` and `.env.template` files are analyzed for documentation quality
- Use `--include-env-files` flag only if explicitly requested by user

The scanner will:
1. Scan source code for hardcoded secrets
2. Analyze `.env.example` templates to check:
   - Which sensitive variables are documented
   - Whether variables have descriptions (comments)
   - If placeholder values look like real secrets
   - Suggestions for missing common variables (SECRET_KEY, DATABASE_URL, etc.)

### Step 5: Pattern Analysis
For each file in the codebase, check against patterns in:
- `references/python-vulnerabilities.md` - Core Python issues
- `references/injection-patterns.md` - Injection flaws
- `references/deserialization.md` - Insecure deserialization
- `references/flask-security.md` - Flask vulnerabilities
- `references/django-security.md` - Django vulnerabilities
- `references/fastapi-security.md` - FastAPI vulnerabilities

### Step 6: Report Generation
Generate a security report using:
- `assets/report-template.md` - Report structure

## Severity Classification

| Severity | Description | Action Required |
|----------|-------------|-----------------|
| CRITICAL | Exploitable vulnerability with severe impact | Immediate fix required |
| HIGH | Significant security risk | Fix before deployment |
| MEDIUM | Potential security issue | Fix in next release |
| LOW | Minor security concern | Consider fixing |
| INFO | Security best practice suggestion | Optional improvement |

## Key Files to Scan

### Always Check
- `**/*.py` - All Python source files
- `requirements.txt`, `Pipfile`, `pyproject.toml` - Dependencies
- `setup.py`, `setup.cfg` - Package configuration
- `config.py`, `settings.py` - Configuration files
- `**/secrets*`, `**/credentials*` - Obvious secret locations

### Environment Files
- `.env.example`, `.env.template` - **SCAN** for template analysis
- `.env`, `.env.local`, `.env.production` - **SKIP** by default (contain real secrets)

**Note:** Real `.env` files should never be committed to version control. The scanner analyzes `.env.example` templates to ensure proper documentation of required variables.

### High Priority Locations
- `app.py`, `main.py`, `wsgi.py` - Entry points
- `**/views.py`, `**/routes.py` - Request handlers
- `**/api/**/*.py` - API endpoints
- `**/auth*`, `**/login*` - Authentication code
- `**/models.py` - Database models
- `**/serializers.py` - Data serialization
- `**/middleware.py` - Middleware code

### Framework-Specific
**Flask:**
- `app.py`, `__init__.py` - Application factory
- `**/blueprints/**` - Blueprint routes
- `templates/**` - Jinja2 templates

**Django:**
- `settings.py`, `**/settings/*.py` - Django settings
- `urls.py` - URL configuration
- `**/views.py` - View functions/classes
- `**/forms.py` - Form definitions
- `templates/**` - Django templates

**FastAPI:**
- `main.py` - Application entry
- `**/routers/**` - API routers
- `**/dependencies.py` - Dependency injection
- `**/schemas.py` - Pydantic models

## Output Format

Findings should be reported as:

```
[SEVERITY] Category: Description
  File: path/to/file.py:lineNumber
  Code: <relevant code snippet>
  Risk: <explanation of the security risk>
  Fix: <recommended remediation>
```

## Integration with CI/CD

This skill can generate output compatible with:
- GitHub Security Advisories
- SARIF format for GitHub Code Scanning
- JSON for custom integrations
- JUnit XML for CI pipelines

## References

Load additional context as needed:
- `references/owasp-top-10.md` - OWASP Top 10:2025 quick reference
- `references/python-vulnerabilities.md` - Python-specific vulnerabilities
- `references/injection-patterns.md` - Injection vulnerability patterns
- `references/deserialization.md` - Insecure deserialization patterns
- `references/flask-security.md` - Flask security guide
- `references/django-security.md` - Django security guide
- `references/fastapi-security.md` - FastAPI security guide
