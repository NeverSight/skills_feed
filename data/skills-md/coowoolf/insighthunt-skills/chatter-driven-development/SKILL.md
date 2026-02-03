---
name: chatter-driven-development
description: Use when designing futuristic agentic workflows, when wanting AI to proactively act on team communications, or when eliminating the bottleneck of formal specifications
---

# Chatter-Driven Development

## Overview

A development paradigm where AI agents monitor unstructured team communications (Slack, Linear, meetings) to infer intent and **proactively generate code** without formal specifications.

**Core principle:** Use existing team "chatter" as input—discussions, complaints, questions—and let agents draft solutions before being asked.

## The Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  1. SIGNAL INPUT                                                │
│     Slack messages, meeting transcripts, Reddit complaints      │
│                          │                                      │
│                          ▼                                      │
│  2. INTENT EXTRACTION                                           │
│     Agent parses chatter to identify:                           │
│     • Bugs    • Feature requests    • Questions                 │
│                          │                                      │
│                          ▼                                      │
│  3. PROACTIVE ARTIFACT GENERATION                               │
│     Agent drafts:                                                │
│     • Pull Requests    • Answers    • Analysis                  │
│                          │                                      │
│                          ▼                                      │
│  4. HUMAN VERIFICATION                                          │
│     Simple approval interface ("Swipe right" / Merge)           │
└─────────────────────────────────────────────────────────────────┘
```

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Ubiquitous Listening** | Agent connected to Slack, Email, Meetings as passive observer |
| **Context Inference** | Parse unstructured chatter to identify actionable items |
| **Proactive Execution** | Draft PR/answer/analysis BEFORE being explicitly asked |
| **Low-Friction Review** | Humans approve via simple interfaces, not deep code review |

## Enablement Requirements

- [ ] Agent has access to team communication channels
- [ ] Agent can parse natural language intent
- [ ] Agent can create artifacts (PRs, docs, analyses)
- [ ] Simple approval workflow exists

## Common Mistakes

- **Requiring formal specs**: Train agents to interpret natural discussions
- **No proactive action**: Waiting for explicit prompts defeats the purpose
- **High-friction review**: Make approval as simple as possible

## Real-World Examples

- **Block**: "Goose" listens to meetings and proactively drafts PRs/emails
- **OpenAI**: Codex answers data queries directly in Slack

---

*Source: Alexander Embiricos (OpenAI Codex) via Lenny's Podcast*
