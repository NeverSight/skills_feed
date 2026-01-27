---
name: codex
description: Hand off a task to Codex CLI for autonomous execution. Use when a task would benefit from a capable subagent to implement, fix, investigate, or review code. Codex has full codebase access and can make changes.
argument-hint: <task description> [--model <model>] [--sandbox <mode>]
allowed-tools: Bash(codex:*), Bash(git:*), Bash(pwd:*), Bash(mkdir:*), Bash(cat:*), Bash(head:*), Bash(tail:*), Bash(wc:*), Read, Grep, Glob
---

# Codex Subagent

Hand off a task to Codex CLI for autonomous execution. Codex is a capable coding agent that can implement features, fix bugs, refactor code, investigate issues, and review changes.

## Session Info

Session ID: ${CLAUDE_SESSION_ID}
Output directory: `~/.claude/codex/${CLAUDE_SESSION_ID}/`

**Output files:**
- `progress-{timestamp}.jsonl` - Streaming JSONL events (for monitoring)
- `summary-{timestamp}.txt` - Final agent message only (for results)

## Parse Arguments

Arguments: $ARGUMENTS

Parse the arguments:
- Everything before flags is the **task description**
- `--model <model>` or `-m <model>`: Override model (only if explicitly requested)
- `--sandbox <mode>`: Override sandbox mode (only if explicitly requested)

**Available models** (only pass if user explicitly requests):
- `gpt-5.2-codex` - Default for Codex CLI, optimized for agentic coding (user's current config)
- `gpt-5.2` - Flagship model, best for complex professional tasks
- `gpt-5-mini` - Fast, cost-efficient (replaces o4-mini)
- `o3` - Deep reasoning model for complex multi-step problems

**Sandbox modes** (only pass if user explicitly requests):
- `read-only` - No file modifications allowed
- `workspace-write` - Can modify files in workspace
- `danger-full-access` - Full system access (use with caution)

**Default behavior:** Omit `--model` and `--sandbox` flags to use the user's `~/.codex/config.toml` preferences.

If no task description provided, ask the user what they want Codex to do.

## Assess Task Complexity

Based on the task description, determine context depth:

**Minimal context** (single file fix, simple query):
- Task mentions specific file or function
- Clear, scoped objective
- Example: "fix the type error in auth.ts", "add logging to handleRequest"

**Medium context** (feature work, multi-file change):
- Task involves a feature or component
- May touch multiple files
- Example: "add input validation to the API", "refactor error handling"

**Full context** (architectural, investigation, unclear scope):
- Task is exploratory or investigative
- Scope unclear or potentially large
- Example: "figure out why tests are flaky", "improve performance"

## Gather Context

### Git State (always include)

```bash
pwd
git rev-parse --show-toplevel 2>/dev/null || echo "Not a git repo"
git branch --show-current 2>/dev/null || echo "N/A"
git status --short 2>/dev/null | head -20
```

### For Medium/Full Context

```bash
git diff --stat 2>/dev/null | tail -20
git log --oneline -5 --since="4 hours ago" 2>/dev/null || echo "No recent commits"
```

### For Full Context Only

Summarize relevant session context:
- What was being worked on
- Key decisions or approaches discussed
- Files that were read or modified
- Any blockers or open questions

## Generate Codex Prompt

Create a prompt using **CTCO structure** (Context → Task → Constraints → Output format) optimized for GPT-5.2.

Structure:

```
<context>
Working directory: {cwd}
Repository: {repo_name}
Branch: {branch}

{git_status if relevant}
{recent_changes if medium/full context}
{session_summary if full context}
</context>

<task>
{task description from arguments}
</task>

<constraints>
- Implement EXACTLY and ONLY what is requested
- No extra features, refactoring, or "improvements" beyond the task
- Read relevant files before making changes
- Run tests/linters if available to validate changes
- If task is ambiguous, state your interpretation before proceeding
</constraints>

<output>
After completing the task, provide a structured summary (≤5 bullets):
- **What changed**: Files modified and nature of changes
- **Where**: Specific locations (file:line when relevant)
- **Validation**: Tests run, linters passed, manual verification
- **Risks**: Any potential issues or edge cases to watch
- **Next steps**: Follow-up work if any (or "None")
</output>
```

## Execute Codex

First, ensure output directory exists:

```bash
mkdir -p ~/.claude/codex/${CLAUDE_SESSION_ID}
```

Check if we're in a git repo:

```bash
git rev-parse --show-toplevel 2>/dev/null && echo "IN_GIT_REPO" || echo "NOT_GIT_REPO"
```

Build and run the command:

```bash
codex exec --json \
  -o ~/.claude/codex/${CLAUDE_SESSION_ID}/summary-{timestamp}.txt \
  {required_flags} \
  {optional_flags} \
  - <<'CODEX_PROMPT'
{generated_prompt}
CODEX_PROMPT > ~/.claude/codex/${CLAUDE_SESSION_ID}/progress-{timestamp}.jsonl
```

**Output handling:**
- `--json` streams progress events to stdout → redirected to `progress-{timestamp}.jsonl`
- `-o` writes only the final message → `summary-{timestamp}.txt`

**Flag rules:**
- **If NOT in a git repo:** add `--skip-git-repo-check` (required)
- **Default:** add `--full-auto` (enables workspace-write sandbox + auto-approval)
- **If user requests read-only:** use `--sandbox read-only` instead of `--full-auto`
- **If user requests specific model:** add `-m <model>`
- **If user requests danger-full-access:** use `--sandbox danger-full-access` instead of `--full-auto`

Run via Bash tool.

### Background vs Foreground

**Always background** tasks that might take >30 seconds:
- Any task touching multiple files
- Investigation/debugging tasks
- Tasks requiring test runs
- Feature implementations

Use `run_in_background: true` in the Bash tool call.

**After backgrounding:**
- Inform the user the task is running
- Do NOT immediately check output
- Wait for user to ask about status, OR continue with other work
- When checking, use the token-efficient methods below

**Foreground only** for trivial tasks (<30 seconds expected):
- Single-line fixes
- Simple file reads
- Quick queries

### Monitoring Execution

Two files are created:
- `progress-*.jsonl` - Streaming JSONL (verbose, for progress checking)
- `summary-*.txt` - Final message only (clean, for results)

**Token-efficient monitoring** (CRITICAL):

```bash
# Check if still running (line count growing = active)
wc -l < ~/.claude/codex/${CLAUDE_SESSION_ID}/progress-*.jsonl

# Quick progress check - last 3 events only
tail -n 3 ~/.claude/codex/${CLAUDE_SESSION_ID}/progress-*.jsonl

# Check if summary exists (means Codex finished)
ls ~/.claude/codex/${CLAUDE_SESSION_ID}/summary-*.txt 2>/dev/null
```

**Do NOT:**
- Read the entire progress file
- Use `tail -f` (streams indefinitely, wastes context)
- Check more than once per 30 seconds for long tasks

**When checking on background tasks:**
1. First: check if summary file exists (finished?)
2. If not finished: `wc -l` on progress file to confirm activity
3. If needed: `tail -n 3` on progress for current status

## Return Result

When Codex completes:

1. **Read the summary file** (already contains only the final message):
   ```bash
   cat ~/.claude/codex/${CLAUDE_SESSION_ID}/summary-*.txt
   ```
2. Parse Codex's structured summary
3. Report concisely to the user (3-6 sentences or ≤5 bullets)

Format:

```
## Codex Result

**Status:** {success/error/partial}

**What changed:**
- {file1}: {change summary}
- {file2}: {change summary}

**Validation:** {tests/linters run, results}

**Risks/Notes:** {if any, otherwise omit}

**Next steps:** {if any, otherwise "None"}
```

Keep the summary concise. If Codex produced verbose output, distill to essentials.

## Examples

### Simple fix
```
/codex fix the null pointer in utils/parser.ts line 42
```
Minimal context, quick execution.

### Feature implementation
```
/codex add rate limiting to the /api/submit endpoint
```
Medium context, may take a few minutes.

### Investigation
```
/codex investigate why the CI build fails on arm64
```
Full context, potentially long-running, consider backgrounding.

### With model override (only when explicitly requested)
```
/codex --model o3 design a caching strategy for the database queries
```

### Read-only mode (for review/analysis tasks)
```
/codex --sandbox read-only review the authentication implementation
```
Skips `--full-auto`, uses read-only sandbox for safe exploration.
