---
name: archive-and-cleanup-vibe-docs
version: "1.0.0"
description: >
  Consolidates and archives durable engineering knowledge from vibe coding
  documents, generates PR-ready summaries, and removes all temporary planning
  artifacts before merge.
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

## When to Trigger

Use this skill **only after**:

* A feature or refactor is fully implemented
* The agent is about to open or finalize a PR
* Temporary documents were created during exploration, planning, or iteration

Do **not** use during active development.

---

## Inputs

The agent may have access to:

* Temporary documents such as:

  * `plan*.md`
  * `progress*.md`
  * `task*.md`
  * design notes, brainstorm files, agent logs
* The final code changes
* Existing project documentation structure

---

## Core Objective

Transform **process artifacts** into **durable engineering assets**, while ensuring:

1. PRs remain clean and reviewer-friendly
2. Long-term design decisions are preserved
3. Temporary documents do not accumulate in the repository

---

## Execution Steps (MANDATORY)

### Step 1: Inventory & Classification

Scan all temporary documents produced during the task and classify each into **one** of the following categories:

1. **Durable Design Knowledge**

   * Architecture decisions
   * Key abstractions and boundaries
   * Important trade-offs (Why X, not Y)

2. **PR-Level Context**

   * Background needed to understand the change
   * Scope clarification
   * Explicit non-goals

3. **Process Noise**

   * Daily progress logs
   * Task checklists
   * Iteration history
   * Prompt drafts or agent conversations

---

### Step 2: Knowledge Extraction & Consolidation

#### 2.1 PR Summary (REQUIRED)

Produce a concise, reviewer-oriented summary suitable for a PR description, containing:

* Background (problem being solved)
* Final design decisions (only conclusions)
* Scope and non-scope
* Follow-up items (if any)

⚠️ Do NOT include:

* Chronological progress
* Failed attempts in detail
* Raw task lists

---

#### 2.2 Architecture / Design Documentation (CONDITIONAL)

If (and only if) durable design knowledge exists:

* Create or update documentation under one of the following:

  * `docs/architecture/<feature>/`
  * `docs/decisions/`
  * module-local `docs/`

Strongly prefer **ADR-style documents**:

```md
# ADR-XXX: <Decision Title>

## Context
## Decision
## Consequences
```

Only extract **final decisions**, not exploration history.

---

### Step 3: Issue & Follow-up Migration

If any temporary documents contain:

* TODOs
* Deferred ideas
* Known limitations

Then:

* Convert them into GitHub Issues or explicit Follow-up notes
* Remove them from temporary documents

---

### Step 4: Cleanup (MANDATORY)

After successful extraction:

1. **Delete all temporary vibe coding documents** from the repository, including but not limited to:

   * plan files
   * progress logs
   * task trackers
   * brainstorming notes

2. Ensure:

   * No references to deleted files remain
   * No broken links in docs or PR description

⚠️ Temporary documents must **not** be committed in the final PR.

---

## Output Requirements

At the end of execution, the agent must produce:

1. ✅ A PR-ready summary (text only)
2. ✅ Any new or updated durable documentation
3. ✅ A clean repository state with all temporary documents removed

---

## Strict Rules

* Never commit raw vibe coding documents
* Never include thinking logs or agent conversations
* Prefer clarity and durability over completeness
* If unsure whether something is durable, **exclude it**

---

## Mental Model

> Temporary docs are **raw material**.
> The repository only accepts **finished products**.

---

## Success Criteria

This skill is successful if:

* A reviewer can understand the PR without reading any temporary documents
* The repository contains only long-lived, intentional documentation
* No vibe coding artifacts remain after merge

