---
name: readthedocs-write-config
description: Create or update Read the Docs `.readthedocs.yaml` v2 configuration files for Sphinx or MkDocs builds, including build images/tools, dependency installs, formats, custom build jobs/commands, conda environments, submodules, and search settings. Use when a user asks for a Read the Docs config file, YAML changes, or build behavior updates.
---

# Write Read the Docs config (v2)

## Overview

Write or revise `.readthedocs.yaml` files for Read the Docs v2 builds. Focus on required fields, correct paths, and supported keys to avoid validation failures.

## Workflow

1. Identify the documentation tool and paths.
   - Confirm whether the project uses Sphinx, MkDocs, or something else.
   - Collect `sphinx.configuration` (conf.py) or `mkdocs.configuration` (mkdocs.yml) paths.
   - Confirm the config file location (repo root by default, subdirectory for monorepos).

2. Choose the build image and tools.
   - Set `build.os` and `build.tools` when using custom build jobs or commands.
   - Choose stable versions; use `latest` only when asked.

3. Define dependency installation.
   - Use `python.install` with requirements and/or package install.
   - Use `conda.environment` when the project uses conda, and set `build.tools.python` accordingly.

4. Configure the build step.
   - Use `sphinx` or `mkdocs` settings for standard builds.
   - Prefer `build.jobs` for customization; use `build.commands` only to fully replace the pipeline.
   - If overriding formats, write outputs under `$READTHEDOCS_OUTPUT/<format>/`.

5. Add optional settings.
   - Set `formats` for extra outputs (Sphinx only).
   - Configure `submodules` or `search` only if requested.

6. Validate against supported keys and required fields.
   - Use `references/v2-config.md` to confirm defaults, allowed values, and constraints.

## Quick start templates

- For Sphinx, start from `assets/sphinx.readthedocs.yaml`.
- For MkDocs, start from `assets/mkdocs.readthedocs.yaml`.

## Decision notes

- Prefer `build.jobs` over `build.commands` because it preserves standard steps and supports per-format commands.
- Avoid `build.apt_packages` when using `build.commands` (not supported together).
- Include `formats` only when the user needs PDF/ePub/HTMLZIP output.
- Do not combine `submodules.include` and `submodules.exclude`.

## Output checklist

- `version: 2` present.
- `build.os` and `build.tools` present when required.
- `sphinx.configuration` or `mkdocs.configuration` path is correct.
- All custom build outputs are written to `$READTHEDOCS_OUTPUT`.
- No unsupported keys or typos.

## Resources

- Reference: `references/v2-config.md`
- Templates: `assets/sphinx.readthedocs.yaml`, `assets/mkdocs.readthedocs.yaml`
