---
name: codex
description: Invokes OpenAI Codex CLI for an independent second opinion from a different model family. Use when (1) reviewing plans, diffs, code, or architecture decisions before acting, (2) doing a fresh pass on code or an entire codebase for bugs, edge cases, or missing requirements, (3) sanity-checking work before sharing with users or stakeholders, (4) wanting a competing perspective on trade-offs or design choices.
context: fork
user-invocable: true
model: opus
allowed-tools:
  - Glob
  - Grep
  - Read
  - Bash(codex:*)
  - Bash(git diff:*)
  - Bash(cat:*)
---

# Codex Second Opinion

Use Codex to get an independent review from OpenAI's reasoning models.

Use when:

- You want a second opinion on a plan, diff, or architecture decision.
- You need a fresh pass for bugs, edge cases, or missing requirements.
- You want a quick sanity check before sharing with users or stakeholders.

## Invocation

Use `codex exec` for non-interactive execution. The prompt can be passed as an argument or piped via stdin.

```bash
# Direct prompt
codex exec "Read the files in src/ and review them for bugs"
```

```bash
# Pipe via stdin
git diff main..HEAD | codex exec "Review this diff for issues"
```

## Key Options

- `-m MODEL`: Select model (always use the most capable available: `gpt-5.2-codex`)
- `-c key=value`: Override config values inline (e.g., `-c model="gpt-5.2-codex"`)
- `-p PROFILE`: Use a config profile from `~/.codex/config.toml` to avoid repeating flags
- `-C DIR`: Set working directory
- `--full-auto`: Automatic execution with workspace-write sandbox (fewer approval pauses)
- `-s SANDBOX_POLICY`: Sandbox policy (`read-only`, `workspace-write`)
- `--skip-git-repo-check`: Skip repo detection (saves time outside git)

## Workflow

1. **Gather context**: Identify the files, plans, or diffs Codex needs
2. **Define the objective**: What does “good” look like? Include constraints and acceptance criteria
3. **Compose a focused prompt**: Be specific about what to review and what feedback you want
4. **Invoke Codex**: Use `codex exec` with appropriate options
5. **Report findings**: Present Codex's feedback to the user with your own assessment of which points are valid

## Model Policy

- Prefer `gpt-5.2-codex`; if unavailable, use `gpt-5.2`.
- If neither is available in this environment, select the strongest model supported by `codex` and note the fallback.

## Safety and Scope

- Default to `-s read-only` for review-only tasks.
- Use `workspace-write` only when Codex needs to run tests or inspect generated artifacts.
- Never pass secrets, tokens, or private customer data.

## Prompt Guidelines

- State the review goal explicitly (e.g., "find logical errors", "evaluate scalability", "check for missing edge cases")
- Include constraints or requirements Codex should check against
- Ask for structured output (numbered issues, severity levels) for actionable feedback
- Ask for concrete references (file:line) when reviewing code or diffs

## Interpreting Results

- Treat Codex feedback as a second opinion, not authority.
- Verify any claims that seem uncertain or conflict with known constraints.
- Prefer actionable items: bugs, regressions, missing tests, and unclear requirements.

## Prompt Examples

### Plan Review

```bash
cat plan.md | codex exec -m gpt-5.2-codex -s read-only \
"Review this plan for risks, missing steps, and unclear assumptions.
Return:
1) Critical issues
2) Medium risks
3) Suggested improvements
4) Questions to clarify"
```

### Diff Review

```bash
git diff main..HEAD | codex exec -m gpt-5.2-codex -s read-only \
"Review this diff for bugs, regressions, security issues, and missing tests.
Return numbered findings with severity and file:line references."
```

### Architecture Review

```bash
cat design.md | codex exec -m gpt-5.2-codex -s read-only \
"Evaluate this architecture for scalability, fault tolerance, and operational risk.
Call out assumptions and suggest alternatives where applicable."
```

### Large Codebase Review

```bash
codex exec -m gpt-5.2-codex -s read-only \
"Review the codebase with focus on correctness, edge cases, and missing tests.
Read these folders: src/, scripts/, and packages/.
Return numbered findings with severity and file:line references."
```
