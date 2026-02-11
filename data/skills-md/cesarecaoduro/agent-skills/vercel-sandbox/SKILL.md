---
name: vercel-sandbox
description: >
  Work with Vercel Sandbox — ephemeral Linux microVMs for running untrusted code, AI agent output,
  and developer experimentation on Vercel. Use this skill when the user mentions "Vercel Sandbox",
  "@vercel/sandbox", sandbox microVMs, running code in isolated environments on Vercel, or wants to
  create/manage/snapshot sandboxes via the TypeScript/Python SDK or Vercel CLI. Also trigger when the
  user asks about sandbox pricing, resource limits, authentication (OIDC tokens, access tokens),
  system specifications, CLI commands (`vercel sandbox`), or wants to update the local documentation
  cache for this skill.
---

# Vercel Sandbox Skill

Vercel Sandbox is an ephemeral compute primitive (Beta, all plans) that runs untrusted or
user-generated code in isolated Linux microVMs on Vercel. It supports AI agents, code generation
tools, developer sandboxes, and backend logic testing.

## When to consult reference files

- **Getting started / setup**: Read [references/quickstart.md](references/quickstart.md)
- **SDK usage (TypeScript)**: Read [references/sdk-reference.md](references/sdk-reference.md)
- **CLI commands**: Read [references/cli-reference.md](references/cli-reference.md)
- **Pricing, limits, resource specs**: Read [references/pricing-and-specs.md](references/pricing-and-specs.md)
- **Authentication details**: Covered in both quickstart and SDK reference files

## Quick reference

### Install

```bash
pnpm i @vercel/sandbox    # TypeScript
pip install vercel-sandbox # Python
```

### Authentication setup

```bash
vercel link         # Link to a Vercel project
vercel env pull     # Pull OIDC token to .env.local (expires 12h locally)
```

### Minimal example (TypeScript)

```ts
import { Sandbox } from '@vercel/sandbox';

const sandbox = await Sandbox.create();
const result = await sandbox.runCommand('echo', ['Hello from Vercel Sandbox!']);
console.log(await result.stdout());
await sandbox.stop();
```

### Key SDK classes

| Class | Purpose |
|-------|---------|
| `Sandbox` | Create, manage, list, snapshot microVMs |
| `Command` | Interact with running/detached commands |
| `CommandFinished` | Access exit code, stdout, stderr after completion |
| `Snapshot` | Save/restore sandbox state for fast restarts |

### Available runtimes

`node24`, `node22`, `python3.13` — all on Amazon Linux 2023.

### Default working directory

`/vercel/sandbox` — user code runs as `vercel-sandbox` user.

### Timeouts

Default 5 min. Max: 45 min (Hobby), 5 hours (Pro/Enterprise). Extend with `sandbox.extendTimeout()`.

### Snapshots

Capture with `sandbox.snapshot()` — sandbox stops after snapshot. Expire after 7 days.

## Updating documentation

When the user asks to "update the Vercel Sandbox documentation", choose the right
method based on the environment:

### Method selection

- **claude.ai / Claude Desktop** (has `web_fetch` tool) → Use **Path A: web_fetch**
- **Claude Code** (has bash with internet) → Use **Path B: Python script**

To detect: if `web_fetch` is in your available tools, use Path A. Otherwise use Path B.

### Path A: web_fetch (claude.ai / Claude Desktop)

1. Use `web_fetch` to retrieve https://vercel.com/docs/vercel-sandbox (the main page)
2. Discover all sub-page links under `/docs/vercel-sandbox/`
3. Fetch each known sub-page URL (see list below) plus any newly discovered pages
4. For each reference file in `references/`:
   a. Read the existing file content
   b. Compare with fetched content — note additions, removals, changes
   c. Rewrite the reference file with updated, clean markdown
   d. Update the `> Last fetched:` date at the top
5. Report to user: pages fetched, what changed per file, update date

### Path B: Python script (Claude Code / local terminal)

Run the update script which has full internet access:

```bash
python3 <skill-path>/scripts/update_docs.py <skill-path>/references
```

The script will:
1. Fetch all known sandbox doc URLs from vercel.com
2. Discover any new sub-pages from the main page
3. For each reference file: compute a diff, overwrite with new content, report changes
4. Print a summary of what changed and when

After the script runs, review its output and report changes to the user.

### Known doc page URLs

- https://vercel.com/docs/vercel-sandbox (overview + system specs)
- https://vercel.com/docs/vercel-sandbox/quickstart
- https://vercel.com/docs/vercel-sandbox/sdk-reference
- https://vercel.com/docs/vercel-sandbox/cli-reference
- https://vercel.com/docs/vercel-sandbox/pricing
- https://vercel.com/docs/vercel-sandbox/examples
- https://vercel.com/docs/vercel-sandbox/managing

Also discover any new pages linked from the main page's sidebar/navigation.
