---
name: ralph-loop-template
version: 0.0.2
category: development
description: Generates iterable checklist PROMPT files for Ralph Loop from plan files or current context, and provides the /ralph-loop execution command.
requires: "[ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum)"
disable-model-invocation: true
argument-hint: "[plan file path]"
---

## Input

```text
$ARGUMENTS
```

## Instructions

### Step 1: Gather Plan

**If an argument is provided**: Read the file to understand the plan content.

**If no argument**: Search for a plan in the following order:

1. Search for plan files in the project root: `PLAN.md`, `plan.md`, `PLAN-*.md`, `plan-*.md`, `TODO.md`, `prd.md`, `PRD.md`
   - 1 found → Use it (inform the user which file was detected)
   - Multiple found → Present the list and ask for selection
   - 0 found → Proceed to next step
2. Use the plan discussed in the current conversation context.
3. If no plan exists in the conversation context, ask the user to describe the plan.

### Step 2: Identify Project Environment

Collect project-specific information to embed in the PROMPT file.

**Search for agent/project configuration files** in the following priority order:
1. `CLAUDE.md` (Claude Code)
2. `.cursorrules` (Cursor)
3. `.windsurfrules` (Windsurf)
4. `AGENTS.md`, `COPILOT.md`, `GEMINI.md`

If a config file is found, extract:
- Verification commands: Combine build, test, lint into a single chain (e.g., `npm run lint && npm run build && npm test`)
- Key code style rules (items to insert into the PROMPT's absolute rules `{AGENT_RULES}`, max 3)

**If no config file is found**: Infer from project structure:
- `package.json` → npm/yarn commands
- `Makefile` / `Justfile` → make/just commands
- `Cargo.toml` → cargo commands
- `pyproject.toml` / `setup.py` → python toolchain
- If undetectable, ask the user for build/test commands

### Step 3: Analyze Plan

Extract the following from the plan:

- **Goal**: What is being built
- **Non-goals**: What will NOT be done in this task (to prevent Feature Invention)
- **Phase list**: Ordered implementation steps
- **Key content per phase**: Files to change, implementation details
- **Reference docs/files**: Pattern references, design document paths
- **Completion criteria**: Criteria for determining the entire task is complete

Completion criteria **must be mechanically verifiable** (e.g., command execution returns exit code 0). Do not use subjective criteria like "works well" or "looks clean".

### Step 4: Phase Splitting

Split the plan into phases suitable for Ralph Loop iterations.

**Splitting principles**:

- **One iteration = exactly one phase**. Processing 2+ phases is strictly forbidden.
- When a phase is completed, immediately end the iteration. The next phase is handled in the next iteration.
- Each phase must be the **minimum unit that can independently pass verification**.
- Split phases that are too large, merge phases that are too small.

**Size guideline** (reference, not absolute):

- If description needs 3+ sentences → candidate for splitting
- If it's a single-line change to one file → candidate for merging with adjacent phase
- The appropriate size is one the agent can implement + verify within a single context

**max-iterations calculation**: `number of phases + 2`
- +1: Buffer for automatic retry on verification failure
- +1: Buffer for promise output iteration after final phase completion

### Step 5: Generate PROMPT File

Use `references/prompt-template.md` as the base template and `references/iteration-procedure.md` as the iteration procedure block to generate the PROMPT file.

Create a `PROMPT-{kebab-case-name}.md` file in the project root.

**Placeholder mapping**:

| Placeholder | Source | Fallback |
|-------------|--------|----------|
| `{goal title}` | Step 3 | Ask user |
| `{project name}` | Project directory name or CLAUDE.md | Ask user |
| `{goal}` | Step 3 | Ask user |
| `{AGENT_RULES}` | Step 2 (agent config rules) | Omit entire line if no config file |
| `{non-goals}` | Step 3 + non-goal writing rules for inference | Min 2 items |
| `{reference doc rows}` | Step 2-3 | Omit entire reference docs section if 0 docs |
| `{iteration procedure}` | Entire `references/iteration-procedure.md` | — |
| `{checklist}` | Step 4 phase splitting result | — |
| `{verification command}` | Step 2 (project detection) | Ask user |
| `{COMPLETION_PROMISE}` | COMPLETION_PROMISE generation rules | — |

**Note**: Example text that uses curly braces (such as the recording format for out-of-scope findings) should be left as-is without substitution.

### Step 6: Output Result

Provide the generated PROMPT file path and output the `/ralph-loop` command in the following format:

```
### Generated File

`{PROMPT file path}`

> Review the generated PROMPT file before execution. Check the verification commands and phase structure in particular.

### Ralph Loop Execution Command

/ralph-loop "Read {PROMPT file path} and implement the next unchecked phase. Always read the file first to find the first phase with [ ] items." --max-iterations {number of phases + 2} --completion-promise "{COMPLETION_PROMISE}"
```

Output the command block above so it can be copied and used directly.

---

## Generation Rules

### Checklist Writing Rules

- **Phase = iteration unit**: A single `### Phase N` block is processed in one iteration
- **Sub-items = detailed tasks within a phase**: Place 2-5 `- [ ]` sub-items under each Phase
- Sub-items should specify files to change and implementation details
- Verification is not a checklist item — it runs automatically in STEP 4 of the iteration procedure. Use the project's build/test commands detected in Step 2

### Non-Goal Writing Rules

In addition to items explicitly excluded by the plan, infer and add:
- Refactoring outside the plan's scope
- Unrequested test/documentation/configuration changes
- Existing API or interface changes (if not specified in the plan)

### COMPLETION_PROMISE Generation Rules

- Uppercase English, space-separated
- Briefly summarize the goal (e.g., "HELP OVERLAY COMPLETE", "AUTH REFACTOR DONE")
