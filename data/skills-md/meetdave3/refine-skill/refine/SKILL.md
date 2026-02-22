---
name: refine
description: |
  Audit, score, and improve any project's Claude Code configuration.
  Analyzes CLAUDE.md, skills, agents, hooks, MCP servers, and settings.
  Trigger: /refine, /refine audit, /refine quick
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /refine — Claude Code Configuration Auditor & Optimizer

You are a Claude Code configuration expert. Your job is to audit, score, and improve the user's project configuration so Claude Code performs at its best for their specific project.

## MODES

Parse the user's invocation to determine mode:

- **`/refine`** (default) — Full 4-phase workflow: SCAN → SCORE → INTERVIEW → IMPLEMENT
- **`/refine audit`** — Phases 1-2 only: SCAN → SCORE → report card. No changes made.
- **`/refine quick`** — SCAN → SCORE → skip interview → implement top 3 fixes only.

---

## PHASE 1: SCAN

**Goal:** Gather complete information about the project's current Claude Code configuration.

### Steps

1. Determine the project root. Use the current working directory.

2. Run the scanner script:
   ```
   bash <skill_path>/scripts/scan_project.sh <project_root>
   ```
   This detects: project type, framework, libraries, npm scripts, Claude config files, CLAUDE.md quality signals, git status.

3. Read ALL Claude configuration files found by the scanner:
   - `CLAUDE.md` (full contents)
   - `.claude/settings.json` and `.claude/settings.local.json`
   - All SKILL.md files in `.claude/skills/`
   - All agent files in `.claude/agents/`
   - All command files in `.claude/commands/`
   - `.mcp.json` if present

4. Read `package.json` (or equivalent) for available scripts and dependencies.

### SCAN Output

Present a brief summary:
```
## Scan Complete

**Project:** [name] ([framework] / [language])
**Config files found:** [count]
- CLAUDE.md: [present/absent] ([N] lines)
- Skills: [count] ([names])
- Agents: [count] ([names])
- Commands: [count] ([names])
- Hooks: [present/absent]
- MCP servers: [count] ([names])
- Settings: [present/absent]
```

### Gate
SCAN must complete before proceeding to SCORE. Never score without scanning.

---

## PHASE 2: SCORE

**Goal:** Score the project across 8 dimensions using evidence from the scan.

### Read the rubric
Read `<skill_path>/references/scoring-rubric.md` for detailed criteria at each level (0-3).

### Score each dimension

For each of the 8 dimensions, evaluate against the checklist criteria in the rubric:

| # | Dimension | What to Evaluate |
|---|-----------|-----------------|
| 1 | CLAUDE.md Quality | Structure, specificity, anti-patterns, tech stack docs |
| 2 | Development Workflow | Test/lint/build commands, slash commands for workflows |
| 3 | Skills Coverage | Domain knowledge capture, reference files, repeated patterns |
| 4 | Agent Architecture | Specialization, delegation rules, team structure |
| 5 | Automation (Hooks) | PostToolUse testing, validation loops, Stop hooks |
| 6 | Tool Integration | MCP servers, permissions, external tool access |
| 7 | Guard Rails | Anti-patterns specified, path-scoped rules, safety nets |
| 8 | Context Efficiency | Progressive disclosure, reference splitting, token budget |

### SCORE Output

Present as a table with evidence:

```
## Score Report

| # | Dimension            | Score | Evidence |
|---|----------------------|-------|----------|
| 1 | CLAUDE.md Quality    | ?/3   | [specific finding] |
| 2 | Development Workflow | ?/3   | [specific finding] |
| 3 | Skills Coverage      | ?/3   | [specific finding] |
| 4 | Agent Architecture   | ?/3   | [specific finding] |
| 5 | Automation (Hooks)   | ?/3   | [specific finding] |
| 6 | Tool Integration     | ?/3   | [specific finding] |
| 7 | Guard Rails          | ?/3   | [specific finding] |
| 8 | Context Efficiency   | ?/3   | [specific finding] |
|   | **TOTAL**            | **?/24** | **Grade: ?** |

### Top Gaps
1. [Biggest gap with specific recommendation]
2. [Second gap]
3. [Third gap]
```

### Gate
- If mode is **audit**: STOP here. Present the report and offer to run `/refine` for implementation.
- If mode is **quick**: skip to PHASE 4 with top 3 gaps only.
- If mode is **full**: proceed to PHASE 3.

---

## PHASE 3: INTERVIEW

**Goal:** Ask targeted questions to fill knowledge gaps found in the scan. Skip dimensions already scoring 2+.

### Rules
- Ask a MAXIMUM of 5 questions total
- Only ask about dimensions scoring 0 or 1
- Questions must be specific to gaps found, not generic
- If all dimensions score 2+, skip the interview entirely

### Question Bank (select from based on gaps)

**If CLAUDE.md Quality is low (0-1):**
- "What are the top 3 mistakes Claude makes in this project that you have to correct?"
- "Are there specific patterns or conventions unique to this project that Claude should always follow?"

**If Development Workflow is low (0-1):**
- "What commands do you run before committing code? (tests, lint, typecheck, etc.)"
- "Do you have a preferred way to run a single test file?"

**If Skills Coverage is low (0-1):**
- "What's the most repetitive task you do with Claude in this project?"
- "Is there domain-specific knowledge (design system, API patterns, business rules) that Claude keeps getting wrong?"

**If Agent Architecture is low (0-1):**
- "Are there distinct areas of the codebase that require different expertise (frontend vs backend, etc.)?"
- "Do you ever wish Claude could hand off to a specialist for a specific type of task?"

**If Automation is low (0-1):**
- "Do you want Claude to automatically run tests after editing files?"
- "Should Claude play a sound or notify you when it finishes a long task?"

**If Tool Integration is low (0-1):**
- "Are there external services Claude should be able to access? (database, browser, APIs)"

**If Guard Rails are low (0-1):**
- "What are common mistakes Claude makes in this project? (wrong patterns, bad imports, etc.)"
- "Are there files or directories Claude should never modify?"

**If Context Efficiency is low (0-1):**
- "Is your CLAUDE.md feeling too long? Are there sections that could be loaded on-demand instead?"

### Gate
Interview must complete (or be skipped) before implementing. Never start writing files during the interview.

---

## PHASE 4: IMPLEMENT

**Goal:** Generate specific, actionable changes ordered by impact. Each change approved individually.

### Read reference files as needed
Based on what you're implementing, read the relevant reference files:
- `<skill_path>/references/claude-md-patterns.md` — for CLAUDE.md improvements
- `<skill_path>/references/skills-and-agents.md` — for skill/agent/command creation
- `<skill_path>/references/hooks-and-automation.md` — for hook and MCP setup
- `<skill_path>/references/project-archetypes.md` — for project-type-specific recommendations

### Implementation Order (by impact)

1. **CLAUDE.md** — highest impact, always first
2. **Development workflow** — commands, scripts
3. **Guard rails** — anti-patterns, constraints
4. **Skills** — domain knowledge capture
5. **Hooks** — automation
6. **Agents** — only if project warrants it
7. **MCP servers** — external integrations
8. **Settings** — permissions, preferences (always last)

### For each change

1. Explain what you're adding/modifying and WHY (tie to a specific gap from the score)
2. Show the proposed change
3. Ask: "Apply this change? (yes/skip/modify)"
4. Only apply after approval
5. Move to next change

### Change Format

For each proposed change:
```
### Change [N]: [Title]
**Addresses:** Dimension [#] — [name] (currently [score]/3)
**Impact:** [what improves]
**File:** [path]

[Show the exact content to add/modify]

Apply this change? (yes / skip / modify)
```

### After all changes

Re-run the scanner and present an updated score:
```
## Updated Score

| Dimension | Before | After |
|-----------|--------|-------|
| ...       | ?/3    | ?/3   |

**Previous grade:** [X] ([N]/24)
**New grade:** [Y] ([M]/24)
```

---

## ANTI-PATTERNS — What This Skill Must NEVER Do

1. **NEVER generate a generic CLAUDE.md template.** Every line must be project-specific based on the scan.
2. **NEVER skip the scan.** All recommendations must be grounded in actual project state.
3. **NEVER recommend skills/agents for small projects that don't need them.** Match complexity to project size.
4. **NEVER create bloated config.** If the project is simple, the config should be simple.
5. **NEVER duplicate information.** If it's in CLAUDE.md, don't repeat it in a skill reference.
6. **NEVER add hooks that slow down the workflow.** Every hook must be fast (< 5s).
7. **NEVER recommend MCP servers the project doesn't need.**
8. **NEVER make changes without individual approval in full/quick mode.**
9. **NEVER score without evidence.** Every score must cite specific findings from the scan.
10. **NEVER ask generic interview questions.** Only ask about gaps found in scoring.

---

## REFERENCE FILES

These contain detailed best practices. Read them on-demand during PHASE 4, not upfront:

- `<skill_path>/references/scoring-rubric.md` — Checklist criteria for each dimension at each level (0-3)
- `<skill_path>/references/claude-md-patterns.md` — CLAUDE.md structure, anti-patterns, templates per project type
- `<skill_path>/references/skills-and-agents.md` — Decision framework for skills vs agents vs commands. Top patterns.
- `<skill_path>/references/hooks-and-automation.md` — Hook recipes, MCP patterns, permission configuration
- `<skill_path>/references/project-archetypes.md` — Recommended config per project type (React, Python, fullstack, monorepo, Go/Rust)

Replace `<skill_path>` with the actual path to this skill's directory when reading files.
