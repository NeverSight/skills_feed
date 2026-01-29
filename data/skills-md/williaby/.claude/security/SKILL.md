---
name: security
description: Security validation, vulnerability scanning, and compliance checking for development environments. Auto-activates on keywords security, vulnerability, audit, OWASP, encryption, GPG, SSH, signing, secrets, scan. Routes to specialized security workflows.
allowed-tools: Read, Bash(gpg:*, ssh:*, git:*, safety:*, bandit:*), Grep, Task
---

# Security Skill

Comprehensive security domain for development environment validation, vulnerability scanning, and security compliance. Provides automated security workflows with intelligent routing based on user intent.

## Auto-Activation Keywords

This skill activates automatically when you mention:
- **General**: security, secure, vulnerability, vulnerabilities
- **Validation**: validate security, security check, environment security
- **Scanning**: scan, security scan, vulnerability scan, dependency scan
- **Encryption**: encrypt, decrypt, GPG, PGP, secrets
- **Signing**: sign commits, SSH key, GPG key, signed commits
- **Compliance**: OWASP, audit, security audit, compliance
- **Tools**: safety, bandit, semgrep, security tools

## Routing Logic

Based on user intent, this skill routes to appropriate workflows:

### Environment Validation
**Keywords**: "validate security", "check security environment", "security setup", "GPG key", "SSH key"
- **Simple validation** → Use `/security/validate-env` workflow
- **Comprehensive audit** → Invoke `security-auditor` agent

### Vulnerability Scanning
**Keywords**: "scan dependencies", "security scan", "vulnerability check", "safety check", "bandit"
- **Dependency scanning** → Use `/security/scan` workflow
- **Full security audit** → Invoke `security-auditor` agent

### File Encryption
**Keywords**: "encrypt", "decrypt", "GPG encrypt", "protect secrets", "encrypt .env"
- **File encryption/decryption** → Use `/security/encrypt` workflow
- **Secrets management review** → Invoke `security-auditor` agent

### Security Audit
**Keywords**: "security audit", "penetration test", "threat assessment", "vulnerability assessment"
- **Complex security audit** → Invoke `security-auditor` agent directly
- **Compliance validation** → Use workflows + agent for comprehensive review

## Workflow Quick Reference

```bash
# Validate security environment
/security/validate-env [--verbose]

# Scan for vulnerabilities
/security/scan [--type=dependencies|code|all]

# Encrypt/decrypt files
/security/encrypt [file-path]
/security/decrypt [file-path]
```

## Complex Task Delegation

For comprehensive security analysis, invoke the `security-auditor` agent via Task tool:

```
Use security-auditor agent when:
- Conducting full security audits across multiple components
- Threat modeling and risk assessment
- Compliance validation against security standards
- Penetration testing simulation
- Security architecture review
```

## Supporting Context

- **OWASP Top 10**: See `context/owasp-top-10.md` for common vulnerabilities
- **Security commands**: See `context/security-commands.md` for comprehensive command reference
- **Security standards**: See `/standards/security.md` for project requirements

## Integration Points

### Agents
- **security-auditor**: Comprehensive security audits and vulnerability assessment
- **test-engineer**: Security testing integration (via testing/workflows/security.md)

### MCP Tools
- **mcp__zen-core__chat**: Multi-model consensus for security decisions

### Hooks
- **Pre-commit**: Security validation on file changes
- **Post-tool-use**: MCP usage tracking

### Standards
- Security standards: `/standards/security.md` (GPG/SSH requirements, encrypted secrets)
- Git workflow: `/standards/git-workflow.md` (signed commits requirement)

## Security Requirements Summary

**Required for all projects:**
- GPG key configured (for .env encryption)
- SSH key configured and loaded (for signed commits)
- Git signing enabled (commit.gpgsign = true)
- No secrets in repository (use encrypted .env files)
- Dependency scanning (safety check passes)
- Static analysis (bandit passes)

**Git signing configuration:**
```bash
# SSH signing (recommended)
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global commit.gpgsign true

# Or GPG signing
git config --global user.signingkey <GPG_KEY_ID>
git config --global commit.gpgsign true
```

**Dependency scanning:**
```bash
# Check Python dependencies
poetry run safety check --full-report

# Static security analysis
poetry run bandit -r src
```

**Secrets encryption:**
```bash
# Encrypt .env file
gpg --symmetric --cipher-algo AES256 .env

# Decrypt .env file
gpg --decrypt .env.gpg > .env
```

## Examples

**Example 1: Validate security environment**
```
User: "Can you check if my security environment is properly configured?"
→ Security skill auto-activates
→ Routes to /security/validate-env workflow
→ Validates GPG keys, SSH keys, Git signing, environment setup
```

**Example 2: Scan for vulnerabilities**
```
User: "Scan my project for security vulnerabilities"
→ Security skill auto-activates
→ Routes to /security/scan workflow
→ Runs safety check and bandit analysis
→ Reports vulnerabilities with remediation steps
```

**Example 3: Comprehensive security audit**
```
User: "Perform a comprehensive security audit of the authentication system"
→ Security skill auto-activates
→ Invokes security-auditor agent
→ Agent performs:
  - Threat modeling
  - Vulnerability assessment
  - Code review for security issues
  - Compliance validation
  - Risk-prioritized recommendations
```

**Example 4: Encrypt sensitive file**
```
User: "Encrypt my .env file with GPG"
→ Security skill auto-activates
→ Routes to /security/encrypt workflow
→ Encrypts file with AES256
→ Provides decryption instructions
```

---

*This skill consolidates check-security-env skill and security commands into a unified security domain with intelligent routing.*
