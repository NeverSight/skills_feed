---
name: incident
description: Handle production incidents with urgency. Use when production issues occur for debugging, fixes, and post-mortems.
---

# Incident Response

Handle production incidents systematically.

## When to Use

- Production is down or degraded
- Critical errors affecting users
- Security incidents
- Data issues
- Performance emergencies

## Incident Workflow

```
DETECT → TRIAGE → MITIGATE → RESOLVE → REVIEW
```

### 1. Detect & Triage

```bash
# Quick health checks
curl -s https://api.example.com/health | jq .
kubectl get pods -n production | grep -v Running

# Check recent deployments
git log --oneline -5
kubectl rollout history deployment/app

# Error rates
grep -c "ERROR" /var/log/app.log
```

### 2. Mitigate First

**Priority: Stop the bleeding before finding root cause**

```bash
# Rollback deployment
kubectl rollout undo deployment/app

# Scale up if overloaded
kubectl scale deployment/app --replicas=10

# Feature flag disable
curl -X POST api.example.com/admin/flags -d '{"feature": false}'

# Circuit breaker
# Block problematic endpoint or dependency
```

### 3. Investigate

```bash
# Recent logs
kubectl logs -l app=myapp --since=30m | grep -i error

# Resource usage
kubectl top pods -n production

# Database connections
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

# Network issues
curl -w "@curl-format.txt" -o /dev/null -s https://api.example.com
```

## Severity Levels

| Level | Impact               | Response Time | Example          |
| ----- | -------------------- | ------------- | ---------------- |
| P1    | Complete outage      | Immediate     | Site down        |
| P2    | Major feature broken | 15 min        | Payments failing |
| P3    | Minor feature broken | 1 hour        | Search slow      |
| P4    | Low impact           | Next day      | UI glitch        |

## Communication Template

```markdown
## Incident Update

**Status:** Investigating | Identified | Mitigated | Resolved
**Severity:** P1/P2/P3
**Started:** YYYY-MM-DD HH:MM UTC
**Duration:** X hours

### Summary

[1-2 sentences on what's happening]

### Impact

[Who is affected and how]

### Current Actions

- [Action 1]
- [Action 2]

### Next Update

[Time of next update]
```

## Post-Mortem Template

```markdown
## Incident Post-Mortem

**Date:** YYYY-MM-DD
**Duration:** X hours
**Severity:** P1

### Summary

[What happened in 2-3 sentences]

### Timeline

- HH:MM - [Event]
- HH:MM - [Event]

### Root Cause

[Technical explanation]

### Impact

- Users affected: X
- Revenue impact: $Y
- Data loss: None/Describe

### Action Items

| Action                  | Owner | Due Date   |
| ----------------------- | ----- | ---------- |
| Add monitoring for X    | @name | YYYY-MM-DD |
| Improve circuit breaker | @name | YYYY-MM-DD |

### Lessons Learned

- [What we learned]
```

## Examples

**Input:** "API is returning 500 errors"
**Action:** Check logs, identify failing component, rollback if recent deploy, fix

**Input:** "Database is overloaded"
**Action:** Kill long queries, scale read replicas, optimize or cache hot queries
