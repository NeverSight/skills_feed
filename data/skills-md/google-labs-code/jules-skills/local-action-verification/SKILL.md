---
name: local-action-verification
description: Set up a repository for local GitHub Actions verification using act, so Jules can validate CI before pushing
allowed-tools:
  - "Bash"
  - "Read"
  - "Write"
---

# Local Action Verification with act

You are setting up a repository so that Jules (or any agent) can run GitHub Actions workflows locally using [act](https://github.com/nektos/act) to verify code changes pass CI before pushing.

## What You're Setting Up

Two scripts and an agents.md section that enable local CI verification:

1. **install-act.sh** — Installs `act` if missing (platform-aware, sudo fallback)
2. **run-act.sh** — Runs `act` in the background with log polling to avoid agent timeouts
3. **AGENTS.md section** — Instructions Jules reads to know how to use these scripts

## Setup Steps

### Step 1: Copy scripts to the repository

Copy the `scripts/` directory from this skill into the target repository at `scripts/act/`:

```
Target structure:
scripts/act/
├── install-act.sh
└── run-act.sh
```

Make sure the scripts are executable:

```bash
chmod +x scripts/act/install-act.sh scripts/act/run-act.sh
```

### Step 2: Add instructions to AGENTS.md

Append the following section to the repository's `AGENTS.md` file (create it if it doesn't exist). This is how Jules discovers the local verification capability:

```markdown
## Local CI Verification

Before pushing code or opening a PR, verify changes pass CI locally using `act`.

### Prerequisites
- Docker must be running
- If `act` is not installed, run: `bash scripts/act/install-act.sh`

### How to Verify

1. Read `.github/workflows/` to find the CI workflow and identify the job ID
2. Run the verification script:
   ```bash
   bash scripts/act/run-act.sh "push -j <JOB_ID>"
   ```
   With matrix: `bash scripts/act/run-act.sh "push -j <JOB_ID> --matrix <KEY>:<VALUE>"`
3. If the run fails, read the log output, fix the code, and re-run
4. After verification, clean up:
   ```bash
   rm -f act_output.log
   git checkout <any unintended file changes>
   ```

### Configuration
- Timeout: `ACT_TIMEOUT=900 bash scripts/act/run-act.sh "..."`  (default: 600s)
- Poll interval: `ACT_POLL=15 bash scripts/act/run-act.sh "..."`  (default: 10s)
- Custom image: pass `-P ubuntu-latest=node:20-bookworm` in the arguments for faster pulls
```

### Step 3: Update .gitignore

Append these entries to `.gitignore` if they don't already exist:

```
# act artifacts
act_output.log
.secrets
```

### Step 4: Print next steps for the user

Tell the user:
1. Docker must be installed and running on any machine (or Jules VM) where verification runs
2. `act` will be auto-installed on first use via `scripts/act/install-act.sh`
3. If workflows require secrets, create a `.secrets` file (KEY=VALUE format) — never commit it
4. Commit all generated files

## Troubleshooting

- **Docker not running**: `act` requires Docker. Ensure the Docker daemon is started.
- **Image pull slow**: First run downloads ~2GB+. Use `-P ubuntu-latest=node:20-bookworm` for faster pulls.
- **ARM64 issues**: On Apple Silicon, add `--container-architecture linux/amd64` to act arguments.
- **Secrets required**: Create a `.secrets` file and pass `--secret-file .secrets` in the act arguments.
- **Timeout**: Increase with `ACT_TIMEOUT=1200 bash scripts/act/run-act.sh "..."`.

## Resource References

- [Troubleshooting Guide](resources/troubleshooting.md) — Detailed solutions for common issues
