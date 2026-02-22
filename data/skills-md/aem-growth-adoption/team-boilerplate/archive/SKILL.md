---
name: archive
description: Archive a project — deletes Cloudflare infra (Worker + KV) and archives the GitHub repo using GitHub's built-in archive feature.
disable-model-invocation: true
---

This skill archives a project created from the growth boilerplate template. It deletes the Cloudflare infrastructure and archives the GitHub repository (making it read-only and hidden from the org's default repo listing).

**IMPORTANT: NEVER delete, remove, or modify local files or directories. This skill only operates on remote resources.**

## Step 1: Identify the project

Read `wrangler.jsonc` to get the worker name and KV namespace info. Read `package.json` to confirm the project name. Read the git remote to identify the GitHub repository (org and repo name).

If any of these contain unresolved `{{PROJECT_NAME}}` placeholders, stop and tell the user this project was never set up — there's nothing to archive.

## Step 2: Confirm with the user

**Use the `AskUserQuestion` tool** to ask for confirmation. Show the user exactly what will happen:

- **Delete Cloudflare Worker**: `<worker-name>`
- **Delete Cloudflare KV namespace**: `<namespace-id>` (from `kv_namespaces` in `wrangler.jsonc`)
- **Archive GitHub repo** `<org>/<repo>` (makes it read-only, hidden from default org view)

Ask: "This will permanently delete the infra and archive the repo. Are you sure?" with options "Yes, archive it" and "Cancel".

If the user cancels, stop immediately.

## Step 3: Delete the Cloudflare Worker

Run:
```
npx wrangler delete --name <worker-name>
```

If it fails (e.g. worker doesn't exist), warn but continue.

## Step 3b: Deregister from Access

Clone `aem-growth-adoption/access-apps` (if not already cloned). Find the matching entry in `apps.json` by project name and set its `status` to `"archived"`. Commit and push. GitHub Actions will delete the Access app.

If the entry doesn't exist in `apps.json`, skip this step with a note.

## Step 4: Delete the KV namespace

Read the namespace ID from `kv_namespaces` in `wrangler.jsonc` and run:
```
npx wrangler kv namespace delete --namespace-id <namespace-id>
```

If it fails (e.g. namespace doesn't exist or ID is still the placeholder), warn but continue.

## Step 5: Archive the GitHub repository

Run:
```
gh repo archive <org>/<repo> --yes
```

If `gh` is not available or the command fails, print the manual steps:
1. Go to the repository settings page
2. Scroll to the "Danger Zone"
3. Click "Archive this repository"

## Step 6: Done

Summarize what was done:
- Cloudflare Worker and KV namespace deleted (or note failures)
- GitHub repository archived (read-only, hidden from default org listing)

Do not touch or delete local files.
