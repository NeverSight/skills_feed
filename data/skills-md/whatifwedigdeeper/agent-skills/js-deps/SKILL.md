---
name: js-deps
description: >
  Maintain JavaScript/Node.js packages through security audits or dependency updates on a dedicated branch.
  Supports npm, yarn, pnpm, and bun. Use for: security audits, CVE fixes, vulnerability checks, dependency updates,
  package upgrades, outdated packages, bump versions, fix npm vulnerabilities, modernize node_modules, or when user
  types "/js-deps" with or without specific package names or glob patterns. Use "help" or "--help" to show options.
license: MIT
compatibility: Requires git, a JavaScript package manager (npm, yarn, pnpm, or bun), and network access to package registries
metadata:
  author: Gregory Murray
  repository: github.com/whatifwedigdeeper/agent-skills
  version: "0.4"
---

# JS Deps

## Arguments

Specific package names (e.g. `jest @types/jest`), `.` for all packages, or glob patterns (e.g. `@testing-library/*`).

If `$ARGUMENTS` is `help`, `--help`, `-h`, or `?`, skip the workflow and read [references/options.md](references/options.md).

## Workflow Selection

Based on user request:
- **Security audit** (audit, CVE, vulnerabilities, security): Read [references/audit-workflow.md](references/audit-workflow.md)
- **Dependency updates** (update, upgrade, latest, modernize): Read [references/update-workflow.md](references/update-workflow.md)

## Shared Process

### 1. Create Branch

Stash uncommitted changes and create a dedicated branch:
```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BRANCH_NAME="js-deps-$TIMESTAMP"
git stash --include-untracked
git checkout -b "$BRANCH_NAME"
```

### 2. Detect Package Manager

Detect from lock files and `package.json` `packageManager` field (which takes precedence). See [references/package-managers.md](references/package-managers.md) for detection logic and command mappings.

### 3. Verify Registry Access

Verify the package manager CLI is available and, for npm, that it can reach the registry. See [references/package-managers.md](references/package-managers.md) for manager-specific verification commands.

If verification fails, prompt user: "Cannot reach package registry. Sandbox may be blocking network access. To allow package manager commands in sandbox mode, update settings.json."

Do not proceed until verification passes.

### 4. Discover Package Locations

Find all `package.json` files excluding `node_modules`. Store results as an array of directories to process.

### 5. Install Dependencies

Install dependencies in each discovered package directory so that `npm outdated` (and similar commands) can accurately compare installed versions against the registry. Without `node_modules`, exact-pinned packages (no `^` or `~`) won't appear in outdated reports.

### 6. Identify Packages

- Parse `$ARGUMENTS` to determine packages
- For globs, expand against package.json dependencies
- For `.`, process all packages

### 7. Validate Changes

Check `package.json` scripts for available validation commands. Run available scripts using `$PM run <script>` in order (build, lint, test), continuing on failure to collect all errors. Skip any that don't exist.

If validation fails, revert the failing package to its previous version before continuing with remaining packages:
```bash
git checkout -- package.json package-lock.json  # or the equivalent lock file
$PM install
```

### 8. Update Documentation for Major Version Changes

For major version upgrades (e.g., 18.x to 19.x):

1. Search for version references in markdown files
2. Update in: `CLAUDE.md`, `README.md`, `docs/*.md`
3. Include changes in report/PR description

### 9. Cleanup

If a PR was created, do not delete the branch — it's needed for the open PR.

```bash
git checkout -
git stash list | grep -q . && git stash pop
# Only delete branch if no PR was created
if ! gh pr view "$BRANCH_NAME" --json url > /dev/null 2>&1; then
  git branch -d "$BRANCH_NAME"
fi
```

## Edge Cases

- **Glob matches nothing**: Warn and list available packages
- **Unsupported package manager**: Prompt user for guidance
- **Peer dep conflicts after major upgrades**: When a plugin doesn't declare support for the new major version of its host (e.g., `eslint-plugin-react-hooks` not supporting eslint 10), add `"overrides"` to `package.json` rather than using `--legacy-peer-deps`. Example: `"overrides": { "eslint-plugin-react-hooks": { "eslint": "$eslint" } }`. The `$eslint` syntax references the version already declared in the package's own dependencies
- **Lockfile sync**: After all package.json changes, run `$PM install` in every modified directory and commit lockfiles — CI tools like `npm ci` require exact sync between package.json and the lockfile
- **Verify devDependencies placement**: After bulk installs across directories, verify that linting/testing/build packages (eslint, typescript, vite, etc.) ended up in `devDependencies`, not `dependencies` — easy to misplace when running install commands across many directories
