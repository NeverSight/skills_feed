---
name: memory-quality-auditor
description: Audit memory retrieval quality (drift, staleness, citation-groundedness) and produce remediation backlog.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Glob, Grep, Bash, Skill, MemoryRecord]
args: '--mode summary|full [--hours 24]'
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Memory Quality Auditor

Audit the memory system as a unified retrieval layer (STM/MTM/LTM files + index + spawn citation outcomes).

## Scope

- Retrieval drift signals
- stale memory ratio
- evidence injection coverage
- citation usage/groundedness continuity

## Workflow

1. Read memory artifacts and latest eval reports.
2. Compute quality metrics and threshold status.
3. Emit remediation backlog with TDD checks.
4. Record findings in memory and optional evolution recommendation.
