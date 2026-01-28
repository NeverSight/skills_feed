---
name: multi-agent-patterns
description: Design multi-agent architectures for complex tasks. Use when single-agent context limits are exceeded, when tasks decompose naturally into subtasks, or when specializing agents improves quality.
---

# Multi-Agent Architecture Patterns for Claude Code

Multi-agent architectures distribute work across multiple agent invocations, each with its own focused context. When designed well, this distribution enables capabilities beyond single-agent limits. When designed poorly, it introduces coordination overhead that negates benefits. The critical insight is that sub-agents exist primarily to isolate context, not to anthropomorphize role division.

## Core Concepts

Multi-agent systems address single-agent context limitations through distribution. Three dominant patterns exist: supervisor/orchestrator for centralized control, peer-to-peer/swarm for flexible handoffs, and hierarchical for layered abstraction. The critical design principle is context isolation—sub-agents exist primarily to partition context rather than to simulate organizational roles.

Effective multi-agent systems require explicit coordination protocols, consensus mechanisms that avoid sycophancy, and careful attention to failure modes including bottlenecks, divergence, and error propagation.

## Why Multi-Agent Architectures

### The Context Bottleneck

Single agents face inherent ceilings in reasoning capability, context management, and tool coordination. Multi-agent architectures address these limitations by partitioning work across multiple context windows.

### The Parallelization Argument

Many tasks contain parallelizable subtasks that a single agent must execute sequentially. Multi-agent architectures assign each subtask to a dedicated agent with a fresh context.

### The Specialization Argument

Different tasks benefit from different agent configurations. Multi-agent architectures enable specialization without combinatorial explosion.

## Progressive Loading

**L2 Content** (loaded when architectural patterns and implementation details needed):
- See: [references/patterns.md](./references/patterns.md)

**L3 Content** (loaded when memory systems and advanced coordination needed):
- See: [references/memory-systems.md](./references/memory-systems.md)
