---
name: "@gw-multi-worktree-dev"
description: Advanced patterns for developing across multiple Git worktrees simultaneously. Use this skill when managing dependencies across worktrees, synchronizing files, handling databases for multiple branches, running parallel tests, or orchestrating services across worktrees. Triggers on tasks involving multi-branch development, dependency sharing, database isolation, or service orchestration with gw.
license: MIT
metadata:
  author: mthines
  version: "1.0.0"
---

# Multi-Worktree Development - Comprehensive Guide

Advanced patterns for developing across multiple Git worktrees simultaneously.

## Table of Contents

1. [Parallel Development Workflows](#1-parallel-development-workflows)
2. [Dependency Management](#2-dependency-management)
3. [File Synchronization](#3-file-synchronization)
4. [Database and Service Management](#4-database-and-service-management)
5. [Testing Workflows](#5-testing-workflows)
6. [Build Artifact Management](#6-build-artifact-management)
7. [Team Collaboration](#7-team-collaboration)
8. [Performance and Optimization](#8-performance-and-optimization)

---

## 1. Parallel Development Workflows

### Benefits of Parallel Development

Working on multiple branches simultaneously eliminates:
- Context switching overhead
- IDE reindexing delays
- Stashing/committing incomplete work
- Mental context loss

### Setting Up Multiple Worktrees

```bash
# Create worktrees for different features
gw add feat/user-auth
gw add feat/payment-gateway
gw add feat/email-notifications

# List all worktrees
gw list
```

### Managing Mental Context

**Strategy 1: Dedicated terminals**
```bash
# Terminal 1: User Auth
gw cd feat/user-auth
npm run dev

# Terminal 2: Payment Gateway
gw cd feat/payment-gateway
npm run dev
```

**Strategy 2: Terminal multiplexer (tmux)**
```bash
# Create named sessions
tmux new -s auth
gw cd feat/user-auth

tmux new -s payments
gw cd feat/payment-gateway

# Switch between sessions
tmux attach -t auth
tmux attach -t payments
```

**Strategy 3: IDE workspaces**

VS Code multi-root workspace:
```json
{
  "folders": [
    {"name": "Auth Feature", "path": "../feat/user-auth"},
    {"name": "Payments", "path": "../feat/payment-gateway"}
  ]
}
```

### Quick Context Switching

```bash
# Fast navigation with partial matching
gw cd auth     # Matches feat/user-auth
gw cd pay      # Matches feat/payment-gateway
```

---

## 2. Dependency Management

### Understanding the Problem

Each worktree has independent working files, including `node_modules`:

```
repo.git/
├── main/
│   └── node_modules/     # ~500MB
├── feat/user-auth/
│   └── node_modules/     # ~500MB (duplicate!)
└── feat/payment-gateway/
    └── node_modules/     # ~500MB (duplicate!)
```

With 5 worktrees: **2.5GB** of duplicated dependencies!

### Strategy 1: Accept Duplication (Simplest)

**Pros:** Full isolation, no conflicts
**Cons:** Disk space usage

```bash
# Each worktree installs independently
gw add feat/new-feature
gw cd feat/new-feature
npm install
```

Best for: Testing different dependency versions, small projects.

### Strategy 2: Use pnpm (Recommended)

pnpm uses a content-addressable store that deduplicates packages:

```bash
# Install pnpm
npm install -g pnpm

# In each worktree
gw cd feat/user-auth
pnpm install  # Uses shared store

gw cd feat/payment-gateway
pnpm install  # Reuses cached packages
```

**Result:** Near-zero duplication, full isolation.

### Strategy 3: Symlink node_modules (Advanced)

**Warning:** Only works if all worktrees need identical dependencies.

```bash
# In feature worktree
gw cd feat/user-auth
rm -rf node_modules
ln -s ../main/node_modules node_modules
```

**Risks:**
- Package version conflicts
- Native modules may break
- Hoisting issues

Best for: Read-only testing, identical environments.

### Strategy 4: Post-Add Hook for Auto-Install

```bash
gw init --post-add "npm install"
```

Now every `gw add` automatically installs dependencies.

---

## 3. File Synchronization

### Using `gw sync`

Sync files between worktrees without recreating them:

```bash
# Sync all autoCopyFiles from config
gw sync feat/user-auth

# Sync specific file from main to feature branch
gw sync feat/user-auth .env

# Sync from specific source
gw sync --from staging feat/user-auth .env

# Sync multiple files
gw sync feat/user-auth .env secrets/ config/local.json
```

### Common Sync Patterns

**Pattern 1: Update secrets across all worktrees**

```bash
# After updating .env in main - sync autoCopyFiles to all worktrees
for worktree in $(gw list | grep -v main | awk '{print $1}' | xargs -n1 basename); do
  gw sync "$worktree"
done

# Or sync specific file
for worktree in $(gw list | grep -v main | awk '{print $1}' | xargs -n1 basename); do
  gw sync "$worktree" .env
done
```

**Pattern 2: Propagate config changes**

```bash
# Updated shared config in main
gw cd feat/user-auth
gw sync --from main feat/user-auth config/shared.json
```

**Pattern 3: Hot-swap environment**

```bash
# Test feature with production-like config
gw sync --from production-mirror feat/user-auth .env
```

### Dry Run Mode

Preview what would be synced:

```bash
gw sync --dry-run feat/user-auth .env secrets/
```

---

## 4. Database and Service Management

### Database Isolation Strategies

**Strategy 1: Separate databases per worktree**

```bash
# In feat/user-auth/.env
DATABASE_URL=postgresql://localhost:5432/myapp_auth

# In feat/payment-gateway/.env
DATABASE_URL=postgresql://localhost:5432/myapp_payments
```

**Strategy 2: Docker Compose per worktree**

Create `docker-compose.worktree.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    ports:
      - "${DB_PORT:-5432}:5432"
    environment:
      POSTGRES_DB: myapp_${WORKTREE_NAME:-dev}
```

```bash
# In each worktree
export WORKTREE_NAME=$(basename $PWD)
export DB_PORT=5433  # Different port per worktree
docker-compose -f docker-compose.worktree.yml up -d
```

**Strategy 3: Shared database with schema prefixes**

```sql
-- feat/user-auth uses schema: auth_feature
CREATE SCHEMA auth_feature;

-- feat/payment-gateway uses schema: payments_feature
CREATE SCHEMA payments_feature;
```

### Port Management

Avoid port conflicts between worktrees:

```bash
# main/.env
PORT=3000
DB_PORT=5432

# feat/user-auth/.env
PORT=3001
DB_PORT=5433

# feat/payment-gateway/.env
PORT=3002
DB_PORT=5434
```

### Service Orchestration

Running frontend and backend in separate worktrees:

```bash
# Terminal 1: API (main branch)
gw cd main
npm run dev:api  # Port 3001

# Terminal 2: Frontend (feature branch)
gw cd feat/new-ui
API_URL=http://localhost:3001 npm run dev:web  # Port 3000
```

---

## 5. Testing Workflows

### Parallel Testing Across Environments

Test the same feature in multiple environments:

```bash
# Create test worktrees
gw add test-node18 --force
gw add test-node20 --force

# Terminal 1: Node 18
gw cd test-node18
nvm use 18
npm install && npm test

# Terminal 2: Node 20
gw cd test-node20
nvm use 20
npm install && npm test
```

### CI/CD Integration

**GitHub Actions with worktrees:**

```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node ${{ matrix.node }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm install
      - run: npm test
```

**Local simulation:**

```bash
#!/bin/bash
# test-matrix.sh
for version in 18 20 22; do
  gw add "test-node$version" --force
  (
    gw cd "test-node$version"
    nvm use "$version"
    npm install
    npm test
  ) &
done
wait
echo "All tests complete"
```

### Test Isolation

Each worktree can have different test configurations:

```bash
# In feat/user-auth
npm test -- --testPathPattern="auth"

# In feat/payment-gateway
npm test -- --testPathPattern="payment"
```

---

## 6. Build Artifact Management

### Separate Build Outputs

Each worktree maintains independent build artifacts:

```
repo.git/
├── main/
│   └── dist/        # Production build
├── feat/user-auth/
│   └── dist/        # Feature build
└── feat/payment-gateway/
    └── dist/        # Different feature build
```

### Sharing Build Caches

**Turborepo/Nx caching:**

```bash
# Turbo's cache is shared automatically
gw cd feat/user-auth
pnpm turbo build  # Fast: uses cache from main
```

**Manual cache sharing:**

```bash
# Share .next/cache between worktrees
ln -s ../main/.next/cache .next/cache
```

### Clean Build Strategies

When you need guaranteed clean builds:

```bash
# Remove build artifacts
rm -rf dist/ .next/ build/

# Fresh install and build
rm -rf node_modules/
npm install
npm run build
```

---

## 7. Team Collaboration

### Code Review Workflows

**Reviewer worktree pattern:**

```bash
# Create worktree from PR branch
gw add review-pr-123
gw cd review-pr-123

# Review code, run tests
npm install
npm test
npm run dev  # Manual testing

# Leave review comments
# ...

# Clean up
gw remove review-pr-123
```

### Pair Programming

**Each developer in their own worktree:**

```bash
# Developer A
gw add pair/feature-x-alice
gw cd pair/feature-x-alice
# Work on frontend...

# Developer B
gw add pair/feature-x-bob
gw cd pair/feature-x-bob
# Work on backend...

# Sync changes via git
git pull origin pair/feature-x
```

### Demo Environments

**One worktree per demo:**

```bash
# Create demo worktrees
gw add demo/client-a
gw add demo/client-b

# Each with different configuration
# demo/client-a/.env
FEATURE_FLAGS=clientA

# demo/client-b/.env
FEATURE_FLAGS=clientB
```

---

## 8. Performance and Optimization

### Monitoring Disk Usage

```bash
# Check worktree sizes
du -sh /path/to/repo.git/*/

# Find large node_modules
du -sh /path/to/repo.git/*/node_modules/ | sort -h
```

### Cleanup Strategies

**Remove old worktrees:**

```bash
# List worktrees older than 2 weeks (by branch last commit)
gw list | while read path commit branch; do
  age=$(git log -1 --format=%cr "$branch" 2>/dev/null)
  echo "$branch: $age"
done

# Remove stale worktrees
gw remove feat/old-feature-1
gw remove feat/old-feature-2
```

**Prune stale references:**

```bash
gw prune
```

### Resource Balancing

**Limit concurrent worktrees:**
- Development machine: 3-5 active worktrees
- CI machine: As many as needed (ephemeral)

**Memory considerations:**
- Each running dev server uses memory
- Each `node_modules` uses disk space
- Database containers use memory + disk

**Recommended setup:**
```bash
# Keep essential worktrees
main/           # Always ready
feat/current/   # Active feature
review/         # Code review (temporary)
hotfix/         # Emergency fixes (temporary)
```

### When NOT to Use Multiple Worktrees

Consider alternatives when:
- Single small fix → Just commit and switch back
- Same file being edited → Use branches instead
- Limited disk space → Use branch switching
- Team uses different workflow → Align first

---

## Summary

You now understand:

- ✅ Managing parallel development workflows effectively
- ✅ Dependency strategies (pnpm recommended)
- ✅ Keeping files in sync with `gw sync`
- ✅ Database and service isolation patterns
- ✅ Parallel testing across environments
- ✅ Build artifact management
- ✅ Team collaboration patterns
- ✅ Performance optimization techniques

### Next Steps

1. Set up pnpm for efficient dependency management
2. Configure post-add hooks for automatic setup
3. Create team guidelines for worktree usage
4. Implement cleanup automation

### Additional Resources

- [Sharing Dependencies Example](./examples/sharing-dependencies.md)
- [Parallel Testing Example](./examples/parallel-testing.md)
- [Database Management Example](./examples/database-management.md)
- [Service Orchestration Example](./examples/service-orchestration.md)

---

*Part of the [gw-tools skills collection](../README.md)*
