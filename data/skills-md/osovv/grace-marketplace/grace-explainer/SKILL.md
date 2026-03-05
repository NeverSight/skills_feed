---
name: grace-explainer
description: "Complete GRACE methodology reference. Use when explaining GRACE to users, onboarding new projects, or when you need to understand the GRACE framework — its principles, semantic markup, knowledge graphs, contracts, and unique tag conventions."
---

# GRACE — Graph-RAG Anchored Code Engineering

GRACE is a methodology for AI-driven code generation that makes codebases **navigable by LLMs**. It solves the core problem of AI coding assistants: they generate code but can't reliably navigate, maintain, or evolve it across sessions.

## The Problem GRACE Solves

LLMs lose context between sessions. Without structure:
- They don't know what modules exist or how they connect
- They generate code that duplicates or contradicts existing code
- They can't trace bugs through the codebase
- They drift from the original architecture over time

GRACE provides three interlocking systems that fix this:

```
Knowledge Graph (docs/knowledge-graph.xml)
    maps modules, dependencies, exports
Module Contracts (MODULE_CONTRACT in each file)
    defines WHAT each module does
Semantic Markup (START_BLOCK / END_BLOCK in code)
    makes code navigable at ~500 token granularity
```

## Five Core Principles

### 1. Never Write Code Without a Contract
Before generating any module, create its MODULE_CONTRACT with PURPOSE, SCOPE, INPUTS, OUTPUTS. The contract is the source of truth — code implements the contract, not the other way around.

### 2. Semantic Markup Is Not Comments
Markers like `// START_BLOCK_NAME` and `// END_BLOCK_NAME` are **navigation anchors**, not documentation. They serve as attention anchors for LLM context management and retrieval points for RAG systems.

### 3. Knowledge Graph Is Always Current
`docs/knowledge-graph.xml` is the single map of the entire project. When you add a module — add it to the graph. When you add a dependency — add a CrossLink. The graph never drifts from reality.

### 4. Top-Down Synthesis
Code generation follows a strict pipeline:
```
Requirements -> Technology -> Development Plan -> Module Contracts -> Code
```
Never jump to code. If requirements are unclear — stop and clarify.

### 5. Governed Autonomy (PCAM)
- **Purpose**: defined by the contract (WHAT to build)
- **Constraints**: defined by the development plan (BOUNDARIES)
- **Autonomy**: you choose HOW to implement
- **Metrics**: the contract's outputs tell you if you're done

You have freedom in HOW, not in WHAT. If a contract seems wrong — propose a change, don't silently deviate.

## How the Elements Connect

```
docs/requirements.xml          — WHAT the user needs (use cases, AAG notation)
        |
docs/technology.xml            — WHAT tools we use (runtime, language, versions)
        |
docs/development-plan.xml      — HOW we structure it (modules, phases, contracts)
        |
docs/knowledge-graph.xml       — MAP of everything (modules, dependencies, exports)
        |
src/**/*                       — CODE with GRACE markup (contracts, blocks, maps)
```

Each layer feeds the next. The knowledge graph is both an output of planning and an input for code generation.

## Development Workflow

1. `$grace-init` — create docs/ structure and AGENTS.md
2. Fill in `requirements.xml` with use cases
3. Fill in `technology.xml` with stack decisions
4. `$grace-plan` — architect modules, generate development plan and knowledge graph
5. `$grace-generate module-name` — generate one module with full markup
6. `$grace-execute` — generate all modules with review and commits
7. `$grace-refresh` — sync knowledge graph after manual changes
8. `$grace-fix error-description` — debug via semantic navigation
9. `$grace-status` — health report

## Detailed References

For in-depth documentation on each GRACE component, see the reference files in this skill's `references/` directory:

- `references/semantic-markup.md` — Block conventions, granularity rules, logging
- `references/knowledge-graph.md` — Graph structure, module types, CrossLinks, maintenance
- `references/contract-driven-dev.md` — MODULE_CONTRACT, function contracts, PCAM
- `references/unique-tag-convention.md` — Unique ID-based XML tags, why they work, full naming table
