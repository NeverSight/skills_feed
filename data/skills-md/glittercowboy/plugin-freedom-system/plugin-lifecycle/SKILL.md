---
name: plugin-lifecycle
description: Manage complete plugin lifecycle - install, uninstall, reset, destroy. Use when user runs /install-plugin, /uninstall, /reset-to-ideation, /destroy, /clean commands, or says 'install [Name]', 'remove [Name]', 'uninstall [Name]', 'delete [Name]'.
allowed-tools:
  - Bash
  - Read
  - Edit # For PLUGINS.md updates
  - Write # For backup metadata
preconditions:
  - Varies by mode (see mode-specific preconditions)
---

# plugin-lifecycle Skill

**Purpose:** Manage the complete lifecycle of plugins from installation to removal with proper state tracking and safety features.

## Overview

This skill handles all plugin lifecycle operations on macOS:

- **Installation (Mode 1)**: Copy Release binaries to system folders (`~/Library/Audio/Plug-Ins/`)
- **Uninstallation (Mode 2)**: Clean removal from system folders (preserves source code)
- **Reset to Ideation (Mode 3)**: Remove implementation, keep idea/mockups (surgical rollback)
- **Destroy (Mode 4)**: Complete removal with backup (nuclear option)

All operations include proper permissions, cache clearing, state tracking, and safety features (confirmations, backups).

---


## Mode Dispatcher

This skill operates in different modes based on the invoking command:

| Mode | Operation | Command | Purpose |
|------|-----------|---------|---------|
| 1 | Installation | `/install-plugin` | Deploy to system folders |
| 2 | Uninstallation | `/uninstall` | Remove binaries, keep source |
| 3 | Reset to Ideation | `/reset-to-ideation` | Remove implementation, keep idea/mockups |
| 4 | Destroy | `/destroy` | Complete removal with backup |
| Menu | Interactive | `/clean` | Present menu, user chooses mode |

**Invocation Pattern:**
When user runs `/install-plugin [Name]`, the command expands to a prompt that invokes THIS skill.
Determine mode by examining command (see [references/invocation-protocol.md](references/invocation-protocol.md)), then load ONLY the relevant reference file:
- Mode 1 → Load and execute `references/installation-process.md` ONLY
- Mode 2 → Load and execute `references/uninstallation-process.md` ONLY
- Mode 3 → Load and execute `references/mode-3-reset.md` ONLY
- Mode 4 → Load and execute `references/mode-4-destroy.md` ONLY
- Menu → Present menu, wait for selection, then load chosen mode reference file

**IMPORTANT:** Do NOT load other mode reference files. Load only the reference file for the active mode to optimize context window usage.

**Installation targets (macOS):**
- VST3, AU: `~/Library/Audio/Plug-Ins/VST3/`, `~/Library/Audio/Plug-Ins/Components/`
- AAX: `~/Library/Application Support/Avid/Audio/Plug-Ins/` (future)

---

## Installation Workflow (Mode 1 - Critical - Do Not Skip Steps)

Copy this checklist to track installation progress:

```
Installation Progress:
- [ ] Step 1: Build verification (BLOCKING)
- [ ] Step 2: Product name extraction
- [ ] Step 3: Old version removal
- [ ] Step 4: Copy to system folders (BLOCKING)
- [ ] Step 5: Permissions verification (BLOCKING)
- [ ] Step 6: Cache clearing
- [ ] Step 7: Verification (BLOCKING)
- [ ] Step 8: PLUGINS.md update (BLOCKING)
```

Execute these steps in order:

1. **Build Verification** (BLOCKING) - Check Release binaries exist, offer to build if missing
   - See: `references/installation-process.md` Step 1
   - Cannot proceed without binaries

2. **Product Name Extraction** - Extract PRODUCT_NAME from CMakeLists.txt
   - See: `references/installation-process.md` Step 2
   - Required for all subsequent steps

3. **Old Version Removal** - Remove existing installations to prevent conflicts
   - See: `references/installation-process.md` Step 3
   - Can proceed if no old version exists

4. **Copy to System Folders** (BLOCKING) - Install VST3 and AU to macOS plugin directories
   - See: `references/installation-process.md` Step 4
   - Core installation step

5. **Permissions Verification** (BLOCKING) - Set 755 permissions for DAW access
   - See: `references/installation-process.md` Step 5
   - DAWs cannot load plugins without correct permissions

6. **Cache Clearing** - Clear Ableton Live and Logic Pro caches
   - See: `references/cache-management.md`
   - Display warning if fails, then proceed

7. **Verification** (BLOCKING) - Confirm installation with file checks and size validation
   - See: `references/installation-process.md` Step 7
   - Must confirm success before declaring completion

8. **PLUGINS.md Update** (BLOCKING) - Record installation status and locations
   - See: `references/installation-process.md` Step 8
   - State tracking is part of success criteria

**Note:** Steps marked BLOCKING must succeed before proceeding.

**Feedback Loop:**
If Step 7 (Verification) fails:
1. Review error details
2. Check reference file: `references/error-handling.md`
3. Apply fix
4. Retry from Step 4 (Copy to System Folders)

If verification succeeds, proceed to decision menu.

See **[references/installation-process.md](references/installation-process.md)** for complete implementation.

---

## Cache Management

See **[references/cache-management.md](references/cache-management.md)** for cache clearing procedures (invoked during installation and uninstallation).

---

## Uninstallation Workflow (Mode 2)

See **[references/uninstallation-process.md](references/uninstallation-process.md)** for complete uninstallation process (locate, confirm, remove, clear caches, update PLUGINS.md).

---

## Reset to Ideation Workflow (Mode 3)

Surgical rollback - removes implementation, preserves idea/mockups. Use case: Implementation failed but concept is solid. See **[references/mode-3-reset.md](references/mode-3-reset.md)** for complete process.

---

## Destroy Workflow (Mode 4)

Complete removal with backup. Use case: Abandoned experiment, never using again. Requires exact plugin name confirmation (safety gate). See **[references/mode-4-destroy.md](references/mode-4-destroy.md)** for complete process.

---

## Interactive Menu (Mode: Menu)

When invoked via `/clean [PluginName]`, present interactive menu:

```
Plugin cleanup options for [PluginName]:

1. Uninstall - Remove binaries from system folders (keep source code)
2. Reset to ideation - Remove implementation, keep idea/mockups
3. Destroy - Complete removal with backup (IRREVERSIBLE except via backup)
4. Cancel

Choose (1-4): _
```

**Menu logic:**
1. Read current status from PLUGINS.md
2. Filter options based on status:
   - IF status = "💡 Ideated" → Show options 2, 3, 4 (cannot uninstall what isn't built)
   - IF status = "✅ Working" → Show options 1, 2, 3, 4 (not installed yet)
   - IF status = "📦 Installed" → Show ALL options (full lifecycle available)
   - IF status = "🚧 In Progress" → Show only option 4 (Cancel)
   - ELSE (unknown status) → Show ALL options with warning: "Unknown status '[status]' - showing all options"
3. Present filtered menu, wait for user choice
4. Route to selected mode (1-4) or exit on Cancel

---

## Checkpoint Protocol

After successful operations, check workflow mode before presenting decision menu:

1. **Check workflow mode:**
   - Read `.claude/preferences.json` for `workflow.mode` setting
   - Modes: "manual" (present menu) or "express" (skip menu)

2. **Manual mode (default):**
   - Present decision menu to user
   - See [references/decision-menu-protocol.md](references/decision-menu-protocol.md) for menu format

3. **Express mode:**
   - Skip decision menu
   - Return control to caller immediately

**Note:** plugin-lifecycle operations are terminal (don't chain to next stage), so express mode behavior is: complete operation → skip menu → end workflow.

---

## Integration Points

**Invoked by:**

- `/install-plugin [PluginName]` → Mode 1 (Installation)
- `/uninstall [PluginName]` → Mode 2 (Uninstallation)
- `/reset-to-ideation [PluginName]` → Mode 3 (Reset)
- `/destroy [PluginName]` → Mode 4 (Destroy)
- `/clean [PluginName]` → Interactive menu
- `plugin-workflow` skill → After Stage 3 (auto-installs)
- `plugin-improve` skill → After successful changes (offers reinstallation)
- Natural language: "Install [PluginName]", "Remove [PluginName]", "Clean up [PluginName]"

**Invokes:**

- None (terminal skill, doesn't invoke others)

**Invocation patterns**: See [references/invocation-protocol.md](references/invocation-protocol.md) for mode detection and routing.

**Updates:**

- `PLUGINS.md` → Table row: status, version, last updated
- `plugins/[Name]/NOTES.md` → Status metadata, timeline entries, installation details

**Creates:**

- System folder installations (non-git-tracked):
  - `~/Library/Audio/Plug-Ins/VST3/[Product].vst3`
  - `~/Library/Audio/Plug-Ins/Components/[Product].component`

**Blocks:**

- None (installation is optional, plugins can be tested without installing)

---

## Success Criteria

Installation is successful when: VST3/AU installed with 755 permissions, caches cleared, PLUGINS.md updated, user informed of next steps.

---

