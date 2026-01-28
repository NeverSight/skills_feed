---
name: deep-research
description: Multi-agent parallel investigation for complex JUCE problems. Use when troubleshooting fails after Level 3, problems require novel research, or user requests /research command.
allowed-tools:
  - Read # Local troubleshooting docs
  - Grep # Search docs
  - Task # Spawn parallel research subagents (Level 3)
  - WebSearch # Web research (Level 2-3)
---

# deep-research Skill

**Purpose:** Multi-level autonomous investigation for complex JUCE plugin development problems using graduated research depth protocol.

## Overview

Multi-level autonomous investigation (Level 1: 5 min local → Level 2: 30 min web → Level 3: 60 min parallel). Stops at first confident answer. User controls depth.

---

<invariant type="read_only_protocol" severity="critical">
This skill is READ-ONLY and ADVISORY ONLY.

NEVER:

- Edit code files via Edit/Write/NotebookEdit tools
- Run build commands (npm, CMake, compiler)
- Modify contracts or configurations
- Implement any solutions

ONLY:

- Search for information (Grep, Glob, Read, WebSearch, WebFetch)
- Analyze existing code and documentation
- Generate reports and recommendations
- Present findings with decision menus

ALWAYS delegate implementation to plugin-improve skill via handoff protocol.
Violation of this invariant breaks the system architecture.
</invariant>

<handoff_protocol target_skill="plugin-improve">
<trigger>User selects option 1 ("Apply solution") from decision menu</trigger>

<deep_research_action>
When user selects "Apply solution":

1. Output confirmation: "User selected: Apply solution. Invoking plugin-improve skill..."
2. Use Skill tool to invoke plugin-improve directly
3. STOP execution (no further implementation)
   </deep_research_action>

<context_passing>
plugin-improve reads research findings from conversation history.
plugin-improve skips Phase 0.5 investigation (already completed by deep-research).
</context_passing>

<enforcement>
deep-research NEVER implements. Only plugin-improve implements.
deep-research MUST invoke plugin-improve via Skill tool.
</enforcement>
</handoff_protocol>

**Note:** deep-research invokes plugin-improve directly via the Skill tool when user selects "Apply solution". This ensures the handoff happens automatically without requiring main conversation orchestration.

**Why separation matters:**

- Research uses Opus + extended thinking (expensive)
- Implementation needs codebase context (different focus)
- Clear decision gate between "here are options" and "making changes"
- Research can't break anything (safe exploration)

---

## Entry Points

Invoked by: troubleshooter (Level 4), `/research [topic]`, build-automation "Investigate", or natural language ("research [topic]").

**Parameters**: Topic/question (required), context (optional: plugin name, stage, error), starting level (optional: `/research [topic] --level 2` to skip Level 1).

---

<critical_sequence name="graduated_research_protocol" skip_prevention="strict">
<level number="1" name="quick_check" max_time_minutes="10">
<goal>Find quick answer from local knowledge base or JUCE API docs</goal>

<required_steps> 1. Search local troubleshooting docs 2. Quick Context7 lookup 3. Assess confidence
</required_steps>

<exit_conditions>
IF confidence = HIGH: Present decision menu, ALLOW user to proceed
ELSE: MUST escalate to Level 2 (no skip option)
</exit_conditions>
</level>

<level number="2" name="moderate_investigation" max_time_minutes="30">
  <prerequisite>Level 1 completed OR user manually started at Level 2</prerequisite>

<goal>Deep-dive JUCE docs, forums, GitHub for authoritative answers</goal>

<required_steps> 1. Context7 deep-dive (advanced queries, cross-references) 2. JUCE forum search via WebSearch 3. GitHub issue search (juce-framework/JUCE) 4. Synthesize findings from multiple sources
</required_steps>

<exit_conditions>
IF confidence IN [HIGH, MEDIUM]: Present decision menu
ELSE IF confidence = LOW OR novel_problem = true: MUST escalate to Level 3
</exit_conditions>
</level>

<level number="3" name="deep_research" max_time_minutes="60">
  <prerequisite>Level 2 completed OR user manually started at Level 3</prerequisite>

<goal>Parallel subagent investigation for novel/complex problems</goal>

<model_requirements>
MUST use: claude-opus-4-1-20250805
MUST enable: extended-thinking with 15k budget
NEVER use: Sonnet (insufficient synthesis capacity)
</model_requirements>

<required_steps> 1. Switch to Opus + extended thinking 2. Identify 2-3 research approaches 3. Spawn parallel subagents via Task tool (NOT serial) 4. Synthesize findings with extended thinking 5. Generate comprehensive report
</required_steps>

<exit_conditions>
ALWAYS: Present decision menu (no further escalation possible)
</exit_conditions>
</level>

<enforcement_rules>

- NEVER skip Level 1 unless user explicitly requests starting at Level 2/3 (via `/research [topic] --level 2` or "Start with Level 2 investigation of [topic]")
- NEVER use serial investigation at Level 3 (must be parallel)
- NEVER use Sonnet at Level 3 (must be Opus)
- NEVER forget extended thinking at Level 3
- NEVER implement solutions (always delegate to plugin-improve)
  </enforcement_rules>
  </critical_sequence>

## Level 1: Quick Check (5-10 min, Sonnet, no extended thinking)

**Goal:** Find quick answer from local knowledge base or JUCE API docs

**Sources:** Local troubleshooting docs, Context7 JUCE documentation

**Exit criteria:** HIGH confidence solution → present decision menu, otherwise escalate to Level 2

See `references/research-protocol.md#level-1-quick-check` for detailed process.

---

## Level 2: Moderate Investigation (15-30 min, Sonnet, no extended thinking)

**Goal:** Deep-dive JUCE docs, forums, GitHub for authoritative answers

**Sources:** Context7 deep-dive, JUCE forum search, GitHub issue search

**Exit criteria:** MEDIUM-HIGH confidence solution → present decision menu, otherwise escalate to Level 3

See `references/research-protocol.md#level-2-moderate-investigation` for detailed process.

---

## Level 3: Deep Research (30-60 min, Opus, extended thinking 15k budget)

**Goal:** Parallel subagent investigation for novel/complex problems

**Model requirements:** claude-opus-4-1-20250805 with extended-thinking (15k budget)

**Process:** Spawn 2-3 parallel research subagents via Task tool, synthesize findings

**Exit criteria:** ALWAYS present decision menu (no further escalation)

See `references/research-protocol.md#level-3-deep-research` for detailed process.

---

## Report Generation

Each level generates a structured report using templates in `assets/`:

- Level 1: `assets/level1-report-template.md`
- Level 2: `assets/level2-report-template.md`
- Level 3: `assets/level3-report-template.md`

Reports include: findings summary, confidence assessment, recommended solution, and source references.

**Progress tracking**: Use `assets/research-progress.md` template to track investigation progress across levels.

---

<state_requirement name="checkpoint_protocol">
At the end of each level (when presenting findings), MUST:

1. Present decision menu (numbered list format, NOT AskUserQuestion tool)
2. WAIT for user response (NEVER auto-proceed)
3. Route based on selection:

<response_handler option="1" action="apply_solution">
<condition>User selects option 1 ("Apply solution")</condition>
<action>

1. Output confirmation: "User selected: Apply solution. Invoking plugin-improve skill..."
2. Use Skill tool to invoke plugin-improve
3. STOP execution (no further implementation)
   </action>
   </response_handler>

<response_handler option="2" action="review_findings">
<condition>User selects option 2 ("Review full findings")</condition>
<action>

1. Display complete research report
2. Re-present decision menu
3. WAIT for new selection
   </action>
   </response_handler>

<response_handler option="3" action="escalate">
<condition>User selects option 3 ("Escalate to next level")</condition>
<action>

1. Proceed to next level (Level 1 → Level 2 → Level 3)
2. If already at Level 3, inform user no further escalation available
3. Continue with next level's process
   </action>
   </response_handler>

<response_handler option="other" action="clarify">
<condition>User provides custom response</condition>
<action>

1. Ask for clarification
2. Re-present decision menu with context
3. WAIT for selection
   </action>
   </response_handler>

<enforcement>
NEVER auto-proceed to implementation.
NEVER skip decision menu.
ALWAYS wait for user response before continuing.
</enforcement>
</state_requirement>

## Decision Menus

After each level, present decision menu using checkpoint protocol format:

**Example (Level 1 - HIGH confidence):**

```
✓ Level 1 complete (found solution in local docs)

Solution: [Brief description of solution]
Source: troubleshooting/[category]/[file].md
Confidence: HIGH (exact match)

What's next?

1. Apply solution (recommended)
2. Review full findings
3. Continue deeper - Escalate to Level 2
4. Other

Choose (1-4): _
```

**Example (Level 2 - MEDIUM confidence):**

```
✓ Level 2 complete (found 2 potential solutions)

Recommended: [Solution 1 name]
Alternative: [Solution 2 name]
Confidence: MEDIUM (verified by JUCE forum + docs)

What's next?

1. Apply recommended solution
2. Review all findings
3. Try alternative approach
4. Continue deeper - Escalate to Level 3
5. Other

Choose (1-5): _
```

**Example (Level 3 - comprehensive investigation):**

```
✓ Level 3 complete (parallel investigation)

Investigated 3 approaches:
- Approach A: [Brief description] (recommended)
- Approach B: [Brief description] (viable alternative)
- Approach C: [Brief description] (not recommended)

Confidence: HIGH after synthesis

What's next?

1. Apply recommended solution (recommended)
2. Review detailed comparison
3. Try alternative approach B
4. Document findings
5. Other

Choose (1-5): _
```

NEVER use AskUserQuestion tool for decision menus. Always use inline numbered lists with "Choose (1-N): \_" format matching checkpoint protocol.

See `<state_requirement name="checkpoint_protocol">` below for response handling.

---

## Integration Points

See [references/integrations.md](references/integrations.md) for troubleshooter and troubleshooting-docs integration details.

---

## Error Handling

See [references/error-handling.md](references/error-handling.md) for timeout, failure, and fallback patterns.

---
