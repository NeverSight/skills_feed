---
name: write-agents-entry
description: Write or revise AGENTS.md per embedded output contract. Use when creating Agent entry for new projects, auditing existing AGENTS.md, or adopting the AI Cortex entry format.
tags: [documentation, eng-standards]
version: 1.0.0
license: MIT
related_skills: [refine-skill-design]
recommended_scope: user
metadata:
  author: ai-cortex
---

# Skill: Write Agents Entry

## Purpose

Write or revise **AGENTS.md** at the repo root per the “Output contract” section below, so that when an Agent touches the project it has a clear **project identity**, **authoritative sources**, and **behavioral expectations**, and behaves consistently and predictably. The output contract is embedded in this SKILL.md so one load gives the full spec and steps.

---

## Use Cases

- **New project**: Add an Agent entry for a repo that has no AGENTS.md; produce a first draft following the output contract’s recommended structure and sections.
- **Revise existing entry**: Audit and complete an existing AGENTS.md (add missing sections such as authoritative sources, behavior, reference table) or fix wording that does not match the contract.
- **Adopt the format elsewhere**: Other projects can use this skill’s output contract to produce an AGENTS.md with identity, authority, and behavior, then replace asset types and paths for their project.
- **Compliance check**: Audit an existing AGENTS.md against the contract (§3 sections, §4 content, §6 reference table) and output revision suggestions.

---

## Behavior

1. **Read the contract first**: Before executing, read this file’s “Output contract” section and use it as the only source of truth; do not invent sections or drop recommended elements.
2. **Gather input**: From the user or context get: one-line project positioning, top-level asset types and dirs (e.g. skills/ and spec paths), whether a Raw URL is provided, primary description language. If information is missing, ask per the skill’s interaction policy.
3. **Produce by section**: Output or revise AGENTS.md in the contract §3 order: opening → Project identity → Authoritative sources → Behavioral expectations → Discovery and loading (summary) → Language and communication → Reference table. Section titles may be adjusted but keep the order: identity → authority → behavior → operations summary → language → reference.
4. **Executable behavior**: Use “must,” “shall,” “must not” (or equivalent) so each expectation is actionable; each item can reference a spec or doc. Do not paste full spec/docs into AGENTS.md; only index and summarize.
5. **Complete reference table**: Include at least: spec source, this entry’s Raw URL (if applicable), definition specs, usage and install, entry indexes; use relative paths or resolvable URLs.
6. **Self-check before submit**: After producing or revising, run this skill’s Self-Check; only submit when all pass. If the user asked only for a compliance audit, output a revision list instead of editing the file.

---

## Input & Output

### Input

- **One-line positioning**: What the project is (e.g. “agent-first, governance-ready capability inventory”).
- **Top-level assets and dirs**: Asset types (e.g. Skill), directories, spec paths (e.g. spec/skill.md); if a type is absent, say “none” or omit.
- **Optional**: AGENTS.md Raw URL, existing AGENTS.md or README excerpt (for revision), primary description language (e.g. English).

### Output

- **Authoring**: Full AGENTS.md that satisfies the output contract (or diff / revised full text).
- **Audit**: Compliance checklist and revision suggestions per contract §3–§6 (missing sections, reference table gaps, behavior wording); do not force-rewrite the file.

---

## Restrictions

- **Do not leave the contract**: Do not add sections as “required” that the contract does not require, or remove any of the seven recommended section types without justification.
- **Do not paste full specs**: Do not paste full content of spec/skill.md or other specs into AGENTS.md; only summarize and link.
- **No vague behavior**: Do not use “where possible,” “as appropriate,” etc.; use “must,” “shall,” “must not” (or equivalent).
- **Do not omit reference table**: The table must include spec source, definition/usage/install spec, entry indexes; if the project has no index, say “N/A” or omit that row.

---

## Self-Check

- [ ] **Contract**: Was the output contract read and §3 section order followed?
- [ ] **Three elements**: Are project identity, authoritative sources, and behavioral expectations clearly present?
- [ ] **Sections**: Opening, project identity, authoritative sources, behavior, discovery and loading (summary), language and communication, reference table?
- [ ] **Executable**: Does behavior use “must”/“shall”/“must not” (or equivalent) with each item mappable to a spec or doc?
- [ ] **Reference table**: At least spec source, this entry Raw URL (if applicable), definition spec, usage and install, entry indexes?
- [ ] **No duplication**: Does AGENTS.md avoid repeating full spec/docs text and only index and summarize?

---

## Examples

### Example 1: New project (minimal info)

**Input**: Project: my-cli. One-line: A CLI for local batch file renaming. Assets: no skills, only README and source. Want an Agent entry; primary language English.

**Expected**: Produce AGENTS.md with: opening (this file is the Agent entry and contract), project identity (one line + asset table; can be simplified to “docs/source” etc.), authoritative sources (definitions and catalog from README or docs/), behavioral expectations (several “must” items), discovery and loading (summary if INDEX or equivalent exists, else how the Agent should understand the project), language and communication (English), reference table (spec source, this entry Raw if applicable, docs and entry links). Do not invent spec/ paths that do not exist.

### Example 2: Edge case — incomplete AGENTS.md

**Input**: Existing AGENTS.md has only “This project is XX” and “Read INDEX,” no authoritative sources, no behavior, no reference table. Project has docs/, README, no skills. Complete per the output contract.

**Expected**: Keep existing “project identity”; add authoritative sources (where definitions and catalog live), behavioral expectations (at least 2–3 executable items, e.g. “Follow README and docs,” “When listing capabilities, read index then enumerate”), discovery and loading (summary), language and communication, reference table. Do not remove correct user wording; if the project has no INDEX, reference table can say “N/A” or list README/docs. Output revised full text or diff and state which sections were added.

---

## Output contract: AGENTS.md authoring standard

The following is the standard used by this skill when producing AGENTS.md; it is embedded in this SKILL.md. Projects adopting the “agent-first, governance-ready capability inventory (Spec)” shape can use it; this repo’s [AGENTS.md](../../AGENTS.md) follows it.

### 1. Purpose and role

- **AGENTS.md** is the **single entry and contract** for AI Agents interacting with the project; it is usually at the repo root.
- **Purpose**: When an Agent touches the project, define **project identity**, **authoritative sources**, and **behavioral expectations** so the Agent behaves consistently and predictably in or when referencing the repo.
- **Audience**: Agents that can read files (e.g. IDE Agent, CLI Agent); can also be used by consumer repos that reference it via Raw URL.

### 2. Primary goals

AGENTS.md’s main goal is not “teach the Agent how to use skills” but to establish **entry and behavior**. That means three things:

| Goal | Description |
| :--- | :--- |
| **Project identity** | One sentence on what the project is; list top-level asset types (e.g. Skills), their directories, and definition specs. |
| **Authoritative sources** | Where “definitions” and “catalog/list” live; the Agent treats these as truth, not verbal or scattered docs. |
| **Behavioral expectations** | What the Agent **must or must not** do in or when referencing the project (e.g. follow spec, self-check before submit, read index then enumerate when listing capabilities). |

### 3. Recommended structure and sections

Organize in this order for both Agents and humans:

| Order | Section | Content |
| :--- | :--- | :--- |
| 1 | **Opening** | One sentence: this file is the Agent entry and contract; purpose (identity + authority + behavior). |
| 2 | **Project identity** | One-line positioning + asset type/dir/spec table + catalog and manifest (if any). |
| 3 | **Authoritative sources** | Where definitions, catalog/list, and usage contract live; pointers only, no long detail. |
| 4 | **Behavioral expectations** | Numbered expectations the Agent must follow; each can reference a spec or doc. |
| 5 | **Discovery and loading (summary)** | Asset root, how to discover, how to inject; details in AGENTS.md §4 or equivalent; avoid repeating in AGENTS.md. |
| 6 | **Language and communication** | Primary description language and terminology; align with spec/skill or equivalent. |
| 7 | **Reference** | Table: spec source, this entry Raw URL (if applicable), definition spec, usage and install, entry indexes. |

Section titles and levels can follow project style, but keep the order: identity → authority → behavior → operations summary → language → reference.

### 4. Content requirements

- **Executable expectations**: Use “must,” “shall,” “must not” (or equivalent) so the Agent can parse and follow.
- **Do not duplicate spec and docs**: AGENTS.md indexes and summarizes; point to `spec/` or `docs/` for full definitions and install.
- **Stable references**: Use relative paths or resolvable URLs to specs and indexes in the repo; if the project can be referenced via Raw URL, provide the canonical Raw URL for AGENTS.md in the reference table.

### 5. Format and style

- **Headings**: Short and parseable; optional English subtitle (e.g. “Agent Entry”).
- **Length**: Aim for about one page (e.g. 60–80 lines) so the Agent can load and parse in one go.
- **Language**: Match the project’s main asset language; if the project uses English, see [spec/skill.md](../../spec/skill.md) language requirements.
- **Tables**: Use Markdown tables for project identity, authoritative sources, and reference for structured parsing.

### 6. Reference table

- End with a **reference table** listing at least: spec source, this entry Raw URL (if Raw reference is supported), definition specs (e.g. spec/skill), entry indexes (e.g. skills/INDEX.md). Usage is in AGENTS.md §4. The table lets Agents and tools jump to authoritative docs without crawling the repo.

### 7. Relation to other specs

- **Usage**: Runtime behavior for discovery, injection, and self-check is in AGENTS.md §4; AGENTS.md is the single entry and contract.
- **Language**: AGENTS.md’s description and communication expectations should align with [spec/skill.md](../../spec/skill.md) language requirements (if the project uses that spec).

### 8. Adapting for other projects

Other projects adopting this contract can: keep the three elements (identity, authority, behavior) and the recommended section order; replace “project identity” with their one-line positioning and asset table; replace paths and spec names in “authoritative sources,” “behavior,” and “discovery and loading” with their `spec/` or equivalent; if the project has no Skills or INDEX, omit or replace with that project’s top-level assets and dirs, and adjust the reference table accordingly.
