---
name: runbook-creator
description: Templates and patterns for creating operational runbooks and playbooks. Use when creating runbooks, writing operational documentation, playbook creation, or documenting procedures for on-call teams.
---

# Runbook Creator

Templates and best practices for creating effective operational runbooks.

## When to Use This Skill

- Creating runbooks for new services
- Documenting incident response procedures
- Writing operational playbooks
- Standardizing on-call documentation
- Automating common procedures

## Runbook Principles

1. **Actionable**: Every step should be executable
2. **Testable**: Verify each step works
3. **Current**: Update when systems change
4. **Accessible**: Available during incidents (not behind VPN-only)
5. **Linked**: Referenced from alerts

## Standard Runbook Template

Copy and customize this template:

```markdown
# [Service Name] - [Issue Type]

## Overview
Brief description of what this runbook addresses.

**Last Updated**: YYYY-MM-DD
**Owner**: [Team/Person]
**Related Alerts**: [Alert names that link here]

## Symptoms
What indicates this issue is occurring:
- [ ] Symptom 1
- [ ] Symptom 2
- [ ] Symptom 3

## Impact
- **Users Affected**: [Description]
- **Severity**: [SEV1/SEV2/SEV3/SEV4]
- **Business Impact**: [Description]

## Prerequisites
- Access to [system/tool]
- Permissions: [required permissions]
- Tools: [required CLI tools]

## Diagnostic Steps

### Step 1: [Verify the Issue]
```bash
# Command to run
kubectl get pods -n production | grep -v Running
```

**Expected Output**: [What you should see]
**If Different**: [What to do]

### Step 2: [Gather Information]
```bash
# Command to run
kubectl logs deployment/my-service -n production --tail=100
```

**Look For**: [What to look for in output]

## Resolution Steps

### Option A: [Quick Fix - e.g., Restart]
Use when: [conditions]

```bash
# Step 1: Restart the service
kubectl rollout restart deployment/my-service -n production

# Step 2: Verify pods are coming up
kubectl get pods -n production -w
```

**Verification**: [How to confirm fix worked]

### Option B: [Rollback]
Use when: [conditions]

```bash
# Step 1: Check rollout history
kubectl rollout history deployment/my-service -n production

# Step 2: Rollback to previous version
kubectl rollout undo deployment/my-service -n production
```

**Verification**: [How to confirm fix worked]

## Verification
How to confirm the issue is resolved:
- [ ] Error rate returned to normal
- [ ] Latency within SLO
- [ ] No related alerts firing
- [ ] User-facing functionality working

## Escalation
If this runbook doesn't resolve the issue:
1. **First**: Contact [Team/Person] via [Slack/Phone]
2. **Then**: Page [Escalation contact]
3. **Finally**: [Further escalation path]

## Related Resources
- [Dashboard Link](https://grafana/d/xxx)
- [Architecture Diagram](link)
- [Related Runbook](link)

## Revision History
| Date | Author | Change |
|------|--------|--------|
| YYYY-MM-DD | Name | Initial version |
```

## Quick Runbook Templates

### Service Restart

```markdown
# [Service] - Restart Procedure

## When to Use
- Service unresponsive
- Memory leak suspected
- After configuration change

## Steps

1. **Notify team**
   ```
   Post in #incidents: "Restarting [service] due to [reason]"
   ```

2. **Restart service**
   ```bash
   kubectl rollout restart deployment/[service] -n [namespace]
   ```

3. **Monitor rollout**
   ```bash
   kubectl rollout status deployment/[service] -n [namespace]
   ```

4. **Verify health**
   ```bash
   kubectl get pods -n [namespace] | grep [service]
   # All pods should be Running, 1/1 Ready
   ```

5. **Check metrics**
   - Error rate: [dashboard link]
   - Latency: [dashboard link]

## Rollback
If restart makes things worse:
```bash
kubectl rollout undo deployment/[service] -n [namespace]
```
```

### Database Failover

```markdown
# [Database] - Failover Procedure

## When to Use
- Primary database unresponsive
- Planned maintenance
- Primary showing errors

## Prerequisites
- Database admin access
- Verify replica is in sync

## Pre-Failover Checks

1. **Check replication status**
   ```sql
   SELECT * FROM pg_stat_replication;
   ```
   Verify: `state = 'streaming'`, lag is minimal

2. **Check replica health**
   ```bash
   pg_isready -h replica-host -p 5432
   ```

## Failover Steps

1. **Stop writes to primary** (if possible)
   ```sql
   ALTER SYSTEM SET default_transaction_read_only = on;
   SELECT pg_reload_conf();
   ```

2. **Promote replica**
   ```bash
   pg_ctl promote -D /var/lib/postgresql/data
   ```

3. **Update connection strings**
   - Update DNS/load balancer to point to new primary
   - Or update application config

4. **Verify applications reconnected**
   ```sql
   SELECT count(*) FROM pg_stat_activity WHERE state = 'active';
   ```

## Post-Failover
- [ ] Monitor error rates
- [ ] Set up new replica from old primary
- [ ] Update documentation
```

### Cache Clear

```markdown
# [Service] - Cache Clear Procedure

## When to Use
- Stale data being served
- Cache corruption suspected
- After data migration

## Impact Assessment
- Cache clear will cause temporary latency spike
- Database load will increase temporarily

## Steps

1. **Notify team**
   ```
   Post in #incidents: "Clearing [cache] cache due to [reason]"
   ```

2. **Clear cache**
   
   **Redis - All keys**:
   ```bash
   redis-cli -h [host] FLUSHALL
   ```
   
   **Redis - Specific pattern**:
   ```bash
   redis-cli -h [host] --scan --pattern "user:*" | xargs redis-cli DEL
   ```
   
   **Application cache**:
   ```bash
   curl -X POST http://[service]/admin/cache/clear
   ```

3. **Monitor**
   - Watch cache hit rate recover
   - Monitor database load
   - Check latency

## Verification
- Cache hit rate returning to normal
- No errors from cache operations
- Latency stabilizing
```

## Runbook Checklist

Before publishing a runbook, verify:

```
Runbook Quality Checklist:
- [ ] Title clearly describes the issue/procedure
- [ ] Symptoms section helps identify when to use
- [ ] All commands are copy-pasteable
- [ ] Expected output documented for each command
- [ ] Verification steps confirm success
- [ ] Escalation path is clear
- [ ] Links to dashboards work
- [ ] Tested by someone other than author
- [ ] Linked from relevant alerts
```

## Automation Integration

### Runbook with Automation Hooks

```markdown
# [Service] - Automated Recovery

## Automatic Actions
The following actions run automatically:
1. Pod restart on OOMKilled (Kubernetes)
2. Scale-up on high CPU (HPA)

## Manual Steps (if auto-recovery fails)

### Check why auto-recovery failed
```bash
kubectl describe hpa [service] -n [namespace]
kubectl get events -n [namespace] --sort-by='.lastTimestamp'
```

### Manual intervention
[Steps here]
```

### Script-Backed Runbook

```markdown
# [Service] - Diagnostic Script

## Quick Diagnosis
Run the diagnostic script:
```bash
./scripts/diagnose-service.sh [service-name]
```

This script checks:
- Pod status
- Recent logs
- Resource usage
- Dependency health

## Interpreting Results
| Result | Meaning | Action |
|--------|---------|--------|
| `HEALTHY` | All checks pass | No action needed |
| `DEGRADED` | Some issues | Follow specific recommendations |
| `CRITICAL` | Major issues | Escalate immediately |
```

## Common Runbook Categories

Every service should have runbooks for:

```
Essential Runbooks:
- [ ] Service restart
- [ ] Rollback deployment
- [ ] Scale up/down
- [ ] Clear cache
- [ ] Database failover (if applicable)
- [ ] Dependency failure response
- [ ] High error rate investigation
- [ ] High latency investigation
```

## Additional Resources

- [Example Runbooks](references/example-runbooks.md)
- [Runbook Automation](references/automation.md)
