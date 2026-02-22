---
name: python-pep8-coach
description: "Review and verify Python code against PEP 8 using flake8, and optionally apply safe formatting fixes with black after explicit user confirmation. Use when users ask to check style compliance, lint Python files, or fix PEP 8 issues in a target folder."
---

# Python PEP 8 Coach

## Purpose

Use this skill to audit and improve Python style compliance with PEP 8.

Primary tools:

- `flake8` for lint diagnostics
- `black` for optional, safe automated formatting fixes

## Local References

This skill includes reference material in:

- `references/pep-0008.md` (canonical PEP 8 style guide)

Use this file as source context when resolving style disputes or choosing
between strict PEP 8 and project-specific conventions.

## When To Use

Use this skill when the user asks to:

- review Python code for PEP 8 compliance
- identify style violations in one file or folder
- apply style fixes while minimizing manual edits
- standardize formatting consistently across Python files

## Default Behavior

- Scope defaults to a user-specified folder.
- Do not change code outside the requested path.
- If the requested scope is repository root, confirm before scanning/editing broadly.
- Run checks first and report findings before editing.
- Ask for explicit confirmation before applying fixes.
- Apply automatic fixes only when user approves.
- Re-run format and lint checks after formatting and report remaining issues.

Mode selection:

- Default to **strict PEP 8** unless project config or user request indicates Black.
- Use **Black-compatible mode** when repository conventions require Black.

## Workflow

1. Confirm target path (file or folder) from user input.
2. Verify tool availability (`flake8 --version`, `black --version`).
3. Detect style mode from user instruction and project config (`pyproject.toml`, `setup.cfg`, `.flake8`, `tox.ini`).
4. Run diagnostics:
     - Strict PEP 8 mode:
         - `flake8 <target> --max-line-length 79 --exclude=.venv,build,dist,__pycache__`
     - Black-compatible mode:
         - `black --check --line-length 88 <target>`
         - `flake8 <target> --max-line-length 88 --extend-ignore=E203,W503 --exclude=.venv,build,dist,__pycache__`
5. Summarize results by file and error code.
6. Ask for confirmation before edits.
7. If approved, apply formatting:
     - Strict PEP 8 mode: propose manual edits or minimal safe fixes (no semantic refactor).
     - Black-compatible mode: `black --line-length 88 <target>`
8. Re-run:
     - Strict PEP 8 mode:
         - `flake8 <target> --max-line-length 79 --exclude=.venv,build,dist,__pycache__`
     - Black-compatible mode:
         - `black --check --line-length 88 <target>`
         - `flake8 <target> --max-line-length 88 --extend-ignore=E203,W503 --exclude=.venv,build,dist,__pycache__`

## Style Policy

Strict PEP 8 baseline (from reference):

- Code line length: 79 characters.
- Comments/docstrings line length: 72 characters.
- Indentation: 4 spaces (spaces preferred over tabs).
- Use blank lines per PEP 8 conventions (2 between top-level defs, 1 between methods).

Black-compatible policy (project-specific):

- Code line length: 88 characters.
- Ignore `E203` and `W503` in `flake8`.
- Use when project already standardizes on Black.

## Safety Rules

- Never auto-edit without explicit user confirmation.
- Never apply semantic refactors as part of auto-fix.
- Keep changes limited to formatting and whitespace normalization.
- Exclude obvious non-target paths when needed (`.venv`, `build`, `dist`, caches).
- If strict PEP 8 mode is requested, do not force Black defaults.

## Missing Dependency Handling

If `flake8` or `black` is missing:

1. Inform the user exactly which tool is unavailable.
2. Ask permission to install with pip in the active environment.
3. If user declines, provide manual install commands and stop safely.
4. If user approves, install only the missing tool(s) and re-run diagnostics.

## Output Expectations

When reporting, provide:

- analyzed scope
- command(s) run
- number of files checked
- key lint categories found
- whether fixes were applied
- post-fix remaining issues (if any)

If no violations are found, return a short success summary.

## Examples

### Scenario 1: Auditing a single file

**User:** "Can you check `script.py` for style issues?"

**Agent Reference:**

1.  Check diagnostics:
    ```bash
    flake8 script.py --max-line-length 79
    ```
2.  Report: "Found 3 issues in `script.py`: E231 missing whitespace, E302 expected 2 blank lines. Would you like me to fix them?"
3.  User: "Yes."
4.  Apply minimal safe formatting fixes and re-run `flake8`.

### Scenario 2: Black-compatible repository

**User:** "Format `src/` according to our Black setup and verify lint."

**Agent Reference:**

1.  Check and report summary first.
    ```bash
    black --check --line-length 88 src/
    flake8 src/ --max-line-length 88 --extend-ignore=E203,W503
    ```
2.  "Checked 12 files. Found 45 violations. Proceed with formatting?"
3.  User: "Go ahead."
4.  Apply fixes:
    ```bash
    black --line-length 88 src/
    ```

### Scenario 3: Strict PEP 8 in directory

**User:** "Fix PEP 8 issues in `src/` without Black rules."

**Agent Reference:**

1.  Run strict diagnostics:
    ```bash
    flake8 src/ --max-line-length 79
    ```
2.  Summarize violations by file/code and ask approval.
3.  Apply only approved, non-semantic edits and re-run strict diagnostics.