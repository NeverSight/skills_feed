---
name: commit
description: Commit workflow for agent-media - builds, typechecks, creates changeset, and pushes
---

# Commit Workflow

When committing changes to this repository, follow these steps:

## 1. Build and typecheck

Run both commands and ensure they pass:

```bash
pnpm build && pnpm typecheck
```

**Do not proceed if either fails.** Fix all errors first.

## 2. Check what changed

```bash
git status
git diff --stat
```

## 3. Create a changeset file

**IMPORTANT:** The CLI package is named `agent-media` (NOT `@agent-media/cli`).

Create `.changeset/<descriptive-name>.md`:

```markdown
---
"agent-media": patch|minor|major
"@agent-media/core": patch|minor|major
"@agent-media/providers": patch|minor|major
"@agent-media/image": patch|minor|major
"@agent-media/audio": patch|minor|major
"@agent-media/video": patch|minor|major
---

Brief description of changes
```

Only include packages that were actually modified. Use:
- `patch` for bug fixes
- `minor` for new features (backward compatible)
- `major` for breaking changes

## 4. Create feature branch

```bash
git checkout -b feat/<descriptive-name>
# or fix/<descriptive-name> for bug fixes
```

## 5. Stage and commit

```bash
git add <files> .changeset/<name>.md
git commit -m "feat|fix: descriptive message"
```

## 6. Push and create PR

```bash
git push -u origin <branch-name>
gh pr create --title "..." --body "..."
```

> **Note:** If you need to switch GitHub accounts for PR creation, check `.claude.local/workflow.md` for your personal account switching commands.

## Important reminders

- **NEVER** manually edit CHANGELOG.md - changesets auto-generates it
- **NEVER** run `pnpm changeset version` locally
- **ALWAYS** run `pnpm build && pnpm typecheck` before committing
- **ALWAYS** sync README.md to packages/cli/README.md when README changes
