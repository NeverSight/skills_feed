---
name: shareful-mine
description: Mines past Claude Code conversations for the best shareable coding solutions using claude-code-search (ccs). Uses quality signals -- breakthrough markers, difficulty indicators, and community value scoring -- to surface high-recall content from conversation history. Use when the user wants to "mine conversations for shares", "populate my shares repo", "recall my best work", "find my best solved problems", or "solve the cold start problem".
---

# Shareful Mine

Mine past Claude Code conversations for the best problems worth sharing on shareful.ai. Uses quality signal detection -- breakthrough moments, difficulty tiers, and community value scoring -- to surface your highest-value solved problems. This solves the cold start problem -- every developer already solves real problems daily, and the best solutions are sitting in conversation history waiting to be shared.

## Prerequisites

Install claude-code-search globally:

```bash
npm install -g claude-code-search
```

Verify installation:

```bash
ccs --help
```

The user must also have a shares repo set up. If not, run `npx shareful-ai init` first.

## Reference Files

| File | Read When |
|------|-----------|
| [references/ccs-commands.md](references/ccs-commands.md) | Looking up ccs CLI syntax, flags, or output format |
| [references/search-strategies.md](references/search-strategies.md) | Choosing what to search for and evaluating candidates |
| [references/recall-scoring.md](references/recall-scoring.md) | Scoring candidates by quality signals (breakthrough, difficulty, community value) |

## Mining Workflow

Copy this checklist to track progress:

```text
- [ ] Step 1: Check existing shares to avoid duplicates
- [ ] Step 2: Run discovery searches with ccs
- [ ] Step 3: Score and rank candidates
- [ ] Step 4: Create SHARE.md files
- [ ] Step 5: Validate with npx shareful-ai check
```

### Step 1: Check Existing Shares

Before mining, list what already exists to avoid duplicates:

```bash
ls shares/
```

### Step 2: Run Discovery Searches

Run multiple targeted searches to surface problems from conversation history. Use JSON output for programmatic processing:

```bash
# Error-focused searches
ccs -s "error" -j -n 30
ccs -s "fix" -j -n 30
ccs -s "TypeError" -j -n 20
ccs -s "cannot find" -j -n 20
ccs -s "failed" -j -n 20

# Framework-specific searches
ccs -s "nextjs" -j -n 20
ccs -s "tailwind" -j -n 20
ccs -s "prisma" -j -n 20
ccs -s "react" -j -n 20
ccs -s "typescript" -j -n 20
```

Read [references/search-strategies.md](references/search-strategies.md) for the full list of recommended searches and how to evaluate results.

Beyond error and framework searches, run quality signal searches to find breakthrough moments and hard problems. These often surface the highest-value share candidates:

```bash
# Breakthrough markers -- user prompts after solving a hard problem
ccs -s "finally working" -j -n 20
ccs -s "that fixed it" -j -n 20
ccs -s "that worked" -j -n 20

# Difficulty indicators -- prompts suggesting deep debugging
ccs -s "still not working" -j -n 20
ccs -s "tried everything" -j -n 20
ccs -s "hours" -j -n 20
```

Read [references/recall-scoring.md](references/recall-scoring.md) for the complete list of quality signal searches and how to score candidates.

### Step 3: Score and Rank Candidates

Apply the recall scoring system to rank candidates. Each candidate is scored on three dimensions:

1. **Breakthrough signal** (0-2 pts) -- Did the user's prompts indicate a hard-won solution?
2. **Problem quality** (0-3 pts) -- Is the problem specific, reproducible, and well-described?
3. **Community value** (0-3 pts) -- Would other developers encounter this and search for it?

Total score ranges from 0-8. Prioritize candidates scoring 5+ and skip anything below 3. Read [references/recall-scoring.md](references/recall-scoring.md) for detailed scoring rubrics, difficulty tiers, and examples.

Discard prompts that are:
- Generic requests ("review my code", "test this", "explain this")
- Project-specific business logic with no general applicability
- Simple typos or one-character fixes
- Incomplete -- the problem was described but never resolved

### Step 4: Create SHARE.md Files

For each candidate, create a share following the `shareful-create` workflow. Write directly to `shares/<slug>/SHARE.md` with complete frontmatter and all four required sections.

Each share needs:
- YAML frontmatter (title, slug, tags, problem, solution_type, created, environment)
- `## Problem` -- the error message and broken code from the conversation
- `## Solution` -- the fix that resolved it
- `## Why It Works` -- explanation of the root cause
- `## Context` -- versions, gotchas, related tools

When creating multiple shares, parallelize by assigning batches to subagents. Each subagent writes to separate directories so there are no file conflicts.

### Step 5: Validate

Run the shareful checker to validate all shares:

```bash
npx shareful-ai check
```

All shares must pass validation before committing. Fix any errors flagged by the checker.

## Candidate Evaluation Criteria

| Signal | Good Candidate | Bad Candidate |
|--------|---------------|---------------|
| Error specificity | `TypeError: Cannot read properties of undefined` | "something broke" |
| Technology scope | Framework/library issue any user could hit | App-specific business logic |
| Fix clarity | Clear code change that resolves the error | Vague "try restarting" |
| Frequency | Common framework gotcha or migration issue | One-off environment quirk |
| Searchability | Error message is Google-able | No distinctive error string |
| Breakthrough signal | "finally working after 3 hours" | "thanks" (generic) |
| Problem difficulty | Multi-step debugging, config interaction | One-liner typo fix |

## Anti-patterns

- **Mining private/sensitive content** -- never include API keys, credentials, internal URLs, or proprietary business logic in shares
- **Sharing unresolved problems** -- only share problems that were actually fixed
- **Over-mining** -- focus on quality over quantity; 10 great shares beat 50 mediocre ones
- **Duplicating existing shares** -- always check the repo first
- **Vague problems** -- if you cannot write a specific error message for the Problem section, skip it
- **Mining only easy wins** -- prioritize hard problems (Tier 3-4) over trivial fixes; shares for simple issues add noise, not value

## Related Skills

- `shareful-create` for the detailed SHARE.md writing workflow and validation
- `shareful-search` for checking if a solution already exists on shareful.ai
- `shareful-init` for setting up a shares repository
