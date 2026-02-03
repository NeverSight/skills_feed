---
name: superspec-init
description: Use when OpenSpec is not initialized in the current project or the superspec-rpi schema is missing.
user-invocable: true
---

# Superspec Init: Project Bootstrap

## Purpose
Initialize OpenSpec in the current project for Superspec workflow and ensure the superspec-rpi schema is available.

## Preconditions
- OpenSpec CLI must be installed in PATH

## Workflow

### 1. Verify OpenSpec exists
Run `openspec --help`.

If command fails: tell user to install OpenSpec and re-run this skill. Do not proceed.

### 2. Initialize OpenSpec
Run `openspec init --tools none`.

**IMPORTANT**: If this command prompts interactively (e.g., cleanup questions), STOP immediately and ask the user what to do. Do NOT add `--force` automatically.

If init succeeds without prompts, proceed to step 3.

### 3. Ensure superspec-rpi schema exists
Verify `openspec/schemas/superspec-rpi/` directory exists.

If needed, create parent directories first:
- `mkdir -p openspec/schemas/superspec-rpi/templates`

**If missing**: Create these files by copying the exact contents (verbatim; do not invent or paraphrase) from the canonical assets listed in "Required Files Reference" below:
- `openspec/schemas/superspec-rpi/schema.yaml`
- `openspec/schemas/superspec-rpi/templates/proposal.md`
- `openspec/schemas/superspec-rpi/templates/spec.md`
- `openspec/schemas/superspec-rpi/templates/design.md`
- `openspec/schemas/superspec-rpi/templates/tasks.md`

**If present**: Validate instead of overwriting. Proceed to step 4.

### 4. Validate schema
Run `openspec schema validate superspec-rpi --json`.

- If validation fails: show the JSON summary, prioritizing `issues` if present. If unsure how to summarize, show the full JSON output. Then ask user whether to edit schema files or re-run init.
- If validation passes: proceed to confirmation.

### 5. Confirm success
Run `openspec schemas --json` and confirm `superspec-rpi` appears in output.

### 6. Report result
Output exactly:

```
Superspec initialized successfully
Selected schema: superspec-rpi
Next: /superspec-research
```

## Required Files Reference

Canonical file contents live under this skill's `assets/` directory. When you need to create missing schema/template files in the project, copy the contents **verbatim** from these asset files into the corresponding destination paths.

**Rules**:
- Copy exactly. Do not invent or paraphrase.
- Keep references one level deep (SKILL.md -> assets/*).
- If the destination file already exists, validate it instead of overwriting.

**Sources (copy-from) -> Destinations (copy-to)**:
- `skills/superspec-init/assets/openspec/schemas/superspec-rpi/schema.yaml` -> `openspec/schemas/superspec-rpi/schema.yaml`
- `skills/superspec-init/assets/openspec/schemas/superspec-rpi/templates/proposal.md` -> `openspec/schemas/superspec-rpi/templates/proposal.md`
- `skills/superspec-init/assets/openspec/schemas/superspec-rpi/templates/spec.md` -> `openspec/schemas/superspec-rpi/templates/spec.md`
- `skills/superspec-init/assets/openspec/schemas/superspec-rpi/templates/design.md` -> `openspec/schemas/superspec-rpi/templates/design.md`
- `skills/superspec-init/assets/openspec/schemas/superspec-rpi/templates/tasks.md` -> `openspec/schemas/superspec-rpi/templates/tasks.md`
