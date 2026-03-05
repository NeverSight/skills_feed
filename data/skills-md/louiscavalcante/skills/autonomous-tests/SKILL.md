---
name: autonomous-tests
description: 'Run autonomous E2E tests. Args: staged | unstaged | N (last N commits) | working-tree
  | file:<path> | rescan | guided [description] (default: working-tree with smart doc analysis). Example: /autonomous-tests guided "payment checkout flow"'
argument-hint: 'staged | unstaged | N | working-tree | file:<path> | rescan | guided'
disable-model-invocation: true
allowed-tools: Bash(*), Read(*), Write(*), Edit(*), Glob(*), Grep(*), Agent(*),
  EnterPlanMode(*), ExitPlanMode(*), TaskCreate(*),
  TaskUpdate(*), TaskList(*), TaskGet(*), TeamCreate(*),
  SendMessage(*), TeamDelete(*), AskUserQuestion(*)
hooks:
  PreToolUse:
    - matcher: ExitPlanMode
      hooks:
        - type: command
          command: "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\"}}'"
    - matcher: AskUserQuestion
      hooks:
        - type: command
          command: "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\"}}'"
---

## Dynamic Context

- Args: $ARGUMENTS
- Branch: !`git branch --show-current`
- Unstaged: !`git diff --stat HEAD 2>/dev/null | tail -5`
- Staged: !`git diff --cached --stat 2>/dev/null | tail -5`
- Commits: !`git log --oneline -5 2>/dev/null`
- Docker: !`docker compose ps 2>/dev/null | head -10 || echo "No docker-compose found"`
- Config: !`test -f .claude/autonomous-tests.json && echo "YES" || echo "NO -- first run"`
- Agent Teams: !`python3 -c "import json;s=json.load(open('$HOME/.claude/settings.json'));print('ENABLED' if s.get('env',{}).get('CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS')=='1' else 'DISABLED')" 2>/dev/null || echo "DISABLED -- settings not found"`
- Capabilities: !`python3 -c "import json;c=json.load(open('.claude/autonomous-tests.json'));caps=c.get('capabilities',{});mcps=len(caps.get('dockerMcps',[]));ab='Y' if caps.get('frontendTesting',{}).get('agentBrowser') else 'N';pw='Y' if caps.get('frontendTesting',{}).get('playwright') else 'N';ec=sum(1 for s in c.get('externalServices',[]) if s.get('cli',{}).get('available'));print(f'MCPs:{mcps} agent-browser:{ab} playwright:{pw} ext-clis:{ec} scanned:{caps.get(\"lastScanned\",\"never\")}')" 2>/dev/null || echo "NOT SCANNED"`

## Role

Project-agnostic autonomous E2E test runner. Exercise features against the live LOCAL stack, verify state at every step, produce documentation, never touch production.

## Orchestrator Protocol

The main agent is the Orchestrator. It coordinates phases but NEVER executes operational work.

**Orchestrator MUST delegate to agents:**
- Bash commands (capabilities scan, health checks, port scanning, cleanup)
- Source code reading (only agents read application source)
- File generation (docs, reports)
- Test execution, fix application, verification

**Orchestrator MAY directly:**
- Read config, SKILL.md, and reference files
- Run `date -u` for timestamps, `test -f` for file checks
- Enter/exit plan mode
- Use AskUserQuestion for user interaction
- Use TeamCreate/TaskCreate/TaskUpdate/SendMessage for coordination
- Compile summaries from agent reports
- Make phase-gating decisions (proceed/stop/abort)

**Reporting hierarchy:** Agent → Orchestrator → Plan

## Arguments: $ARGUMENTS

| Arg | Meaning |
|---|---|
| _(empty)_ | Default: working-tree (staged + unstaged) with smart doc analysis |
| `staged` | Staged changes only |
| `unstaged` | Unstaged changes only |
| `N` (number) | Last N commits (e.g., `1` = last commit) |
| `working-tree` | Staged + unstaged (same as default) |
| `file:<path>` | `.md` doc as additional test context. Combinable. |
| `rescan` | Force capabilities re-scan. Combinable. |
| `guided` | User augmentation mode — bypasses git diff. Alone: prompts for doc or description. |
| `guided "desc"` | Description-based: happy-path workflows only, user performs actions. |
| `guided file:<path>` | Doc-based: happy-path workflows only, user performs actions. |

Space-separated, combinable (e.g., `staged file:docs/feature.md rescan`). `file:` validated as existing `.md` relative to project root.

**Guided mode** — user augmentation (NOT automation):
- **Doc-based** (`guided file:<path>` or pick from `docs/`/`_autonomous/pending-guided-tests/`): happy-path workflows only.
- **Description-based** (`guided "description"` or describe when prompted): happy-path workflows only.

User performs all actions on their real device/browser. Claude provides step-by-step instructions and verifies results via DB queries/API/logs. Only happy-path workflows in guided mode. Categories 2-9 handled exclusively in autonomous mode — NEVER in guided session. No agent-browser, no Playwright — guided mode never loads or uses browser automation tools.

`guided` alone prompts via `AskUserQuestion` to pick a doc or describe a feature. Combinable with `rescan` but NOT with `staged`/`unstaged`/`N`/`working-tree` (git-scope args incompatible — guided bypasses git diff).

Smart doc analysis always active in standard mode: match `docs/` files to changed code by path, feature name, cross-references — read only relevant docs.

Print resolved scope, then proceed without waiting.

---

## Phase 0 — Bootstrap

**Config hash method**: `python3 -c "import json,hashlib;d=json.load(open('.claude/autonomous-tests.json'));[d.pop(k,None) for k in ('_configHash','lastRun','capabilities')];print(hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest())"` — referenced throughout as "Config hash method".

**Step 0: Prerequisites Check** — Read `~/.claude/settings.json`:
1. **Agent teams flag**: `env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` must be `"1"`. If not → STOP: "Run `bash <skill-dir>/scripts/setup-hook.sh` to enable agent teams and the ExitPlanMode hook."
2. **ExitPlanMode hook** (informational): if missing → inform user the skill-scoped hook handles it automatically; global setup available via the script. Continue.
3. **AskUserQuestion hook** (informational): same as above. Continue.

**Step 1: Capabilities Scan** — Triggers: `rescan` arg, `capabilities` missing, or `lastScanned` older than `rescanThresholdDays` (default 7 days). If none → use cache.

Spawn **Explore agent** (`subagent_type: "Explore"`, no `team_name`) to perform:
1. **Docker MCP Discovery**: `mcp-find` for MCPs matching service names and generic queries. Record `name`, `description`, `mode`; `safe: true` only for known sandbox MCPs. If unavailable → empty array.
2. **Frontend Testing**: `which agent-browser`, `which playwright`/`npx playwright --version` → set `frontendTesting` booleans.
3. **External Service CLI Detection**: Load `references/external-services-catalog.json`. Scan CLAUDE.md files for `claudeMdKeywords`. Per match: run `detectionCommand` → if unavailable, `cli.available: false` → if available, run `modeDetection.command` → pattern-match: production → `live`/blocked, sandbox → `sandbox`/unblocked, else → `unknown`/unblocked → warn if blocked → populate `allowedOperations`/`prohibitedFlags` → merge into `externalServices[]`.

Agent reports back. Orchestrator writes to `capabilities` with `lastScanned` = UTC time (`date -u`).

**CLAUDE.md deep scan** (Phase 0 + Phase 2): `find . -maxdepth 3 -name "CLAUDE.md" -type f` + `~/.claude/CLAUDE.md` + `.claude/CLAUDE.md`. Cache list for: capabilities scan, auto-extract, Phase 2 enrichment, Feature Context Document. Read each once.

**Step 2: Config Check** — `test -f .claude/autonomous-tests.json && echo "CONFIG_EXISTS" || echo "CONFIG_MISSING"`. Schema: `references/config-schema.json`.

### If `CONFIG_EXISTS` (returning run):
1. Read config.
2. **Version validation**: require `version: 5` + fields `project`, `database`, `testing`. v4→v5: migrate `*Cli` fields from `capabilities` to `externalServices[].cli`. v3→v4→v5: add empty `capabilities` first. <3 or missing fields → warn, re-run first-run.
   - Missing `database.seedStrategy` → default `"autonomous"`, inform user.
   - Missing `documentation.fixResults` → add `"docs/_autonomous/fix-results"`.
   - Legacy `userContext.credentialType` → delete silently.
3. **Config trust**: Compute hash using **Config hash method**. Check trust store `~/.claude/trusted-configs/{project-hash}.sha256` (project hash: `python3 -c "import hashlib,os;print(hashlib.sha256(os.path.realpath('.').encode()).hexdigest()[:16])"`). Mismatch → show config (redact `testCredentials` values as `"********"`) → `AskUserQuestion` for approval → write hash.
4. **Testing priorities**: Show `userContext.testingPriorities`. `AskUserQuestion`: "Pain points or priorities?" with "None" option to clear. Update config.
5. **Re-scan services**: Delegate to Explore agent (same as Step 1). Update config if needed.
6. `date -u +"%Y-%m-%dT%H:%M:%SZ"` → update `lastRun`.
7. Empty `userContext` → run questionnaire below, save.
8. **Re-stamp trust**: if config modified → recompute using **Config hash method**, write to trust store.
9. Skip to Phase 1.

### If `CONFIG_MISSING` (first run):
Spawn **Explore agent** (`subagent_type: "Explore"`, no `team_name`) for auto-extraction:
1. **Auto-extract** from CLAUDE.md files (deep scan) + compose + env + package manifests. Detect `migrationCommand`/`cleanupCommand` from compose, `scripts/`, Makefiles, package.json (`manage.py migrate`, `npx prisma migrate deploy`, `knex migrate:latest`, etc.). Detect seed commands.
   **DB type**: MongoDB (`mongosh`/`mongo`, `mongoose`/`mongodb`/`@typegoose`, `mongodb://`, mongo containers) vs SQL (`psql`/`mysql`/`sqlite3`, `pg`/`mysql2`/`sequelize`/`prisma`/`knex`/`typeorm`/`drizzle`/`sqlalchemy`/`django.db`, `postgres://`/`mysql://`/`sqlite:///`, SQL containers). Both found → ask user.
2. **Topology**: `single` | `monorepo` (workspace configs, multiple `package.json`, `backend/`+`frontend/`) | `multi-repo` (CLAUDE.md cross-refs, sibling `.git`, shared docker-compose).
3. **Related projects**: scan sibling dirs, grep for external paths → ask user per candidate → populate `relatedProjects`.

Agent reports. Orchestrator proceeds:
4. **Capabilities scan** — delegate (Step 1).
5. **Seeding strategy** via `AskUserQuestion`: autonomous (recommended, agents create per-suite data) or command (global seed command).
6. **User Context Questionnaire** (all at once, partial OK): flaky areas? credentials (env var/role names only)? priorities? notes? → store in `userContext`.
7. **Propose config** → STOP for confirmation → write.
8. **Stamp trust**: compute using **Config hash method** → write to trust store.
9. If CLAUDE.md < 140 lines and lacks startup instructions → append max 10 lines.

## Phase 1 — Safety & Environment

**Objective**: Verify the environment is safe and ready for testing.

Spawn ONE **general-purpose agent** (`model: "opus"`, no `team_name`) to perform:
1. **Production scan**: `.env` files for `productionIndicators`, `*LIVE*SECRET*`, `NODE_ENV=production`, production DB endpoints (RDS, Atlas without dev/stg/test), non-local URLs. Show variable NAME only.
2. Run `sandboxCheck` commands from config.
3. Verify Docker is local.
4. **Service startup**: per service in config + related projects with `startCommand`: health check → healthy: `already-running` → unhealthy: start + poll 5s/30s → `started-this-run` or report failure.
5. Start webhook listeners.
6. **Service Readiness Report**: per service — name, URL/port, health status, health check endpoint, source (`config`|`relatedProject`).

Agent reports: safety assessment + Service Readiness Report. Gates: **ABORT** if production. **STOP** if unhealthy. Keep report for Phase 3.

## Phase 2 — Discovery

Fully autonomous — derive from code diff, codebase, or guided source. Never ask what to test.

**Delegation**: ONE Explore agent (`subagent_type: "Explore"`, no `team_name` — pre-team).

### Standard mode
1. Changed files from git (scope args) — include `relatedProjects[].path` for cross-project deps.
2. If `file:<path>` → read `.md`, extract features/criteria/endpoints/edge cases (supplements diff).
3. **Spawn Explore agent** with: changed files, file reference content, `relatedProjects[]`, `testing.contextFiles`, CLAUDE.md paths, `documentation.*` paths. Agent performs:
   - **Feature map**: API endpoints, DB ops (MongoDB: `find`/`aggregate`/`insertMany`/`updateOne`/`deleteMany`/`bulkWrite`/`createIndex`/schema changes; SQL: `SELECT`/`INSERT`/`UPDATE`/`DELETE`/`JOIN`/`GROUP BY`/`CREATE TABLE`/`ALTER TABLE`/`CREATE INDEX`/migrations/ORM), external services, business logic, auth flows, signal/event chains
   - **Dependency graph**: callers → changed code → callees, cross-file/project imports
   - **Smart doc analysis**: (a) match paths/features/endpoints against `docs/` (read relevant only), (b) `_autonomous/` scan (Summary + Issues Found only, extract prior failures/bugs), (c) fix completion scan (`RESOLVED`+`PASS` → regression targets, `Ready for Re-test: YES` → priority)
   - **Edge case inventory**: error handlers, validation branches, race conditions, retry logic
4. Receive structured report.

### Guided mode (user augmentation)
**Validate first**: `guided` + `staged`/`unstaged`/`N`/`working-tree` → STOP with combinability error.
1. **Resolve source**: `guided file:<path>` → doc-based | `guided "desc"` → description-based | `guided` alone → `AskUserQuestion` (pick doc or describe).
2. **Spawn Explore agent** with: source content, mode type, `relatedProjects[]`, `testing.contextFiles`, CLAUDE.md paths, `documentation.*` paths. Agent performs: deep feature analysis (keywords, endpoints, models, workflows via Glob/Grep, import tracing) + same feature map/dependency/doc analysis/edge cases as standard. Agent also identifies: DB seed requirements per test, external service setup needs, prerequisite state for each happy-path workflow.
3. Receive report. Orchestrator extracts only happy-path workflows — discard security, edge case, validation, race condition findings (those are autonomous-only).

### Feature Context Document (both modes)
Compile from Explore report (do NOT re-read files). Contents: features, endpoints, DB collections/tables, external services, edge cases, test history, file reference content, capabilities. Guided mode adds `Mode` + `Source` at top. Cascaded to every Phase 4 agent.

## Phase 3 — Plan (Plan Mode)

**Enter plan mode (/plan).** Plan starts with:

**Step 0 — Context Reload** (for post-approval reconstruction):
- Re-read: SKILL.md, config, `references/templates.md`
- Scope: `$ARGUMENTS`, branch, commit range
- Findings: Phase 2 discoveries (modules, endpoints, dependencies)
- User context: flaky areas, priorities, notes
- Service Readiness Report from Phase 1 (agents use directly, MUST NOT start services or re-check health)
- If guided: type, source, and full guided test list with per-test seed requirements

**Tool loading gate**: If autonomous mode needs agent-browser/Playwright, list tools and prompt user via AskUserQuestion before plan approval. Declined tools excluded from plan. Guided mode: NEVER include browser automation tools — skip this gate entirely.

**Self-containment mandate** — the plan MUST embed directly (not reference "above" or prior phases):
1. All test suites with full details (name, objective, pre-conditions, steps, expected outcomes, teardown, verification)
2. Feature Context Document (condensed but complete)
3. Service Readiness Report from Phase 1
4. Per-suite agent spawn instructions with resolved values (env, steps, verification, credential role name, DB lifecycle, browser priority chain)
5. Config paths: `documentation.*`, `database.connectionCommand`, `testing.unitTestCommand`, `testDataPrefix`
6. Credential role names from `testCredentials`
7. If guided: per-test DB seed commands, user-facing step-by-step instructions, and verification queries

- Execution Protocol — autonomous mode (embed verbatim — orchestrator uses this after context reset):
  ```
  TEAM: TeamCreate → general-purpose team (team_name for all agents)
  MODEL: Always model: "opus"
  SETUP AGENT: Spawn first (general-purpose, opus, team_name). Reads source files, compiles Feature Context Document, reports via SendMessage. Shut down before suite agents.
  FLOW: STRICTLY SEQUENTIAL — one suite agent at a time:
    1. TaskCreate per suite (env, steps, verification, teardown, Feature Context Document, credential role name, Service Readiness Report, DB lifecycle, browser priority chain)
    2. TaskUpdate with owner
    3. For each suite (in order):
       a. Spawn ONE agent (general-purpose, opus, team_name)
       b. Assign via TaskUpdate
       c. BLOCK — wait for completion
       d. SendMessage type: "shutdown_request"
       e. Wait for shutdown confirmation
       f. Report PASS/FAIL
       g. Next suite
  PROHIBITED: multiple agents alive, spawning N+1 before N shutdown, parallel execution, main-conversation execution
  SHUTDOWN: SendMessage shutdown_request to all teammates after completion
  AUDIT: agents spawned count, suites executed, cleanup status
  ```

- Execution Protocol — guided mode (embed verbatim):
  ```
  MODE: User augmentation
  NO BROWSER AUTOMATION: agent-browser and Playwright MUST NOT be loaded
  CATEGORIES: Happy-path workflows ONLY
  FLOW: For each guided test (in order):
    1. Spawn ONE agent for DB seeding + external service setup
    2. Agent seeds database, configures services
    3. Agent reports readiness → shut down
    4. Orchestrator presents steps to user via AskUserQuestion
    5. User performs actions on real device/browser
    6. Orchestrator verifies results via DB queries/API/logs
    7. Record PASS/FAIL → next test
  PROHIBITED: agent-browser, Playwright, security/edge-case/validation tests
  ```

**Test categories** — standard (autonomous): all 9. Guided mode (both sub-modes): category 1 ONLY. Categories 2-9 never in guided. Non-happy-path findings queued as pending-autonomous-tests.

1. **Happy path** — normal expected flows end-to-end
2. **Invalid inputs & validation** — malformed data, missing fields, wrong types, boundary values
3. **Duplicate/idempotent requests** — rapid same-call repetition, verify no duplicate records/charges/side-effects
4. **Error handling** — trigger every error branch (network failures, invalid states, auth failures, permission denials)
5. **Unexpected DB changes** — orphaned records, missing refs, unintended mutations, index-less slow queries
6. **Race conditions & timing** — concurrent writes, out-of-order webhooks, expired tokens mid-flow
7. **Security** — injection (SQL/NoSQL/command/LDAP/XPath/SSTI/header/log), XSS (stored/reflected/DOM)/CSRF/clickjacking, auth bypass/broken access/privilege escalation/session mgmt/JWT manipulation, data exposure (sensitive responses/stack traces/metadata/timing), input attacks (file uploads: sizes/zip bombs/polyglots/path traversal; payloads: oversized/nested/type confusion/prototype pollution; params: injection/pollution/encoding; headers: host injection/SSRF; volume: rate limiting/ReDoS), infrastructure (SSRF/path traversal/deserialization/known vulns/misconfig/logging), compliance (data minimization/PII/consent/retention). Findings → `### Vulnerabilities` in test-results. Each: risk, exploit scenario, impact, mitigation, priority (data leaks > credentials > escalation > DoS > compliance).
8. **Edge cases from code reading** — test every `if/else`, `try/catch`, guard clause, fallback
9. **Regression** — existing unit tests + re-verify previously broken flows

Each suite: name, objective, pre-conditions, steps + expected outcomes, teardown, verification queries. **Wait for user approval.**

## Phase 4 — Execution (Agent Teams)

`TeamCreate` → spawn `general-purpose` agents sequentially. Always `model: "opus"`. Coordinate via `TaskCreate`/`TaskUpdate`/`SendMessage`.

**Setup agent** (mandatory): spawn first (`general-purpose`, `opus`, `team_name`) to read source files, compile Feature Context Document, report via `SendMessage`. Shut down after.

**Credential assignment**: Rotate role names from `testCredentials` across suites. Task descriptions include only the **role name** — never values or env var refs. Agents resolve at runtime.

**Cascading context**: Every agent receives full Feature Context Document from Phase 2.

**Capability-aware execution**: Agents leverage detected capabilities from config.

**Browser test enforcement (autonomous mode ONLY)** — priority order (skipping without attempting is PROHIBITED):
1. `agent-browser` (PRIMARY) if available — `open <url>` → `snapshot -i` → `click/fill @ref` → re-snapshot
2. Playwright (FALLBACK) if agent-browser unavailable/errors
3. Direct HTTP/API (LAST RESORT) — mark untestable parts as "guided"

**Guided mode**: No browser automation. User performs all UI interactions. Agents only seed DB, configure services, and verify outcomes.

- `mcp-add` for `safe: true` MCPs relevant to suite. NEVER `safe: false`.
- **External CLI gate**: per `externalServices[]` where `cli.available && !cli.blocked` and plan depends on it → `AskUserQuestion` once per service using `userPromptTemplate`. Declined → "guided". Approved → `cli.approvedThisRun: true`, only `allowedOperations`. NEVER use when `cli.blocked`.

**Anomaly detection** — agents watch for: duplicate records, unexpected DB changes, warning/error logs, slow queries/missing indexes, orphaned references, auth token anomalies, unexpected response fields/status codes.

**Finding verification** (mandatory): Before reporting any finding: (1) identify source code, (2) read to confirm real behavior vs test artifacts, (3) distinguish real vs agent-created, (4) report only confirmed. Unconfirmed → `Severity: Unverified` in `### Unverified` subsection.

**API Response Security Inspection** — analyze ALL responses for:
- *Exposed identifiers*: internal DB IDs, sequential/guessable IDs, sensitive refs (paths, internal URLs)
- *Leaked secrets*: API keys, tokens beyond scope, passwords/hashes, env vars in errors, cloud secrets
- *Personal data* (multi-regulation): PII (names, emails, phones, addresses, govt IDs, DOB), sensitive (health/financial/biometric/racial/political/religious/sexual/genetic), regulations (LGPD, GDPR, CCPA/CPRA, HIPAA, others)

Verify against source: read model/serializer/DTO to confirm field exists in real schema — not test data. False positives MUST NOT be reported. Each finding: Severity, Regulatory impact, Exploitability, Compliance risk → `### API Response Security` subsection.

**Execution flow**:
1. `TaskCreate` per suite — include: env details, steps, verification queries, teardown, Feature Context Document, credential **role name**, browser tools/status, Service Readiness Report (use directly, no re-check), DB lifecycle:
   - Pre-test: `migrationCommand` → seed (`autonomous`: create with `testDataPrefix`; `command`: run `seedCommand`)
   - Verification: `connectionCommand` for queries
   - Post-test: `cleanupCommand` or clean `testDataPrefix` data. Order: migrate → seed → test → cleanup.
   - Browser: include workflow + priority chain. "Do NOT skip browser suites."
2. `TaskUpdate` with `owner`
3. Strictly sequential:
   ```
   for each suite_task in approved_suite_tasks (in order):
       1. Spawn ONE agent (general-purpose, opus, team_name)
       2. Assign via TaskUpdate
       3. BLOCK — wait for completion
       4. Shut down via SendMessage shutdown_request
       5. Wait for shutdown confirmation
       6. Report PASS/FAIL
       7. Proceed to next
   ```
   Prohibited: multiple agents alive, spawning N+1 before N shut down, concurrent assignment, parallel execution, main-conversation execution.
4. PASS/FAIL + anomalies after each suite
5. Shut down all teammates after completion
6. **Audit summary**: agents spawned, suites executed, docker exec count, cleanup status

## Phase 5 — Results & Docs

**Objective**: Process results, generate documentation, clean up test data.

**Fix cycle**: Runtime-fixable (env/container/stuck job) → delegate fix to agent → re-run suite → max 3 cycles. Code bug → document (file, line, expected vs actual) → ask user.

**Documentation**: Delegate to agent. Timestamp via `date -u +"%Y-%m-%d-%H-%M-%S"`. Pattern: `{timestamp}_{semantic-name}.md`. Read `references/templates.md` first. Four doc types: test-results (always), pending-fixes (bugs/infra issues), pending-guided-tests (browser/visual/physical), pending-autonomous-tests (identified but not run). Re-runs → append "Re-run" section.

**Cleanup**: Delegate to agent. Remove `testDataPrefix` data only. Never touch pre-existing. Log actions. Verify with DB query.

## Phase 6 — Finalize

> **Important**: Run `/clear` before invoking another skill (e.g., `/autonomous-fixes`) to free context window tokens and prevent stale state from interfering with the next operation.

---

## Rules

| Rule | Detail |
|---|---|
| No production | Never modify production data or connect to production services |
| No credentials in output | Never expose credentials, keys, tokens, or env var values — pass role names only |
| Plan before execution | Phase 3 plan mode required before any test execution |
| Agent Teams only | TeamCreate → TaskCreate → agents with `team_name`. Plain `Agent` without `team_name` PROHIBITED in Phases 4-5 |
| Always opus | All agents spawned with `model: "opus"` |
| Strictly sequential | One agent at a time in Phases 4-5. Spawn → complete → shut down → next |
| Explore agents read-only | No file edits or state-modifying commands |
| UTC timestamps | Via `date -u` only, never guess |
| No unsafe MCPs | Never activate `safe: false` MCPs |
| External CLI gating | Blocked when `cli.blocked`. Per-run user confirmation. `allowedOperations` only. `prohibitedFlags`/`prohibitedOperations` always blocked |
| No dynamic commands | Only execute verbatim config commands — no generation/concatenation/interpolation |
| Finding verification | Verify against source code before reporting any finding |
| Idempotent test data | Prefix with `testDataPrefix`. Skip or reset if exists |
| External API care | Delays between calls, sandbox modes, minimize requests |
| `_autonomous/` reading | Summary + Issues Found sections only |
| Capabilities auto-detected | Never ask user to configure manually |
| Guided = user augmentation | No browser automation in guided mode — user performs all actions |
| Guided = happy path only | Category 1 only in guided mode — categories 2-9 autonomous-only |
| Tool loading gate | Browser tools need pre-plan approval in autonomous mode, never in guided |
| Plan self-containment | All context embedded in plan for post-reset survival — no "see above" references |

## Operational Bounds

| Bound | Constraint |
|---|---|
| Max agents | Approved test suites + one setup agent |
| Max fix cycles | 3 per suite |
| Health check timeout | 30s per service |
| Capability cache | `rescanThresholdDays` (default 7 days) |
| Command scope | User-approved config commands only |
| Docker scope | Local only — Phase 1 aborts on production indicators |
| Credential scope | Env var references only — raw values forbidden, redacted on display |
| MCP scope | `safe: true` only |
| Agent lifecycle | One suite agent at a time in Phases 4-5 |
| Explore agent scope | One per Phase 2. Read-only. No `team_name` |
| External CLI scope | `allowedOperations` only. Per-run confirmation. Blocked when `cli.blocked` |
| System commands | `which`, `docker compose ps`, `git branch`/`diff`/`log`, `test -f`, `find . -maxdepth 3 -name "CLAUDE.md" -type f`, `date -u`, `curl -sf` localhost, `python3 -c` json/hashlib only |
| External downloads | Docker images via user's compose only. Playwright browsers if present. No other downloads |
| Data access | Outside project: `~/.claude/settings.json` (RO), `~/.claude/trusted-configs/` (RW, one hash), `~/.claude/CLAUDE.md` (RO). `.env` scanned for patterns only — values never stored/logged |
| Trust boundaries | Config SHA-256 verified out-of-repo. Untrusted inputs → analysis only → plan → user approval. No interpolation into commands |
