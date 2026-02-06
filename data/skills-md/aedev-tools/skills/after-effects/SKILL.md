---
name: after-effects
description: >
  Automate Adobe After Effects via ExtendScript. Use when the user asks to
  create, modify, or query anything in an After Effects project — layers,
  keyframes, expressions, effects, compositions, assets, rendering, batch
  operations. Generates and executes JSX ExtendScript via osascript on macOS.
compatibility: Requires macOS with Adobe After Effects installed. Needs "Allow Scripts to Write Files and Access Network" enabled in AE Preferences > Scripting & Expressions.
allowed-tools: Bash(osascript *) Bash(chmod *) Bash(bash *) Read Write
metadata:
  author: aedev-tools
  version: "1.0"
---

## Overview

This skill automates After Effects by generating ExtendScript (.jsx) and executing it via osascript. It reads project state through query scripts, uses rule files for domain knowledge, and wraps all mutations in undo groups.

## First-Time Setup

1. Run `scripts/runner.sh` with any query script to detect the AE version
2. If multiple AE versions are installed, the user must choose one — runner.sh will prompt
3. Ensure AE Preferences > Scripting & Expressions > "Allow Scripts to Write Files and Access Network" is enabled

## Workflow

For every user request:

### Step 1: Gather context (auto-run, no confirmation needed)

Run the active state query:
```bash
bash scripts/runner.sh scripts/active-state.jsx
```
Then read `/tmp/ae-assistant-result.json` for active comp, selected layers, CTI.

If this is the first interaction or the project context is unknown, also run:
```bash
bash scripts/runner.sh scripts/project-overview.jsx
```
This returns a **summary** by default: folder tree with counts, all comps listed, footage grouped by file type. NOT every individual file.

To drill into a specific folder:
```bash
bash scripts/runner.sh scripts/project-overview.jsx '{"mode": "folder", "folderName": "Images"}'
```

Only use full mode when you actually need every item listed:
```bash
bash scripts/runner.sh scripts/project-overview.jsx '{"mode": "full"}'
```

### Step 2: Drill down if needed (auto-run)

If the task targets a specific comp:
```bash
bash scripts/runner.sh scripts/comp-detail.jsx '{"compName": "Comp Name"}'
```

If the task targets specific layers:
```bash
bash scripts/runner.sh scripts/layer-detail.jsx '{"layerNames": ["Layer 1", "Layer 2"]}'
```

Omit `compName` to use the active comp. Omit `layerNames` to use selected layers.

### Step 3: Load domain knowledge

Read the relevant rule file from `rules/`. Always read `rules/extendscript-fundamentals.md` — it contains ES3 constraints that apply to every generated script.

| Task involves | Load rule file |
|---|---|
| Layers (create, move, parent, duplicate) | [rules/layer-manipulation.md](rules/layer-manipulation.md) |
| Keyframes, animation, easing | [rules/keyframes-animation.md](rules/keyframes-animation.md) |
| Expressions | [rules/expressions.md](rules/expressions.md) |
| Compositions (create, precompose, nest) | [rules/composition-management.md](rules/composition-management.md) |
| Effects and parameters | [rules/effects.md](rules/effects.md) |
| Import, footage, assets | [rules/assets-footage.md](rules/assets-footage.md) |
| Render queue, export | [rules/rendering.md](rules/rendering.md) |
| Bulk/batch operations | [rules/batch-operations.md](rules/batch-operations.md) |
| Version-specific features | [references/ae-api-versions.md](references/ae-api-versions.md) |

### Step 4: Generate the action script

**CRITICAL: Resolve the skill's real path first**

Before writing or executing any action script, resolve the skill's real (non-symlinked) path. ExtendScript `#include` cannot follow symlinks, so you MUST use the real filesystem path.

Run this once at the start of each session:
```bash
SKILL_SCRIPTS="$(readlink -f ~/.claude/skills/after-effects-assistant/scripts 2>/dev/null || readlink ~/.claude/skills/after-effects-assistant/scripts)"
echo "$SKILL_SCRIPTS"
```

Use the resolved path (`$SKILL_SCRIPTS`) for all subsequent Write and Bash commands in this session.

**Why this matters:**
- `~/.claude/skills/` is typically a symlink — ExtendScript `#include` fails through symlinks
- Writing to the real `scripts/` directory lets `#include "lib/json2.jsx"` resolve correctly
- The resolved path changes per machine, so never hardcode it

Every generated script MUST follow this template:

```jsx
#include "lib/json2.jsx"
#include "lib/utils.jsx"

(function() {
    app.beginUndoGroup("AE Assistant: <action description>");
    try {
        var args = readArgs();
        var comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) {
            writeResult({ error: "No active composition" });
            return;
        }

        // ... action code ...

        writeResult({ success: true, message: "<what was done>" });
    } catch (e) {
        try { writeResult({ error: e.toString(), line: e.line, fileName: e.fileName }); }
        catch(e2) { writeError(e.toString(), "line:" + e.line); }
    } finally {
        app.endUndoGroup();
    }
})();
```

**Write the script using the Write tool, then execute with a short bash command:**

1. Use the **Write** tool to write the script to `$SKILL_SCRIPTS/ae-action.jsx` (the resolved real path)
2. Execute it with bash:
```bash
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/ae-action.jsx"
```

**IMPORTANT:** Do NOT use `cat > file << 'SCRIPT'` heredocs — they put the entire script in the bash command, cluttering the permission prompt. Always use the Write tool for the script content, then a short bash command to run it.

### Step 5: Execute or confirm

**Auto-run** (no confirmation needed):
- All read-only queries (active-state, project-overview, comp-detail, layer-detail)
- Non-destructive additions: adding a keyframe, adding an effect, creating a layer, creating a comp

**Confirm before running** (show the script and ask the user):
- Deleting layers or comps
- Removing keyframes
- Replacing footage
- Clearing expressions
- Render queue operations
- Any operation the user might not expect

### Step 6: Execute and read result

```bash
# Execute the action script (already written to $SKILL_SCRIPTS/ae-action.jsx in Step 4)
bash "$SKILL_SCRIPTS/runner.sh" "$SKILL_SCRIPTS/ae-action.jsx" '{"arg1": "value1"}'
```

Read `/tmp/ae-assistant-result.json` for the result.

### Debugging failures

If a script fails, check these in order:
1. **`~/.ae-assistant-log`** — runner.sh logs every execution, args, results, and errors here
2. **`/tmp/ae-assistant-error.txt`** — JXA-level errors (AE not responding, DoScriptFile failure)
3. **`~/.ae-assistant-extendscript.log`** — ExtendScript-level logs from `appendLog()` in utils.jsx
4. **AE Preferences** — Ensure "Allow Scripts to Write Files and Access Network" is enabled

When an error occurs, read `~/.ae-assistant-log` to understand what happened, fix the script, and retry.

## MUST

- ALWAYS wrap mutations in `app.beginUndoGroup()` / `app.endUndoGroup()`
- ALWAYS use matchNames for property access, not display names (display names are localized)
- ALWAYS use 1-based indexing for layers and project items
- ALWAYS write action scripts to `$SKILL_SCRIPTS/ae-action.jsx` (the resolved real path, NOT `/tmp/`)
- ALWAYS use relative `#include "lib/json2.jsx"` and `#include "lib/utils.jsx"` (NOT absolute paths)
- ALWAYS wrap in an IIFE to avoid global scope pollution
- ALWAYS use `var`, never `let` or `const` (ES3)
- ALWAYS write results to /tmp/ae-assistant-result.json via writeResult()
- ALWAYS check `comp instanceof CompItem` before accessing comp properties

## FORBIDDEN

- NEVER use ES5+ syntax: let, const, arrow functions, template literals, destructuring
- NEVER use Array.map, Array.filter, Array.reduce, Array.forEach (not in ES3)
- NEVER use JSON.parse or JSON.stringify without including json2.jsx
- NEVER write action scripts to `/tmp/` — ExtendScript `#include` can't resolve paths from there
- NEVER use absolute paths in `#include` — they break through symlinks
- NEVER hardcode layer indices — use names, selection, or iteration
- NEVER run destructive operations without user confirmation
- NEVER assume a comp is active without checking
- NEVER use `cat > file << 'SCRIPT'` heredocs to write scripts — use the Write tool instead, then execute with a short bash command
