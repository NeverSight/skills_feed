---
name: git-commit-messages
description: Generates consistent git commit messages following project conventions. Use when committing changes, creating PRs, or when asked to write commit messages.
---

# Git Commit Message Generator

## Format

```
type(scope): subject in imperative mood

- Body bullet in past tense with period.
- Another change description.
```

## Types

| Type | When to Use |
|------|-------------|
| `feat` | Added new functionality |
| `fix` | Fixed a bug |
| `refactor` | Restructured code, no behavior change |
| `chore` | Dependencies, tooling, configs |
| `docs` | Documentation |
| `test` | Tests |
| `cicd` | CI/CD pipelines, deployment, `.github/` configs (workflows, dependabot, etc.) |
| `ai` | AI/Claude configurations |

## Rules

1. **Subject**: Imperative mood, lowercase after colon, no period, max 72 chars
2. **Scope**: Derived from path (e.g., `apps-server`, `apps-expo`, `shared-domain`, `scripts`, `services`). When changes span multiple scopes, omit the scope entirely
3. **Body**: Past tense, capital start, period at end
4. **No attribution**: Never include "Co-Authored-By", "Generated with", or any AI/author attribution
5. **AI-only changes**: When changes are exclusively AI-related (skills, prompts, Claude configs), always use `ai` type—never `refactor`, `chore`, or other types
6. **Preview before commit**: Always show the proposed commit message to the user for confirmation before executing the commit

## Examples

```
feat(apps-server): add health check endpoint
```

```
refactor(apps-server): migrate from LibSQL to PostgreSQL

- Replaced LibSQL/Turso with PostgreSQL for Better Auth storage.
- Removed OpenFGA environment variables.
- Added pg and Effect SQL dependencies.
```

```
chore: update workspaces and dependencies

- Added shared/repositories/* to workspaces.
- Bumped @biomejs/biome to 2.3.8.
```

```
fix(apps-cli): update build filter to exclude xiroi-apps directory

- Changed the build command filter from excluding './apps/*' to excluding
  './xiroi-apps/*' for more accurate targeting.
```

```
ai: secure Claude settings by restricting dangerous permissions
```
