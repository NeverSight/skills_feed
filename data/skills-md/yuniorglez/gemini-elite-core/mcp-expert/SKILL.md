---
name: mcp-expert
id: mcp-expert
version: 1.4.0
description: "Senior MCP Architect & Orchestrator. Master of MCP Apps, Server Development (2025-11-25 Spec), and Multi-Agent Tooling."
---

# 🛠️ Skill: mcp-expert (v1.4.0)

## Executive Summary
`mcp-expert` is the definitive resource for building and managing Model Context Protocol (MCP) ecosystems. In 2026, MCP is the backbone of autonomous AI agents, enabling them to navigate complex data, interact with legacy APIs, and render dynamic user interfaces. This skill covers the entire lifecycle—from proactive onboarding to advanced MCP App development and high-security server orchestration.

---

## 📋 Table of Contents
1. [Core Capabilities](#core-capabilities)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Quick Start: Onboarding Protocol](#quick-start-onboarding-protocol)
4. [Standard Production Patterns](#standard-production-patterns)
5. [Professional Server Engineering](#professional-server-engineering)
6. [Security & Zero-Trust Auth](#security--zero-trust-auth)
7. [MCP Apps: Interactive Outcomes](#mcp-apps-interactive-outcomes)
8. [Reference Library](#reference-library)

---

## 🚀 Core Capabilities
- **Proactive Onboarding**: Automatically detecting and configuring missing MCP servers.
- **Agentic Tool Design**: Crafting outcome-oriented tool interfaces for LLM excellence.
- **Multimodal Interaction**: Leveraging resources for long-form data (Video, PDF) via MCP URIs.
- **Interactive UI Rendering**: Implementing **MCP Apps** for direct user-agent interaction.
- **Resilient Orchestration**: Managing tool timeouts, pagination, and error recovery.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **Chatty APIs** | Wastes LLM tokens and increases latency. | Use **Outcome-Oriented Tools**. |
| **Raw Exceptions** | LLM cannot self-correct from stack traces. | Return **Helpful Error Strings**. |
| **Hardcoded Secrets** | Massive security vulnerability. | Use **Environment Variable Mapping**. |
| **Stdout Logging** | Breaks the Stdio transport channel. | Log only to **Stderr**. |
| **Monolithic Servers** | Hard to maintain and discover. | Use **Focused, Small Servers** (5-15 tools). |

---

## ⚡ Quick Start: Onboarding Protocol

When an agent needs a new capability (e.g., "Search the web"):

1.  **Validation**: Check if the required MCP server is already active.
2.  **Guide**: If missing, provide the user with a direct installation path.
    - *"I need to browse the web. I'll setup the `browser-use` MCP server now."*
3.  **Config**: Use `uvx` for zero-install execution where possible.

```json
"browser-use": {
  "command": "uvx",
  "args": ["mcp-server-browser-use", "server"],
  "env": { "BROWSER_USE_API_KEY": "..." }
}
```

---

## 🛠 Standard Production Patterns

### Pattern A: The "Progressive Disclosure" Resource
For large datasets, don't return all data. Return a list of URIs.
-   `mcp://sales/2026/summary`
-   `mcp://sales/2026/detailed-report`

### Pattern B: The "Retryable" Tool
Tools that return a `retry_with` suggestion if inputs are slightly off.

---

## ⚙️ Professional Server Engineering

Building a high-performance server in 2026:
-   **Runtime**: Bun.
-   **Validation**: Zod.
-   **Standard**: 2025-11-25 Specification.

*See [References: Server Development](./references/server-development.md) for the blueprint.*

---

## 🔒 Security & Zero-Trust Auth

-   **OAuth 2.1**: Mandatory for enterprise data access.
-   **Capability Scopes**: Limit the agent to the task at hand.
-   **HITL Gate**: Human-in-the-loop approval for destructive actions.

*See [References: Security & Auth](./references/security-auth.md) for implementation.*

---

## 🖥️ MCP Apps: Interactive Outcomes

MCP Apps are the next evolution of AI interfaces.
-   **Live Dashboards**.
-   **Interactive File Editors**.
-   **Visual Selection Tools**.

*See [References: MCP Apps](./references/mcp-apps.md) for architectural details.*

---

## 📖 Reference Library

Detailed deep-dives into MCP excellence:

- [**Server Development**](./references/server-development.md): Professional engineering standards.
- [**Security & Auth**](./references/security-auth.md): Protecting your data and tools.
- [**MCP Apps**](./references/mcp-apps.md): Interactive UI standard for 2026.
- [**Troubleshooting Guide**](./references/troubleshooting.md): Debugging complex interactions.

---

*Updated: January 22, 2026 - 17:35*
