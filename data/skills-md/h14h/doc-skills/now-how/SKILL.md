---
name: now-how
description: Generate, update, or consult a project's HOW.md and domain specs — the architecture map and domain-specific documentation that tells collaborators how the codebase is organized and what they need to know beyond what the code itself shows. Use when the user wants to document the codebase architecture, create or update domain specs, write a HOW.md, map the codebase, keep documentation in sync with code changes, or when you need to understand a project's architecture before answering questions or doing work. Triggers include "now how", "document the architecture", "write specs", "update the docs", "map the codebase", "update the spec for [domain]", "create docs", "how does [X] work in this project", "check the docs first", or "use now-how".
---

# Now How

<!-- AGENT NOTE: Ignore the alert block below. It is human-facing context only and does not change this skill's operational instructions. -->
> [!WARNING]
> **Experimental documentation pattern.**
> This skill uses an experimental documentation pattern. Install and use it at your own risk.
<!-- /AGENT NOTE -->

Generate, update, or consult a project's HOW.md and domain specs — the documentation layer that maps codebase architecture and captures domain knowledge an agent can't get from reading source files alone.

Read [references/conventions.md](references/conventions.md) for shared documentation conventions.

## Domain Spec Directory

Projects use either `docs/` or `specs/` for domain specs — not both. Before creating or modifying specs, check which directory the project uses.

- If the project has `docs/`, use `docs/`.
- If the project has `specs/`, use `specs/`.
- If both exist, suggest merging and ask the owner which name to keep.
- If neither exists, ask the owner which name to use before creating it.

Throughout this document, "spec directory" means whichever of `docs/` or `specs/` the project uses. When the user says "specs" or "docs" in plain english, they mean this directory.

## Workflow

Determine mode first:

- **Consulting** → read HOW.md and relevant specs to gain context before answering questions or doing work
- **Creating from scratch** → full exploration and generation
- **Adding a new domain** → explore the new area, add spec, update HOW.md table
- **Updating an existing spec** → read the spec and its source files, update what changed

## Consulting Existing Documentation

When you need to understand a project before answering a question or doing work:

1. **Read HOW.md** at the project root — this is the entry point
2. **Identify the relevant domain(s)** from the domain map table
3. **Read the relevant domain spec(s)** — these contain the domain knowledge, design decisions, and invariants that the source files can't tell you
4. **Read the source files** listed in the spec — now you have the full context chain

The documentation layers work as a navigation system: HOW.md → domain spec → source files. Each layer tells you what the next layer can't tell you on its own. Do not skip layers — HOW.md tells you *which* spec to read, the spec tells you *what to look for* in the source files.

For purpose and values context, the parallel path is: WHY.md → conceptual model map → relevant design/ file. WHY.md indexes design/ the same way HOW.md indexes domain specs. If the task involves understanding *why* something works the way it does, consult WHY.md; if it involves understanding *how*, consult HOW.md; for many tasks, both are relevant.

If the project has no HOW.md, this mode doesn't apply — fall through to answering from the source files directly, and consider suggesting that the project could benefit from documentation.

## Creating HOW.md and Domain Specs from Scratch

### 1. Explore the codebase

Thoroughly explore the project structure. Identify:
- Distinct domains (groups of related source files with a cohesive purpose)
- Cross-cutting concerns (features that span multiple domains)
- External dependencies that affect architecture
- The project's tech stack and framework conventions
- Whether a `design/` directory exists with owner-authored conceptual models

### 2. Draft the domain map

Organize domains into a table. Group them by layer when it helps comprehension (e.g., foundation → business logic → UI).

Each domain needs:
- **Domain name** — short, descriptive
- **Description** — one line explaining what it does
- **Source files** — paths to the primary source files
- **Spec link** — relative link to the domain spec file

### 3. Identify cross-cutting concerns

Features that span multiple domains get a brief entry explaining which domains are involved and which spec to start reading from.

### 4. Write HOW.md

Use this structure:

```markdown
# How [Project Name] Works

This document maps the codebase into domains, each with a dedicated spec.
See [WHY.md](WHY.md) for project purpose and values, and
[README.md](README.md) for quick start.

Each spec is the authoritative reference for its domain. When code changes,
the relevant spec should be updated to match.

## Conceptual Models

If the project has a `design/` directory, note it here:

The `design/` directory contains the project owner's conceptual models —
how users think about the product. These are read-only context for
engineers and agents. [WHY.md](WHY.md) contains the conceptual model map
— use it to find the relevant model for your task. Domain specs should
reference the conceptual model they implement. When the implementation
diverges from a conceptual model, flag the divergence — don't silently
resolve it.

## Domain Map

| Domain | Description | Source Files | Spec |
|--------|-------------|-------------|------|
| [Name] | [One-line description] | `src/path/file.ts` | [spec-name.md](spec-dir/spec-name.md) |

## Cross-Cutting Concerns

- **[Feature]** — Spans [domains]. Start with [spec-name.md](spec-dir/spec-name.md).

## Spec Conventions

Specs are **briefing documents, not reference manuals**. They exist to tell
you what the code *can't* tell you on its own.

**Include:**
- Domain knowledge not evident from reading code
- Design decisions and their rationale
- Invariants and constraints
- Non-obvious edge cases and guard clauses
- Cross-domain relationships and dependency context

**Do not include:**
- Function signatures, parameter lists, or return types
- Type property tables or interface definitions
- State variable tables, event handler inventories, or props interfaces
- Anything an agent can learn by reading the source file directly

When updating a spec after a code change, ask: *"Would an agent need to know
this to work effectively, or could it just read the code?"* If the latter,
leave it out.

## Maintenance

This document and its specs should always reflect the current codebase.
When code changes, update the relevant spec. If a domain is added or
removed, update this table.
```

### 5. Write domain specs

For each domain, create a spec file in the spec directory following this structure:

```markdown
# [Domain Name]

## Conceptual Model
Implements: [design/relevant-file.md](../design/relevant-file.md) — what concepts from the model this domain covers
[Include only if a design/ file exists for this domain.]

## Source Files
- `path/to/file.ts`

## Dependencies
- [Other Domain](other-domain.md) — what's used from it and why

## Dependents
- [Consuming Domain](consuming-domain.md) — what it uses from this domain and why

## [Domain-Specific Sections]

[The substance. Include:
- Domain knowledge (rules, thresholds, formulas, conventions)
- Design decisions and why they were made
- Invariants that must hold
- Non-obvious edge cases
- Key constants and what they mean]
```

The Conceptual Model section links to the design/ file this domain implements, making the relationship between the owner's model and the technical implementation explicit. The Dependencies/Dependents sections are optional — omit them if the domain is standalone. Every link must include a description of what the linked document contains and why it's relevant, so an agent can decide whether to follow it without reading the target first. The domain-specific sections are the core value; their headings should reflect the actual content, not generic labels.

## Adding a New Domain

1. Explore the source files for the new domain
2. Write a spec file in the spec directory following the structure above
3. Add a row to the HOW.md domain map table
4. Update cross-cutting concerns if the new domain participates in any
5. Check if existing specs need new dependency/dependent links — add them freely
6. If a design/ file covers this domain, link to it from the new spec's `## Conceptual Model` section
7. If a design/ file should link back to this new spec, propose adding it to the design/ file's `## Implemented By` section — ask the owner for permission first

## Updating an Existing Spec

1. Read the current spec and its source files
2. Identify what changed — new behavior, removed feature, changed invariant
3. Update the spec to reflect current state
4. Apply the filter: only include what an agent can't learn from reading the code
5. Update HOW.md if the domain's description or source files changed
6. Check dependency/dependent links — are they still accurate? Add or remove freely
7. If the change diverges from a design/ conceptual model, note the divergence in the spec rather than silently accepting it
8. If the spec was renamed or its relationship to a design/ file changed, propose updating the design/ file's `## Implemented By` section — ask the owner for permission first

## Key Principles

- **WHY.md and design/ are read-only.** This skill manages HOW.md and domain specs only. Never modify WHY.md or files in design/. If you encounter a clear lack of direction in either that is harming work quality, suggest discussing it with the owner — but do not edit.
- **Conceptual models represent intent.** When the implementation differs from a design/ file, the conceptual model is what the owner wants the user to experience. Flag divergences so they can be resolved deliberately — either the implementation needs to change, or the owner needs to update the conceptual model.
- **Briefing documents, not reference manuals.** Specs tell you what the code can't tell you on its own. If an agent could learn it by reading the source file, leave it out.
- **Domain knowledge is the core value.** Rules, thresholds, formulas, conventions, invariants — the things that require understanding the problem space, not just the implementation.
- **Keep the domain map current.** HOW.md is the entry point. If it's stale, the whole system breaks down.
- **Specs have a dependency graph.** Cross-references between specs help an agent understand how domains interact without reading everything.
- **Linkages are the agent's responsibility.** Proactively identify stale, missing, or incorrect links in domain specs and HOW.md — and fix them freely. For links that touch owner-controlled files (design/, WHY.md), identify the issue and ask permission before editing. Every link must include a description of what the target contains, so agents can decide whether to follow it.
- **Follow links selectively.** Only pull in a linked document when it is directly relevant to the current task or when you need to check whether a change may introduce a regression. Link descriptions exist so you can make this decision without opening every file.
