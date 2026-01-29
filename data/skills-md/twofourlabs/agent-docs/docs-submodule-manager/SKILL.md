---
name: docs-submodule-manager
description: Manage documentation in the docs/ git submodule with proper structure and synchronization. Use when (1) user explicitly mentions "add docs", "specs", or documentation creation, (2) creating or reading files in docs/ directory, (3) working on features that need specification documents, implementation plans, or progress tracking, (4) documenting solutions, PRDs, or technical specs. Handles submodule initialization, proper directory structure (solutions/specs/feature), syncing from remote master, and committing changes.
---

# Docs Submodule Manager

Manage documentation stored in the `docs/` git submodule with proper structure, syncing, and version control.

## Overview

This skill automates the workflow for working with the `docs/` submodule:
- Ensures submodule is initialized
- Maintains structured documentation (solutions/specs/feature)
- Syncs with remote before changes
- Commits both in submodule and parent repo

## Workflow

### Step 1: Ensure Submodule is Initialized

Check if the `docs/` directory exists and is initialized:

```bash
# Check if docs directory is a git repository
if [ ! -d "docs/.git" ]; then
  # Try npm run setup if it exists
  if grep -q '"setup"' package.json 2>/dev/null; then
    npm run setup
  else
    # Fallback to git submodule commands
    git submodule update --init --recursive
  fi
fi
```

### Step 2: Determine Directory Structure

Navigate to `docs/<repo-name>/` where `<repo-name>` is the parent repository name.

**Get repo name:**
```bash
# Extract repo name from git remote URL
REPO_NAME=$(basename $(git rev-parse --show-toplevel))
```

**Choose appropriate directory based on content type:**

| Directory | Purpose | Examples |
|-----------|---------|----------|
| `solutions/<issue>/` | Bug fixes, workarounds, issue documentation | `android-build-failure/`, `navigation-crash/` |
| `specs/<feature>/` | Technical specs, implementation plans, progress tracking | `chat-refactor/`, `offline-sync/` |
| `feature/<feature-name>/` | PRDs, product requirements, user stories | `voice-messaging/`, `payment-integration/` |

For detailed guidance and examples, see [structure-guide.md](references/structure-guide.md).

**Standard files for specs/:**
- `implementation-plan.md` - Initial technical plan
- `progress.md` - Development tracking (use for features with 5+ todos)

If content doesn't fit these categories, create a descriptive directory (e.g., `research/`, `rfcs/`, `architecture/`).

### Step 3: Create/Modify Documentation

Create the necessary directory structure and files:

```bash
cd docs/$REPO_NAME

# Create directory if needed (example for specs)
mkdir -p specs/<feature-name>

# Create or edit the file
# Use Write or Edit tools to create/modify the documentation
```

### Step 4: Sync and Commit

**Inside the docs submodule:**

```bash
cd docs

# Sync from remote master first
git fetch origin
git pull origin master

# Stage and commit changes
git add .
git commit -m "doc: added spec for <feature-name>"
# OR
git commit -m "doc: update progress for <feature-name>"

# Push to remote
git push origin master
```

**In the parent repository:**

```bash
cd ..  # Return to parent repo root

# Commit the submodule update
git add docs
git commit -m "doc: update docs submodule for <feature-name>"
```

**Commit message format:**
- Adding new docs: `doc: added spec for <feature-name>`
- Updating docs: `doc: update progress for <feature-name>`
- Solutions: `doc: added solution for <issue-name>`
- Features/PRDs: `doc: added PRD for <feature-name>`

## Error Handling

**If submodule pull fails due to conflicts:**
- Alert user about the conflict
- Ask whether to stash local changes or manually resolve
- Do not force push or reset without explicit permission

**If docs directory structure doesn't exist:**
- Create `docs/<repo-name>/` if it doesn't exist
- Create the appropriate subdirectory (solutions/specs/feature)

**If unable to determine appropriate directory:**
- Ask user which category fits best
- Suggest creating a new category if none fit

## Resources

### references/structure-guide.md

Detailed documentation structure guide with:
- Complete directory layout
- When to use each category (solutions/specs/feature)
- Naming conventions
- Examples for each category
- Guidelines for creating dynamic directories
