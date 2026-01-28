---
name: agents-md-assistant
description: Inspect a repository and draft an AGENTS.md file using the standard template, capturing commands, structure, and workflow rules.
---

# AGENTS.md Assistant

## Quick start
- Review `README.md`, `CONTRIBUTING.md`, and docs/CI configs to learn the intended workflow.
- Pull exact commands from build scripts (`Makefile`, `package.json`, `pyproject.toml`, `justfile`).
- Map key directories (source, tests, docs, scripts) and mark generated or vendor paths.
- Capture architecture: key entrypoints, components, and configuration locations.
- Fill unknowns with TODOs and confirm them with the user.

## Workflow
1) **Inspect the repository**  
   - Read `README.md`, `CONTRIBUTING.md`, and `/docs` for goals and workflows.  
   - Check build/config files: `Makefile`, `package.json`, `pyproject.toml`, `justfile`, `Dockerfile`, CI pipelines.  

2) **Extract commands**  
   - Record install, dev, lint, format, typecheck, test, and build commands exactly as documented.  
   - If multiple options exist, capture the preferred default and note alternates.  

3) **Map structure**  
   - Identify primary code, tests, docs, scripts, and generated/ignored folders.  
   - Note where key configs live and any build artifacts to avoid editing.  

4) **Summarize architecture & environment**  
   - Document key components, data flow, and entrypoints.  
   - Capture required versions, services, env vars, and migration/seed steps.  

5) **Author AGENTS.md**  
   - Use `references/agents_md_template.md` as the base.  
   - Place `AGENTS.md` at the repo root unless instructed otherwise.  
   - Flag missing info with TODOs and ask for confirmation.  

## Reference
- `references/agents_md_template.md`: base template to fill.
