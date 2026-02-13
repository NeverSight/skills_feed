---
name: decontextualize-text
description: Convert text with private context or internal dependencies into generic, unbiased expressions. Use for project decontextualization (handoff, open-source prep), methodology abstraction, cross-team sharing, anonymization. Includes path strings and file/folder names as they appear in text.
tags: [writing, security, privacy, generalization]
related_skills: [generate-standard-readme]
version: 1.3.0
license: MIT
recommended_scope: user
metadata:
  author: ai-cortex
---

# Skill: Decontextualize Text

## Purpose

Turn content that **depends on private context, implicit assumptions, or environment-specific details** into **generic, reusable wording**. Primary scenario: **project decontextualization** — preparing a project for handoff, open-source, or cross-org use. By removing or replacing specific identifiers (including path strings and file/folder names as they appear in text), the content can be understood correctly in different contexts while protecting organizational privacy.

---

## Use Cases

- **Project decontextualization**: Prepare a project for handoff or open-source — decontextualize docs, README, comments; replace path strings and file/folder names (as they appear in text) with generic equivalents (e.g. `acme-internal/config.yaml` → `project-root/config.yaml`).
- **Generalization**: Turn project-specific lessons into generic methodology or best practices.
- **Cross-team collaboration**: Remove jargon or codenames that only one team understands so others can read the doc without extra context.
- **De-identification**: Before sharing case studies or blog posts, strip sensitive project names, people, and internal addresses.
- **Release preparation**: Final cleanup before publishing internal content externally (e.g. open source, handoff).
- **Doc sync**: After forking or merging cross-org repos, clean up outdated environment-specific descriptions.

**When to use**: When you need to remove “understanding barriers due to environment differences” or “information security boundaries.”

---

## Behavior

### Principles

- Keep **what is done** and **why**.
- Remove **who**, **where**, and **which internal conditions**.
- Replace proper nouns with generic descriptions (e.g. “internal system”, “a given workflow”).
- Make implicit assumptions explicit or drop them.

### Interaction policy

- **Uncertain terms**: When you spot possibly sensitive or internal terms (e.g. unclear abbreviations, internal server names), **list them** and ask the user to confirm before rewriting.
- **Alternatives**: For core logic, offer 2–3 rewrite options at different abstraction levels for the user to choose.

### Steps

1. **Identify sensitive terms**: Scan for company names, project codenames, internal URLs, people’s names, **path strings**, and **file/folder names** that carry internal context (e.g. `acme-internal/`, `team-alpha-output/`).
2. **Extract core logic**: Identify the essence of the steps (e.g. “JIRA approval” → “task state change review”).
3. **Rewrite generically**: Use neutral wording for the identified parts.
4. **Preserve structure**: Keep paragraph structure and capability boundaries; do not drop information.

---

## Input & Output

### Input

- Text that has one or more of:
  - Organization, company, project, or system names.
  - **Path strings and file/folder names** that carry internal context (e.g. `acme-internal/config.yaml`, `team-alpha/output/`).
  - Internal conventions, implicit context, or default assumptions.
  - Processes or assumptions that only hold in a specific environment.

### Output

- **Generic version**: Text with private context removed or replaced.
- **Structure preserved**: Logic hierarchy, Markdown, and functional instructions must be preserved.
- **Reusable**: Output should be usable without extra context.

---

## Restrictions

- **No invention**: Do not invent context or capabilities not in the original.
- **No inference**: Do not add facts or conclusions not stated.
- **No new semantics**: Do not introduce new business meaning.
- **No residue**: Do not leave anything that can re-identify an organization or person (e.g. unique IDs, internal process numbers, non-public terms).

---

## Self-Check

- [ ] **Standalone**: Content is fully understandable without the original context.
- [ ] **Anonymous**: Hard to infer which company or project it came from.
- [ ] **Consistent**: Core logic and function match the original.
- [ ] **Compliant**: Meets de-identification or public-release privacy standards.

---

## Examples

**Example 1: Internal process → generic**

| Original | Decontextualized |
|----------|------------------|
| In Acme’s JIRA workflow, when a requirement enters “Tech Review”, run X team’s Checklist, then notify PM Li Si. | When a requirement enters the “Tech Review” stage, run the defined Checklist and notify the relevant product owner. |

**Example 2: System and API → neutral**

| Original | Decontextualized |
|----------|------------------|
| Call gpt-4 via our company LLM Gateway (api.acme.internal), timeout 30s. | Call the model via an LLM API; set a reasonable timeout (e.g. 30s). |

**Example 3: Team-specific rule → abstract**

| Original | Decontextualized |
|----------|------------------|
| Per Kiro team policy, Python must pass `pylint` with score ≥ 9.0 before merging to `master`. | Per code quality policy, code should pass static checks (e.g. `pylint`) and meet the required threshold before merging to the main branch. |

**Example 4: Path and file/folder names in docs**

| Original | Decontextualized |
|----------|------------------|
| Config is in `acme-internal/settings.yaml`. Output goes to `team-alpha/output/`. | Config is in `project-root/settings.yaml` (or `config/settings.yaml`). Output goes to `output/`. |

---

## Appendix: Output contract

When this skill produces decontextualized text, it follows this contract:

| Element | Requirement |
| :--- | :--- |
| Preserve | What is done and why; logic hierarchy; Markdown structure; functional instructions. |
| Remove | Who, where, internal conditions; proper nouns → generic descriptions; path strings and file/folder names → generic equivalents. |
| Interaction | When uncertain terms appear: list them and ask user to confirm before rewriting. |
| Restrictions | No invention, inference, new semantics, or residue that could re-identify org/person. |
