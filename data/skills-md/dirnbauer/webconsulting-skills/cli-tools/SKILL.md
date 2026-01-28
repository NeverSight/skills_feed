---
name: cli-tools
description: CLI tool management and auto-installation. Use when commands fail with 'command not found', installing tools, or checking project environments.
version: 1.0.0
triggers:
  - cli
  - tools
  - installation
  - command not found
  - brew
  - apt
---

# CLI Tools Skill

Manage CLI tool installation, environment auditing, and updates.

## Capabilities

1. **Reactive**: Auto-install missing tools on "command not found"
2. **Proactive**: Audit project dependencies and tool versions
3. **Maintenance**: Batch update all managed tools

## Triggers

**Reactive** (auto-install):
```
bash: <tool>: command not found
zsh: command not found: <tool>
```

**Proactive** (audit): "check environment", "what's missing", "update tools"

## Binary to Tool Mapping

Common binary names that differ from package names:

| Binary | Package (Homebrew) | Package (apt) |
|--------|-------------------|---------------|
| `rg` | `ripgrep` | `ripgrep` |
| `fd` | `fd` | `fd-find` |
| `bat` | `bat` | `bat` |
| `delta` | `git-delta` | N/A |
| `exa` / `eza` | `eza` | `eza` |
| `fzf` | `fzf` | `fzf` |
| `ag` | `the_silver_searcher` | `silversearcher-ag` |
| `http` | `httpie` | `httpie` |
| `jq` | `jq` | `jq` |
| `yq` | `yq` | N/A |
| `gh` | `gh` | `gh` |
| `glab` | `glab` | N/A |

## Installation Commands

### macOS (Homebrew)

```bash
# Install single tool
brew install <package>

# Install multiple tools
brew install ripgrep fd bat eza fzf jq gh

# Update all tools
brew update && brew upgrade
```

### Linux (apt)

```bash
# Install single tool
sudo apt install <package>

# Install multiple tools
sudo apt install ripgrep fd-find bat fzf jq

# Update all tools
sudo apt update && sudo apt upgrade
```

### PHP Tools (Composer)

```bash
# Global PHP tools
composer global require phpstan/phpstan
composer global require friendsofphp/php-cs-fixer
composer global require rector/rector

# Project-specific
composer require --dev phpstan/phpstan
composer require --dev friendsofphp/php-cs-fixer
```

### Node.js Tools (npm)

```bash
# Global Node tools
npm install -g prettier eslint typescript

# Project-specific
npm install --save-dev prettier eslint typescript
```

## Project Type Detection

### PHP Project
Indicators: `composer.json`, `vendor/`, `*.php`

Required tools:
- `php` - PHP interpreter
- `composer` - Dependency manager
- `phpstan` - Static analysis
- `php-cs-fixer` - Code style

### TYPO3 Project
Indicators: `composer.json` with `typo3/cms-core`, `public/typo3/`

Required tools:
- All PHP tools
- `ddev` - Local development
- `typo3` - TYPO3 CLI

### Node.js Project
Indicators: `package.json`, `node_modules/`

Required tools:
- `node` - Node.js runtime
- `npm` / `pnpm` / `yarn` - Package manager

### Go Project
Indicators: `go.mod`, `*.go`

Required tools:
- `go` - Go compiler
- `golangci-lint` - Linter

## Environment Audit

Check if required tools are installed:

```bash
# Check single tool
command -v <tool> &> /dev/null && echo "Found" || echo "Missing"

# Check version
<tool> --version

# PHP project audit
php --version
composer --version
command -v phpstan &> /dev/null || echo "Missing: phpstan"
command -v php-cs-fixer &> /dev/null || echo "Missing: php-cs-fixer"

# TYPO3 project audit
php --version
composer --version
ddev --version
```

## Tool Catalog

### Core CLI Tools
- `curl` - HTTP client
- `wget` - File downloader
- `jq` - JSON processor
- `yq` - YAML processor
- `tree` - Directory visualizer
- `htop` - Process viewer
- `tmux` - Terminal multiplexer

### Development Tools
- `git` - Version control
- `gh` - GitHub CLI
- `glab` - GitLab CLI
- `docker` - Containerization
- `ddev` - Local development

### Search & Navigation
- `ripgrep` (`rg`) - Fast grep
- `fd` - Fast find
- `fzf` - Fuzzy finder
- `bat` - Cat with syntax highlighting
- `eza` - Modern ls replacement
- `delta` - Git diff viewer

### PHP Tools
- `php` - PHP interpreter
- `composer` - Dependency manager
- `phpstan` - Static analysis
- `rector` - Automated refactoring
- `php-cs-fixer` - Code style fixer
- `phpunit` - Testing framework
- `infection` - Mutation testing

### Node.js Tools
- `node` - JavaScript runtime
- `npm` / `pnpm` - Package managers
- `prettier` - Code formatter
- `eslint` - JavaScript linter
- `typescript` - TypeScript compiler

### Security Tools
- `trivy` - Vulnerability scanner
- `grype` - Container scanner
- `cosign` - Container signing

## Auto-Install Workflow

When a command fails with "command not found":

1. **Extract tool name** from error message
2. **Lookup package name** in binary-to-tool mapping
3. **Detect OS** (macOS/Linux)
4. **Install** using appropriate package manager
5. **Retry** original command

Example:

```bash
# Error: zsh: command not found: rg

# Resolution:
brew install ripgrep  # macOS
# or
sudo apt install ripgrep  # Linux

# Retry
rg "pattern" .
```

## Batch Update

Update all managed tools:

```bash
# macOS
brew update && brew upgrade

# Linux
sudo apt update && sudo apt upgrade

# PHP global tools
composer global update

# Node global tools
npm update -g
```

---

## Credits & Attribution

This skill is based on the excellent work by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/cli-tools-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
