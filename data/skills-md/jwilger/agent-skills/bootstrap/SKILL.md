---
name: bootstrap
description: >-
  Zero-config SDLC onboarding. Detects project environment, harness
  capabilities, and harness type. Configures TDD mode, generates AGENTS.md,
  offers optional enforcement hooks, and recommends skills by phase. Single
  entry point for all harnesses.
license: CC0-1.0
metadata:
  author: jwilger
  version: "2.0"
  requires: []
  context: []
  phase: understand
  standalone: true
---

# Bootstrap

**Value:** Communication -- establish shared understanding of environment,
capabilities, and workflow before any work begins.

## Purpose

Single entry point for configuring the SDLC workflow on any harness. Detects
the project environment and harness capabilities, configures TDD mode
(guided or automated), generates harness-appropriate instruction files, and
recommends skills. Never silently installs or modifies anything.

## Practices

### Step 1: Detect the Environment

Gather project context silently before asking questions:

```
!test -f package.json && echo "js" || true
!test -f Cargo.toml && echo "rust" || true
!test -f pyproject.toml && echo "python" || true
!test -f go.mod && echo "go" || true
!test -f mix.exs && echo "elixir" || true
!git rev-parse --is-inside-work-tree 2>/dev/null && echo "git" || true
!ls skills/*/SKILL.md 2>/dev/null | sed 's|skills/||;s|/SKILL.md||' || true
```

Record: languages detected, git available, skills already installed.

### Step 2: Detect Harness Capabilities

Probe for delegation primitives. See `references/capability-detection.md`
for the full detection procedure.

| Capability | How to detect | Implication |
|------------|---------------|-------------|
| Skill chaining | Always available | Guided TDD mode works |
| Subagents | Task tool present | Serial subagent strategy works |
| Agent teams | TeamCreate tool present | Ping-pong pairing works |

### Step 3: Detect Harness Type

Identify the harness to generate the correct instruction files:

| Signal | Harness |
|--------|---------|
| `CLAUDE.md` convention, Claude Code tools | Claude Code |
| `AGENTS.md` convention, Codex tools | Codex |
| `.cursor/rules` directory | Cursor / Windsurf |
| None of the above | Generic (AGENTS.md only) |

### Step 4: Configure TDD Mode

Recommend based on detected capabilities:

- **Subagents or teams available:** Recommend automated mode (`/tdd`).
- **No delegation primitives:** Recommend guided mode (`/tdd red`, `/tdd green`, etc.).
- Let the user override. Record the choice.

If Claude Code is detected and the user wants maximum enforcement, offer
to install optional hook templates from `skills/tdd/references/hooks/`.

### Step 5: Ask the User

**Question 1: What are you trying to do?**
- "Start a new project" -- recommend Understand + Decide + Build phases
- "Add a feature or fix a bug" -- recommend Build + Ship phases
- "Set up team workflow" -- recommend all phases plus ensemble team

**Question 2: How much process structure?**
- "Minimal" -- recommend tdd, domain-modeling
- "Standard" -- recommend core + ship skills
- "Full" -- recommend all skills

See `references/skill-recommendations.md` for the full skill list by phase.

### Step 6: Generate Instruction Files

Generate harness-appropriate files. See `references/agents-md.md` for
AGENTS.md best practices (small routing document, progressive disclosure,
managed markers) and `references/harness-files.md` for harness-specific
generation rules.

### Step 7: Optional Ensemble Team

If the user selected "Set up team workflow" or "Full" process structure,
offer to invoke the `ensemble-team` skill for AI team formation. Present
the three presets (solo-plus, lean, full). If accepted, invoke the skill
and record the preset in configuration.

### Step 8: Commit and Display

Stage generated files, commit with a descriptive message, and display:
- What was configured (harness, TDD mode, skills recommended)
- Next steps (`/tdd` to start a TDD cycle, or phase-specific commands)
- If ensemble team was configured, note the preset and member count

## Enforcement Note

This skill is purely advisory. It generates configuration and instruction
files but cannot install skills or modify harness settings without user
confirmation.

## Verification

- [ ] Environment was detected before asking questions
- [ ] Harness capabilities were probed (not assumed)
- [ ] No more than 2-3 questions were asked
- [ ] TDD mode recommendation matched detected capabilities
- [ ] Generated files use managed markers for safe re-runs
- [ ] Nothing was installed without user confirmation

## Dependencies

This skill works standalone. It recommends but does not require other skills.
It generates configuration that references the `tdd` skill for TDD workflow.
