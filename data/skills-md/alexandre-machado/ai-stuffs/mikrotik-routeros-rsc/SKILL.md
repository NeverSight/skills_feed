---
name: mikrotik-routeros-rsc
description: "Creation, editing, and review of RouterOS scripts (.rsc) with focus on idempotency, security, and best practices. Use when you need to generate, adjust, or import .rsc files for MikroTik: (1) create new configurations via script, (2) edit existing scripts with safe corrections, (3) review risks and execution policies, (4) validate with import dry-run and error handling."
---

# Skill: RouterOS .rsc

This skill guides the creation, editing, and review of RouterOS (.rsc) scripts with safe and idempotent patterns, plus validation before import.

## Quick workflow

1. Define script objective and scope.
2. Apply idempotent patterns (see References).
3. Validate syntax and risks with the linter (scripts/lint_rsc.py).
4. Test import with `dry-run` and `on-error`.
5. Import in a controlled manner to production.

## Essential practices

- Prefer `find where ...` + conditionals before `add`/`set`.
- Avoid broad policies in `/system script add policy=...`.
- Use `:onerror` and `:jobname` for robustness and single instance.
- Never include destructive commands (`system reset-configuration`, etc.).
- Parameterize and isolate scopes (`:local` vs `:global`).

## Validation and testing

- Lint: `python scripts/lint_rsc.py path/to/script.rsc`.
- Safe import (RouterOS ≥ 7.16.x):
  - `import test.rsc verbose=yes dry-run` to find multiple errors without applying changes.
  - `do { import test.rsc } on-error={ :put "Failure" }` to capture error.
  - `onerror e in={ import test.rsc } do={ :put "Failure - $e" }` for detailed message.

## References (use as needed)

- Language and syntax: see references/LANGUAGE.md
- .rsc export/import, `dry-run` and `onerror`: see references/RSC_GUIDE.md
- Security and idempotency best practices: see references/SAFE_PRACTICES.md
- Common examples and patterns: see references/EXAMPLES.md
- Linter rules: see references/LINTER_RULES.md

## Notes

- Scripts should be consistent with RouterOS v7 (preferred) and compatible with v6 where possible.
- Use `print as-value`, arrays, and `where` filters for robust queries.
- For scheduled execution, use Scheduler with appropriate permissions.
