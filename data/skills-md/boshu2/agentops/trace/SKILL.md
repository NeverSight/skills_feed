---
name: trace
description: 'Trace design decisions and concepts through session history, handoffs, and git. Triggers: "trace decision", "how did we decide", "where did this come from", "design provenance", "decision history".'
dependencies:
  - provenance # alternative - for artifact lineage
---

# Trace Skill

> **Quick Ref:** Trace design decisions through CASS sessions, handoffs, git, and artifacts. Output: `.agents/research/YYYY-MM-DD-trace-*.md`

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

## When to Use

- Trace HOW architectural decisions evolved
- Find WHEN a concept was introduced
- Understand WHY something was designed a certain way
- Build provenance chain for design decisions

For knowledge artifact lineage (learnings, patterns, tiers), use `/provenance` instead.

## Execution Steps

Given `/trace <concept>`:

### Step 1: Classify Target Type

Determine what kind of provenance to trace:

```
IF target is a file path (contains "/" or "."):
  → Use /provenance (artifact lineage)

IF target is a git ref (sha, branch, tag):
  → Use git-based tracing (Step 2b)

ELSE (keyword/concept):
  → Use design decision tracing (Step 2a)
```

### Step 2a: Design Decision Tracing (Concepts)

**Launch parallel search agents using Task tool:**

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  model: "haiku"
  description: "CASS search: <concept>"
  prompt: |
    Search session transcripts for: <concept>

    Run this command:
    cass search "<concept>" --json --limit 10

    Parse the JSON output and extract:
    - Session dates (created_at field, convert from Unix ms)
    - Session paths (source_path field)
    - Agents used (agent field)
    - Relevance scores (score field)
    - Key snippets (snippet/content fields)

    Return a structured list sorted by date (oldest first).
```

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  model: "haiku"
  description: "Handoff search: <concept>"
  prompt: |
    Search handoff documents for: <concept>

    1. List handoff files:
       ls -la .agents/handoff/*.md 2>/dev/null

    2. Search for concept mentions:
       grep -l "<concept>" .agents/handoff/*.md 2>/dev/null

    3. For each matching file, extract:
       - File date (from filename YYYY-MM-DD)
       - Context around the mention (grep -B5 -A5)
       - Related decisions or questions

    Return a structured list sorted by date.
```

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  model: "haiku"
  description: "Git search: <concept>"
  prompt: |
    Search git history for: <concept>

    1. Search commit messages:
       git log --oneline --grep="<concept>" | head -20

    2. For interesting commits, get details:
       git show --stat <commit-sha>

    3. Extract:
       - Commit dates
       - Commit messages
       - Files changed
       - Authors

    Return a structured list sorted by date.
```

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  model: "haiku"
  description: "Research search: <concept>"
  prompt: |
    Search research and learning artifacts for: <concept>

    1. Search research docs:
       grep -l "<concept>" .agents/research/*.md 2>/dev/null

    2. Search learnings:
       grep -l "<concept>" .agents/learnings/*.md 2>/dev/null

    3. Search patterns:
       grep -l "<concept>" .agents/patterns/*.md 2>/dev/null

    4. For each match, extract:
       - File date (from filename or modification time)
       - Context around the mention
       - Related concepts

    Return a structured list sorted by date.
```

**Wait for all 4 agents to complete.**

### Step 2b: Git-Based Tracing (Commits/Refs)

For git refs, trace the commit history:

```bash
# Get commit details
git show --stat <ref>

# Get commit ancestry
git log --oneline --ancestry-path <ref>..HEAD | head -20

# Find related commits
git log --oneline --all --grep="$(git log -1 --format=%s <ref> | head -c 50)" | head -10
```

### Step 3: Build Timeline

**Merge results from all sources into a single timeline:**

```markdown
| Date | Source | Event | Evidence |
|------|--------|-------|----------|
| YYYY-MM-DD | CASS | First mention in session | session-id, snippet |
| YYYY-MM-DD | Handoff | Decision recorded | handoff-file, context |
| YYYY-MM-DD | Git | Implementation committed | commit-sha, message |
| YYYY-MM-DD | Research | Documented in research | research-file |
```

**Deduplication rules:**
- Same content within 24 hours = single event (note multiple sources)
- Same session ID = single event
- Preserve ALL sources as evidence

**Sorting:**
- Chronological order (oldest first)
- Show evolution of the concept over time

### Step 4: Extract Key Decisions

For each event in timeline, identify:
- **What changed:** The decision or evolution
- **Why:** Reasoning if available
- **Who:** Session/author/commit author
- **Evidence:** Link to source (session path, file, commit)

### Step 5: Write Trace Report

**Write to:** `.agents/research/YYYY-MM-DD-trace-<concept-slug>.md`

```markdown
# Trace: <Concept>

**Date:** YYYY-MM-DD
**Query:** <original concept>
**Sources searched:** CASS, Handoffs, Git, Research

## Summary

<2-3 sentence overview of how the concept evolved>

## Timeline

| Date | Source | Event | Evidence |
|------|--------|-------|----------|
| ... | ... | ... | ... |

## Key Decisions

### Decision 1: <title>
- **Date:** YYYY-MM-DD
- **Source:** <CASS session / Handoff / Git commit>
- **What:** <what was decided>
- **Why:** <reasoning if known>
- **Evidence:** <link/path>

### Decision 2: <title>
...

## Evolution Summary

<How the concept changed over time, key inflection points>

## Current State

<Where the concept stands now based on most recent evidence>

## Related Concepts

- <related concept 1> - see `/trace <concept1>`
- <related concept 2> - see `/trace <concept2>`

## Sources

### CASS Sessions
| Date | Session Path | Score |
|------|--------------|-------|
| ... | ... | ... |

### Handoff Documents
| Date | File | Context |
|------|------|---------|
| ... | ... | ... |

### Git Commits
| Date | SHA | Message |
|------|-----|---------|
| ... | ... | ... |

### Research/Learnings
| Date | File |
|------|------|
| ... | ... |
```

### Step 6: Report to User

Tell the user:
1. Concept traced successfully
2. Timeline of evolution (key dates)
3. Most significant decisions
4. Location of trace report
5. Related concepts to explore

## Handling Edge Cases

### No CASS Results
```
IF cass search returns 0 results:
  - Log: "No session transcripts mention '<concept>'"
  - Continue with other sources
  - Note in report: "Concept not found in session history"
```

### No Handoff Documents
```
IF .agents/handoff/ doesn't exist OR no matches:
  - Log: "No handoff documents mention '<concept>'"
  - Continue with other sources
  - Note in report: "Concept not documented in handoffs"
```

### Ambiguous Concept (Too Many Results)
```
IF CASS returns >20 results:
  - Show top 10 by score
  - Ask user: "Many sessions mention this. Want to narrow by date range or workspace?"
  - Suggest related but more specific concepts
```

### All Sources Empty
```
IF all 4 searches return nothing:
  - Report: "No provenance found for '<concept>'"
  - Suggest: "Try related terms: <suggestions>"
  - Ask: "Is this concept documented somewhere else?"
```

## Key Rules

- **Search ALL sources** - CASS, handoffs, git, research
- **Build timeline** - chronological evolution is the goal
- **Cite evidence** - every claim needs a source
- **Handle gaps gracefully** - not all concepts are in all sources
- **Write report** - trace must produce `.agents/research/` artifact

## Relationship to /provenance

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| `/provenance` | Artifact lineage | File path | Tier/promotion history |
| `/trace` | Design decisions | Concept/keyword | Timeline of evolution |

Use `/provenance` for: "Where did this learning come from?"
Use `/trace` for: "How did we decide on this architecture?"

## Examples

```bash
# Trace a design decision
/trace "three-level architecture"

# Trace a role/concept
/trace "Chiron"

# Trace a pattern
/trace "brownian ratchet"

# Trace a feature
/trace "parallel wave execution"
```
