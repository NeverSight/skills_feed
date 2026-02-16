---
name: automate-github-issues
description: Set up automated GitHub issue triage and resolution using parallel Jules coding agents
allowed-tools:
  - "Bash"
  - "Read"
  - "Write"
---

# Automate GitHub Issues with Jules

You are setting up a repository to automatically analyze open GitHub issues, plan implementation tasks, and dispatch parallel Jules coding agents to fix them.

## What You're Setting Up

A 5-phase automated pipeline that runs via GitHub Actions (or locally):

1. **Analyze** — Fetch open issues and format as structured markdown
2. **Plan** — A Jules session performs deep code-level triage and produces self-contained task prompts
3. **Validate** — Verify no two tasks modify the same file (prevents merge conflicts)
4. **Dispatch** — Spawn parallel Jules sessions, one per task
5. **Merge** — Sequential PR merge with CI validation

## Setup Steps

### Step 1: Copy fleet scripts to the repository

Copy the entire `scripts/` directory from this skill into the target repository at `scripts/fleet/`:

```
Target structure:
scripts/fleet/
├── fleet-analyze.ts
├── fleet-plan.ts
├── fleet-dispatch.ts
├── fleet-merge.ts
├── types.ts
├── prompts/
│   ├── analyze-issues.ts
│   └── bootstrap.ts
└── github/
    ├── git.ts
    ├── issues.ts
    ├── markdown.ts
    └── cache-plugin.ts
```

> **Important:** Preserve the directory structure exactly. The scripts use relative imports between files.

### Step 2: Copy workflow templates

Copy the workflow files from `assets/` to the repository's `.github/workflows/` directory:

- `assets/fleet-dispatch.yml` → `.github/workflows/fleet-dispatch.yml`
- `assets/fleet-merge.yml` → `.github/workflows/fleet-merge.yml`

### Step 3: Create a package.json for the fleet scripts

Create `scripts/fleet/package.json` with the required dependencies:

```json
{
  "name": "fleet-scripts",
  "private": true,
  "type": "module",
  "dependencies": {
    "@google/jules-sdk": "^0.1.0",
    "octokit": "^4.1.0",
    "find-up": "^7.0.0"
  },
  "devDependencies": {
    "@types/bun": "^1.2.0"
  }
}
```

### Step 4: Create environment template

Copy `assets/.env.example` to the repository root.

### Step 5: Install dependencies

```bash
cd scripts/fleet && bun install
```

### Step 6: Print next steps for the user

Tell the user they need to:
1. Add `JULES_API_KEY` as a GitHub repository secret (Settings → Secrets → Actions)
2. `GITHUB_TOKEN` is provided automatically by GitHub Actions
3. Customize the cron schedule in `.github/workflows/fleet-dispatch.yml` (default: daily 6am UTC)
4. Commit all generated files

## Manual Usage

After setup, the user can run the pipeline locally:

```bash
cd scripts/fleet

# Fetch open issues
bun fleet-analyze.ts

# Plan tasks (creates a Jules planning session)
JULES_API_KEY=<key> bun fleet-plan.ts

# Dispatch parallel agents
JULES_API_KEY=<key> bun fleet-dispatch.ts

# Merge PRs sequentially
GITHUB_TOKEN=<token> bun fleet-merge.ts
```

## Customization

### Prompt Tuning
The analysis prompt in `scripts/fleet/prompts/analyze-issues.ts` controls how deeply issues are investigated. Users can adjust:
- Root cause analysis depth
- Solution implementation detail level
- Merge conflict avoidance rules
- File ownership constraints

### Issue Filtering
Edit `scripts/fleet/github/issues.ts` to filter issues by label, milestone, or state.

## Resource References

- [Architecture Overview](resources/architecture.md) — Detailed explanation of the 5-phase pipeline

## Troubleshooting

- **"Unable to parse git remote URL"**: Ensure the repo has a valid GitHub remote (`git remote get-url origin`)
- **Ownership conflict errors**: Two tasks claim the same file. Adjust the task JSON or merge them manually.
- **CI timeout during merge**: Increase `maxWaitMs` in `fleet-merge.ts` (default: 10 minutes)
- **Bun not found**: Install Bun: `curl -fsSL https://bun.sh/install | bash`
