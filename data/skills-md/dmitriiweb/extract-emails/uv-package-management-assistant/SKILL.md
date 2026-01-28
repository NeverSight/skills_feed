---
name: uv-package-management-assistant
description: python's package managing
alwaysApply: false
---

# uv Package Management Assistant

## Quick start
- Use `uv` for all Python dependency tasks; do not use `pip`, `pip-tools`, or `poetry`.
- Add or upgrade with `uv add <package>`; remove with `uv remove <package>`.
- Sync from the lockfile with `uv sync` (or `uv sync --all-extras` when extras are needed).
- Run scripts with the right env using `uv run <script.py>` and manage script-specific deps via `uv add/remove --script`.
- See `references/uv_rules.md` for full command guidance and script metadata examples.

## Workflow
1) **Manage project dependencies**  
   - Add/upgrade: `uv add <package>`  
   - Remove: `uv remove <package>`  
   - Resync from lock: `uv sync` (or `uv sync --all-extras` to include optional deps for development).  

2) **Run apps and scripts**  
   - Execute with `uv run <script.py>` to ensure dependencies are resolved.  
   - Manage script-only deps with `uv add --script <script.py> <package>` or `uv remove --script <script.py> <package>`.  

3) **Inline script metadata**  
   - Optionally define script requirements inline (see reference).  
   - Reinstall script deps from lock with `uv sync --script <script.py>`.  

4) **Do not**  
   - Avoid `pip install`, `pip-tools`, `poetry`, or mypy's install-missing-libraries prompts. Stick to `uv`.  

## Reference
- `references/uv_rules.md`: allowed commands, examples, and script metadata template.
