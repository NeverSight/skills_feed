---
name: project-setup
description: Bootstrap new projects with strong typing, linting, formatting, and testing. Supports Python, TypeScript, and other languages with research fallback.
---

# Project Setup

## Core Principles

- **Strong Typing**: Strict mode enabled; types catch bugs at compile time
- **Strong Linting**: Strict rules by default; easier to disable than add later
- **Auto Formatting**: Automated and consistent; no manual formatting
- **Checks at Every Stage**: Pre-commit hooks + CI; catch issues early
- **Co-located Tests**: `foo.ts` → `foo.test.ts`; obvious what's tested
- **Behavior-Focused**: Test what code does, not how; mock only external boundaries

## Workflow

1. Check `reference/` for language guide (Python, TypeScript)
2. If no guide: WebSearch "[language] project setup best practices"
3. Follow setup: typing → linting → formatting → testing → pre-commit → CI
4. For existing projects: migrate incrementally in same order

## Reference Files

- `reference/python.md` - uv, ruff, basedpyright, pytest
- `reference/typescript.md` - pnpm, ESLint, Prettier, Vitest
- `reference/common-patterns.md` - Testing philosophy, CI patterns, security

## Tool Selection

Prefer tools that are: ecosystem standard, actively maintained, strict by default, fast, well-integrated (editor + CI + pre-commit).

## Quality Checklist

- [ ] Typing: Strictest mode, no `any` without justification
- [ ] Linting: Strict rules, warnings as errors
- [ ] Formatting: Auto-format on save + pre-commit
- [ ] Testing: Co-located tests, coverage >80%
- [ ] Pre-commit: Format, lint, type-check
- [ ] CI: Same checks + coverage reporting
- [ ] README: Setup instructions
- [ ] All checks pass on initial commit
