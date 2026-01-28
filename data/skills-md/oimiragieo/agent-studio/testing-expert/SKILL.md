---
name: testing-expert
description: DEPRECATED - Use 'tdd' skill instead. Testing-expert has been merged into tdd.
version: 1.0.1
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Grep, Glob]
deprecated: true
deprecated_reason: Merged into tdd skill
redirect_to: tdd
---

# Testing Expert (DEPRECATED)

> **DEPRECATION NOTICE**: This skill has been merged into the `tdd` skill.
>
> **Use instead:** `Skill({ skill: "tdd" })`
>
> The `tdd` skill now includes all testing-expert capabilities plus comprehensive TDD methodology.

## Redirect

The `tdd` skill now provides:

- **TDD Methodology**: Red-Green-Refactor cycle with Iron Laws
- **Framework Testing**: Angular (Jasmine/Karma), Cypress, Playwright
- **Anti-Patterns**: Testing anti-patterns reference guide
- **Verification**: Verification checklists for test quality

## Migration

If you were using `testing-expert`, switch to:

```javascript
// Before
Skill({ skill: 'testing-expert' });

// After
Skill({ skill: 'tdd' });
```

The `tdd` skill includes an `aliases: [testing-expert]` directive, so invoking `testing-expert` will automatically load the `tdd` skill.

## Original Content

For reference, the original testing-expert content has been incorporated into the `tdd` skill's "Framework-Specific Testing Guidelines" section.

---

**Deprecated on:** 2026-01-25
**Merged into:** `.claude/skills/tdd/SKILL.md`
