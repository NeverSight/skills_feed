---
name: setup-sandbox
description: Set up the initial file system for a new sandbox. Fetches the account's organizations and artists via the Recoup CLI and scaffolds an opinionated folder structure. Use when a sandbox has just been created and has no existing file system. Before running, check if the sandbox already has an orgs/ directory — if it does, this skill is not needed.
---

# Setup Sandbox

Create the folder structure for the connected account's organizations and artists.

## Environment

- `RECOUP_ACCOUNT_ID` — The account ID to fetch data for. Only needed when using an Org API Key. When using a Personal API Key, omit the `--account` flag and the CLI will use the authenticated account automatically.

## Steps

1. Check if `RECOUP_ACCOUNT_ID` is set. If set, use `--account $RECOUP_ACCOUNT_ID` on all CLI commands below. If not set, omit the `--account` flag.
2. Run `recoup orgs list --json [--account $RECOUP_ACCOUNT_ID]` to get all organizations
3. For each organization, run `recoup artists list --org {organization_id} --json [--account $RECOUP_ACCOUNT_ID]` to get its artists
4. Create the folder structure and a `RECOUP.md` marker in each artist folder:
   - `mkdir -p orgs/{org}/artists/{artist-slug}` for each org/artist pair
   - Write a `RECOUP.md` in each artist folder using the template below
5. Commit and push:
   - `git add -A && git commit -m "setup: create org and artist folders" && git push origin main`

## `RECOUP.md`

Every artist directory has a `RECOUP.md` at its root. This is the **identity file** — it connects the workspace to the Recoupable platform and tracks setup status. It stays permanently.

Fill it with data from the CLI response:

```markdown
---
artistName: {Artist Name}
artistSlug: {artist-slug}
artistId: {uuid-from-recoupable}
status: not-setup
---

# {Artist Name}

This artist workspace has not been set up yet.

Run the `setup-artist` skill to scaffold it — that will create the full directory structure, context files, memory system, and README files.
```

**Fields:**

- `artistName` — display name from the CLI (e.g. `Gatsby Grace`)
- `artistSlug` — lowercase-kebab-case folder name (e.g. `gatsby-grace`)
- `artistId` — the UUID from Recoup
- `status` — `not-setup` at creation, updated to `active` by the `setup-artist` skill

## Next Steps

After the sandbox is set up, run the `setup-artist` skill for each artist. If the skill is not installed, install it first:

```bash
npx skills add recoupable/setup-artist
```

Find which artists still need setup:

```bash
grep -rl "status: not-setup" orgs/*/artists/*/RECOUP.md
```

Any `RECOUP.md` with `status: not-setup` hasn't been scaffolded yet. Run `setup-artist` for each one.
