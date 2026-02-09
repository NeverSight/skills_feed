---
name: pplx-sdk-dev
description: Meta-skill for pplx-sdk development. Orchestrates code review, testing, scaffolding, SSE streaming, and Python best practices into a unified workflow. Use for any development task on this project.
context: fork
agent: orchestrator
---

# pplx-sdk Development Meta-Skill

This meta-skill orchestrates all project-specific and community skills for pplx-sdk development. Activate this skill for any development task — it coordinates the right sub-skills automatically.

## When to use

Use this skill for **any** development task on the pplx-sdk project: implementing features, fixing bugs, reviewing code, writing tests, or scaffolding new modules.

## Subagent Architecture

Each skill delegates to a specialist subagent via `context: fork`. Subagents run in isolated context windows with restricted tool access.

```
┌───────────────────────────────────────────────────────┐
│                  orchestrator                         │
│  (meta-orchestrator, delegates subtasks)              │
├───────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────┐  ┌──────────────┐                  │
│  │ code-reviewer │  │ test-runner   │                  │
│  │ (read-only)   │  │ (run & fix)   │                  │
│  │ view,grep,    │  │ bash,view,    │                  │
│  │ glob,bash     │  │ edit,grep     │                  │
│  └──────────────┘  └──────────────┘                  │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐                  │
│  │ scaffolder    │  │ sse-expert    │                  │
│  │ (create new)  │  │ (streaming)   │                  │
│  │ view,edit,    │  │ view,edit,    │                  │
│  │ bash,grep     │  │ bash,grep     │                  │
│  └──────────────┘  └──────────────┘                  │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐                  │
│  │ reverse-     │  │ architect     │                  │
│  │  engineer    │  │ (diagrams &   │                  │
│  │ (API disc.)  │  │  design)      │                  │
│  │ view,edit,   │  │ view,edit,    │                  │
│  │ bash,grep    │  │ bash,grep     │                  │
│  └──────────────┘  └──────────────┘                  │
│                                                       │
│  ┌──────────────┐  ┌──────────────┐                  │
│  │ spa-expert   │  │ codegraph     │                  │
│  │ (SPA RE,     │  │ (AST, deps,   │                  │
│  │  CDP, ext.)  │  │  knowledge)   │                  │
│  │ view,edit,   │  │ view,edit,    │                  │
│  │ bash,grep    │  │ bash,grep     │                  │
│  └──────────────┘  └──────────────┘                  │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Subagent Definitions (`.claude/agents/`)

| Subagent | Role | Tools | Isolation |
|----------|------|-------|-----------|
| `orchestrator` | Decomposes tasks, coordinates others | view, bash, grep, glob | fork |
| `code-reviewer` | Read-only architecture review | view, grep, glob, bash | fork |
| `test-runner` | Run tests, diagnose, fix failures | bash, view, edit, grep, glob | fork |
| `scaffolder` | Create new modules and files | view, edit, bash, grep, glob | fork |
| `sse-expert` | SSE streaming implementation | view, edit, bash, grep, glob | fork |
| `reverse-engineer` | API discovery, traffic analysis | view, edit, bash, grep, glob | fork |
| `architect` | Architecture diagrams, design validation | view, edit, bash, grep, glob | fork |
| `spa-expert` | SPA RE: React/Vite/Workbox/CDP, extensions | view, edit, bash, grep, glob | fork |
| `codegraph` | AST parsing (Python + JS/TS), dep graphs, knowledge graphs | view, edit, bash, grep, glob | fork |

## Skill Dependencies

This meta-skill composes the following skills. Apply them in the order shown based on the task type.

### Project-Specific Skills (repo root)

| Skill | Path | Subagent | Purpose |
|-------|------|----------|---------|
| `code-review` | `code-review/SKILL.md` | `code-reviewer` | Architecture compliance and conventions |
| `test-fix` | `test-fix/SKILL.md` | `test-runner` | Diagnose and fix failing tests |
| `scaffold-module` | `scaffold-module/SKILL.md` | `scaffolder` | Create new modules per layered architecture |
| `sse-streaming` | `sse-streaming/SKILL.md` | `sse-expert` | SSE protocol and streaming patterns |
| `reverse-engineer` | `reverse-engineer/SKILL.md` | `reverse-engineer` | API discovery from browser traffic |
| `architecture` | `architecture/SKILL.md` | `architect` | System diagrams and design visualization |
| `spa-reverse-engineer` | `spa-reverse-engineer/SKILL.md` | `spa-expert` | React/Vite/Workbox/CDP webapp RE |
| `code-analysis` | `code-analysis/SKILL.md` | `codegraph` | AST parsing (Python + JS/TS), dependency graphs, knowledge graphs |

### Community Skills (installed via `npx skills`)

| Skill | Source | Purpose |
|-------|--------|---------|
| `python-testing-patterns` | `wshobson/agents` | pytest patterns, fixtures, mocking |
| `python-type-safety` | `wshobson/agents` | Type annotations, mypy strict mode |
| `python-error-handling` | `wshobson/agents` | Exception hierarchies, error patterns |
| `python-design-patterns` | `wshobson/agents` | Protocol pattern, DI, factory |
| `api-design-principles` | `wshobson/agents` | REST API design, endpoint conventions |
| `async-python-patterns` | `wshobson/agents` | async/await, concurrency patterns |
| `skill-creator` | `anthropics/skills` | Guide for creating new skills |
| `mcp-builder` | `anthropics/skills` | Build MCP servers for tool integration |
| `webapp-testing` | `anthropics/skills` | Test web apps with Playwright |
| `ast-grep` | `ast-grep/agent-skill` | Structural code search via AST patterns |
| `knowledge-graph-builder` | `daffy0208/ai-dev-standards` | Knowledge graph design and entity relationships |
| `steering` | `nahisaho/codegraphmcpserver` | CodeGraph MCP orchestration and traceability |

## Workflow: New Feature

```
[plan] → [explore] → [research] → [implement] → [test] → [review] → [done]
```

1. **Plan** — `orchestrator` decomposes the task, identifies target layer
2. **Explore** — `code-reviewer` (read-only fork) analyzes existing code and dependencies
3. **Research** — `reverse-engineer` or `sse-expert` (fork) studies API behavior, reads docs, gathers context needed before implementation
4. **Scaffold** — `scaffolder` (fork) creates files from templates
5. **Implement** — `sse-expert` or `scaffolder` (fork) writes the code
6. **Test** — `test-runner` (fork) runs pytest, fixes failures
7. **Review** — `code-reviewer` (fork) validates architecture compliance
8. **Verify** — `ruff check --fix . && ruff format . && mypy pplx_sdk/ && pytest -v`

## Workflow: Bug Fix

1. **Reproduce** — `test-runner` (fork) runs failing test with `-v`
2. **Research** — `code-reviewer` (fork) traces the code path, reads related modules and tests
3. **Diagnose** — `test-runner` reads traceback, identifies root cause
4. **Fix** — `test-runner` edits source/test, applies `python-error-handling` patterns
5. **Verify** — `test-runner` runs full suite

## Workflow: SSE/Streaming Work

1. **Research** — `sse-expert` (fork) reviews SSE protocol spec, existing transport code, and API response patterns
2. **Implement** — `sse-expert` writes streaming code, applies `async-python-patterns`
3. **Test** — `test-runner` (fork) runs tests with mock SSE responses
4. **Review** — `code-reviewer` (fork) validates transport layer compliance

## Workflow: API Discovery (Reverse Engineering)

```
[capture] → [research] → [document] → [scaffold] → [test] → [review]
```

1. **Capture** — `reverse-engineer` (fork) analyzes cURL/traffic from perplexity.ai DevTools
2. **Research** — `reverse-engineer` studies request/response patterns, tests variations, maps edge cases and auth flows
3. **Document** — `reverse-engineer` writes endpoint documentation with field types and examples
4. **Scaffold** — `scaffolder` (fork) creates Pydantic models and service methods from schema
5. **Implement** — `sse-expert` or `scaffolder` implements transport and domain code
6. **Test** — `test-runner` (fork) validates with mock responses matching discovered schemas
7. **Review** — `code-reviewer` (fork) ensures architecture compliance

## Workflow: API Endpoint

1. **Research** — `code-reviewer` (fork) studies existing endpoints and `api-design-principles` patterns
2. **Design** — `code-reviewer` reviews proposed schema against REST conventions
3. **Implement** — `scaffolder` (fork) creates FastAPI endpoint
4. **Test** — `test-runner` (fork) validates with pytest-httpx mocks

## Workflow: Architecture Design & Visualization

```
[analyze] → [research] → [diagram] → [validate] → [document]
```

1. **Analyze** — `architect` (fork) reads existing code, maps imports and layer dependencies
2. **Research** — `architect` studies the components involved and their relationships
3. **Diagram** — `architect` produces Mermaid diagrams (layer map, sequence, class hierarchy, state machine)
4. **Validate** — `architect` checks for circular deps, upward imports, protocol conformance
5. **Document** — `architect` embeds diagrams in README, docs, or PR descriptions

## Workflow: SPA Reverse Engineering

```
[detect] → [research] → [intercept] → [extract] → [code-graph] → [document] → [implement]
```

1. **Detect** — `spa-expert` (fork) identifies the SPA stack (React version, bundler, state management, service workers)
2. **Research** — `spa-expert` studies the SPA internals, React component tree, and network patterns
3. **Intercept** — `spa-expert` captures network traffic via CDP, Chrome extension, or DevTools
4. **Extract** — `spa-expert` extracts React state shapes, API schemas, and Workbox cache strategies
5. **Code Graph** — `codegraph` (fork) analyzes SPA source code: component tree, import graph, hook chains, TypeScript types; cross-references with `spa-expert` runtime findings
6. **Document** — `reverse-engineer` + `spa-expert` map runtime + static discoveries to SDK architecture
7. **Implement** — `scaffolder` creates models and services; `spa-expert` builds tools/extensions

## Workflow: Code Analysis & Knowledge Graph

```
[parse] → [graph] → [analyze] → [report] → [act]
```

1. **Parse** — `codegraph` (fork) parses source AST: Python via `ast` module, JavaScript/TypeScript via grep-based import parsing
2. **Graph** — `codegraph` builds dependency graph (module-to-module imports) and knowledge graph (Python: IMPORTS, INHERITS, IMPLEMENTS, CALLS, RAISES; SPA: RENDERS, USES_HOOK, CALLS_API, PROVIDES, CONSUMES)
3. **Analyze** — `codegraph` detects patterns: circular deps, layer violations, dead code, complexity hotspots (Python); barrel file cycles, prop drilling, orphan routes (SPA)
4. **Report** — `codegraph` produces structured insights report with Mermaid diagrams and actionable findings
5. **Act** — Delegate findings: `architect` updates diagrams, `code-reviewer` reviews violations, `scaffolder` fixes gaps, `spa-expert` cross-references runtime analysis

## Project Quick Reference

```bash
# Install dependencies
pip install -e ".[dev]"

# Install/update community skills
npx skills add wshobson/agents --skill python-testing-patterns --skill python-type-safety --skill python-error-handling --skill python-design-patterns --skill api-design-principles --skill async-python-patterns --agent github-copilot -y
npx skills add anthropics/skills --skill skill-creator --skill mcp-builder --skill webapp-testing --agent github-copilot -y
npx skills add ast-grep/agent-skill --skill ast-grep --agent github-copilot -y
npx skills add "daffy0208/ai-dev-standards@knowledge-graph-builder" --agent github-copilot -y
npx skills add nahisaho/codegraphmcpserver --skill steering --agent github-copilot -y

# Lint, format, type-check, test
ruff check --fix . && ruff format .
mypy pplx_sdk/ --ignore-missing-imports
pytest tests/ -v --cov=pplx_sdk

# Manage skills
npx skills list          # Show installed skills
npx skills check         # Check for updates
npx skills update        # Update all skills
```

## Architecture Invariants

These rules must **never** be violated regardless of which sub-skill is active:

1. **Layer dependencies**: `core/ → shared/ → transport/ → domain/ → client.py` (never reverse)
2. **Exception hierarchy**: All errors extend `PerplexitySDKError`
3. **Type annotations**: 100% coverage, `from __future__ import annotations`
4. **Google docstrings**: On all public APIs
5. **Protocol pattern**: Use `typing.Protocol`, never ABC
