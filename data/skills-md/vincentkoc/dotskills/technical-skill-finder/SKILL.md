---
name: technical-skill-finder
description: Mine coding agent logs (Codex/Cursor/session histories and similar telemetry) to discover high-value candidate skills, then draft structured skill creation/reuse recommendations.
license: AGPL-3.0-only
metadata:
  source: "https://github.com/vincentkoc/dotskills"
---

# Technical Skill Finder

## Purpose

Find recurring pain points from local agent logs and convert them into actionable skill candidates, reuse opportunities, or existing skill updates.

## When to use

- You want to discover missing technical skills from historical agent activity.
- You want reproducible criteria before creating a new skill.
- You want to validate whether an existing skill already covers the pattern.
- You want to include optional personal-signal sources (when authorized).

## Inputs

- `SCOPE` (required): repository paths, workspace, or tool domains to inspect.
- `SOURCES` (required): ordered source list to mine.
- `TIMEFRAME` (optional): default `all` unless constrained by user.
- `PRIVACY_POLICY` (required): explicit user direction for personal logs.
- `TOP_N` (optional): number of highest-priority candidates to return.

## Workflow

1. Initialize source set
   - `~/.codex/history.jsonl`
   - `~/.codex/archived_sessions/*.jsonl`
   - `~/.codex/sessions/*.jsonl` and `~/.codex/log/*` if present
   - Repository-specific telemetry in `AGENTS.md`/local docs when available
   - `Cursor` / `Codex` agent logs detected under known dotfiles directories
2. Normalize extraction signals
   - Parse stack traces and classify failure type (`auth`, `type-check`, `llm-error`, `git/ci`, `runtime`, `refactor-merge`, `test`)
   - Parse recurring command phrases (`rg`, `mypy`, `pytest`, `gh`, `git`, package-manager failures)
   - Record frequency, recency, and affected project context
3. Cluster signals
   - Group by: domain (python/js/rust/docs/tooling), command lineage, and error signature.
   - Deprioritize one-off sessions with low recurrence.
4. Map to existing skills
   - Compare candidate clusters with available skills by `name` and `description`.
   - If overlap is high, propose **skill update** path.
   - If no overlap, propose **new skill**.
5. Emit ranking output
   - Provide `impact`, `frequency`, `confidence`, `skill-fit`, and first-apply command set.
6. Produce minimal first-iteration artifacts for high-priority candidates
   - Candidate title + scope
   - Trigger phrase examples
   - Required inputs
   - Suggested workflow summary
   - Evidence snippets (line/file-level)
   - Suggested dependencies/tools (e.g., `jq`, `rg`, shell utilities, MCP resources)
7. Optional extension to personal-signal sources
   - Only after explicit approval to read personal channels.
   - If MCP is available and user has granted access, run MCP resource discovery and include message-signal-derived patterns.
   - Keep this opt-in and isolated from coding-signal output unless user requests a merged plan.

## Guardrails

- Never infer or emit private content from message logs unless explicitly permitted.
- Skip binary/corrupt files and summarize only parseable text sources.
- Prefer deterministic commands and small scripts over ad-hoc manual parsing.
- Always avoid proposing skills with unresolved operational context (credentials, environment, private URLs).
- If evidence is ambiguous, return `confidence: low` and request one more session sample.

## Outputs

- `skill_candidates.md`-style report in chat:
  - `reuse` candidates (existing skill can be extended)
  - `new` skill candidates (not yet covered)
  - top source anchors with references
  - recommended next action (create/update)

Read `references/sources.md` for source precedence.
Read `references/scorecard.md` for prioritization rules.
