---
name: framework-context
description: Load and synthesize framework architecture context for reflection and planning tasks.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Skill]
error_handling: graceful
streaming: supported
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Framework Context

## Overview

Provide a consistent, source-anchored model of this framework so agents can reason about system-level behavior without guessing.

## When to Use

- System-level reflection or metacognitive assessment
- Planning tasks that depend on routing/memory/workflow architecture
- Capability-gap analysis before recommending ecosystem evolution

## The Iron Law

```
NO SYSTEM-LEVEL REFLECTION WITHOUT LOADING FRAMEWORK CONTEXT FIRST.
```

<identity>
Framework grounding skill for memory architecture, routing, workflows, hooks, and directory layout.
</identity>

<capabilities>
- Produce scoped context summaries (`memory`, `agents`, `workflows`, `hooks`, `all`)
- Anchor every section to concrete repository paths
- Standardize framework context output for reflection/planning consumers
</capabilities>

<instructions>
<execution_process>

### Step 0: Resolve Scope

- Accept `scope` argument: `memory | agents | workflows | hooks | all`
- Default to `all`

### Step 1: Load Canonical Sources

Read only what is required by scope:

- Memory: `.claude/docs/MEMORY_SYSTEM.md`
- Agent registry/routing: `.claude/context/agent-registry.json`, `.claude/lib/routing/routing-table.cjs`
- Reflection flow hooks: `.claude/hooks/reflection/reflection-queue-processor.cjs`, `.claude/hooks/reflection/reflection-step0-guard.cjs`
- Workflow catalog: `.claude/docs/@ENTERPRISE_WORKFLOWS.md`
- Global framework references: `.claude/CLAUDE.md`

### Step 2: Emit Structured Context

Output sections in this exact order:

1. **Memory System**
2. **Agents and Routing**
3. **Workflows**
4. **Hooks**
5. **Directory Layout**

Each section must include:

- 2-6 concise bullets
- At least one concrete path reference
- Behavior notes (what triggers what)

### Step 3: Scope Filter

- If `scope != all`, return only relevant section(s)
- Never fabricate unknown paths or flows
- If a source is missing, state `missing source: <path>`

### Step 3: Output

Return markdown only; do not write framework files from this skill.

</execution_process>
</instructions>

<examples>
<usage_example>
**Example Invocations**:

```javascript
// Full framework model
Skill({ skill: 'framework-context' });

// Memory-only context for reflection prep
Skill({ skill: 'framework-context', args: '--scope memory' });

// Workflow/hook-only context for integration analysis
Skill({ skill: 'framework-context', args: '--scope workflows' });
```

</usage_example>
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**

```powershell
Get-Content .claude/context/memory/learnings.md -TotalCount 120
```

**After completing:**

- New framework-context pattern -> `.claude/context/memory/learnings.md`
- Broken/ambiguous framework mapping -> `.claude/context/memory/issues.md`
- Architectural interpretation decision -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
