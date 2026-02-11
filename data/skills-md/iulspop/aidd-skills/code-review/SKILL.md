---
name: code-review
description: Reviews code changes for correctness, maintainability, security, and adherence to project conventions. Use when reviewing PRs, auditing recent changes, or getting a second opinion on implementation quality.
---

# Code Review

Act as a senior engineer reviewing a pull request. Be direct and specific.

Review: $ARGUMENTS

## Checklist

For each file changed, evaluate:

1. **Correctness** — Does the code do what it claims? Are edge cases handled? Are there off-by-one errors, race conditions, or null dereferences?
2. **Tests** — Are new behaviors covered? Do test names follow "given/should" format? Are assertions specific (no `expect.any`)?
3. **Security** — Any injection risks (SQL, XSS, command)? Secrets in code? Unvalidated user input reaching sensitive operations?
4. **Naming** — Do function/variable names follow project conventions? Are they descriptive without being verbose?
5. **Architecture** — Does the change respect layer boundaries (domain, infrastructure, application)? Are imports valid per the project's import rules?
6. **Simplicity** — Is there unnecessary complexity, premature abstraction, or dead code? Could it be simpler?
7. **Style** — Does it follow the project's lint rules, formatting, and existing patterns?

## Rules

- Read the full diff before commenting. Understand context first.
- Be specific: reference file paths and line numbers.
- Distinguish between blocking issues (must fix) and suggestions (nice to have).
- Don't nitpick formatting if biome/linter handles it.
- Flag any changes that lack tests.
- Flag any changes that break the public API without a migration path.
- If the code is good, say so briefly. Don't invent problems.

## Output Format

```
## Summary
<1-2 sentences on overall assessment>

## Blocking Issues
- **file:line** — description of issue and suggested fix

## Suggestions
- **file:line** — description and rationale

## Looks Good
- <list of files that need no changes>
```
