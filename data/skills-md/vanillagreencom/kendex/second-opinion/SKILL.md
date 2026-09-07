---
name: second-opinion
description: "Load for a cross-model review, challenge, audit, or quick consult."
summary: "Cross-model second opinion: review, challenge, audit, and consult through an external AI CLI (Claude and Codex)."
license: MIT
user-invocable: true
argument-hint: "review [scope] | challenge [description] | audit [path] | quick [question]"
metadata:
  author: vanillagreen
  source: kendex
  repository: "https://github.com/vanillagreencom/kendex"
  bugs: "https://github.com/vanillagreencom/kendex/issues"
  version: "1.0.0"
tags: [review]
---

<!-- kendex:project-instructions:start -->
## Project Instructions

<!-- kendex:shared-instructions:start -->
Problems with a kendex-owned skill go through `kendex report`; check ownership in the file first.
<!-- kendex:shared-instructions:end -->
<!-- kendex:project-instructions:end -->

# Second Opinion

Cross-model second opinion via external AI CLI. Every mode walks the `SECOND_OPINION_MODELS` roster in priority order and takes the first target that is available and runs a different model: Codex from a Claude Code session, Claude from a Codex session; when nothing eligible remains the run refuses and says why. Full contract: `second-opinion --help`.

```bash
.agents/skills/second-opinion/scripts/second-opinion <mode> [options]
```

## Workflows

| Command | Workflow | Output |
|---------|----------|--------|
| `review [scope]` | [workflows/review.md](workflows/review.md) | Review finding JSON |
| `challenge [description]` | [workflows/challenge.md](workflows/challenge.md) | Structured critique (text) |
| `audit [path]` | [workflows/audit.md](workflows/audit.md) | Review finding JSON |
| `quick [question]` | [workflows/quick.md](workflows/quick.md) | Text response |
| `detect` | (built-in) | Target name(s) a review would run |

## Execution Rules

- Execute all workflow sections in order. The workflow decides what to skip via "**Skip if**" conditions. Never skip based on your own scope assessment.
- `<output_format>` tags are literal templates: fill `[PLACEHOLDERS]`, omit empty lines, add nothing else, do not paraphrase.
- **Pass `--target`** when the user explicitly requests a specific model/CLI (e.g., "use Claude", "ask Codex"). Otherwise omit it. The script selects from the roster and the current session's model. A forced target that runs this session's model is refused; report the refusal, do not work around it.
- **Do not pass `--timeout`** unless the user explicitly asks for a different value for this specific call. The script reads the default from project config.
- **Always pass `--cwd`** with the absolute project root path. Never use `--cwd .`.
- Pass `--foreground` when the call can outlast the harness foreground cap. This detaches the run and prints its artifact, deadline, and wait command.
- Execute the exact printed wait command and follow its exit handling in `second-opinion --help` until terminal.
- For `quick` mode, you can pass the question inline: `.agents/skills/second-opinion/scripts/second-opinion quick "your question here" --cwd /path --foreground`.

## Session identity

Cross-model is enforced in every mode: a run with no eligible target exits 1 naming every candidate and its reason, writing nothing and invoking nothing. In a multi-model front end (Pi, OpenCode, Cursor) or an undetected harness, export `SECOND_OPINION_CURRENT_MODEL` in that session's own environment (`none` when there is no session model), never in a project settings file. Identity resolution, normalization, and the refusal rules: `second-opinion --help`.

## Multi-lane review

`SECOND_OPINION_COUNT` of 2 or more makes `review` run up to that many distinct eligible models in parallel on one pinned scope and write a single union artifact. Lane resolution, merge rules, artifact placement and permissions, scratch durability, and the failure taxonomy: [references/multi-lane.md](references/multi-lane.md).

## Configuration

Set non-sensitive defaults in `kendex.settings.toml` under `[env]`; `.env.local` wins over it, and a `.env` file is never read. `SECOND_OPINION_FOREGROUND_CAP` is session-only; a project-file foreground-cap declaration is refused, and shipped workflows pass `--foreground` directly. This skill marks no key `# required`, so an install writes nothing into `kendex.settings.toml`; assign a key there only to change a default the scripts already read (`SECOND_OPINION_TARGET` has none). Keys, defaults, and the built-in `claude`/`codex` commands: `second-opinion --help`.

## Error Handling

On script failure, stderr carries a JSON error object (`{"error": "description", "target": "codex"}`) or a plain `Error:` line for pre-flight configuration errors; exit codes, preserved-response paths, and the output-clearing/ownership rules are in `second-opinion --help`. Report the stated reason. An ineligible-target refusal is fixed by installing the CLI or adjusting `SECOND_OPINION_<NAME>_CMD`, `SECOND_OPINION_MODELS`, or `SECOND_OPINION_CURRENT_MODEL`, never by forcing the same model. For a timeout, suggest a larger `--timeout` or a narrower `--range`.

If the script fails during the orch `review-pr` or `submit-pr` (local pre-PR review) workflows, **continue**. External review is advisory.
