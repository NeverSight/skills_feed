---
name: setup
description: Audit and prepare this skills repository for development and runtime use. Use when the user invokes /setup or asks to bootstrap the repository or install missing project tooling.
---

# /setup

Bring the current checkout to a usable state without changing project source or
configuration as a side effect of setup.

## Contract

- Work from the checkout that contains `Taskfile.yml`, `README.md`, and
  `skills/website-automation-builder`.
- Preserve dirty worktrees. Setup may create ignored `node_modules` directories,
  but must not rewrite manifests, lockfiles, generated skills, or user changes.
- Audit before installing anything. Install only missing or incompatible items.
- Treat network access, global npm installs, package-manager changes, and writes
  outside the checkout as approval-bearing operations in environments that
  require approval.
- Never run `playwright-cli attach` or browser/extension installation
  automatically.
  Those operations change repository, user, or browser state and need a separate
  explicit request.
- Never launch, replace, restart, or close a browser during setup.

## Workflow

1. Locate the repository root. If `node` is available, run:

   ```bash
   node "<SETUP_SKILL_ROOT>/scripts/check.mjs" --root "<REPOSITORY_ROOT>"
   ```

   Use `--json` when structured output is easier to consume. The audit is
   read-only and exits non-zero while a required item is missing or incompatible.

2. If Node cannot run the audit, check `node --version` directly. Install a
   supported Node release (at least 22.16.0, preferably a current LTS) through an
   already-used version manager or the platform's trusted package manager. npm
   must be available with Node. Do not introduce a new version manager without
   explaining that choice.

3. Read [requirements](references/requirements.md). Summarize each missing item,
   its scope, and the exact proposed command before executing approval-bearing
   installs.

4. Install in dependency order:

   ```bash
   npm install -g @go-task/cli
   npm install -g @playwright/cli@0.1.19
   npm ci --prefix "<REPOSITORY_ROOT>/skills/cardmarket-automation"
   ```

   Run only the commands required by the audit. Git and Node themselves are
   platform packages; use the existing platform/version manager rather than
   guessing a universal install command.

5. Re-run the audit. All required findings must be `ok`. If the user asked for a
   complete development setup, also run the browser-free regression suite:

   ```bash
   task --dir "<REPOSITORY_ROOT>" test
   ```

6. Report installed versions, anything still blocked, and whether tests ran.
   Report the Chrome extension as conditional: it is needed for live browser
   automation, not for repository setup or browser-free tests.

## Failure handling

- Stop after a failed install, retain its output, and re-audit before trying a
  different method.
- Do not work around permission errors by changing npm ownership, using `sudo`,
  or weakening security settings. Use the environment's approval mechanism or a
  user-scoped package-manager configuration.
- An unexpected `playwright-cli` version is incompatible, not an invitation to
  silently upgrade the repository. This checkout pins CLI protocol behavior to
  0.1.19.
