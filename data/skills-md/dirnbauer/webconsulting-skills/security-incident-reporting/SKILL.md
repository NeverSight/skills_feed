---
name: security-incident-reporting
description: Security Incident Report templates drawing from NIST/SANS. DDoS post-mortem, CVE correlation, timeline documentation, and blameless root cause analysis.
version: 1.0.0
triggers:
  - incident report
  - post-mortem
  - sir
  - ddos analysis
  - security reporting
  - root cause analysis
  - cve correlation
  - nist 800-61
  - sans incident response
---

# Security Incident Reporting

Comprehensive framework for documenting and analyzing security incidents, drawing from NIST SP 800-61 and SANS methodologies.

## When to Use

- After a security incident (DDoS, breach, vulnerability exploitation)
- Creating post-mortem documentation
- Communicating with stakeholders (C-level, legal, security teams)
- Correlating attack patterns with known CVEs
- Establishing incident response metrics (MTTR, dwell time)

## Related Skills

- [security-audit](../security-audit/SKILL.md) - Pre-incident vulnerability assessment
- [typo3-security](../typo3-security/SKILL.md) - TYPO3 hardening
- [SKILL-TYPO3.md](./SKILL-TYPO3.md) - TYPO3-specific incident reporting

---

## 1. Incident Response Framework

### NIST SP 800-61 / SANS Harmonization

| Phase | NIST | SANS | Documentation Focus |
|-------|------|------|---------------------|
| 1 | Preparation | Preparation | Runbooks, contacts, tools |
| 2 | Detection & Analysis | Identification | Initial detection, triage |
| 3 | Containment | Containment | Isolation actions, timeline |
| 4 | Eradication | Eradication | Root cause removal |
| 5 | Recovery | Recovery | Service restoration |
| 6 | Post-Incident | Lessons Learned | Post-mortem, improvements |

### Documentation Principle

> **Logbuch-Prinzip**: Document in real-time during the incident, then consolidate into the post-mortem report. Never create reports retrospectively from memory.

---

## 2. Severity Rating Systems

### NCISS (National Cyber Incident Scoring System)

| Level | Score | Description |
|-------|-------|-------------|
| Emergency (1) | 100 | Nation-state attack, critical infrastructure |
| Severe (2) | 80-99 | Significant impact, data exfiltration |
| High (3) | 60-79 | Service disruption, potential data loss |
| Medium (4) | 40-59 | Limited impact, contained breach |
| Low (5) | 20-39 | Minor incident, no data loss |
| Baseline (6) | 0-19 | Informational, false positive |

### DDoS Resiliency Score (DRS)

| Level | Description | Typical Bandwidth |
|-------|-------------|-------------------|
| 1-2 | Simple Floods | < 1 Gbps |
| 3-4 | Sophisticated Multi-Vector | 1-5 Gbps |
| 5-6 | Advanced (State-Actor Level) | 5-100 Gbps |
| 7 | Extreme (Hyper-Volumetric) | > 100 Gbps |

### CVSS Integration

For vulnerability-based incidents, include CVSS v3.1 base score from the [security-audit](../security-audit/SKILL.md) skill.

---

## 3. Incident Report Template

### Module A: Metadata & Executive Summary

```markdown
# Security Incident Report

## Metadata
| Field | Value |
|-------|-------|
| Incident ID | SIR-2026-001 |
| Classification | Confidential |
| Status | Closed / Active / Under Investigation |
| Detection Time | 2026-01-21 14:32 UTC |
| Resolution Time | 2026-01-21 15:17 UTC |
| MTTR | 45 minutes |
| Severity | High (NCISS: 65) |
| Lead Analyst | Jane Doe |
| Affected Systems | web-cluster-01, cdn-edge-eu |

## Executive Summary (max 200 words)

On [DATE], our monitoring systems detected [INCIDENT TYPE] targeting [SYSTEMS].
The attack [IMPACT DESCRIPTION]. Through [RESPONSE ACTIONS], normal operations
were restored within [TIMEFRAME]. [DATA IMPACT STATEMENT].

### Business Impact
- Service Availability: [Degraded/Offline for X minutes]
- Data Impact: [None/Potential exposure of X records]
- Financial Impact: [Estimated cost]
- Reputation Impact: [Public/Internal]
```

### Module B: Timeline (Chronological Analysis)

```markdown
## Incident Timeline

| Time (UTC) | Event | Source | Action Taken |
|------------|-------|--------|--------------|
| 14:32 | Traffic spike detected | Cloudflare Alert | On-call notified |
| 14:35 | 5x baseline traffic confirmed | Grafana | Incident declared |
| 14:38 | Geo-blocking activated | Cloudflare | EU/US traffic filtered |
| 14:42 | Attack vector identified: UDP amplification | DPI Analysis | Null-route for UDP/427 |
| 14:55 | Traffic normalized | Monitoring | Mitigation confirmed |
| 15:17 | All systems stable | Status page | Incident closed |

### Dwell Time Analysis
- Time to Detection (TTD): 0 minutes (automated)
- Time to Containment (TTC): 10 minutes
- Time to Eradication (TTE): 23 minutes
- Time to Recovery (TTR): 45 minutes
```

### Module C: Technical Analysis & IoCs

```markdown
## Technical Analysis

### Attack Vectors (MITRE ATT&CK)
- T1498: Network Denial of Service
- T1498.001: Direct Network Flood
- T1498.002: Reflection Amplification

### Indicators of Compromise (IoCs)

#### Network Artifacts
| Type | Value | Context |
|------|-------|---------|
| IP Range | 192.0.2.0/24 | Source (spoofed) |
| ASN | AS12345 | Amplification source |
| Port | UDP/427 | SLP Amplification |
| Signature | \x00\x00\x00\x00SLP | Payload pattern |

#### System Artifacts
| Type | Value | Hash (SHA256) |
|------|-------|---------------|
| Modified File | /var/www/shell.php | a1b2c3... |
| New User | backdoor_admin | N/A |
| Cron Job | /tmp/.hidden/beacon | d4e5f6... |

### Root Cause Analysis (5-Whys)
1. Why did the attack succeed? → Amplification ports were exposed
2. Why were ports exposed? → Firewall rules not updated after migration
3. Why weren't rules updated? → No automated validation in deployment
4. Why no automation? → Security review not in CI/CD pipeline
5. Why not in pipeline? → Technical debt, prioritized features

**Root Cause**: Missing security validation in deployment pipeline
```

---

## 4. DDoS Post-Mortem Analysis

### Metrics Table

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Peak Bandwidth | 45 Gbps | 10 Gbps | Exceeded |
| Peak Packets/sec | 12M PPS | 5M PPS | Exceeded |
| Peak Requests/sec | 850K RPS | 100K RPS | Exceeded |
| Unique Source IPs | 145,000 | N/A | Amplification |
| Attack Duration | 45 min | N/A | - |
| Geographic Spread | 89 countries | N/A | Global botnet |

### Attack Vector Classification

| Vector | % of Traffic | Type | Mitigation |
|--------|--------------|------|------------|
| UDP Flood | 60% | Volumetric | Null-route |
| SYN Flood | 25% | Protocol | SYN cookies |
| HTTP Flood | 15% | Application | Rate limiting |

### Multi-Vector Detection

```
Was this a smoke-screen attack?
├── Volumetric attack started: 14:32
├── Application-layer probing detected: 14:38
├── Login brute-force attempts: 14:40-14:45
└── Conclusion: Coordinated multi-vector attack
```

---

## 5. CVE Correlation for DDoS

Map attack signatures to known vulnerabilities for threat intelligence.

### Amplification Vector CVE Table

| Attack Type | Port | Amplification Factor | CVE | Description |
|-------------|------|---------------------|-----|-------------|
| NTP Monlist | UDP/123 | 556x | CVE-2013-5211 | NTP mode 7 monlist |
| Memcached | UDP/11211 | 51,000x | CVE-2018-1000115 | UDP reflection |
| CLDAP | UDP/389 | 70x | CVE-2020-9490 | LDAP reflection |
| SLP | UDP/427 | 2,200x | CVE-2023-29552 | Service Location Protocol |
| DNS | UDP/53 | 54x | Various | Open resolver abuse |
| SSDP | UDP/1900 | 30x | Various | UPnP reflection |
| Chargen | UDP/19 | 358x | CVE-1999-0103 | Character generator |

### Analysis Example

```markdown
## CVE Correlation Analysis

Traffic analysis shows 40% of UDP flood originated from port 427.
Deep Packet Inspection confirmed payloads typical for CVE-2023-29552.

**Conclusion**: Botnet leveraging unpatched VMware ESXi instances as
SLP reflectors. Recommend:
1. Verify our infrastructure is not acting as reflector
2. Block UDP/427 at edge
3. Report to upstream provider
```

---

## 6. Impact Assessment Matrix

### Operational Impact

| Category | Level | Description |
|----------|-------|-------------|
| Availability | Critical | Complete outage for 15 minutes |
| Performance | High | 50% degradation for 30 minutes |
| Collateral | Medium | API gateway affected |

### Financial Impact

| Category | Estimated Cost |
|----------|----------------|
| Lost Revenue | $15,000 |
| Scrubbing Overage | $2,500 |
| Incident Response | $5,000 (8 person-hours) |
| **Total** | **$22,500** |

### Reputation Impact

| Channel | Severity | Action Required |
|---------|----------|-----------------|
| Social Media | Medium | Prepared statement |
| B2B Partners | Low | Direct notification |
| Press | None | No external coverage |

---

## 7. Blameless Post-Mortem

### Principles

1. **Focus on systems, not individuals**: "Why did the process allow X?" not "Who did X?"
2. **Assume good intentions**: Everyone acted with the best information available
3. **Learn, don't punish**: Goal is improvement, not blame
4. **Share openly**: Publish internally for organizational learning

### Post-Mortem Template

```markdown
## Post-Mortem: [Incident Title]

### What Happened
[Factual description of the incident]

### What Went Well
- Detection was automated (0 min TTD)
- On-call responded within SLA
- Communication was clear

### What Went Wrong
- Firewall rules were outdated
- No alerting for UDP traffic spikes
- Runbook was incomplete

### Action Items
| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| 1 | Add security validation to CI/CD | @devops | 2026-02-01 | Open |
| 2 | Update runbook with DDoS procedures | @security | 2026-01-28 | Open |
| 3 | Implement UDP traffic alerting | @sre | 2026-02-05 | Open |

### Lessons Learned
- Automated security gates prevent configuration drift
- Regular runbook reviews are essential
- Multi-vector attacks require layered defense
```

---

## 8. Report Distribution

### Classification Levels

| Level | Audience | Content |
|-------|----------|---------|
| Executive | C-Level, Board | Summary, business impact, remediation status |
| Technical | Security Team, SOC | Full IoCs, TTPs, forensic details |
| Legal | Legal, Compliance | Data impact, regulatory implications |
| Public | Customers, Press | Sanitized summary, no technical details |

### Retention Requirements

| Document Type | Retention | Storage |
|---------------|-----------|---------|
| Full Incident Report | 7 years | Encrypted archive |
| IoC Data | 2 years | Threat Intelligence Platform |
| Logs & Evidence | 1 year | Immutable storage |

---

## 9. Checklists

### Pre-Incident Preparation

- [ ] Incident response runbooks documented
- [ ] On-call rotation established
- [ ] Communication templates prepared
- [ ] Evidence collection tools ready
- [ ] Stakeholder contact list updated

### During Incident

- [ ] Incident declared and logged
- [ ] Timeline documentation started
- [ ] Evidence preserved (logs, packets)
- [ ] Stakeholders notified
- [ ] Status page updated

### Post-Incident

- [ ] Full incident report completed
- [ ] Post-mortem meeting scheduled
- [ ] Action items assigned and tracked
- [ ] Lessons learned documented
- [ ] Controls validated/improved

---

## References

- [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [SANS Incident Response](https://www.sans.org/white-papers/33901/)
- [MITRE ATT&CK](https://attack.mitre.org/)
- [DDoS Resiliency Score](https://www.ddosresiliencyscore.org/)
- [CISA NCISS](https://www.cisa.gov/sites/default/files/2023-01/cisa_national_cyber_incident_scoring_system_s508c.pdf)

---

## Credits & Attribution

This skill draws from the "Handbuch für Advanced Security Incident Reporting" methodology,
incorporating elements of NIST SP 800-61, SANS frameworks, and industry best practices.

Developed by webconsulting.at for the Claude skill collection.
