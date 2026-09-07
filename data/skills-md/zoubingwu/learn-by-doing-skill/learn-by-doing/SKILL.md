---
name: learn-by-doing
description: Use when a user wants to learn, practice, or improve programming by building real local projects, completing skeleton-code challenges, running tests, receiving hints, and tracking progress in a local workspace.
---

# Learn By Doing

Use this skill to guide a user through programming practice with real local projects. The agent generates a full staged roadmap first, then creates every planned challenge or project during setup.

## Core Rules

- Generate a complete roadmap before creating challenge files.
- Include multiple stages, and include planned challenges or projects in each stage.
- Keep the first challenge small enough to run quickly.
- Create every roadmap stage during setup.
- Proactively ask the user whether to use subagents before dispatching them, and explicitly recommend subagents for parallel batch generation.
- Use subagents to create stage or challenge batches in parallel after the user authorizes delegation and the tools are available.
- Use "skeleton + tests + README" as the default challenge shape.
- Let the user write the core implementation.
- Provide diagnosis and hints on failure.
- Require explicit user authorization before patching user implementation code.
- Require explicit user confirmation before running installation commands or changing machine-level configuration.
- Track progress in `.learn-by-doing/state.json`.
- Use English for generated challenge files unless the user asks for another language.

## Workflow

1. Intake
   - Ask for the learning target, current level, target workspace path, and project preference when useful.
   - Ask only for information needed to generate the initial roadmap.
   - Use a tiny diagnostic challenge when the user's level is unclear.

2. Infer tools
   - Convert the user's goal into a structured tool list.
   - Include the language runtime, package manager, build tool, test runner, common editor commands, and local services needed by the roadmap validation commands.
   - Select the available Python runner in this order when possible: `python3`, `python`, then `py`.
   - Call `scripts/detect_environment.py` with `--tools` and `--json`.

3. Explain environment
   - State the tools required for the current challenge.
   - State available and missing tools.
   - Explain the impact of missing tools.
   - Provide concise installation guidance and verification commands.
   - Ask for confirmation before installing anything.

4. Initialize or resume workspace
   - Use `scripts/state.py init <workspace> --goal "..." --level ...` for new workspaces.
   - Use `scripts/state.py show <workspace> --json` for existing workspaces.
   - Continue from the active challenge when state is clear.

5. Generate roadmap
   - Create a staged roadmap for the whole learning goal.
   - Include multiple stages and planned challenges or projects per stage.
   - Each stage needs an id, title, objective, challenge list, validation style, and completion criterion.
   - Each planned challenge needs an id, title, objective, expected outcome, and project shape.
   - Write the roadmap to a JSON file and persist it with `scripts/state.py set-roadmap`.
   - Use `scripts/state.py add-stage` to persist stages.

6. Generate all stages
   - Create challenge or project directories for every planned roadmap entry.
   - Before generating files, ask the user whether to use subagents for parallel generation.
   - Tell the user that subagents are recommended because they can create many challenges in parallel and make the full batch ready at once.
   - After authorization, dispatch one subagent per stage or per challenge batch to create `README.md`, skeleton code, tests, and validation instructions.
   - Give each subagent the assigned stage or challenge contracts, the shared project conventions, and strict output paths.
   - If the user chooses local generation or the current environment lacks subagent support, generate the full roadmap locally in manageable batches.
   - After generation, inspect the full curriculum for duplicated concepts, gaps in progression, inconsistent commands, missing files, and broken paths.
   - Each challenge directory contains `README.md`, skeleton code, tests, and one primary validation command.
   - Use `scripts/state.py add-challenge` to persist every generated challenge.
   - Mark the first challenge as `active`; keep every other generated challenge `pending`.
   - See `references/challenge-design.md` for the roadmap and challenge contracts.

7. Validate and guide
   - Run the validation command from each generated challenge directory when local tools make this practical.
   - At minimum, validate the active challenge and smoke-check the remaining generated projects for broken setup.
   - Classify failures and provide actionable hints.
   - Update challenge status with `scripts/state.py update-challenge`.
   - After a challenge passes, activate the next pending challenge.
   - See `references/feedback-policy.md` for feedback rules.

8. Dashboard
   - Generate `.learn-by-doing/dashboard.html` from state after the roadmap and all stages are created.
   - Use `scripts/render_dashboard.py <workspace>` for dashboard generation.
   - Show every roadmap stage, every generated challenge, active challenge, and pass/fail status.
   - Keep it static and local.

9. Final report
   - Tell the user how to use the dashboard.
   - Explain the current stage, current challenge, and what the learner will practice.
   - Tell the user how to start, how to validate, and how to continue or generate more challenges.
   - Keep implementation details concise; leave full file listings to the dashboard and challenge README files.
   - See `references/feedback-policy.md` for final report guidance.

## Script Usage

Use the available Python runner for the user's machine. Examples below use `python3`.

Environment probe:

```bash
python3 scripts/detect_environment.py --tools rustc,cargo,git,code --json
```

State management:

```bash
python3 scripts/state.py init <workspace> --goal "Learn Rust" --level beginner
python3 scripts/state.py show <workspace> --json
python3 scripts/state.py summary <workspace>
python3 scripts/state.py set-roadmap <workspace> --file roadmap.json
python3 scripts/state.py add-stage <workspace> --id stage-01 --title "CLI basics"
python3 scripts/state.py add-challenge <workspace> --stage-id stage-01 --id challenge-01 --title "Word counter" --path "stage-01-cli/word-counter" --test-command "cargo test"
python3 scripts/state.py add-challenge <workspace> --stage-id stage-01 --id challenge-02 --title "File parser" --path "stage-01-cli/file-parser" --test-command "cargo test"
python3 scripts/state.py update-challenge <workspace> challenge-01 --status passed --last-result "All tests passed"
python3 scripts/state.py set-environment <workspace> --file environment.json
python3 scripts/render_dashboard.py <workspace>
```

## State Contract

`.learn-by-doing/state.json` is the progress source of truth. Use scripts for regular writes.

Allowed challenge statuses:

- `pending`
- `active`
- `blocked`
- `failed`
- `passed`

Roadmap entries describe the complete learning route. During setup, every planned entry becomes a generated challenge or project and uses the challenge statuses above.
