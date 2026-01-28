---
name: git-commit-composer
description: Create well-formatted semantic commit messages following project conventions. Use when committing changes to ensure consistent, descriptive commit history.
---

# Git Commit Composer

## Instructions

### When to Invoke This Skill
- Ready to commit changes after implementation
- Need to create descriptive commit message
- Following semantic commit conventions
- Linking commits to issues or PRs

### Commit Message Format

#### Structure
```
<type>: <brief description>

<detailed explanation of what changed and why>

<footer with issue links and metadata>
```

#### Components

**Type** (required):
- `feat` - New feature
- `fix` - Bug fix
- `chore` - Maintenance, dependencies, tooling
- `docs` - Documentation changes
- `refactor` - Code restructuring without behavior change
- `test` - Test additions or modifications
- `perf` - Performance improvements
- `style` - Code style/formatting (no logic change)

**Brief Description** (required):
- Imperative mood: "add", not "added" or "adds"
- Lowercase start
- No period at end
- Maximum 50 characters
- Describe what the commit does

**Detailed Explanation** (recommended):
- Explain WHAT changed and WHY
- Don't explain HOW (code shows that)
- Use bullet points for multiple changes
- Wrap at 72 characters per line

**Footer** (optional):
- Issue links: `Fixes #123`, `Resolves #456`, `Closes #789`
- Breaking changes: `BREAKING CHANGE: describe the change`
- Co-authors: `Co-Authored-By: Name <email>`
- Tool attribution: `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

### Standard Workflow

1. **Review Changes**
   ```bash
   git status
   git diff
   ```

2. **Analyze Changes**
   - Determine commit type
   - Identify main purpose
   - Note secondary effects
   - Find related issues

3. **Compose Message**
   Follow the format above

4. **Create Commit**
   ```bash
   git commit -m "$(cat <<'EOF'
   <type>: <brief description>

   <detailed explanation>

   <footer>
   EOF
   )"
   ```

### Best Practices

**Good Brief Descriptions:**
- `feat: add user authentication with JWT`
- `fix: resolve race condition in websocket handler`
- `chore: update dependencies to latest versions`
- `docs: add API endpoint documentation`

**Bad Brief Descriptions:**
- `feat: added some new features` (too vague)
- `fix: Fixed a bug` (not descriptive)
- `update` (missing type)
- `FEAT: Add Feature` (wrong capitalization)

**Good Detailed Explanations:**
```
Add JWT-based authentication to protect API endpoints

- Implement token generation and validation
- Add middleware to verify tokens on protected routes
- Store refresh tokens in database
- Add token expiration and renewal logic

This ensures only authenticated users can access sensitive data.
```

**Bad Detailed Explanations:**
```
Made some changes to auth
```

### Commit Message Templates

#### Feature Commit
```
feat: add dark mode toggle

Implement dark mode toggle in user settings with:
- Theme preference stored in localStorage
- CSS variable switching for colors
- Smooth transitions between themes

Fixes #42

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### Bug Fix Commit
```
fix: resolve websocket race condition

Fix race condition where messages could be sent before connection
fully established:
- Add connection ready flag
- Queue messages during connection
- Flush queue once connected

Fixes #156

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### Chore Commit
```
chore: update Python dependencies

Update uv.lock with latest package versions:
- fastapi 0.104.0 -> 0.109.0
- uvicorn 0.24.0 -> 0.27.0
- pydantic 2.5.0 -> 2.6.0

All tests passing with updated versions.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### Refactor Commit
```
refactor: extract message processing into handlers

Split monolithic message processor into specialized handlers:
- SystemMessageHandler
- AssistantMessageHandler
- UserMessageHandler
- ResultMessageHandler

No behavior changes, improved maintainability.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Multiple Commits vs Single Commit

**Use Multiple Commits When:**
- Changes are logically separate
- Each commit works independently
- Different types (feat + docs)

**Use Single Commit When:**
- Changes are tightly coupled
- Breaking them apart doesn't make sense
- Implementing single issue/feature

### Amending Commits

**When to Amend:**
- Forgot to include a file
- Typo in commit message
- Small addition to last commit
- Commit not yet pushed

**How to Amend:**
```bash
git add <forgotten-files>
git commit --amend --no-edit
```

**When NOT to Amend:**
- Commit already pushed to remote
- Other developers have the commit
- Would rewrite shared history

## Examples

### Example 1: Feature implementation
```
Changes: Added user profile page with avatar upload
Action:
1. Review changes: git diff
2. Identify type: feat (new feature)
3. Compose:
   - Brief: "add user profile page with avatar upload"
   - Detail: List components added, functionality
   - Footer: Fixes #42
4. Commit with formatted message
```

### Example 2: Bug fix
```
Changes: Fixed null pointer error in login handler
Action:
1. Identify type: fix (bug fix)
2. Brief: "resolve null pointer in login handler"
3. Detail: Explain the bug and how it was fixed
4. Footer: Fixes #89
5. Commit
```

### Example 3: Multiple related changes
```
Changes: Updated deps + fixed compatibility issue
Decision: Single commit (changes are coupled)
Action:
1. Type: chore (dependency update)
2. Brief: "update dependencies and fix compatibility"
3. Detail: List updates + explain compatibility fix
4. Commit together
```

### Example 4: Separate concerns
```
Changes: New feature + unrelated docs update
Decision: Two commits (logically separate)
Action:
1. Stage feature files: git add src/
2. Commit feature: feat message
3. Stage docs: git add docs/
4. Commit docs: docs message
```
