---
name: production-readiness
description: Comprehensive checklist for production deployment readiness covering reliability, observability, security, and operational requirements. Use when preparing for go-live, launch readiness review, production deployment checklist, or assessing if a service is ready for production.
---

# Production Readiness

Systematic checklist to ensure services are ready for production deployment.

## When to Use This Skill

- Preparing a new service for production launch
- Go-live readiness review
- Production deployment checklist needed
- Assessing service maturity
- Pre-launch security review

## Quick Readiness Assessment

Copy and complete this checklist:

```
Production Readiness Assessment:
Service: _______________
Date: _________________
Reviewer: _____________

Reliability:     [ ] Pass  [ ] Partial  [ ] Fail
Observability:   [ ] Pass  [ ] Partial  [ ] Fail
Security:        [ ] Pass  [ ] Partial  [ ] Fail
Operations:      [ ] Pass  [ ] Partial  [ ] Fail
Documentation:   [ ] Pass  [ ] Partial  [ ] Fail

Overall Status:  [ ] Ready  [ ] Conditional  [ ] Not Ready
```

## Reliability Checklist

### SLOs Defined

```
SLO Checklist:
- [ ] Availability SLO defined (e.g., 99.9%)
- [ ] Latency SLO defined (e.g., p99 < 200ms)
- [ ] Error rate SLO defined (e.g., < 0.1%)
- [ ] SLOs documented and communicated
- [ ] Error budget policy established
```

### Fault Tolerance

```
Fault Tolerance:
- [ ] No single points of failure
- [ ] Graceful degradation implemented
- [ ] Circuit breakers for dependencies
- [ ] Retry logic with exponential backoff
- [ ] Timeouts configured for all external calls
- [ ] Rate limiting in place
```

### Capacity

```
Capacity Planning:
- [ ] Load tested to 2x expected peak
- [ ] Auto-scaling configured (if applicable)
- [ ] Resource limits set (CPU, memory)
- [ ] Connection pool sizes appropriate
- [ ] Queue capacity sufficient
```

### Data Resilience

```
Data Protection:
- [ ] Backups configured and tested
- [ ] Backup restoration tested
- [ ] Data replication in place
- [ ] RPO/RTO defined and achievable
- [ ] No data loss on service restart
```

## Observability Checklist

### Metrics

```
Metrics:
- [ ] RED metrics exposed (Rate, Errors, Duration)
- [ ] Resource metrics available (CPU, memory, disk)
- [ ] Business metrics tracked
- [ ] Dependency health metrics
- [ ] Custom metrics for key operations
```

### Logging

```
Logging:
- [ ] Structured logging (JSON)
- [ ] Request/trace IDs in all logs
- [ ] Log levels appropriate (no excessive DEBUG)
- [ ] Sensitive data not logged
- [ ] Log retention configured
```

### Tracing

```
Distributed Tracing:
- [ ] Trace context propagated
- [ ] Spans for external calls
- [ ] Key operations instrumented
- [ ] Sampling rate configured
- [ ] Trace storage/retention set
```

### Alerting

```
Alerts:
- [ ] SLO-based alerts configured
- [ ] Alert thresholds tuned (not noisy)
- [ ] Runbooks linked to alerts
- [ ] Escalation paths defined
- [ ] On-call rotation assigned
```

### Dashboards

```
Dashboards:
- [ ] Service health dashboard exists
- [ ] Key metrics visualized
- [ ] Dashboard accessible to team
- [ ] Dependencies shown
- [ ] Historical data available
```

## Security Checklist

### Authentication & Authorization

```
Auth:
- [ ] Authentication required for all endpoints
- [ ] Authorization checks implemented
- [ ] Service-to-service auth configured
- [ ] No hardcoded credentials
- [ ] Secrets in secret manager
```

### Network Security

```
Network:
- [ ] TLS for all connections
- [ ] Network policies/firewall rules
- [ ] Internal services not publicly exposed
- [ ] Egress traffic controlled
- [ ] DDoS protection (if public)
```

### Data Security

```
Data:
- [ ] Sensitive data encrypted at rest
- [ ] PII handling documented
- [ ] Data retention policy applied
- [ ] Audit logging for sensitive operations
- [ ] GDPR/compliance requirements met
```

### Vulnerability Management

```
Vulnerabilities:
- [ ] Dependencies scanned for CVEs
- [ ] Container images scanned
- [ ] No critical vulnerabilities
- [ ] Security review completed
- [ ] Penetration testing (if required)
```

## Operations Checklist

### Deployment

```
Deployment:
- [ ] CI/CD pipeline configured
- [ ] Deployment is automated
- [ ] Rollback procedure documented
- [ ] Rollback tested
- [ ] Blue-green or canary supported
- [ ] Feature flags for risky changes
```

### Runbooks

```
Runbooks:
- [ ] Startup/shutdown procedures
- [ ] Common troubleshooting steps
- [ ] Escalation procedures
- [ ] Disaster recovery steps
- [ ] Maintenance procedures
```

### On-Call

```
On-Call Readiness:
- [ ] On-call rotation scheduled
- [ ] Team trained on service
- [ ] Escalation paths clear
- [ ] Contact information current
- [ ] Handoff procedures defined
```

## Documentation Checklist

```
Documentation:
- [ ] Architecture diagram current
- [ ] API documentation complete
- [ ] README with setup instructions
- [ ] Dependencies documented
- [ ] Configuration documented
- [ ] Known issues/limitations listed
```

## Rollback Plan

Every production deployment needs a rollback plan:

```
Rollback Plan:
- Rollback trigger: [What conditions trigger rollback]
- Rollback method: [How to rollback - automated/manual]
- Rollback time: [Expected time to complete]
- Data considerations: [Any data migration concerns]
- Verification: [How to verify rollback success]
```

## Pre-Launch Final Checklist

Complete immediately before go-live:

```
Final Pre-Launch:
- [ ] All checklist items above addressed
- [ ] Stakeholders notified of launch
- [ ] War room/incident channel ready
- [ ] Key personnel available
- [ ] Monitoring dashboards open
- [ ] Rollback ready to execute
- [ ] Communication templates prepared
```

## Common Blockers

See [references/common-blockers.md](references/common-blockers.md) for typical issues that block production readiness.

## Additional Resources

- [Common Production Blockers](references/common-blockers.md)
- [SLO Design Guide](references/slo-guide.md)
