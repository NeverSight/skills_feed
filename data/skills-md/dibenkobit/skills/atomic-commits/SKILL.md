---
name: atomic-commits
description: Split staged git changes into logical atomic commits. Use when asked to "commit atomically", "split my changes", "make atomic commits", or "create separate commits".
author: dibenkobit
version: 1.0.0
license: MIT
---

# Atomic Commits

Split staged changes into multiple logical commits. Each commit does ONE thing.

## Priority Order (for format, language, types, scopes — everything)

1. **User's explicit instructions** — always wins
2. **Project config** — .commitlintrc*, .czrc, .babygit.json
3. **Recent commits** — match style from `git log --oneline -10`
4. **Defaults** — Conventional Commits, English

## How It Works

### 1. Check prerequisites

```bash
git diff --cached --name-only
```

- **0 files?** → Tell user "Nothing staged. Run `git add` first."
- **1 file?** → Ask: "Only one file staged. Want a single commit or split by hunks?"

### 2. Detect conventions

Check for config: `ls .commitlintrc* .czrc .babygit.json 2>/dev/null`

If found → read and extract types, scopes, format rules.
If not → analyze `git log --oneline -10` for patterns.

### 3. Get diffs and think about grouping

For each file: `git diff --cached -- <file>`

**Reasoning for grouping:**
- Same feature/module? → together (auth.ts + auth.types.ts)
- Test + implementation? → together (utils.ts + utils.test.ts)
- Unrelated purpose? → separate (feature vs deps vs docs)
- Config/deps changes? → usually separate commit

**Ask yourself:** "If I need to revert just THIS change, can I do it with one commit?"

### 4. Validate before showing

- Every staged file in exactly one group? ✓
- No file in multiple groups? ✓
- Commit messages match detected format? ✓

### 5. Show and confirm

```
Proposed commits (3):

1. feat(auth): implement OAuth2 flow
   └─ src/auth/oauth.ts, src/auth/types.ts

2. feat(ui): add login button
   └─ components/LoginButton.tsx

3. chore(deps): update dependencies
   └─ package.json, bun.lock

[Y]es / [E]dit / [C]ancel?
```

**On Edit** → let user reassign files or change messages.
**On Cancel** → stop, leave everything staged as-is.

### 6. Execute commits

For each group in order:
```bash
git stash push -q                    # Save current state
git reset HEAD . -q                  # Unstage all
git add <files-in-group>             # Stage this group only
git commit -m "<message>"            # Commit
```

After all groups done:
```bash
git stash pop -q 2>/dev/null || true # Restore if anything left
```

If any commit fails → stop, show error, don't continue.

## Edge Cases

| Situation | Action |
|-----------|--------|
| No staged files | Tell user, stop |
| 1 file only | Ask if split by hunks or single commit |
| Binary files | Include in commits, skip diff analysis |
| Pre-commit hooks | Warn user they will run |
| Commit fails | Stop immediately, show error |
| User wants to edit | Allow reassigning files between groups |

## Commit Message Format

Default (Conventional Commits):
```
<type>(<scope>): <description>

- detail 1
- detail 2
```

Types: `feat` `fix` `refactor` `chore` `docs` `test` `style` `perf` `ci` `build`

Adapt format based on Priority Order above.

## Example with User Override

**User:** "commit atomically, use gitmoji, write in russian"

**Staged:** auth.ts, auth.test.ts, package.json

**Output:**
```
1. ✨ добавить OAuth2 аутентификацию
   └─ auth.ts, auth.test.ts

2. ⬆️ обновить зависимости
   └─ package.json
```

User instruction (gitmoji + russian) overrides any project config.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Pre-commit hook fails | Linting/formatting errors | Fix the issue, re-stage, create NEW commit (don't amend) |
| Stash conflict | Uncommitted changes conflict with stash | Resolve manually with `git stash show -p \| git apply` |
| "Nothing to commit" | All files already committed | Check `git status`, ensure files are staged |
| Permission denied | No write access | Check file permissions, repository ownership |
| Commit partially applied | Script interrupted mid-execution | Run `git stash pop` to recover, start over |

## Present Results to User

When presenting the commit plan, use this format:

```
Proposed commits ({N}):

1. {type}({scope}): {description}
   └─ {file1}, {file2}

2. {type}({scope}): {description}
   └─ {file1}

...

[Y]es to commit all / [E]dit to modify / [C]ancel
```

After successful execution:
```
✓ Created {N} commits:
  • {hash1} {message1}
  • {hash2} {message2}
```

On failure, stop immediately and show which commit failed and why.
