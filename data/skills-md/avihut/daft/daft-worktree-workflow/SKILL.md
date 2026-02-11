---
name: daft-worktree-workflow
description: Guides the daft worktree workflow for compartmentalized Git development. Use when working in daft-managed repositories (repos with a .git/ bare directory and branch worktrees as sibling directories), when setting up worktree environment isolation, or when users ask about worktree-based workflows. Covers daft commands, hooks automation via daft.yml, and environment tooling like mise, direnv, nvm, and pyenv.
---

# daft Worktree Workflow

## Core Philosophy

daft treats each Git worktree as a **compartmentalized workspace**, not just a branch checked out to disk. Each worktree is a fully isolated environment with its own:

- Working files and Git index
- Build artifacts (`node_modules/`, `target/`, `venv/`, `.build/`)
- IDE state and configuration (`.vscode/`, `.idea/`)
- Environment files (`.envrc`, `.env`)
- Running processes (dev servers, watchers, test runners)
- Installed dependencies (potentially different versions per branch)

This means creating a new worktree is not just "checking out a branch" -- it is spinning up a new development environment. Automation (via `daft.yml` hooks) should install dependencies, configure environment tools, and prepare the workspace so the developer can start working immediately.

Never use `git checkout` or `git switch` to change branches in a daft-managed repo. Navigate between worktree directories instead.

## Detecting a daft-managed Repository

A daft-managed repository has this layout:

```
my-project/
+-- .git/                    # Bare repository (shared Git metadata)
+-- main/                    # Worktree for the default branch
|   +-- src/
|   +-- package.json
+-- feature/auth/            # Worktree for a feature branch
|   +-- src/
|   +-- package.json
+-- bugfix/login/            # Worktree for a bugfix branch
```

Key indicators:
- `.git/` at the project root is a **bare repository** (directory, not a file)
- Branch worktrees are **sibling directories** to `.git/`
- Use `git rev-parse --git-common-dir` from any worktree to find the project root

If you see this layout, the user is using daft. Apply worktree-aware guidance throughout the session.

## Invocation Forms

daft commands can be invoked in three ways:

| Form | Example | Requires |
|------|---------|----------|
| Git subcommand | `git worktree-checkout feature/auth` | `git-worktree-checkout` symlink on PATH |
| Direct binary | `daft worktree-checkout feature/auth` | Only the `daft` binary |
| Shortcut alias | `gwtco feature/auth` | Shortcut symlink on PATH |

The git subcommand form (`git worktree-*`) is what users type in their terminals and what documentation references. Shortcuts are optional short aliases managed via `daft setup shortcuts`.

**Agent execution rule**: When running daft commands, always use the direct binary form (`daft <subcommand>`). The git subcommand form requires symlinks and shell wrappers that are not available in most agent shell sandboxes. When explaining daft usage to users, reference the git subcommand form (`git worktree-*`) or shortcuts, as these are what users interact with in their configured terminals.

After creating a worktree with `daft`, the shell does not automatically `cd` into it (that requires shell wrappers). Navigate to the new worktree using the layout convention: `cd ../<branch-name>/` relative to any existing worktree.

## Command Reference

All commands below use the `daft` binary form for agent execution. Users know these as `git` subcommands (e.g., `daft worktree-checkout` is `git worktree-checkout` to the user).

### Worktree Lifecycle

| Command | Description |
|---------|-------------|
| `daft worktree-clone <url>` | Clone a remote repository into daft's worktree layout |
| `daft worktree-init <name>` | Initialize a new local repository in worktree layout |
| `daft worktree-checkout <branch>` | Create a worktree for an existing local or remote branch |
| `daft worktree-checkout-branch <new-branch> [base]` | Create a new branch and worktree from current or specified base |
| `daft worktree-checkout-branch-from-default <new-branch>` | Create a new branch and worktree from the remote's default branch |
| `daft worktree-prune` | Remove worktrees whose remote branches have been deleted |
| `daft worktree-carry <targets>` | Transfer uncommitted changes to one or more other worktrees |
| `daft worktree-fetch [targets]` | Pull remote updates into worktree branches |

### Adoption and Ejection

| Command | Description |
|---------|-------------|
| `daft worktree-flow-adopt [path]` | Convert a traditional repository to daft's worktree layout |
| `daft worktree-flow-eject` | Convert back to a traditional repository layout |

### Management

| Command | Description |
|---------|-------------|
| `daft hooks <subcommand>` | Manage hooks trust and configuration (`trust`, `deny`, `prompt`, `status`, `list`, `reset-trust`, `migrate`, `install`, `validate`, `dump`) |
| `daft doctor` | Diagnose installation and configuration issues |
| `daft setup shortcuts <subcommand>` | Manage command shortcut symlinks |
| `daft shell-init <shell>` | Generate shell integration wrappers |
| `daft completions <shell>` | Generate shell tab completions |

All worktree commands can be run from **any directory** within any worktree. They find the project root automatically via `git rev-parse --git-common-dir`.

## Shell Integration

Shell integration is important because the daft binary creates worktrees internally, but the parent shell stays in the original directory. Shell wrappers solve this by detecting a `__DAFT_CD__:/path` marker and running `cd` in the parent shell.

```bash
# Bash / Zsh -- add to ~/.bashrc or ~/.zshrc
eval "$(daft shell-init bash)"

# Fish -- add to ~/.config/fish/config.fish
daft shell-init fish | source

# With short aliases (gwco, gwcob, gwcobd)
eval "$(daft shell-init bash --aliases)"
```

Disable auto-cd per-command with `--no-cd` or globally with `git config daft.autocd false`.

## Hooks System (daft.yml)

Hooks automate worktree lifecycle events. The recommended approach is a `daft.yml` file at the repository root.

### Hook Types

| Hook | Trigger | Runs From |
|------|---------|-----------|
| `post-clone` | After `daft worktree-clone` | New default branch worktree |
| `post-init` | After `daft worktree-init` | New initial worktree |
| `worktree-pre-create` | Before new worktree is added | Source worktree |
| `worktree-post-create` | After new worktree is created | New worktree |
| `worktree-pre-remove` | Before worktree is removed | Worktree being removed |
| `worktree-post-remove` | After worktree is removed | Current worktree |

### daft.yml Format

```yaml
min_version: "1.5.0"          # Optional: minimum daft version
hooks:
  worktree-post-create:
    parallel: true             # Run jobs concurrently (default)
    jobs:
      - name: install-deps
        run: npm install
      - name: setup-env
        run: cp .env.example .env
```

### Config File Locations (first match wins)

`daft.yml`, `daft.yaml`, `.daft.yml`, `.daft.yaml`, `.config/daft.yml`, `.config/daft.yaml`

Additionally: `daft-local.yml` for machine-specific overrides (not committed), and per-hook files like `worktree-post-create.yml`.

### Execution Modes

Set one per hook (default is `parallel`):

| Mode | Field | Behavior |
|------|-------|----------|
| Parallel | `parallel: true` | All jobs run concurrently |
| Piped | `piped: true` | Sequential; stop on first failure |
| Follow | `follow: true` | Sequential; continue on failure |

### Job Fields

```yaml
- name: job-name               # Display name and dependency reference
  run: "npm install"           # Inline command (or use script: "setup.sh")
  runner: "bash"               # Interpreter for script files
  root: "frontend"             # Working directory relative to worktree
  env:                         # Extra environment variables
    NODE_ENV: development
  tags: ["build"]              # Tags for filtering
  skip: CI                     # Skip when $CI is set
  only: DEPLOY_ENABLED         # Only run when $DEPLOY_ENABLED is set
  needs: [install-npm]         # Wait for these jobs to complete first
  interactive: true            # Needs TTY (forces sequential)
  priority: 1                  # Lower runs first
  fail_text: "Setup failed"   # Custom failure message
```

### Job Dependencies

```yaml
hooks:
  worktree-post-create:
    jobs:
      - name: install-npm
        run: npm install
      - name: install-pip
        run: pip install -r requirements.txt
      - name: build
        run: npm run build
        needs: [install-npm]
      - name: test
        run: npm test
        needs: [build, install-pip]
```

Independent jobs (`install-npm`, `install-pip`) run in parallel. Dependent jobs wait for their dependencies.

### Groups

A job can contain a nested group with its own execution mode:

```yaml
- name: checks
  group:
    parallel: true
    jobs:
      - name: lint
        run: cargo clippy
      - name: format
        run: cargo fmt --check
```

### Template Variables

Available in `run` commands:

| Variable | Description |
|----------|-------------|
| `{branch}` | Target branch name |
| `{worktree_path}` | Path to the target worktree |
| `{worktree_root}` | Project root directory |
| `{source_worktree}` | Path to the source worktree |
| `{git_dir}` | Path to the `.git` directory |
| `{remote}` | Remote name (usually `origin`) |
| `{job_name}` | Name of the current job |
| `{base_branch}` | Base branch (for checkout-branch commands) |
| `{repository_url}` | Repository URL (for post-clone) |
| `{default_branch}` | Default branch name (for post-clone) |

### Skip and Only Conditions

```yaml
skip: CI                         # Skip when env var is truthy
skip: true                       # Always skip
skip:
  - merge                        # Skip during merge
  - rebase                       # Skip during rebase
  - ref: "release/*"             # Skip if branch matches glob
  - env: SKIP_HOOKS              # Skip if env var is truthy
  - run: "test -f .skip-hooks"   # Skip if command exits 0

only:
  - env: DEPLOY_ENABLED          # Only run when env var is set
  - ref: "main"                  # Only run on main branch
```

### Trust Management

Hooks from untrusted repos do not run automatically. Manage trust with:

```bash
daft hooks trust        # Allow hooks to run
daft hooks prompt       # Prompt before each execution
daft hooks deny         # Never run hooks (default)
daft hooks status       # Check current trust level
daft hooks install      # Scaffold a daft.yml with placeholders
daft hooks validate     # Validate configuration syntax
daft hooks dump         # Show fully merged configuration
```

### Environment Variables in Hooks

All hooks receive: `DAFT_HOOK`, `DAFT_COMMAND`, `DAFT_PROJECT_ROOT`, `DAFT_GIT_DIR`, `DAFT_REMOTE`, `DAFT_SOURCE_WORKTREE`.

Worktree hooks add: `DAFT_WORKTREE_PATH`, `DAFT_BRANCH_NAME`.

Creation hooks add: `DAFT_IS_NEW_BRANCH`, `DAFT_BASE_BRANCH`.

Clone hooks add: `DAFT_REPOSITORY_URL`, `DAFT_DEFAULT_BRANCH`.

Removal hooks add: `DAFT_REMOVAL_REASON` (`remote-deleted`, `manual`, or `ejecting`).

## Environment Tool Detection and Setup

When working in a daft repo, detect environment tools by their marker files and suggest `daft.yml` hooks to automate setup for new worktrees.

### Tool Detection Table

| Tool | Marker Files | Purpose |
|------|-------------|---------|
| mise | `.mise.toml`, `.tool-versions` | Polyglot runtime manager (Node, Python, Ruby, Go, etc.) |
| direnv | `.envrc` | Per-directory environment variables |
| nvm / fnm | `.nvmrc`, `.node-version` | Node.js version management |
| pyenv | `.python-version` | Python version management |
| rbenv | `.ruby-version` | Ruby version management |
| Docker | `Dockerfile`, `docker-compose.yml`, `compose.yml` | Containerized development |
| npm | `package.json`, `package-lock.json` | Node.js dependencies |
| yarn | `yarn.lock` | Node.js dependencies (Yarn) |
| pnpm | `pnpm-lock.yaml` | Node.js dependencies (pnpm) |
| pip | `requirements.txt`, `pyproject.toml`, `setup.py` | Python dependencies |
| Cargo | `Cargo.toml`, `Cargo.lock` | Rust dependencies |
| Go modules | `go.mod`, `go.sum` | Go dependencies |
| Bundler | `Gemfile`, `Gemfile.lock` | Ruby dependencies |
| Composer | `composer.json`, `composer.lock` | PHP dependencies |

### Hook Jobs for Detected Tools

**mise** (if `.mise.toml` or `.tool-versions` exists):
```yaml
- name: mise-install
  run: mise install
```

**direnv** (if `.envrc` exists):
```yaml
- name: direnv-allow
  run: direnv allow .
```

**nvm** (if `.nvmrc` or `.node-version` exists):
```yaml
- name: nvm-use
  run: |
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
    nvm install
```

**npm** (if `package.json` exists):
```yaml
- name: npm-install
  run: npm install
```

**pip with venv** (if `requirements.txt` exists):
```yaml
- name: pip-install
  run: |
    python -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
```

**Cargo** (if `Cargo.toml` exists):
```yaml
- name: cargo-build
  run: cargo build
```

### Comprehensive Example

For a project using mise, direnv, and npm:

```yaml
hooks:
  post-clone:
    piped: true
    jobs:
      - name: mise-install
        run: mise install
      - name: direnv-allow
        run: direnv allow .
      - name: npm-install
        run: npm install
        needs: [mise-install]
      - name: setup-env
        run: cp .env.example .env

  worktree-post-create:
    jobs:
      - name: mise-install
        run: mise install
      - name: direnv-allow
        run: direnv allow .
      - name: npm-install
        run: npm install
        needs: [mise-install]
```

## Suggesting Tooling for Repos That Lack It

When a daft-managed repo has no `daft.yml`, check for dependency files and suggest creating one. A `worktree-post-create` hook that installs dependencies is the most impactful automation to add.

### Starter Configurations

**Node.js project** (detected via `package.json`):
```yaml
hooks:
  worktree-post-create:
    jobs:
      - name: install-deps
        run: npm install
```

**Python project** (detected via `requirements.txt` or `pyproject.toml`):
```yaml
hooks:
  worktree-post-create:
    jobs:
      - name: install-deps
        run: |
          python -m venv .venv
          . .venv/bin/activate
          pip install -r requirements.txt
```

**Rust project** (detected via `Cargo.toml`):
```yaml
hooks:
  worktree-post-create:
    jobs:
      - name: build
        run: cargo build
```

**Go project** (detected via `go.mod`):
```yaml
hooks:
  worktree-post-create:
    jobs:
      - name: download-deps
        run: go mod download
```

When suggesting `daft.yml`, also remind the user to trust the repo: `daft hooks trust`.

## Workflow Guidance for Agents

When working in a daft-managed repository, apply these translations:

| User intent | Correct daft approach |
|-------------|----------------------|
| "Create a branch" | `daft worktree-checkout-branch <name>` -- creates branch + worktree + pushes |
| "Branch from main" | `daft worktree-checkout-branch-from-default <name>` -- branches from remote default |
| "Switch to branch X" | Navigate to the worktree directory: `cd ../X/` |
| "Check out a PR" | `daft worktree-checkout <branch>` -- creates worktree for existing branch |
| "Clean up branches" | `daft worktree-prune` -- removes worktrees for deleted remote branches |
| "Wrong branch" | `daft worktree-carry <correct-branch>` -- moves uncommitted changes |
| "Update from remote" | `daft worktree-fetch` -- pulls updates into current or specified worktrees |
| "Adopt existing repo" | `daft worktree-flow-adopt` -- converts traditional repo to daft layout |

### Per-worktree Isolation

Each worktree has its **own** `node_modules/`, `.venv/`, `target/`, etc. When a new worktree is created without `daft.yml` hooks, dependencies are not installed automatically. If the user creates a new worktree and encounters missing-dependency errors, the fix is to run the appropriate install command in that worktree (e.g., `npm install`, `pip install -r requirements.txt`).

### Navigating Worktrees

From any worktree, sibling worktrees are at `../<branch-name>/`. The project root (containing `.git/`) is at `..` relative to any top-level worktree. Use `git rev-parse --git-common-dir` to programmatically find the root.

### Modifying Shared Files

Files like `daft.yml`, `.gitignore`, and CI configuration live in each worktree independently (they are part of the Git-tracked content). Changes to these files in one worktree must be committed and merged to propagate to other worktrees.

## Shortcuts

daft supports three shortcut styles as symlink aliases for faster terminal use:

| Style | Shortcuts | Example |
|-------|-----------|---------|
| Git (default) | `gwtclone`, `gwtinit`, `gwtco`, `gwtcb`, `gwtcbm`, `gwtprune`, `gwtcarry`, `gwtfetch` | `gwtco feature/auth` |
| Shell | `gwco`, `gwcob`, `gwcobd` | `gwco feature/auth` |
| Legacy | `gclone`, `gcw`, `gcbw`, `gcbdw`, `gprune` | `gcw feature/auth` |

Manage with `daft setup shortcuts list`, `enable <style>`, `disable <style>`, `only <style>`.

When a user asks how to use daft more efficiently, mention shortcuts as a convenience option. Agents should never execute shortcuts directly -- always use the `daft` binary form (see [Invocation Forms](#invocation-forms)).

## Configuration Reference

Key `git config` settings:

| Key | Default | Description |
|-----|---------|-------------|
| `daft.autocd` | `true` | CD into new worktrees via shell wrappers |
| `daft.remote` | `"origin"` | Default remote name |
| `daft.checkout.push` | `true` | Push new branches to remote |
| `daft.checkout.upstream` | `true` | Set upstream tracking |
| `daft.checkout.carry` | `false` | Carry uncommitted changes on checkout |
| `daft.checkoutBranch.carry` | `true` | Carry uncommitted changes on branch creation |
| `daft.fetch.args` | `"--ff-only"` | Default pull arguments for fetch |
| `daft.prune.cdTarget` | `"root"` | Where to cd after pruning (`root` or `default-branch`) |
| `daft.hooks.enabled` | `true` | Master switch for hooks |
| `daft.hooks.defaultTrust` | `"deny"` | Default trust for unknown repos |
| `daft.hooks.timeout` | `300` | Hook timeout in seconds |
