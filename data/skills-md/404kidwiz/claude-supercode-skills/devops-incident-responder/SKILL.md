---
name: devops-incident-responder
description: Expert in SRE practices, incident management, root cause analysis, and automated remediation.
---

# Incident Response Engineer

## Purpose

Provides incident management and reliability engineering expertise specializing in rapid outage response, root cause analysis, and automated remediation. Focuses on minimizing MTTR (Mean Time To Recovery) through effective triage, communication, and prevention strategies.

## When to Use

- Responding to active production incidents (Outage, Latency spike, Error rate increase)
- Establishing or improving On-Call rotation and escalation policies
- Writing or executing Runbooks/Playbooks
- Conducting Blameless Postmortems (RCA)
- Setting up ChatOps (Slack/Teams integration with PagerDuty)
- Implementing automated remediation (Self-healing systems)

---
---

## 2. Decision Framework

### Incident Severity Levels

| Level | Criteria | Response | SLA (Response) |
|-------|----------|----------|----------------|
| **SEV-1** | Critical user impact (Site Down, Data Loss). | Wake up everyone. CEO notified. | 15 mins |
| **SEV-2** | Major feature broken (Checkout fails). | Wake up on-call. | 30 mins |
| **SEV-3** | Minor issue (Internal tool slow). | Handle next business day. | 8 business hours |
| **SEV-4** | Trivial bug / Cosmetic. | Backlog. | N/A |

### Triage Methodology (USE Method)

For every resource (CPU, Memory, Disk), check:
1.  **Utilization**: % time busy (e.g., 99% CPU)
2.  **Saturation**: Queue length (e.g., Load Average)
3.  **Errors**: Count of error events

### Response Roles (ICS Framework)

-   **Incident Commander (IC):** Leads the response. Makes decisions. Does NOT touch the keyboard.
-   **Ops Lead:** Technical lead making changes.
-   **Comms Lead:** Updates stakeholders/status page.

**Red Flags → Escalate to `security-engineer`:**
- Evidence of compromise (Ransomware note, suspicious SSH logs)
- DDoS attack patterns (verify with `netstat` / WAF logs)
- Data exfiltration signals (High outbound bandwidth)

---
---

### Workflow 2: Automated Remediation (StackStorm / Lambda)

**Goal:** Fix "Disk Full" alerts without human intervention.

**Steps:**

1.  **Trigger**
    -   Prometheus Alert: `DiskSpaceLow` (> 90%).
    -   Webhook → Remediation Service.

2.  **Action**
    -   SSH to host / Pod exec.
    -   Run cleanup: `docker system prune -f` or `journalctl --vacuum-time=1d`.
    -   Expand Volume (EBS Modify).

3.  **Notification**
    -   Post to Slack: "Disk space low on host-123. Cleanup ran. Space reclaimed: 5GB."

---
---

## 4. Patterns & Templates

### Pattern 1: Circuit Breaker

**Use case:** Preventing cascading failures when a dependency acts up.

```yaml
# Istio DestinationRule
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: reviews
spec:
  host: reviews
  trafficPolicy:
    connectionPool:
      http:
        http1MaxPendingRequests: 1
        maxRequestsPerConnection: 1
    outlierDetection:
      consecutive5xxErrors: 1
      interval: 1s
      baseEjectionTime: 3m
      maxEjectionPercent: 100
```

### Pattern 2: Runbook Template

```markdown
# Runbook: High Database CPU

**Severity:** SEV-2
**Trigger:** RDS CPU > 90% for 5 mins

## 1. Triage
- Check [Database Dashboard](link).
- Is it a specific query? (See "Top SQL" panel).

## 2. Mitigation Actions
- **Option A (Bad Query):** Kill the session.
  `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE ...`
- **Option B (Traffic Spike):** Scale Read Replicas (Terraform apply).
- **Option C (Maintenance):** Stop non-essential cron jobs.

## 3. Escalation
- If CPU remains > 95% for 15 mins, page @database-team.
```

### Pattern 3: Status Page Update

**Use case:** Clear communication to users.

*   **Investigating:** "We are investigating reports of slow loading times on the dashboard. Our team is looking into it."
*   **Identified:** "We have identified the issue as a database connection pool limit. We are working on increasing capacity."
*   **Monitoring:** "A fix has been implemented and we are monitoring the results."
*   **Resolved:** "The issue has been resolved. All systems operational."

---
---

## 6. Integration Patterns

### **devops-engineer:**
-   **Handoff**: Responder identifies "Drift" as cause → DevOps implements GitOps (ArgoCD) to enforce state.
-   **Collaboration**: Improving observability (adding logs/metrics) in the platform.
-   **Tools**: Terraform, Prometheus.

### **backend-developer:**
-   **Handoff**: Responder identifies bug causing outage → Developer fixes bug.
-   **Collaboration**: Defining SLOs (Service Level Objectives) and Error Budgets.
-   **Tools**: Sentry, Datadog APM.

### **security-engineer:**
-   **Handoff**: Responder notices weird traffic patterns → Security analyzes for DDoS/Breach.
-   **Collaboration**: Managing secrets rotation during incidents.
-   **Tools**: CloudTrail, WAF.

---
