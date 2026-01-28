---
name: deps
description: Manage dependencies with npm/yarn/pnpm. Use for auditing vulnerabilities, checking outdated packages, understanding dependency trees, and upgrading packages safely.
---

# Dependencies Manager

Audit, analyze, and manage project dependencies.

## Prerequisites

At least one package manager:
```bash
# npm (comes with Node.js)
node --version

# yarn
npm install -g yarn

# pnpm
npm install -g pnpm
```

For dependency analysis:
```bash
npm install -g depcheck
```

## CLI Reference

### Security Audit

#### npm
```bash
# Run security audit
npm audit

# JSON output
npm audit --json

# Only production deps
npm audit --omit=dev

# Fix automatically
npm audit fix

# Fix with breaking changes (careful!)
npm audit fix --force
```

#### yarn
```bash
yarn audit
yarn audit --json
```

#### pnpm
```bash
pnpm audit
pnpm audit --json
```

### Check Outdated Packages

#### npm
```bash
# List outdated
npm outdated

# JSON output
npm outdated --json

# Long format with details
npm outdated --long
```

#### yarn
```bash
yarn outdated
```

#### pnpm
```bash
pnpm outdated
pnpm outdated --json
```

### Upgrade Packages

#### npm
```bash
# Update to latest within semver range
npm update

# Update specific package
npm update lodash

# Install latest (ignoring semver)
npm install lodash@latest

# Interactive upgrade (with npm-check)
npx npm-check -u
```

#### yarn
```bash
yarn upgrade
yarn upgrade lodash
yarn upgrade lodash@latest
yarn upgrade-interactive
```

#### pnpm
```bash
pnpm update
pnpm update lodash
pnpm update lodash --latest
pnpm update --interactive
```

### Dependency Analysis

#### Why is this package installed?
```bash
# npm
npm explain lodash
npm ls lodash

# yarn
yarn why lodash

# pnpm
pnpm why lodash
```

#### Find unused dependencies
```bash
npx depcheck

# JSON output
npx depcheck --json

# Ignore patterns
npx depcheck --ignores="@types/*,eslint-*"
```

### View Package Info
```bash
# View package details
npm view lodash

# Specific fields
npm view lodash version
npm view lodash versions
npm view lodash dependencies
npm view lodash repository.url

# JSON output
npm view lodash --json
```

### Dependency Tree
```bash
# Full tree
npm ls

# Specific depth
npm ls --depth=2

# Production only
npm ls --omit=dev

# Specific package
npm ls lodash

# JSON
npm ls --json
```

## Workflow Patterns

### Security Audit Workflow
```bash
# 1. Run audit
npm audit --json > audit-report.json

# 2. Review high/critical
npm audit --audit-level=high

# 3. Auto-fix what's safe
npm audit fix

# 4. Manually review remaining
npm audit
```

### Upgrade Workflow
```bash
# 1. Check what's outdated
npm outdated --json

# 2. Test current state
npm test

# 3. Update patch/minor versions (safer)
npm update

# 4. Test again
npm test

# 5. Update major versions one at a time
npm install package@latest
npm test
```

### Dependency Cleanup
```bash
# 1. Find unused deps
npx depcheck

# 2. Review and remove
npm uninstall unused-package

# 3. Verify
npm test && npm run build
```

### Investigating a Package
```bash
# Package info
npm view express

# Current version in project
npm ls express

# Who depends on it
npm explain express

# Security vulnerabilities
npm audit | grep express
```

## Common Issues

### Peer Dependency Warnings
```bash
# See peer deps
npm ls --json | grep peer

# Install missing peer deps
npm install missing-peer-dep
```

### Version Conflicts
```bash
# See duplicate packages
npm ls --all | grep "deduped"

# Force dedupe
npm dedupe
```

### Lock File Issues
```bash
# Regenerate lock file
rm package-lock.json
npm install

# Or for yarn
rm yarn.lock
yarn install
```

## Best Practices

1. **Audit regularly** - Run `npm audit` weekly or in CI
2. **Update incrementally** - One major version at a time
3. **Test after updates** - Always run tests post-update
4. **Review before fixing** - `npm audit fix --force` can break things
5. **Clean unused deps** - Run `depcheck` periodically
6. **Lock versions** - Commit lock files to git
7. **Check before adding** - Review package health before installing
