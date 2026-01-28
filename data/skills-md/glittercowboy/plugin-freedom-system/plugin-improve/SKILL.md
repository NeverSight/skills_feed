---
name: plugin-improve
description: Fix bugs, add features to completed plugins. Includes versioning, backups, regression testing, changelog automation. Auto-detects deep-research handoffs to preserve investigation context. Trigger terms - improve, fix, add feature, modify plugin, version bump, rollback
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task # For deep-research (Tier 3) and plugin-testing (regression tests)
preconditions:
  - Plugin status must be ✅ Working OR 📦 Installed
  - Plugin must NOT be 🚧 In Development
---

# plugin-improve Skill

**Purpose:** Make changes to completed plugins with versioning, backups, changelog automation, and root cause investigation.

**Integration with deep-research:**

<handoff_protocol>
**Trigger:** deep-research invokes plugin-improve via Skill tool
**Detection:** Phase 0.45 scans conversation history for research findings (MANDATORY)
**Action:** Extract research findings, skip investigation (Phase 0.5)
**Benefits:** Preserve expensive research context (Opus + extended thinking)
</handoff_protocol>

Detection mechanism is implemented in Phase 0.45 below. See `references/handoff-protocols.md` for additional workflow documentation.

## Workflow Overview

```
Phase 0: Specificity Detection (assess request clarity)
  ↓
[Specific?] ─NO→ Present menu (brainstorm OR investigate)
  ↓ YES
Phase 0.3: Clarification Questions (4 targeted questions)
  ↓
Phase 0.4: Decision Gate (confirm understanding)
  ↓
Phase 0.45: Research Detection (MANDATORY - scan conversation history)
  ↓
[Research found?] ─YES→ Skip to Phase 0.9
  ↓ NO
Phase 0.5: Investigation (Tier 1/2/3 auto-detected)
  ↓
Phase 0.9: Backup Verification (CRITICAL GATE - must pass to proceed)
  ↓
Phase 1: Pre-Implementation Checks (version, state, commits)
  ↓
Phase 2: Verify Rollback Path (confirm backup ready)
  ↓
Phase 3: Implementation (make changes)
  ↓
Phase 4: CHANGELOG Update (document changes)
  ↓
Phase 5: Build and Test (delegate to build-automation)
  ↓
Phase 5.5: Regression Testing (conditional: if plugin-testing + baseline exist)
  ↓
Phase 6: Git Workflow (stage changes, prepare commit)
  ↓
Phase 7: Installation (optional, delegate to plugin-lifecycle)
  ↓
Phase 8: Completion (decision menu)
```

**Key:**
- MANDATORY: Always executes (Phase 0.45)
- CRITICAL GATE: Blocks workflow if fails (Phase 0.9)
- CONDITIONAL: Only if conditions met (Phase 5.5, Phase 7)

## Progress Checklist

Copy this checklist and check off phases as you complete them:

```
Improvement Progress:
- [ ] Phase 0: Assessed request specificity
- [ ] Phase 0.3: Asked clarification questions (if needed)
- [ ] Phase 0.4: Confirmed understanding with user
- [ ] Phase 0.45: ✓ MANDATORY - Scanned conversation history for research
- [ ] Phase 0.5: Investigated root cause (if no handoff)
- [ ] Phase 0.9: ✓ CRITICAL - Backup verified (blocks if fails)
- [ ] Phase 1: Loaded current state, determined version bump
- [ ] Phase 2: Confirmed rollback path ready
- [ ] Phase 3: Implemented changes
- [ ] Phase 4: Updated CHANGELOG
- [ ] Phase 5: Built and tested (delegated to build-automation)
- [ ] Phase 5.5: Ran regression tests (if available)
- [ ] Phase 6: Staged git changes
- [ ] Phase 7: Installed plugin (if requested)
- [ ] Phase 8: Presented completion menu
```

<gate_preconditions enforcement="strict">
## Precondition Checking

**MUST execute before any other phase. BLOCK if conditions not met.**

**Before starting, verify:**

1. Read PLUGINS.md:

```bash
grep "^### $PLUGIN_NAME$" PLUGINS.md
```

2. Check status:
   - If status = ✅ Working or 📦 Installed → OK to proceed
   - If status = 🚧 In Development → BLOCK with message:
     ```
     [PluginName] is still in development (Stage [N]).
     Complete the workflow first with /continue [PluginName].
     Cannot use /improve on in-progress plugins.

     Note: The workflow now has 3 stages with automatic validation.
     Stage 1-3 complete = plugin ready for improvement.
     ```
   - If status = 💡 Ideated → BLOCK with message:
     ```
     [PluginName] is not implemented yet (Status: 💡 Ideated).
     Use /implement [PluginName] to build it first.
     ```
   - If not found → BLOCK with message:
     ```
     Plugin [PluginName] not found in PLUGINS.md.
     ```

</gate_preconditions>

## Phase 0: Specificity Detection

**Check if request is specific:**

Request IS specific if it has:

- Feature name (e.g., "resonance parameter", "bypass switch")
- Action (e.g., "add", "remove", "fix", "change from X to Y")
- Acceptance criteria (e.g., "range 0-1", "increase to 500px", "reduce by 3dB")

Request IS vague if lacking above:

- "improve the filters"
- "better presets"
- "UI feels cramped"
- "make it sound warmer"

**Assess specificity:**

- **Specific enough (1-2 clarification questions max):** Proceed to Phase 0.3 (4-question clarification batch)
- **Vague:** Present inline decision menu:

```
Your request needs more detail. How should I proceed?

1. Brainstorm approaches together - I'll ask questions to explore options
2. Implement something reasonable - I'll investigate and propose a solution
3. Other

Choose (1-3): _
```

**Handle responses:**
- Option 1 → Invoke plugin-ideation skill in improvement mode
- Option 2 → Proceed to Phase 0.45 (Research Detection)
- Option 3 → Collect free-form text, reassess

## Phase 0.2: Headless Plugin Detection (GUI-Optional Flow)

**Purpose:** Detect headless plugins and offer "Create custom UI" option before proceeding to normal improvement flow.

**Workflow:**

1. Read .continue-here.md and check `gui_type` field
2. If `gui_type: headless` OR WebView UI files don't exist → Plugin is headless
3. If headless, present 4-option menu: Create UI, Keep headless, Explain headless, Other
4. If "Create UI" selected → Invoke ui-mockup skill, then gui-agent subagent
5. Update version to v1.1.0 (MINOR bump - new feature)
6. Update state files and commit changes

**See**: [references/headless-ui-workflow.md](references/headless-ui-workflow.md) for complete detection logic, menu flows, gui-agent invocation, state updates, and completion protocol.

**If NOT headless:** Skip to Phase 0.3 (normal flow)

## Phase 0.3: Clarification Questions (If Specific)

**See**: [references/clarification-protocol.md](references/clarification-protocol.md) for 4 targeted questions (what to change, scope, version bump, testing approach). Collect all responses before proceeding to Phase 0.4.

## Phase 0.4: Decision Gate

**Show user what you understand, ask for confirmation:**

```
I understand you want to:
- [Summary of change from Question 1]
- Scope: [Answer from Question 2]
- Version bump: [Answer from Question 3]
- Regression testing: [Answer from Question 4]

Is this correct?

1. Yes, proceed - Continue to Phase 0.45 (Research Detection)
2. No, refine - Ask me follow-up questions
3. No, cancel - Stop the workflow
4. Other

Choose (1-4): _
```

**Handle responses:**
- Option 1 → Proceed to Phase 0.45
- Option 2 → Return to Phase 0.3, ask follow-up questions
- Option 3 → Stop workflow, wait for new instruction
- Option 4 → Collect free-form text, reassess

## Phase 0.45: Research Detection

**MANDATORY**: Scan conversation history for deep-research findings to avoid duplicate investigation.

**See**: [references/research-detection.md](references/research-detection.md) for complete detection algorithm, extraction logic, and decision trees.

**Decision**: If research detected → Skip to Phase 0.9 | If not detected → Continue to Phase 0.5

## Phase 0.5: Investigation (Auto-Tiered)

**Purpose:** Find root causes, prevent band-aid fixes

**Workflow:**

1. Analyze request and auto-detect tier (1/2/3) - never ask user which tier
2. Execute tier-appropriate investigation protocol
3. For Tier 3 (complex issues), delegate to deep-research skill
4. Present findings and wait for approval before implementing

**See**: [references/investigation-tiers.md](references/investigation-tiers.md) for complete tier detection algorithm and protocols for each tier (1: Basic Code Inspection, 2: Root Cause Analysis, 3: Deep Research Delegation).

<critical_sequence phase="backup-verification" enforcement="strict">
## Phase 0.9: Backup Verification

**CRITICAL INVARIANT:** Phase 1 MUST NOT execute until backup verified.
**ENFORCEMENT:** Block execution, halt workflow if backup fails.
**VIOLATION CONSEQUENCE:** Data loss, no rollback path.

**Goal:** Ensure rollback is possible if improvement fails

**Process:**
1. Check if backup exists at `backups/[PluginName]/v[CurrentVersion]/`
2. If missing, create backup using rsync (exclude build/ and build.log)
3. Verify backup integrity: `./scripts/verify-backup.sh [PluginName] [CurrentVersion]`
4. If verification fails, HALT workflow with error message
5. If verification succeeds, present confirmation and proceed

**See**: [assets/backup-template.sh](assets/backup-template.sh) for complete backup creation script.

</critical_sequence>

<phase id="1" name="pre-implementation" dependencies="backup-verification">
## Phase 1: Pre-Implementation Checks

**DEPENDENCY:** MUST NOT execute until Phase 0.9 (Backup Verification) completes.

**Load current state (parallelize file reads):**

Read these files in parallel using multiple Read tool calls:
1. CHANGELOG.md - Extract current version (e.g., v1.2.3)
2. PLUGINS.md - Get plugin entry for additional context
3. Git log - Check recent commits: `git log --oneline plugins/[PluginName]/ -10`

**Determine version bump:**

Present choice:

```
Current version: v[X.Y.Z]

What type of change is this?
1. PATCH (v[X.Y.Z] → v[X.Y.Z+1]) - Bug fixes, cosmetic changes
2. MINOR (v[X.Y] → v[X.Y+1]) - New features, enhancements
3. MAJOR (v[X] → v[X+1]) - Breaking changes (presets won't load, parameters changed)

Choose (1-3): _
```

**If Major version selected, warn:**

```
⚠️ Major version bump will break compatibility.

Breaking changes include:
- Changed parameter IDs (presets won't load)
- Removed parameters (sessions will have missing automation)
- Changed state format (existing sessions corrupted)

Are you sure? This should be rare. (y/n): _
```

Calculate new version based on selection.

### Breaking Change Detection

Check for breaking changes BEFORE confirming version bump:

**Breaking if:**
- ❌ Parameter ID renamed (automation breaks)
- ❌ Parameter range changed (saved values invalid)
- ❌ Parameter removed (automation breaks)
- ❌ Parameter type changed (e.g., float → choice)
- ❌ State format changed (old presets won't load)
- ❌ Feature removed (users lose functionality)
- ❌ Public API signature changed

**If breaking changes detected:** Force MAJOR version bump, warn user, require confirmation.

**See**: [references/breaking-changes.md](references/breaking-changes.md) for detailed detection criteria and edge cases.

</phase>

<critical_sequence phase="backup-creation" enforcement="strict">
## Phase 2: Verify Rollback Path

**Baseline backup verified in Phase 0.9. Confirm ready to proceed:**

```
✓ Backup verified: backups/[PluginName]/v[CurrentVersion]/
Ready to implement changes for v[NewVersion]
```

</critical_sequence>

<phase id="3" name="implementation" dependencies="backup-creation">
## Phase 3: Implementation

**DEPENDENCY:** MUST NOT execute until Phase 2 (Backup Creation) completes.
**SAFETY:** If implementation fails, rollback path guaranteed by Phase 2 backup.

**Execute the change:**

1. Modify source files according to investigation findings
2. Update build configuration if needed (CMakeLists.txt)
3. Adjust UI if required (PluginEditor.cpp)
4. Update parameter definitions if needed (PluginProcessor.cpp)

**Follow best practices:**

- Real-time safety in processBlock
- No allocations in audio thread
- Thread-safe parameter access
- JUCE API correctness

**Log changes as you go for CHANGELOG.**

</phase>

## Phase 4: CHANGELOG Update

**Add version entry at top of CHANGELOG.md with technical details:**

**Required fields:**
- Date in ISO format (YYYY-MM-DD)
- Root cause for fixes (from Phase 0.5 investigation)
- Testing notes (regression test results if Phase 5.5 ran)

**Sections by version type:**
- **PATCH (0.0.X):** Use "Fixed" section primarily
- **MINOR (0.X.0):** Use "Added" and/or "Changed" sections
- **MAJOR (X.0.0):** Include "Breaking Changes" and "Migration Notes"

**See**: [references/changelog-format.md](references/changelog-format.md) for complete template structure, section usage guide, and examples by version type (PATCH/MINOR/MAJOR).

<delegation_rule target="build-automation" required="true">
## Phase 5: Build and Test

**DELEGATION:** MUST invoke build-automation skill for all build operations.
**REASON:** Centralized build logic, 7-phase pipeline with verification.

**1. Build:** Invoke build-automation skill - handles full build pipeline, installation, cache clearing, and failure protocol.

**2. Test:** After build succeeds, invoke plugin-testing skill - present 4-option menu (automated tests, pluginval, manual DAW testing, skip).

</delegation_rule>

<validation_gate gate="regression-tests" required="conditional">
## Phase 5.5: Regression Testing

**GATE CONDITION:** Conditional - only runs if both conditions met
**GATE FAILURE:** Present rollback options, require user decision

**Conditions required:**
1. plugin-testing skill exists
2. Baseline backup exists at `backups/[Plugin]/v[baseline]/`

**If conditions not met:** Skip regression tests, warn user, add note to CHANGELOG, continue to Phase 6.

**If conditions met:**
1. Build baseline version from backup
2. Run plugin-testing on baseline (capture results)
3. Run plugin-testing on current version (capture results)
4. Compare results and present findings with decision menu

**See**: [references/regression-testing.md](references/regression-testing.md) for complete RegressionReport interface, comparison logic, and rollback decision trees.

</validation_gate>

## Phase 6: Git Workflow

**Stage changes:** `git add plugins/[PluginName]/ backups/[PluginName]-v[X.Y.Z]-[timestamp]/`

**Commit format:** `improve: [PluginName] v[X.Y.Z] - [description]`

**Tag release:** `git tag -a "v[X.Y.Z]" -m "[PluginName] v[X.Y.Z]"`

**Note:** Display git commands for user to run manually. Do not execute git commit or git push.

<delegation_rule target="plugin-lifecycle" required="false">
## Phase 7: Installation (Optional)

**If user requested installation:** Invoke plugin-lifecycle skill, then update PLUGINS.md and NOTES.md (version, status, timeline entry).

</delegation_rule>

<checkpoint_protocol>
## Phase 8: Completion

**Present numbered decision menu (inline format, NOT AskUserQuestion tool):**

Options: Test in DAW, Make another improvement, Create new plugin, Document this change, Other

</checkpoint_protocol>

## Version History

**Phase 7 enhancements (2025-11):**
- Regression testing integration (Phase 5.5)
- Enhanced changelog format (Phase 4)
- Backup verification protocol (Phase 0.9)
- One-command rollback mechanism
- Breaking change detection

**See:** `architecture/17-testing-strategy.md`, `scripts/verify-backup.sh`, `references/regression-testing.md`

## Integration Points

**Invoked by:**

- `/improve` command
- Natural language: "Fix [plugin]", "Add [feature] to [plugin]"
- `plugin-ideation` skill (after improvement brief)

**Invokes:**

- `plugin-ideation` skill (if vague request, user chooses brainstorm)
- `deep-research` skill (Tier 3 investigation) - Phase 7
- `build-automation` skill (building) - Phase 4
- `plugin-testing` skill (validation)
- `plugin-lifecycle` skill (installation)

**Updates:**

- CHANGELOG.md (adds version entry)
- PLUGINS.md (table row: version, last updated, status)
- plugins/[Name]/NOTES.md (status, version, timeline entries, known issues)
- Source files (implementation changes)

**Creates:**

- Backup in `backups/[PluginName]-v[X.Y.Z]-[timestamp]/`
- Git tag `v[X.Y.Z]`

## Error Handling

**Build failure:**
Present investigation menu, wait for user decision.

**Test failure:**
Present investigation menu, don't proceed to installation.

**Breaking change detected:**
Warn user, require confirmation, force MAJOR version.

**Backup creation fails:**
STOP immediately, don't proceed with changes.

**Git operations fail:**
Log warning, continue (non-critical).

## Success Criteria

Improvement is successful when:

- Root cause investigated (not band-aid fix)
- Backup created before changes
- Changes implemented correctly
- CHANGELOG updated with version entry
- Build succeeds without errors
- Tests pass
- Git staged with conventional commit message
- PLUGINS.md table row updated (version, status, last updated)
- NOTES.md updated (status, version, timeline entry)
- User knows how to rollback if needed
