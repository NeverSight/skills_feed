---
name: format-lint-assistant
description: Run the project's formatter, linters, and mypy checks in the required order, fixing issues and managing any needed stub dependencies via uv.
---

# Format and Lint Assistant

## Quick start
- Run `make format` before linting to apply project formatting.
- Run `make lint`; fix linter errors first, rerun `make lint`, then address any remaining mypy issues.
- If mypy needs missing stubs/libs, add them with `uv add --dev <package>` so they land in `pyproject.toml`; never use mypy's install-missing-libraries command.
- Keep rerunning `make lint` until it passes cleanly; share any unresolved issues.
- See `references/linting_rules.md` for the exact workflow.

## Workflow
1) **Prepare and format**  
   - Review the scope of files to format/lint.  
   - Run `make format` to apply formatting before linting.  

2) **Lint and iterate**  
   - Run `make lint`.  
   - If linters fail, fix those issues first and rerun `make lint` to confirm the lint portion is clean.  
   - After lint fixes, address mypy errors reported by the same command, then rerun `make lint` to verify.  

3) **Manage dependencies**  
   - When mypy reports missing libraries or type stubs, add the needed package with `uv add --dev <package>` so it updates the dev dependencies in `pyproject.toml`.  
   - Do **not** use mypy's automatic install-missing-libraries flag.  

4) **Validate and report**  
   - Run `make lint` once more after all fixes to ensure a clean result.  
   - Summarize what was run, what was fixed, and call out any remaining issues.  
