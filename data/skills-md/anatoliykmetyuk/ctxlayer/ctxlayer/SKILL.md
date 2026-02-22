---
name: ctxlayer
description: Manages context layer domains, tasks, and documentation. Use when the user mentions "context layer" (e.g. "using context layer", "in the context layer", "in the context", "to the context layer", "into the context layer") ctx commands, context layer projects or tasks, or requests you to write any form of documentation -- such as documenting implemented features, research findings, or drawing diagrams. Also use when the user asks to add a repository to the context layer, clone a repo as context layer context, or access context layer's "data" folder.
---

# Context Layer

## ctx CLI commands

The `ctx` CLI manages domains and tasks. Available commands:

- `ctx` -- Show help and available commands
- `ctx new [name]` -- Create a new task (prompts for domain if needed; prompts for task name if `name` is not specified)
- `ctx import` -- Import a task from any domain as a symlink into `.ctxlayer/` (sets active when config is empty)
- `ctx status` -- Show the active domain and task, plus git tracking info
- `ctx set` -- Set active domain and task (interactive)
- `ctx git [args...]` -- Run git in the active task directory
- `ctx drop task [name]` -- Remove a task symlink from `.ctxlayer/`. Prompts for task if `name` is not specified
- `ctx drop domain [name]` -- Remove a domain directory from `.ctxlayer/`. Prompts for domain if `name` is not specified
- `ctx delete task` -- Permanently delete a task from the context layer. Prompts for task
- `ctx delete domain` -- Permanently delete a domain from the context layer. Prompts for domain

Configuration lives at `.ctxlayer/config.yaml` in the current working directory with two fields:

```yaml
active-domain: <domain-name>
active-task: <task-name>   # may be omitted if no task is active
```

Domains are stored globally at `~/.agents/ctxlayer/domains/`. Each domain contains task folders, and each task folder has `docs/` and `data/` subdirectories.

**Which task to access:** By default, use the **active** domain and task from `config.yaml` (run `ctx status` to obtain them). When the user explicitly specifies a domain and task in the prompt (e.g. "in the context layer, domain A, task B, use documents 1 and 2"), use that instead. You may only access them via symlinks in the `.ctxlayer/<domain>/<task>/` folder. If the requested task is not linked (no symlink at `.ctxlayer/<domain>/<task>/`), advise the user to run `ctx import` first. All operations below apply to this resolved task.

## Documentation operations

Documentation operations are read and write operations requested by the user with the intent of documenting something or accessing previously documented information. All documentation operations are performed on the resolved task's `docs/` folder.

### Documentation conventions

Documentation is stored in the form of numbered markdown files in the resolved task's `docs/` folder. The following are the conventions for writing and reading documentation:

- **Prefix:** two-digit incrementing number (`01`, `02`, `03`, …) based on existing files
- **Separator:** Single dash
- **Name:** Descriptive kebab-case summary
- **Extension:** `.md`

**Examples:** `01-initial-research.md`, `02-feature-implementation.md`, `03-architecture-diagram.md`

Semantically, each file is a standalone document covering one topic. The docs folder serves as a running report and journal for the task.

You MUST follow the documentation conventions when writing or reading the documentation.

### Reading documents

When the user asks to read a document referring to it by name, e.g. "document number N", resolve it to the file with prefix `NN-<name>.md` (e.g. document 1 → `01-initial-research.md`) in the resolved task's `docs/` folder.

### Writing documents

When the user asks to write a document, create a new numbered markdown file in the resolved task's `docs/` folder and write the content as a markdown file. To obtain the next prefix number, list existing files, determine the greatest prefix number, and increment it by 1.

## Data operations

The task's `data/` folder holds reference material: sample data, configuration snippets, external repositories, and anything else useful as a reference during implementation.

### Accessing the data folder

If the user asks to access something in the context layer that is not a document, it is understood that they want to access the information in the resolved task's `data/` folder.

If the user explicitly mentions the data folder, e.g. "the data folder", "the context layer's data folder", "the context layer data", resolve it to the resolved task's `data/` folder.

### Adding repositories to data

When the user asks to "add a repository to the context layer" or "clone a repo as context layer context", do **NOT** run a regular `git clone`. Instead, from the domain root (`~/.agents/ctxlayer/domains/<domain>/`), run `git submodule add <repo-url> <task>/data/<subdir>` to add the repo into the task's data folder.

This keeps the domain repo lightweight and version-controlled via submodule references.

## Git operations

When the user requests any git operations (e.g., status, add, commit, push, pull) on the context layer or task context, perform them via `ctx git <args>` rather than running `git` directly. For example:

> "Commit all the changes to the context layer"

Is understood as a request to summarize the changes in the resolved task, compose a descriptive commit message, and commit the changes via `ctx git add -A . && ctx git commit -a -m "<descriptive commit message>"`.
