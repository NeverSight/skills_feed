---
name: security
description: Use this skill when doing security reviews, penetration testing, threat modeling, compliance work, or incident response. Activates on mentions of security audit, vulnerability, penetration test, pentest, OWASP, CVE, security review, threat model, zero trust, SOC 2, HIPAA, GDPR, compliance, incident response, SBOM, supply chain security, secrets management, or authentication security.
---

# Security Operations

Secure systems from design through deployment and incident response.

## Quick Reference

### Security Architecture Principles

**Zero Trust Model:**

1. Never trust, always verify
2. Assume breach
3. Verify explicitly
4. Least privilege access
5. Micro-segmentation

**SLSA Framework (Supply Chain):**

- Level 1: Documentation
- Level 2: Hosted build, signed provenance
- Level 3: Hardened builds, 2-person review
- Level 4: Hermetic, reproducible builds

### Threat Modeling (STRIDE)

| Threat                     | Example             | Mitigation                  |
| -------------------------- | ------------------- | --------------------------- |
| **S**poofing               | Fake identity       | Strong auth, MFA            |
| **T**ampering              | Modified data       | Integrity checks, signing   |
| **R**epudiation            | Deny actions        | Audit logs, non-repudiation |
| **I**nformation Disclosure | Data leak           | Encryption, access control  |
| **D**enial of Service      | Overload            | Rate limiting, scaling      |
| **E**levation of Privilege | Unauthorized access | Least privilege, RBAC       |

### Code Security Review Checklist

```markdown
## OWASP Top 10 (2021)

- [ ] A01: Broken Access Control
- [ ] A02: Cryptographic Failures
- [ ] A03: Injection (SQL, NoSQL, OS, LDAP)
- [ ] A04: Insecure Design
- [ ] A05: Security Misconfiguration
- [ ] A06: Vulnerable Components
- [ ] A07: Auth Failures
- [ ] A08: Software/Data Integrity Failures
- [ ] A09: Logging/Monitoring Failures
- [ ] A10: SSRF
```

### Secrets Management

**Never commit secrets.** Use environment-based injection:

```yaml
# Kubernetes External Secrets
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: api-keys
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: api-keys
  data:
    - secretKey: OPENAI_API_KEY
      remoteRef:
        key: secret/data/api-keys
        property: openai
```

### SBOM Generation

```bash
# Generate SBOM with Syft
syft packages dir:. -o spdx-json > sbom.spdx.json

# Scan for vulnerabilities with Grype
grype sbom:sbom.spdx.json --fail-on high
```

### Container Security

```dockerfile
# Secure Dockerfile patterns
FROM cgr.dev/chainguard/node:latest AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM cgr.dev/chainguard/node:latest
WORKDIR /app
COPY --from=build /app/node_modules ./node_modules
COPY . .
USER nonroot
CMD ["node", "server.js"]
```

**Scan images:**

```bash
trivy image myapp:latest --severity HIGH,CRITICAL
```

### Runtime Security (eBPF)

**Tetragon** for kernel-level enforcement:

```yaml
apiVersion: cilium.io/v1alpha1
kind: TracingPolicy
metadata:
  name: sensitive-file-access
spec:
  kprobes:
    - call: "fd_install"
      selectors:
        - matchArgs:
            - index: 1
              operator: "Prefix"
              values: ["/etc/shadow", "/etc/passwd"]
      action: NotifyEnforcer
```

**Falco** for threat detection:

```yaml
- rule: Shell Spawned in Container
  desc: Detect shell spawned in a container
  condition: >
    spawned_process and container and
    proc.name in (shell_binaries)
  output: >
    Shell spawned in container
    (user=%user.name container=%container.name shell=%proc.name)
  priority: WARNING
```

### Compliance Automation

**Vanta/Drata Integration:**

- Continuous monitoring of 35+ frameworks
- Automated evidence collection
- Risk flagging and remediation tracking

**Key Frameworks:**

- SOC 2 Type II
- ISO 27001
- HIPAA
- GDPR
- PCI DSS

### Incident Response Playbook

```markdown
## Phase 1: Detection & Analysis (MTTD < 5 min)

1. Alert triggered → Acknowledge in SOAR
2. Gather initial IOCs (IPs, hashes, usernames)
3. Determine scope and severity
4. Escalate if P1/P2

## Phase 2: Containment (MTTR < 1 hour)

1. Isolate affected systems
2. Block malicious IPs/domains
3. Disable compromised accounts
4. Preserve evidence (disk images, logs)

## Phase 3: Eradication

1. Remove malware/backdoors
2. Patch vulnerabilities
3. Reset credentials
4. Verify clean state

## Phase 4: Recovery

1. Restore from clean backups
2. Monitor for re-infection
3. Gradual service restoration
4. Validate functionality

## Phase 5: Lessons Learned

1. Timeline reconstruction
2. Root cause analysis
3. Update playbooks
4. Security improvements
```

### Penetration Testing Checklist

```markdown
## Reconnaissance

- [ ] DNS enumeration
- [ ] Subdomain discovery
- [ ] Port scanning
- [ ] Service fingerprinting

## Web Application

- [ ] Authentication bypass
- [ ] Session management
- [ ] Input validation
- [ ] Access control
- [ ] Business logic

## Infrastructure

- [ ] Network segmentation
- [ ] Privilege escalation
- [ ] Lateral movement
- [ ] Data exfiltration paths
```

## Agents

- **security-architect** - Threat modeling, secure design, compliance
- **incident-responder** - Incident handling, forensics, recovery

## Deep Dives

- [references/zero-trust.md](references/zero-trust.md)
- [references/sbom-slsa.md](references/sbom-slsa.md)
- [references/ebpf-security.md](references/ebpf-security.md)
- [references/incident-response.md](references/incident-response.md)

## Examples

- [examples/security-pipeline/](examples/security-pipeline/)
- [examples/tetragon-policies/](examples/tetragon-policies/)
- [examples/compliance-checks/](examples/compliance-checks/)
