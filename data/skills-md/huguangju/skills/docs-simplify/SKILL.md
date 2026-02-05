---
name: docs-simplify
description: Simplify technical/product documentation without changing meaning, keeping structure and key terms intact
metadata:
  author: Carson
  version: "2026.2.3"
---

# Documentation Simplification (Meaning-Preserving)

Transform technical/product docs into shorter, clearer text **without altering meaning**. Preserve terminology, APIs, paths, config keys, and (unless allowed) structure.

---

## Usage Scenarios

**Use this Skill when you need to:**
- Shorten documentation while preserving meaning
- Keep technical identifiers unchanged (APIs, paths, config keys)
- Improve clarity and consistency across multiple docs

**Do NOT use this Skill when:**
- You need structural rewrites or marketing copy
- You need translation/localization
- You must add new content or change technical facts

---

## Core Principles

1. **Meaning first** — never change constraints or behavior.
2. **Identifiers are sacred** — APIs/paths/config keys remain unchanged.
3. **Structure is stable** — keep headings and code blocks unless explicitly allowed.
4. **Brevity with precision** — shorter, but still exact.

---

## Workflow

1. **Confirm scope**: target files, audience, and whether headings can change.
2. **Scan structure**: map headings, lists, tables, and code blocks; flag verbose sections.
3. **Simplify**:
   - Sentence level: remove redundancy, merge repeats, use active verbs.
   - List level: dedupe items, compress descriptions, keep all information.
   - Table level: shorten “description/usage” cells while retaining key terms.
4. **Guardrails**:
   - Do not change meaning or technical identifiers.
   - Keep code blocks and examples unless clearly redundant.
   - Keep heading hierarchy unless permission to restructure.
5. **Consistency pass**: terminology, punctuation, and tone.
6. **Summarize changes**: list edited files and high‑level edits.
7. **Handle ambiguity**: if a change could alter meaning, ask a minimal clarification.

---

## Quality Gates

- No technical identifiers changed.
- No meaning/constraints altered.
- Code blocks and paths preserved.
- Lists/tables remain complete.

---

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Concise Editing Guide | Rules and examples for meaning‑preserving edits | [reference](references/concise-editing.md) |
