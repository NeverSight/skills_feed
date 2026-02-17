---
name: docs-writing
description: Writes and audits technical documentation using Diataxis, Stripe-style clarity, and the Eight Rules. 52 rules across 9 categories covering voice, structure, clarity, code examples, formatting, navigation, scanability, content hygiene, and review. Use when writing docs, creating READMEs, documenting APIs, writing tutorials, building a docs site, or auditing documentation quality.
---

# Documentation Writing

52 rules across 9 categories for documentation quality. Focuses on concrete issues with concrete fixes.

## Doc Writing/Audit Workflow

Copy and track this checklist during the audit:

```text
Doc writing/audit progress:
- [ ] Step 1: Determine doc type (tutorial, how-to, reference, explanation) and audience
- [ ] Step 2: Run CRITICAL checks (voice and tone, structure and organization)
- [ ] Step 3: Run HIGH checks (clarity and language, code examples)
- [ ] Step 4: Run MEDIUM+ checks for remaining categories in scope
- [ ] Step 5: Report findings with file:line and concrete fixes
```

1. Audit only changed files unless a full sweep is requested.
2. Identify the doc type (tutorial, how-to, reference, explanation) and intended audience to select relevant categories.
3. Load rule files progressively by category prefix — read only what applies.
4. Prioritize CRITICAL and HIGH findings before medium-priority polish.
5. After fixes, rerun the relevant rules before finalizing.

## Rule Categories by Priority

| Priority | Category | Impact | Prefix | Rules |
|----------|----------|--------|--------|-------|
| 1 | Voice & Tone | CRITICAL | `voice-` | 4 |
| 2 | Structure & Organization | CRITICAL | `structure-` | 10 |
| 3 | Clarity & Language | HIGH | `clarity-` | 6 |
| 4 | Code Examples | HIGH | `code-` | 7 |
| 5 | Formatting & Syntax | MEDIUM-HIGH | `format-` | 8 |
| 6 | Navigation & Linking | MEDIUM-HIGH | `nav-` | 6 |
| 7 | Scanability & Readability | MEDIUM | `scan-` | 2 |
| 8 | Content Hygiene | MEDIUM | `hygiene-` | 6 |
| 9 | Review & Testing | LOW-MEDIUM | `review-` | 3 |

## Quick Reference

Read only what is needed for the current scope:
- Category map and impact rationale: `rules/_sections.md`
- Rule-level guidance and examples: `rules/<prefix>-*.md`

Example rule files:

```
rules/voice-defaults.md
rules/structure-diataxis.md
rules/clarity-defaults.md
```

Each rule file contains:
- Why the rule matters
- Incorrect example
- Correct example

## Review Output Contract

Report findings in this format:

```markdown
## Documentation Audit Findings

### path/to/file.md
- [CRITICAL] `voice-defaults`: Passive voice obscures who performs the action.
  - Fix: Rewrite "The configuration is loaded by the server" as "The server loads the configuration."

### path/to/clean-file.md
- ✓ pass
```

- Group findings by file.
- Use `file:line` when line numbers are available.
- State issue and propose a concrete fix.
- Include clean files as `✓ pass`.
