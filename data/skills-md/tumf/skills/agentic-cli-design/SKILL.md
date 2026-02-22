---
name: agentic-cli-design
description: |
  Design principles for building CLI tools that LLM/AI agents can safely and reliably operate.
  Provides 7 core principles (Machine-readable, Non-interactive, Idempotent, Safe-by-default,
  Observable, Context-efficient, Introspectable) with scorecard, templates, and anti-patterns.
  Use when: (1) designing new CLI tools for agent use, (2) improving existing CLIs for agent
  compatibility, (3) reviewing CLI design for agent-friendliness, or (4) need guidance on
  JSON output formats, exit codes, authentication flows, or self-describing CLI patterns.
---

# Agentic CLI Design

## Overview

**Agentic CLI Design** is a design philosophy that treats CLIs not as "tools for humans to operate in terminals," but as **protocols/APIs that LLMs/agents can safely, reliably, and repeatably invoke**.

The success criteria is that agents can operate the CLI:
- **Without confusion** (options are explicit)
- **Without breaking things** (safe-by-default)
- **Without getting stuck** (non-interactive, timeout/retry strategies)
- **Repeatedly** (idempotent, re-execution tolerant)
- **With self-healing** (observable, self-describing)

This skill provides a comprehensive framework for designing and evaluating CLI tools for agent use.

## Core Definition

**Agentic CLI Design** = *Design principles for CLIs that enable LLM/agents to execute commands safely and reliably in non-interactive, repetitive, failure-prone environments.*

Rather than optimizing for human "feel," we optimize for **machines to read, decide, re-execute, and recover**.

## The 7 Principles

### P1. Machine-readable (Primary Output Format)

**Machine-readable output is the primary interface, not human-readable text.**

- Provide `--json` / `--output json|yaml|text` as a first-class option
- Strict separation: stdout=results / stderr=logs/progress (never mix)
- **Errors are also structured** (preferably JSON)
- Schema stability (manage breaking changes with `schemaVersion`)

**When to use**: Every CLI command should support structured output.

### P2. Non-interactive by Default

**Interactive prompts should not be the default behavior.**

- Don't assume interactive prompts
- Provide `--yes` / `--force` / `--no-confirm` / `--non-interactive` flags
- Must complete successfully in TTY-less environments (CI, job runners)

**When to use**: Any command that might prompt for user input.

### P3. Idempotent & Replayable

**Commands should be safe to run multiple times with the same result.**

- Send/create operations accept dedupe-key / client-request-id
- "Already exists" behavior is configurable: `--if-exists skip|update|error`
- Retrieval uses explicit pagination: `--limit` `--cursor` `--all`

**When to use**: Any write operation or data retrieval command.

### P4. Safe-by-default

**Destructive operations require explicit confirmation.**

- Destructive operations support `--dry-run` / `--confirm <id>`
- Deletion requires `--force` or similar (default prevents accidents)
- Permissions/scopes are minimized; insufficient permissions return "next steps"

**When to use**: Any command that modifies or deletes data.

### P5. Observable & Debuggable

**Operations must be traceable and debuggable.**

- Provide `--verbose` / `--debug` / `--log-format json`
- Accept `--trace-id` for correlation IDs
- Exit codes are categorized for automatic recovery:
  - 0: success
  - 2: invalid arguments
  - 3: authentication/permission
  - 4: retryable (rate limit, transient errors)

**When to use**: All commands should support observability flags.

### P6. Context-efficient

**Minimize token/context consumption for LLM agents.**

- `--fields/--select` (projection)
- `--output ndjson` (streaming)
- Default is summary; details via `get`/`--include-*` explicitly
- Rich server-side filtering (since/until/query/type...)

**When to use**: Commands that return large datasets or detailed information.

### P7. Introspectable (Self-describing CLI)

**The CLI itself can emit its specification in machine-readable format.**

MCP tools have schema definitions, but CLIs are often black boxes. Solution: **CLI emits its own specification**.

- `commands --json` (list commands and arguments)
- `schema --command ... --output json-schema` (per-command JSON Schema)
- `--help --json` (examples, exit codes, error vocabulary)
- `--output json` top-level fixed fields:
  - `schemaVersion`, `type`, `ok`

**When to use**: For CLIs that need to be discoverable and self-documenting to agents.

## Reference Documentation

This skill includes detailed reference materials organized by topic:

### [references/principles.md](references/principles.md)
Detailed explanation of each of the 7 principles with concrete examples, implementation guidance, and best practices.

**Use when**: You need in-depth understanding of a specific principle or implementation examples.

### [references/scorecard.md](references/scorecard.md)
Complete checklist for reviewing CLI design against the 7 principles. Each principle has specific checkboxes for evaluation.

**Use when**: Reviewing existing CLIs for agent-friendliness or validating new CLI designs.

### [references/templates.md](references/templates.md)
Concrete templates for:
- JSON response formats (success/failure)
- Exit code conventions
- Introspection command patterns
- Authentication status responses

**Use when**: Implementing specific features like JSON output, error handling, or self-description.

### [references/anti-patterns.md](references/anti-patterns.md)
Common failure patterns that break agent compatibility, including:
- Mixed stdout/stderr
- Inconsistent JSON schemas
- Interactive-by-default behavior
- Unsafe destructive operations
- Context explosion
- Browser-only authentication

**Use when**: Troubleshooting agent failures or avoiding common pitfalls.

## Quick Start

### For New CLI Design

1. Review the 7 principles above
2. Use [references/scorecard.md](references/scorecard.md) as a design checklist
3. Implement using patterns from [references/templates.md](references/templates.md)
4. Avoid patterns in [references/anti-patterns.md](references/anti-patterns.md)

### For Existing CLI Review

1. Run through [references/scorecard.md](references/scorecard.md)
2. Identify gaps in principle coverage
3. Check [references/anti-patterns.md](references/anti-patterns.md) for current issues
4. Prioritize fixes based on agent use cases

### For Agent Skill Creation

When creating an Agent Skill for a CLI tool, include:
- Task-specific recipes (minimal command sequences)
- Guardrails (dry-run → confirm → execute patterns)
- Input/output types (typical success/failure JSON)
- Error recovery procedures (rate limit, auth_required, etc.)
- Recommended defaults (`--json`/`--non-interactive`/`--limit`)

## Authentication Considerations

For OAuth/headless authentication:
- Prefer **Device Authorization Grant** (RFC 8628) as first choice
- Provide `auth status --json` for agents to check prerequisites
- Support `auth export` / `auth import` for headless environment migration
- In `--non-interactive` mode: return error + next steps (don't prompt)

See [references/templates.md](references/templates.md) for authentication response formats.

## Scoring Your CLI

Each principle can be scored 0/1/2 points for easy comparison:
- 0: Not implemented
- 1: Partially implemented
- 2: Fully implemented

Maximum score: 14 points (2 points × 7 principles)

Use [references/scorecard.md](references/scorecard.md) for detailed scoring criteria.

## Related Concepts

- **MCP (Model Context Protocol)**: Provides tool definitions with schemas; Agentic CLI Design makes standalone CLIs equally discoverable
- **Agent Skills**: Documentation layer that teaches agents safe CLI usage patterns
- **Infrastructure as Code**: Shares idempotency and declarative principles
- **12-Factor Apps**: Shares configuration and observability principles

## Examples in the Wild

Well-designed CLIs that demonstrate these principles:
- **GitHub CLI (`gh`)**: Excellent `--json` support, non-interactive flags
- **kubectl**: Strong idempotency, declarative apply, dry-run support
- **AWS CLI**: Comprehensive `--output json`, pagination, filtering

## When to Use This Skill

Use this skill when:

1. **Designing a new CLI** intended for agent/automation use
2. **Improving an existing CLI** to be more agent-friendly
3. **Creating an Agent Skill** for a CLI tool
4. **Debugging agent failures** with CLI tools
5. **Reviewing CLI design** for production readiness
6. **Choosing between CLI tools** for agent workflows

## When NOT to Use This Skill

This skill may be overkill for:
- One-off scripts for personal use
- CLIs exclusively for human interactive use
- Prototypes not intended for production
- Tools with inherently interactive workflows (text editors, REPLs)

## Further Reading

- [references/principles.md](references/principles.md) - Deep dive into each principle
- [references/scorecard.md](references/scorecard.md) - Evaluation checklist
- [references/templates.md](references/templates.md) - Implementation templates
- [references/anti-patterns.md](references/anti-patterns.md) - What to avoid
