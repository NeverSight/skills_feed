---
name: latency-principles
description: "Principles, laws, and checklists for analyzing and optimizing software latency. Use this skill when: (1) Diagnosing slow performance or latency spikes, (2) Designing systems with strict latency requirements, (3) Analyzing theoretical limits using Little's Law or Amdahl's Law, or (4) Learning about latency sources (OS, Hardware, Network)."
---

# Latency Principles

This skill provides a systematic approach to understanding and reducing latency in software systems, based on the book "Latency" by Pekka Enberg.

## Core Concepts

Latency is the time delay between a cause and its observed effect. It is a distribution, not a single number.

### Quick Reference

- **Little's Law**: `Concurrency = Throughput * Latency`. Use to size queues and thread pools.
- **Amdahl's Law**: Speedup is limited by the serial part of the task. Use to estimate max benefit of parallelization.
- **Tail Latency**: The experience of the 99th percentile users. In high-fanout systems, tail latency dominates.

For detailed definitions and laws, see [references/principles.md](references/principles.md).

## Diagnosis & Optimization

When facing latency issues, follow this systematic approach:

1.  **Measure First**: Identify *where* the time is going. Don't guess.
2.  **Check the Usual Suspects**: Use the checklist to rule out common issues.
    - See [references/diagnostic_checklist.md](references/diagnostic_checklist.md) for a comprehensive list covering Hardware, OS, and Architecture.
3.  **Model the System**:
    - Is it a throughput problem (queuing)? -> Apply Little's Law.
    - Is it a serial execution problem? -> Apply Amdahl's Law.
    - Is it a tail latency problem (variability)? -> Check fanout and shared resource contention.

## Common Sources of Latency

- **Physics**: Distance (Speed of light).
- **Hardware**: CPU frequency scaling, cache misses, NUMA.
- **OS**: Context switching, interrupts, scheduler latency.
- **Runtime**: Garbage collection pauses, JIT compilation.

## When to use Reference Files

- **[references/principles.md](references/principles.md)**: When you need deep theoretical background, definitions of laws, or understanding of latency compounding.
- **[references/diagnostic_checklist.md](references/diagnostic_checklist.md)**: When you are actively debugging a slow system and need a list of things to check.
