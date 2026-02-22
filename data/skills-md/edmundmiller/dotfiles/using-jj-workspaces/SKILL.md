---
name: using-jj-workspaces
description: Set up isolated jj workspaces for parallel development. Use when creating new workspaces, organizing workspace directories, or setting up gitignore for workspaces.
---

# Using JJ Workspaces

You're helping set up an isolated jj workspace for parallel development work without disrupting the current workspace.

## Core Workflow: Systematic Directory Selection + Safety Verification

### 1. Directory Selection (Priority Order)

Check for workspace directory preferences in this order:

1. **First**: Check if `.workspaces/` or `workspaces/` directory exists in project root
2. **Second**: Review CLAUDE.md or similar project documentation for workspace preferences
3. **Third**: If neither exists, ask the user:
   - Option A: Create project-local directory (`.workspaces/` or `workspaces/`)
   - Option B: Use global location (e.g., `~/workspaces/`)

**Never assume** - always follow this priority system.

### 2. Safety Verification (CRITICAL for project-local directories)

If using a project-local directory (`.workspaces/`, `workspaces/`, etc.):

1. **Check `.gitignore`** (or `.jjignore` if it exists) for the workspace directory pattern
2. **If NOT in .gitignore**:
   - Immediately add it: `echo "workspaces/" >> .gitignore` (or `.workspaces/`)
   - Commit the change: `jj describe -m "gitignore: Add workspaces directory"`
   - This prevents accidentally tracking workspace contents

**Never skip this verification** - it's a critical safety check.

### 3. Workspace Creation

```bash
# Detect project name from git/jj repository
PROJECT_NAME=$(basename $(jj workspace root))

# Construct workspace path
WORKSPACE_PATH="<selected-directory>/${PROJECT_NAME}-<branch-or-feature-name>"

# Create the workspace
jj workspace add "$WORKSPACE_PATH"

# JJ will automatically:
# - Create the directory
# - Set up a new workspace tracking the current repository
# - Create a new working-copy commit
```

### 4. Project Setup (Auto-detect and run)

After workspace creation, detect project type and run appropriate setup:

**Detection patterns:**

- `package.json` → `npm install` or `yarn install` or `pnpm install`
- `Cargo.toml` → `cargo build`
- `pyproject.toml` → `poetry install` or `pip install -e .`
- `flake.nix` → `nix develop` or `hey shell`
- `Gemfile` → `bundle install`
- `go.mod` → `go mod download`

**Always:**

1. Change to workspace directory: `cd "$WORKSPACE_PATH"`
2. Run the appropriate setup command
3. Report any setup errors to the user

### 5. Baseline Verification

Before reporting success, run project tests to ensure clean state:

```bash
# Attempt to run tests based on project type
# Examples:
npm test
cargo test
pytest
nix flake check
# etc.
```

**If baseline tests fail:**

- Report the failure to the user
- **Do NOT proceed** with implementation unless user explicitly approves
- The workspace may have inherited an unstable state

### 6. Report Status

Provide a clear summary:

```
✓ JJ workspace created at: <path>
✓ Project setup completed: <command run>
✓ Baseline tests: <passed/failed>
✓ Ready to work on: <feature/branch name>

To switch to this workspace:
  cd <workspace-path>

To return to main workspace:
  cd <original-path>

To list all workspaces:
  jj workspace list
```

## JJ Workspace Commands Reference

```bash
# Create new workspace
jj workspace add <path>

# List all workspaces
jj workspace list

# Remove a workspace (doesn't delete files)
jj workspace forget <workspace-name>

# Show workspace root
jj workspace root

# Update workspace to latest changes
jj workspace update-stale
```

## Critical Rules

1. **Never skip .gitignore verification** for project-local workspace directories
2. **Always follow the directory priority system** - don't assume location
3. **Require explicit permission** before proceeding if baseline tests fail
4. **Report clearly** when workspace is ready with all relevant paths and commands
5. **Auto-detect and run setup** - don't make the user do it manually

## JJ-Specific Considerations

Unlike git worktrees, jj workspaces:

- Share the same operation log (visible in `jj op log`)
- Each workspace has its own working-copy commit
- Changes in one workspace don't affect others until explicitly moved/rebased
- No need to specify a branch - jj creates a new working-copy commit automatically
- Use `@` to refer to the current workspace's working-copy commit

## Integration Notes

This skill is typically invoked during:

- Feature development requiring isolation from main work
- Testing changes without affecting current workspace
- Parallel development on multiple features
- Experimentation that might be abandoned

Pairs well with:

- JJ squash workflow for finishing work
- JJ split for organizing changes before moving back to main workspace
