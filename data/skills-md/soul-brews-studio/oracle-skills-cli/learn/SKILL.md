---
name: learn
description: Explore a codebase with parallel Haiku agents. Modes - --fast (1 agent), default (3), --deep (5). Use when user says "learn [repo]", "explore codebase", "study this repo".
---

# /learn - Deep Dive Learning Pattern

Explore a codebase with 3 parallel Haiku agents → create organized documentation.

## Usage

```
/learn [url]             # Auto: clone via ghq, symlink origin/, then explore
/learn [slug]            # Use slug from ψ/memory/slugs.yaml
/learn [repo-path]       # Path to repo
/learn [repo-name]       # Finds in ψ/learn/owner/repo
/learn --init            # Restore all origins after git clone (like submodule init)
```

## Depth Modes

| Flag | Agents | Files | Use Case |
|------|--------|-------|----------|
| `--fast` | 1 | 1 overview | Quick scan, "what is this?" |
| (default) | 3 | 3 docs | Normal exploration |
| `--deep` | 5 | 5 docs | Master complex codebases |

```
/learn --fast [target]   # Quick overview (1 agent, ~2 min)
/learn [target]          # Standard (3 agents, ~5 min)
/learn --deep [target]   # Deep dive (5 agents, ~10 min)
```

## Directory Structure

```
ψ/learn/
├── .origins             # Manifest of learned repos (committed)
└── owner/
    └── repo/
        ├── origin       # Symlink to ghq source (gitignored)
        ├── repo.md      # Hub file - links to all sessions (committed)
        └── YYYY-MM-DD/  # Date folder
            ├── 1349_ARCHITECTURE.md      # Time-prefixed files
            ├── 1349_CODE-SNIPPETS.md
            ├── 1349_QUICK-REFERENCE.md
            ├── 1520_ARCHITECTURE.md      # Second run same day
            └── ...
```

**Multiple learnings**: Each run gets time-prefixed files (HHMM_), nested in date folder.

**Offload source, keep docs:**
```bash
unlink ψ/learn/owner/repo/origin   # Remove symlink
ghq rm owner/repo                  # Remove source
# Docs remain in ψ/learn/owner/repo/
```

## /learn --init

Restore all origins after cloning (like `git submodule init`):

```bash
ROOT="$(pwd)"
# Read .origins manifest and restore symlinks
while read repo; do
  ghq get -u "https://github.com/$repo"
  OWNER=$(dirname "$repo")
  REPO=$(basename "$repo")
  mkdir -p "$ROOT/ψ/learn/$OWNER/$REPO"
  ln -sf "$(ghq root)/github.com/$repo" "$ROOT/ψ/learn/$OWNER/$REPO/origin"
  echo "✓ Restored: $repo"
done < "$ROOT/ψ/learn/.origins"
```

## Step 0: Detect Input Type + Resolve Path

```bash
date "+🕐 %H:%M %Z (%A %d %B %Y)"
```

**CRITICAL: Capture ABSOLUTE paths first (before spawning any agents):**
```bash
ROOT="$(pwd)"
echo "Learning from: $ROOT"
```

**IMPORTANT FOR SUBAGENTS:**
When spawning Haiku agents, you MUST give them TWO literal paths:
1. **SOURCE_DIR** (where to READ code) - the `origin/` symlink
2. **DOCS_DIR** (where to WRITE docs) - the parent directory, NOT inside origin/

⚠️ **THE BUG**: If you only give agents `origin/` path, they cd into it and write there → files end up in WRONG repo!

**FIX**: Always give BOTH paths as LITERAL absolute values (no variables!):

Example: ROOT=/home/user/ghq/.../my-oracle, learning acme-corp/cool-library, TODAY=2026-02-04, TIME=1349:
```
READ from:  .../ψ/learn/acme-corp/cool-library/origin/
WRITE to:   .../ψ/learn/acme-corp/cool-library/2026-02-04/1349_[FILENAME].md
```

Tell each agent: "Read from [SOURCE_DIR]. Write to [DOCS_DIR]/[TIME]_[FILENAME].md"

### If URL (http* or owner/repo format)

**Clone, create docs dir, symlink origin, update manifest:**
```bash
# Replace [URL] with actual URL
URL="[URL]"
ROOT="$(pwd)"  # CRITICAL: Save current directory!
ghq get -u "$URL" && \
  GHQ_ROOT=$(ghq root) && \
  OWNER=$(echo "$URL" | sed -E 's|.*github.com/([^/]+)/.*|\1|') && \
  REPO=$(echo "$URL" | sed -E 's|.*/([^/]+)(\.git)?$|\1|') && \
  mkdir -p "$ROOT/ψ/learn/$OWNER/$REPO" && \
  ln -sf "$GHQ_ROOT/github.com/$OWNER/$REPO" "$ROOT/ψ/learn/$OWNER/$REPO/origin" && \
  echo "$OWNER/$REPO" >> "$ROOT/ψ/learn/.origins" && \
  sort -u -o "$ROOT/ψ/learn/.origins" "$ROOT/ψ/learn/.origins" && \
  echo "✓ Ready: $ROOT/ψ/learn/$OWNER/$REPO/origin → source"
```

**Verify:**
```bash
ls -la "$ROOT/ψ/learn/$OWNER/$REPO/"
```

> **Note**: Grep tool doesn't follow symlinks. Use: `rg -L "pattern" ψ/learn/owner/repo/origin/`

### Then resolve path:
```bash
# Find by name (searches origin symlinks)
find ψ/learn -name "origin" -type l | xargs -I{} dirname {} | grep -i "$INPUT" | head -1
```

## Scope

**For external repos**: Clone with script first, then explore via `origin/`
**For local projects** (in `specs/`, `ψ/lib/`): Read directly

## Step 1: Detect Mode & Calculate Paths

Check arguments for `--fast` or `--deep`:
- `--fast` → Single overview agent
- `--deep` → 5 parallel agents
- (neither) → 3 parallel agents (default)

**Calculate ACTUAL paths (replace variables with real values):**
```
TODAY = YYYY-MM-DD (e.g., 2026-02-04)
TIME = HHMM (e.g., 1349)
REPO_DIR = [ROOT]/ψ/learn/[OWNER]/[REPO]/
DOCS_DIR = [ROOT]/ψ/learn/[OWNER]/[REPO]/[TODAY]/   ← date folder
SOURCE_DIR = [ROOT]/ψ/learn/[OWNER]/[REPO]/origin/  ← symlink
FILE_PREFIX = [TIME]_                               ← time prefix for files

Example:
- ROOT = /home/user/ghq/github.com/my-org/my-oracle
- OWNER = acme-corp
- REPO = cool-library
- TODAY = 2026-02-04, TIME = 1349
- DOCS_DIR = .../ψ/learn/acme-corp/cool-library/2026-02-04/
- Files: 1349_ARCHITECTURE.md, 1349_CODE-SNIPPETS.md, etc.
```

**⚠️ CRITICAL: Create symlink AND date folder FIRST, then spawn agents!**

1. Run the clone + symlink script in Step 0 FIRST
2. Capture TIME: `date +%H%M` (e.g., 1349)
3. Create the date folder: `mkdir -p "$DOCS_DIR"`
4. Capture DOCS_DIR, SOURCE_DIR, and TIME as literal values
5. THEN spawn agents with paths including TIME prefix

**Multiple runs same day?** Each run gets unique TIME prefix → no overwrites.

---

## Mode: --fast (1 agent)

### Single Agent: Quick Overview

**Prompt the agent with (use LITERAL paths, not variables!):**
```
You are exploring a codebase.

READ source code from: [SOURCE_DIR]
WRITE your output to:   [DOCS_DIR]/[TIME]_OVERVIEW.md

⚠️ IMPORTANT: Write to DOCS_DIR (the date folder), NOT inside origin/!

Analyze:
- What is this project? (1 sentence)
- Key files to look at
- How to use it (install + basic example)
- Notable patterns or tech
```

**Skip to Step 2** after agent completes.

---

## Mode: Default (3 agents)

Launch 3 agents in parallel. Each prompt must include (use LITERAL paths!):
```
READ source code from: [SOURCE_DIR]
WRITE your output to:   [DOCS_DIR]/[TIME]_[filename].md

⚠️ IMPORTANT: Write to DOCS_DIR (the date folder), NOT inside origin/!
```

### Agent 1: Architecture Explorer → `[TIME]_ARCHITECTURE.md`
- Directory structure
- Entry points
- Core abstractions
- Dependencies

### Agent 2: Code Snippets Collector → `[TIME]_CODE-SNIPPETS.md`
- Main entry point code
- Core implementations
- Interesting patterns

### Agent 3: Quick Reference Builder → `[TIME]_QUICK-REFERENCE.md`
- What it does
- Installation
- Key features
- Usage patterns

**Skip to Step 2** after all agents complete.

---

## Mode: --deep (5 agents)

Launch 5 agents in parallel. Each prompt must include (use LITERAL paths!):
```
READ source code from: [SOURCE_DIR]
WRITE your output to:   [DOCS_DIR]/[TIME]_[filename].md

⚠️ IMPORTANT: Write to DOCS_DIR (the date folder), NOT inside origin/!
```

### Agent 1: Architecture Explorer → `[TIME]_ARCHITECTURE.md`
- Directory structure & organization philosophy
- Entry points (all of them)
- Core abstractions & their relationships
- Dependencies (direct + transitive patterns)

### Agent 2: Code Snippets Collector → `[TIME]_CODE-SNIPPETS.md`
- Main entry point code
- Core implementations with context
- Interesting patterns & idioms
- Error handling examples

### Agent 3: Quick Reference Builder → `[TIME]_QUICK-REFERENCE.md`
- What it does (comprehensive)
- Installation (all methods)
- Key features with examples
- Configuration options

### Agent 4: Testing & Quality Patterns → `[TIME]_TESTING.md`
- Test structure and conventions
- Test utilities and helpers
- Mocking patterns
- Coverage approach

### Agent 5: API & Integration Surface → `[TIME]_API-SURFACE.md`
- Public API documentation
- Extension points / hooks
- Integration patterns
- Plugin/middleware architecture

**Skip to Step 2** after all agents complete.

## Step 2: Create/Update Hub File ([REPO].md)

```markdown
# [REPO] Learning Index

## Source
- **Origin**: ./origin/
- **GitHub**: https://github.com/$OWNER/$REPO

## Explorations

### [TODAY] [TIME] ([mode])
- [[YYYY-MM-DD/HHMM_ARCHITECTURE|Architecture]]
- [[YYYY-MM-DD/HHMM_CODE-SNIPPETS|Code Snippets]]
- [[YYYY-MM-DD/HHMM_QUICK-REFERENCE|Quick Reference]]
- [[YYYY-MM-DD/HHMM_TESTING|Testing]]        <!-- --deep only -->
- [[YYYY-MM-DD/HHMM_API-SURFACE|API Surface]] <!-- --deep only -->

**Key insights**: [2-3 things learned]

### [TODAY] [EARLIER-TIME] ([mode])
...
```

## Output Summary

### --fast mode
```markdown
## 📚 Quick Learn: [REPO]

**Mode**: fast (1 agent)
**Location**: ψ/learn/$OWNER/$REPO/[TODAY]/[TIME]_*.md

| File | Description |
|------|-------------|
| [REPO].md | Hub (links all sessions) |
| [TODAY]/[TIME]_OVERVIEW.md | Quick overview |
```

### Default mode
```markdown
## 📚 Learning Complete: [REPO]

**Mode**: default (3 agents)
**Location**: ψ/learn/$OWNER/$REPO/[TODAY]/[TIME]_*.md

| File | Description |
|------|-------------|
| [REPO].md | Hub (links all sessions) |
| [TODAY]/[TIME]_ARCHITECTURE.md | Structure |
| [TODAY]/[TIME]_CODE-SNIPPETS.md | Code examples |
| [TODAY]/[TIME]_QUICK-REFERENCE.md | Usage guide |

**Key Insights**: [2-3 things learned]
```

### --deep mode
```markdown
## 📚 Deep Learning Complete: [REPO]

**Mode**: deep (5 agents)
**Location**: ψ/learn/$OWNER/$REPO/[TODAY]/[TIME]_*.md

| File | Description |
|------|-------------|
| [REPO].md | Hub (links all sessions) |
| [TODAY]/[TIME]_ARCHITECTURE.md | Structure & design |
| [TODAY]/[TIME]_CODE-SNIPPETS.md | Code examples |
| [TODAY]/[TIME]_QUICK-REFERENCE.md | Usage guide |
| [TODAY]/[TIME]_TESTING.md | Test patterns |
| [TODAY]/[TIME]_API-SURFACE.md | Public API |

**Key Insights**: [3-5 things learned]
```

## .gitignore Pattern

For Oracles that want to commit docs but ignore symlinks:

```gitignore
# Ignore origin symlinks only (source lives in ghq)
# Note: no trailing slash - origin is a symlink, not a directory
ψ/learn/**/origin
```

**After running /learn**, check your repo's `.gitignore` has these patterns so docs are committed but symlinks are ignored.

## Notes

- `--fast`: 1 agent, quick scan for "what is this?"
- Default: 3 agents in parallel, good balance
- `--deep`: 5 agents, comprehensive for complex repos
- Haiku for exploration = cost effective
- Main reviews = quality gate
- `origin/` structure allows easy offload
- `.origins` manifest enables `--init` restore
