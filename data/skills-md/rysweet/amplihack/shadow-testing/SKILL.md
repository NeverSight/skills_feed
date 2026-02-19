---
name: shadow-testing
description: |
  Creates isolated container environments for testing local uncommitted changes before pushing.
  Use when testing library changes, multi-repo coordination, or validating "works on my machine" → "works in CI".
  Provides git bundle snapshots, embedded git server, selective URL rewriting, and package manager cache isolation.
  Works with any coding agent via standalone CLI, shell scripts, or Docker Compose.
version: 1.0.0
amplifier_bundle: https://github.com/microsoft/amplifier-bundle-shadow
---

# Shadow Testing Skill

## Purpose [LEVEL 1]

Shadow testing creates **isolated container environments** where you can test local uncommitted changes without affecting your host system or pushing to remote repositories.

**Key Principle**: Test exactly what's on your machine (including uncommitted changes) in a clean, isolated environment that mirrors CI.

## When to Use This Skill [LEVEL 1]

### Perfect For

- **Pre-Push Validation**: Test changes before committing/pushing
- **Multi-Repo Coordination**: Validate changes across multiple repositories work together
- **Clean-State Testing**: "Does it work on a fresh machine?"
- **Library Development**: Test library changes with dependent projects
- **CI Parity**: See what CI will see before pushing
- **Destructive Testing**: Tests that modify system state won't affect host

### Use This Skill When

- Making breaking changes to a library others depend on
- Coordinating changes across multiple repositories
- Unsure if your changes will work in CI
- Need to test with specific dependency versions
- Want to verify install/setup procedures work
- Testing changes that require clean environment state

### Don't Use This Skill When

- Running unit tests on already-committed code (use local test runner)
- Need to debug with live code changes (shadow captures snapshots)
- Testing production deployment (use staging environments)
- Simple single-file changes with good test coverage

## Core Concepts [LEVEL 1]

### Shadow Environment Architecture

A shadow environment is a Docker/Podman container with:

1. **Git Bundle Snapshots** - Exact working tree state (including uncommitted changes)
2. **Embedded Gitea Server** - Local git server at localhost:3000 inside container
3. **Selective URL Rewriting** - Git `insteadOf` rules redirect specific repos to local Gitea
4. **Package Manager Isolation** - UV, pip, npm, cargo, go caches isolated per shadow
5. **API Key Passthrough** - Common API keys automatically forwarded to container

```
┌─────────────────────────────────────────────────────────┐
│  Shadow Container                                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Gitea Server (localhost:3000)                    │  │
│  │  - myorg/my-library (your snapshot)               │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  Git URL Rewriting:                                     │
│  github.com/myorg/my-library → Gitea (local)           │
│  github.com/myorg/other-repo → Real GitHub             │
│                                                         │
│  /workspace (pre-cloned local sources)                 │
└─────────────────────────────────────────────────────────┘
```

### How Git URL Rewriting Works

When you create a shadow with `~/repos/my-lib:myorg/my-lib`:

1. Your working directory is captured **exactly as-is** (uncommitted changes included)
2. Snapshot is bundled with full git history
3. Container starts with Gitea server
4. Snapshot pushed to Gitea as `myorg/my-lib`
5. Git config adds `insteadOf` rules:
   ```
   [url "http://shadow:shadow@localhost:3000/myorg/my-lib.git"]
       insteadOf = https://github.com/myorg/my-lib.git
   ```
6. Any `git clone https://github.com/myorg/my-lib` → uses YOUR local snapshot
7. All other GitHub URLs → fetch from real GitHub

**Result**: Only your specified repos are local; everything else uses production sources.

## Quick Start [LEVEL 1]

### Installation

**For Amplifier Users** (native integration):

```bash
# Shadow tool is built-in - no installation needed
amplifier run --bundle amplihack
```

**For Other Agents** (standalone CLI):

```bash
# Install via uvx (recommended)
uvx amplifier-shadow --version

# Or via pip
pip install amplifier-bundle-shadow

# Verify installation
amplifier-shadow --version
```

**Prerequisites**:

- Docker or Podman installed and running
- Git installed

### Your First Shadow (CLI)

```bash
# Create shadow with your local library changes
amplifier-shadow create --local ~/repos/my-library:myorg/my-library --name test-lib

# Inside the shadow, install via git URL
# → my-library uses YOUR LOCAL snapshot
# → all other dependencies fetch from REAL GitHub
amplifier-shadow exec test-lib "uv pip install git+https://github.com/myorg/my-library"

# Run tests
amplifier-shadow exec test-lib "cd /workspace && pytest"

# See what changed
amplifier-shadow diff test-lib

# Clean up when done
amplifier-shadow destroy test-lib
```

### Your First Shadow (Amplifier Tool)

```python
# Create shadow with local changes
shadow.create(local_sources=["~/repos/my-library:myorg/my-library"])

# Execute commands
shadow.exec(shadow_id, "uv pip install git+https://github.com/myorg/my-library")
shadow.exec(shadow_id, "pytest tests/")

# Extract results
shadow.extract(shadow_id, "/workspace/test-results", "./results")

# Cleanup
shadow.destroy(shadow_id)
```

## Tool Reference by Agent Type [LEVEL 2]

### Amplifier (Native Integration)

**Best experience** - shadow is a first-class tool with automatic setup:

```python
# All operations via shadow tool
result = shadow.create(
    local_sources=["~/repos/lib:org/lib"],
    verify=True  # Automatic smoke test
)

# Integrated error handling and observability
if result.ready:
    shadow.exec(result.shadow_id, "pytest")
```

**Features**:

- Automatic API key passthrough
- Built-in smoke tests and health checks
- Integrated with other Amplifier tools
- Session-aware cleanup

### Claude Code Standalone

Use the CLI directly from bash tool:

```bash
# All operations via amplifier-shadow CLI
uvx amplifier-shadow create --local ~/repos/my-lib:org/my-lib --name test

uvx amplifier-shadow exec test "pip install -e /workspace/org/my-lib"
uvx amplifier-shadow exec test "pytest"

uvx amplifier-shadow destroy test
```

### GitHub Copilot

Same CLI interface as Claude Code:

```bash
# Install once
pip install amplifier-bundle-shadow

# Use in workflow
amplifier-shadow create --local ~/repos/lib:org/lib
amplifier-shadow exec shadow-xxx "npm install && npm test"
```

### Manual/DIY (Any Agent)

Use the provided shell scripts and Docker Compose examples (see Level 3).

## Common Patterns [LEVEL 2]

### Pattern: Test Library Changes Before Publishing

```bash
# Test your library with its dependents
amplifier-shadow create --local ~/repos/my-library:myorg/my-library --name lib-test

# Clone dependent project and install
amplifier-shadow exec lib-test "
  cd /workspace &&
  git clone https://github.com/myorg/dependent-app &&
  cd dependent-app &&
  uv venv && . .venv/bin/activate &&
  uv pip install git+https://github.com/myorg/my-library &&
  pytest
"
```

### Pattern: Multi-Repo Changes

```bash
# Testing changes across multiple repos
amplifier-shadow create \
    --local ~/repos/core-lib:myorg/core-lib \
    --local ~/repos/cli-tool:myorg/cli-tool \
    --name multi-test

# Both local sources will be used
amplifier-shadow exec multi-test "uv pip install git+https://github.com/myorg/cli-tool"
```

### Pattern: Iterate on Failures

```bash
# 1. Create shadow and run tests
amplifier-shadow create --local ~/repos/lib:org/lib --name test
amplifier-shadow exec test "pytest" # Fails

# 2. Fix code locally on host

# 3. Destroy and recreate (picks up your local changes)
amplifier-shadow destroy test
amplifier-shadow create --local ~/repos/lib:org/lib --name test
amplifier-shadow exec test "pytest" # Passes

# 4. Commit with confidence!
git commit -m "Fix issue"
```

### Pattern: Pre-Push CI Validation

```bash
# Run your CI script in shadow before pushing
amplifier-shadow create --local ~/repos/project:org/project --name ci-check

amplifier-shadow exec ci-check "
  cd /workspace/org/project &&
  ./scripts/ci.sh
"

# If CI script passes, your push will likely succeed
```

## Verification Best Practices [LEVEL 2]

### Always Verify Local Sources Are Used

After creating a shadow, confirm your local code is actually being used:

```bash
# Step 1: Check snapshot commits (from create output)
amplifier-shadow create --local ~/repos/lib:org/lib
# Output shows: snapshot_commits: {"org/lib": "abc1234..."}

# Step 2: Compare with install output
amplifier-shadow exec shadow-xxx "uv pip install git+https://github.com/org/lib"
# Look for: lib @ git+...@abc1234

# If commits match, your local code is being used!
```

### Pre-Cloned Repository Locations

Local sources are automatically cloned to `/workspace/{org}/{repo}`:

```bash
# Your local source microsoft/my-library is available at:
/workspace/microsoft/my-library

# Use for editable installs (Python)
amplifier-shadow exec shadow-xxx "pip install -e /workspace/microsoft/my-library"

# Or for Node.js
amplifier-shadow exec shadow-xxx "cd /workspace/microsoft/my-package && npm install"
```

**Always check this location first** - the repo is already there.

### Environment Variable Verification

```bash
# Don't assume - verify API keys are present!
amplifier-shadow exec shadow-xxx "env | grep API_KEY"

# Check all passed variables
amplifier-shadow status shadow-xxx
# Shows: env_vars_passed: ["ANTHROPIC_API_KEY", ...]
```

## Troubleshooting [LEVEL 2]

### Common Issues

**"UV tool install" uses cache instead of local source**:

Problem: UV may bypass git URL rewriting for cached packages.

Solution:

```bash
# Option 1: Install from pre-cloned workspace (recommended)
amplifier-shadow exec xxx "pip install -e /workspace/org/lib"

# Option 2: Clear UV cache first
amplifier-shadow exec xxx "rm -rf /tmp/uv-cache && uv tool install git+https://github.com/org/lib"
```

**"PEP 668: Externally-Managed Environment"**:

Solution: Always use virtual environments inside shadow:

```bash
amplifier-shadow exec xxx "
  cd /workspace &&
  uv venv &&
  . .venv/bin/activate &&
  uv pip install ...
"
```

**"Container image not found"**:

Solution: Build the image locally:

```bash
amplifier-shadow build
```

**"/workspace permission denied"**:

Solution: Use `$HOME` or `/tmp` as alternatives:

```bash
amplifier-shadow exec xxx "cd $HOME && git clone ..."
```

## Level 3: Advanced Topics [LEVEL 3]

### Custom Docker Images

Build your own shadow image with additional tools:

```dockerfile
FROM ghcr.io/microsoft/amplifier-shadow:latest

# Add your tools
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools

# Add custom scripts
COPY my-test-script.sh /usr/local/bin/
```

Build and use:

```bash
docker build -t my-shadow:latest .
amplifier-shadow create --image my-shadow:latest --local ~/repos/lib:org/lib
```

### Shell Scripts (DIY Shadow Setup)

For agents without Amplifier access, use these standalone scripts:

**Script 1: Create Git Bundle** (`scripts/create-bundle.sh`):

```bash
#!/bin/bash
# Create git bundle snapshot of working tree

REPO_PATH=$1
OUTPUT_PATH=$2

cd "$REPO_PATH"

# Fetch all refs to ensure complete history
git fetch --all --tags --quiet 2>/dev/null || true

# Check for uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
    # Create temp clone and commit changes
    TEMP_DIR=$(mktemp -d)
    git clone --quiet "$REPO_PATH" "$TEMP_DIR"

    # Sync working tree (including deletions)
    rsync -a --delete --exclude='.git' "$REPO_PATH/" "$TEMP_DIR/"

    cd "$TEMP_DIR"
    git add -A
    git commit --allow-empty -m "Shadow snapshot" --author="Shadow <shadow@localhost>"

    # Create bundle
    git bundle create "$OUTPUT_PATH" --all

    cd /
    rm -rf "$TEMP_DIR"
else
    # Clean repo - just bundle it
    git bundle create "$OUTPUT_PATH" --all
fi

echo "Bundle created: $OUTPUT_PATH"
```

**Script 2: Setup Shadow Container** (`scripts/setup-shadow.sh`):

```bash
#!/bin/bash
# Start container with Gitea and configure git URL rewriting

CONTAINER_NAME=$1
BUNDLE_PATH=$2
ORG=$3
REPO=$4

# Start container
docker run -d \
    --name "$CONTAINER_NAME" \
    -v "$BUNDLE_PATH:/snapshots/bundle.git:ro" \
    ghcr.io/microsoft/amplifier-shadow:latest

# Wait for Gitea
echo "Waiting for Gitea to start..."
until docker exec "$CONTAINER_NAME" curl -sf http://localhost:3000/api/v1/version > /dev/null; do
    sleep 1
done

# Create org and repo in Gitea
docker exec "$CONTAINER_NAME" bash -c "
    curl -s -u shadow:shadow \
        -H 'Content-Type: application/json' \
        -d '{\"username\":\"$ORG\"}' \
        http://localhost:3000/api/v1/orgs

    curl -s -u shadow:shadow \
        -H 'Content-Type: application/json' \
        -d '{\"name\":\"$REPO\",\"private\":false}' \
        http://localhost:3000/api/v1/orgs/$ORG/repos
"

# Push bundle to Gitea
docker exec "$CONTAINER_NAME" bash -c "
    cd /tmp &&
    git init --bare repo.git &&
    cd repo.git &&
    git fetch /snapshots/bundle.git refs/heads/*:refs/heads/* &&
    git remote add origin http://shadow:shadow@localhost:3000/$ORG/$REPO.git &&
    git push origin --all --force
"

# Configure git URL rewriting
docker exec "$CONTAINER_NAME" bash -c "
    git config --global url.'http://shadow:shadow@localhost:3000/$ORG/$REPO.git'.insteadOf 'https://github.com/$ORG/$REPO.git'
"

echo "Shadow container ready: $CONTAINER_NAME"
echo "Local source: $ORG/$REPO"
```

**Usage**:

```bash
# Create bundle from your repo
./scripts/create-bundle.sh ~/repos/my-lib /tmp/my-lib.bundle

# Setup shadow container
./scripts/setup-shadow.sh shadow-test /tmp/my-lib.bundle myorg my-lib

# Test
docker exec shadow-test bash -c "
    git clone https://github.com/myorg/my-lib /tmp/test &&
    cd /tmp/test &&
    git log -1 --oneline
"
```

### Docker Compose Examples

**Example 1: Single Repository** (`docker-compose/single-repo.yml`):

```yaml
version: "3.8"

services:
  shadow:
    image: ghcr.io/microsoft/amplifier-shadow:latest
    container_name: shadow-single
    volumes:
      - ./snapshots:/snapshots:ro
      - ./workspace:/workspace
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    command: >
      bash -c "
        /usr/local/bin/gitea-init.sh &&
        tail -f /dev/null
      "
```

**Example 2: Multi-Repository Testing** (`docker-compose/multi-repo.yml`):

```yaml
version: "3.8"

services:
  shadow-multi:
    image: ghcr.io/microsoft/amplifier-shadow:latest
    container_name: shadow-multi
    volumes:
      # Mount multiple bundles
      - ./snapshots/core-lib.bundle:/snapshots/org/core-lib.bundle:ro
      - ./snapshots/cli-tool.bundle:/snapshots/org/cli-tool.bundle:ro
      - ./workspace:/workspace
    environment:
      # Pass API keys from host
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      # UV cache isolation
      - UV_CACHE_DIR=/tmp/uv-cache
    command: >
      bash -c "
        /usr/local/bin/gitea-init.sh &&
        /usr/local/bin/setup-repos.sh org/core-lib org/cli-tool &&
        tail -f /dev/null
      "
```

**Usage**:

```bash
# Create bundles for your repos
git -C ~/repos/core-lib bundle create snapshots/core-lib.bundle --all
git -C ~/repos/cli-tool bundle create snapshots/cli-tool.bundle --all

# Start shadow
docker-compose -f docker-compose/multi-repo.yml up -d

# Run tests
docker-compose exec shadow-multi bash -c "
    cd /workspace &&
    git clone https://github.com/org/cli-tool &&
    cd cli-tool &&
    uv pip install -e .
    pytest
"

# Cleanup
docker-compose down
```

**Example 3: CI Integration** (`docker-compose/ci-shadow.yml`):

```yaml
version: "3.8"

services:
  ci-shadow:
    image: ghcr.io/microsoft/amplifier-shadow:latest
    container_name: ci-shadow
    volumes:
      - ./snapshots:/snapshots:ro
      - ./test-results:/test-results
    environment:
      - CI=true
      - GITHUB_ACTIONS=true
    command: >
      bash -c "
        /usr/local/bin/gitea-init.sh &&
        /usr/local/bin/run-ci-tests.sh > /test-results/output.log 2>&1
      "
```

**GitHub Actions Integration**:

```yaml
# .github/workflows/shadow-test.yml
name: Shadow Test

on: [push, pull_request]

jobs:
  shadow-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Create git bundle
        run: git bundle create snapshot.bundle --all

      - name: Run shadow tests
        run: |
          docker run --rm \
            -v $PWD/snapshot.bundle:/snapshots/bundle.git:ro \
            ghcr.io/microsoft/amplifier-shadow:latest \
            /usr/local/bin/test-in-shadow.sh org/repo
```

### Integration with Outside-In Testing

Combine shadow environments with agentic outside-in tests:

```bash
# Create shadow with local changes
amplifier-shadow create --local ~/repos/lib:org/lib --name test

# Run outside-in test scenarios inside shadow
amplifier-shadow exec test "gadugi-agentic-test run test-scenario.yaml"

# Extract evidence
amplifier-shadow extract test /evidence ./test-evidence
```

See the `outside-in-testing` skill for complete integration examples.

## Best Practices [LEVEL 2]

### 1. Always Verify Your Sources Are Used

Don't assume - verify that the shadow is actually using your local code:

```bash
# Check snapshot commits
amplifier-shadow status shadow-xxx | grep snapshot_commit

# Verify install resolves to that commit
amplifier-shadow exec shadow-xxx "pip install git+https://github.com/org/lib" | grep "org/lib @"
```

### 2. Use Pre-Cloned Workspace

Local sources are automatically at `/workspace/{org}/{repo}`:

```bash
# ✅ FAST: Use pre-cloned repo
amplifier-shadow exec xxx "pip install -e /workspace/org/lib"

# ❌ SLOWER: Clone again
amplifier-shadow exec xxx "git clone https://github.com/org/lib && pip install -e lib"
```

### 3. Isolate Package Manager Caches

Shadow environments automatically isolate caches to prevent stale packages:

- Python UV: `/tmp/uv-cache`
- Python pip: `/tmp/pip-cache`
- Node npm: `/tmp/npm-cache`
- Rust cargo: `/tmp/cargo-home`
- Go modules: `/tmp/go-mod-cache`

These are set automatically - no action needed.

### 4. Pass Required Environment Variables

```bash
# Amplifier (automatic for common API keys)
shadow.create(local_sources=["~/repos/lib:org/lib"])

# CLI (explicit)
amplifier-shadow create \
    --local ~/repos/lib:org/lib \
    --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    --env CUSTOM_VAR=value
```

### 5. Clean Up After Testing

```bash
# Always destroy shadows when done
amplifier-shadow destroy shadow-xxx

# Or destroy all
amplifier-shadow destroy-all
```

### 6. Use Named Shadows for Clarity

```bash
# ✅ GOOD: Descriptive name
amplifier-shadow create --local ~/repos/lib:org/lib --name test-breaking-change

# ❌ BAD: Auto-generated
amplifier-shadow create --local ~/repos/lib:org/lib
# Creates shadow-a3f2b8c1 (hard to remember)
```

## Integration Patterns [LEVEL 3]

### Pattern: Shadow + Outside-In Tests

Combine shadow isolation with declarative test scenarios:

```yaml
# test-scenario.yaml
scenario:
  name: "Library Integration Test"
  type: cli

  steps:
    - action: launch
      target: "/workspace/org/lib/cli.py"

    - action: verify_output
      contains: "Success"
```

Run in shadow:

```bash
amplifier-shadow create --local ~/repos/lib:org/lib --name test
amplifier-shadow exec test "gadugi-agentic-test run test-scenario.yaml"
```

### Pattern: Shadow + pytest

```bash
amplifier-shadow create --local ~/repos/lib:org/lib --name pytest-run

amplifier-shadow exec pytest-run "
  cd /workspace/org/lib &&
  uv venv && . .venv/bin/activate &&
  pip install -e '.[dev]' &&
  pytest --cov=src --cov-report=html
"

# Extract coverage report
amplifier-shadow extract pytest-run /workspace/org/lib/htmlcov ./coverage-report
```

### Pattern: Shadow + npm test

```bash
amplifier-shadow create --local ~/repos/pkg:org/pkg --name npm-test

amplifier-shadow exec npm-test "
  cd /workspace/org/pkg &&
  npm install &&
  npm test
"
```

### Pattern: Shadow + cargo test

```bash
amplifier-shadow create --local ~/repos/crate:org/crate --name cargo-test

amplifier-shadow exec cargo-test "
  cd /workspace/org/crate &&
  cargo build &&
  cargo test
"
```

## Philosophy Alignment [LEVEL 2]

This skill follows amplihack's core principles:

### Ruthless Simplicity

- **Minimal abstraction**: Shadow = container + gitea + URL rewriting
- **No frameworks**: Pure Docker, git, and shell scripts
- **Essential only**: Only captures what's needed (git bundle, not entire filesystems)

### Modular Design (Bricks & Studs)

- **Self-contained**: Each shadow is independent
- **Clear contract**: Git URLs in → local sources out
- **Composable**: Combine with other testing tools

### Zero-BS Implementation

- **No stubs**: Every script works completely
- **Working defaults**: Reasonable defaults for all operations
- **Clear errors**: Actionable error messages with troubleshooting

### Outside-In Thinking

- **User perspective**: Test what users will see
- **Implementation agnostic**: Don't care how code works internally
- **Behavior-driven**: Focus on outcomes

## CLI Reference [LEVEL 3]

### Commands

```bash
# Create shadow environment
amplifier-shadow create [OPTIONS]
  --local, -l TEXT    Local source mapping: /path/to/repo:org/name (repeatable)
  --name, -n TEXT     Name for environment (auto-generated if not provided)
  --image, -i TEXT    Container image (default: amplifier-shadow:local)
  --env, -e TEXT      Environment variable: KEY=VALUE or KEY to inherit (repeatable)
  --env-file FILE     File with environment variables (one per line)
  --pass-api-keys     Auto-pass common API key env vars (default: enabled)

# Execute command in shadow
amplifier-shadow exec SHADOW_ID COMMAND
  --timeout INTEGER   Timeout in seconds (default: 300)

# Show changed files
amplifier-shadow diff SHADOW_ID [PATH]

# Extract file from shadow
amplifier-shadow extract SHADOW_ID CONTAINER_PATH HOST_PATH

# Inject file into shadow
amplifier-shadow inject SHADOW_ID HOST_PATH CONTAINER_PATH

# List all shadows
amplifier-shadow list

# Show shadow status
amplifier-shadow status SHADOW_ID

# Destroy shadow
amplifier-shadow destroy SHADOW_ID
  --force             Force destruction even on errors

# Destroy all shadows
amplifier-shadow destroy-all
  --force             Force destruction even on errors

# Build shadow image locally
amplifier-shadow build

# Open interactive shell
amplifier-shadow shell SHADOW_ID
```

## Quick Reference Card [LEVEL 1]

```bash
# Typical workflow
amplifier-shadow create --local ~/repos/lib:org/lib --name test
amplifier-shadow exec test "pytest"
amplifier-shadow destroy test

# Multi-repo
amplifier-shadow create \
  --local ~/repos/lib1:org/lib1 \
  --local ~/repos/lib2:org/lib2 \
  --name multi

# With environment variables
amplifier-shadow create \
  --local ~/repos/lib:org/lib \
  --env API_KEY=$API_KEY \
  --name test

# Interactive shell
amplifier-shadow shell test

# Extract results
amplifier-shadow extract test /workspace/results ./local-results
```

## Related Skills [LEVEL 1]

- **outside-in-testing**: Run agentic tests in shadow environments
- **test-gap-analyzer**: Find untested code paths (complement shadow testing)
- **philosophy-guardian**: Verify shadow scripts follow ruthless simplicity

## Troubleshooting Checklist [LEVEL 2]

When shadow tests fail:

- [ ] Verify local sources are being used (check snapshot commits)
- [ ] Check pre-cloned repos exist at `/workspace/{org}/{repo}`
- [ ] Verify environment variables are passed (run `env` inside shadow)
- [ ] Clear package manager caches if stale
- [ ] Check git URL rewriting is configured (`git config --list`)
- [ ] Verify Gitea is accessible (`curl http://localhost:3000/api/v1/version`)
- [ ] Use virtual environments (avoid PEP 668 errors)
- [ ] Check container is running (`amplifier-shadow status`)

## Changelog [LEVEL 3]

### Version 1.0.0 (2026-01-29)

- Initial skill release
- Support for Amplifier, Claude Code, GitHub Copilot, manual DIY
- Shell scripts for standalone usage
- Docker Compose examples for CI integration
- Complete CLI reference and troubleshooting guide
- Integration patterns with outside-in-testing
- Philosophy alignment with ruthless simplicity

---

**Remember**: Shadow environments let you test **exactly** what's on your machine (uncommitted changes and all) in a **clean, isolated environment** that mirrors CI. Use them before every significant push to catch issues early.
