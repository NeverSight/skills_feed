---
name: manus-expert
id: manus-expert
version: 1.2.0
description: "Senior Orchestrator for Autonomous Missions. Expert in Manus API v2, Multi-Step Task Logic, and Secure Connectors (RSA-SHA256)."
---

# 🕵️‍♂️ Skill: Manus Expert (v1.2.0)

## Executive Summary
The `manus-expert` is the master of high-level autonomous orchestration. In 2026, Manus AI is the primary engine for **Long-Horizon Missions** that span multiple web platforms and APIs. This skill focuses on managing the **Asynchronous Mission Lifecycle**, enforcing **RSA Cryptographic Security**, and implementing **Resilient Recovery Patterns** to ensure that autonomous agents achieve their goals reliably and securely.

---

## 📋 Table of Contents
1. [Autonomous Mission Lifecycle](#autonomous-mission-lifecycle)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Secure Connector Architecture](#secure-connector-architecture)
4. [RSA-SHA256 Webhook Verification](#rsa-sha256-webhook-verification)
5. [Multi-Step Task Orchestration](#multi-step-task-orchestration)
6. [Resilience & Mission Recovery](#resilience--mission-recovery)
7. [Reference Library](#reference-library)

---

## 🚀 Autonomous Mission Lifecycle

Missions are persistent and stateful:
1.  **Creation**: `POST /v1/tasks` with clear, objective-driven goals.
2.  **Execution**: Transition from `pending` to `running`.
3.  **Observation**: Real-time status monitoring via Webhooks.
4.  **Completion**: Handling `task.completed` with idempotent result processing.
5.  **Audit**: Reviewing the agent's reasoning logs for compliance.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Micro-Instruction** | Limits agent reasoning power. | Use **Objective-Based Goals**. |
| **Polling for Results** | Inefficient and adds latency. | Use **RSA-Signed Webhooks**. |
| **Hardcoded Secrets** | Credentials leak in prompts. | Use **Manus Connectors System**. |
| **Unlimited Runtime** | Costs spiral out of control. | Implement **Logical Timeouts**. |
| **Unmapped Task IDs** | Lost missions on server crash. | **Session-Task State Mapping**. |

---

## 🔒 Secure Connector Architecture

Connectors bridge agents to the world without exposing keys:
-   **Zero-Trust**: Agents never see the raw credentials.
-   **Least Privilege**: Scoped access to specific repos or channels.
-   **Verification**: RSA signatures ensure data integrity.

*See [References: Secure Connectors](./references/secure-connectors-system.md) for details.*

---

## 🛠️ Multi-Step Orchestration

Manus doesn't just respond; it **Executes**:
-   **Sub-tasking**: Automatic deconstruction of complex requests.
-   **Tool Selection**: Dynamic identification of the best connector for the job.
-   **Feedback Loops**: Agent-led self-correction during navigation.

---

## 📖 Reference Library

Detailed deep-dives into Manus Excellence:

- [**Task Orchestration**](./references/manus-task-orchestration.md): Multi-step logic and goals.
- [**Secure Connectors**](./references/secure-connectors-system.md): Managing agent access.
- [**Mission Recovery**](./references/mission-recovery-patterns.md): Retries, checkpoints, and rehydration.
- [**Webhook Security**](./references/webhook-security-rsa.md): Implementing RSA-SHA256.

---

*Updated: January 22, 2026 - 21:15*
