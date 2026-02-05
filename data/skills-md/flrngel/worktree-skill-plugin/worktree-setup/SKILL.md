---
name: worktree-setup
description: Set up git worktree management with isolated databases, caches, and ports for parallel development. Run once per project to generate standalone scripts.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, Grep, Edit
---

# Worktree Setup Skill

You are setting up git worktree management for this project. Your job is to analyze the project, then generate **standalone shell scripts** that manage worktrees with fully isolated resources (databases, caches, ports, env files). After setup, everything works via `git wt` with zero dependency on Claude Code.

Follow the phases below. At each step, make decisions based on what you actually find in the project — do not assume any specific stack.

---

## Phase 1: Analyze the Project

### 1.1 Verify This Is a Git Repository

Confirm the working directory is inside a git repo. If not, stop and tell the user.

If `.worktree/` already exists, ask the user whether to re-run setup (overwrite scripts but preserve existing worktree entries in config).

### 1.2 Detect the Project Stack

Look for manifest files to determine the language, framework, and package manager. Check for:

- **Node.js**: `package.json`, and which lockfile exists (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`) to determine the package manager
- **Python**: `requirements.txt`, `Pipfile`, `pyproject.toml`, `poetry.lock`, `uv.lock`
- **Ruby**: `Gemfile`
- **Go**: `go.mod`
- **Rust**: `Cargo.toml`
- **PHP**: `composer.json`
- **Java/Kotlin**: `build.gradle`, `pom.xml`
- **Elixir**: `mix.exs`
- Other manifest files you recognize

From this, determine the **dependency install command** that should run in each new worktree (e.g., the correct `install` command for the detected package manager).

For Node.js projects, also check `package.json` scripts to identify the dev server command (commonly `dev`, `start:dev`, `serve`, or `start`). Note this for the summary but don't put it in the scripts — worktrees are for development, the user starts their own server.

### 1.3 Detect Environment Configuration

Read the `.env` file (and `.env.local`, `.env.development`, etc. if they exist). Identify:

**Database connection** — Look for any of these patterns:
- `DATABASE_URL` (connection string format: `postgresql://`, `postgres://`, `mysql://`, `mongodb://`, `sqlite:`, etc.)
- Individual vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- Postgres-specific: `PGDATABASE`, `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`
- MySQL-specific: `MYSQL_HOST`, `MYSQL_DATABASE`, etc.
- ORM-specific: `TYPEORM_DATABASE`, `PRISMA_DATABASE_URL`, etc.

From the connection info, extract: database type, host, port, user, password, database name.

**Cache/queue connection** — Look for:
- `REDIS_URL` (connection string: `redis://host:port/db` or `rediss://`)
- Individual vars: `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`
- Other caches: `MEMCACHED_URL`, `CACHE_URL`, etc.

**Application port** — Look for:
- `PORT`, `APP_PORT`, `SERVER_PORT`, `HTTP_PORT`
- Framework-specific: `NEXT_PUBLIC_PORT`, `VITE_PORT`, `FLASK_RUN_PORT`, `RAILS_PORT`

**Other env vars that need per-worktree isolation** — Look for:
- `APP_NAME`, `APP_URL` (may contain port)
- `SESSION_NAME`, `COOKIE_NAME` (session isolation)
- Log file paths, tmp directories
- Any var that references a resource that would conflict between parallel instances

Record exactly which env var keys you found and their current values. You need this to write correct env patching logic in the scripts.

### 1.4 Detect Infrastructure Configuration

Check for Docker Compose files (`docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`). If found, read them to understand:
- Which services run (postgres, mysql, redis, mongo, elasticsearch, etc.)
- Port mappings (to know the correct host ports)
- Environment variables (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, etc.)
- Volume mounts

This serves as a fallback or confirmation for the env var detection above.

### 1.5 Assess What Tools Are Available

Check which command-line tools are installed on the system. You need this to decide how to implement the scripts. Things to check:

- **JSON processing**: Is there a tool for reading/writing JSON from bash? (e.g., `jq`, `python3`, `node`)
- **Database tools**: For the detected database type, are the CLI tools available? (e.g., for Postgres: `createdb`, `dropdb`, `pg_dump`, `psql`; for MySQL: `mysql`, `mysqldump`, `mysqladmin`)
- **Cache tools**: For the detected cache, are CLI tools available? (e.g., `redis-cli`)
- **Port checking**: Is `lsof` or `ss` or `netstat` available?
- **General**: `sed`, `awk`, `grep` — these are virtually always available but note the platform (macOS `sed` vs GNU `sed` differ in `-i` flag behavior)

**Based on what's available, you choose the implementation approach for the scripts.** For example:
- If `jq` is available, use it for JSON. If not, use `python3 -c` or `node -e` or even `awk`/`sed` — whatever works.
- If `createdb` isn't available but `psql` is, use `psql -c "CREATE DATABASE ..."`.
- If no database CLI tools are available at all, the scripts should print a warning and skip DB operations.

The scripts must work with whatever is on the machine. Do not require the user to install additional tools — adapt to what exists. If a critical operation can't be done (e.g., no way to process JSON at all), then tell the user what to install.

---

## Phase 2: Generate Config

Create `.worktree/config.json` storing everything the scripts need. The config serves as:
1. A record of detected project settings
2. A registry of active worktrees and their allocated resources
3. The single source of truth the scripts read from

### Config Schema

Include only the sections relevant to what was detected. Example for a project with Postgres and Redis:

```json
{
  "base_port": 3000,
  "database": {
    "type": "postgres",
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "main_db": "myapp"
  },
  "cache": {
    "type": "redis",
    "host": "localhost",
    "port": 6379
  },
  "init_commands": ["npm install"],
  "env_file": ".env",
  "env_mappings": {
    "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/myapp",
    "REDIS_URL": "redis://localhost:6379/0",
    "PORT": "3000"
  },
  "worktrees": {}
}
```

**Considerations:**
- `env_mappings` records the original env var keys and values that need per-worktree patching. The scripts use this to know exactly what to replace.
- `worktrees` is an object keyed by sanitized name, storing: branch, port, database name, cache DB number, path, created timestamp.
- Omit `database` if none detected. Omit `cache` if none detected.
- Use whatever values you actually detected — don't guess or use defaults if you found real values.

---

## Phase 3: Generate Scripts

Create scripts in `.worktree/bin/`. These must be **complete, standalone, and functional** — no placeholders, no TODOs, no references back to this skill. The user (or any developer) should be able to read and understand them.

You are writing five scripts. The implementation details are up to you based on what you detected, but each must fulfill the contract described below.

### 3.1 `.worktree/bin/git-wt` — Command Router

**Contract:**
- Entry point for all `git wt` commands
- Subcommands: `create`, `delete` (aliases: `rm`, `remove`), `list` (alias: `ls`), `checkout` (aliases: `cd`, `go`), `help`
- Must resolve to the **main repository root** — not the current worktree root (see "Resolving the Main Repo Root" below)
- Must verify config exists before dispatching
- Must verify its JSON processing dependency is available
- Must show helpful usage on `help` or unknown command

### 3.2 `.worktree/bin/wt-create.sh` — Create Worktree

**Arguments:** `<branch-name> [from-ref]` where `from-ref` defaults to HEAD.

**Contract — must do all of the following:**

1. **Sanitize the branch name** for use as directory name and database suffix. Replace characters that are problematic in paths or DB names (`/` -> `-`, strip special chars). Keep the mapping so the user can still reference by original branch name.

2. **Reject duplicates.** Check the config for an existing worktree with the same sanitized name. Also check if the directory already exists on disk.

3. **Allocate a unique port.** Start from `base_port + 1`, scan existing worktree entries in config to find the first unused number. Then verify the port isn't actually in use on the system (a worktree might have been deleted outside of `git wt`). Skip ports that are occupied.

4. **Clone the database** (if database detected):
   - Generate a database name: `{main_db}_wt_{sanitized_name}`
   - Create it as a copy of the main database. For Postgres, the fastest approach is template copy (`createdb -T`), but this fails if the source has active connections — fall back to dump-and-restore. For MySQL, use `mysqldump | mysql`. For other DBs, do what makes sense or skip with a warning.
   - If the database tools aren't available, print a warning and skip — don't fail the whole operation.

5. **Allocate a cache namespace** (if cache detected):
   - For Redis: allocate the next unused DB number (main uses 0, worktrees start from 1). Track allocated numbers in config.
   - For other caches: decide an appropriate isolation strategy or skip.

6. **Create the git worktree.** Use `git worktree add <path> -b <branch> <from-ref>`.

7. **Copy and patch the env file.** This is critical — copy the env file to the worktree directory, then replace the relevant values:
   - Database name in the connection string or individual var
   - Cache DB number in the connection string or individual var
   - Port number
   - Any other vars identified in Phase 1 as needing per-worktree values

   **Considerations for env patching:**
   - Connection strings need surgical replacement (change only the DB name part of a URL, not the whole string)
   - `sed -i` behaves differently on macOS vs Linux. Use `sed -i.bak` + `rm *.bak` for portability, or use another approach.
   - Some projects use multiple env files (`.env`, `.env.local`). Copy all that exist.
   - Be careful not to corrupt the env file — test your sed patterns mentally against the actual values you detected.

8. **Run init commands** in the worktree directory. Run the detected install command(s). If they fail, warn but don't abort — the worktree itself is still valid.

9. **Update config.json** with the new worktree entry including all allocated resources and a creation timestamp.

10. **Print a summary** of what was created: path, branch, port, database, cache DB.

### 3.3 `.worktree/bin/wt-delete.sh` — Delete Worktree

**Arguments:** `<branch-name>`

**Contract:**

1. **Look up the worktree** in config. Accept both the original branch name and the sanitized form. If not found, list available worktrees and exit.

2. **Drop the database** (if one was created). Use the appropriate tool for the DB type. Use `--if-exists` or equivalent to avoid errors. If the tool isn't available or the drop fails, warn but continue.

3. **Clean up the cache namespace** (if one was allocated). For Redis, flush the allocated DB. Warn on failure but continue.

4. **Remove the git worktree.** Use `git worktree remove --force`, falling back to manual directory removal if that fails. Run `git worktree prune` afterward.

5. **Remove the entry from config.json.**

6. **Print confirmation** of what was deleted.

### 3.4 `.worktree/bin/wt-list.sh` — List Worktrees

**Contract:**

1. Read all worktree entries from config.
2. If none exist, say so and show the create command.
3. Display a formatted table with columns appropriate to what was configured. Always show: NAME, BRANCH, PORT, CREATED. Conditionally show: DATABASE, CACHE_DB (only if the project uses them).
4. Keep the output readable — align columns, truncate long values if needed.

### 3.5 `.worktree/bin/wt-checkout.sh` — Switch to a Worktree or Main Repo Directory

**Arguments:** `[worktree-name]` (optional; accepts original branch name or sanitized name)

**Contract:**

1. **No argument or `-` or `main`**: Output the main repository root path. This lets the user switch back to the main repo from any worktree.
2. **With a worktree name**: Look up the worktree in config (same fuzzy lookup as delete — accept both `feat/foo` and `feat-foo`). If not found, list available worktrees and exit with an error.
3. Verify the target directory actually exists on disk. If the directory is gone but the config entry remains, warn the user.
4. **Output the resolved absolute path** to stdout.

**Note:** A git alias runs in a subshell and cannot change the parent shell's working directory. `git wt checkout` outputs the path to stdout so the user can compose it with `cd`:
```
cd $(git wt checkout feat/foo)
```

---

## Phase 4: Configure Git (Local Only)

**Zero tracked changes.** Nothing you do should appear in `git status`.

1. **Exclude `.worktree` from git** by adding it to `.git/info/exclude` (NOT `.gitignore`). Check if it's already there before adding.

2. **Create a local git alias** so `git wt` routes to the script:
   ```
   git config alias.wt '!.worktree/bin/git-wt'
   ```
   This is stored in `.git/config` (local only, not committed).

3. **Make all scripts executable.**

4. **Verify the setup works** by running `git wt help` and confirming it produces output.

---

## Phase 5: Report to the User

Print a clear summary covering:

- What project type and stack was detected
- What resources will be isolated per worktree (database, cache, port — only mention what applies)
- What files were generated
- What git config was set up (and emphasize: zero tracked changes)
- The commands available (`git wt create/delete/list/checkout`) with examples
- For checkout, show the `cd $(git wt checkout <name>)` usage pattern
- Any warnings (e.g., "Postgres CLI tools not found — database cloning will be skipped")

---

## Key Considerations

### Resolving the Main Repo Root

This is critical. All scripts need to find the **main repository root** where `.worktree/` lives — not the current worktree's root.

`git rev-parse --show-toplevel` returns the root of whichever working tree you're currently in. If you're inside a worktree at `.worktree/feat-foo/`, it returns that path — not the main repo. So using `--show-toplevel` alone would fail to find `.worktree/config.json` when running from inside a worktree.

The scripts must resolve the main repo root regardless of whether the user is in the main working tree or any worktree. `git rev-parse --git-common-dir` returns the path to the shared `.git` directory, which always belongs to the main repo. From that, the main repo root can be derived (it's the parent of the `.git` directory). There may be other approaches — choose whatever is robust and works across git versions.

Every script must use this resolution. Do not assume the user is in the main working tree.

### Portability
- Scripts should work on both macOS and Linux.
- Handle `sed -i` portability (macOS requires a backup extension argument, GNU doesn't).
- Use `/usr/bin/env bash` shebang for portability.
- Use dynamic path resolution as described above — never hardcode absolute paths.

### Robustness
- Branch names can contain `/`, `.`, and other characters. The sanitization must produce safe directory names and database identifiers.
- Port allocation should handle gaps (if worktree 1 was deleted, its port should be reusable by a new worktree).
- Database operations can fail for many reasons (server not running, permissions, active connections). Scripts should warn and continue, not abort entirely.
- The config file is the source of truth. If the file gets corrupted, the scripts should fail gracefully with a clear message rather than doing something destructive.

### Isolation
- Each worktree gets its OWN: git working tree, env file, database, cache namespace, port.
- The main working tree's resources are never modified — base_port, main DB, Redis DB 0 are reserved.
- Env patching must be precise — only change the specific values that need to differ, leave everything else intact.

### Cleanup
- `git wt delete` must clean up ALL allocated resources, not just the git worktree.
- If a resource can't be cleaned up (e.g., DB server not running), warn but still remove the config entry and git worktree — don't leave things in a half-deleted state.

### Config as Source of Truth
- All allocated resources (ports, DB names, cache DBs) are tracked in config.json.
- Scripts must read from config to determine what exists — don't rely on filesystem or database state alone.
- Config updates must be atomic (write to temp file, then rename) to avoid corruption from interrupted operations.
