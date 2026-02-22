---
name: setup
description: Create and set up a new project from the growth boilerplate template. Handles repo creation, placeholder replacement, dependency installation, and KV namespace setup.
disable-model-invocation: true
---

This skill sets up a new project from the growth boilerplate template. It works in two modes depending on context.

## Step 0: Detect mode

Check if the current directory contains the boilerplate template by looking for `{{PROJECT_NAME}}` in `package.json`.

- **If placeholders are found**: you're inside a template project. Skip to Step 2.
- **If not found** (or `package.json` doesn't exist): you need to create the repo first. Start at Step 1.

## Step 1: Create the repository (global mode only)

**Use the `AskUserQuestion` tool to ask all of these in a single prompt:**
- Project name (kebab-case, e.g. `my-cool-tool`)
- One-line description
- Whether to use the **current directory** or create a **new subdirectory**

The repo is always created under the `aem-growth-adoption` org as **private**. Do not ask for the org.

Then check if `gh` CLI is available by running `gh --version`.

**If `gh` is not available**, install it automatically:
```bash
brew install gh
```
If `brew` is not available either, install Homebrew first:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then install `gh` with `brew install gh`.

**After installing `gh`**, or if `gh` is available but not authenticated (check with `gh auth status`), log in non-interactively with pre-selected defaults:
```bash
gh auth login --hostname github.com --git-protocol https --web
```
This chooses GitHub.com, HTTPS protocol, and opens the browser for authentication — no interactive prompts. Tell the user to complete the login in the browser window that opens, then wait for confirmation before continuing.

**Once `gh` is installed and authenticated**, run the appropriate commands based on the answers already collected above. Do not ask again.

If the user chose **current directory**:
```
gh repo create aem-growth-adoption/<project-name> --template aem-growth-adoption/team-boilerplate --private
```
Then clone into the current directory. Use `git clone ... .` only if the directory is truly empty. Otherwise (e.g. a `.claude` directory exists), use this approach instead:
```
git init
git remote add origin https://github.com/aem-growth-adoption/<project-name>.git
git fetch origin
git checkout -b main origin/main
```

If the user chose **new subdirectory**:
```
gh repo create aem-growth-adoption/<project-name> --template aem-growth-adoption/team-boilerplate --private --clone
cd <project-name>
```

After the repo is created and files are present, continue to Step 2.

## Step 2: Ask for project info (if not already collected)

If you didn't already ask in Step 1, **use the `AskUserQuestion` tool** to ask for:
- Project name (kebab-case, e.g. `my-cool-tool`)
- One-line description of the project

## Step 3: Replace placeholders

Replace in these files:
- `package.json`: replace `{{PROJECT_NAME}}` with the project name and `{{PROJECT_DESCRIPTION}}` with the description
- `wrangler.jsonc`: replace `{{PROJECT_NAME}}` with the project name
- `AGENTS.md`: replace `{{PROJECT_NAME}}` and `{{PROJECT_DESCRIPTION}}`
- `index.html`: replace `{{PROJECT_NAME}}`
- `app.jsx`: replace `{{PROJECT_NAME}}` and `{{PROJECT_DESCRIPTION}}`

Note: `CLAUDE.md` imports `AGENTS.md` via `@AGENTS.md`, so it doesn't need separate replacement.

Then, redesign `app.jsx` to be a visually appealing landing page for the project using React Spectrum components. The page should reflect the project's purpose based on its name and description. Be creative — use Spectrum layout components (`Flex`, `Grid`, `View`), typography (`Heading`, `Text`), and interactive elements (`Button`, `Well`, `Divider`, etc.) to make it look polished and professional. Keep it a single file.

### Rewrite README.md

Replace the entire `README.md` with a project-specific version. Remove all boilerplate/template references (no mentions of "boilerplate", "template", skill installation, or `gh repo create --template`). The new README should contain:

- **Title**: the project name as an `h1`
- **Description**: the one-line project description
- **Stack table**: same tech stack table (Workers, Hono, Zero Trust, KV, React Spectrum, Vite)
- **Project Structure**: updated tree — exclude `.claude/skills/` (it gets deleted in Step 4). Include `worker/`, `knowledge-base/`, `index.html`, `app.jsx`, `vite.config.js`, `CLAUDE.md`, `AGENTS.md`
- **Development section**: `npm run dev`, `npm run build`, `npm run deploy`
- **Knowledge Base section**: link to the markdown files in `knowledge-base/`

Do **not** include a production URL yet — that gets added after deploy in Step 8.

## Step 4: Remove boilerplate skills

Delete the `.claude/skills/` directory — it contains skills (`setup`, `teardown`) that belong to the boilerplate template and are not needed in the new project.

**Do NOT delete `.claude/settings.json`** — it contains the Cloudflare plugin configuration that the new project needs. Only remove the `skills/` subdirectory:

```
rm -rf .claude/skills
```

## Step 5: Git setup

Stage all files and create an initial commit: `Initial commit for <project-name>`

## Step 6: Install dependencies

The project requires the Node version specified in `.nvmrc`. Before installing, ensure the correct version is active:

```
nvm install
npm install
```

If `nvm` is not available, attempt to install it first:
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install
```
If that also fails, check `node --version` against `.nvmrc` and warn the user about the version mismatch.

## Step 7: Deploy

Run `npm run deploy` to build and deploy the project to Cloudflare Workers. Share the live URL with the user from the deploy output.

After a successful deploy, update `README.md` to add the production URL. Add it directly below the project description as a link, e.g.:

```
**Live:** https://<project-name>.<subdomain>.workers.dev
```

Use the actual URL from the deploy output. Stage and amend the most recent commit (or create a small `Add production URL to README` commit).

> **Note:** If the user's Cloudflare account has access to multiple accounts, they should set `CLOUDFLARE_ACCOUNT_ID` before running wrangler commands (e.g. `export CLOUDFLARE_ACCOUNT_ID=<account-id>`). Mention this if wrangler prompts for an account choice or fails with an account-related error. If wrangler fails because the user is not logged in, tell them to run `npx wrangler login` and re-run `/setup` from this step.

## Step 7a: Register with Access

Clone `aem-growth-adoption/access-apps` (if not already cloned). Add an entry to `apps.json`:

```json
{ "name": "<project-name>", "status": "active" }
```

Commit and push. GitHub Actions will create the Access app and set `CF_ACCESS_AUD` on the worker.

## Step 7b: Push to GitHub

Push all local commits to the remote:

```bash
git push origin main
```

This ensures the repo on GitHub reflects the customized project (placeholder replacements, KV config, production URL, etc.).

## Step 8: Done

Tell the user what was done automatically vs. what's left:
- **Done**: Deployed to Cloudflare Workers (KV namespace auto-provisioned), pushed to GitHub, Access app registered (or pending CI)
- Auth is handled by Cloudflare Zero Trust — `CF_ACCESS_AUD` is set automatically via the access-apps repo
- Run `npm run dev` for local development

Share the key links:
- **Live**: the production URL from the deploy output
- **Repo**: `https://github.com/aem-growth-adoption/<project-name>`

Point them to `knowledge-base/` for more on project conventions.
