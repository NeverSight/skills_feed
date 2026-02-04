---
name: direnv
description: Guide for using direnv - a shell extension for loading directory-specific environment variables. Use when setting up project environments, creating .envrc files, configuring per-project environment variables, integrating with Python/Node/Ruby/Go layouts, working with Nix flakes, or troubleshooting environment loading issues on macOS and Linux.
---

# direnv Skill

This skill provides comprehensive guidance for working with direnv, covering installation, configuration, stdlib functions, and best practices for per-project environment management.

## When to Use This Skill

Use this skill when:
- Installing and configuring direnv on macOS or Linux
- Creating or modifying `.envrc` files for projects
- Setting up per-project environment variables
- Configuring language-specific layouts (Python, Node.js, Ruby, Go, Perl)
- Integrating direnv with Nix or Nix Flakes
- Managing secrets and environment configuration for teams
- Troubleshooting environment loading issues
- Creating custom direnv extensions

## Core Concepts

### What is direnv?
direnv is a shell extension that loads and unloads environment variables based on the current directory. When you `cd` into a directory with a `.envrc` file, direnv automatically loads the environment. When you leave, it unloads the changes.

### Security Model
direnv uses an allowlist-based security approach:
- New or modified `.envrc` files must be explicitly allowed with `direnv allow`
- Prevents automatic execution of untrusted scripts
- Use `direnv deny` to revoke access

### How It Works
1. Shell hook intercepts directory changes
2. Checks for `.envrc` file in current or parent directories
3. If allowed, executes `.envrc` in a bash subshell
4. Captures exported variables and applies them to current shell

## Installation

### macOS (Homebrew - Recommended)

```bash
brew install direnv
```

### Linux

```bash
# Ubuntu/Debian
sudo apt install direnv

# Fedora
sudo dnf install direnv

# Arch
sudo pacman -S direnv

# Binary installer (any system)
curl -sfL https://direnv.net/install.sh | bash
```

### Verify Installation

```bash
direnv version
```

## Shell Configuration

Add the hook to your shell's config file. **This is required for direnv to function.**

### Zsh (~/.zshrc)

```bash
eval "$(direnv hook zsh)"
```

**With Oh My Zsh:**
```bash
plugins=(... direnv)
```

### Bash (~/.bashrc)

```bash
eval "$(direnv hook bash)"
```

**Important:** Place after rvm, git-prompt, and other prompt-modifying extensions.

### Fish (~/.config/fish/config.fish)

```fish
direnv hook fish | source
```

### After Configuration

Restart your shell:
```bash
exec $SHELL
```

## .envrc File Basics

### Creating an .envrc

```bash
# In your project directory
touch .envrc

# Edit with your preferred editor
vim .envrc
```

### Basic Syntax

```bash
# Export environment variables
export NODE_ENV=development
export API_URL=http://localhost:3000
export DATABASE_URL=postgres://localhost/myapp

# The export keyword is required for direnv to capture variables
```

### Allowing the .envrc

```bash
# Allow current directory
direnv allow

# Allow specific path
direnv allow /path/to/project

# Deny/revoke access
direnv deny
```

## Standard Library Functions

direnv includes a powerful stdlib. Always prefer stdlib functions over manual exports.

### PATH Management

```bash
# Prepend to PATH (safer than manual export)
PATH_add bin
PATH_add node_modules/.bin
PATH_add scripts

# Add to arbitrary path-like variable
path_add PYTHONPATH lib
path_add LD_LIBRARY_PATH /opt/lib

# Remove from PATH
PATH_rm "*/.git/bin"
```

### Environment File Loading

```bash
# Load .env file (current directory)
dotenv

# Load specific file
dotenv .env.local

# Load only if exists (no error)
dotenv_if_exists .env.local
dotenv_if_exists .env.${USER}

# Source another .envrc
source_env ../.envrc
source_env /path/to/.envrc

# Search upward and source parent .envrc
source_up

# Source if exists
source_env_if_exists .envrc.local
```

### Language Layouts

**Node.js:**
```bash
# Adds node_modules/.bin to PATH
layout node
```

**Python:**
```bash
# Creates virtualenv in .direnv/python-X.X/
layout python

# Use specific Python version
layout python python3.11

# Shortcut for Python 3
layout python3

# Use Pipenv (reads from Pipfile)
layout pipenv
```

**Ruby:**
```bash
# Sets GEM_HOME to project directory
layout ruby
```

**Go:**
```bash
# Modifies GOPATH and adds bin to PATH
layout go
```

**Perl:**
```bash
# Configures local::lib environment
layout perl
```

### Nix Integration

```bash
# Load nix-shell environment
use nix

# With specific file
use nix shell.nix

# Load from Nix flake
use flake

# Load specific flake
use flake "nixpkgs#hello"
use flake ".#devShell"
```

**For better Nix Flakes support, install nix-direnv:**
```bash
# Provides faster, cached use_flake implementation
# https://github.com/nix-community/nix-direnv
```

### Version Managers

```bash
# rbenv
use rbenv

# Node.js (with fuzzy version matching)
use node 18
use node 18.17.0

# Reads from .nvmrc if version not specified
use node

# Julia
use julia 1.9
```

### Validation

```bash
# Require environment variables (errors if missing)
env_vars_required API_KEY DATABASE_URL SECRET_KEY

# Enforce minimum direnv version
direnv_version 2.32.0

# Check git branch
if on_git_branch main; then
  export DEPLOY_ENV=production
fi
if on_git_branch develop; then
  export DEPLOY_ENV=staging
fi
```

### File Watching

```bash
# Reload when files change
watch_file package.json
watch_file requirements.txt
watch_file .tool-versions
watch_file config/*.yaml

# Watch entire directory
watch_dir config
watch_dir migrations
```

### Utility Functions

```bash
# Check if command exists
if has docker; then
  export DOCKER_HOST=unix:///var/run/docker.sock
fi

# Expand relative path to absolute
expand_path ./bin

# Find file searching upward
find_up package.json

# Enable strict mode (exit on errors)
strict_env

# Load prefix (configures CPATH, LD_LIBRARY_PATH, etc.)
load_prefix /usr/local/custom

# Load remote script with integrity verification
source_url https://example.com/script.sh "sha256-HASH..."
```

## Best Practices

### Recommended .envrc Template

```bash
#!/usr/bin/env bash
# .envrc - Project environment configuration

# Enforce direnv version for team consistency
direnv_version 2.32.0

# Load .env if exists
dotenv_if_exists

# Load local overrides (not committed to git)
source_env_if_exists .envrc.local

# Language-specific layout
layout node  # or: layout python3

# Add project bin directories
PATH_add bin
PATH_add scripts

# Development defaults
export NODE_ENV="${NODE_ENV:-development}"
export LOG_LEVEL="${LOG_LEVEL:-debug}"

# Watch for dependency changes
watch_file package.json
watch_file .nvmrc
```

### Git Configuration

**.gitignore:**
```gitignore
# Environment files with secrets
.env
.env.local
.envrc.local

# direnv virtualenv/cache
.direnv/
```

**Commit to repository:**
- `.envrc` (base configuration, no secrets)
- `.env.example` (template for team members)

### Secrets Management

**Never commit secrets.** Use environment variable fallbacks:

```bash
# .envrc (committed)
export DATABASE_URL="${DATABASE_URL:-postgres://localhost/dev}"
export API_KEY="${API_KEY:-}"

# Validate required secrets
env_vars_required API_KEY

# .envrc.local (gitignored)
export DATABASE_URL="postgres://user:secret@prod/app"
export API_KEY="actual-secret-key"
```

### Layered Configuration

```bash
# ~/projects/.envrc (global dev settings)
export EDITOR=vim

# ~/projects/api/.envrc
source_up
export API_PORT=3000

# ~/projects/api/feature/.envrc
source_up
export FEATURE_FLAG=true
```

### Project Structure

```
my-project/
├── .envrc           # Base environment (committed)
├── .envrc.local     # Local overrides (gitignored)
├── .env             # Environment variables (gitignored)
├── .env.example     # Template for team (committed)
└── .direnv/         # direnv cache (gitignored)
```

## Custom Extensions

Create `~/.config/direnv/direnvrc` for custom functions:

```bash
#!/usr/bin/env bash
# ~/.config/direnv/direnvrc

# Custom function: Use specific Kubernetes context
use_kubernetes() {
  local context="${1:-default}"
  export KUBECONFIG="${HOME}/.kube/config"
  kubectl config use-context "$context" >/dev/null 2>&1
  log_status "kubernetes context: $context"
}

# Custom function: Load from AWS Secrets Manager
use_aws_secrets() {
  local secret_name="$1"
  local region="${2:-us-east-1}"
  eval "$(aws secretsmanager get-secret-value \
    --secret-id "$secret_name" \
    --region "$region" \
    --query SecretString \
    --output text | jq -r 'to_entries | .[] | "export \(.key)=\"\(.value)\""')"
  log_status "loaded secrets from: $secret_name"
}

# Custom function: Use asdf versions from .tool-versions
use_asdf() {
  watch_file .tool-versions
  source_env "$(asdf direnv local)"
}
```

Usage in `.envrc`:
```bash
use kubernetes dev-cluster
use aws_secrets myapp/dev
use asdf
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `direnv allow` | Allow the current .envrc |
| `direnv deny` | Revoke .envrc access |
| `direnv reload` | Force reload environment |
| `direnv status` | Show current status |
| `direnv dump` | Dump current environment |
| `direnv edit` | Open .envrc in editor |
| `direnv version` | Show direnv version |

## Troubleshooting

### Environment Not Loading

```bash
# Check status
direnv status

# Force reload
direnv reload

# Re-allow .envrc
direnv allow

# Check if hook is installed
echo $DIRENV_DIR
```

### Shell Hook Issues

1. Verify hook is in shell config file
2. Ensure it's at the END of the file
3. Restart shell completely: `exec $SHELL`
4. Check for errors: `direnv hook zsh`

### Performance Issues

```bash
# Show what's being evaluated
direnv show_dump

# For Nix, use nix-direnv for caching
# https://github.com/nix-community/nix-direnv
```

### Debugging

```bash
# Verbose output
export DIRENV_LOG_FORMAT='%s'

# Show exported variables
direnv dump | jq

# Test .envrc syntax
bash -n .envrc
```

## IDE Integration

### VS Code
Install [direnv extension](https://marketplace.visualstudio.com/items?itemName=mkhl.direnv) for automatic environment loading in integrated terminal.

### JetBrains
Install [direnv integration plugin](https://plugins.jetbrains.com/plugin/15285-direnv-integration).

### Neovim
Use [direnv.vim](https://github.com/direnv/direnv.vim) or configure with lua.

## Common Patterns

### Development vs Production

```bash
# .envrc
export NODE_ENV="${NODE_ENV:-development}"

if [[ "$NODE_ENV" == "development" ]]; then
  export DEBUG=true
  export LOG_LEVEL=debug
else
  export DEBUG=false
  export LOG_LEVEL=info
fi
```

### Multi-Service Projects (Monorepo)

```bash
# root/.envrc
export PROJECT_ROOT="$(pwd)"
export COMPOSE_PROJECT_NAME=myapp

# services/api/.envrc
source_up
export SERVICE_NAME=api
export SERVICE_PORT=3000

# services/web/.envrc
source_up
export SERVICE_NAME=web
export SERVICE_PORT=8080
```

### Docker Integration

```bash
# .envrc
export COMPOSE_FILE=docker-compose.yml
export COMPOSE_PROJECT_NAME="${PWD##*/}"

if has docker-compose; then
  export DOCKER_HOST="${DOCKER_HOST:-unix:///var/run/docker.sock}"
fi

# Add Docker bin for containers that install CLI tools
PATH_add .docker/bin
```

## References

- [Official Documentation](https://direnv.net/)
- [Installation Guide](https://direnv.net/docs/installation.html)
- [Shell Hook Setup](https://direnv.net/docs/hook.html)
- [Standard Library Reference](https://direnv.net/man/direnv-stdlib.1.html)
- [nix-direnv](https://github.com/nix-community/nix-direnv)
- [Homebrew Formula](https://formulae.brew.sh/formula/direnv)
