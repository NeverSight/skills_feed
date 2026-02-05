---
name: package-json-maintenance
description: >
  Maintain JavaScript/Node.js packages through security audits or dependency updates in an isolated git worktree.
  Supports npm, yarn, pnpm, and bun. Use for: (1) Security requests - audit, CVE, vulnerabilities, fix security issues,
  check for vulnerable dependencies; (2) Update requests - update dependencies, upgrade packages, get latest versions,
  modernize dependencies.
license: MIT
metadata:
  author: Gregory Murray
  repository: github.com/whatifwedigdeeper/agent-skills
  version: "0.1"
---

# Package.json Maintenance

Manages JavaScript package maintenance tasks in an isolated worktree, including security audits and dependency updates. Automatically detects and uses the project's package manager (npm, yarn, pnpm, or bun).

## Arguments

- **Specific packages**: `jest @types/jest`
- **All packages**: `.`
- **Glob patterns**: `@testing-library/* jest*`

## Workflow Selection

Based on user request:
- **Security audit** (audit, CVE, vulnerabilities, security): Read [references/audit-workflow.md](references/audit-workflow.md)
- **Dependency updates** (update, upgrade, latest, modernize): Read [references/update-workflow.md](references/update-workflow.md)

## Shared Process

### 1. Create Isolated Environment

**Preferred: Worktree** (isolated, non-disruptive)
```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BRANCH_NAME="pkg-maintenance-$TIMESTAMP"
WORKTREE_PATH="../$BRANCH_NAME"
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"
cd "$WORKTREE_PATH"
USE_WORKTREE=true
```

**Fallback: Branch** (if worktree fails due to sandbox directory restrictions)

Prompt user: "Worktree creation failed (sandbox may restrict creating directories outside the working directory). Run in current directory on a new branch instead? This will stash any uncommitted changes."

If user accepts:
```bash
git stash --include-untracked
git checkout -b "$BRANCH_NAME"
USE_WORKTREE=false
```

### 2. Detect Package Manager

Check for lock files to determine the package manager. See [references/package-managers.md](references/package-managers.md) for detection logic and command mappings.

```bash
if [ -f "bun.lockb" ]; then PM="bun"
elif [ -f "pnpm-lock.yaml" ]; then PM="pnpm"
elif [ -f "yarn.lock" ]; then PM="yarn"
else PM="npm"
fi
```

Also check `package.json` for `packageManager` field which takes precedence.

### 3. Verify Registry Access

Verify the package manager can reach its registry. See [references/package-managers.md](references/package-managers.md) for manager-specific commands.

If this fails, prompt user: "Cannot reach package registry. Sandbox may be blocking network access. To allow package manager commands in sandbox mode, update settings.json."

Do not proceed until connectivity is confirmed.

### 4. Discover Package Locations

Find all package.json files excluding node_modules:
```bash
find . -name "package.json" -not -path "*/node_modules/*" -type f
```

Store results as an array of directories to process.

### 5. Identify Packages

- Parse `$ARGUMENTS` to determine packages
- For globs, expand against package.json dependencies
- For `.`, process all packages

### 6. Validate Changes

Check `package.json` scripts for available validation commands:

| Purpose | Common names |
|---------|--------------|
| Build | `build`, `compile`, `tsc` |
| Lint | `lint`, `check`, `eslint` |
| Test | `test`, `jest`, `vitest` |

Run available scripts using `$PM run <script>` in order (build → lint → test), continuing on failure to collect all errors. Skip any that don't exist.

If validation fails, revert to previous version before continuing.

### 7. Update Documentation for Major Version Changes

For major version upgrades (e.g., 18.x to 19.x):

1. Search for version references: `grep -r "React 18\|Express 4" --include="*.md" .`
2. Update in: `CLAUDE.md`, `README.md`, `docs/*.md`
3. Skip: `specs/*/research.md`, `specs/*/tasks.md`, archived files
4. Include changes in report/PR description

### 8. Cleanup

**If using worktree:**
```bash
cd -
git worktree remove "$WORKTREE_PATH"
# Delete branch only if no PR was created
git branch -d "$BRANCH_NAME"
```

**If using branch fallback:**
```bash
git checkout -
git stash pop
# Delete branch only if no PR was created
git branch -d "$BRANCH_NAME"
```

## Edge Cases

- **No package.json**: Error with clear message
- **Not a git repo**: Error - git required for branch/worktree isolation
- **Package not found**: Suggest checking package name
- **Glob matches nothing**: Warn and list available packages
- **Network restricted**: Package manager commands require internet access; will fail in offline sandbox environments
- **Unsupported package manager**: If using an unrecognized package manager, prompt user for guidance
