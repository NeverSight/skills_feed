---
name: crunch-compete
description: Use when working with Crunch competitions - setting up workspaces, exploring quickstarters, testing solutions locally, or submitting entries.
---

# Cruncher Skill

Guides users through Crunch competition lifecycle: setup, quickstarter discovery, solution development, local testing, and submission.

## Prerequisites
- Python 3.9+ with `venv` module (included in standard Python)
- `pip` for package installation

## Package Installation

This skill installs Python packages from [PyPI](https://pypi.org) into isolated virtual environments:

| Package | Source | Purpose |
|---------|--------|---------|
| `crunch-cli` | [PyPI](https://pypi.org/project/crunch-cli/) | CrunchDAO competition CLI (setup, test, submit) |
| `jupyter` | [PyPI](https://pypi.org/project/jupyter/) | Notebook support (optional) |
| `ipykernel` | [PyPI](https://pypi.org/project/ipykernel/) | Jupyter kernel registration (optional) |
| Competition SDKs (e.g. `crunch-synth`, `birdgame`) | PyPI | Competition-specific libraries (varies) |

**Agent rules for package installation:**
- **Always use a virtual environment** — never install into system Python
- **Only install known packages** listed above or referenced in competition docs (PACKAGES.md)
- **Ask the user before installing** any package not listed here
- **All packages are from PyPI** — no custom URLs, no `--index-url` overrides, no `.whl` files from unknown sources


## Credentials

### Submission Token (required for setup & submit)
- **How to get:** User logs into [CrunchDAO Hub](https://hub.crunchdao.com), navigates to the competition's submit page (`/competitions/<competition>/submit`), and copies their token
- **How it's used:** Passed once via `--token <TOKEN>` during `crunch setup`
- **Persistence:** After setup, the CLI stores the token in the project's `.crunch/` config directory. All subsequent commands (`crunch test`, `crunch push`, `crunch download`) authenticate automatically — no need to pass the token again
- **If token expires:** Run `crunch update-token` inside the project directory to refresh it

**Agent rules for tokens:**
- **Always ask the user** to provide the token — never assume, guess, or reuse tokens from other projects
- **Never write tokens** into source files, scripts, notebooks, or any committed file
- **Never log or echo tokens** in shell output (use `--token <TOKEN>` placeholder in examples shown to user)
- Tokens are user-specific and project-scoped — each `crunch setup` call requires the user to supply one

### GitHub API (optional, unauthenticated)
- Used only for browsing quickstarter listings via `api.github.com` (public repo, no auth needed)
- Rate-limited to 60 requests/hour per IP; sufficient for normal use

## Network Access

| Operation | Requires network | Endpoint |
|-----------|-----------------|----------|
| `crunch setup` | Yes | hub.crunchdao.com |
| `crunch push` | Yes | hub.crunchdao.com |
| `crunch download` | Yes | hub.crunchdao.com |
| `crunch test` | **No** | Local only |
| `crunch list` | Yes | hub.crunchdao.com |
| `pip install` | Yes | pypi.org |
| Quickstarter browsing | Yes | api.github.com |

## Quick Setup

**Each competition needs its own virtual environment** (dependencies can conflict).

```bash
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
python -m venv .venv && source .venv/bin/activate 
pip install crunch-cli jupyter ipykernel --upgrade --quiet --progress-bar=off
python -m ipykernel install --user --name <competition> --display-name "Crunch - <competition>"

# Get token from: https://hub.crunchdao.com/competitions/<competition>/submit
crunch setup <competition> <project-name> --token <TOKEN>
cd <competition>-<project-name>
```

For competition-specific packages and full examples, see [references/competition-setup.md](references/competition-setup.md).

## Core Workflow

### 1. Discover
```bash
crunch list                    # List competitions
```


### 2. Explain
Read the quickstarter code (`main.py` or notebook) and competition's SKILL.md/README.md. Provide walkthrough covering: Goal, Interface, Data flow, Approach, Scoring, Constraints, Limitations, Improvement ideas.

### 3. Propose Improvements
Analyze current approach, cross-reference competition docs (SKILL.md, LITERATURE.md, PACKAGES.md), generate concrete code suggestions:
- Model: mixture densities, NGBoost, quantile regression, ensembles
- Features: volatility regimes, cross-asset correlation, seasonality
- Architecture: online learning, Bayesian updating, horizon-specific models

### 4. Test
```bash
crunch test                    # Test solution locally
```

### 5. Submit
```bash
crunch test                    # Always test first
crunch push -m "Description"   # Submit
```

## Phrase Mapping

| User says | Action |
|-----------|--------|
| `what competitions are available` | `crunch list` |
| `show quickstarters for <name>` | Fetch from GitHub API |
| `set up <competition>` | Full workspace setup |
| `download the data` | `crunch download` |
| `get the <name> quickstarter` | `crunch quickstarter --name` |
| `explain this quickstarter` | Structured code walkthrough |
| `propose improvements` | Analyze and suggest code improvements |
| `test my solution` | `crunch test` |
| `compare with baseline` | Run both, side-by-side results |
| `submit my solution` | `crunch push` |

## Important Rules

- Entrypoint must be `main.py` (default for `crunch push`/`crunch test`)
- Model files go in `resources/` directory
- Respect competition interface and constraints (time limits, output format)
- Ask before installing new packages

## Reference

- CLI commands: [references/cli-reference.md](references/cli-reference.md)
- Setup examples: [references/competition-setup.md](references/competition-setup.md)
