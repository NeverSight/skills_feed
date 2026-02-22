---
name: security-compliance
description: Implement security scanning, vulnerability detection, and compliance checks. Use when working with security audits, dependency vulnerabilities, secret detection, CodeQL scanning, SAST/DAST tools, or security best practices. Handles threat modeling and security hardening.
---

# Security & Compliance Guardian

## Mission
Maintain and enhance security posture for Brainarr through comprehensive scanning, vulnerability management, and compliance monitoring.

## Current Security Infrastructure
- ✅ **CodeQL Scanning**: Automated C# security analysis
- ✅ **Secret Detection**: Pre-commit hooks + GitLeaks
- ✅ **Dependency Scanning**: Dependabot automated updates
- ✅ **SBOM Generation**: Software Bill of Materials in releases
- ✅ **Artifact Signing**: Cosign keyless signing

## Expertise Areas

### 1. Static Application Security Testing (SAST)
- CodeQL query customization for C# and .NET
- Security code review automation
- Vulnerability pattern detection (injection, XSS, etc.)
- False positive management and suppression

### 2. Dependency Security
- Dependabot configuration optimization
- Vulnerability remediation strategies
- Supply chain attack prevention
- License compliance checking

### 3. Secret Management
- Credential scanning (GitLeaks, TruffleHog)
- Environment variable security
- Secrets rotation policies
- API key protection strategies

### 4. Container Security (Future)
- Image vulnerability scanning (Trivy, Grype)
- Base image hardening
- Runtime security monitoring
- Registry security policies

### 5. Compliance & Auditing
- SBOM generation and management
- Security audit trails
- Compliance reporting (OWASP, CWE)
- Penetration testing coordination

## Enhancement Opportunities
1. **Dynamic Analysis**: Add DAST for runtime vulnerability detection
2. **Container Scanning**: Scan Docker images when published
3. **Secrets Rotation**: Automate API key rotation
4. **Security Dashboards**: Centralized security metrics
5. **Threat Modeling**: Regular security architecture reviews

## Security Best Practices

### Code Security
- Input validation on all external data
- Parameterized queries (no SQL injection)
- Output encoding (prevent XSS)
- Secure cryptographic operations
- No hardcoded secrets

### Dependency Management
- Pin dependency versions
- Regular security updates
- Monitor transitive dependencies
- Review dependency changes in PRs

### API Security
- Authentication required for AI providers
- API key encryption at rest
- Rate limiting to prevent abuse
- Request/response validation

## Security Checklist
- [ ] No hardcoded secrets in code
- [ ] All dependencies up-to-date
- [ ] CodeQL findings addressed
- [ ] SBOM generated for releases
- [ ] Artifacts signed and verified
- [ ] Security advisories monitored
- [ ] Incident response plan documented
- [ ] Third-party audits completed

## Related Skills
- `code-quality` - Security is quality
- `release-automation` - Secure release processes
- `observability` - Security monitoring

## Examples

### Example 1: Review Security Scan Results
**User**: "Check the CodeQL findings and fix critical issues"
**Action**: Review security alerts, prioritize by severity, fix vulnerabilities, add suppressions for false positives

### Example 2: Update Vulnerable Dependency
**User**: "Dependabot found a critical vulnerability in Newtonsoft.Json"
**Action**: Review vulnerability details, test compatibility, update version, verify tests pass, merge PR

### Example 3: Implement Secret Scanning
**User**: "Add secret scanning to prevent API key leaks"
**Action**: Configure GitLeaks, add .gitleaks.toml, create pre-commit hooks, scan history, document process
