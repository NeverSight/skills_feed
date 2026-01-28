---
name: security
description: Production-grade security testing skill with OWASP Top 10, vulnerability scanning, penetration testing guidance, and compliance validation
sasmp_version: "1.3.0"
bonded_agent: qa-expert
bond_type: PRIMARY_BOND
version: "2.1.0"
---

# Security Testing Skill

## Overview

Enterprise-grade security testing capabilities covering OWASP Top 10, vulnerability assessment, and compliance validation with actionable remediation guidance.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "action": {
      "type": "string",
      "enum": ["scan", "analyze", "remediate", "compliance_check", "generate_report"],
      "description": "Security action to perform"
    },
    "scan_type": {
      "type": "string",
      "enum": ["owasp_top10", "dependency", "sast", "dast", "secrets", "configuration"],
      "description": "Type of security scan"
    },
    "target": {
      "type": "object",
      "properties": {
        "url": {"type": "string", "format": "uri"},
        "repository": {"type": "string"},
        "file_path": {"type": "string"},
        "docker_image": {"type": "string"}
      }
    },
    "compliance": {
      "type": "string",
      "enum": ["owasp", "pci_dss", "hipaa", "gdpr", "soc2", "iso27001"]
    },
    "severity_filter": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low", "all"],
      "default": "all"
    }
  },
  "required": ["action"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "status": {"type": "string", "enum": ["success", "partial", "failed"]},
    "vulnerabilities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "severity": {"type": "string"},
          "category": {"type": "string"},
          "description": {"type": "string"},
          "location": {"type": "string"},
          "remediation": {"type": "string"},
          "references": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "critical": {"type": "integer"},
        "high": {"type": "integer"},
        "medium": {"type": "integer"},
        "low": {"type": "integer"},
        "total": {"type": "integer"}
      }
    },
    "compliance_status": {"type": "string", "enum": ["pass", "fail", "partial"]},
    "recommendations": {"type": "array", "items": {"type": "string"}}
  }
}
```

## Parameter Validation

```yaml
target.url:
  required: false
  validate:
    - type: format
      pattern: "^https?://"
    - type: authorization_check
      require: explicit_consent

scan_type:
  required: false
  default: owasp_top10
  validate:
    - type: enum
      values: [owasp_top10, dependency, sast, dast, secrets, configuration]
    - type: tool_availability_check

compliance:
  required: false
  validate:
    - type: enum
      values: [owasp, pci_dss, hipaa, gdpr, soc2, iso27001]
```

## Error Handling

```yaml
retry_config:
  strategy: exponential_backoff
  max_retries: 3
  base_delay_ms: 2000
  max_delay_ms: 30000
  retryable_errors:
    - SCAN_TIMEOUT
    - TARGET_TEMPORARILY_UNAVAILABLE
    - RATE_LIMITED

error_categories:
  authorization_errors:
    - NO_CONSENT
    - SCOPE_EXCEEDED
    - UNAUTHORIZED_TARGET
    recovery: require_explicit_authorization

  scan_errors:
    - SCAN_TIMEOUT
    - PARTIAL_SCAN
    - TOOL_UNAVAILABLE
    recovery: retry_or_fallback_tool

  target_errors:
    - TARGET_UNREACHABLE
    - INVALID_TARGET
    - WAF_BLOCKED
    recovery: verify_target_access

  compliance_errors:
    - UNKNOWN_STANDARD
    - MISSING_CONTROLS
    - INCOMPLETE_ASSESSMENT
    recovery: manual_review_required
```

## OWASP Top 10 (2021) Coverage

### A01: Broken Access Control
```yaml
tests:
  - Horizontal privilege escalation
  - Vertical privilege escalation
  - Insecure direct object references
  - Missing function level access control
  - CORS misconfiguration

detection_methods:
  - Access matrix testing
  - Role-based testing
  - URL manipulation
  - API endpoint enumeration

remediation:
  - Implement proper authorization checks
  - Use deny-by-default
  - Enforce ownership validation
  - Log access control failures
```

### A02: Cryptographic Failures
```yaml
tests:
  - Weak encryption algorithms
  - Hardcoded secrets
  - Insufficient key length
  - Missing TLS
  - Improper certificate validation

detection_methods:
  - SSL/TLS analysis
  - Code review for crypto usage
  - Secret scanning
  - Traffic analysis

remediation:
  - Use modern encryption (AES-256, RSA-2048+)
  - Implement proper key management
  - Enforce TLS 1.2+
  - Rotate secrets regularly
```

### A03: Injection
```yaml
tests:
  - SQL injection
  - NoSQL injection
  - OS command injection
  - LDAP injection
  - XPath injection

detection_methods:
  - Input fuzzing
  - SAST analysis
  - Parameterized query check
  - Error message analysis

remediation:
  - Use parameterized queries
  - Input validation/sanitization
  - Least privilege database accounts
  - WAF rules
```

### A04-A10 (Continued)
```yaml
A04_insecure_design:
  - Threat modeling
  - Security requirements review
  - Architecture analysis

A05_security_misconfiguration:
  - Default credentials check
  - Unnecessary features enabled
  - Missing security headers
  - Verbose error messages

A06_vulnerable_components:
  - Dependency scanning
  - CVE database check
  - License compliance

A07_authentication_failures:
  - Brute force testing
  - Session management
  - Password policy
  - MFA implementation

A08_integrity_failures:
  - CI/CD security
  - Unsigned updates
  - Deserialization issues

A09_logging_failures:
  - Log injection
  - Sensitive data in logs
  - Insufficient logging

A10_ssrf:
  - Internal network access
  - Cloud metadata access
  - URL validation bypass
```

## Security Test Templates

### SQL Injection Test
```python
# sql_injection_test.py
import requests
from typing import List, Dict

PAYLOADS = [
    "' OR '1'='1",
    "' OR '1'='1' --",
    "' UNION SELECT NULL--",
    "1; DROP TABLE users--",
    "' AND 1=1--",
    "' AND 1=2--",
]

def test_sql_injection(url: str, param: str) -> List[Dict]:
    findings = []

    for payload in PAYLOADS:
        try:
            response = requests.get(
                url,
                params={param: payload},
                timeout=10
            )

            # Check for SQL error indicators
            error_indicators = [
                "sql syntax",
                "mysql_fetch",
                "sqlite_",
                "ORA-",
                "PostgreSQL",
            ]

            for indicator in error_indicators:
                if indicator.lower() in response.text.lower():
                    findings.append({
                        "vulnerability": "SQL Injection",
                        "severity": "CRITICAL",
                        "payload": payload,
                        "indicator": indicator,
                        "url": url,
                        "parameter": param
                    })
                    break

        except requests.exceptions.RequestException as e:
            continue

    return findings
```

### XSS Test
```javascript
// xss_test.js
const XSS_PAYLOADS = [
  '<script>alert(1)</script>',
  '<img src=x onerror=alert(1)>',
  '<svg onload=alert(1)>',
  'javascript:alert(1)',
  '"><script>alert(1)</script>',
];

async function testXSS(url, param) {
  const findings = [];

  for (const payload of XSS_PAYLOADS) {
    const testUrl = `${url}?${param}=${encodeURIComponent(payload)}`;

    const response = await fetch(testUrl);
    const body = await response.text();

    // Check if payload is reflected without encoding
    if (body.includes(payload)) {
      findings.push({
        vulnerability: 'Reflected XSS',
        severity: 'HIGH',
        payload,
        url,
        parameter: param
      });
    }
  }

  return findings;
}
```

## Troubleshooting

### Issue: False Positives
```yaml
symptoms:
  - High volume of low-quality findings
  - Legitimate features flagged
  - WAF rules triggered

diagnosis:
  1. Review scan configuration
  2. Analyze finding context
  3. Compare with manual testing
  4. Check scan scope

solutions:
  - Tune scan sensitivity
  - Add false positive exclusions
  - Use authenticated scanning
  - Combine with manual review
```

### Issue: Incomplete Coverage
```yaml
symptoms:
  - Known vulnerabilities missed
  - Low finding count
  - Scan completed too quickly

diagnosis:
  1. Check scan depth configuration
  2. Review authentication state
  3. Analyze crawl coverage
  4. Check for scan blocks

solutions:
  - Increase scan depth
  - Provide valid credentials
  - Whitelist scanner IP
  - Use multiple scan tools
```

### Issue: Scan Blocked
```yaml
symptoms:
  - Connection refused
  - Rate limited
  - WAF blocks

diagnosis:
  1. Check firewall rules
  2. Review rate limiting
  3. Analyze WAF logs
  4. Verify authorization

solutions:
  - Whitelist scanner IP
  - Reduce scan intensity
  - Configure WAF bypass
  - Use internal scanning
```

## Compliance Mapping

```yaml
pci_dss:
  requirement_6_5: OWASP_Top_10
  requirement_6_6: WAF_or_code_review
  requirement_11_3: Penetration_testing

gdpr:
  article_32: Security_measures
  article_35: Impact_assessment

soc2:
  cc6_1: Logical_access
  cc6_6: System_boundaries
  cc6_7: Change_management
```

## Best Practices

```yaml
scanning:
  - Always get authorization
  - Start with passive scanning
  - Use authenticated scans
  - Schedule during low traffic

remediation:
  - Prioritize by risk score
  - Fix critical issues first
  - Verify fixes with retest
  - Document all changes

continuous_security:
  - Integrate in CI/CD
  - Regular dependency updates
  - Security code review
  - Bug bounty program
```

## Logging & Observability

```yaml
log_events:
  - scan_started
  - vulnerability_found
  - scan_completed
  - remediation_verified

metrics:
  - vulnerabilities_by_severity
  - mean_time_to_remediate
  - scan_coverage_percentage
  - compliance_score

alerts:
  - critical_vulnerability_found
  - compliance_threshold_breached
  - scan_failure
```

## Ethical Guidelines

```yaml
authorization:
  - Always obtain written consent
  - Define scope clearly
  - Respect boundaries
  - Report all findings

responsible_disclosure:
  - Follow disclosure timeline
  - Work with vendor on fixes
  - Protect user data
  - Document everything
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.1.0 | 2025-01 | Production-grade with OWASP 2021 |
| 2.0.0 | 2024-12 | SASMP v1.3.0 compliance |
| 1.0.0 | 2024-11 | Initial release |
