---
name: bmad-observability-readiness
description: Establishes instrumentation, monitoring, and alerting foundations.
allowed-tools: ["Read", "Write", "Grep", "Bash"]
metadata:
  auto-invoke: true
  triggers:
    patterns:
      - "add logging"
      - "monitoring setup"
      - "no telemetry"
      - "instrument this"
      - "observability gaps"
      - "alert fatigue"
      - "SLO dashboard"
    keywords:
      - observability
      - logging
      - monitoring
      - tracing
      - metrics
      - alerting
      - telemetry
  capabilities:
    - instrumentation-design
    - metrics-cataloging
    - logging-standards
    - alert-tuning
    - slo-definition
  prerequisites:
    - bmad-architecture-design
    - bmad-test-strategy
  outputs:
    - observability-plan
    - instrumentation-backlog
    - slo-dashboard-spec
---

# BMAD Observability Readiness Skill

## When to Invoke

Use this skill when the user:
- Mentions missing or low-quality logging, metrics, or tracing.
- Requests monitoring/alerting setup before a launch or major release.
- Needs SLOs, dashboards, or on-call runbooks.
- Reports alert fatigue or noise that needs rationalization.
- Wants to ensure performance and reliability work has data coverage.

If instrumentation already exists and only specific bug fixes are required, hand over to `bmad-development-execution` with the backlog produced here.

## Mission

Deliver a comprehensive observability plan that enables diagnosis, alerting, and measurement across the system. Ensure downstream performance, reliability, and security work has trustworthy telemetry.

## Inputs Required

- Architecture diagrams and component inventory.
- Existing logging/monitoring/tracing configuration (if any).
- Current incidents, outages, or blind spots experienced by the team.
- SLAs/SLOs, business KPIs, or compliance reporting requirements.

## Outputs

- **Observability plan** detailing metrics, logs, traces, dashboards, and retention policies.
- **Instrumentation backlog** with implementation tasks, owners, and acceptance criteria.
- **SLO dashboard specification** covering golden signals, alert thresholds, and runbook links.
- Updated runbook or escalation paths if gaps were discovered.

## Process

1. Audit current telemetry coverage, tooling, and data retention. Document gaps.
2. Define observability objectives aligned with user journeys and business KPIs.
3. Design instrumentation strategy: metrics taxonomy, structured logging, trace spans, event schemas.
4. Establish SLOs, SLIs, and alerting strategy with on-call expectations and noise controls.
5. Produce dashboards/reporting requirements and data governance notes.
6. Create backlog with prioritized instrumentation tasks and verification approach.

## Quality Gates

- Every critical user journey has metrics and alerts defined (latency, errors, saturation, traffic).
- Logging standards specify structure, PII handling, and retention.
- Alert runbooks documented or flagged for creation.
- Observability plan references integration with performance, security, and incident workflows.

## Error Handling

- If telemetry tooling is undecided, present comparative options with trade-offs.
- Highlight dependencies on platform teams or infrastructure before finalizing timeline.
- Escalate when observability requirements conflict with compliance or privacy constraints.
