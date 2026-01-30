---
name: chezmoi-config
description: Comprehensive chezmoi dotfile management skill for creating, modifying, and maintaining dotfile templates, configuration files, scripts, and external resources. Use when working with chezmoi for creating new dotfile templates (.tmpl files) with Go template syntax, managing .chezmoi.toml.tmpl configuration and .chezmoidata, configuring .chezmoiexternal files for external resources, writing run_once/run_onchange/run_before/run_after scripts, integrating password managers for secrets, managing cross-platform configurations, and handling conditional logic based on OS/architecture/hostname. This skill includes comprehensive reference documentation for all chezmoi features and can consult the latest chezmoi documentation via Context7.
---

# Chezmoi Configuration Management

Comprehensive guide for managing chezmoi dotfiles with templates, scripts, external resources, and advanced configurations.

## ⚠️ Safety Constraints

**This skill is READ-ONLY and validation-only. It MUST NOT modify your actual environment.**

### Forbidden Operations

NEVER execute these commands - they will modify your system:
- `chezmoi apply` - Applies changes to your home directory
- `chezmoi apply --force` - Forcefully applies changes
- `chezmoi update` - Updates source state and may change managed files
- Any operations that directly execute scripts (scripts run automatically during `chezmoi apply`)

### Allowed Safe Operations

ONLY use these read-only validation commands:
- `chezmoi diff` - Preview what would change (safe)
- `chezmoi apply --dry-run` - Simulate changes without applying (safe)
- `chezmoi doctor` - Check configuration validity (safe)
- `chezmoi data` - Display template data variables (safe)
- `chezmoi managed` - List files currently managed by chezmoi (read-only, safe)
- `chezmoi unmanaged` - List files currently unmanaged by chezmoi (read-only, safe)
- `chezmoi ignored` - List files ignored by chezmoi (read-only, safe)
- `chezmoi execute-template < file.tmpl` - Preview expanded template output (safe)
- `chezmoi state dump` - View script execution state (safe)
- `chezmoi verify` - Verify source state integrity (safe)
- `chezmoi cd` - Enter source directory (safe)
- `chezmoi source-path` - Show source directory path (safe)

### User Responsibility

This skill helps you **create and validate** chezmoi configurations. To apply changes, **you must manually run** `chezmoi apply` in your terminal after reviewing the output.

## Quick Start

### Creating a New Template

1. **Add existing file as template:**
   ```bash
   chezmoi add --template ~/.gitconfig
   ```

2. **Or create manually:**
   ```bash
   chezmoi cd
   $EDITOR dot_gitconfig.tmpl
   ```

3. **Use Go template syntax:**
   ```go
   [user]
       name = {{ .name }}
   {{- if eq .chezmoi.os "darwin" }}
   [credential]
       helper = osxkeychain
   {{- end }}
   ```

### Managing External Resources

Create `.chezmoiexternal.toml.tmpl`:

```toml
[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    exact = true
    stripComponents = 1
```

### Writing Scripts

Create `run_onchange_install-packages.sh.tmpl`:

```bash
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew install git vim ripgrep
{{ end -}}
```

## Reference Documentation

This skill includes comprehensive reference documentation. Consult these guides for detailed information:

- **[template-syntax.md](references/template-syntax.md)** - Go template syntax, variables, conditionals, loops, and examples
- **[external-files.md](references/external-files.md)** - .chezmoiexternal configuration for files, archives, and git repositories
- **[ignore-files.md](references/ignore-files.md)** - .chezmoiignore/.chezmoiignore.tmpl patterns, templates, and scope
- **[password-managers.md](references/password-managers.md)** - Integrating 20+ password managers (1Password, Bitwarden, Vault, etc.)
- **[scripts.md](references/scripts.md)** - run_once, run_onchange, run_before, run_after scripts
- **[advanced-configuration.md](references/advanced-configuration.md)** - .chezmoi.toml, prompting, encryption, and advanced features

## Common Tasks

### 1. Create Platform-Specific Configuration

**Template file (dot_gitconfig.tmpl):**
```go
[user]
    name = {{ .name }}
    email = {{ .email }}

{{- if eq .chezmoi.os "darwin" }}
[credential]
    helper = osxkeychain
{{- else if eq .chezmoi.os "linux" }}
[credential]
    helper = cache
{{- end }}
```

**Configuration (chezmoi.toml):**
```toml
[data]
    name = "John Doe"
    email = "john@example.com"
```

### 2. Manage Secrets with Password Managers

```go
{{- if (bitwarden "github") }}
[github]
    token = {{ (bitwarden "github").login.password }}
{{- end }}
```

### 3. Install Packages Conditionally

**run_onchange_install-packages.sh.tmpl:**
```bash
{{ if eq .chezmoi.os "darwin" -}}
#!/bin/bash
brew bundle --file=/dev/stdin <<EOF
{{ range .packages.darwin.brews -}}
brew "{{ . }}"
{{ end -}}
EOF
{{ else if eq .chezmoi.os "linux" -}}
#!/bin/bash
sudo apt install -y {{ range .packages.linux }}{{ . }} {{ end }}
{{ end -}}
```

**.chezmoidata/packages.yaml:**
```yaml
darwin:
  brews:
    - git
    - vim
    - ripgrep

linux:
  - git
  - vim
  - ripgrep
  - fd-find
```

### 4. Include External Resources

**.chezmoiexternal.toml.tmpl:**
```toml
[".vim/autoload/plug.vim"]
    type = "file"
    url = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"

[".oh-my-zsh"]
    type = "archive"
    url = "https://github.com/ohmyzsh/ohmyzsh/archive/master.tar.gz"
    exact = true
    stripComponents = 1
    refreshPeriod = "168h"

[".local/bin/age"]
    type = "archive-file"
    url = "https://github.com/FiloSottile/age/releases/download/v1.1.1/age-v1.1.1-{{ .chezmoi.os }}-{{ .chezmoi.arch }}.tar.gz"
    path = "age/age"
    executable = true
```

### 5. Configure Interactive Prompts

**.chezmoi.toml.tmpl:**
```toml
{{- $editor := promptChoice "favorite editor" ["vim" "neovim" "vscode"] -}}
[data]
    name = "{{ promptString "your name" }}"
    email = "{{ promptString "your email" }}"
    editor = {{ $editor }}

{{ if promptBool "enable work config?" -}}
[data.work]
    enabled = true
    work_email = "{{ promptString "work email" }}"
{{ end }}
```

### 6. Ignore Files Conditionally

**.chezmoiignore (template-aware):**
```text
README.md
*.log

{{- if ne .chezmoi.hostname "work-laptop" }}
.work
{{- end }}

{{- if eq .chezmoi.os "windows" }}
Documents/*
!Documents/*PowerShell/
{{- end }}
```

### 7. Interpret `chezmoi managed` / `chezmoi unmanaged` Output (Config Files)

When reviewing `chezmoi unmanaged`, note that the *destination* config file is `~/.config/chezmoi/chezmoi.toml`, while the *source* is typically managed as a template such as `dot_config/chezmoi/chezmoi.toml.tmpl` (or `private_dot_config/chezmoi/chezmoi.toml.tmpl`) in the chezmoi source state.

If `~/.config/chezmoi` appears as unmanaged:
- First check `chezmoi managed` to confirm whether the config file is already managed in source.
- If it is not managed, add it as a template and manage it in source (recommended when you maintain machine-specific values in `chezmoi.toml`).

### 8. Manage run_once Scripts

**run_once_000-bootstrap.sh.tmpl:**
```bash
#!/bin/bash
{{ if eq .chezmoi.os "darwin" -}}
if ! command -v brew &> /dev/null; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
{{ end -}}
```

**Reset run_once state:**
```bash
# Clear all run_once script state
chezmoi state delete-bucket --bucket=scriptState
```

## Built-in Variables

Commonly used chezmoi variables available in all templates:

| Variable | Description | Example |
|----------|-------------|---------|
| `.chezmoi.os` | Operating system | `linux`, `darwin`, `windows` |
| `.chezmoi.arch` | Architecture | `amd64`, `arm64` |
| `.chezmoi.hostname` | Machine hostname | `my-laptop` |
| `.chezmoi.username` | Current user | `john` |
| `.chezmoi.homeDir` | Home directory | `/home/john` |
| `.chezmoi.sourceDir` | Source state directory | `/home/john/.local/share/chezmoi` |
| `.chezmoi.env.VAR` | Environment variables | `.chezmoi.env.EDITOR` |

## Template Syntax Reference

### Conditionals

```go
{{ if eq .chezmoi.os "darwin" }}
# macOS-specific
{{ else if eq .chezmoi.os "linux" }}
# Linux-specific
{{ end }}
```

### Loops

```go
{{ range .packages.darwin.brews -}}
brew "{{ . }}"
{{ end -}}
```

### String Operations

```go
{{ .name | quote }}          # Add quotes
{{ .chezmoi.homeDir }}        # No trimming
{{- "content" -}}            # Trim whitespace
```

## Best Practices

1. **Use templates for cross-platform configs** - Leverage `.chezmoi.os`, `.chezmoi.arch`
2. **Store secrets in password managers** - Never hardcode sensitive data
3. **Make scripts idempotent** - Safe to run multiple times
4. **Use descriptive filenames** - `run_once_000-bootstrap.sh.tmpl`
5. **Test templates locally** - Use `chezmoi execute-template < file.tmpl`
6. **Organize .chezmoidata** - Separate concerns into multiple files
7. **Document dependencies** - Comment complex configurations
8. **Use appropriate refresh periods** - Balance freshness and bandwidth

## Consulting Latest Documentation

This skill can consult the latest chezmoi documentation via Context7 to ensure accuracy:

```bash
# When in doubt, ask for the latest docs
"Check the chezmoi documentation for [topic]"
```

If the question involves `.tmpl` behavior (especially `.chezmoiignore{,.tmpl}`), prefer checking the official docs first.

## Useful Commands

```bash
# ⚠️ FORBIDDEN - Apply all changes (must run manually)
chezmoi apply

# Dry run (preview changes) - SAFE
chezmoi apply --dry-run

# ⚠️ FORBIDDEN - Update source state (may change managed files)
chezmoi update

# Edit source state - SAFE
chezmoi cd

# Add file as template - SAFE
chezmoi add --template ~/.config/file

# Verify configuration - SAFE
chezmoi doctor

# View all template data - SAFE
chezmoi data

# List ignored files - SAFE
chezmoi ignored

# Test template (preview output) - SAFE
chezmoi execute-template < ~/.local/share/chezmoi/dot_file.tmpl

# View run_once state - SAFE
chezmoi state dump

# Clear run_once script state (use with caution) - SAFE
chezmoi state delete-bucket --bucket=scriptState

# Clear run_onchange script state (use with caution) - SAFE
chezmoi state delete-bucket --bucket=entryState

# See what would change - SAFE
chezmoi diff

# Verify files match expected state - SAFE
chezmoi verify
```

## File Structure

Standard chezmoi source state structure:

```
~/.local/share/chezmoi/
├── .chezmoi.toml.tmpl          # Main configuration (optional)
├── .chezmoiexternal.toml.tmpl   # External resources (optional)
├── .chezmoiignore.tmpl          # Ignore rules (template-aware, optional)
├── .chezmoidata/
│   ├── packages.yaml            # Custom data
│   └── work.yaml
├── dot_gitconfig.tmpl           # Regular templates
├── dot_zshrc.tmpl
├── run_once_000-bootstrap.sh.tmpl
├── run_onchange_install-packages.sh.tmpl
└── run_after_dot_vimrc.sh.tmpl
```

## Debugging

**注意：调试时也不要执行 `chezmoi update`，如需检查变更请用 `chezmoi diff` 或 `chezmoi apply --dry-run`。**

**Verbose output:**
```bash
chezmoi apply --verbose
```

**Check what would change:**
```bash
chezmoi diff
```

**Validate configuration:**
```bash
chezmoi doctor
```

**See expanded template:**
```bash
chezmoi execute-template < template-file
```

## When to Use This Skill

Use this skill whenever you're:
- Creating new chezmoi templates with Go syntax
- Modifying existing .chezmoi configuration files
- Managing .chezmoiignore/.chezmoiignore.tmpl rules
- Setting up .chezmoiexternal for external resources
- Writing run_once/run_onchange scripts
- Integrating password managers for secrets
- Managing cross-platform dotfiles
- Debugging template issues
- Organizing .chezmoidata files

For specific concerns, refer to the detailed reference documentation listed above.
