---
name: drupal-contribute-fix
description: >
  REQUIRED when user mentions a Drupal module + error/bug/issue - even without
  stack traces. Trigger on: (1) "<module_name> module has an error/bug/issue",
  (2) "Acquia/Pantheon/Platform.sh" + module problem, (3) any contrib module name
  (metatag, webform, mcp, paragraphs, etc.) + problem description. Searches
  drupal.org BEFORE you write any patch. NOT just for upstream contributions -
  use for ALL local fixes to contrib/core.
license: GPL-2.0-or-later
metadata:
  author: Drupal Community
  version: "1.4.0"
---

# drupal-contribute-fix

**Use this skill for ANY Drupal contrib/core bug - even "local fixes".**

Checks drupal.org before you write code, so you don't duplicate existing fixes.

## FIRST STEP - Before Writing Any Code

**If you are debugging an error in `docroot/modules/contrib/*` or `web/modules/contrib/*`,
run `preflight` BEFORE editing any code - even if the user only asked for a local fix.**

```bash
python3 scripts/contribute_fix.py preflight \
  --project <module-name> \
  --keywords "<error message>" \
  --out .drupal-contribute-fix
```

This takes 30 seconds and may save hours of duplicate work.

## LAST STEP - After Making Any Local Fix

**After you fix the bug locally, you MUST run `package` to generate contribution artifacts.**

```bash
python3 scripts/contribute_fix.py package \
  --root /path/to/drupal/site \
  --changed-path docroot/modules/contrib/<module-name> \
  --keywords "<error message>" \
  --test-steps "<step 1>" "<step 2>" "<step 3>" \
  --out .drupal-contribute-fix
```

This generates:
- A properly-named patch file for drupal.org
- A paste-ready issue comment
- A report with next steps

**Then tell the user** about the generated files and guide them through submission.

## NEVER DELETE Contribution Artifacts

**DO NOT delete these files:**
- `.drupal-contribute-fix/` directory
- Patch files in `patches/`
- `ISSUE_COMMENT.md`
- `REPORT.md`

Even if the user asks to "reset" or "undo" the local fix, **preserve the contribution artifacts**
so the fix can be submitted upstream. The whole point is to help the Drupal community.

## Complete Workflow

```
1. DETECT    → Error from contrib/core? Trigger activated.
2. PREFLIGHT → Search drupal.org BEFORE writing code
3. DECIDE    → Use existing fix OR proceed with new fix
4. FIX       → Make the local fix (edit files, create composer patch)
5. PACKAGE   → Run `package` command to generate contribution artifacts
6. PRESERVE  → Keep .drupal-contribute-fix/ and patches/ directories
7. GUIDE     → Tell user: "Here's how to submit this upstream..."
```

**Steps 5-7 are MANDATORY.** Don't just fix locally and move on.

## When to Use This Skill

### Early Conversational Triggers - Fire BEFORE Investigation

**You don't need a stack trace to trigger this skill.** Fire on high-level descriptions:

| User Says | Trigger? | Why |
|-----------|----------|-----|
| "The metatag module has an error" | **YES** | Module name + "error" |
| "mcp module isn't working with Acquia" | **YES** | Module + platform constraint |
| "I'm getting a bug in webform" | **YES** | Module name + "bug" |
| "paragraphs module throws an exception" | **YES** | Module + error indicator |
| "contrib module X has a problem" | **YES** | Explicit "contrib" mention |
| "my custom module has a bug" | Maybe | Only if it triggers a contrib/core bug |

**Key insight:** If the user mentions a Drupal module name (that isn't clearly custom) + any problem indicator (error, bug, issue, not working, exception, broken), trigger this skill FIRST. Don't wait until you've investigated and found a stack trace.

### MANDATORY Triggers - You MUST Use This Skill When:

1. **Error/exception originates FROM contrib or core code**
   - Stack trace shows `modules/contrib/` or `core/` as the source
   - Error message references a class in `Drupal\<contrib_module>\` namespace
   - Fatal error, TypeError, exception thrown by contrib/core code

2. **You are about to edit files in contrib or core**
   - `docroot/modules/contrib/*` or `web/modules/contrib/*`
   - `docroot/core/*` or `web/core/*`
   - `docroot/themes/contrib/*` or `web/themes/contrib/*`

3. **You are about to create a Composer patch for `drupal/*`**
   - Adding to `extra.patches` in composer.json
   - Creating files in `patches/` directory for Drupal packages

4. **Custom module encounters a bug in core/contrib**
   - Custom code works correctly but triggers a bug in contrib/core
   - The fix would need to be in the contrib/core code, not the custom module

5. **Hosting platform constraints cause contrib/core issues**
   - "Acquia best practices", "Pantheon", "Platform.sh" constraints
   - Core module disabled/unavailable causing contrib to fail

### This Skill is NOT Just for "Upstream Contributions"

**Common misconception:** This skill is only for contributing patches to drupal.org.

**Reality:** Use it for ALL local fixes to contrib modules. Why?
- The bug may already be fixed upstream (save yourself the work)
- An existing patch may exist that you can just apply
- Even if you need a local fix NOW, the preflight search is fast

### How to Recognize Contrib/Core Errors

Look for these patterns in error messages or stack traces:

```
# Error ORIGINATES from contrib - USE THIS SKILL
Drupal\metatag\MetatagManager->build()
docroot/modules/contrib/mcp/src/Plugin/Mcp/General.php
web/modules/contrib/webform/src/...
core/lib/Drupal/Core/...

# Error in CUSTOM module - skill may not apply
# (unless the custom code is triggering a bug in contrib/core)
modules/custom/mymodule/src/...
```

### Path Triggers:

- `web/core/`, `web/modules/contrib/`, `web/themes/contrib/`
- `docroot/core/`, `docroot/modules/contrib/`, `docroot/themes/contrib/`
- `patches/` directory (especially `patches/drupal-*`)

## What To Do

1. **FIRST**: Run `preflight` to search drupal.org (even for "local fixes")
2. **IF** existing fix found: Use it instead of writing your own
3. **IF** no fix found: Make the local fix, then run `package` to generate contribution artifacts
4. **AFTER FIXING**: Run `package` command to create patch + issue comment
5. **PRESERVE**: Keep `.drupal-contribute-fix/` directory - NEVER delete it
6. **GUIDE USER**: Tell them about the generated files and how to submit to drupal.org

## What This Skill Does

1. **Searches drupal.org** for existing issues matching your bug/fix
2. **Checks for existing solutions** (MRs, patches, closed-fixed status)
3. **Decides whether to proceed** or stop (use existing fix)
4. **Generates contribution artifacts** when appropriate:
   - Paste-ready issue comment
   - Properly-named patch file
   - Validation results (php lint, phpcs if available)

## Mandatory Gatekeeper Behavior

**No new patch file may be generated until upstream search + "already fixed?" checks are complete.**

The skill ends in exactly one of these outcomes:

| Exit Code | Outcome | Meaning |
|-----------|---------|---------|
| 0 | PROCEED | Patch (or test patch) generated |
| 10 | STOP | Existing upstream fix found (MR-based, patch-based, or closed-fixed) |
| 20 | STOP | Fixed upstream in newer version (reserved for future use) |
| 30 | STOP | Analysis-only recommended (patch would be hacky/broad) |
| 40 | ERROR | Couldn't determine project/baseline, network failure |
| 50 | STOP | Security-related issue detected (follow security team process) |

**Workflow modes:** When an existing fix is found (exit 10), the skill reports whether the
issue is MR-based or patch-based to guide the contributor on how to proceed.

## Commands

### Preflight (search only)

Search drupal.org for existing issues without generating a patch:

```bash
python3 scripts/contribute_fix.py preflight \
  --project metatag \
  --keywords "TypeError MetatagManager::build" \
  --paths "src/MetatagManager.php" \
  --out .drupal-contribute-fix
```

### Package (search + generate)

Search upstream AND generate contribution artifacts if appropriate:

```bash
# For web/ docroot layout:
python3 scripts/contribute_fix.py package \
  --root /path/to/drupal/site \
  --changed-path web/modules/contrib/metatag \
  --keywords "TypeError MetatagManager::build" \
  --out .drupal-contribute-fix

# For docroot/ layout (common in Acquia/BLT projects):
python3 scripts/contribute_fix.py package \
  --root /path/to/drupal/site \
  --changed-path docroot/modules/contrib/mcp \
  --keywords "module not installed" "update_get_available" \
  --out .drupal-contribute-fix
```

**Note:** `package` always runs `preflight` first and refuses to generate a patch
if an existing fix is found (unless `--force` is provided).

### Test (generate RTBC comment)

Generate a Tested-by/RTBC comment for an existing MR or patch you've tested:

```bash
python3 scripts/contribute_fix.py test \
  --issue 3345678 \
  --tested-on "Drupal 10.2, PHP 8.2" \
  --result pass \
  --out .drupal-contribute-fix
```

Options: `--result` can be `pass`, `fail`, or `partial`. Use `--mr` or `--patch`
to specify which artifact you tested.

### Reroll (patch for different version)

Reroll an existing patch that doesn't apply to your version:

```bash
python3 scripts/contribute_fix.py reroll \
  --issue 3345678 \
  --patch-url "https://www.drupal.org/files/issues/metatag-fix-3345678-15.patch" \
  --target-ref 2.0.x \
  --out .drupal-contribute-fix
```

This downloads the patch, attempts to apply it to your target branch, and generates
a rerolled patch if needed (or confirms it applies cleanly).

### Common Options

| Option | Description |
|--------|-------------|
| `--project` | Drupal project machine name (e.g., `metatag`, `drupal`) |
| `--keywords` | Error message fragments or search terms (space-separated) |
| `--paths` | Relevant file paths (space-separated) |
| `--out` | Output directory for artifacts |
| `--offline` | Use cached data only, don't hit API |
| `--force` | Override gatekeeper and generate patch anyway |
| `--issue` | Known issue number (runs gatekeeper check against this issue) |
| `--detect-deletions` | Include deleted files in patch (risky with Composer trees) |
| `--test-steps` | **REQUIRED** Specific test steps for the issue (agent must provide) |

### Test Steps (MANDATORY)

**Agents MUST provide specific test steps via `--test-steps`.** Generic placeholders are not acceptable.

```bash
python3 scripts/contribute_fix.py package \
  --changed-path docroot/modules/contrib/mcp \
  --keywords "update module not installed" \
  --test-steps \
    "Enable MCP module with Update module disabled" \
    "Call the general:status tool via MCP endpoint" \
    "Before patch: Fatal error - undefined function update_get_available()" \
    "After patch: JSON response with status unavailable" \
  --out .drupal-contribute-fix
```

Test steps should:
1. Describe how to set up the environment to reproduce the bug
2. Describe the action that triggers the bug
3. Describe the expected behavior BEFORE the patch (the bug)
4. Describe the expected behavior AFTER the patch (the fix)

## Output Files

```
.drupal-contribute-fix/
├── UPSTREAM_CANDIDATES.json              # Search results cache (shared)
├── 3541839-fix-metatag-build/            # Known issue
│   ├── REPORT.md                         # Analysis & next steps
│   ├── ISSUE_COMMENT.md                  # Paste-ready drupal.org comment
│   └── patches/
│       └── project-fix-3541839.patch
└── unfiled-update-module-check/          # New issue needed
    ├── REPORT.md
    ├── ISSUE_COMMENT.md
    └── patches/
        └── project-fix-new.patch
```

**Directory naming:**
- `{issue_nid}-{slug}/` - Existing issue matched or specified
- `unfiled-{slug}/` - No existing issue found

**Preflight vs Package:** `preflight` only updates `UPSTREAM_CANDIDATES.json`.
Issue directories are created by `package` when generating artifacts.

## Security Issue Handling

If the fix appears security-related, the skill will **STOP with exit code 50**.

Security indicators:
- Access bypass patterns
- User input reaching dangerous sinks (SQL, shell, eval)
- Authentication/session handling changes
- File system access control modifications

**Do NOT post security issues publicly.** Follow the Drupal Security Team process:
https://www.drupal.org/drupal-security-team/security-team-procedures

## Minimal + Upstream Acceptable

The skill enforces contribution best practices:

- **Warns** if patch touches >3 files or has large LOC changes
- **Separates** "must fix" from "nice-to-haves" (nice-to-haves excluded from patch)
- **Detects** patterns likely to be rejected:
  - Broad cache disables/bypasses
  - Swallowed exceptions
  - Access check bypasses
  - Environment-specific hacks

See [references/hack-patterns.md](references/hack-patterns.md) for details.

## Validation

The skill runs validation and reports results honestly:

- **Always runs:** `php -l` on changed PHP files
- **Runs if available:** PHPCS with Drupal standard
- **Never claims** tests passed if they weren't run

## After Completion - What To Tell The User

When you finish fixing the bug, **you MUST inform the user** about the contribution artifacts:

```
I've fixed the bug locally and generated contribution artifacts:

📁 .drupal-contribute-fix/<nid>-<slug>/
  - REPORT.md - Full analysis and next steps
  - ISSUE_COMMENT.md - Copy/paste this to drupal.org
  - patches/<patch-file>.patch - Upload this to the issue

**To contribute this fix upstream:**
1. Go to: https://www.drupal.org/node/<nid>
2. Paste the content from ISSUE_COMMENT.md as a new comment
3. Attach the patch file
4. Set status to "Needs review"
```

For unfiled issues (no existing drupal.org issue found):
```
📁 .drupal-contribute-fix/unfiled-<slug>/
  - Create a new issue at https://www.drupal.org/project/issues/<project>
  - Use ISSUE_COMMENT.md as the issue description template
  - Attach the patch file
```

**DO NOT skip this step.** The user may not know about the contribution workflow.

## References

- [references/issue-status-codes.md](references/issue-status-codes.md) - Drupal.org issue status mapping
- [references/patch-conventions.md](references/patch-conventions.md) - Patch naming and format
- [references/hack-patterns.md](references/hack-patterns.md) - Patterns to avoid

## Example Output

See [examples/sample-report.md](examples/sample-report.md) for a complete example.
