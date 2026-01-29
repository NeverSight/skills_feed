---
name: setting-up-devcontainers
description: Generate devcontainer configurations for Claude Code development environments. Use when setting up development containers with Claude Code and optional Codex CLI. Automatically detects marketplace.json for plugin marketplace configurations.
license: Apache-2.0
metadata:
  author: Softgraphy GK
  version: "0.2.0"
---

# Setting Up Devcontainers for Claude Code

Generate complete `.devcontainer/` configurations for Claude Code development environments with:
- Pre-installed Claude Code (+ optional Codex CLI built into Docker image)
- Persistent credentials and config via Docker volumes
- **Marketplace mode** (if marketplace.json exists): Auto-enabled plugins and skills

## Quick Start

```
User: Set up a devcontainer for this project
Agent: I'll check for marketplace.json and generate the devcontainer configuration.
```

## Workflow

### Step 1: Detect Mode

Check for `.claude-plugin/marketplace.json`:

```bash
ls .claude-plugin/marketplace.json
```

**Mode determination**:
- **Marketplace mode**: If `marketplace.json` exists → full plugin/skill setup
- **Generic mode**: If not found → Claude Code environment (+ optional Codex CLI)

For **Marketplace mode**, extract:
- `name` - Marketplace name (used for volume naming)
- `plugins` - Array of plugin definitions

For **Generic mode**, use:
- Project directory name for volume naming

### Step 2: Ask About Codex CLI Support (Optional)

**Ask the user explicitly**:

> Do you want to add Codex CLI (OpenAI) support alongside Claude Code?
>
> - **Yes**: Adds Volta, Node.js, Codex CLI, and skill sync mechanism
> - **No** (default): Claude Code only

If yes:
- Add Volta/Node.js/Codex CLI installation to Dockerfile (installed at build time)
- Add `~/.codex/` volume mount for config persistence
- Add `sync-codex-skills.sh` script (copies skills to `~/.codex/skills/`) [Marketplace mode only]
- Add Codex sync call to `post-create.sh` [Marketplace mode only]

**Note**: Both Claude Code and Codex CLI are installed at Docker build time for faster container startup.

### Step 3: Discover Plugins and Skills [Marketplace Mode Only]

Skip this step in Generic mode.

For each plugin in `marketplace.json`:

1. Read `source` path (e.g., `"./plugins/plugin-name"`)
2. Check for `.claude-plugin/plugin.json` in source directory
3. Find `skills` path from plugin.json or use `./skills/` default
4. List all SKILL.md files in skills directory
5. Extract skill names from directory names

**Build two lists**:
- `enabledPlugins`: `{"plugin-name@marketplace-name": true, ...}`
- `allowedSkills`: `["Skill(skill-1)", "Skill(skill-2)", ...]`

### Step 4: Ask About Auto-Sync on Container Start [Marketplace Mode Only]

Skip this step in Generic mode.

**Ask the user explicitly**:

> Do you want to automatically reinstall the marketplace on every container start?
>
> - **Yes**: Adds `postStartCommand` to run `reinstall-marketplace.sh` automatically
> - **No** (recommended for stable development): Run manually when needed
>
> Note: This is a workaround for Claude Code not detecting local plugin changes.
> Running on every start adds ~5-10 seconds delay.

### Step 5: Generate Files from Templates

Use the templates in `templates/` directory, substituting placeholders:

#### Common Placeholders

| Placeholder | Value |
|-------------|-------|
| `{{PROJECT_NAME}}` | Marketplace name (if exists) or project directory name |
| `{{PROJECT_DIR}}` | Project directory name |
| `{{CODEX_VOLUME_MOUNT}}` | If Codex: `,\n    "source=codex-config-{{PROJECT_NAME}},..."` else: empty |
| `{{VOLTA_ENV_BLOCK}}` | If Codex: `ENV VOLTA_HOME=... ENV PATH=...` else: empty |
| `{{CODEX_INSTALL_BLOCK}}` | If Codex: Volta/Codex RUN command, else: empty |
| `{{CODEX_DIR_LIST}}` | If Codex: ` "$HOME/.codex"` else: empty |
| `{{CODEX_ALIASES}}` | If Codex: Codex alias lines, else: empty |
| `{{CODEX_ALIAS_ECHO}}` | If Codex: `echo "  codex-f   - codex --full-auto"` else: empty |
| `{{DEVCONTAINER_READY_MESSAGE}}` | "Claude Code devcontainer ready!" or "Claude Code + Codex CLI devcontainer ready!" |

#### Marketplace Mode Placeholders

| Placeholder | Value |
|-------------|-------|
| `{{ENABLED_PLUGINS}}` | Object entries like `"plugin@market": true` |
| `{{ALLOWED_SKILLS}}` | Array entries like `"Skill(name)"` |
| `{{PLUGIN_INSTALL_COMMANDS}}` | Plugin install commands (with `|| true`) |
| `{{CODEX_SETUP_BLOCK}}` | If Codex **and** Marketplace mode: Codex skill sync in post-create.sh, else: empty |
| `{{CODEX_SYNC_BLOCK}}` | If Codex: Codex sync in reinstall-marketplace.sh, else: empty |
| `{{POST_START_COMMAND}}` | If auto-sync: `,\n  "postStartCommand": "bash .devcontainer/reinstall-marketplace.sh"` else: empty |
| `{{SETTINGS_BLOCK}}` | Shell commands to create settings.json with enabledPlugins/allowedSkills |
| `{{MARKETPLACE_REGISTER_BLOCK}}` | Marketplace registration and plugin install commands |
| `{{MARKETPLACE_SYNC_HINT}}` | `echo "To sync marketplace: bash .devcontainer/reinstall-marketplace.sh"` |

#### Generic Mode Placeholders

| Placeholder | Value |
|-------------|-------|
| `{{POST_START_COMMAND}}` | empty (no postStartCommand) |
| `{{SETTINGS_BLOCK}}` | empty (no plugin settings needed) |
| `{{MARKETPLACE_REGISTER_BLOCK}}` | empty (no marketplace registration) |
| `{{CODEX_SETUP_BLOCK}}` | empty (no skill sync needed) |
| `{{MARKETPLACE_SYNC_HINT}}` | empty |

**Templates**:
- [devcontainer.json.template](templates/devcontainer.json.template) - Container configuration
- [Dockerfile.template](templates/Dockerfile.template) - Ubuntu + dependencies
- [post-create.sh.template](templates/post-create.sh.template) - Initial setup
- [reinstall-marketplace.sh.template](templates/reinstall-marketplace.sh.template) - Marketplace sync (Marketplace mode only)
- [sync-codex-skills.sh.template](templates/sync-codex-skills.sh.template) - Codex skill sync (Marketplace mode + Codex only)

**Conditional logic**:
- **Generic mode**: Omit reinstall-marketplace.sh and sync-codex-skills.sh
- **If user chose no auto-sync**: Remove `postStartCommand` from devcontainer.json
- **If user chose no Codex**: Omit Volta/Codex sections

### Step 6: Write Files and Set Permissions

1. Create `.devcontainer/` directory if not exists
2. Write all generated files (without `.template` suffix)
3. Make shell scripts executable: `chmod +x .devcontainer/*.sh`

### Step 7: Provide Usage Instructions

**Generic mode**:
```
Devcontainer files created in .devcontainer/

To use:
1. Open project in VS Code
2. Click "Reopen in Container" when prompted
   (or use Command Palette: "Dev Containers: Reopen in Container")
3. Run 'claude' on first use to complete initial setup

Your credentials persist in Docker volumes.
```

**Marketplace mode**:
```
Devcontainer files created in .devcontainer/

To use:
1. Open project in VS Code
2. Click "Reopen in Container" when prompted
   (or use Command Palette: "Dev Containers: Reopen in Container")
3. Run 'claude' on first use to complete initial setup

Your credentials persist in Docker volumes.

To manually sync marketplace changes:
  bash .devcontainer/reinstall-marketplace.sh
```

## Generated File Locations

**Generic mode**:
```
.devcontainer/
├── devcontainer.json         # Container configuration
├── Dockerfile                # Ubuntu + Claude Code (+ Volta/Codex if enabled)
└── post-create.sh            # Initial setup (config, aliases)
```

**Marketplace mode**:
```
.devcontainer/
├── devcontainer.json         # Container configuration
├── Dockerfile                # Ubuntu + Claude Code (+ Volta/Codex if enabled)
├── post-create.sh            # Initial setup (config, marketplace, Codex sync)
├── reinstall-marketplace.sh  # Marketplace sync script (+ Codex sync if enabled)
└── sync-codex-skills.sh      # Codex skill sync (only if Codex enabled)
```

## Key Configuration Details

### Volume Strategy

Uses named Docker volumes plus a symlink for complete persistence:

```
Docker Image (built once):
├── ~/.local/bin/claude      # Claude Code binary
└── ~/.volta/                # Volta + Node.js + Codex CLI (if enabled)

Volume 1: claude-config-${PROJECT_NAME} → ~/.claude/
├── .home-claude.json        # Setup state (symlink target)
├── .credentials.json        # Auth tokens
├── settings.json            # User settings
└── plugins/                 # Plugin data (Marketplace mode)

Volume 2: claude-data-${PROJECT_NAME} → ~/.local/share/claude/
└── (Claude Code data)       # Session data, etc.

Volume 3 (if Codex enabled): codex-config-${PROJECT_NAME} → ~/.codex/
├── config.toml              # Codex CLI configuration
├── sessions/                # Session data
└── skills/                  # Synced skills from marketplace (Marketplace mode)

Symlink (created by post-create.sh):
~/.claude.json → ~/.claude/.home-claude.json
```

**Why this architecture?**

| Location | Purpose | Persistence Method |
|----------|---------|-------------------|
| `~/.local/bin/claude` | Claude Code binary | Docker image (fast startup) |
| `~/.volta/` | Codex CLI binary | Docker image (fast startup) |
| `~/.claude/` | Config, credentials, settings | Volume mount |
| `~/.local/share/claude/` | Claude session data | Volume mount |
| `~/.claude.json` | Initial setup state | Symlink to volume |
| `~/.codex/` (optional) | Codex config, sessions, skills | Volume mount |

**Important**: `~/.claude.json` cannot be directly mounted as a volume (Docker creates a directory instead of a file). The symlink approach allows the file to persist inside the `~/.claude/` volume.

### Shell Alias

The setup creates a persistent alias file in the volume:

- `post-create.sh` creates `~/.claude/.shell-aliases` (persists in volume)
- `post-create.sh` adds `source` line to `.zshrc` (both modes, with duplicate protection)
- `reinstall-marketplace.sh` also adds `source` line to `.zshrc` on every start (Marketplace mode only)

```bash
# ~/.claude/.shell-aliases (persisted)
alias claude-y='claude --dangerously-skip-permissions'

# If Codex enabled:
alias codex-f='codex --full-auto'
```

This survives container rebuilds because the alias file is stored in the volume.

### Plugin Format [Marketplace Mode Only]

**enabledPlugins** must be object format (not array):

```json
{
  "enabledPlugins": {
    "plugin-a@marketplace": true,
    "plugin-b@marketplace": true
  }
}
```

### Marketplace Sync (Workaround) [Marketplace Mode Only]

`reinstall-marketplace.sh` is a **workaround** for Claude Code not automatically detecting local plugin/skill changes.

**What it does**:
- Removes and re-adds the marketplace
- Reinstalls all enabled plugins

**When to run**:
- Manually after editing SKILL.md files: `bash .devcontainer/reinstall-marketplace.sh`
- Or automatically via `postStartCommand` (if user opted in)

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No plugins found | Empty plugins array | Warn user, generate minimal config |
| Source path invalid | Plugin source doesn't exist | Report error, skip invalid plugins |
| Existing .devcontainer/ | Files already present | Ask before overwriting |
| GID/UID 1000 already exists | Ubuntu base image has existing user | Use `getent` to detect and rename existing user |
| Permission denied on config | Volume owned by root | Use `sudo chown` in post-create.sh |
| claude: command not found | PATH not set | Export `PATH="$HOME/.local/bin:$PATH"` in scripts |
| EISDIR on ~/.claude.json | Volume mounted as directory | Remove directory, use symlink instead |
| JSON Parse error: Unexpected EOF | Empty ~/.claude.json file | Initialize with `{}` not empty file |
| Raw mode not supported | Plugin commands in non-interactive shell | Only run plugin commands if setup complete |
| Login required after rebuild | ~/.claude.json not persisted | Symlink to file inside volume |

## References

- [Devcontainer Specification](references/devcontainer-spec.md)
- [Claude Code Installation](references/claude-code-installation.md)
- [Codex CLI Installation](references/codex-cli-installation.md)
