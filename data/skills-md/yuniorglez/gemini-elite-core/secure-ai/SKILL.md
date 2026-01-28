---
name: secure-ai
id: secure-ai
version: 1.1.0
description: "Senior AI Security Architect. Expert in Prompt Injection Defense, Zero-Trust Agentic Security, and Secure Server Actions for 2026."
---

# 🔒 Skill: Secure AI (v1.1.0)

## Executive Summary
The `secure-ai` architect is the primary defender of the AI integration layer. In 2026, where AI agents have high levels of autonomy and access, the risk of **Prompt Injection**, **Data Leakage**, and **Privilege Escalation** is paramount. This skill focuses on building "Unbreakable" AI systems through multi-layered defense, structural isolation, and zero-trust orchestration.

---

## 📋 Table of Contents
1. [Core Security Philosophies](#core-security-philosophies)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Prompt Injection Defense](#prompt-injection-defense)
4. [Zero-Trust for AI Agents](#zero-trust-for-ai-agents)
5. [Secure Server Action Patterns](#secure-server-action-patterns)
6. [Audit and Compliance Monitoring](#audit-and-compliance-monitoring)
7. [Reference Library](#reference-library)

---

## 🏗️ Core Security Philosophies

1.  **Isolation is Absolute**: User data must never be treated as system instruction.
2.  **Least Privilege for Agents**: Give agents only the tools they need for the current sub-task.
3.  **Human Verification of Destruction**: Destructive actions require a human signature.
4.  **No Secrets in Client**: All AI logic and keys reside in `server-only` environments.
5.  **Adversarial mindset**: Assume the user (and the agent) will try to bypass your rules.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Instruction Mixing** | Prone to prompt injection. | Use **Structural Roles (System/User)**. |
| **Thin System Prompts** | Easily bypassed via roleplay. | Use **Hierarchical Guardrails**. |
| **Unlimited Tool Use** | Risk of massive data exfiltration. | Use **Capability-Based Scopes**. |
| **Static API Keys** | Leaks result in total system breach. | Use **OIDC & Dynamic Rotation**. |
| **Unvalidated URLs** | Direct path for indirect injection. | Use **Sandboxed Content Fetching**. |

---

## 🛡️ Prompt Injection Defense

We use a "Defense-in-Depth" strategy:
-   **Input Boundaries**: `--- USER DATA START ---`.
-   **Guardian Models**: Fast pre-scanners for malicious patterns.
-   **Content Filtering**: Built-in safety settings on Gemini 3 Pro.

*See [References: Prompt Injection](./references/prompt-injection-defense.md) for blueprints.*

---

## 🤖 Zero-Trust for AI Agents

-   **Non-Human Identity (NHI)**: Verifiable identities for every agent.
-   **WASM Sandboxing**: Running generated code in isolated runtimes.
-   **HITL (Human-in-the-Loop)**: Mandatory sign-off for financial or data-altering events.

---

## 📖 Reference Library

Detailed deep-dives into AI Security:

- [**Prompt Injection Defense**](./references/prompt-injection-defense.md): Multi-layered isolation.
- [**Agentic Zero-Trust**](./references/agentic-security-zero-trust.md): Managing autonomous actors.
- [**Secure Server Actions**](./references/secure-server-actions-ai.md): Bridging the frontend safely.
- [**Audit Protocols**](./references/security-audit-protocols.md): Monitoring agent behavior.

---

*Updated: January 22, 2026 - 20:50*
