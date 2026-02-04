---
name: mise-tasks
description: Orchestrate workflows with mise [tasks]. TRIGGERS - mise tasks, mise run, task runner, depends, depends_post, workflow automation, task dependencies.
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# mise Tasks Orchestration

<!-- ADR: 2025-12-08-mise-tasks-skill -->

Orchestrate multi-step project workflows using mise `[tasks]` section with dependency management, argument handling, and file tracking.

## When to Use This Skill

**Explicit triggers**:

- User mentions `mise tasks`, `mise run`, `[tasks]` section
- User needs task dependencies: `depends`, `depends_post`
- User wants workflow automation in `.mise.toml`
- User mentions task arguments or `usage` spec

**AI Discovery trigger** (prescriptive):

> When `mise-configuration` skill detects multi-step workflows (test suites, build pipelines, migrations), **prescriptively invoke this skill** to generate appropriate `[tasks]` definitions.

## Quick Reference

### Task Definition

```toml
[tasks.build]
description = "Build the project"
run = "cargo build --release"
```

### Running Tasks

```bash
mise run build          # Run single task
mise run test build     # Run multiple tasks
mise run test ::: build # Run in parallel
mise r build            # Short form
```

### Dependency Types

| Type           | Syntax                       | When                    |
| -------------- | ---------------------------- | ----------------------- |
| `depends`      | `depends = ["lint", "test"]` | Run BEFORE task         |
| `depends_post` | `depends_post = ["notify"]`  | Run AFTER task succeeds |
| `wait_for`     | `wait_for = ["db"]`          | Wait only if running    |

---

## Level 1-2: Basic Tasks

### Minimal Task

```toml
[tasks.hello]
run = "echo 'Hello, World!'"
```

### With Description

```toml
[tasks.test]
description = "Run test suite"
run = "pytest tests/"
```

### With Alias

```toml
[tasks.test]
description = "Run test suite"
alias = "t"
run = "pytest tests/"
```

Now `mise run t` works.

### Working Directory

```toml
[tasks.frontend]
dir = "packages/frontend"
run = "npm run build"
```

### Task-Specific Environment

```toml
[tasks.test]
env = { RUST_BACKTRACE = "1", LOG_LEVEL = "debug" }
run = "cargo test"
```

**Note**: `env` values are NOT passed to dependency tasks.

### GitHub Token Verification Task

For multi-account GitHub setups, add a verification task:

```toml
[tasks._verify-gh-auth]
description = "Verify GitHub token matches expected account"
hide = true  # Hidden helper task
run = """
expected="${GH_ACCOUNT:-}"
if [ -z "$expected" ]; then
  echo "GH_ACCOUNT not set - skipping verification"
  exit 0
fi
actual=$(gh api user --jq '.login' 2>/dev/null || echo "")
if [ "$actual" != "$expected" ]; then
  echo "ERROR: GH_TOKEN authenticates as '$actual', expected '$expected'"
  exit 1
fi
echo "✓ GitHub auth verified: $actual"
"""

[tasks.release]
description = "Create semantic release"
depends = ["_verify-gh-auth"]  # Verify before release
run = "npx semantic-release --no-ci"
```

See [`mise-configuration` skill](../mise-configuration/SKILL.md#github-token-multi-account-patterns) for GH_TOKEN setup.

> **SSH ControlMaster Warning**: If using multi-account SSH, ensure `ControlMaster no` is set for GitHub hosts in `~/.ssh/config`. Cached connections can authenticate with the wrong account.

### Multi-Command Tasks

```toml
[tasks.setup]
run = [
  "npm install",
  "npm run build",
  "npm run migrate"
]
```

---

## Level 3-4: Dependencies & Orchestration

### Pre-Execution Dependencies

```toml
[tasks.deploy]
depends = ["test", "build"]
run = "kubectl apply -f deployment.yaml"
```

Tasks `test` and `build` run BEFORE `deploy`.

### Post-Execution Tasks

```toml
[tasks.release]
depends = ["test"]
depends_post = ["notify", "cleanup"]
run = "npm publish"
```

After `release` succeeds, `notify` and `cleanup` run automatically.

### Soft Dependencies

```toml
[tasks.migrate]
wait_for = ["database"]
run = "./migrate.sh"
```

If `database` task is already running, wait for it. Otherwise, proceed.

### Task Chaining Pattern

```toml
[tasks.ci]
description = "Full CI pipeline"
depends = ["lint", "test", "build"]
depends_post = ["coverage-report"]
run = "echo 'CI passed'"
```

Single command: `mise run ci` executes entire chain.

### Parallel Dependencies

Dependencies without inter-dependencies run in parallel:

```toml
[tasks.validate]
depends = ["lint", "typecheck", "test"]  # These can run in parallel
run = "echo 'All validations passed'"
```

---

## Level 5: Hidden Tasks & Organization

### Hidden Tasks

```toml
[tasks._check-credentials]
description = "Verify credentials are set"
hide = true
run = '''
if [ -z "$API_KEY" ]; then
  echo "ERROR: API_KEY not set"
  exit 1
fi
'''

[tasks.deploy]
depends = ["_check-credentials"]
run = "deploy.sh"
```

Hidden tasks don't appear in `mise tasks` output but can be dependencies.

View hidden tasks: `mise tasks --hidden`

### Colon-Prefixed Namespacing

```toml
[tasks.test]
run = "pytest"

[tasks."test:unit"]
run = "pytest tests/unit/"

[tasks."test:integration"]
run = "pytest tests/integration/"

[tasks."test:e2e"]
run = "playwright test"
```

Run all test tasks: `mise run 'test:*'`

### Wildcard Patterns

```bash
mise run 'test:*'      # All tasks starting with test:
mise run 'db:**'       # Nested: db:migrate:up, db:seed:test
```

---

## Level 6: Task Arguments

### Usage Specification (Preferred Method)

```toml
[tasks.deploy]
description = "Deploy to environment"
usage = '''
arg "<environment>" help="Target environment" {
  choices "dev" "staging" "prod"
}
flag "-f --force" help="Skip confirmation"
flag "--region <region>" default="us-east-1" env="AWS_REGION"
'''
run = '''
echo "Deploying to ${usage_environment}"
[ "$usage_force" = "true" ] && echo "Force mode enabled"
echo "Region: ${usage_region}"
'''
```

### Argument Types

**Required positional**:

```toml
usage = 'arg "<file>" help="Input file"'
```

**Optional positional**:

```toml
usage = 'arg "[file]" default="config.toml"'
```

**Variadic (multiple values)**:

```toml
usage = 'arg "<files>" var=#true'
```

### Flag Types

**Boolean flag**:

```toml
usage = 'flag "-v --verbose"'
# Access: ${usage_verbose:-false}
```

**Flag with value**:

```toml
usage = 'flag "-o --output <file>" default="out.txt"'
# Access: ${usage_output}
```

**Environment-backed flag**:

```toml
usage = 'flag "--port <port>" env="PORT" default="8080"'
```

### Accessing Arguments

In `run` scripts, arguments become `usage_<name>` environment variables:

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
${usage_environment}      # Required arg value
${usage_verbose:-false}   # Boolean flag with default
${usage_output}           # Flag with value
SKILL_SCRIPT_EOF
```

**DEPRECATION WARNING**: The Tera template method (`{{arg(name="...")}}`) will be removed in mise 2026.11.0. Use `usage` spec instead.

For complete argument syntax, see: [arguments.md](./references/arguments.md)

---

## Level 7: File Tracking & Caching

### Source Files

```toml
[tasks.build]
sources = ["Cargo.toml", "src/**/*.rs"]
run = "cargo build"
```

Task re-runs only when source files change.

### Output Files

```toml
[tasks.build]
sources = ["Cargo.toml", "src/**/*.rs"]
outputs = ["target/release/myapp"]
run = "cargo build --release"
```

If outputs are newer than sources, task is **skipped**.

### Force Execution

```bash
mise run build --force  # Bypass caching
```

### Auto Output Detection

```toml
[tasks.compile]
outputs = { auto = true }  # Default behavior
run = "gcc -o app main.c"
```

---

## Level 8: Advanced Execution

### Confirmation Prompts

```toml
[tasks.drop-database]
confirm = "This will DELETE all data. Continue?"
run = "dropdb myapp"
```

### Output Control

```toml
[tasks.quiet-task]
quiet = true   # Suppress mise's output (not task output)
run = "echo 'This still prints'"

[tasks.silent-task]
silent = true  # Suppress ALL output
run = "background-job.sh"

[tasks.silent-stderr]
silent = "stderr"  # Only suppress stderr
run = "noisy-command"
```

### Raw Mode (Interactive)

```toml
[tasks.edit-config]
raw = true  # Direct stdin/stdout/stderr
run = "vim config.yaml"
```

**Warning**: `raw = true` disables parallel execution.

### Task-Specific Tools

```toml
[tasks.legacy-test]
tools = { python = "3.9", node = "18" }
run = "pytest && npm test"
```

Use specific tool versions for this task only.

### Custom Shell

```toml
[tasks.powershell-task]
shell = "pwsh -c"
run = "Get-Process | Select-Object -First 5"
```

---

## Level 9: Watch Mode

### Basic Watch

```bash
mise watch build  # Re-run on source changes
```

Requires `watchexec`: `mise use -g watchexec@latest`

### Watch Options

```bash
mise watch build --debounce 500ms  # Wait before re-run
mise watch build --restart          # Kill and restart on change
mise watch build --clear            # Clear screen before run
```

### On-Busy Behavior

```bash
mise watch build --on-busy-update=queue    # Queue changes
mise watch build --on-busy-update=restart  # Restart immediately
mise watch build --on-busy-update=do-nothing  # Ignore (default)
```

---

## Level 10: Monorepo (Experimental)

**Requires**: `MISE_EXPERIMENTAL=1` and `experimental_monorepo_root = true`

### Path Syntax

```bash
mise run //projects/frontend:build    # Absolute from root
mise run :build                       # Current config_root
mise run //...:test                   # All projects
```

### Wildcards

```bash
mise run '//projects/...:build'       # Build all under projects/
mise run '//projects/frontend:*'      # All tasks in frontend
```

### Discovery

Tasks in subdirectories are auto-discovered with path prefix:

- `packages/api/.mise.toml` tasks → `packages/api:taskname`

For complete monorepo documentation, see: [advanced.md](./references/advanced.md)

---

## Level 11: Polyglot Monorepo with Pants + mise

For Python-heavy polyglot monorepos (10-50 packages), combine **mise** for runtime management with **Pants** for build orchestration and native affected detection.

### Division of Responsibility

| Tool      | Responsibility                                                         |
| --------- | ---------------------------------------------------------------------- |
| **mise**  | Runtime versions (Python, Node, Rust) + environment variables          |
| **Pants** | Build orchestration + native affected detection + dependency inference |

### Architecture

```
monorepo/
├── mise.toml                    # Runtime versions + env vars (SSoT)
├── pants.toml                   # Pants configuration
├── BUILD                        # Root BUILD file (minimal)
├── packages/
│   ├── core-python/
│   │   ├── mise.toml           # Package-specific env (optional)
│   │   └── BUILD               # Auto-generated: python_sources()
│   ├── core-rust/
│   │   └── BUILD               # cargo-pants plugin
│   └── core-bun/
│       └── BUILD               # pants-js plugin
```

### Pants Native Affected Detection

**No more manual git scripts** - Pants has native affected detection:

```bash
# Test only affected packages (NATIVE)
pants --changed-since=origin/main test

# Lint only affected packages
pants --changed-since=origin/main lint

# Build only affected packages
pants --changed-since=origin/main package

# See what's affected (dry run)
pants --changed-since=origin/main list
```

### mise.toml Wrapper Tasks (Optional Convenience)

```toml
[tasks."test:affected"]
description = "Test affected packages via Pants"
run = "pants --changed-since=origin/main test"

[tasks."lint:affected"]
description = "Lint affected packages via Pants"
run = "pants --changed-since=origin/main lint"

[tasks.test-all]
description = "Test all packages"
run = "pants test ::"

[tasks."pants:tailor"]
description = "Generate BUILD files"
run = "pants tailor"
```

### pants.toml Minimal Config

```toml
[GLOBAL]
pants_version = "<version>"
backend_packages = [
    "pants.backend.python",
    "pants.backend.python.lint.ruff",
    "pants.backend.experimental.rust",
    "pants.backend.experimental.javascript",
]

[python]
interpreter_constraints = [">=3.11"]

[source]
root_patterns = ["packages/*"]

[python-bootstrap]
# Use mise-managed Python (mise sets PATH)
search_path = ["<PATH>"]
```

### When to Use Pants + mise

| Scale                             | Recommendation                             |
| --------------------------------- | ------------------------------------------ |
| < 10 packages                     | mise + custom affected (Level 10 patterns) |
| **10-50 packages (Python-heavy)** | **Pants + mise** (this section)            |
| 50+ packages                      | Consider Bazel                             |

→ See [polyglot-affected.md](./references/polyglot-affected.md) for complete Pants + mise integration guide and tool comparison

---

## Integration with [env]

Tasks automatically inherit `[env]` values:

```toml
[env]
DATABASE_URL = "postgresql://localhost/mydb"
_.file = ".env"  # Load additional env vars

[tasks.migrate]
run = "diesel migration run"  # $DATABASE_URL available
```

### Credential Loading Pattern

```toml
[env]
_.file = { path = ".env.secrets", redact = true }

[tasks._check-env]
hide = true
run = '[ -n "$API_KEY" ] || { echo "Missing API_KEY"; exit 1; }'

[tasks.deploy]
depends = ["_check-env"]
run = "deploy.sh"
```

---

## Anti-Patterns

| Anti-Pattern                    | Why Bad                                       | Instead                                                                  |
| ------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------ |
| Replace /itp:go with mise tasks | No TodoWrite, no ADR tracking, no checkpoints | Use mise tasks for project workflows, /itp:go for ADR-driven development |
| Hardcode secrets in tasks       | Security risk                                 | Use `_.file = ".env.secrets"` with `redact = true`                       |
| Giant monolithic tasks          | Hard to debug, no reuse                       | Break into small tasks with dependencies                                 |
| Skip `description`              | Poor discoverability                          | Always add descriptions                                                  |
| Publish without build `depends` | Runtime failure instead of DAG prevention     | Add `depends = ["build"]` to publish tasks                               |
| Orchestrator without all phases | "Run X next" messages get ignored             | Include all phases in `release:full` depends array                       |

For release-specific anti-patterns and patterns, see [Release Workflow Patterns](./references/release-workflow-patterns.md).

---

## Cross-Reference: mise-configuration

**Prerequisites**: Before defining tasks, ensure `[env]` section is configured.

> **PRESCRIPTIVE**: After defining tasks, invoke **[`mise-configuration` skill](../mise-configuration/SKILL.md)** to ensure [env] SSoT patterns are applied.

The `mise-configuration` skill covers:

- `[env]` - Environment variables with defaults
- `[settings]` - mise behavior configuration
- `[tools]` - Version pinning
- Special directives: `_.file`, `_.path`, `_.python.venv`

---

## Additional Resources

- [Task Patterns](./references/patterns.md) - Real-world task examples
- [Task Arguments](./references/arguments.md) - Complete usage spec reference
- [Advanced Features](./references/advanced.md) - Monorepo, watch, experimental
- [Polyglot Affected](./references/polyglot-affected.md) - Pants + mise integration guide and tool comparison
- [Bootstrap Monorepo](./references/bootstrap-monorepo.md) - Autonomous polyglot monorepo bootstrap meta-prompt
- [Release Workflow Patterns](./references/release-workflow-patterns.md) - Release task DAG patterns, build-before-publish enforcement

---

## Troubleshooting

| Issue                  | Cause                     | Solution                                   |
| ---------------------- | ------------------------- | ------------------------------------------ |
| Task not found         | Typo or wrong mise.toml   | Run `mise tasks` to list available tasks   |
| Dependencies not run   | Circular dependency       | Check task depends arrays for cycles       |
| Sources not working    | Wrong glob pattern        | Use relative paths from mise.toml location |
| Watch not triggering   | File outside sources list | Add file pattern to sources array          |
| Env vars not available | Task in wrong directory   | Ensure mise.toml is in cwd or parent       |
| Run fails with error   | Script path issue         | Use absolute path or relative to mise.toml |
