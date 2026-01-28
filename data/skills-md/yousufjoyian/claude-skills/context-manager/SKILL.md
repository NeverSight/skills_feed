---
name: context-manager
description: Maintain compiled context artifacts for stateless agent spawning. This skill produces BOOT_CONTEXT (stable project brain), DELTA_CONTEXT (recent changes), and feature bundles so any agent can spawn with deep understanding without reading the entire repo. Use this skill when setting up multi-agent workflows or when agents need fast, token-efficient onboarding.
---

# Context Manager Skill (CMS)

**Triggers:** "compile context", "update context", "cms compile", "cms update", "refresh context"

## Purpose

Maintain a set of compiled context artifacts so any agent can spawn stateless and still get deep, up-to-date understanding without rereading the entire repo.

CMS produces:
- **BOOT_CONTEXT** - stable, curated project brain
- **DELTA_CONTEXT** - what changed since last compile
- **Feature bundles** - compartmentalized working sets for parallel agents
- **MANIFEST** - hashes, pointers, provenance for deterministic rehydration

Agents consume these artifacts on startup instead of scanning the repo.

## Output Artifacts

All artifacts live in `.claude/compiled/`:

```
.claude/compiled/
├── BOOT_CONTEXT.md      # Stable project brain (~500-1500 tokens)
├── DELTA_CONTEXT.md     # Recent changes (~200-500 tokens)
├── FEATURES/            # Working-set context slices
│   ├── <feature>.md
│   └── ...
├── MANIFEST.json        # Hashes, timestamps, provenance
└── FEATURE_MAP.yaml     # Feature definitions
```

### BOOT_CONTEXT.md

**Goal:** The smallest truthful "project brain" that doesn't change often.

**Contains:**
- Architecture overview
- Invariants and constraints
- Key flows
- File map
- Conventions
- "How to work here" guidance

**Rules:**
- Keep dense but stable
- Decision-oriented, not narrative
- Never include giant code blocks; only pointers
- Target: 500-1500 tokens

### DELTA_CONTEXT.md

**Goal:** What changed since last compile, with implications.

**Contains:**
- Commit summary since baseline
- File changes with descriptions
- Behavior changes
- New decisions
- New open questions
- Agent action items

**Rules:**
- Always small (target: 200-500 tokens)
- Must answer: "What's different now and why it matters?"
- Reset on full compile

### Feature Bundles (FEATURES/*.md)

**Goal:** Working-set context slices for parallel agents.

Each feature file includes:
- Purpose
- Key files (with line pointers where relevant)
- Invariants
- Current tasks
- Known issues
- Interface contracts (inputs/outputs)

### MANIFEST.json

**Goal:** Deterministic rehydration + auditing.

Tracks:
- Hashes of source files considered
- Hashes of compiled artifacts
- Last compile time
- Commit baseline
- Feature definitions and membership

## Agent Boot Contract

Every worker agent spawn uses this startup order:

1. Read `.claude/compiled/BOOT_CONTEXT.md`
2. Read `.claude/compiled/DELTA_CONTEXT.md`
3. If working on a scoped task: read `.claude/compiled/FEATURES/<feature>.md`
4. Only open raw files referenced by those docs

**Hard prohibition:** Do not scan directories or "rediscover architecture" unless CMS explicitly marks "unknown".

This is what makes the system save tokens.

## CMS Modes

### Mode 1: Compile (Full Rebuild)

**Triggers:**
- "compile context" / "cms compile"
- No MANIFEST exists
- Major architecture changes
- BOOT_CONTEXT quality degraded (manual trigger)
- Baseline commit changed significantly

**Output:**
- BOOT_CONTEXT regenerated
- DELTA reset to "since compile"
- All features refreshed
- New MANIFEST written

### Mode 2: Update (Incremental)

**Triggers:**
- "update context" / "cms update"
- New commits since baseline
- File timestamps changed
- Agent outcomes logged (new decisions/blockers)
- Feature bundle needs refresh

**Output:**
- DELTA_CONTEXT updated
- BOOT_CONTEXT updated only if stable knowledge truly changed
- Relevant feature bundles updated
- New MANIFEST written

## Compile Protocol

### Step 1: Establish Current State

```bash
PROJECT=$(basename $(pwd))
COMPILED_DIR=.claude/compiled

mkdir -p $COMPILED_DIR/FEATURES

# Get current git state
git rev-parse HEAD
git status --porcelain
```

### Step 2: Read Key Architecture Files

Read to understand:
- Entry points (main files, index files)
- Configuration (package.json, tsconfig, etc.)
- Existing documentation (README, PROJECT.md)
- Core source files

### Step 3: Generate BOOT_CONTEXT.md

Write using template from `references/BOOT_CONTEXT_TEMPLATE.md`:

```markdown
# BOOT_CONTEXT | <project> | <timestamp>

## Architecture
[Dense overview - what this project IS]

## Invariants
[Rules that must never be broken]

## Key Flows
[How data/control moves through the system]

## File Map
[Critical files with purposes - NOT every file]

## Conventions
[Code style, naming, patterns to follow]

## How to Work Here
[Agent-specific guidance for this codebase]
```

### Step 4: Generate DELTA_CONTEXT.md

On full compile, write:

```markdown
# DELTA_CONTEXT | <project> | <timestamp>

## Baseline
Compiled from: [commit hash]
No prior delta - clean compile.

## Changes
None - fresh compile.

## Agent Actions
Read BOOT_CONTEXT, then proceed with assigned task.
```

### Step 5: Generate Feature Bundles

Read `FEATURE_MAP.yaml` (create if missing using template).

For each feature, generate `FEATURES/<feature>.md`:

```markdown
# Feature: <name>

## Purpose
[What this feature does]

## Key Files
- `path/file.ts:L10-50` - [what it does]

## Invariants
[Rules for this feature]

## Current Tasks
- [ ] Task from CONTEXT.md if applicable

## Known Issues
- [Issue] → [Workaround]

## Interface
**Inputs:** [what this feature receives]
**Outputs:** [what this feature produces]
**Depends on:** [other features]
```

### Step 6: Write MANIFEST.json

```json
{
  "compiled_at": "2026-01-20T23:00:00-05:00",
  "mode": "compile",
  "baseline": {
    "git_commit": "abc123def",
    "dirty": false
  },
  "inputs": {
    "files": {
      "src/index.ts": "sha256:...",
      "package.json": "sha256:..."
    }
  },
  "outputs": {
    "BOOT_CONTEXT.md": "sha256:...",
    "DELTA_CONTEXT.md": "sha256:...",
    "FEATURES/api.md": "sha256:..."
  },
  "features": {
    "api": {
      "files": ["src/api/"],
      "keywords": ["endpoint", "route", "handler"]
    }
  }
}
```

### Step 7: Confirm

```
CMS Compile Complete

BOOT_CONTEXT.md: Generated (1,234 tokens)
  - Architecture: 5 sections
  - File map: 12 files

DELTA_CONTEXT.md: Reset (clean compile)

Features: 3 bundles
  - api: 4 files tracked
  - ui: 6 files tracked
  - data: 2 files tracked

MANIFEST.json: Written
  Baseline: abc123def
  Compiled: 2026-01-20 23:00
```

## Update Protocol

### Step 1: Read Existing Manifest

```bash
MANIFEST=.claude/compiled/MANIFEST.json

# If no manifest, trigger full compile instead
if [ ! -f "$MANIFEST" ]; then
  echo "No manifest - run compile first"
  exit 1
fi

BASELINE=$(jq -r '.baseline.git_commit' $MANIFEST)
```

### Step 2: Detect Changes

```bash
# Files changed since baseline
git diff --name-only $BASELINE HEAD

# Uncommitted changes
git status --porcelain
```

### Step 3: Classify Changes

Bucket each changed file:
- **Hot files** (core): affects architecture/flows
- **Feature files**: belongs to a feature bundle
- **Noise**: docs, formatting, unrelated

### Step 4: Extract Facts

For each relevant changed file, record high-level changes:
- New endpoint added
- Function behavior changed
- Config flag added
- File created/deleted

Keep it factual, not narrative.

### Step 5: Update DELTA_CONTEXT.md

```markdown
# DELTA_CONTEXT | <project> | <timestamp>

## Baseline
Prior compile: [old commit] → Current: [new commit]

## Changes Since Baseline
- `src/api/routes.ts` - Added /users/:id endpoint
- `src/utils/cache.ts` - NEW: caching utility
- `config.json` - Added CACHE_TTL setting

## Implications
- New endpoint requires auth middleware
- Caching may affect test isolation

## New Decisions
- Use in-memory cache for v1 (rationale: simplicity)

## Risks / Blockers
- Cache invalidation strategy TBD

## Agent Actions
1. When working on API: note new /users/:id endpoint
2. When writing tests: account for cache side effects
```

### Step 6: Check if BOOT Needs Update

BOOT_CONTEXT changes **only if**:
- Architecture changed (new major component)
- Invariants changed
- File map changed (new critical file)
- Canonical flow changed

If only DELTA-level changes, BOOT stays stable.

### Step 7: Update Feature Bundles

For each feature whose files changed:
- Update key files list
- Update current tasks
- Update pitfalls/gotchas
- Update interface contracts if changed
- Ensure cross-links valid

### Step 8: Write New MANIFEST

Update all hashes, timestamp, and baseline.

### Step 9: Confirm

```
CMS Update Complete

BOOT_CONTEXT.md: Unchanged
DELTA_CONTEXT.md: Updated
  - 3 file changes
  - 1 new decision
  - 2 agent actions

Features: 1 updated
  - api: +1 file, tasks updated

MANIFEST.json: Updated
  Baseline: abc123 → def456
  Updated: 2026-01-20 23:30
```

## Feature System

### FEATURE_MAP.yaml

```yaml
# Feature definitions for parallel agent work

api:
  description: REST API endpoints and handlers
  files:
    - src/api/
    - src/routes/
  keywords: ["endpoint", "route", "handler", "middleware"]
  depends_on: []

ui:
  description: Frontend components and views
  files:
    - src/components/
    - src/views/
  keywords: ["component", "render", "useState", "props"]
  depends_on: [api]

data:
  description: Data layer and storage
  files:
    - src/models/
    - src/db/
  keywords: ["model", "schema", "query", "database"]
  depends_on: []
```

### Feature Bundle Rules

A feature bundle must include:
- What it **owns** (files)
- What it **depends on** (other features)
- What it **guarantees** (contracts)
- Where to find **truth** (authoritative files)

## Multi-Agent Safety

### Per-Agent Runtime Notes

```
.claude/runtime/agents/<agent_id>/SESSION.md
```

Each agent writes its own session notes here.

### Project-Wide State

`.claude/CONTEXT.md` remains the official shared human-approved state.

Agents propose updates, CMS (or human) merges them.

### Merge Rule

- CMS can ingest SESSION logs from agents
- CMS must NOT overwrite shared context silently
- CMS writes:
  - "Proposed additions" into DELTA
  - "Conflicts detected" section if agents diverged

## Integration with Existing Skills

| Skill | Relationship |
|-------|--------------|
| `session-save` | Human-facing session handoff; CMS is agent-facing compiled context |
| `context-extract` | Verbose history archive; CMS is optimized snapshot |
| `onboard` | Should read BOOT_CONTEXT + DELTA if available |

### When to Use Each

| Need | Use |
|------|-----|
| Quick human handoff | `session-save` |
| Full history archive | `context-extract` |
| Agent spawning | `context-manager` (this) |
| Getting up to speed | `onboard` + CMS artifacts |

## Resources

Templates in `references/`:
- `BOOT_CONTEXT_TEMPLATE.md` - Template for BOOT_CONTEXT
- `DELTA_CONTEXT_TEMPLATE.md` - Template for DELTA_CONTEXT
- `FEATURE_TEMPLATE.md` - Template for feature bundles
- `MANIFEST_SCHEMA.json` - JSON schema for MANIFEST
- `FEATURE_MAP_TEMPLATE.yaml` - Template for feature definitions
