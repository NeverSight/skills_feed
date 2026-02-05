---
name: incident-response
description: >-
  Production incident response procedures for Python/React applications. Use when
  responding to production outages, investigating error spikes, diagnosing performance
  degradation, or conducting post-mortems. Covers severity classification (SEV1-SEV4),
  incident commander role, communication templates, diagnostic commands for FastAPI/
  PostgreSQL/Redis, rollback procedures, and blameless post-mortem process. Does NOT
  cover monitoring setup (use monitoring-setup) or deployment procedures (use
  deployment-pipeline).
license: MIT
compatibility: 'Any backend/frontend stack'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: operations
allowed-tools: Read Grep Glob Bash(curl:*) Bash(jq:*)
context: fork
---

# Incident Response

## When to Use

Activate this skill when:
- Production service is down or returning errors to users
- Error rate has spiked beyond normal thresholds
- Performance has degraded significantly (latency increase, timeouts)
- An alert has fired from the monitoring system
- Users are reporting issues that indicate a systemic problem
- A failed deployment needs investigation and remediation
- Conducting a post-mortem or root cause analysis after an incident

Do NOT use this skill for:
- Setting up monitoring or alerting rules (use `monitoring-setup`)
- Performing routine deployments (use `deployment-pipeline`)
- Docker image or infrastructure issues (use `docker-best-practices`)
- Feature development or code changes (use `python-backend-expert` or `react-frontend-expert`)

## Instructions

### Severity Classification

Classify every incident immediately. Severity determines response urgency, communication cadence, and escalation path.

| Severity | Impact | Examples | Response Time | Update Cadence |
|----------|--------|----------|---------------|----------------|
| **SEV1 (P1)** | Complete outage, all users affected | Service down, data loss, security breach | Immediate (< 5 min) | Every 15 min |
| **SEV2 (P2)** | Major degradation, most users affected | Core feature broken, severe latency | < 15 min | Every 30 min |
| **SEV3 (P3)** | Partial degradation, some users affected | Non-critical feature broken, intermittent errors | < 1 hour | Every 2 hours |
| **SEV4 (P4)** | Minor issue, few users affected | Cosmetic bug, edge case error | < 4 hours | Daily |

**Escalation rules:**
- SEV1: Page on-call engineer + engineering manager immediately
- SEV2: Page on-call engineer, notify engineering manager
- SEV3: Notify on-call engineer via Slack
- SEV4: Create ticket, address during normal working hours

See `references/escalation-contacts.md` for the contact matrix.

### 5-Minute Triage Workflow

When an incident is detected, follow this triage workflow within the first 5 minutes.

```
┌─────────────────────────────────────────────────────────┐
│  MINUTE 0-1: Acknowledge and Classify                   │
│  • Acknowledge the alert or report                      │
│  • Assign severity (SEV1-SEV4)                          │
│  • Designate incident commander                         │
├─────────────────────────────────────────────────────────┤
│  MINUTE 1-2: Assess Scope                               │
│  • Check health endpoints for all services              │
│  • Check error rate and latency dashboards              │
│  • Determine: which services are affected?              │
├─────────────────────────────────────────────────────────┤
│  MINUTE 2-3: Identify Recent Changes                    │
│  • Check: was there a recent deployment?                │
│  • Check: any infrastructure changes?                   │
│  • Check: any external dependency issues?               │
├─────────────────────────────────────────────────────────┤
│  MINUTE 3-4: Initial Communication                      │
│  • Post in #incidents channel                           │
│  • Update status page if SEV1/SEV2                      │
│  • Page additional responders if needed                 │
├─────────────────────────────────────────────────────────┤
│  MINUTE 4-5: Begin Investigation or Mitigate            │
│  • If recent deploy: consider immediate rollback        │
│  • If not deploy-related: begin diagnostic commands     │
│  • Start incident timeline log                          │
└─────────────────────────────────────────────────────────┘
```

**Quick health check command:**
```bash
./skills/incident-response/scripts/health-check-all-services.sh \
  --output-dir ./incident-triage/
```

### Incident Commander Role

The incident commander (IC) coordinates the response. They do NOT investigate directly.

**IC responsibilities:**
1. **Coordinate** -- Assign tasks to responders, prevent duplicate work
2. **Communicate** -- Post regular updates to stakeholders
3. **Decide** -- Make go/no-go decisions on rollback, escalation, communication
4. **Track** -- Maintain the incident timeline
5. **Close** -- Declare the incident resolved and schedule the post-mortem

**IC communication template (initial):**
```
INCIDENT DECLARED: [Title]
Severity: [SEV1/SEV2/SEV3/SEV4]
Commander: [Name]
Start time: [UTC timestamp]
Impact: [What users are experiencing]
Status: Investigating
Next update: [Time]
```

**IC communication template (update):**
```
INCIDENT UPDATE: [Title]
Severity: [SEV level]
Duration: [Time since start]
Status: [Investigating/Identified/Mitigating/Resolved]
Current findings: [What we know]
Actions in progress: [What we are doing]
Next update: [Time]
```

### Investigation Steps

Follow these diagnostic steps based on the type of issue.

#### Application Errors (FastAPI)

```bash
# 1. Check application logs for errors
./skills/incident-response/scripts/fetch-logs.sh \
  --service backend \
  --since "15 minutes ago" \
  --output-dir ./incident-logs/

# 2. Check error rate from logs
docker logs app-backend --since 15m 2>&1 | grep -c "ERROR"

# 3. Check active connections and request patterns
curl -s http://localhost:8000/health/ready | jq .

# 4. Check if the issue is in a specific endpoint
docker logs app-backend --since 15m 2>&1 | \
  grep "ERROR" | \
  grep -oP '"path":"[^"]*"' | sort | uniq -c | sort -rn

# 5. Check Python process status
docker exec app-backend ps aux
docker exec app-backend python -c "import sys; print(sys.version)"
```

#### Database Issues (PostgreSQL)

```bash
# 1. Check database connectivity
docker exec app-db pg_isready -U postgres

# 2. Check active connections (connection pool exhaustion?)
docker exec app-db psql -U postgres -d app_prod -c "
  SELECT count(*), state FROM pg_stat_activity
  GROUP BY state ORDER BY count DESC;
"

# 3. Check for long-running queries (locks, deadlocks?)
docker exec app-db psql -U postgres -d app_prod -c "
  SELECT pid, now() - pg_stat_activity.query_start AS duration,
         query, state
  FROM pg_stat_activity
  WHERE (now() - pg_stat_activity.query_start) > interval '30 seconds'
  AND state != 'idle'
  ORDER BY duration DESC;
"

# 4. Check for lock contention
docker exec app-db psql -U postgres -d app_prod -c "
  SELECT blocked_locks.pid AS blocked_pid,
         blocking_locks.pid AS blocking_pid,
         blocked_activity.query AS blocked_query
  FROM pg_catalog.pg_locks blocked_locks
  JOIN pg_catalog.pg_stat_activity blocked_activity
    ON blocked_activity.pid = blocked_locks.pid
  JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.relation = blocked_locks.relation
    AND blocking_locks.pid != blocked_locks.pid
  JOIN pg_catalog.pg_stat_activity blocking_activity
    ON blocking_activity.pid = blocking_locks.pid
  WHERE NOT blocked_locks.granted;
"

# 5. Check disk space
docker exec app-db df -h /var/lib/postgresql/data
```

#### Redis Issues

```bash
# 1. Check Redis connectivity
docker exec app-redis redis-cli ping

# 2. Check memory usage
docker exec app-redis redis-cli info memory | grep used_memory_human

# 3. Check connected clients
docker exec app-redis redis-cli info clients | grep connected_clients

# 4. Check slow log
docker exec app-redis redis-cli slowlog get 10

# 5. Check keyspace
docker exec app-redis redis-cli info keyspace
```

#### Network and Infrastructure

```bash
# 1. Check DNS resolution
nslookup api.example.com

# 2. Check SSL certificate expiry
echo | openssl s_client -servername api.example.com -connect api.example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# 3. Check container resource usage
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"

# 4. Check disk space on host
df -h /

# 5. Check if dependent services are reachable
curl -sf https://external-api.example.com/health || echo "External API unreachable"
```

### Remediation Actions

#### Immediate Mitigations (apply within minutes)

| Issue | Mitigation | Command |
|-------|-----------|---------|
| Bad deployment | Rollback | `./scripts/deploy.sh --rollback --env production --version $PREV_SHA --output-dir ./results/` |
| Connection pool exhausted | Restart backend | `docker restart app-backend` |
| Long-running query | Kill query | `SELECT pg_terminate_backend(<pid>);` |
| Memory leak | Restart service | `docker restart app-backend` |
| Redis full | Flush non-critical keys | `redis-cli --scan --pattern "cache:*" \| xargs redis-cli del` |
| SSL expired | Apply new cert | Update cert in load balancer |
| Disk full | Clean logs/temp files | `docker system prune -f` |

#### Longer-Term Fixes (apply after stabilization)

1. **Fix the root cause in code** -- Create a branch, fix, test, deploy through normal pipeline
2. **Add monitoring** -- If the issue was not caught by existing alerts, add new alert rules
3. **Add tests** -- Write regression tests for the failure scenario
4. **Update runbooks** -- Document the new failure mode and remediation steps

### Communication Protocol

#### Internal Communication

**Channels:**
- `#incidents` -- Active incident coordination (SEV1/SEV2)
- `#incidents-low` -- SEV3/SEV4 tracking
- `#engineering` -- Post-incident summaries

**Rules:**
1. All communication happens in the designated incident channel
2. Use threads for investigation details, keep main channel for status updates
3. IC posts updates at the defined cadence (see severity table)
4. Tag relevant people explicitly, do not assume they are watching
5. Timestamp all significant findings and actions

#### External Communication (SEV1/SEV2)

**Status page update template:**
```
[Investigating] We are investigating reports of [issue description].
Users may experience [user-visible impact].
We will provide an update within [time].
```

```
[Identified] The issue has been identified as [brief description].
We are working on a fix. Estimated resolution: [time estimate].
```

```
[Resolved] The issue affecting [service] has been resolved.
The root cause was [brief description].
We apologize for the disruption and will publish a detailed post-mortem.
```

### Post-Mortem / RCA Framework

Conduct a blameless post-mortem within 48 hours of every SEV1/SEV2 incident. SEV3 incidents receive a lightweight review.

See `references/post-mortem-template.md` for the full template.

**Post-mortem principles:**
1. **Blameless** -- Focus on systems and processes, not individuals
2. **Thorough** -- Identify all contributing factors, not just the trigger
3. **Actionable** -- Every finding must produce a concrete action item with an owner
4. **Timely** -- Conduct within 48 hours while details are fresh
5. **Shared** -- Publish to the entire engineering team

**Post-mortem structure:**
1. **Summary** -- What happened, when, and what was the impact
2. **Timeline** -- Minute-by-minute account of detection, investigation, mitigation
3. **Root cause** -- The fundamental reason the incident occurred
4. **Contributing factors** -- Other conditions that made the incident worse
5. **What went well** -- Effective parts of the response
6. **What could be improved** -- Gaps in detection, response, or tooling
7. **Action items** -- Specific tasks with owners and due dates

**Five Whys technique for root cause analysis:**
```
Why did users see 500 errors?
  -> Because the backend service returned errors to the load balancer.
Why did the backend service return errors?
  -> Because database connections timed out.
Why did database connections time out?
  -> Because the connection pool was exhausted.
Why was the connection pool exhausted?
  -> Because a new endpoint opened connections without releasing them.
Why were connections not released?
  -> Because the endpoint was missing the async context manager for sessions.

Root cause: Missing async context manager for database sessions in new endpoint.
```

**Generate a structured incident report:**
```bash
python skills/incident-response/scripts/generate-incident-report.py \
  --title "Database connection pool exhaustion" \
  --severity SEV2 \
  --start-time "2024-01-15T14:30:00Z" \
  --end-time "2024-01-15T15:15:00Z" \
  --output-dir ./post-mortems/
```

### Incident Response Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/fetch-logs.sh` | Fetch recent logs from services | `./scripts/fetch-logs.sh --service backend --since "30m" --output-dir ./logs/` |
| `scripts/health-check-all-services.sh` | Check health of all services | `./scripts/health-check-all-services.sh --output-dir ./health/` |
| `scripts/generate-incident-report.py` | Generate structured incident report | `python scripts/generate-incident-report.py --title "..." --severity SEV1 --output-dir ./reports/` |

### Quick Reference: Common Incident Patterns

| Pattern | Symptom | Likely Cause | First Action |
|---------|---------|--------------|--------------|
| 502/503 errors | Users see error page | Backend crashed or overloaded | Check `docker ps`, restart if needed |
| Slow responses | High latency, timeouts | DB queries, external API | Check slow query log, DB connections |
| Partial failures | Some endpoints fail | Single dependency down | Check individual service health |
| Memory growth | OOM kills, restarts | Memory leak | Check `docker stats`, restart |
| Error spike after deploy | Errors start exactly at deploy time | Bug in new code | Rollback immediately |
| Gradual degradation | Slowly worsening metrics | Resource exhaustion, connection leak | Check resource usage trends |
