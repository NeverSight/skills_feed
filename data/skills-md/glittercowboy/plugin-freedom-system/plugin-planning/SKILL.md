---
name: plugin-planning
description: Orchestrates Stage 0 research and planning for JUCE plugins - creates architecture.md and plan.md contracts through subagent delegation. Use when creative brief exists and plugin needs DSP architecture specification, complexity assessment, or implementation planning. Invoke via /plan command, natural language (plan architecture, research DSP), or as first implementation step.
allowed-tools:
  - Read # For contracts and references
  - Write # For architecture.md, plan.md
  - Edit # For state updates (PLUGINS.md, .continue-here.md)
  - Bash # For git commits, precondition checks
  - Task # For subagent delegation
  - WebSearch # For professional plugin research
  - Grep # For searching existing implementations
  - Glob # For finding reference files
preconditions:
  - creative-brief.md must exist in plugins/[Name]/.ideas/
  - Parameter specification must exist (parameter-spec.md OR parameter-spec-draft.md)
  - Plugin must NOT already be past Stage 0
---

# plugin-planning Skill

**Purpose:** Handle Stage 0 (Research & Planning - consolidated) through subagent delegation. This skill creates the foundation contracts (architecture.md, plan.md) that guide implementation in a single consolidated pass.

**Invoked by:** `/plan` command or as first step of `/implement` workflow

---

## Entry Point

**Check preconditions first:** See [references/preconditions.md](references/preconditions.md) for detailed validation logic.

Quick validation:
1. creative-brief.md must exist at `plugins/[Name]/.ideas/`
2. Parameter specification required (parameter-spec.md OR parameter-spec-draft.md)
3. Plugin status must be ≤ Stage 0 (not already in implementation)
4. Detect existing contracts (architecture.md, plan.md) for resume logic

If all preconditions pass → proceed to Stage 0

---

## Stage 0: Research & Planning

**Goal:** Create DSP architecture specification (architecture.md) AND implementation plan (plan.md)
**Duration:** 5-35 minutes (complexity-dependent)
**Implementation:** Delegated to research-planning-agent subagent via Task tool

**Dispatch pattern:**

1. Read contracts in parallel (use parallel Read calls in single tool invocation):
   - plugins/[Name]/.ideas/creative-brief.md
   - plugins/[Name]/.ideas/parameter-spec.md OR parameter-spec-draft.md
   - plugins/[Name]/.ideas/mockups/*.yaml (if exists)

2. Invoke subagent:
   ```
   Task(subagent_type="research-planning-agent", description="[prompt with contracts]", model="sonnet")
   ```

   See [references/subagent-invocation.md](references/subagent-invocation.md) for detailed prompt construction.

3. After subagent returns, execute checkpoint protocol:
   - Read subagent's return message
   - Verify architecture.md and plan.md created
   - Present decision menu (use assets/decision-menu-stage-0.md template)
   - WAIT for user response

**Subagent executes:** Full Stage 0 protocol from research-planning-agent.md

**Outputs:**
- `plugins/[Name]/.ideas/architecture.md` (see assets/architecture-template.md)
- `plugins/[Name]/.ideas/plan.md` (see assets/plan-template.md)

**Decision menu:** Use assets/decision-menu-stage-0.md template

**Menu option routing:**

- **Option 1 (Start implementation):** Invoke plugin-workflow skill
- **Option 2 (Review contracts):** Read and display architecture.md, plan.md, parameter-spec.md, creative-brief.md
- **Option 3 (Improve brief):** Invoke plugin-ideation skill
- **Option 4 (Deep research):** Invoke deep-research skill
- **Option 5 (Pause):** Verify state saved, exit skill
- **Option 6 (Other):** Route based on request (plugin-workflow, ui-mockup, deep-research, or handle directly)

**Note:** research-planning-agent runs in fresh context (5-35 min session doesn't pollute orchestrator)

**Validation before proceeding to Stage 1:**

1. Verify architecture.md exists with all required sections (Core Components, Processing Chain, Parameter Mapping)
2. Verify plan.md exists with complexity score and implementation strategy
3. If verification fails: Display error and return to Stage 0
4. When user chooses option 1: Delegate to plugin-workflow skill (plugin-workflow owns Stages 1-4)

---

## Reference Files

- [references/preconditions.md](references/preconditions.md) - Detailed precondition validation logic
- [references/subagent-invocation.md](references/subagent-invocation.md) - Subagent dispatch pattern and prompt construction
- [references/state-updates.md](references/state-updates.md) - State file update protocol
- [references/git-operations.md](references/git-operations.md) - Commit patterns

**Templates:**
- `assets/architecture-template.md` - DSP architecture contract template
- `assets/plan-template.md` - Implementation plan template
- `assets/decision-menu-stage-0.md` - Decision menu template
