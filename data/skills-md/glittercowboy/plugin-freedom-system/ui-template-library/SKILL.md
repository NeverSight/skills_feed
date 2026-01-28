---
name: ui-template-library
description: Manage aesthetic templates - save visual systems from completed mockups as interpretable prose, apply to new plugins with adaptive layouts
allowed-tools:
  - Read
  - Write
  - Bash
preconditions:
  - .claude/aesthetics/ directory exists (created by system-setup skill or auto-created on first save_aesthetic)
---

# ui-template-library Skill

**Purpose:** Capture and apply aesthetic "vibes" across plugins using structured prose descriptions rather than rigid specifications.

---

## Operations

**You MUST determine which operation the user is requesting, then execute ONLY that operation.**

**Operation Routing** (match user request to keywords):
- save/capture/extract → **save_aesthetic** (Operation 1)
- apply/use/generate → **apply_aesthetic** (Operation 2)
- list/show/browse → **list_aesthetics** (Operation 3)
- delete/remove → **delete_aesthetic** (Operation 4)
- update/modify/refine → **update_aesthetic** (Operation 5)

1. **save_aesthetic** - Analyze mockup HTML and generate structured prose aesthetic.md
2. **apply_aesthetic** - Interpret aesthetic.md to generate new mockup with appropriate layout
3. **list_aesthetics** - Show all saved aesthetics with prose summaries
4. **delete_aesthetic** - Remove aesthetic from library
5. **update_aesthetic** - Refine aesthetic.md from improved mockup

---

## CRITICAL: Checkpoint Verification Protocol

**Before presenting decision menu in ANY operation:**

ALL steps must complete successfully. If ANY step fails: HALT, report specific error, DO NOT proceed to decision menu.

**Verification checklist** (run before showing menu):
- [ ] All required files created successfully
- [ ] File contents are valid (aesthetic.md not empty, metadata.json valid JSON)
- [ ] manifest.json updated successfully
- [ ] Git commit completed (if applicable)
- [ ] No error states from previous steps

**Error handling**:
- Steps 1-6 fail → Report error, do not create partial aesthetic directory
- Step 7 fails (manifest) → Aesthetic files exist but not registered, offer retry
- Step 7.5 fails (git) → Non-fatal, warn "Aesthetic saved but not committed"

**Note**: Always use inline numbered menus (NOT AskUserQuestion tool) to maintain consistency with system-wide Checkpoint Protocol.

---

## Directory Structure

```text
.claude/aesthetics/
├── manifest.json                    # Registry of all aesthetics
└── [aesthetic-id]/
    ├── aesthetic.md                 # Structured prose description (THE SOURCE OF TRUTH)
    ├── preview.html                 # Visual reference (original mockup)
    └── metadata.json                # Name, description, source plugin, tags
```

**Key change from previous system:**
- **aesthetic.yaml → aesthetic.md**: YAML specs replaced with structured prose descriptions
- Format is consistent and parseable, but content is interpretable concepts, not rigid values

---

<operation name="save_aesthetic">
  <purpose>Capture visual design from mockup as structured prose aesthetic.md</purpose>

  <critical_sequence>
    <step id="-1" required="true">
      Initialize .claude/aesthetics/ directory if missing (mkdir -p)
    </step>
    <step id="0" required="true" depends_on="-1">
      Validate mockup file exists and is readable
    </step>
    <step id="1" required="true" depends_on="0">
      Read mockup HTML file into memory (Read tool)
    </step>
    <step id="2" required="true" depends_on="1">
      Extract visual patterns using pattern-extraction.md strategies
    </step>
    <step id="3" required="true" depends_on="2">
      Generate prose descriptions using prose-generation.md guidelines
    </step>
    <step id="4" required="true" depends_on="3">
      Write aesthetic.md following aesthetic-template.md structure exactly: same section headers in same order, fill all sections with prose (no placeholders) (load template from assets/aesthetic-template.md, if missing: report critical error)
    </step>
    <step id="5" required="true" depends_on="4">
      Copy preview.html to aesthetic directory
    </step>
    <step id="6" required="true" depends_on="5">
      Generate metadata.json with inferred tags
    </step>
    <step id="7" required="true" depends_on="6">
      Update manifest.json using Read → modify → Write pattern (if missing: initialize from assets/manifest-init.json)
    </step>
    <step id="7.5" required="true" depends_on="7">
      Commit aesthetic to git using conventional format
    </step>
    <step id="8" required="true" depends_on="7.5">
      Present confirmation + decision menu
    </step>
  </critical_sequence>

  <state_requirement>
    See "CRITICAL: Checkpoint Verification Protocol" section for complete verification requirements.
  </state_requirement>
</operation>

## Operation 1: save_aesthetic

**See:** [references/save-operation.md](references/save-operation.md) for complete 8-step workflow.

---

<operation name="apply_aesthetic">
  <purpose>Generate new mockup by interpreting aesthetic prose and adapting to target plugin</purpose>

  <critical_sequence>
    <step id="1" required="true">
      Load aesthetic.md and metadata.json (Read tool)
    </step>
    <step id="2" required="true">
      Read target plugin parameter-spec.md or creative-brief.md
    </step>
    <step id="3" required="true" depends_on="1,2">
      Interpret aesthetic prose using aesthetic-interpretation.md strategies
    </step>
    <step id="4" required="true" depends_on="3">
      Choose layout based on parameter count (layout-generation.md)
    </step>
    <step id="5" required="true" depends_on="3,4">
      Generate HTML/CSS applying aesthetic to chosen layout
    </step>
    <step id="6" required="true" depends_on="5">
      Save generated mockup to target plugin mockups directory
    </step>
    <step id="7" required="true" depends_on="6">
      Update aesthetic metadata.json usedInPlugins array
    </step>
    <step id="8" required="true" depends_on="7">
      Present decision menu as inline numbered list, NOT AskUserQuestion tool (rationale: consistent with system-wide Checkpoint Protocol - see CLAUDE.md)
    </step>
  </critical_sequence>

  <decision_gate wait_required="true">
    Present decision menu with preview/continue options
    MUST wait for user response
  </decision_gate>
</operation>

## Operation 2: apply_aesthetic

**See:** [references/apply-operation.md](references/apply-operation.md) for complete 8-step workflow.

---

<operation name="list_aesthetics">
  <critical_sequence>
    <step id="1" required="true">Read manifest.json</step>
    <step id="2" required="true">Format as markdown table</step>
    <step id="3" required="true">Show preview paths</step>
    <step id="4" required="true">Present decision menu</step>
  </critical_sequence>

  <decision_gate wait_required="true">
    Wait for user to select action from menu
  </decision_gate>
</operation>

## Operation 3: list_aesthetics

Display all saved aesthetics in table format with preview paths.
**See:** [references/list-operation.md](references/list-operation.md) for complete 4-step workflow.

---

## Operation 4: delete_aesthetic

Remove aesthetic from library with confirmation.
**See:** [references/delete-operation.md](references/delete-operation.md) for complete 4-step workflow.

---

## Operation 5: update_aesthetic

Refine aesthetic.md from improved mockup while preserving user edits.
**See:** [references/update-operation.md](references/update-operation.md) for complete 7-step workflow.

---

## API Contract

This skill provides operations for managing aesthetic templates. Called by ui-mockup skill.

**save_aesthetic(mockup_path, plugin_name, aesthetic_name?)**:
- **Input**: Absolute path to mockup HTML, plugin name, optional aesthetic name
- **Output**: aesthetic_id (string), aesthetic_path (absolute path)
- **Process**: Analyzes mockup, generates aesthetic.md prose, saves to .claude/aesthetics/

**apply_aesthetic(aesthetic_id, plugin_name, parameter_spec_path)**:
- **Input**: Aesthetic ID, target plugin name, path to parameter-spec.md
- **Output**: mockup_path (absolute path to generated mockup)
- **Process**: Loads aesthetic prose, interprets to CSS, generates mockup with appropriate layout

**Invocation**: Inline invocation from ui-mockup (both skills are lightweight and stateless).

---
## Success Criteria

**Save operation successful when:**
- ✅ aesthetic.md generated following exact template structure
- ✅ All sections filled with interpretable prose (no placeholders)
- ✅ Example color codes provided as concrete reference
- ✅ preview.html copied to aesthetic directory
- ✅ metadata.json created with tags and source info
- ✅ manifest.json updated with new aesthetic entry
- ✅ Format is idempotent (same mockup → same structure every time)

**Apply operation successful when:**
- ✅ aesthetic.md parsed and interpreted correctly
- ✅ Appropriate layout chosen for parameter count
- ✅ Generated mockup reflects aesthetic visual language
- ✅ Control styling matches prose descriptions
- ✅ Colors, typography, spacing consistent with aesthetic
- ✅ WebView constraints enforced (no viewport units, etc.)
- ✅ Result is recognizably the same aesthetic despite different layout

**List operation successful when:**
- ✅ All aesthetics shown in readable table
- ✅ Vibe summaries extracted from prose
- ✅ Preview paths provided for visual reference
- ✅ Decision menu presented for next action

---

## Implementation Notes

Technical details about parsing, quality control, and constraints.
**See:** [references/implementation-notes.md](references/implementation-notes.md) for complete technical documentation.

---

## Reference Documentation

- **Pattern extraction:** `references/pattern-extraction.md` - String/regex strategies for extracting visual patterns from HTML
- **Prose generation:** `references/prose-generation.md` - Guidelines for transforming patterns into interpretable prose
- **Aesthetic interpretation:** `references/aesthetic-interpretation.md` - Strategies for parsing prose and generating CSS/HTML
- **Layout generation:** `references/layout-generation.md` - Layout decision trees and control placement strategies

---

## Template Assets

- **Aesthetic template:** `assets/aesthetic-template.md` - Complete structured prose template (THE FORMAT SPEC)
- **Metadata template:** `assets/metadata-template.json` - Metadata JSON structure
- **Manifest init:** `assets/manifest-init.json` - Empty manifest structure for initialization
