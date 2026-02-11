---
name: refine-skill-design
description: Audit and refactor existing SKILLs. Use when improving drafts, fixing quality, or aligning to spec. For creating new skills from scratch use skill-creator (anthropics/skills).
tags: [writing, eng-standards, meta-skill, optimization]
related_skills: [decontextualize-text, generate-standard-readme]
version: 1.2.0
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
---

# Skill: Refine Skill Design

## Purpose

As a "Skill for Skills," this skill **audits and refactors** AI capability definitions in draft form. It applies a senior prompt-engineering perspective to improve logic robustness, scenario coverage, and instruction adherence so each capability meets LLM best practices.

---

## Use Cases

- **New skill onboarding**: Expert review after an Agent has generated a new Skill draft.
- **Quality fixes**: When a Skill behaves inconsistently on newer models, align logic and strengthen examples.
- **Consistency audit**: Check that a new Skill matches the tagging system and naming in `INDEX.md`.
- **Upgrade**: Turn a simple "formatting tool" into a full Agent capability with interaction policy and error handling.

**Scope**: This skill is for **auditing and refactoring existing SKILLs**, not creating from scratch. For learning how to create new skills, plan scripts/references/assets, or run init/package scripts, use skills.sh's `skill-creator` (e.g. anthropics/skills).

---

## Behavior

### Meta-audit model

1. **Intent**: Is Purpose specific enough? Avoid vague terms like "Helper," "Utilities."
2. **Logic**: Does Input → Behavior → Output form a clear chain?
3. **Constraints**: Do Restrictions cover the most common failure modes in the domain?
4. **Examples**: Do Examples progress from simple to complex and include at least one edge case?

### Optimization flow

1. **Structure**: Apply the standard template (YAML, Purpose, Use cases, Behavior, I/O, Restrictions, Self-Check, Examples).
2. **Verbs**: Use precise, unambiguous verbs (e.g. "handle" → "parse," "transform," "trim").
3. **Interaction**: For complex logic, add "confirm before proceed" or "choose among options."
4. **Metadata**: Align tags with `INDEX.md` and suggest a sensible SemVer version.

---

## Input & Output

### Input

- A SKILL Markdown document to optimize, or a rough draft.

### Output

- **Optimized SKILL**: Production-grade Markdown that satisfies the spec.
- **Diff summary**: What was changed and why.
- **Version suggestion**: SemVer recommendation.

---

## Restrictions

- **Do not change intent**: Optimization must preserve the skill's core purpose.
- **Minimize prose**: Prefer lists and tables over long README-style text.
- **Multiple examples**: Do not keep only one "happy path" example; include at least one challenging or edge-case example.

---

## Self-Check

- [ ] **Self-apply**: Could this skill successfully refine itself?
- [ ] **Clarity**: Could an Agent without domain background reproduce results from Behavior?
- [ ] **Compliance**: Are all required sections and metadata fields present?

---

## Examples

### Before

> name: spell-check
> This skill checks spelling.
> Input: multilingual text.
> Output: corrected text.

### After

> name: polish-text-spelling
> description: Context-aware spelling and terminology correction for multilingual documents.
> tags: [writing, quality-control]
> version: 1.1.0
> ---
> # Skill: Spelling and terminology
> ## Purpose: Identify and fix low-level spelling errors and terminology inconsistency without changing the author's intent or tone.
> ## Behavior:
> 1. Detect language.
> 2. Build a term list if the text is long.
> 3. Distinguish "typos" from "intentional style."
> ## Restrictions: Do not change proper nouns or specific abbreviations unless clearly wrong.

### Example 2: Edge case — ambiguous draft

- **Input**: A Skill draft whose Purpose is "help users handle files," with no Use Cases or Restrictions.
- **Expected**: Pin down intent (replace "handle" with concrete verbs: parse, convert, merge, etc.); add Use Cases and Restrictions (e.g. do not overwrite source; do not modify binaries); add at least one edge example (e.g. empty file, very large file, permission denied).

---

## Appendix: Output contract

When this skill produces a refinement, the output MUST satisfy this contract so that Agents and downstream tools can consume it consistently:

| Element | Requirement |
| :--- | :--- |
| **Optimized SKILL** | Full Markdown content (or path to file). MUST satisfy [spec/skill.md](../../spec/skill.md): YAML front matter, Purpose, Use cases, Behavior, I/O, Restrictions, Self-Check, and at least one Example. |
| **Diff summary** | List of changes. Each entry MUST include **Section** (e.g. `Purpose`, `Behavior`, `metadata`), **Change** (short description of what was changed), and **Reason** (why the change was made). |
| **Version suggestion** | SemVer string `major.minor.patch`. Optionally **Rationale** (e.g. `minor: added Restrictions`). |
