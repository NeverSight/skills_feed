---
name: git-workflow
description: "[AUTO-INVOKE] MUST be invoked BEFORE creating git commits, PRs, or code reviews. Covers Conventional Commits, PR templates, review requirements, and AI-assisted development rules. Trigger: any task involving git commit, git push, PR creation, or code review."
---

# Git Collaboration Standards

## Language Rule

- **Always respond in the same language the user is using.** If the user asks in Chinese, respond in Chinese. If in English, respond in English.

## Commit Rules

Use Conventional Commits format: `<type>: <short description>`

| Type | When to use |
|------|------------|
| `feat:` | New feature or contract |
| `fix:` | Bug fix |
| `refactor:` | Code restructure without behavior change |
| `test:` | Add or update tests |
| `docs:` | Documentation changes |
| `chore:` | Build config, dependency updates, toolchain |
| `security:` | Security fix or hardening |

### Commit Workflow

1. Run `git diff` to review all changes before staging
2. Stage specific files — avoid `git add .` to prevent committing `.env` or artifacts
3. Write concise commit message describing the **why**, not the **what**
4. **Only commit** — never `git push` unless explicitly requested
5. **Never push directly to main/master** — always use feature branches

## Branch Naming

| Pattern | Example |
|---------|---------|
| `feat/<name>` | `feat/staking-pool` |
| `fix/<name>` | `fix/reentrancy-guard` |
| `refactor/<name>` | `refactor/token-structure` |

## PR Requirements

Every PR must include:

| Section | Content |
|---------|---------|
| Change description | What was changed and why |
| Test results | `forge test` output (all pass) |
| Gas impact | `forge test --gas-report` diff for changed functions |
| Deployment impact | Does this affect deployed contracts? Migration needed? |
| Review focus | Specific areas that need careful review |

## Code Review Rules

| Scenario | Requirement |
|----------|------------|
| Standard changes | Minimum 1 maintainer approval |
| Security-related changes | Minimum 2 maintainer approvals |
| AI-generated code | Must pass manual review + `forge test` before merge |
| Contract upgrades | Requires full team review + upgrade simulation on fork |

## AI Assistance Rules

- AI-generated code must pass `forge test` before committing
- Always review AI output for: correct import paths, proper access control, gas implications
- Include relevant file paths and test cases in AI prompts for better results
- Run `forge fmt` after AI generates code to ensure consistent formatting
