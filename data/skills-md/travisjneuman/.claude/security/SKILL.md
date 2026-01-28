---
name: security
description: Information security expertise for cybersecurity frameworks (NIST, ISO 27001), security architecture, incident response, vulnerability management, identity management, and cloud security. Use when designing security programs, responding to incidents, or assessing vulnerabilities.
---

# Information Security Expert

Comprehensive security frameworks for cybersecurity, incident response, and security architecture.

## Security Architecture

### Zero Trust Architecture

```
ZERO TRUST PRINCIPLES:
- Never trust, always verify
- Assume breach
- Verify explicitly
- Least privilege access
- Micro-segmentation

ZERO TRUST COMPONENTS:

IDENTITY:
- Strong authentication (MFA)
- Identity governance
- Privileged access management
- Continuous validation

DEVICES:
- Device health verification
- Endpoint detection and response
- Mobile device management
- Asset inventory

NETWORK:
- Micro-segmentation
- Software-defined perimeter
- Encrypted communications
- Network access control

APPLICATIONS:
- Application-level authentication
- API security
- Web application firewall
- Secure coding practices

DATA:
- Data classification
- Encryption at rest and in transit
- Data loss prevention
- Access controls
```

### Defense in Depth

```
SECURITY LAYERS:

PHYSICAL:
- Data center security
- Badge access
- Surveillance
- Environmental controls

PERIMETER:
- Firewalls
- IDS/IPS
- DMZ
- VPN

NETWORK:
- Segmentation
- Encryption
- Network monitoring
- NAC

HOST:
- Endpoint protection
- Host-based firewall
- Hardening
- Patch management

APPLICATION:
- WAF
- Secure coding
- Input validation
- Authentication

DATA:
- Encryption
- DLP
- Access controls
- Backup/recovery
```

### Cloud Security

| Domain         | Controls                            |
| -------------- | ----------------------------------- |
| **Identity**   | SSO, MFA, PAM, IAM policies         |
| **Compute**    | Hardened images, container security |
| **Network**    | VPC, security groups, WAF           |
| **Storage**    | Encryption, access policies, backup |
| **Logging**    | CloudTrail, SIEM integration        |
| **Compliance** | Config rules, automated remediation |

For detailed security frameworks (NIST, ISO 27001, CIS Controls, MITRE ATT&CK), see [Security Frameworks Reference](references/security-frameworks.md).

## Vulnerability Management

### Vulnerability Management Process

```
LIFECYCLE:

1. DISCOVERY
   - Asset inventory
   - Vulnerability scanning
   - Penetration testing
   - Code analysis

2. PRIORITIZATION
   - CVSS scoring
   - Asset criticality
   - Exploit availability
   - Business context

3. REMEDIATION
   - Patch management
   - Configuration changes
   - Compensating controls
   - Risk acceptance

4. VERIFICATION
   - Rescan
   - Validation testing
   - Documentation
   - Reporting

5. REPORTING
   - Executive dashboards
   - Trend analysis
   - Compliance reporting
   - SLA tracking
```

### CVSS Scoring

| Score    | Severity | SLA Target  |
| -------- | -------- | ----------- |
| 9.0-10.0 | Critical | 7 days      |
| 7.0-8.9  | High     | 30 days     |
| 4.0-6.9  | Medium   | 90 days     |
| 0.1-3.9  | Low      | Best effort |

### Patch Management

```
PATCH PROCESS:

1. IDENTIFICATION
   - Vendor announcements
   - Vulnerability feeds
   - Security bulletins

2. ASSESSMENT
   - Applicability
   - Risk evaluation
   - Test requirements

3. TESTING
   - Lab validation
   - Compatibility testing
   - Rollback planning

4. DEPLOYMENT
   - Pilot group
   - Phased rollout
   - Monitoring

5. VERIFICATION
   - Confirm installation
   - Functional testing
   - Documentation
```

## Identity & Access Management

### IAM Framework

```
IAM COMPONENTS:

IDENTITY LIFECYCLE:
- Provisioning
- Modification
- De-provisioning
- Certification

AUTHENTICATION:
- Password policies
- Multi-factor authentication
- Single sign-on
- Passwordless

AUTHORIZATION:
- Role-based access (RBAC)
- Attribute-based access (ABAC)
- Least privilege
- Separation of duties

GOVERNANCE:
- Access reviews
- Policy enforcement
- Audit logging
- Compliance reporting
```

### Privileged Access Management

```
PAM CONTROLS:

VAULT:
- Credential storage
- Password rotation
- Secrets management

SESSION:
- Session recording
- Just-in-time access
- Time-limited credentials

MONITORING:
- Activity logging
- Behavioral analytics
- Alert on anomalies

GOVERNANCE:
- Access certification
- Policy enforcement
- Compliance reporting
```

## Security Awareness

### Security Training Program

| Topic                   | Frequency  | Audience         |
| ----------------------- | ---------- | ---------------- |
| **New Hire Security**   | Onboarding | All employees    |
| **Annual Refresh**      | Annually   | All employees    |
| **Phishing Awareness**  | Quarterly  | All employees    |
| **Developer Security**  | Annually   | Development team |
| **Executive Briefings** | Quarterly  | Leadership       |
| **Role-Based**          | As needed  | Specific roles   |

### Phishing Simulation

```
SIMULATION PROGRAM:

FREQUENCY: Monthly

DIFFICULTY LEVELS:
- Easy: Generic, obvious errors
- Medium: Branded, some personalization
- Hard: Targeted, well-crafted

METRICS:
- Click rate
- Report rate
- Training completion
- Trend over time

RESPONSE:
- Click → Immediate training
- Report → Positive reinforcement
- Repeat offenders → Additional training
```

## Security Metrics

### Key Security Metrics

| Category          | Metric                       | Target    |
| ----------------- | ---------------------------- | --------- |
| **Vulnerability** | Critical vulns open >30 days | 0         |
| **Patching**      | Systems patched within SLA   | 95%+      |
| **Incidents**     | Mean time to detect          | <24 hours |
| **Access**        | Orphan accounts              | 0         |
| **Training**      | Completion rate              | 95%+      |
| **Phishing**      | Click rate                   | <5%       |

### Security Dashboard

```
EXECUTIVE DASHBOARD:

RISK POSTURE:
- Overall risk score
- Risk trend
- Top risks

COMPLIANCE:
- Framework coverage
- Audit findings
- Remediation status

OPERATIONS:
- Incident summary
- Vulnerability status
- Patching compliance

INVESTMENT:
- Budget utilization
- Tool effectiveness
- Headcount
```

## Threat Intelligence

### Threat Intelligence Sources

| Type            | Sources                        | Use                 |
| --------------- | ------------------------------ | ------------------- |
| **Strategic**   | Industry reports, geopolitical | Executive briefings |
| **Tactical**    | TTPs, malware analysis         | Detection rules     |
| **Operational** | IOCs, campaigns                | Active response     |
| **Technical**   | Signatures, hashes             | Automated blocking  |

For detailed incident response processes and SOC operations, see [Incident Response Reference](references/incident-response.md).

## References

- [Security Frameworks Reference](references/security-frameworks.md) - NIST, ISO 27001, CIS Controls, MITRE ATT&CK
- [Incident Response Reference](references/incident-response.md) - IR process, severity levels, SOC operations

## See Also

- [Fortune 50 Risk Management](../fortune50-risk-management/SKILL.md)
- [Fortune 50 Legal/Compliance](../fortune50-legal-compliance/SKILL.md)
- [Fortune 50 Operations](../fortune50-operations/SKILL.md)
