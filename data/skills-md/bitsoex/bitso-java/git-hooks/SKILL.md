---
name: git-hooks
description: >
  Set up, validate, and maintain Git hooks (pre-commit, pre-push, etc.) following
  best practices. Ensures hooks are version-controlled, automatically installed,
  and follow consistent patterns across the team. Use when creating new hooks,
  debugging hook issues, or ensuring hook compliance.
compatibility: Requires Node.js 20+; works with any Git repository
metadata:
  version: "2.0"
  targeting:
    include:
      - repo: "bitsoex/ai-code-instructions"
---

# Git Hooks

This skill provides guidance for implementing and maintaining Git hooks that enforce code quality standards before commits and pushes reach the repository.

## When to use this skill

- Setting up Git hooks in a new repository
- Creating new pre-commit or pre-push hooks
- Debugging hook installation or execution issues
- Ensuring hooks follow team standards
- Migrating from manual hooks to version-controlled hooks
- Integrating with existing hook systems (Husky, pre-commit, lefthook)

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L20-L28)
- [Distributed Hooks (Informative Mode)](#distributed-hooks-informative-mode) (L64-L125)
- [Assets](#assets) (L126-L136)
- [Architecture](#architecture) (L137-L161)
- [Instructions](#instructions) (L162-L256)
- [Hook Types](#hook-types) (L257-L267)
- [Best Practices](#best-practices) (L268-L396)
- [Informative vs Enforcing Mode](#informative-vs-enforcing-mode) (L397-L405)
- [References](#references) (L406-L416)
- [Documentation](#documentation) (L417-L424)
- [Related Skills](#related-skills) (L425-L432)
- [Troubleshooting](#troubleshooting) (L433-L495)

### Available Resources

**📚 references/** - Detailed documentation
- [go](references/go)
- [java](references/java)
- [python](references/python)
- [typescript](references/typescript)

**📦 assets/** - Templates and resources
- [ensure node](assets/ensure-node.sh)
- [hooks bootstrap](assets/hooks-bootstrap.sh)
- [hooks bridge strategy](assets/hooks-bridge-strategy.md)
- [hooks checks](assets/hooks-checks.js)
- [pre commit](assets/pre-commit)
- [pre push](assets/pre-push)

---

## Distributed Hooks (Informative Mode)

For repositories receiving distributed AI rules, we provide **informative hooks** that:

- **Never block** commits or pushes (always exit 0)
- **Warn** about issues with clear fix commands
- **Auto-detect Node.js** via nvm, fnm, or system PATH (shows setup instructions if not found)
- **Coexist** with existing hook setups (Husky, pre-commit, lefthook)

### How It Works

```
# Source location: global/skills/git-hooks/assets/
# Deployed to target repo as:

.git-hooks/
├── pre-commit          → Delegates to hooks-bootstrap.sh (same directory)
├── pre-push            → Delegates to hooks-bootstrap.sh (same directory)
├── ensure-node.sh      → Ensures Node.js 20+ is available
├── hooks-bootstrap.sh  → Entry point, loads Node, runs checks
└── hooks-checks.js     → Multi-language quality checks
```

### Enabling Distributed Hooks

```bash
# Set Git to use our hooks directory
git config core.hooksPath .git-hooks

# Verify
git config --get core.hooksPath
# Should output: .git-hooks
```

### Output Example

```
============================================================
  Bitso Quality Checks (Informative)
============================================================

  Pre-commit checks found some issues:

  [!] Linting: ESLint errors detected
      Run: pnpm run lint:fix

  [!] TypeScript: Type errors detected
      Run: npx tsc --noEmit

  These are recommendations. Your commit will proceed.
  For AI agents: Please address these issues before completing.

============================================================
```

### Coexistence with Existing Hooks

See `assets/hooks-bridge-strategy.md` for detailed integration patterns with:
- **Husky**: Add our checks to `.husky/pre-commit`
- **pre-commit (Python)**: Add as a `local` hook in `.pre-commit-config.yaml`
- **lefthook**: Add to `lefthook.yml` commands

## Assets

| Asset | Purpose |
|-------|---------|
| `assets/ensure-node.sh` | Node.js detection and auto-installation |
| `assets/hooks-bootstrap.sh` | Hook entry point (ensures Node, runs checks) |
| `assets/hooks-checks.js` | Multi-language quality checks |
| `assets/pre-commit` | Pre-commit hook entry point |
| `assets/pre-push` | Pre-push hook entry point |
| `assets/hooks-bridge-strategy.md` | Integration patterns for existing setups |

## Architecture

### Recommended Directory Structure

```
project/
├── .git-hooks/              # Version-controlled hooks directory
│   ├── pre-commit           # Symlink → ../.scripts/pre-commit-hook.sh
│   └── pre-push             # Symlink → ../.scripts/pre-push-hook.sh
├── .scripts/
│   ├── setup-hooks.js       # Hook installation script (runs on npm install)
│   ├── pre-commit-hook.sh   # Pre-commit hook implementation
│   ├── pre-push-hook.sh     # Pre-push hook implementation
│   └── lib/skills/          # Skill modules for hook operations
└── package.json             # Contains "prepare": "node .scripts/setup-hooks.ts"
```

### Why This Architecture?

1. **Version-controlled**: Hooks live in `.git-hooks/`, tracked by Git
2. **Automatic installation**: `npm install` configures hooks via `prepare` script
3. **Team consistency**: Everyone gets the same hooks automatically
4. **Implementation separation**: Actual logic in `.scripts/`, symlinks in `.git-hooks/`
5. **Skippable in CI**: Setup script detects CI environment and skips

## Instructions

### Step 1: Create the Hooks Directory

```bash
mkdir -p .git-hooks
```

### Step 2: Create the Setup Script

Create `.scripts/setup-hooks.ts`:

```javascript
#!/usr/bin/env node
/**
 * Setup Git Hooks
 *
 * Runs on `npm install` via the "prepare" script.
 * Configures git to use .git-hooks/ for hooks.
 */

if (process.env.CI || process.env.SKIP_HOOKS) {
  console.log('⏭️  Skipping hook setup (CI or SKIP_HOOKS=true)');
  process.exit(0);
}

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT_DIR = path.join(__dirname, '..');
const HOOKS_DIR = '.git-hooks';

function setupHooks() {
  if (!fs.existsSync(path.join(ROOT_DIR, '.git'))) {
    console.log('⚠️  Not a git repository, skipping hook setup');
    return;
  }

  const githooksPath = path.join(ROOT_DIR, HOOKS_DIR);
  if (!fs.existsSync(githooksPath)) {
    console.error(`❌ Hooks directory not found: ${HOOKS_DIR}`);
    process.exit(1);
  }

  // Set core.hooksPath
  try {
    execSync(`git config core.hooksPath ${HOOKS_DIR}`, { cwd: ROOT_DIR });
    console.log(`✅ Git hooks configured: core.hooksPath → ${HOOKS_DIR}`);
  } catch (error) {
    console.error('❌ Failed to set core.hooksPath:', error.message);
    process.exit(1);
  }
}

setupHooks();
```

### Step 3: Configure package.json

Add the prepare script to automatically set up hooks on install:

```json
{
  "scripts": {
    "prepare": "node .scripts/setup-hooks.ts"
  }
}
```

### Step 4: Create Hook Implementation

Create hook scripts in `.scripts/` following the template in the References section.

### Step 5: Create Symlinks

Create symlinks in `.git-hooks/` pointing to the implementation:

```bash
cd .git-hooks
ln -sf ../.scripts/pre-commit-hook.sh pre-commit
ln -sf ../.scripts/pre-push-hook.sh pre-push
chmod +x pre-commit pre-push
```

### Step 6: Validate Hook Setup

```bash
# Run validation
npm run skills:hooks

# Or use CLI directly
node .scripts/skills-cli.ts git-hooks validate
```

## Hook Types

| Hook | When It Runs | Typical Checks |
|------|-------------|----------------|
| `pre-commit` | Before commit is created | Linting, formatting, tests, validation |
| `pre-push` | Before push to remote | Full test suite, coverage, build verification |
| `commit-msg` | After commit message written | Message format validation |
| `prepare-commit-msg` | Before editor opens | Template insertion |
| `post-checkout` | After checkout completes | Dependency updates, cache clearing |
| `post-merge` | After merge completes | Dependency updates |

## Best Practices

### 1. Exit Codes Matter

```bash
# Exit 0 = success, commit/push proceeds
# Exit non-zero = failure, operation aborted
if ! npm test; then
  echo "Tests failed"
  exit 1
fi
```

### 2. Provide Clear Feedback

```bash
# Use colors and emojis for visibility
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🔍 Running tests...${NC}"
if npm test --silent; then
  echo -e "${GREEN}   ✓ Tests passed${NC}"
else
  echo -e "${RED}   ✗ Tests failed${NC}"
  exit 1
fi
```

### 3. Keep Hooks Fast

Pre-commit hooks should complete in seconds, not minutes:
- Run only essential checks
- Use incremental/cached operations where possible
- Move heavy checks to pre-push

### 4. Allow Emergency Bypass

```bash
# Document how to skip in emergencies
git commit --no-verify  # Skip pre-commit
git push --no-verify    # Skip pre-push
```

### 5. Fail Early, Fail Fast

Order checks from fastest to slowest:

```bash
# 1. Fast checks first
echo "Checking for debug statements..."
if grep -r "console.log" src/; then
  echo "Remove debug statements before committing"
  exit 1
fi

# 2. Medium checks
echo "Running linter..."
npm run lint

# 3. Slow checks last
echo "Running tests..."
npm test
```

### 6. Handle Auto-Fixes

If a hook auto-fixes files, stage them:

```bash
if git diff --name-only | grep -q "formatted-file.js"; then
  git add formatted-file.js
  echo "Auto-formatted file added to commit"
fi
```

### 7. Never Add Coverage Exclusions as First Approach

**IMPORTANT**: When pre-push hooks fail due to coverage thresholds, the correct approach is:

1. **Add tests** to increase coverage (preferred)
2. Use `--no-verify` as a **temporary emergency bypass** if absolutely necessary
3. **Never add exclusions** to `.c8rc.json`, `.nycrc`, or coverage config

**Why?**

- Exclusions hide untested code and accumulate over time
- They defeat the purpose of coverage thresholds
- They make it harder to identify actual coverage gaps

**Correct approach when coverage fails:**

```bash
# 1. Run coverage report to identify gaps
npm run test:coverage:report

# 2. Add tests for uncovered lines
# ... write tests ...

# 3. Verify coverage now passes
npm run test:coverage

# 4. Commit and push normally
git push
```

**Emergency bypass (use sparingly):**

```bash
# Only when you MUST push immediately and will add tests in follow-up
git push --no-verify

# Document why in commit message or PR
# Create a ticket to add missing tests
```

**Never do this:**

```json
// ❌ DON'T add exclusions to avoid writing tests
{
  "exclude": [
    ".scripts/new-module.ts"  // ❌ WRONG - write tests instead
  ]
}
```

## Informative vs Enforcing Mode

| Mode | Exit Code | Use Case |
|------|-----------|----------|
| **Informative** (default) | Always 0 | Distributed hooks for all repos |
| **Enforcing** | Non-zero on failure | AI agent hooks, CI validation |

The distributed hooks use **informative mode** to guide developers and AI agents without blocking workflow. For enforcing mode, see the `agent-hooks` skill which integrates with Claude Code and Cursor IDE.

## References

Technology-specific hook patterns are available in the `references/` folder:

| Technology | Reference |
|------------|-----------|
| Java | `references/java/hook-patterns.md` |
| TypeScript/JavaScript | `references/typescript/hook-patterns.md` |
| Python | `references/python/hook-patterns.md` |
| Go | `references/go/hook-patterns.md` |

## Documentation

For comprehensive documentation, see:

- [Git Hooks Architecture](../../../docs/ai-ide-management/concepts/git-hooks-architecture.md) - System design and flow diagrams
- [How to Enable Git Hooks](../../../docs/ai-ide-management/how-tos/enable-git-hooks.md) - Setup and troubleshooting
- [Conflict Detection](../../../docs/ai-ide-management/concepts/conflict-detection.md) - How conflicts are detected during distribution

## Related Skills

| Skill | Purpose |
|-------|---------|
| `agent-hooks` | AI IDE hooks (Claude Code, Cursor) with enforcing mode |
| `quality-gateway` | Quality gate orchestration |
| `coding-standards` | Code style enforcement |

## Troubleshooting

### Hooks not running

1. Verify hooks are installed:

   ```bash
   git config --get core.hooksPath
   # Should output: .git-hooks
   ```

2. Check symlinks are valid:

   ```bash
   ls -la .git-hooks/
   # Should show symlinks pointing to .scripts/*-hook.sh
   ```

3. Verify execute permissions:

   ```bash
   chmod +x .git-hooks/*
   chmod +x .scripts/*-hook.sh
   ```

### Hooks running but failing

1. Run hooks manually to see full output:

   ```bash
   ./.scripts/pre-commit-hook.sh
   ```

2. Check for missing dependencies:

   ```bash
   npm install
   ```

3. Run with DEBUG mode:

   ```bash
   DEBUG=1 ./.scripts/pre-commit-hook.sh
   ```

### Hooks too slow

1. Profile each check:

   ```bash
   time npm run lint
   time npm test
   ```

2. Move slow checks to pre-push
3. Use incremental/cached operations
4. Consider staged-files-only validation

### Different behavior locally vs CI

1. CI should skip hooks (set `CI=true`)
2. CI runs validations directly, not via hooks
3. Ensure setup-hooks.js checks for CI environment
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/git-hooks/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

