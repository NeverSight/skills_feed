---
name: web-security
description: Exploits web application vulnerabilities. Use when working with SQL injection, XSS, SSRF, SSTI, command injection, path traversal, authentication bypass, deserialization, or any web-based CTF challenge.
allowed-tools: Bash, Read, Write, Grep, Glob
---

# Web Security Skill

## Quick Workflow

```
Progress:
- [ ] Identify technology stack
- [ ] Check common files (robots.txt, .git)
- [ ] Test injection points (SQLi, XSS, SSTI)
- [ ] Check authentication/session flaws
- [ ] Develop exploit
- [ ] Extract flag
```

## Quick Recon

```bash
# Directory enumeration
gobuster dir -u http://target -w /usr/share/wordlists/dirb/common.txt
ffuf -u http://target/FUZZ -w wordlist.txt

# Technology detection
whatweb http://target
curl -I http://target

# Check robots.txt, .git exposure
curl http://target/robots.txt
curl http://target/.git/HEAD
```

## Vulnerability Reference

| Vulnerability | Reference File |
|--------------|----------------|
| SQL Injection | [reference/sqli.md](reference/sqli.md) |
| XSS | [reference/xss.md](reference/xss.md) |
| SSTI | [reference/ssti.md](reference/ssti.md) |
| Command Injection | [reference/command-injection.md](reference/command-injection.md) |
| SSRF / Path Traversal | [reference/ssrf-lfi.md](reference/ssrf-lfi.md) |
| Auth Bypass / Deserialization | [reference/auth-deser.md](reference/auth-deser.md) |

## Tools Quick Reference

| Tool | Purpose | Command |
|------|---------|---------|
| sqlmap | SQLi automation | `sqlmap -u URL --dbs` |
| commix | Command injection | `commix -u URL` |
| tplmap | SSTI automation | `tplmap -u URL` |
| ffuf | Fuzzing | `ffuf -u URL/FUZZ -w wordlist` |
| Burp Suite | Proxy/intercept | GUI |
| jwt_tool | JWT attacks | `jwt_tool TOKEN` |
