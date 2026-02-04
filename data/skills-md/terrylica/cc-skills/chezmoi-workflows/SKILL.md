---
name: chezmoi-workflows
description: Dotfile backup and sync with chezmoi. TRIGGERS - chezmoi, dotfiles, sync dotfiles, backup configs, cross-machine sync.
allowed-tools: Read, Edit, Bash
---

# Chezmoi Workflows

## When to Use This Skill

Use this skill when:

- Backing up dotfiles to Git repository
- Syncing configuration files across machines
- Tracking changes to shell configs, editor settings, or other dotfiles
- Managing templated configurations with chezmoi
- Troubleshooting dotfile drift between source and target

## Architecture

| Component  | Location                         | Purpose                               |
| ---------- | -------------------------------- | ------------------------------------- |
| **Source** | `$(chezmoi source-path)`         | Git repository with dotfile templates |
| **Target** | `~/`                             | Home directory (deployed files)       |
| **Remote** | GitHub (private recommended)     | Cross-machine sync and backup         |
| **Config** | `~/.config/chezmoi/chezmoi.toml` | User preferences and settings         |

---

## 1. Status Check

```bash
chezmoi source-path                    # Show source directory
chezmoi git -- remote -v               # Show GitHub remote
chezmoi status                         # Show drift between source and target
chezmoi managed | wc -l                # Count tracked files
```

---

## 2. Track File Changes

After editing a config file, add it to chezmoi:

```bash
chezmoi status                         # 1. Verify file shows as modified
chezmoi diff ~/.zshrc                  # 2. Review changes
chezmoi add ~/.zshrc                   # 3. Add to source (auto-commits if configured)
chezmoi git -- log -1 --oneline        # 4. Verify commit created
chezmoi git -- push                    # 5. Push to remote
```

---

## 3. Track New File

Add a previously untracked config file:

```bash
chezmoi add ~/.config/app/config.toml  # 1. Add file to source
chezmoi managed | grep app             # 2. Verify in managed list
chezmoi git -- push                    # 3. Push to remote
```

---

## 4. Sync from Remote

Pull changes from GitHub and apply to home directory:

```bash
chezmoi update                         # 1. Pull + apply (single command)
chezmoi verify                         # 2. Verify all files match source
chezmoi status                         # 3. Confirm no drift
```

---

## 5. Push All Changes

Bulk sync all modified tracked files to remote:

```bash
chezmoi status                         # 1. Review all drift
chezmoi re-add                         # 2. Re-add all managed files (auto-commits)
chezmoi git -- push                    # 3. Push to remote
```

---

## 6. First-Time Setup

### Install chezmoi

```bash
brew install chezmoi                   # macOS
```

### Initialize (fresh start)

```bash
/usr/bin/env bash << 'CONFIG_EOF'
chezmoi init                           # Create empty source
chezmoi add ~/.zshrc ~/.gitconfig      # Add first files
gh repo create dotfiles --private --source="$(chezmoi source-path)" --push
CONFIG_EOF
```

### Initialize (clone existing)

```bash
chezmoi init git@github.com:<user>/dotfiles.git
chezmoi apply                          # Deploy to home directory
```

---

## 7. Configure Source Directory

Move source to custom location (e.g., for multi-account SSH):

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
mv "$(chezmoi source-path)" ~/path/to/dotfiles
SKILL_SCRIPT_EOF
```

Edit `~/.config/chezmoi/chezmoi.toml`:

```toml
sourceDir = "~/path/to/dotfiles"
```

Verify:

```bash
chezmoi source-path                    # Should show new location
```

---

## 8. Change Remote

Switch to different GitHub account or repository:

```bash
chezmoi git -- remote -v                                              # View current
chezmoi git -- remote set-url origin git@github.com:<user>/<repo>.git # Change
chezmoi git -- push -u origin main                                    # Push to new remote
```

---

## 9. Resolve Merge Conflicts

```bash
/usr/bin/env bash << 'GIT_EOF'
chezmoi git -- status                  # 1. Identify conflicted files
chezmoi git -- diff                    # 2. Review conflicts
# Manually edit files in $(chezmoi source-path)
chezmoi git -- add <resolved-files>    # 3. Stage resolved files
chezmoi git -- commit -m "Resolve merge conflict"
chezmoi apply                          # 4. Apply to home directory
chezmoi git -- push                    # 5. Push resolution
GIT_EOF
```

---

## 10. Validation (SLO)

After major operations, verify system state:

```bash
chezmoi verify                         # Exit 0 = all files match source
chezmoi diff                           # Empty = no drift
chezmoi managed                        # Lists all tracked files
chezmoi git -- log --oneline -3        # Recent commit history
```

---

## Reference

- [Setup Guide](./references/setup.md) - Installation, multi-account GitHub, migration
- [Prompt Patterns](./references/prompt-patterns.md) - Detailed workflow examples
- [Configuration](./references/configuration.md) - chezmoi.toml settings, templates
- [Secret Detection](./references/secret-detection.md) - Handling detected secrets

**Chezmoi docs**: <https://www.chezmoi.io/reference/>

---

## Troubleshooting

| Issue              | Cause                      | Solution                                     |
| ------------------ | -------------------------- | -------------------------------------------- |
| chezmoi not found  | Not installed              | Install via `brew install chezmoi`           |
| Source path empty  | Not initialized            | Run `chezmoi init`                           |
| Git remote not set | Missing GitHub repo        | Run `chezmoi git -- remote add origin URL`   |
| Apply fails        | Template error             | Check template syntax with `chezmoi diff`    |
| Merge conflicts    | Diverged source and target | Use `chezmoi merge` to resolve               |
| Secrets detected   | Plain text credentials     | Use chezmoi templates with 1Password/Doppler |
