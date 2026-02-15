---
name: setup-sandbox
description: Create org and artist folder structure using the Recoup CLI
---

# Setup Sandbox

Create the folder structure for the connected account's organizations and artists.

## Environment

- `RECOUP_ACCOUNT_ID` — The account ID to fetch data for. Only needed when using an Org API Key. When using a Personal API Key, omit the `--account` flag and the CLI will use the authenticated account automatically.

## Steps

1. Check if `RECOUP_ACCOUNT_ID` is set. If set, use `--account $RECOUP_ACCOUNT_ID` on all CLI commands below. If not set, omit the `--account` flag.
2. Run `recoup orgs list --json [--account $RECOUP_ACCOUNT_ID]` to get all organizations
3. For each organization, run `recoup artists list --org <organization_id> --json [--account $RECOUP_ACCOUNT_ID]` to get its artists
4. Create the folder structure with a `RECOUP.md` in each artist folder (so git tracks the directories):
   - `mkdir -p orgs/<organization_name>/artists/<artist_name> && touch orgs/<organization_name>/artists/<artist_name>/RECOUP.md` for each org/artist pair
5. Commit and push:
   - `git add -A && git commit -m "setup: create org and artist folders" && git push origin main`
