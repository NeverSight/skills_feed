---
name: forge
description: >
  FORGE (Framework for Orchestrated Resilient Generative Engineering) — Unified AI-driven
  development framework combining multi-agent agile workflows, autonomous iteration loops,
  persistent memory, Claude Code Skills architecture, MCP service integration, and n8n
  workflow automation. Use when: building software projects end-to-end, planning architecture,
  running autonomous dev loops, creating MCP servers, orchestrating n8n workflows, setting up
  CI/CD pipelines, managing multi-agent development teams, or any structured AI-driven
  development task.
  Triggers: "forge", "autonomous dev", "agent loop", "agile planning", "multi-agent",
  "development pipeline", "scaffold project", "run forge", "autopilot".
---

# FORGE — Framework for Orchestrated Resilient Generative Engineering

## French Language Rule

All content generated in French MUST use proper accents (é, è, ê, à, ù, ç, ô, î, etc.), follow French grammar rules (agreements, conjugations), and use correct spelling.

## Philosophy

FORGE unifies five paradigms into one secure, production-grade system:

| Paradigm                      | What FORGE Takes                                                  | What FORGE Improves                                                  |
| ----------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------------- |
| **Multi-Agent Agile**         | Agent personas, artifact-driven workflows, scale-adaptive planning | Lighter agent definitions, no npm installer dependency               |
| **Autonomous Iteration**      | Iteration loops, exit detection, rate limiting                     | Sandboxed execution, cost caps, rollback gates                       |
| **Claude Skills**             | Progressive disclosure, SKILL.md structure, scripts/references     | Native integration, auto-discovery                                   |
| **Persistent Memory**         | Project memory, session tracking, agent-specific context           | Security-first: sandbox isolation, input validation, least privilege |
| **Workflow Automation (n8n)** | Webhook triggers, MCP bridge, pipeline orchestration               | Declarative workflow-as-code, version-controlled pipelines           |

## Quick Start

```bash
# 1. Initialize FORGE in any project
/forge-init

# 2. Choose track based on project scale
#    → Quick (bug fix, small feature): 3 commands
#    → Standard (feature, module): full pipeline
#    → Enterprise (system, platform): all agents + governance

# 3. Run the pipeline
/forge-plan       # Agent: Analyst + PM → PRD artifact
/forge-architect  # Agent: Architect → Architecture artifact
/forge-ux         # Agent: UX → UX design, wireframes, accessibility
/forge-stories    # Agent: SM → Stories with test specs
/forge-build      # Agent: Dev → Code + unit tests + functional tests
/forge-verify     # Agent: QA → Audit Dev tests + advanced tests + certification
/forge-deploy     # Automated deployment pipeline

# Autopilot mode — FORGE decides everything
/forge-auto           # Full pipeline, FORGE drives
/forge-auto "goal"    # Autopilot with specific objective

# Multi-agent collaboration
/forge-party "topic"  # Launch 2-3 agents in parallel on a topic
/forge-status         # Sprint status, stories, metrics

# Quick commands
/forge-quick-spec     # Quick track: spec + implement
/forge-quick-test     # Quick QA: zero-config testing
/forge-review <path>  # Adversarial review of an artifact
```

---

## 1. AGENTS — Multi-Agent Personas

FORGE agents are lightweight Markdown personas. Each agent is a role Claude adopts
with specific expertise, constraints, and outputs.

### 1.1 Agent Registry

Load agent definitions from `references/agents/` only when needed.

| Agent            | Role                                                            | Trigger             | Output Artifact                         |
| ---------------- | --------------------------------------------------------------- | ------------------- | --------------------------------------- |
| **Orchestrator** | Meta-agent, routing, party mode, parallelization                | `/forge-party`      | Orchestration plan                      |
| **Analyst**      | Requirements elicitation, domain research                       | `/forge-analyze`    | `docs/analysis.md`                      |
| **PM**           | Product requirements, user stories, prioritization              | `/forge-plan`       | `docs/prd.md`                           |
| **Architect**    | System design, tech stack, API contracts                        | `/forge-architect`  | `docs/architecture.md`                  |
| **UX**           | User research, wireframes, accessibility                        | `/forge-ux`         | `docs/ux-design.md`                     |
| **Dev**          | Implementation, code generation, unit + functional tests        | `/forge-build`      | Source code + tests                     |
| **SM**           | Story decomposition, sprint planning, context sharding          | `/forge-stories`    | `docs/stories/*.md`                     |
| **QA**           | Audit Dev tests, advanced tests (8 TEA workflows), validation   | `/forge-verify`     | Quality report + supplementary tests    |
| **Quick QA**     | Zero-config testing, automatic framework detection              | `/forge-quick-test` | Tests + quick report                    |
| **Reviewer**     | Adversarial review, devil's advocate                            | `/forge-review`     | Critical review report                  |
| **DevOps**       | CI/CD, deployment, infrastructure                               | `/forge-deploy`     | Pipeline configs                        |
| **Security**     | Threat modeling, audit, compliance                              | `/forge-audit`      | `docs/security.md`                      |

### 1.2 Agent Invocation Pattern

```markdown
## Activating an Agent

When user requests `/forge-plan`, Claude:

1. Reads `references/agents/pm.md` for persona definition
2. Adopts the PM persona (expertise, constraints, output format)
3. Runs the associated workflow (elicitation → drafting → validation)
4. Produces the artifact in `docs/`
5. Returns to base Claude persona
```

### 1.3 Scale-Adaptive Intelligence

FORGE auto-detects project scale and adjusts depth:

- **Quick Track** (bug fix, hotfix, <1 day):
  - Skip: Analysis, Architecture, Stories
  - Run: `/forge-quick-spec` → generates spec + implements
  - Agents: Dev only
  - Tests: Dev writes unit + functional tests for the fix

- **Standard Track** (feature, module, 1-5 days):
  - Run: Plan → Architect → Stories (with test specs) → Build (code + tests) → Verify (audit + advanced tests)
  - Agents: PM, Architect, SM, Dev, QA
  - Tests: SM specifies → Dev writes unit + functional → QA audits + completes

- **Enterprise Track** (system, platform, 5+ days):
  - Run: Full lifecycle with governance gates
  - Agents: All + Security + DevOps
  - Extras: ADRs, threat model, compliance checks
  - Tests: Complete + performance + security + cross-module E2E

---

## 2. WORKFLOWS — Structured Pipelines

### 2.1 Core Development Pipeline

```
Analysis → Planning → Architecture → UX Design → Stories → Implementation+Tests → Verification → Deployment
   │           │           │            │           │              │                    │              │
   ▼           ▼           ▼            ▼           ▼              ▼                    ▼              ▼
analysis.md  prd.md  architecture.md ux-design.md stories/   src/ + tests/       quality report    deployed
                                                 (with test    (unit + func)      (audit + advanced
                                                  specs)                          tests)
```

### 2.2 Artifact-Driven Context

Every phase produces a versioned artifact. Downstream agents consume upstream artifacts,
eliminating context loss:

```
PM reads analysis.md → produces prd.md
Architect reads prd.md → produces architecture.md
UX reads prd.md + architecture.md → produces ux-design.md
SM reads architecture.md + prd.md + ux-design.md → produces stories/*.md (with test specs)
Dev reads story file → implements code + unit tests + functional tests
QA reads story file + Dev tests → audits, completes (integration/E2E/perf/security), certifies
```

### 2.3 Integrated Test Strategy (Test-Driven Story Development)

Tests are integrated at EVERY stage of the pipeline, not just the verification phase.

#### Responsibilities per Agent

```
SM (/forge-stories)  → Specifies tests in each story:
                        - Unit test cases (TU-x) per function/component
                        - Mapping AC-x → functional test
                        - Test data / fixtures
                        - Test files to create

Dev (/forge-build)   → Writes AND runs tests alongside code:
                        - Unit tests BEFORE code (TDD)
                        - Functional tests for each AC-x
                        - Coverage >80% on new code
                        - Story NOT done if tests fail

QA (/forge-verify)   → Audits, completes, and certifies:
                        - Audit: did the Dev write all required tests?
                        - Completes: integration, E2E, performance, security tests
                        - Certifies: GO/NO-GO verdict
```

#### Test Structure

```
tests/
├── unit/                    # Unit tests (Dev) — per module
│   ├── <module>/
│   │   └── <file>.test.<ext>
├── functional/              # Functional tests (Dev) — per feature
│   ├── <feature>/
│   │   └── <scenario>.test.<ext>
├── integration/             # Integration tests (QA) — cross-component
│   └── <scenario>.test.<ext>
├── e2e/                     # E2E tests (QA) — full user journeys
│   └── <journey>.test.<ext>
├── fixtures/                # Shared test data
│   └── <name>.fixture.<ext>
└── helpers/                 # Test utilities
    └── setup.<ext>
```

#### Validation Gate

No story moves to "done" without:

- Unit tests present and passing (>80% coverage)
- Functional tests present for each AC-x and passing
- Non-regression validated (pre-existing tests not broken)

### 2.4 n8n Workflow Integration

For automated pipelines, FORGE generates n8n-compatible workflow definitions.
See `.claude/skills/forge/n8n-integration.md` for:

- Webhook-triggered build pipelines
- MCP server exposure of FORGE commands
- Automated deployment workflows
- Monitoring and alerting patterns

### 2.5 Document Sharding (token optimization)

Large artifacts are split into sections to optimize token consumption.
Each agent only loads the sections relevant to its work.

```
# Principle: split on ## (heading level 2)

docs/prd.md (complete)
  → Section "Functional Requirements" → loaded by SM, Dev
  → Section "Non-Functional Requirements" → loaded by Architect, QA
  → Section "User Stories" → loaded by SM
  → Section "Constraints" → loaded by all

# Sharding rules:
# - An agent NEVER loads an entire artifact if it doesn't need it
# - Sections are identified by their ## heading
# - The Orchestrator determines the relevant sections per agent
```

### 2.6 Artifact Modes (Create / Validate / Edit)

Each artifact supports 3 operating modes:

| Mode         | When                                       | Behavior                                             |
| ------------ | ------------------------------------------ | ---------------------------------------------------- |
| **Create**   | Artifact does not exist                    | Full generation from scratch                         |
| **Validate** | Artifact exists, verification requested    | Checks consistency, completeness, compliance         |
| **Edit**     | Artifact exists, modifications requested   | Incremental update, preserves valid content          |

```
# Automatic mode detection:
# - If docs/prd.md does not exist → Create mode
# - If /forge-plan --validate → Validate mode
# - If /forge-plan "add feature X" → Edit mode (PRD already exists)
```

### 2.7 Sprint Status (/forge-status)

FORGE maintains a `.forge/sprint-status.yaml` file for tracking:

```yaml
# Read via /forge-status
sprint:
  id: 1
  started_at: '2025-01-15'
  stories:
    - id: story-001
      title: '...'
      status: completed # pending | in_progress | completed | blocked
      assigned_to: dev
      blockedBy: []
    - id: story-002
      title: '...'
      status: in_progress
      assigned_to: dev
      blockedBy: [story-001]
  metrics:
    total: 5
    completed: 2
    in_progress: 1
    blocked: 0
    pending: 2
    velocity: '2 stories/day'
```

---

## 3. AUTONOMOUS LOOPS — Iteration Engine

### 3.1 Loop Architecture

FORGE provides autonomous iteration with security guardrails:

```bash
# FORGE Autonomous Loop
/forge-loop "Implement authentication module" --max-iterations 20 --sandbox docker

# How it works:
# 1. Claude receives task + PROMPT.md
# 2. Works on implementation
# 3. Tries to exit → Stop hook intercepts
# 4. Same prompt re-fed with file system state
# 5. Loop continues until:
#    a. Completion criteria met (tests pass + EXIT_SIGNAL)
#    b. Max iterations reached
#    c. Cost cap hit
#    d. Circuit breaker triggers (repeated errors)
```

### 3.2 Security Guardrails

```yaml
# .forge/config.yml — Loop Security
loop:
  max_iterations: 30 # Hard cap
  cost_cap_usd: 5.00 # Per-loop spending limit
  timeout_minutes: 60 # Per-iteration timeout
  mode: hitl # afk | hitl | pair
  rate_limit_per_hour: 60 # Max iterations per hour
  state_directory: .forge-state/ # State persistence
  sandbox:
    enabled: true # ALWAYS for AFK loops
    provider: docker # docker | e2b | local
    mount_readonly: # Read-only mounts
      - ./docs
      - ./references
    mount_readwrite: # Read-write mounts
      - ./src
      - ./tests
    network: restricted # No outbound except allowed domains
    allowed_domains: # Whitelist for network access
      - registry.npmjs.org
      - pypi.org
  circuit_breaker:
    consecutive_errors: 3 # Stop after 3 consecutive failures
    no_progress_iterations: 5 # Stop if no git diff for N iterations
    same_output_repeats: 3 # Stop if same output repeated N times
  rollback_gate:
    enabled: true # Git tag checkpoint before each iteration
    max_checkpoints: 5 # Keep last N checkpoints
```

### 3.3 Loop Modes

| Mode     | Behavior             | HITL Gates                          | Usage              |
| -------- | -------------------- | ----------------------------------- | ------------------ |
| **afk**  | Fully autonomous     | None                                | Overnight, batch   |
| **hitl** | Semi-autonomous      | Confirmation every 5 iterations     | Default            |
| **pair** | Collaborative        | Continuous explanation, small commits| Active development |

```bash
# Examples
/forge-loop "task" --mode afk --max-iterations 50   # Overnight
/forge-loop "task" --mode hitl                       # Default
/forge-loop "task" --mode pair                       # Pair programming
```

### 3.4 State Management

Each loop maintains its state in `.forge-state/`:

```
.forge-state/
├── state.json      # Current state (iteration, errors, mode, status)
├── history.jsonl   # Complete event history
└── fix_plan.md     # In-loop task plan
```

### 3.5 Checkpoint and Rollback

```bash
# Automatic checkpoints via git tags
# Each iteration creates: forge-ckpt-iter-N
# The last 5 are kept

# List checkpoints
forge-loop.sh checkpoint-list

# Restore a checkpoint
forge-loop.sh rollback --story forge-ckpt-iter-5
```

### 3.6 PROMPT.md Template

The PROMPT.md template is automatically generated by `forge-loop.sh` and includes:

- Task description
- Story context (if provided)
- Reference to fix_plan.md for tracking
- Mode-specific instructions (afk/hitl/pair)
- Completion criteria
- Current state (iteration, errors, progress)

See `.claude/skills/forge/loop-patterns.md` for advanced patterns.

---

## 4. PERSISTENT MEMORY — Project Continuity

### 4.1 Memory Architecture

FORGE maintains persistent Markdown-based memory to ensure continuity across sessions.
Every `/forge-*` command reads memory at start and writes updates at end.

```
.forge/memory/
├── MEMORY.md                    # Core project knowledge (long-term)
├── sessions/
│   ├── 2025-01-15.md            # Daily session log
│   ├── 2025-01-16.md
│   └── ...
└── agents/
    ├── pm.md                    # PM agent-specific memory
    ├── architect.md             # Architect decisions log
    ├── dev.md                   # Dev patterns, gotchas
    └── qa.md                    # QA coverage state, known issues
```

### 4.2 Two-Layer Memory

| Layer              | File                              | Purpose                              | Updated By          |
| ------------------ | --------------------------------- | ------------------------------------ | ------------------- |
| **Long-term**      | `.forge/memory/MEMORY.md`         | Project state, decisions, milestones | All agents          |
| **Session**        | `.forge/memory/sessions/DATE.md`  | Daily log of what was done           | Auto per session    |
| **Agent-specific** | `.forge/memory/agents/AGENT.md`   | Context specific to each agent role  | Respective agent    |

### 4.3 Memory Protocol

Every FORGE command follows this protocol:

```
START:
  1. Read .forge/memory/MEMORY.md → project context
  2. Read latest session log → recent activity
  3. Read agent-specific memory → role context (if applicable)
  4. forge-memory search "<task summary>" --limit 3
     → Load relevant fragments as additional context

EXECUTE:
  5. Perform the command's work
  6. Track decisions, issues, and progress
  7. If additional context needed: forge-memory search "<question>"

END:
  8. Update MEMORY.md → current state, decisions, blockers
  9. Append to session log → what was done
  10. Update agent memory → role-specific context
  11. Update sprint-status.yaml → story states
```

### 4.4 Memory + Autopilot Integration

The memory system is what makes `/forge-auto` intelligent:

- FORGE reads MEMORY.md to know exactly where the project is
- It reads session logs to understand recent activity and avoid repeating work
- It reads agent memories to provide continuity to each agent role
- On resume, FORGE picks up exactly where it left off

### 4.5 Memory Configuration

```yaml
# .forge/config.yml
memory:
  enabled: true          # Enable persistent memory
  auto_save: true        # Auto-save after each command
  session_logs: true     # Keep daily session logs
  agent_memory: true     # Per-agent memory files
```

### 4.6 Vector Search (Mémoire Vectorielle)

FORGE enrichit sa mémoire Markdown avec un index vectoriel SQLite pour des recherches sémantiques rapides.

#### Architecture

```
.forge/memory/
  MEMORY.md              <- source de vérité
  sessions/YYYY-MM-DD.md <- source de vérité
  agents/{agent}.md      <- source de vérité
  index.sqlite           <- index dérivé (auto-synchronisé)
```

- **Sync unidirectionnelle** : Markdown = maître, SQLite = index dérivé
- **Auto-sync** : avant chaque recherche, les fichiers modifiés sont réindexés
- **Recherche hybride** : similarité vectorielle (70%) + FTS5 BM25 mots-clés (30%)
- **Embeddings locaux** : `all-MiniLM-L6-v2` (384 dims, ~80 Mo)
- **Chunking markdown-aware** : ~400 tokens/chunk, respect des headings et blocs de code

#### Utilisation dans le protocole mémoire

```
START:
  1. Read .forge/memory/MEMORY.md -> project context
  2. Read latest session log -> recent activity
  3. Read agent-specific memory -> role context
  4. forge-memory search "<task summary>" --limit 3
     -> Charge uniquement les fragments pertinents comme contexte additionnel

EXECUTE:
  5. Perform work
  6. Track decisions
  7. Si besoin de contexte en cours : forge-memory search "<question>"

END:
  8-9-10-11. (inchangé -- écriture markdown)
  [IMPLICITE] L'auto-sync réindexera au prochain search
```

#### Installation

```bash
bash ~/.claude/skills/forge/scripts/forge-memory/setup.sh
```

#### Commandes CLI

```bash
forge-memory sync [--force] [--verbose]
forge-memory search "query" [--namespace all|project|session|agent] [--agent NAME] [--limit 5]
forge-memory status [--json]
forge-memory reset --confirm
```

---

## 5. SECURITY MODEL

### 4.1 Threat Model

FORGE addresses the "Lethal Trifecta" (Simon Willison, 2025):

1. **Untrusted input** → All external data treated as potentially hostile
2. **Tool access** → Least privilege, sandbox isolation
3. **Autonomous execution** → Human-in-the-loop gates for destructive actions

### 4.2 Security Layers

```
┌─────────────────────────────────────────────┐
│ Layer 1: Input Validation                    │
│  - Prompt injection detection                │
│  - Schema validation on all MCP inputs       │
│  - Content sanitization                      │
├─────────────────────────────────────────────┤
│ Layer 2: Sandbox Isolation                   │
│  - Docker/E2B containers for AFK loops       │
│  - Read-only mounts for sensitive files      │
│  - Network whitelist (no arbitrary outbound)  │
├─────────────────────────────────────────────┤
│ Layer 3: Credential Management               │
│  - NO plaintext secrets in config files      │
│  - Environment variables injected at runtime │
│  - Secret rotation support                   │
│  - Scoped access tokens (not master keys)    │
├─────────────────────────────────────────────┤
│ Layer 4: Audit & Rollback                    │
│  - Git checkpoint before each iteration      │
│  - Full audit log of all tool invocations    │
│  - Instant rollback via git reset            │
│  - Cost tracking per loop/session            │
├─────────────────────────────────────────────┤
│ Layer 5: Human Gates                         │
│  - Destructive operations require approval   │
│  - Deployment gates (staging → production)   │
│  - Budget approval for expensive operations  │
└─────────────────────────────────────────────┘
```

### 4.3 Skill Validation (from Cisco research on OpenClaw)

Before loading any third-party skill:

```bash
# Validate skill for security threats
/forge-audit-skill <path-to-skill>

# Checks:
# - No suspicious network calls in scripts
# - No credential harvesting patterns
# - No prompt injection in SKILL.md
# - No file access outside declared scope
# - Dependencies audited (npm audit / pip audit)
```

---

## 6. MCP INTEGRATION

### 6.1 FORGE as MCP Server

FORGE exposes its capabilities as MCP tools for external clients.

```typescript
// FORGE MCP Server — exposes development tools
tools: [
  'forge_analyze', // Run analysis phase
  'forge_plan', // Generate PRD
  'forge_architect', // Generate architecture
  'forge_build', // Run implementation loop
  'forge_verify', // Run test suite
  'forge_deploy', // Deploy to environment
  'forge_status', // Get project status
  'forge_loop', // Start autonomous loop
];
```

### 6.2 Consuming MCP Servers

FORGE can connect to external MCP servers for enhanced capabilities:

```yaml
# .forge/mcp-servers.yml
servers:
  n8n:
    url: 'http://localhost:5678/mcp'
    auth: api_key
    tools: [create_workflow, execute_workflow, list_workflows]

  github:
    url: 'https://mcp.github.com'
    auth: oauth
    tools: [create_issue, create_pr, list_issues]

  database:
    url: 'http://localhost:3001/mcp'
    auth: api_key
    tools: [query, migrate, backup]
    readonly: true # Security: read-only by default
```

### 6.3 n8n Workflow Automation

FORGE generates n8n workflows for CI/CD automation:

```json
{
  "name": "FORGE Deploy Pipeline",
  "nodes": [
    { "type": "webhook", "name": "Git Push Trigger" },
    { "type": "claude-code", "name": "Run Tests", "params": { "prompt": "/forge-verify" } },
    { "type": "if", "name": "Tests Pass?" },
    { "type": "claude-code", "name": "Build", "params": { "prompt": "/forge-build --production" } },
    { "type": "ssh", "name": "Deploy to Server" },
    { "type": "slack", "name": "Notify Team" }
  ]
}
```

---

## 7. PROJECT SCAFFOLDING

### 7.1 /forge-init Command

Initialize FORGE in any project:

```
project-root/
├── .forge/
│   ├── config.yml          # FORGE configuration
│   ├── mcp-servers.yml     # MCP server connections
│   ├── memory/             # Persistent memory
│   │   ├── MEMORY.md       # Core project knowledge
│   │   ├── sessions/       # Daily session logs
│   │   └── agents/         # Agent-specific memories
│   └── templates/          # Artifact templates
├── docs/
│   ├── analysis.md         # Analyst output
│   ├── prd.md              # PM output
│   ├── architecture.md     # Architect output
│   ├── security.md         # Security audit
│   └── stories/            # SM output (stories with test specs)
│       ├── story-001.md
│       └── ...
├── src/                    # Source code (Dev output)
├── tests/                  # Tests (Dev + QA output)
│   ├── unit/               # Unit tests per module (Dev)
│   ├── functional/         # Functional tests per feature (Dev)
│   ├── integration/        # Integration tests (QA)
│   ├── e2e/                # E2E tests (QA)
│   ├── fixtures/           # Shared test data
│   └── helpers/            # Test utilities
├── CLAUDE.md               # Project conventions (auto-generated)
└── PROMPT.md               # Loop prompt (when using /forge-loop)
```

### 7.2 CLAUDE.md Auto-Generation

FORGE generates a `CLAUDE.md` tailored to the project:

```markdown
# CLAUDE.md — Generated by FORGE

## Project

[Auto-detected from package.json/go.mod/Cargo.toml/etc.]

## Architecture

[Summary from docs/architecture.md]

## Conventions

- Commits: conventional commits (type(scope): description)
- Tests: MANDATORY for all new code (unit + functional per story)
- Reviews: all changes via PR
- Coverage: >80% minimum on new code

## FORGE Commands

- /forge-plan — Generate/update PRD
- /forge-architect — Generate/update architecture
- /forge-stories — Decompose into stories with test specs
- /forge-build — Code implementation + unit tests + functional tests
- /forge-loop "task" — Autonomous iteration loop
- /forge-auto — Full autopilot mode
- /forge-verify — Test audit + advanced tests + QA certification
- /forge-deploy — Deploy
- /forge-status — Project status
```

---

## 8. CONFIGURATION

### 8.1 .forge/config.yml

```yaml
project:
  name: 'my-project'
  type: auto-detect # web-app | api | library | cli | mobile
  language: auto-detect # typescript | python | go | rust | etc.
  scale: auto-detect # quick | standard | enterprise

agents:
  default_set: standard # quick | standard | enterprise | custom
  custom_agents: [] # Path to custom agent definitions

loop:
  max_iterations: 30
  cost_cap_usd: 10.00
  sandbox:
    enabled: true
    provider: docker

memory:
  enabled: true
  auto_save: true
  session_logs: true
  agent_memory: true

security:
  audit_skills: true # Validate third-party skills
  sandbox_loops: true # Sandbox all autonomous loops
  credential_store: env # env | vault | keyring
  allowed_domains: [] # Network whitelist for sandbox

mcp:
  servers: [] # External MCP server connections
  expose: false # Expose FORGE as MCP server

n8n:
  enabled: false
  instance_url: ''
  api_key_env: 'N8N_API_KEY' # Env var name (NOT the key itself)

deploy:
  provider: '' # hostinger | docker | k8s | vercel | custom
  staging_url: ''
  production_url: ''
  require_approval: true # Human gate for production deploy
```

---

## 9. REFERENCE FILES

Load these resources as needed during development:

### Agent Definitions

- `references/agents/orchestrator.md` — Orchestrator meta-agent, party mode, parallelization
- `references/agents/analyst.md` — Analyst persona, workflows, outputs
- `references/agents/pm.md` — Product Manager persona
- `references/agents/architect.md` — Architect persona
- `references/agents/ux.md` — UX/Design persona, wireframes, accessibility
- `references/agents/dev.md` — Developer persona
- `references/agents/sm.md` — Scrum Master persona
- `references/agents/qa.md` — QA/TEA persona (8 workflows)
- `references/agents/quick-qa.md` — Quick QA, zero-config testing
- `references/agents/reviewer.md` — Adversarial reviewer
- `references/agents/devops.md` — DevOps persona
- `references/agents/security.md` — Security persona

### Integration Guides

- `.claude/skills/forge/n8n-integration.md` — n8n workflow patterns, MCP bridge setup
- `.claude/skills/forge/loop-patterns.md` — Autonomous loop patterns, prompt engineering
- `.claude/skills/forge/security-model.md` — Detailed security architecture

### Templates

- `.forge/templates/prd.md` — PRD template
- `.forge/templates/architecture.md` — Architecture document template
- `.forge/templates/story.md` — Story template (context-rich, self-contained)
- `.forge/templates/sprint-status.yaml` — Sprint status tracking template
- `.forge/templates/ux-design.md` — UX design document template

### Workflows (Declarative YAML)

- `.forge/workflows/standard.yaml` — Standard track workflow
- `.forge/workflows/quick.yaml` — Quick track workflow
- `.forge/workflows/enterprise.yaml` — Enterprise track workflow

### Scripts

- `.claude/skills/forge/forge-init.sh` — Project initialization
- `.claude/skills/forge/forge-loop.sh` — Secured autonomous loop runner
- `.claude/skills/forge/audit-skill.py` — Skill security auditor
