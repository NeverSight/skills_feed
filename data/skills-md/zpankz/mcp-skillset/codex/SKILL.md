---
name: codex
description: |
  Execute OpenAI Codex CLI for code analysis, refactoring, and automated editing.
  Also use for delegating complex debugging and research to GPT models for second opinions.
tools:
  - Bash
  - Read
  - Grep
  - Glob
  - WebFetch
  - AskUserQuestion
disallowedTools:
  - Write
  - Edit
  - TodoWrite
context: fork
model: opus
agent: codex-agent
---

# Codex Skill Guide

## When to Use This Skill

**Primary Use Cases**:

1. User explicitly requests `codex` CLI execution (Mode 1: Direct CLI)
2. Complex debugging requiring GPT second opinion (Mode 2: GPT Delegation)
3. Deep research on unfamiliar technologies (Mode 2: GPT Delegation)
4. Algorithm optimization validation (Mode 2: GPT Delegation)

**Do NOT use for**:

- Simple code explanations
- Routine file operations
- Standard debugging that Claude can handle directly

## Execution Modes

### Mode 1: Direct CLI Execution

**When**: User explicitly asks to run codex CLI (`codex exec`, `codex resume`)

**Workflow**:

1. Utilise `AskUserQuestion` to evaluate and extend the users query, providing at least 5 questions, each with multi-select options to determine the best model and reasoning effort. Let the first question include options for the following combinations:

2. Execute:
   `codex exec --skip-git-repo-check -m <MODEL> --config model_reasoning_effort="<EFFORT>" --sandbox <MODE> --full-auto 2>/dev/null`

3. Inform user: "You can resume with 'codex resume' anytime"

**Resuming**:
`echo "new prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null`

### Mode 2: GPT Delegation for Analysis

**When**: Complex problem needs second opinion (async race conditions,
architecture decisions, algorithm validation)

**Workflow**:

1. Analyze context and identify what GPT analysis would help
2. Formulate comprehensive query with all relevant context:
   - Problem statement
   - Current findings
   - Code snippets (if applicable)
   - Error messages
   - Attempted solutions
   - Specific questions
3. Keep context concise but complete (<10K tokens preferred)
4. Execute: `codex -p "<DETAILED CONTEXT>"`
5. Synthesize GPT response into actionable insights
6. Report findings with:
   - Clear summary of GPT's analysis
   - Specific recommendations or solutions
   - Additional considerations or caveats
   - Next steps if applicable

### Error Handling

- Verify codex binary exists before execution: `which codex`
- Stop immediately on non-zero exit codes and report to user
- Request direction before retrying failed commands
- See 'High-Impact Flags Confirmation' in AskUserQuestion Tool Usage section
  before using:
  - `--full-auto`
  - `--sandbox danger-full-access`
  - `--skip-git-repo-check` (default, but mention to user)

### Context Management

- Prioritize most relevant information when building queries
- Summarize background information if context is large
- Break complex problems into specific, answerable questions
- Avoid passing entire codebases - extract relevant snippets

## AskUserQuestion Tool Usage

This skill uses the AskUserQuestion tool for all user interactions.
Here are the standard invocation patterns:

### Initial Configuration (Mode 1, Step 1)

At the start of Mode 1 execution, gather model, reasoning effort, and sandbox
mode with a single question:

**Invoke the tool like this:**

```text
Use AskUserQuestion with:
- Question: "Select codex configuration (model, reasoning effort, and sandbox)"
- Options:
  1. "gpt-5.2-codex / high / read-only (Recommended)" - Balanced, analysis only
  2. "gpt-5.2-codex / xhigh / read-only" - Max quality, analysis only
  3. "gpt-5.2-codex / high / workspace-write" - Balanced, can edit files
  4. "gpt-5.2-codex / xhigh / workspace-write" - Max quality, can edit files
  5. "gpt-5.2 / medium / read-only" - Faster, general purpose
  6. "gpt-5.2-codex / high / danger-full-access" - Network/broad access
  7. "Custom" - User will specify model, effort, and sandbox separately
```

### High-Impact Flags Confirmation

Before executing with --full-auto or dangerous flags:

**Invoke the tool like this:**

```text
Use AskUserQuestion with:
- Question: "Ready to execute with these flags: [LIST FLAGS]. Proceed?"
- Show complete command preview
- Options:
  1. "Execute now" - Run as configured
  2. "Modify configuration" - Change settings
  3. "Cancel" - Abort
```

### Post-Execution Follow-up

After codex command completes:

**Invoke the tool like this:**

```text
Use AskUserQuestion with:
- Question: "Codex completed. [SUMMARY]. Next steps?"
- Options:
  1. "Resume with additional prompt" - Continue session
  2. "Analyze results" - Review output
  3. "Complete" - Finished
  4. "Retry with different config" - Adjust settings
```

### Error Recovery

When command fails or has warnings:

**Invoke the tool like this:**

```text
Use AskUserQuestion with:
- Question: "Error: [SPECIFIC ERROR]. How to proceed?"
- Show what succeeded vs failed
- Options:
  1. "Resume with adjustments" - Fix and continue
  2. "Retry with different config" - Change model/effort/sandbox
  3. "Accept partial results" - Use what worked
  4. "Invoke heal-skill" - Fix outdated SKILL.md
```

## Running a Task

1. See 'Initial Configuration' in AskUserQuestion Tool Usage section to gather
   model, reasoning effort, and sandbox mode in one question
2. Assemble the command with the appropriate options:
   - `-m, --model <MODEL>`
   - `--config model_reasoning_effort="<xhigh|high|medium|low>"`
   - `--sandbox <read-only|workspace-write|danger-full-access>`
   - `--full-auto`
   - `-C, --cd <DIR>`
   - `--skip-git-repo-check`
3. Always use --skip-git-repo-check.
4. When continuing a previous session, use
   `codex exec --skip-git-repo-check resume --last` via stdin. When resuming
   don't use any configuration flags unless explicitly requested by the user.
   Resume syntax:
   `echo "your prompt here" | codex exec --skip-git-repo-check resume --last 2>/dev/null`.
   All flags have to be inserted between exec and resume.
5. **IMPORTANT**: By default, append `2>/dev/null` to all `codex exec` commands
   to suppress thinking tokens (stderr). Only show stderr if the user
   explicitly requests to see thinking tokens or if debugging is needed.
6. Run the command, capture stdout/stderr (filtered as appropriate), and
   summarize the outcome for the user.
7. **After Codex completes**, inform the user: "You can resume this Codex
   session at any time by saying 'codex resume' or asking me to continue with
   additional analysis or changes."

### Quick Reference

| Use case | Sandbox mode | Key flags |
| --- | --- | --- |
| Read-only review or analysis | `read-only` | `--sandbox read-only 2>/dev/null` |
| Apply local edits | `workspace-write` | `--sandbox workspace-write --full-auto 2>/dev/null` |
| Permit network or broad access | `danger-full-access` | `--sandbox danger-full-access --full-auto 2>/dev/null` |
| Resume recent session | Inherited from original | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` |
| Run from another directory | Match task needs | `-C <DIR>` plus other flags `2>/dev/null` |

## Following Up

- After every `codex` command, see 'Post-Execution Follow-up' in AskUserQuestion
  Tool Usage section
- When resuming, pipe the new prompt via stdin:
  `echo "new prompt" | codex exec resume --last 2>/dev/null`. The resumed
  session automatically uses the same model, reasoning effort, and sandbox mode
  from the original session.
- Restate the chosen model, reasoning effort, and sandbox mode when proposing
  follow-up actions.

## Error Handling Guidelines

- Stop and report failures whenever `codex --version` or a `codex exec` command
  exits non-zero; request direction before retrying.
- See 'High-Impact Flags Confirmation' and 'Error Recovery' in AskUserQuestion
  Tool Usage section
- When output includes warnings or partial results, see 'Error Recovery' in
  AskUserQuestion Tool Usage section

## Heal-Skill Integration

When codex CLI API changes are detected (command failures, unexpected output formats, or deprecated flags):

1. **Detection**: Notice command failures or API mismatches during execution
2. **Trigger**: Flag skill for healing via `/heal-skill codex`
3. **Analysis**: Healing agent analyzes current CLI with `codex --help` and `codex features list`
4. **Update**: Updates skill documentation to match current API
5. **Validation**: Re-validates agent configuration for compatibility
6. **Model Verification**: Ensures only gpt-5.2 and gpt-5.2-codex models are referenced

**Common Changes to Monitor**:
- New or deprecated command flags
- Changes to sandbox modes or reasoning effort options
- Model availability updates
- MCP integration changes
- Session management API modifications
