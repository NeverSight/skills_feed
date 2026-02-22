---
name: uv
description: >
  Uses the uv Python package and project manager correctly for dependencies, venvs, and scripts.
  Use when creating or modifying Python projects, adding dependencies, running scripts with inline deps,
  managing virtual environments, pinning Python versions, running CLI tools from PyPI, setting the IDE Python interpreter,
  or using uv in CI (e.g. GitHub Actions) or Docker containers.
  Use when the user mentions uv, pyproject.toml, uv.lock, uv run, uv add, uv sync, .venv, Python interpreter, poetry, pipenv, conda, CI, Docker, GitHub Actions, or asks to use uv instead of pip or poetry.
---

# uv Package Manager

Prefer **uv** over pip/poetry for Python dependency and project management. Use the workflow below and choose the right mode (project, script, or tool).

## Mode Decision

```
User needs to...
│
├─ Repo uses poetry / pipenv / conda (poetry.lock, Pipfile, environment.yml)
│  → Ask: "This repo uses [poetry/pipenv/conda]. Do you want to switch to uv?"
│  → If yes: prefer the migrate-to-uv tool (uvx migrate-to-uv in project root) to convert metadata and lockfile; then uv sync. Remove legacy files only after user confirms.
│  → If no: do not use uv for project management; use the existing tool or uv pip only if appropriate.
│
├─ Repo has requirements.txt (no pyproject.toml)
│  → Ask: "This repo uses requirements.txt. Do you want to convert to uv (pyproject.toml + uv.lock)?"
│  → If yes: guide conversion (uv init, uv add from requirements, then uv sync)
│  → If no: use Pip-Compatible workflow (uv pip)
│
├─ Manage a project (pyproject.toml, lockfile, team repo)
│  → Use PROJECT workflow (uv init, uv add, uv sync, uv run)
│
├─ Run a single script with dependencies
│  → Use SCRIPT workflow (uv add --script, uv run <script>)
│
├─ Run a one-off CLI tool (no project)
│  → Use uvx: uvx <package> [args] or uv tool install <package>
│
└─ User declined conversion; existing pip/requirements workflow
   → Use uv pip (uv venv, uv pip sync, uv pip compile)
```

## Project Workflow

Use for apps, libraries, or any repo with `pyproject.toml`.

### New project

```bash
uv init [project-name]
cd [project-name]
uv add <package> [package2...]
uv sync
uv run python main.py
# or: uv run <any command>
```

### Existing project (already has pyproject.toml)

```bash
uv sync                    # install from lockfile (or resolve and lock)
uv add <package>           # add dependency, update lockfile and env
uv remove <package>       # remove dependency
uv run <command>          # run in project venv (creates .venv if needed)
uv lock                   # refresh lockfile only
```

### Pin Python version (optional)

```bash
uv python pin 3.11        # writes .python-version
uv python install 3.11    # ensure that version is available
```

**Rules:**

- Use `uv add` for project dependencies; avoid editing `pyproject.toml` by hand for deps when uv can do it.
- After changing dependencies, run `uv sync` (or rely on `uv add`/`uv remove` which update the env).
- Run project commands via `uv run` so the correct venv and env are used; do not assume `pip install` or manual activate.
- When creating a new project, ensure `.venv` is in `.gitignore` (uv init usually adds it; add it if missing).
- Treat `uv.lock` as a mandatory source-controlled artifact: commit it so all environments and CI use the same dependency versions; the lockfile is universal (one file for Windows, macOS, Linux).

## Script Workflow

For a single Python file that needs packages (no full project).

1. Add inline script metadata (or use `uv add --script` to add deps to the file):

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
import requests
print(requests.get("https://example.com"))
```

2. Add deps from CLI (updates the script file):

```bash
uv add --script example.py requests
```

3. Run with uv (creates an ephemeral env if needed):

```bash
uv run example.py
```

For executable scripts that run without typing `uv run`, use a shebang (PEP 723):

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
```

**Rules:**

- Use `uv add --script <file>` to declare dependencies for that script.
- Use `uv run <script>.py` to run it; do not tell the user to `pip install` first.
- For portability, scripts can use shebang `#!/usr/bin/env -S uv run --script`.

## Tools (one-off CLI from PyPI)

Run without installing globally:

```bash
uvx <package> [args]
# e.g. uvx ruff check .
# e.g. uvx pycowsay "hello"
```

Install the tool for repeated use:

```bash
uv tool install <package>
# e.g. uv tool install ruff
```

**Rules:**

- Prefer `uvx` for one-off runs; use `uv tool install` when the user will call the tool often.

## Repos Using requirements.txt

When the repo has **requirements.txt** (and no `pyproject.toml`):

1. **Ask the user:** "This repo uses requirements.txt. Do you want to convert to uv (pyproject.toml + uv.lock)?"
2. **If yes:** Guide conversion: `uv init`, then `uv add -r requirements.txt` (or, if you have requirements.in and locked requirements.txt, `uv add -r requirements.in -c requirements.txt` to preserve versions), then `uv sync`. Optionally remove or keep requirements.txt per user preference.
3. **If no:** Use the Pip-Compatible workflow below (no conversion).

Do not convert to uv without asking when the repo currently uses only requirements.txt.

## Pip-Compatible Workflow

For repos that still use `requirements.txt` or `pip` (and user did not want conversion):

```bash
uv venv                           # create .venv
uv pip sync requirements.txt      # install from locked requirements
uv pip compile requirements.in -o requirements.txt  # compile/lock
```

Use `uv pip` instead of `pip` for the same commands when you want speed and better resolution.

## CI and Docker

When the user asks about **uv in CI** (e.g. GitHub Actions) or **uv in Docker**, advise using the patterns below and point to [references/docker-and-ci.md](references/docker-and-ci.md) for full detail.

**CI (e.g. GitHub Actions):**
- Install uv with the official `astral-sh/setup-uv` action; use cache keyed by `uv.lock` and `pyproject.toml`.
- Run `uv sync --locked` so the job fails if the lockfile is out of sync (no silent deploy of untested deps).
- Optionally run `uv cache prune --ci` at end of job to keep cache lean.

**Docker:**
- Use a multi-stage build: builder stage with `ghcr.io/astral-sh/uv`, copy only `uv.lock` and `pyproject.toml` first, run `uv sync` (or equivalent), then copy `.venv` and app code into a slim runtime image (no uv/Rust in final image).
- Set `UV_COMPILE_BYTECODE=1` and `UV_LINK_MODE=copy` in the build stage; use `--no-editable` when syncing so the final image doesn’t depend on source.
- Run the container as a non-root user when possible.

For step-by-step Dockerfiles and CI workflow examples, see [references/docker-and-ci.md](references/docker-and-ci.md).

## IDE Setup (Use uv .venv)

After uv creates or uses a project `.venv`, **automatically try** to configure the IDE to use that interpreter so run/debug and IntelliSense use the same environment.

1. **Target:** Workspace settings (project-scoped, shareable): `.vscode/settings.json`
2. **Setting:** `python.defaultInterpreterPath` pointing at the project’s `.venv`:
   - Linux/macOS: `"${workspaceFolder}/.venv/bin/python"`
   - Windows: `"${workspaceFolder}/.venv/Scripts/python.exe"`
3. **Behavior:** If `.vscode/settings.json` exists, read it, add or update only `python.defaultInterpreterPath`, then write back. If it doesn’t exist, create `.vscode/` and the file with this setting. Preserve all other keys.
4. **When:** After `uv init`, `uv sync`, or conversion from requirements.txt that creates/updates `.venv`.

**Rules:**

- Use workspace settings (`.vscode/settings.json`), not user settings, so the choice is per-project and can be committed.
- Do not overwrite or remove other settings in the file.
- If the workspace already has a Python interpreter selected, still add/update this key so the project’s `.venv` is the default.

## Automation and Agent Behavior

1. **New Python project:** Run `uv init` (or `uv init <name>`), then `uv add` for initial deps, then `uv sync`. Suggest `uv run` for run/test commands.
2. **Add dependency:** Use `uv add <package>`. For dev/optional: `uv add --dev <package>`.
3. **Run something:** Use `uv run <command>` in a project; `uv run script.py` for scripts; `uvx <tool>` for one-off tools.
4. **No manual venv activate:** Prefer `uv run` so the agent and user don’t depend on `source .venv/bin/activate`.
5. **Lockfile:** Commit `uv.lock`; treat it as mandatory for parity. After pull or after editing deps, run `uv sync`. In CI, use `uv sync --locked` so the job fails if the lockfile is out of sync with `pyproject.toml`.
6. **Detecting uv:** If `pyproject.toml` exists and there is no poetry/pipenv/conda (no poetry.lock, Pipfile, environment.yml), assume uv is allowed and suggest uv commands. If the user said "use uv", always prefer uv over pip/poetry. If poetry/pipenv/conda is present, ask before switching to uv (see Mode Decision).
7. **requirements.txt only:** If the repo has requirements.txt but no pyproject.toml, ask whether the user wants to convert to uv before converting or using uv pip.
8. **IDE interpreter:** After uv creates or syncs `.venv`, try to set the workspace Python interpreter by adding or updating `python.defaultInterpreterPath` in `.vscode/settings.json` (see IDE Setup above).

## Common Commands Reference

| Task              | Command                    |
|-------------------|----------------------------|
| New project       | `uv init [name]`           |
| Add dependency    | `uv add <pkg>`             |
| Add dev dependency| `uv add --dev <pkg>`       |
| Remove dependency | `uv remove <pkg>`          |
| Install from lock | `uv sync`                  |
| Update lockfile   | `uv lock`                  |
| Run in project    | `uv run <cmd>`             |
| Run script        | `uv run script.py`        |
| Run CLI tool once | `uvx <pkg> [args]`         |
| Install tool      | `uv tool install <pkg>`    |
| Create venv       | `uv venv`                  |
| Pin Python        | `uv python pin 3.11`       |
| Install Python    | `uv python install 3.11`   |

## Additional Resources

- Full CLI and options: [references/cli-and-commands.md](references/cli-and-commands.md)
- Example flows: [references/examples.md](references/examples.md)
- Common issues and fixes: [references/troubleshooting.md](references/troubleshooting.md)
- Docker and CI: [references/docker-and-ci.md](references/docker-and-ci.md)
- Workspaces (monorepos) and resolution: [references/workspaces-and-resolution.md](references/workspaces-and-resolution.md)
