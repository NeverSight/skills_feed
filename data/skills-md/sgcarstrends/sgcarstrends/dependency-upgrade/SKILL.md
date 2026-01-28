---
name: dependency-upgrade
description: Upgrade dependencies safely using pnpm catalog, checking for breaking changes, and testing upgrades. Use when updating packages, applying security patches, or upgrading major versions.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Dependency Upgrade Skill

This skill helps you safely upgrade dependencies across the monorepo using pnpm catalog and proper testing procedures.

## When to Use This Skill

- Upgrading npm packages
- Applying security patches
- Updating to latest versions
- Upgrading major versions
- Resolving dependency conflicts
- Modernizing tech stack
- Following breaking change guides

## Dependency Management

The project uses **pnpm with catalog** for centralized dependency management:

```yaml
# pnpm-workspace.yaml
packages:
  - "apps/*"
  - "packages/*"

catalog:
  # Shared versions across workspace
  next: ^16.0.0
  react: ^19.0.0
  react-dom: ^19.0.0
  typescript: ^5.3.3
  drizzle-orm: ^0.30.0
  # ... more dependencies
```

## Checking for Updates

### List Outdated Packages

```bash
# Check all outdated packages
pnpm outdated

# Check recursively across workspace
pnpm -r outdated

# Check specific package
pnpm -F @sgcarstrends/api outdated

# Output:
# Package        Current  Latest  Wanted
# next           15.0.0   16.0.0  16.0.0
# react          18.2.0   19.0.0  19.0.0
# drizzle-orm    0.28.0   0.30.0  0.30.0
```

### Interactive Update

```bash
# Interactive upgrade tool
pnpm dlx npm-check-updates --interactive

# Or use taze (modern alternative)
pnpm dlx taze --interactive
```

## Upgrading Dependencies

### Update Catalog Versions

```yaml
# pnpm-workspace.yaml
catalog:
  # Before
  next: ^15.0.0

  # After
  next: ^16.0.0
```

### Update Package.json

```json
// package.json uses catalog:
{
  "dependencies": {
    "next": "catalog:",  // Automatically uses catalog version
    "react": "catalog:"
  }
}
```

### Install Updates

```bash
# Update all packages to catalog versions
pnpm install

# Update specific workspace
pnpm -F @sgcarstrends/web install

# Update recursively
pnpm -r install
```

## Safe Upgrade Process

### 1. Check Current Versions

```bash
# List current versions
pnpm list | grep package-name

# Check specific package
pnpm list next
```

### 2. Review Changelog

```bash
# Check package changelog
pnpm view next versions
pnpm view next --json | jq '.versions[-5:]'

# Visit GitHub releases
open https://github.com/vercel/next.js/releases
```

### 3. Check Breaking Changes

```bash
# Read upgrade guide
# Next.js example:
open https://nextjs.org/docs/app/building-your-application/upgrading/version-16

# Check migration codemods
pnpm dlx @next/codemod upgrade latest
```

### 4. Create Branch

```bash
# Create upgrade branch
git checkout -b upgrade/next-16

# Or for security patches
git checkout -b security/fix-vulnerabilities
```

### 5. Update Catalog

```yaml
# pnpm-workspace.yaml
catalog:
  next: ^16.0.0  # Upgraded from ^15.0.0
  react: ^19.0.0  # Upgraded from ^18.2.0
```

### 6. Install and Test

```bash
# Install updates
pnpm install

# Run tests
pnpm test

# Type check
pnpm tsc --noEmit

# Lint
pnpm biome check .

# Build
pnpm build

# Start development
pnpm dev
```

### 7. Fix Breaking Changes

```typescript
// Example: Next.js 16 async params
// Before (Next.js 15)
export default function Page({ params }: { params: { id: string } }) {
  return <div>{params.id}</div>;
}

// After (Next.js 16)
export default async function Page({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <div>{id}</div>;
}
```

### 8. Commit Changes

```bash
# Add changes
git add pnpm-workspace.yaml pnpm-lock.yaml

# Commit with conventional commit
git commit -m "chore(deps): upgrade Next.js to v16

- Upgrade Next.js 15 → 16
- Upgrade React 18 → 19
- Fix async params migration
- Run migration codemod

BREAKING CHANGE: Requires Node.js 20+"
```

## Major Version Upgrades

### Next.js Upgrade

```bash
# Step 1: Check current version
pnpm list next

# Step 2: Review upgrade guide
open https://nextjs.org/docs/app/building-your-application/upgrading

# Step 3: Run codemod
pnpm dlx @next/codemod@latest upgrade latest

# Step 4: Update catalog
vim pnpm-workspace.yaml

# Step 5: Install
pnpm install

# Step 6: Fix breaking changes
# - Async params
# - Async cookies/headers
# - Cache Components (if enabled)

# Step 7: Test
pnpm -F @sgcarstrends/web build
pnpm -F @sgcarstrends/web test
```

### React Upgrade

```bash
# Upgrade React 18 → 19
# Update catalog
catalog:
  react: ^19.0.0
  react-dom: ^19.0.0

# Install
pnpm install

# Check for breaking changes
# - Server Components (stable)
# - useTransition changes
# - Suspense improvements

# Test thoroughly
pnpm test
```

### TypeScript Upgrade

```bash
# Upgrade TypeScript 5.2 → 5.3
catalog:
  typescript: ^5.3.3

pnpm install

# Check for type errors
pnpm tsc --noEmit

# Fix any new strict checks
```

## Security Updates

### Check Vulnerabilities

```bash
# Audit dependencies
pnpm audit

# Output:
# High: Prototype pollution in lodash
# Package: lodash
# Patched in: >=4.17.21
# Path: lodash
```

### Apply Security Patches

```bash
# Update vulnerable package
# In catalog:
catalog:
  lodash: ^4.17.21  # Patched version

pnpm install

# Verify fix
pnpm audit

# Or use audit fix
pnpm audit --fix
```

### Automated Security PRs

Enable Dependabot:

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    groups:
      security:
        patterns:
          - "*"
        update-types:
          - "patch"
          - "minor"
```

## Dependency Conflicts

### Resolve Conflicts

```bash
# Issue: Peer dependency conflict
npm ERR! Could not resolve dependency:
npm ERR! peer react@"^18.0.0" from some-package@1.0.0

# Solution 1: Update catalog to compatible version
catalog:
  react: ^19.0.0
  some-package: ^2.0.0  # Version compatible with React 19

# Solution 2: Use overrides (last resort)
{
  "pnpm": {
    "overrides": {
      "react": "^19.0.0"
    }
  }
}
```

### Deduplicate Dependencies

```bash
# Check for duplicates
pnpm list --depth=0 | grep package-name

# Deduplicate
pnpm dedupe

# Verify
pnpm install
```

## Testing Upgrades

### Test Checklist

```bash
# 1. Type check
pnpm tsc --noEmit

# 2. Lint
pnpm biome check .

# 3. Unit tests
pnpm test

# 4. E2E tests
pnpm test:e2e

# 5. Build
pnpm build

# 6. Manual testing
pnpm dev
# Test critical flows manually

# 7. Check bundle size
pnpm -F @sgcarstrends/web build
# Review .next/analyze (if enabled)
```

### Rollback if Needed

```bash
# If upgrade causes issues
git reset --hard HEAD

# Or revert commit
git revert <commit-hash>

# Restore pnpm-lock.yaml
git checkout main -- pnpm-lock.yaml
pnpm install
```

## Automated Upgrades

### Renovate Bot

```json
// renovate.json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true
    }
  ],
  "schedule": ["before 3am on Monday"],
  "timezone": "Asia/Singapore"
}
```

## Best Practices

### 1. Update Gradually

```bash
# ❌ Update everything at once
pnpm dlx npm-check-updates -u
pnpm install

# ✅ Update incrementally
# Week 1: Update minor versions
# Week 2: Update React/Next.js
# Week 3: Update build tools
```

### 2. Read Changelogs

```bash
# ❌ Blindly upgrade
pnpm install next@latest

# ✅ Review changes first
pnpm view next --json | jq .versions
open https://github.com/vercel/next.js/releases
# Read breaking changes
# Update code accordingly
```

### 3. Test Thoroughly

```bash
# ❌ Only run unit tests
pnpm test

# ✅ Comprehensive testing
pnpm tsc --noEmit  # Type check
pnpm test          # Unit tests
pnpm test:e2e      # E2E tests
pnpm build         # Build check
# Manual testing
```

### 4. Commit Separately

```bash
# ❌ Mix feature and upgrades
git commit -m "feat: add feature X and upgrade deps"

# ✅ Separate commits
git commit -m "chore(deps): upgrade Next.js to v16"
git commit -m "feat: add feature X"
```

## Common Upgrades

### Next.js 15 → 16

```bash
# Run codemod
pnpm dlx @next/codemod@latest upgrade latest

# Update catalog
catalog:
  next: ^16.0.0
  react: ^19.0.0
  react-dom: ^19.0.0

# Install
pnpm install

# Fix breaking changes
# - Async params/searchParams
# - Async cookies/headers
# - Cache Components patterns
```

### Drizzle ORM

```bash
# Update catalog
catalog:
  drizzle-orm: ^0.30.0
  drizzle-kit: ^0.20.0

pnpm install

# Generate new migrations if schema changed
pnpm -F @sgcarstrends/database db:generate
```

### Biome (replacing ESLint)

```bash
# Remove ESLint
pnpm remove -r eslint @typescript-eslint/*

# Add Biome
catalog:
  "@biomejs/biome": ^1.9.4

pnpm install

# Migrate config
pnpm dlx @biomejs/biome migrate eslint --write
```

## Troubleshooting

### Lockfile Conflicts

```bash
# Issue: pnpm-lock.yaml conflicts
# Solution: Regenerate lockfile

rm pnpm-lock.yaml
pnpm install
```

### Peer Dependency Warnings

```bash
# Issue: Peer dependency warning
# Solution: Update to compatible versions

# Check peer dependencies
pnpm why package-name

# Update catalog
catalog:
  package-name: ^2.0.0
```

### Build Failures After Upgrade

```bash
# Issue: Build fails after upgrade
# Solution: Clear caches

rm -rf node_modules .turbo dist .next
pnpm install
pnpm build
```

## References

- pnpm Catalog: https://pnpm.io/catalogs
- npm-check-updates: https://github.com/raineorshine/npm-check-updates
- Next.js Codemods: https://nextjs.org/docs/app/building-your-application/upgrading/codemods
- Renovate: https://docs.renovatebot.com
- Related files:
  - `pnpm-workspace.yaml` - Catalog configuration
  - `package.json` - Package dependencies
  - Root CLAUDE.md - Dependency guidelines

## Best Practices Summary

1. **Use Catalog**: Centralize versions in pnpm-workspace.yaml
2. **Test Thoroughly**: Run all tests after upgrades
3. **Read Changelogs**: Review breaking changes before upgrading
4. **Upgrade Incrementally**: Don't update everything at once
5. **Commit Separately**: Separate dependency upgrades from features
6. **Automate Security**: Use Dependabot or Renovate for patches
7. **Check Compatibility**: Verify peer dependencies
8. **Document Changes**: Note breaking changes in commit message
