---
name: odoo-commit-message-guidelines
description: "Draft, rewrite, and validate Odoo-style commit messages using [TAG] module: summary format, 50/72 length limits, imperative English, WHY-first body, and correct tag selection. Includes optional migration tagging ([MIG]) when the project workflow (like OCA) uses it."
---

# Odoo Commit Message Guidelines

## Purpose

Use this skill to produce high-quality Odoo commit messages that are consistent,
reviewable, and easy to revert.

## Local References

This skill includes reference material in:

- `references/git_guidelines.md` (official Odoo commit message conventions)
- `references/CONTRIBUTING.md` (OCA contribution and commit message extensions)

Use these files as source context when user requests stricter validation,
edge-case tagging decisions, or policy justification.

## When To Use

Use this skill when the user asks to:

- write a new commit message for Odoo code
- rewrite or improve an existing commit message
- validate whether a commit message follows Odoo rules
- choose the correct Odoo tag

## Required Inputs

Before drafting, collect:

- modified module name (or `various` for cross-module commits)
- change type and intent (bug fix, refactor, migration, etc.)
- core rationale (WHY the change is needed)
- notable implementation choices (only if relevant)
- references (`task-*`, `ticket-*`, `Fixes #`, `Closes #`, `opw-*`) when available
- specific CI directives (e.g., `[NO CI]`) if mentioned by the user

If required inputs are missing, ask only the minimum concise follow-up questions.

## Output Format

Use this structure:

```text
[TAG] module: short summary (ideally < 50 chars)

WHY the change is needed.
WHAT changed and technical choices (only if useful).

task-123
ticket-12345
Fixes #123
Closes #456
opw-789
```

Rules:

- Commit message must be in English.
- Header must start with a tag from `Tag Selection Rules` in this exact pattern: `[TAG]` (e.g., `[FIX]`, `[ADD]`).
- The tag must be uppercase and enclosed in brackets; reject lowercase or malformed tags.
- Keep header concise; target about 50 characters in the summary part.
- Body must be multiline and wrapped to 72 characters per line.
- Body should use structured plain text (lists using `*` or `-`). Avoid advanced Markdown (like tables) since commit messages are read in terminals.
- Use imperative present voice: `Fix`, `Remove`, `Add` (not `Fixes`, `Removes`).
- Make the header meaningful; avoid generic summaries like `bugfix`.
- Prioritize WHY over WHAT in the body.

Compatibility note:

- Official Odoo documentation does not define `[MIG]` as a core tag.
- `[MIG]` is the official standard for Odoo Community Association (OCA) repositories. If the repository workflow uses migration tags, `[MIG]` can be used.

## Tag Selection Rules

Choose exactly one main tag for the commit:

- `[FIX]` bug fix
- `[REF]` major refactor / heavy rewrite
- `[ADD]` add a new module
- `[REM]` remove dead code/resources/modules
- `[REV]` revert an earlier commit
- `[MOV]` move files/code while preserving history intent
- `[REL]` release commit
- `[IMP]` incremental improvement
- `[MERGE]` merge / forward-port integration commit
- `[CLA]` individual contributor license signature
- `[I18N]` translation updates
- `[PERF]` performance improvement
- `[CLN]` cleanup
- `[LINT]` linting pass
- `[MIG]` module migration (only when the project convention supports it)

Decision guidance:

- Prefer the tag that best captures intent, not file type.
- If it is clearly a migration, use `[MIG]`.
- If it fixes a regression while migrating, split into two commits when possible.
- Avoid stacking multiple tags in one header.

## Module Naming Rules

- Use technical module name, not marketing/functional display names.
- If multiple modules are touched, list them briefly or use `various`.
- Prefer one logical change per commit and avoid large cross-module commits.

## Writing Workflow

1. Identify the smallest logical change set.
2. Choose the module scope.
3. Select the tag from the rule set above.
4. Draft header: `[TAG] module: imperative summary`.
5. Draft body with WHY first, then concise WHAT if needed (plain text, wrapped at 72 chars).
6. Add references and CI directives at the end using canonical formats.
7. Validate against checklist before returning.

## Validation Checklist

Confirm all items:

- Header follows `[TAG] module: summary`.
- Header starts with exactly one valid tag from `Tag Selection Rules`.
- Tag token is uppercase and bracketed (`[FIX]`, not `[fix]` or `FIX`).
- Summary is concise and not truncated with ellipsis in PR UI.
- Body lines are wrapped at max 72 characters.
- Body formatting avoids advanced Markdown, using simple plain text.
- Rationale (WHY) is explicit.
- Verb tense is imperative present.
- Tag matches change intent.
- Module naming is technical and accurate.
- Commit scope is a single logical change set.
- References are formatted correctly when present.

If any check fails, rewrite the message before returning.

## Good Examples

```text
[FIX] website: remove unused alert div

Fix the look of input-group-btn.
Bootstrap requires input-group-btn to be the first or last child.
An invisible alert node broke that structure and produced visual issues.

Fixes #22769
Closes #22793
```

```text
[FIX] various: resolve rounding issues in currency conversions

Address inconsistent decimal rounding behavior across multiple reporting
and accounting modules. Instead of allowing components to do ad-hoc
rounding, enforce standard decimal precision in the core tools.

ticket-10928
[NO CI]
```

```text
[IMP] web: add module system to web client

Introduce a module system for JavaScript code to improve isolation,
load order control, and maintainability as the client grows.
```

```text
[MIG] stock_account: migrate valuation hooks to 19.0

Align valuation hook signatures with 19.0 API to preserve extension
compatibility and avoid runtime errors during upgrade.

task-8421
```

## Anti-Patterns To Reject

Reject and rewrite messages with:

- generic headers (`bugfix`, `improvements`)
- missing module name
- missing rationale
- past tense or third-person verbs in header
- oversized multi-topic commits in one message
- truncated first line (`...`) caused by long header

## Response Behavior

When asked to produce a commit message:

1. Return only the raw commit message (no code fences) unless the user asks for explanation.
2. If info is missing, ask only the minimum necessary clarifying questions.
3. If user provides a draft, return a corrected Odoo-compliant version.
4. Be strict: if the header does not begin with one uppercase bracketed tag from `Tag Selection Rules`, rewrite it before returning.
5. For IDE Source Control usage, return a ready-to-use commit message suggestion that can be inserted directly in the Source Control commit box (no preamble, no labels, no markdown).
6. **Execution Offer**: After providing the generated commit message, **proactively offer to execute the commit** using `git commit -m "..." -m "..."`. Always ask for explicit user confirmation before running the `git commit` command. Do not execute the commit automatically.

## Usage Examples

### Scenario 1: Create a new commit message

**User:** "Write an Odoo commit message for a bug fix in `sale_stock` where delivered qty was computed twice. Reference task-9123."

**Agent behavior:**

1. Identify tag as `[FIX]` and module as `sale_stock`.
2. Draft concise header in imperative form.
3. Explain WHY first in body, then concise WHAT.
4. Append `task-9123` as reference.
5. Suggest the commit message and ask: *"Would you like me to execute this commit for you?"*

### Scenario 2: Rewrite an existing draft

**User:** "Improve this commit message: `fixed stuff in stock module`"

**Agent behavior:**

1. Reject generic summary and missing rationale.
2. Ask minimum questions if context is missing (what bug, why needed).
3. Return corrected message in Odoo format.
4. Offer to execute the commit if the user is satisfied.

### Scenario 3: Validate tag choice

**User:** "I changed API hooks for 19.0 migration and also fixed a small bug. Should I use `[MIG]` or `[FIX]`?"

**Agent behavior:**

1. Prefer `[MIG]` for migration intent.
2. Recommend splitting migration and bug fix into separate commits when possible.
3. Provide one valid commit message for each resulting commit if requested.
4. Offer to stage and execute both commits sequentially.

