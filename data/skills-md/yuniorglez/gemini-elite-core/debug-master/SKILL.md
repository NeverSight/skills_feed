---
name: debug-master
id: debug-master
version: 1.1.0
description: "Senior Site Reliability Engineer & Debug Architect. Expert in AI-assisted observability, distributed tracing, and autonomous incident remediation in 2026."
---

# 🕵️‍♂️ Skill: Debug Master (v1.1.0)

## Executive Summary
The `debug-master` is a high-level specialist dedicated to the health, reliability, and observability of complex, distributed systems. In 2026, debugging is no longer a manual scavenger hunt through log files; it is an **Orchestrated Investigation** using AI-assisted tracing, predictive anomaly detection, and automated remediation loops. This skill focuses on minimizing MTTR (Mean Time To Repair) and maximizing system resilience through elite SRE standards.

---

## 📋 Table of Contents
1. [Incident Resolution Protocol](#incident-resolution-protocol)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Distributed Tracing (OpenTelemetry)](#distributed-tracing-opentelemetry)
4. [Autonomous Remediation (Agentic Loop)](#autonomous-remediation-agentic-loop)
5. [Predictive Observability](#predictive-observability)
6. [Fullstack Troubleshooting Layers](#fullstack-troubleshooting-layers)
7. [Reference Library](#reference-library)

---

## 🛠️ Incident Resolution Protocol

Every incident follows the **Elite SRE Loop**:

1.  **Evidence Collection**: Correlate metrics, logs, and traces. Read the "Observability Graph" to find the service in red.
2.  **Impact Analysis**: Determine the blast radius. Is it a single user, a region, or the entire tenant base?
3.  **Isolation**: Use binary search (`git bisect`) and trace-filtering to isolate the logic or infra failure.
4.  **Surgical Fix / Rollback**: Apply a precise fix or execute a total rollback if the 5-minute MTTR window is exceeded.
5.  **Post-Mortem**: Generate an automated report summarizing the "Why" and store it in long-term vector memory.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **"Guess and Check"** | Extremely slow and dangerous. | Use **Distributed Tracing**. |
| **Ignoring Warnings** | Leads to "Alert Fatigue" and outages. | Use **Dynamic SLO Tracking**. |
| **Manual Log Scraping**| Inefficient for large datasets. | Use **AI-Assisted Querying (o3)**. |
| **Hotfixing Production** | Bypasses CI/CD and causes drift. | Fix in **Feature Branch** + Deploy. |
| **Disabling RLS/Security**| Huge security risk for a "quick fix." | Fix the **Capability Scope**. |

---

## 🕸️ Distributed Tracing (OpenTelemetry)

We use **OTel** as our source of truth.
-   **Standard Spans**: Every operation must have a traceable span ID.
-   **Adaptive Sampling**: 100% errors, 1% healthy traffic.
-   **Context Propagation**: Mandatory headers for cross-service calls.

*See [References: Distributed Tracing](./references/distributed-tracing-otel.md) for setup.*

---

## 🤖 Autonomous Remediation

In 2026, AI agents handle the triage.
-   **Detection**: Automatic anomaly triggers.
-   **Remediation**: Agents execute safe actions (scale up, cache clear).
-   **HITL Gate**: Humans approve destructive actions.

*See [References: Agentic Response](./references/agentic-incident-response.md) for patterns.*

---

## 📈 Predictive Observability

Identify failures *before* they occur.
-   **Anomaly Detection**: Spotting memory leaks or CPU creep.
-   **Chaos Engineering**: Running agentic "stress tests" weekly.
-   **Dynamic SLOs**: Thresholds that adjust based on business importance.

---

## 📖 Reference Library

Detailed deep-dives into SRE excellence:

- [**Distributed Tracing (OTel)**](./references/distributed-tracing-otel.md): Standardizing your observability.
- [**Agentic Incident Response**](./references/agentic-incident-response.md): The autonomous remediation loop.
- [**Predictive Observability**](./references/predictive-observability.md): Hardening systems for the future.
- [**Fullstack Troubleshooting**](./references/advanced-troubleshooting-fullstack.md): Layers of defense.

---

*Updated: January 22, 2026 - 18:30*
