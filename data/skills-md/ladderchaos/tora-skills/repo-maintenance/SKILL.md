---
name: repo-maintenance
description: Manage repository versioning, releases, deployments, and documentation. Use this skill for version bumps, changelog updates, deployment syncs, status tracking, and release management.
---

# Repo Maintenance

This skill guides repository maintenance tasks including version control, release management, deployment synchronization, and documentation updates for the Sooth Protocol monorepo.

## When to Use This Skill

Invoke this skill when:
- Updating CHANGELOG.md after features, fixes, or deployments
- Bumping version numbers in package.json or config files
- Syncing deployment addresses after contract deploys
- Updating STATUS.md with current project state
- Preparing releases or deployments
- Managing branch workflows and conventional commits

## Core Files

| File | Purpose | Update Frequency |
|------|---------|------------------|
| `CHANGELOG.md` | Release history with breaking changes, fixes, deployments | Per release |
| `STATUS.md` | Live project status, current deployments, pending work | Per session |
| `DECISIONS.md` | Architectural Decision Records (ADRs) | Per major decision |
| `apps/web/src/config/deployments.json` | Canonical contract addresses (source of truth) | Per deployment |
| `apps/web/src/config/markets.json` | Active markets per chain | Per market creation |
| `packages/contracts-evm/package.json` | Contract version (semantic) | Per contract release |

## Version Bump Workflow

### 1. Identify Version Type

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| Breaking API change | Major (X.0.0) | Interface signature change |
| New feature | Minor (0.X.0) | New contract function |
| Bug fix | Patch (0.0.X) | Logic correction |

### 2. Update Version Files

```bash
# Contract version (packages/contracts-evm/package.json)
# Update "version" field

# Frontend cache invalidation (apps/web/src/config/deployments.json)
# Bump "version" field to force browser refresh
```

### 3. Update CHANGELOG.md

Follow this format:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### ⚠️ BREAKING CHANGE
- **Description**: What changed and migration steps

### Fixed
- **Bug Name** (date): Root cause and solution

### Added
- **Feature Name**: Description with test count

### Deployed
- **Network Name VX.Y.Z**:
  - **Contract**: `0xAddress`

### Coverage
- X tests passing (Y new)
- ContractName: XX.XX% lines, XX.XX% functions
```

## Deployment Sync Workflow

After any contract deployment:

### 1. Verify On-Chain State (MANDATORY)

```bash
cd packages/contracts-evm
source .env

# Verify core contracts are live
cast call $LAUNCHPAD_ENGINE "owner()" --rpc-url $BASE_SEPOLIA_RPC_URL
cast call $COLLATERALIZER "usdc()" --rpc-url $BASE_SEPOLIA_RPC_URL
cast call $AMM_ENGINE "usdc()" --rpc-url $BASE_SEPOLIA_RPC_URL

# Verify market initialization
cast call $LAUNCHPAD_ENGINE "isInitialized(address)" $MARKET --rpc-url $BASE_SEPOLIA_RPC_URL
```

**STOP if any check fails.**

### 2. Update deployments.json (Canonical Source)

```json
{
  "version": "9.1.0",  // BUMP THIS to invalidate browser cache
  "lastUpdated": "2025-12-29T00:00:00Z",
  "networks": {
    "84532": {
      "name": "Base Sepolia",
      "contracts": {
        "LaunchpadEngine": "0x...",
        "AMMEngine": "0x...",
        "TickBookPoolManager": "0x..."
      }
    }
  }
}
```

### 3. Run Sync Script

```bash
./sync-deployments.sh
```

This copies from `apps/web/src/config/deployments.json` to `packages/contracts-evm/deployments.json`.

### 4. Verify Frontend Build

```bash
cd apps/web
npm run build  # Runs validate-config.js automatically
```

### 5. Update STATUS.md

Add new deployment addresses to the Active Deployment tables.

### 6. Commit with Conventional Format

```bash
git add apps/web/src/config/deployments.json apps/web/src/config/markets.json STATUS.md CHANGELOG.md
git commit -m "feat(deploy): V9.1.0 to Base Sepolia

- AMMEngine: 0x...
- LaunchpadEngine: 0x...

🤖 Generated with Claude Code"
```

## STATUS.md Update Pattern

Update STATUS.md during each work session:

### Session Start
- Check "Pending Work" section for context
- Review "Active Deployment" tables for current state

### During Session
- Move completed items from "Pending Work" to "Completed This Session"
- Add new pending items as discovered

### Session End
- Update version badges at top if deployment occurred
- Update deployment address tables if contracts changed
- Add session summary at bottom

### Format

```markdown
# Project Status

> Last Updated: YYYY-MM-DD (VX.Y.Z Description)

- **✅ FEATURE DEPLOYED** — Brief description
- **⚠️ KNOWN ISSUE** — Brief description with workaround

## 🆕 VX.Y.Z Feature Name (YYYY-MM-DD)
**Summary**: What this version adds/fixes

### Contract Changes
| Contract | Change |
|----------|--------|
| **ContractName** | Description of change |

### New Tests (N)
| Test | Priority | Status |
|------|----------|--------|
| `test_Name` | P0 | ✅ |

### VX.Y.Z Deployed Addresses (Network)
| Contract | Address |
|----------|---------|
| **ContractName** | `0x...` |

## Pending Work (Next Session)
- [ ] **Task** — Description with effort estimate (S/M/L)

## Completed This Session (YYYY-MM-DD)
- ✅ **Task** — What was done
```

## Conventional Commits

Use this format for all commits:

```
<type>(<scope>): <description>

[optional body]

🤖 Generated with Claude Code
```

### Types
| Type | Use For |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes bug nor adds feature |
| `test` | Adding or updating tests |
| `chore` | Maintenance tasks |
| `deploy` | Deployment-related changes (often `feat(deploy):`) |

### Scopes
| Scope | Package/Area |
|-------|--------------|
| `contracts` | packages/contracts-evm |
| `web` | apps/web |
| `deploy` | Deployment configuration |
| `config` | Configuration files |

## Pre-Commit Hook Behavior

The `.husky/pre-commit` hook runs when staging deployment configs:

1. **Deployment Verification**: Runs `./script/verify-deployment.sh` when `deployments.json` or `markets.json` are staged
2. **Version Bump Warning**: Alerts if `deployments.json` changed but version not bumped

If hook fails, fix the issue before committing.

## ADR (Architectural Decision Record) Format

For major decisions, add to DECISIONS.md:

```markdown
## ADR-XXX: Decision Title

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded

### Context
What is the issue that we're seeing that motivates this decision?

### Decision
What is the change that we're proposing and/or doing?

### Consequences
What becomes easier or more difficult because of this change?
```

## Quick Reference Commands

```bash
# Check current versions
cat packages/contracts-evm/package.json | grep version
cat apps/web/src/config/deployments.json | grep version

# Verify deployment
cd packages/contracts-evm && source .env
cast call $LAUNCHPAD_ENGINE "owner()" --rpc-url $BASE_SEPOLIA_RPC_URL

# Sync after deployment
./sync-deployments.sh

# Build to verify config
cd apps/web && npm run build

# View recent commits for message style
git log --oneline -10
```

## Browser Cache Invalidation

After deployment sync, users need to hard refresh:
- **Chrome/Edge**: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
- **Firefox**: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)

The `version` field in `deployments.json` triggers automatic cache invalidation when bumped.

## Multi-Network Deployment

When deploying to multiple networks:

1. Deploy to each network separately
2. Update `deployments.json` with all network addresses
3. Update `markets.json` with markets per chain
4. Bump version once (covers all networks)
5. Document all deployments in CHANGELOG.md

## Effort Estimates

Use these labels for pending work:
- **S (Small)**: < 2 hours
- **M (Medium)**: 2-6 hours
- **L (Large)**: > 6 hours

## Version File Organization

When upgrading to a new major version, archive previous version files to maintain history while keeping the working directory clean.

### Directory Structure

```
copan/
├── packages/contracts-evm/
│   ├── deployments/
│   │   ├── v9-latest.json           # Current version
│   │   ├── v9-baseSepolia.json      # Per-network current
│   │   ├── v9-monadTestnet.json
│   │   └── v8-archive/              # Previous version archive
│   │       ├── v8-latest.json
│   │       ├── v8-baseSepolia.json
│   │       └── README.md
│   │
│   ├── docs/
│   │   ├── v9/                      # Active version docs
│   │   └── _archive/                # Archived docs
│   │       ├── v8/
│   │       ├── v7/
│   │       └── v6/
│   │
│   ├── test/v9/                     # Active version tests
│   ├── archive_tests/               # Archived tests
│   │   └── v8/
│   │
│   ├── abi/v9/                      # Active ABIs
│   └── archive_scripts/             # Deprecated scripts
│
├── apps/web/
│   ├── src/config/
│   │   ├── deployments.json         # Canonical (current)
│   │   └── markets.json             # Current markets
│   ├── archive/                     # Frontend archives
│   │   └── v8/
│   └── docs/_archive/
│       └── v8-implementation/
```

### Archive Locations by Artifact Type

| Artifact | Active Location | Archive Pattern |
|----------|-----------------|-----------------|
| **Deployments** | `deployments/v{N}-*.json` | `deployments/v{N-1}-archive/` |
| **Docs** | `docs/v{N}/` | `docs/_archive/v{N-1}/` |
| **Tests** | `test/v{N}/` | `archive_tests/v{N-1}/` |
| **Scripts** | `script/` | `archive_scripts/` |
| **Frontend** | `apps/web/src/` | `apps/web/archive/v{N-1}/` |
| **ABIs** | `abi/v{N}/` | Keep in place (small files) |

### Major Version Upgrade Checklist

When releasing a new major version (e.g., V9 → V10):

1. **Archive Deployments**
   ```bash
   cd packages/contracts-evm/deployments
   mkdir v9-archive
   mv v9-*.json v9-archive/
   echo "# V9 Archive\nArchived: $(date)\nReason: V10 release" > v9-archive/README.md
   ```

2. **Archive Version-Specific Docs**
   ```bash
   mv docs/v9 docs/_archive/v9
   mkdir docs/v10
   ```

3. **Archive Version-Specific Tests** (if superseded)
   ```bash
   mkdir -p archive_tests/v9
   mv test/v9/* archive_tests/v9/  # Only if tests no longer apply
   ```

4. **Create New Version Files**
   ```bash
   touch deployments/v10-latest.json
   mkdir docs/v10
   mkdir test/v10
   ```

5. **Update package.json**
   ```json
   {
     "version": "10.0.0",
     "description": "Sooth Protocol V10 EVM Contracts"
   }
   ```

6. **Document in CHANGELOG.md**
   ```markdown
   ## [10.0.0] - YYYY-MM-DD

   ### ⚠️ BREAKING CHANGE
   - Major architecture change (see docs/v10/)
   - V9 contracts archived to deployments/v9-archive/
   ```

### What NOT to Archive

- **CHANGELOG.md** — Always append, never archive
- **STATUS.md** — Rolling document, clear old sessions periodically
- **DECISIONS.md** — Append ADRs, mark old ones as "Superseded"
- **Core contracts** — Keep all versions in `contracts/` (git tracks history)
- **Root configs** — `package.json`, `foundry.toml`, etc. are versioned in git

### Archive README Template

Create a `README.md` in each archive folder:

```markdown
# V{N} Archive

**Archived**: YYYY-MM-DD
**Superseded By**: V{N+1}
**Reason**: [Brief explanation]

## Contents
- `v{N}-latest.json` — Final deployment addresses
- `v{N}-baseSepolia.json` — Base Sepolia deployment
- `v{N}-monadTestnet.json` — Monad deployment

## Historical Context
[Brief summary of what this version implemented]

## Migration Notes
[Any notes for understanding changes to next version]
```

### Quick Archive Commands

```bash
# Archive a version's deployments
VERSION=9
cd packages/contracts-evm/deployments
mkdir v${VERSION}-archive
mv v${VERSION}-*.json v${VERSION}-archive/

# Archive version docs
cd ../docs
mv v${VERSION} _archive/v${VERSION}

# Archive version tests (if applicable)
cd ../
mkdir -p archive_tests/v${VERSION}
mv test/v${VERSION}/* archive_tests/v${VERSION}/
```
