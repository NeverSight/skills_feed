---
name: kata-doctor
description: Run health checks on Kata project structure, detecting and fixing format issues. Triggers include "doctor", "health check", "fix roadmap", "check project", "kata doctor".
metadata:
  version: "1.8.0"
---
<objective>
Run diagnostic health checks on a Kata project and fix detected issues.

**Health Checks:**
1. **Roadmap format migration** — Detects old-format ROADMAP.md and migrates to current format
2. **Phase directory collision detection** — Detects duplicate numeric prefixes and migrates to globally sequential numbering

When invoked directly by user: run interactively with confirmation prompts.
When invoked by other skills (auto mode): format migration proceeds automatically, collision fix reports the problem and suggests `/kata-doctor` for interactive resolution.
</objective>

<execution_context>
@./references/roadmap-format-spec.md
</execution_context>

<context>
Mode: $ARGUMENTS (optional: --auto for non-interactive mode)

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>

<step name="parse_mode">

Parse arguments for mode:

```bash
AUTO_MODE=false
if echo "$ARGUMENTS" | grep -q "\-\-auto"; then
  AUTO_MODE=true
fi
```

</step>

<step name="display_banner">

Display diagnostic banner:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► PROJECT HEALTH CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running diagnostics...
```

</step>

## Check 1: Roadmap Format

<step name="check_roadmap_format">

Run format detection:

```bash
bash ./scripts/check-roadmap-format.sh 2>/dev/null
FORMAT_EXIT=$?
```

**Exit code handling:**
- `0` = Current format, skip migration
- `1` = Old format, needs migration  
- `2` = No ROADMAP.md, skip check

**If exit code 0:**

```
✓ ROADMAP.md format: current
```

Continue to Check 2.

**If exit code 2:**

```
— ROADMAP.md: not found (skipped)
```

Continue to Check 2.

**If exit code 1:**

```
⚠ ROADMAP.md format: old (needs migration)
```

Proceed to roadmap migration.

</step>

<step name="migrate_roadmap_format">

**Only runs if format check returned exit code 1.**

**Step 1: Parse old-format ROADMAP.md**

Read the existing ROADMAP.md and extract:
- Project name (from `# Roadmap:` or `#` heading)
- All phases with their numbers, names, status, plan counts
- Any milestone version references
- Phase completion dates if present

```bash
cat .planning/ROADMAP.md
```

**Step 2: Detect milestone boundaries**

Analyze phases to group them by milestone. Look for:
- Version references in phase goals or headers
- `<details>` blocks (already partially migrated)
- Completed vs in-progress phases

**Step 3: Build current-format structure**

Transform to canonical format per `roadmap-format-spec.md`:

1. Add `## Milestones` overview section with status icons
2. Wrap completed milestone phases in `<details>` blocks
3. Add `## Current Milestone:` heading for active work
4. Preserve all phase details and content

**Step 4: Write migrated ROADMAP.md**

Use Write tool to update `.planning/ROADMAP.md` with new format.

**Step 5: Verify migration**

```bash
bash ./scripts/check-roadmap-format.sh 2>/dev/null
VERIFY_EXIT=$?
```

**If exit code 0:**

```
✓ ROADMAP.md migrated to current format
```

**If still exit code 1:**

```
✗ ROADMAP.md migration failed - manual review needed
```

Display the file for user review.

**Step 6: Commit (if enabled)**

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=true`:**

```bash
git add .planning/ROADMAP.md
git commit -m "docs: migrate ROADMAP.md to current format"
```

</step>

## Check 2: Phase Directory Collisions

<step name="check_phase_collisions">

Scan for duplicate numeric prefixes across all phase state directories:

```bash
DUPES=$(for state in active pending completed; do
  ls .planning/phases/${state}/ 2>/dev/null
done | grep -oE '^[0-9]+' | sort -n | uniq -d)

# Also check flat directories (unmigrated projects)
FLAT_DUPES=$(ls .planning/phases/ 2>/dev/null | grep -E '^[0-9]' | grep -oE '^[0-9]+' | sort -n | uniq -d)

ALL_DUPES=$(echo -e "${DUPES}\n${FLAT_DUPES}" | sort -nu | grep -v '^$')
```

**If no duplicates:**

```
✓ Phase directories: no collisions
```

Continue to completion.

**If duplicates found:**

```
⚠ Phase directories: collisions detected
  Duplicate prefixes: [list]
```

**If AUTO_MODE=true:**

```
Collision fix requires user confirmation.
Run `/kata-doctor` interactively to resolve.
```

Exit without fixing.

**If AUTO_MODE=false:**

Proceed to collision migration.

</step>

<step name="migrate_phase_collisions">

**Only runs if collisions detected AND AUTO_MODE=false.**

This step incorporates the full logic from `kata-migrate-phases`:

**Step 1: Validate environment**

```bash
[ -f .planning/ROADMAP.md ] || { echo "ERROR: No ROADMAP.md found."; exit 1; }
[ -f .planning/STATE.md ] || { echo "ERROR: No STATE.md found."; exit 1; }
```

**Step 2: Build milestone chronology**

Parse ROADMAP.md to build globally sequential phase numbering:

```bash
GLOBAL_SEQ=0
CHRONOLOGY=""

while IFS= read -r line; do
  name=$(echo "$line" | grep -oE 'Phase [0-9.]+: .+' | sed 's/Phase [0-9.]*: //' | sed 's/\*\*$//' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
  if [ -n "$name" ]; then
    CHRONOLOGY="${CHRONOLOGY}${GLOBAL_SEQ} ${name}\n"
    GLOBAL_SEQ=$((GLOBAL_SEQ + 1))
  fi
done < <(grep -E 'Phase [0-9.]+:' .planning/ROADMAP.md)
```

Display: `Chronology ([N] phases): 00 → foundation, 01 → api-endpoints, ...`

**Step 3: Map directories to phases**

For each chronology entry, find matching directory across all states.
Build mapping: `STATE/OLD_DIR → STATE/NEW_PREFIX-SLUG`

**Step 4: Present migration plan**

```
Migration Plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  completed/01-foundation      → completed/00-foundation
  completed/02-api-endpoints   → completed/01-api-endpoints
  completed/01-setup           → completed/02-setup
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: [N] directories to rename
```

Use AskUserQuestion:
- header: "Migration"
- question: "Rename [N] directories to globally sequential numbers?"
- options:
  - "Proceed" — Execute all renames
  - "Cancel" — Abort migration

If cancelled: exit with "Migration cancelled."

**Step 5: Execute two-pass rename**

**Pass 1:** Rename all directories to temporary names: `mv OLD tmp-{seq}-{slug}`

**Pass 2:** Rename from temporary to final: `mv tmp-{seq}-{slug} {padded}-{slug}`

For active/pending phases, also rename internal files (`*-PLAN.md`, `*-RESEARCH.md`, etc.).

**Step 6: Update documentation**

Update ROADMAP.md current milestone phase numbers.
Update STATE.md current position.
Leave historical `<details>` blocks unchanged.

**Step 7: Verify**

Re-run collision detection:

```bash
DUPES=$(for state in active pending completed; do
  ls .planning/phases/${state}/ 2>/dev/null
done | grep -oE '^[0-9]+' | sort -n | uniq -d)
```

**If clean:**

```
✓ Phase directories migrated to globally sequential numbers
✓ No duplicate prefixes remain
```

**Step 8: Commit**

```bash
COMMIT_PLANNING_DOCS=$(cat .planning/config.json 2>/dev/null | grep -o '"commit_docs"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "true")
git check-ignore -q .planning 2>/dev/null && COMMIT_PLANNING_DOCS=false
```

**If `COMMIT_PLANNING_DOCS=true`:**

```bash
git add .planning/phases/ .planning/ROADMAP.md .planning/STATE.md
git commit -m "chore: migrate phase directories to globally sequential numbering"
```

</step>

## Completion

<step name="completion">

Display completion summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Kata ► HEALTH CHECK COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[List each check with status]

✓ ROADMAP.md format: [current | migrated | not found]
✓ Phase directories: [no collisions | migrated | skipped]
```

**If any migrations were performed:**

```
Changes committed. Run `/kata-track-progress` to continue.
```

</step>

</process>

<anti_patterns>
- Don't modify historical `<details>` blocks content (only add if missing)
- Don't rename completed phase internal files during collision fix
- Don't run collision fix in auto mode without user confirmation
- Don't fail the entire health check if one check has issues
</anti_patterns>

<success_criteria>
- [ ] Roadmap format detected correctly (current/old/missing)
- [ ] Old-format roadmaps migrated to current format
- [ ] Migrated format verified with check script
- [ ] Phase collisions detected across all state directories
- [ ] Collision migration uses two-pass rename (no mid-rename collisions)
- [ ] Documentation updated after collision migration
- [ ] Changes committed (if commit_docs enabled)
- [ ] Auto mode skips collision fix with informative message
- [ ] User informed of all check results
</success_criteria>
