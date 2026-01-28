---
name: code-architect
id: code-architect
version: 1.1.0
description: "Senior Software Architect. Expert in AI-Native Systems, Modular Monoliths, and Edge-Cloud Orchestration for 2026 ecosystems."
---

# 🏗️ Skill: Code Architect (v1.1.0)

## Executive Summary
The `code-architect` is the visionary behind the system's structural integrity, scalability, and "Agent Friendliness." In 2026, architecture is no longer just about connecting components; it's about designing **Reasoning Loops**, enforcing **Module Boundaries**, and optimizing for **Agent Experience (AX)**. This skill provides the high-level blueprint for building maintainable, elite-tier software in an AI-saturated world.

---

## 📋 Table of Contents
1. [Core Architectural Philosophies](#core-architectural-philosophies)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [The Modern Modular Monolith](#the-modern-modular-monolith)
4. [AI-Native Architecture (Reasoning Layers)](#ai-native-architecture-reasoning-layers)
5. [Edge Orchestration Standards](#edge-orchestration-standards)
6. [Designing for Agent Experience (AX)](#designing-for-agent-experience-ax)
7. [Reference Library](#reference-library)

---

## 🏛️ Core Architectural Philosophies

1.  **Decoupling is Mandatory**: Business logic (Domain) must be agnostic of infrastructure (DB, UI, External APIs).
2.  **Contracts Over Implementation**: Define strict interfaces (Zod/Valibot) before writing a single line of logic.
3.  **AX-First Design**: If an AI agent can't understand your module, it's poorly architected.
4.  **Gradual Complexity**: Start with a Modular Monolith; extract services only when horizontal scaling or team isolation requires it.
5.  **Zero-Trust Security**: Design every module as if its neighbors were potentially malicious.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Premature Microservices** | High operational tax and latency. | Use **Modular Monoliths**. |
| **Spaghetti Context** | AI gets lost in tangled dependencies. | Use **Explicit Module Interfaces**. |
| **Silent Failures** | Agents cannot self-heal or retry. | Use **Actionable Feedback APIs**. |
| **Hard-Coded Workflows** | Limits system adaptability. | Use **Goal-Driven Architectures**. |
| **Stateful Edge** | Inconsistent UX and high egress. | Use **Lazy Sync & Ephemeral State**. |

---

## 🧱 The Modern Modular Monolith

In 2026, we prioritize **Development Velocity** via:
-   **Strict Namespaces**: `modules/auth`, `modules/billing`.
-   **In-Memory Event Bus**: Decoupling modules without network overhead.
-   **Atomic Deployments**: Ensuring all modules are always in sync.

*See [References: Modular Monoliths](./references/modular-monoliths-2026.md) for the blueprint.*

---

## 🤖 AI-Native Architecture

We design systems that "Think":
-   **Guardian Agents**: Architectural validation of every state change.
-   **Reasoning Logs**: Storing the "Why" behind every AI decision.
-   **Context-Rich DBs**: Merging SQL and Vector stores.

*See [References: AI-Native Architecture](./references/ai-native-architecture.md) for patterns.*

---

## 🌍 Edge Orchestration

-   **Global Routing**: Requests land on the node closest to the user.
-   **WASM Runtimes**: Minimal cold starts for edge functions.
-   **Policy-Driven Placement**: Moving data based on usage patterns.

---

## 📖 Reference Library

Detailed deep-dives into Architectural Excellence:

- [**Modular Monoliths**](./references/modular-monoliths-2026.md): The modern standard for speed and scale.
- [**AI-Native Design**](./references/ai-native-architecture.md): Systems with integrated reasoning.
- [**Edge Orchestration**](./references/edge-orchestration-patterns.md): Global patterns for 2026.
- [**Agent Experience (AX)**](./references/agent-experience-ax.md): Designing for machine users.

---

*Updated: January 22, 2026 - 19:20*
