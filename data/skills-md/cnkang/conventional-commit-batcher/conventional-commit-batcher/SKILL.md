---
name: conventional-commit-batcher
version: 1.0.0
description: Auto-split mixed changes into logical commit batches with validated Conventional Commit messages
---

# Conventional Commit Batcher

Use this skill to turn a messy working tree into clean, reviewable Conventional Commit history.

## Use This Skill When

- changes from different intents are mixed in one branch
- you want a plan-first commit process before opening a PR
- you need reliable Conventional Commit messages across team and agents

## Skip This Skill When

- the change is tiny and clearly single-intent
- you only need one quick commit without batching

## High-Success Prompt

```text
Inspect my current git changes and split them into logical Conventional Commit batches.
Output a full Commit Plan first.
Do not run git add or git commit until I confirm the plan.
After confirmation, execute each batch one by one.
```

## Output Contract (Required)

Before any staging or committing, always output:

```text
Commit Plan
Batch #1: <type(scope): subject>
Intent: <why this batch exists>
Files/Hunks:
- <path> (...)
Staging commands:
- git add ...
Commit command:
- git commit -m "..."
```

## Required Behavior

- Always load `references/core-rules.md` first.
- Treat `references/core-rules.md` as the single source of truth.
- Run `python3 scripts/precommit_safety_gate.py` before every commit attempt
  when Python is available; otherwise run the equivalent manual gate checks
  from `references/core-rules.md`.
- Run the sensitive-data gate before every commit and require explicit user
  confirmation if risky files/hunks are detected.
- When any gate reports risk, include triggered file paths and brief evidence
  in user-facing output, plus a concrete "please review" suggestion.
- Run the `.gitignore`/local-artifact gate before every commit and require
  explicit user confirmation if suspicious files are present.
- Run branch/conflict/large-file/empty-stage safety checks before every commit.
- Never skip commit-time checks with `--no-verify`.
- If check/hook fails, stop and report concise diagnostics.

## Entrypoints

- Codex skill: `SKILL.md`
- Codex repo loader: `AGENTS.md`
- Claude: `CLAUDE.md`, `.claude/agents/conventional-commit-batcher.md`, `.claude/commands/commit-batch.md`
- Kiro: `.kiro/agents/conventional-commit-batcher.json`, `.kiro/steering/commit-batching.md`
- Shared skill (Kimi / Qwen / Gemini): `.agents/skills/conventional-commit-batcher/SKILL.md`
- Shared subagent (Qwen / Gemini): `.agents/agents/conventional-commit-batcher.md`
- OpenAI: `agents/openai.yaml`

## References

- Canonical rules: `references/core-rules.md`
- Commit plan examples: `references/plan-examples.md`
- Commit batching guidance: `references/commit-batching-guide.md`
- commit-msg hook example: `references/commit-msg-hook-example.md`
- Agent setup docs:
  - `references/codex-setup.md`
  - `references/claude-setup.md`
  - `references/kiro-setup.md`
  - `references/kimi-setup.md`
  - `references/qwen-setup.md`
  - `references/gemini-setup.md`
- Validator script: `scripts/validate_conventional_commit.py`
- Safety gate script: `scripts/precommit_safety_gate.py`
- Validator tests: `scripts/test_validate_conventional_commit.py`
- Safety gate tests: `scripts/test_precommit_safety_gate.py`
