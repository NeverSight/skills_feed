---
name: gitmoji-commits
description: "Create high-quality git commits with semantic gitmoji emojis. Automatically suggests appropriate gitmojis for commit types, review/stage intended changes, split into logical commits, and write clear conventional commit messages. Use when the user asks to commit, wants gitmoji-enhanced messages, needs to stage changes, or split work into multiple commits."
---

# Gitmoji Commits

Create meaningful commits with semantic gitmoji emojis that make commit history readable and visually organized.

## Goal

Make commits that are easy to review, ship-safe, and visually clear:
- Only intended changes are included
- Commits are logically scoped (split when needed)
- Commit messages include semantic gitmojis describing the change type
- Messages follow Conventional Commits format with gitmoji prefix

## When to Use This Skill

Use this skill when:
- User asks to commit changes with gitmoji support
- User wants emoji-enhanced commit messages
- Need to stage changes with gitmoji awareness
- Splitting work into multiple meaningful commits
- Creating Conventional Commits with visual distinction

## Inputs to Ask For (if missing)

- Single commit or multiple commits? (Default: multiple small commits when unrelated changes exist)
- Any project-specific conventions? (scope requirements, commit message rules)
- Preference: auto-suggest gitmoji or let user choose?

## Workflow (checklist)

### 1. Inspect the Working Tree
```bash
git status
git diff              # unstaged changes
git diff --stat       # summary if many changes
```

### 2. Decide Commit Boundaries
Split by:
- Feature vs refactor vs docs vs tests
- Backend vs frontend vs config
- Logic changes vs formatting/cleanup
- Dependency changes vs behavior changes

**Tip**: If mixed changes in one file, plan patch staging: `git add -p`

### 3. Determine Gitmoji for This Commit
Consult `references/gitmoji-guide.md` for complete mapping.

Quick reference:
- **Feature**: ✨ sparkles
- **Bug fix**: 🐛 bug
- **Documentation**: 📝 memo
- **Test**: 🧪 test_tube
- **Refactor**: ♻️ recycle
- **Performance**: ⚡ zap
- **Style/UI**: 💄 lipstick
- **Dependencies**: 📦 package
- **Security**: 🔐 lock
- **Build/Config**: ⚙️ gear
- **Cleanup**: 🗑️ wastebasket

Or use the selector script: `scripts/gitmoji_selector.py "your commit description"`

### 4. Stage the Right Changes
```bash
# Stage specific files
git add <file>

# Stage specific hunks from a file
git add -p

# Review what's staged
git diff --cached

# Unstage if needed
git restore --staged <file>
```

**Sanity checks before committing:**
- No secrets or tokens
- No debug logging
- No unrelated formatting churn
- All changes are intentional

### 5. Describe the Change Concisely
Before writing the message, describe what changed and why in 1-2 sentences.

If you can't describe it cleanly, the commit is too big or mixed—go back to step 2.

### 6. Write the Commit Message
Format: `emoji type(scope): subject`

**Structure:**
```
✨ feat(auth): Add two-factor authentication

- Implement TOTP support  
- Update user model with secret key
- Add verification endpoint

Closes #123
```

**Rules:**
- Subject line: max 50 characters
- Emoji at the start (from gitmoji selection)
- Type: feat, fix, refactor, docs, test, perf, style, chore, ci, build
- Scope (optional): Feature area (auth, api, ui, db, etc.)
- Subject: Imperative form ("Add" not "Added"), lowercase after scope
- Body: Explain what/why (not implementation details)
- Footer: Reference issues (Closes #123, Fixes #456)

**Multi-line commits:** Use `git commit -v` for an editor.

### 7. Run Verification
Run the repo's fastest meaningful check before moving on:
- Unit tests: `npm test` or `bun test`
- Linting: `npm run lint`
- Build: `npm run build`

### 8. Repeat for Next Commit
Until the working tree is clean, repeat steps 1-7.

## Deliverable

Provide:
- Final commit message(s) with gitmojis
- Short summary per commit (what/why)
- Commands used to stage/review (at minimum: `git diff --cached`)
- Any test/build verification results

## Gitmoji Reference

See `references/gitmoji-guide.md` for:
- Complete gitmoji catalog with descriptions
- Selection decision tree
- Conventional Commits examples
- Tips for consistent emoji usage

## Helper Script

The `scripts/gitmoji_selector.py` script suggests gitmojis automatically:

```bash
# Analyze a message and suggest gitmoji
python3 scripts/gitmoji_selector.py "fix critical bug in authentication"

# Generate Conventional Commits format
python3 scripts/gitmoji_selector.py --conventional feat auth "Add two-factor authentication"
```

## Best Practices

1. **One emoji per commit**: Each commit has exactly one primary gitmoji
2. **Be specific**: Choose the most appropriate emoji, not a generic one
3. **Consistent scope**: Use consistent scope names across commits
4. **Clear messages**: Subject line should be understandable without body
5. **Atomic commits**: Each commit should be independently buildable/testable
