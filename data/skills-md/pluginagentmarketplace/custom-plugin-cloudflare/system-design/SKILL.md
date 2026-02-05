---
# ═══════════════════════════════════════════════════════════════════════════
# SKILL: System Design
# Version: 2.0.0 | Updated: 2025-01
# ═══════════════════════════════════════════════════════════════════════════
name: system-design
description: System design, software architecture, API design, cybersecurity, and threat modeling. Build secure, scalable systems.

# ACTIVATION TRIGGERS
triggers:
  - architecture
  - system design
  - security
  - api
  - scalability
  - owasp
  - threat modeling
  - compliance

# SKILL PARAMETERS
parameters:
  system_type:
    type: string
    required: true
    description: Type of system (web app, API, data platform)
  scale:
    type: string
    enum: [startup, growth, enterprise]
    required: false
  security_level:
    type: string
    enum: [standard, high, compliance]
    required: false

# OUTPUT SPECIFICATION
outputs:
  architecture:
    type: object
  security_measures:
    type: array
  trade_offs:
    type: array

# RELIABILITY
retry:
  max_attempts: 3
  backoff: exponential

# OBSERVABILITY
observability:
  log_level: info

level: advanced
prerequisites:
  - core-development
  - data-structures

sasmp_version: "1.3.0"
bonded_agent: 01-core-paths
bond_type: PRIMARY_BOND
---

# System Design Skill

## Quick Reference

| Pattern | Best For | Complexity | Scaling |
|---------|----------|------------|---------|
| **Monolith** | Startups, MVPs | Low | Limited |
| **Microservices** | Large teams | High | Excellent |
| **Serverless** | Event-driven | Medium | Auto |
| **Event-Driven** | High throughput | High | Excellent |

---

## Scalability Progression

```
Level 1: Single Server
    │
    ▼ Bottleneck: CPU/Memory
Level 2: Load Balancer + Multiple Servers
    │
    ▼ Bottleneck: Database reads
Level 3: Caching Layer (Redis)
    │
    ▼ Bottleneck: Database writes
Level 4: Read Replicas
    │
    ▼ Bottleneck: Single DB limits
Level 5: Sharding / Partitioning
    │
    ▼ Bottleneck: Cross-shard queries
Level 6: CQRS + Event Sourcing
```

---

## Architecture Decision Tree

```
What's your team size and product stage?
│
├─► Team < 10, product unclear
│   └─► Monolith (start simple)
│
├─► Team > 10, clear domain boundaries
│   └─► Microservices
│
├─► Variable workloads, pay-per-use
│   └─► Serverless
│
└─► High throughput, async workflows
    └─► Event-Driven
```

---

## API Design

### REST Best Practices
```
GET    /api/v1/users              # List
GET    /api/v1/users/{id}         # Get
POST   /api/v1/users              # Create
PUT    /api/v1/users/{id}         # Replace
PATCH  /api/v1/users/{id}         # Update
DELETE /api/v1/users/{id}         # Delete

GET    /api/v1/users/{id}/orders  # Nested
```

### HTTP Status Codes
| Code | Meaning | Use When |
|------|---------|----------|
| 200 | OK | GET/PUT/PATCH success |
| 201 | Created | POST success |
| 204 | No Content | DELETE success |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | No/invalid auth |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource missing |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Server failure |

---

## Database Selection

| Use Case | Best Choice | Notes |
|----------|-------------|-------|
| Transactions | PostgreSQL | ACID, most versatile |
| High write | Cassandra | Write-optimized |
| Caching | Redis | Sub-millisecond |
| Search | Elasticsearch | Full-text search |
| Analytics | BigQuery | Column-store |
| Time-series | TimescaleDB | Time-based data |
| Graph | Neo4j | Relationships |

---

## Security: OWASP Top 10 (2025)

| # | Vulnerability | Prevention |
|---|---------------|------------|
| 1 | Broken Access Control | Verify auth on every request |
| 2 | Cryptographic Failures | TLS 1.3, AES-256, Argon2 |
| 3 | Injection | Parameterized queries |
| 4 | Insecure Design | Threat modeling |
| 5 | Security Misconfiguration | Harden defaults |
| 6 | Vulnerable Components | Dependency scanning |
| 7 | Auth Failures | MFA, rate limiting |
| 8 | Data Integrity | Sign data, verify sources |
| 9 | Logging Failures | Comprehensive logging |
| 10 | SSRF | Allowlist URLs |

---

## Encryption Standards

| Layer | Standard | Notes |
|-------|----------|-------|
| In Transit | TLS 1.3 | HTTPS everywhere |
| At Rest | AES-256 | Encrypt sensitive data |
| Passwords | Argon2id | bcrypt acceptable |
| API Keys | SHA-256 | Store hashed |

---

## Threat Modeling: STRIDE

```
┌─────────────────────────────────────────┐
│              STRIDE MODEL                │
├─────────────────────────────────────────┤
│  S - Spoofing                           │
│      → Strong auth, MFA                 │
│                                         │
│  T - Tampering                          │
│      → Integrity checks, signatures     │
│                                         │
│  R - Repudiation                        │
│      → Audit logging                    │
│                                         │
│  I - Information Disclosure             │
│      → Encryption, access control       │
│                                         │
│  D - Denial of Service                  │
│      → Rate limiting, DDoS protection   │
│                                         │
│  E - Elevation of Privilege             │
│      → Least privilege, RBAC            │
└─────────────────────────────────────────┘
```

---

## Compliance Requirements

| Standard | Domain | Key Requirements |
|----------|--------|------------------|
| GDPR | EU Data | Consent, right to delete |
| HIPAA | Healthcare | PHI encryption, audit logs |
| SOC 2 | Services | Security controls |
| PCI DSS | Payments | Card data protection |
| CCPA | CA Privacy | Consumer rights |

---

## Disaster Recovery

| Strategy | RTO | RPO | Cost |
|----------|-----|-----|------|
| Backup/Restore | Hours | Hours | Low |
| Pilot Light | 10s min | Minutes | Medium |
| Warm Standby | Minutes | Seconds | High |
| Active-Active | Seconds | Zero | Very High |

---

## Troubleshooting

```
System not scaling?
├─► Database bottleneck? → Add caching, replicas
├─► Single point of failure? → Add redundancy
├─► Stateful services? → Make stateless
└─► Network limits? → CDN, optimize payloads

Security incident response?
├─► 1. CONTAIN: Isolate affected systems
├─► 2. IDENTIFY: Scope and entry point
├─► 3. ERADICATE: Remove threat, patch
├─► 4. RECOVER: Restore from clean backup
└─► 5. LEARN: Post-mortem, improve
```

---

## Common Failure Modes

| Symptom | Root Cause | Recovery |
|---------|------------|----------|
| Cascading failures | Tight coupling | Circuit breakers |
| Works locally | Env differences | Containers, IaC |
| Data breach | Missing controls | Audit, RBAC |
| Audit failed | Missing compliance | Gap analysis |

---

## Next Actions

Describe your system requirements for architecture recommendations.
