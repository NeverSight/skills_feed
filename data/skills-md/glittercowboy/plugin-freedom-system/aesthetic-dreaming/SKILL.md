---
name: aesthetic-dreaming
description: Create aesthetic templates without first creating a plugin - capture visual design concepts through adaptive questioning. Use when you want to build a library of visual systems before plugin implementation.
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - Skill
preconditions:
  - None (entry point)
---

# aesthetic-dreaming Skill

**Purpose:** Create aesthetic templates before implementing any plugins. Capture visual design systems through adaptive questioning, generate structured aesthetic.md, and optionally create test previews demonstrating the aesthetic across different plugin types.

**Solves:** The friction of needing to create a full plugin just to design and save an aesthetic template. Build a library of visual design systems first, apply them later.

---

<workflow_overview>
<critical_sequence enforcement="strict">
This workflow MUST execute phases in order. Do NOT skip phases or proceed to finalization before completing gap analysis and question batches.

**Phase Flow:**
1. **Phase 1: Free-form collection** - Gather initial aesthetic vision
2. **Phase 2: Gap analysis** - Identify missing visual elements
3. **Phase 3: Question batch** - Ask 4 contextual questions via AskUserQuestion
4. **Phase 3.5: Decision gate** - Finalize / Continue / Add context
5. **Phase 3.7: Name aesthetic** (if finalizing)
6. **Phase 4: Test preview selection**
7. **Phase 5: Generate files**
8. **Phase 6: Decision menu**

**Loop Structure:**
Phases 2-3-3.5 repeat until user chooses "finalize" at decision gate.

**Critical Rules:**
- Do NOT skip phases
- Do NOT execute phases out of order
- Do NOT proceed to finalization before decision gate approval
- NEVER auto-proceed past decision gates
</critical_sequence>
</workflow_overview>

---

<phase id="1" name="free_form_collection">
<instructions>
Present open invitation to user. Extract all mentioned visual concepts verbatim and accumulate in context.
</instructions>

<required_prompt>
What aesthetic are you envisioning?

Describe the visual design system you want to create—share as much or as little as you want. I'll ask follow-ups for anything missing.

Consider: overall vibe, color palette, control styling, spacing, textures, typography, and plugin types this would suit.

You can reference existing designs, describe feelings, or provide technical specifics.
</required_prompt>

<extraction_targets>
- Visual Identity: Overall vibe, mood, design philosophy
- Color System: Palette, warm/cool, contrast, specific colors
- Typography: Font choices, sizing philosophy
- Control Styling: Knobs, sliders, buttons, rotaries
- Spacing: Density, breathing room, layout approach
- Surface Treatment: Textures, shadows, depth, glossy vs. matte
- Details: Special features, animations, microinteractions
- Best For: Plugin types, use cases
- Inspirations: References to existing designs
</extraction_targets>

<state_requirement>
**Context Storage**: Maintain cumulative context as structured object in agent memory throughout all phases and question batches. Format: key-value pairs for each design dimension (vibe, color_philosophy, control_style, typography, spacing, etc.). NEVER overwrite existing keys - only append new information. NEVER lose information from previous phases.
</state_requirement>
</phase>

---

<phase id="2" name="gap_analysis">
<critical_sequence>
1. Parse user's accumulated context (from Phase 1 + any previous question batches)
2. Check coverage against tier priority system
3. Identify top 4 gaps by tier priority
4. NEVER ask about already-provided information
</critical_sequence>

<tier_system>
**Tier 1 (Critical):** Overall vibe/mood, color philosophy, control style
**Tier 2 (Visual Core):** Specific colors, typography, spacing, textures, control details
**Tier 3 (Context):** Best suited for, special features, inspirations
</tier_system>

<anti_pattern>
NEVER ask redundant questions. If user stated "dark modern blue", do NOT ask:
- "What's the overall vibe?" (modern already stated)
- "Light or dark?" (dark already stated)
- "What accent color?" (blue already stated)

Instead focus on uncovered gaps: typography, spacing, textures, plugin types.
</anti_pattern>

<delegation_rule>
Detailed question banks are in references/aesthetic-questions.md. Reference for gap analysis strategies and question options.
</delegation_rule>
</phase>

---

<phase id="3" name="question_batch">
<instructions>
Generate exactly 4 questions using AskUserQuestion tool based on gaps identified in Phase 2.
</instructions>

<requirements>
- MUST use AskUserQuestion tool (not inline menu)
- Provide 3-4 meaningful options per question (not just open text)
- Always include "Other" option for custom input
- Users can type "skip" in "Other" to skip questions
- Questions MUST target identified gaps, prioritized by tier
</requirements>

<tool_usage>
Tool: AskUserQuestion
Parameters:
  - questions: array[1-4] of question objects
  - Each question has: question, header, multiSelect, options[2-4]
  - Always include "Other" option automatically
</tool_usage>

<example>
See references/question-examples.md for detailed AskUserQuestion formatting examples and question banks by category.
</example>

<state_transition>
After receiving question batch answers:
1. Merge answers into accumulated context object by appending to relevant keys (e.g., answer "Dark with blue accents" → context.color_philosophy = "Dark with blue accents"). Preserve all previous keys. Never overwrite existing information.
2. Proceed DIRECTLY to decision gate (Phase 3.5)
3. Decision gate will route to Phase 2 (re-analyze) or Phase 3.7 (finalize)
</state_transition>
</phase>

---

<decision_gate id="finalize_or_continue" phase="3.5">
<critical_sequence>
MUST present this decision gate after EVERY question batch (Phase 3).
MUST use inline numbered list format (consistent with checkpoint protocol).
MUST wait for user response before proceeding.
</critical_sequence>

<required_menu>
Ready to finalize the aesthetic concept?

1. Yes, finalize it - Create aesthetic.md and optional previews
2. Ask me 4 more questions - Continue refining the design
3. Let me add more context first - Provide additional details before questions

Choose (1-3): _
</required_menu>

<routing_logic>
IF option 1 THEN proceed to Phase 3.7
ELSE IF option 2 THEN return to Phase 2 (with accumulated context)
ELSE IF option 3 THEN collect user input, merge with context, return to Phase 2
</routing_logic>

<state_requirement>
Context accumulation is cumulative across all iterations. Never lose previously collected information.
</state_requirement>
</decision_gate>

---

<phase id="3.7" name="name_aesthetic">
<preconditions>
Only execute if user chose "finalize" at decision gate (Phase 3.5).
</preconditions>

<conditional_execution>
IF aesthetic name already provided in initial description THEN skip this phase and proceed to Phase 4.
ELSE ask user for name via AskUserQuestion with 3 suggested names + "Other" option.
</conditional_execution>

<name_generation_rules>
- Suggest 3 names based on accumulated context (vibe + colors + style)
- Examples: "Dark modern blue" → "Modern Professional", "Blue Tech", "Dark Elegance"
- Allow user to provide custom name via "Other" option
</name_generation_rules>

<slug_generation>
- Slugify name: "Modern Professional" → "modern-professional"
- Check for existing IDs in manifest.json and append counter: "modern-professional-001"
- Increment suffix from -001 to -999 until unique ID found
- If all suffixes exhausted (aesthetic has 999+ versions), ask user to provide alternative name
</slug_generation>
</phase>

---

<phase id="4" name="test_preview_selection">
<instructions>
Present test preview selection menu using AskUserQuestion with multiSelect: true.
</instructions>

<requirements>
- MUST use AskUserQuestion tool with multiSelect: true
- Offer 4 test plugin types: simple-compressor, complex-reverb, drum-machine, simple-synth
- User can select 0-4 options (0 = skip previews entirely)
</requirements>

<tool_format>
AskUserQuestion({
  questions: [{
    question: "Generate test previews to see this aesthetic applied? (select 0-4 plugin types)",
    header: "Test previews",
    multiSelect: true,
    options: [
      { label: "Simple compressor", description: "4 parameters: threshold, ratio, attack, release" },
      { label: "Complex reverb", description: "8 parameters: size, damping, predelay, mix, tone, width, decay, diffusion" },
      { label: "Drum machine", description: "16-pad grid + 4 controls: tempo, swing, volume, pattern" },
      { label: "Simple synth", description: "6 oscillator controls: waveform, frequency, attack, decay, sustain, release" }
    ]
  }]
})
</tool_format>

<routing_logic>
IF user selects 0 options THEN skip test preview generation, proceed directly to Phase 5 (aesthetic.md only)
ELSE IF user selects 1-4 options THEN proceed to Phase 5 with selected preview types
</routing_logic>

<state_requirement>
Store selected preview types in context for Phase 5 generation.
</state_requirement>
</phase>

---

<phase id="5" name="generate_files">
<instructions>
Execute the complete 8-step generation sequence with verification checkpoints.

See references/file-generation.md for complete Phase 5 implementation protocol.
</instructions>
</phase>

---

<phase id="6" name="decision_menu">
<checkpoint_protocol>
This is a system checkpoint. MUST follow Plugin Freedom System checkpoint protocol.
MUST use inline numbered list format (NOT AskUserQuestion tool) per CLAUDE.md checkpoint protocol.
</checkpoint_protocol>

<workflow_mode_check>
Before presenting decision menu:
1. Read .claude/preferences.json to check workflow.mode setting
2. IF mode === "express" AND skill was NOT explicitly invoked via /dream command:
   - Skip decision menu
   - Exit skill gracefully with completion message
3. ELSE:
   - Present decision menu and wait for user response
</workflow_mode_check>

<decision_menu>
✅ Aesthetic "[Name]" ready!

What's next?
1. Open test previews - View mockups in browser
2. Refine aesthetic - Adjust and regenerate aesthetic.md
3. Create another aesthetic - Start new aesthetic
4. Apply to existing plugin - Choose plugin from PLUGINS.md
5. Done

Choose (1-5): _
</decision_menu>

<routing_logic>
Option 1: Run `open` commands for test preview HTML files, return to menu
Option 2: Ask what to change, re-run question batches (Phases 2-3-3.5), regenerate aesthetic.md (preserve ID)
Option 3: Return to Phase 1 with fresh context
Option 4: Read PLUGINS.md, user selects plugin, invoke ui-mockup skill with aesthetic pre-selected
Option 5: Exit skill
</routing_logic>

<state_requirement>
MUST wait for user response. NEVER auto-proceed to any option.
</state_requirement>
</phase>

---

<adaptive_questioning_strategy>
**Core Algorithm**: Extract concepts → Check tier coverage → Identify gaps → Generate 4 questions → Decision gate → Loop or finalize

**Anti-pattern**: Never ask about concepts already provided. Never repeat questions in different words.

**Tier Priority**: Tier 1 (Critical: vibe, color philosophy, control style) → Tier 2 (Visual Core: specific colors, typography, spacing, textures) → Tier 3 (Context: plugin types, inspirations, special features)

See references/aesthetic-questions.md for detailed gap analysis strategies and question banks.
See references/workflow-examples.md for complete examples showing adaptive questioning across different input scenarios.
</adaptive_questioning_strategy>

---

<handoff_protocol>
See references/handoff-protocol.md for complete skill invocation details and integration with ui-template-library and ui-mockup.
</handoff_protocol>

---

<error_handling>
See references/error-handling.md for complete edge case handling and recovery strategies.
</error_handling>

---

## Success Criteria

Skill is successful when:
- Aesthetic concept captured through adaptive questions
- No redundant questions asked (respects already-provided info)
- aesthetic.md generated with all 12 sections filled
- Test previews generated for selected plugin types (if any)
- Files stored in correct locations (.claude/aesthetics/[id]/)
- Aesthetic immediately available in ui-mockup skill
- User feels creative flow, not interrogated
- Clear next steps presented

---

## Design Rationale

See [references/design-rationale.md](references/design-rationale.md) for detailed explanation of design decisions, format consistency rules, and quality control procedures.

---

## Reference Documentation

**See also:**
- `ui-template-library` skill - Apply and save operations
- `ui-mockup` skill - Integration with Phase 0 aesthetic selection
- `plugin-ideation` skill - Adaptive questioning pattern reference
- `assets/test-plugin-specs.json` - Test plugin parameter definitions
- `references/aesthetic-questions.md` - Question bank and strategies
- `references/question-examples.md` - AskUserQuestion formatting examples
- `references/test-preview-protocol.md` - Test preview generation protocol
- `references/error-handling.md` - Error handling and edge cases
