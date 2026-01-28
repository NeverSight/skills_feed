---
name: Security
description: Python security best practices, OWASP, and vulnerability prevention
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 07-best-practices
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: vulnerability_count
---

# Python Security Skill

## Overview
Implement secure Python code practices and protect applications from common vulnerabilities.

## Topics Covered

### Common Vulnerabilities
- SQL injection prevention
- Command injection
- Path traversal
- Deserialization attacks
- SSRF vulnerabilities

### Secure Coding
- Input validation
- Output encoding
- Secure file handling
- Secrets management
- Environment variables

### Authentication
- Password hashing (bcrypt, argon2)
- JWT implementation
- Session security
- OAuth integration
- API key management

### Dependency Security
- pip audit usage
- Safety scanner
- Snyk for Python
- Dependabot setup
- Vulnerability databases

### Security Testing
- Bandit static analysis
- Security unit tests
- Penetration testing basics
- SAST/DAST tools
- Code review checklist

## Prerequisites
- Python fundamentals
- Web development basics

## Learning Outcomes
- Write secure Python code
- Prevent common attacks
- Audit dependencies
- Implement authentication securely
