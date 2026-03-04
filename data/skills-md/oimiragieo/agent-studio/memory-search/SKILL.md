---
name: memory-search
description: Semantic search over global agent memory. Use to retrieve previously learned patterns, decisions, gotchas, and workarounds. Prevents stale-context errors across long sessions and multi-agent pipelines.
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash]
agents:
  - developer
  - architect
  - planner
  - qa
  - code-reviewer
  - technical-writer
  - security-architect
  - devops
  - researcher
category: memory
tags: [memory, search, semantic, context, rag, recall]

verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
best_practices:
  - Run memory-search at the start of any non-trivial task
  - Use focused queries, not broad ones
  - Treat results as pointers to canonical sources, not ground truth
  - Pair high-similarity results with explicit file reads for critical decisions
error_handling: graceful
streaming: supported
---

# Memory Search

<identity>
Memory Search is the live recall layer for all agents in the ecosystem. It performs semantic search over the global memory corpus (learnings, decisions, issues, gotchas, patterns) using vector similarity. Every agent must use this skill to avoid working from stale or contradictory context — especially in long sessions where in-conversation memory has been compressed or reset.
</identity>

<capabilities>
- Semantic similarity search over all memory files (learnings.md, decisions.md, issues.md, gotchas.json, patterns.json)
- Returns up to 10 results ranked by similarity score
- Output includes: source file, similarity percentage, and 200-character content preview
- Supports natural language queries — no keyword matching required
- Cross-agent knowledge retrieval: surfaces knowledge from previous agents in the same or prior sessions
</capabilities>

<instructions>
<execution_process>

### Step 1: Formulate a Focused Query

Identify the specific knowledge gap before invoking. Good queries target a concrete decision, pattern, or error — not a broad topic.

**Good queries:**

- `"JWT refresh token rotation pattern"`
- `"Windows path normalization in hooks"`
- `"BM25 index rebuild performance"`
- `"agent spawning without task_id error"`

**Bad queries (too broad):**

- `"authentication"` — too generic, returns noise
- `"everything about routing"` — unfocused
- `"what have we done before"` — meaningless for semantic search

### Step 2: Run the Search

Invoke via the `Bash` tool:

```bash
node .claude/lib/memory/memory-search.cjs "your focused search query"
```

**Full invocation:**

```bash
node .claude/lib/memory/memory-search.cjs "JWT refresh token rotation pattern"
```

### Step 3: Parse the Output

The output format is:

```
Found N results for: "<query>"

[<source-file>] Similarity: XX.X%
<200-character content preview>...

[<source-file>] Similarity: YY.Y%
<200-character content preview>...
```

**Example real output:**

```
Found 3 results for: "JWT refresh token rotation pattern"

[learnings.md] Similarity: 87.3%
JWT refresh tokens must be stored in httpOnly cookies to prevent XSS. See ADR-045 for detailed rationale and trade-offs vs localStorage approach...

[decisions.md] Similarity: 74.1%
ADR-045: JWT over sessions chosen for stateless architecture. Refresh token rotation every 15 minutes. Invalidate on logout via token blocklist...

[issues.md] Similarity: 61.2%
Known issue: JWT expiry not propagated to frontend — workaround in auth.middleware.ts line 47 until ADR-045 Phase 2 is implemented...
```

### Step 4: Interpret Similarity Scores

| Similarity | Interpretation                                      | Action                                         |
| ---------- | --------------------------------------------------- | ---------------------------------------------- |
| >80%       | Highly relevant — directly matches the query        | Read the full source file for complete context |
| 60–80%     | Likely relevant — related topic or adjacent pattern | Skim and use if applicable                     |
| 40–60%     | Possibly relevant — tangentially related            | Use judgment, may be noise                     |
| <40%       | Probably not relevant                               | Discard unless nothing better exists           |

### Step 5: Follow Up on High-Similarity Results

For results with similarity >60%, read the full source file to get untruncated content:

```bash
# Results showed [decisions.md] Similarity: 87.3%
# Follow up with:
Read({ file_path: '.claude/context/memory/decisions.md' })
```

Or search for the specific ADR/pattern by keyword:

```bash
node .claude/lib/memory/memory-search.cjs "ADR-045 JWT"
```

### Step 6: Handle Zero Results

If `Found 0 results`, try:

1. **Rephrase the query** using synonyms or the actual error message text
2. **Broaden slightly** — e.g., `"JWT authentication"` instead of `"JWT RS256 key rotation"`
3. **Check memory files directly** if the topic is recent and may not yet be indexed

Zero results means the knowledge is either not yet documented or the query was too specific.

### Step 7: Apply or Document Findings

- **If result confirms known approach:** proceed with confidence; cite the source in your reasoning.
- **If result reveals a better approach:** update your plan to align with the documented pattern.
- **If result reveals a known issue/workaround:** apply the workaround immediately rather than discovering it yourself.
- **If nothing useful found:** continue with your best judgment; document your decision afterward to Memory Protocol.

</execution_process>

<best_practices>

1. **Run early, not late**: Memory search at the START of a task prevents wasted effort. Running it after you have already made decisions is too late to benefit.

2. **One query per knowledge gap**: Don't batch all your unknowns into one query. Run targeted queries for each specific gap.

3. **Use the actual error message as the query**: If you hit an error, search for the error message text verbatim — it often finds a documented workaround.

4. **Results are pointers, not canonical sources**: Always follow up by reading the full source file when similarity is >70%. The 200-char preview is not the complete record.

5. **After a session gap or context compression**: Always run memory-search to re-establish current state before proceeding. Context may have been lost.

6. **Cross-agent knowledge sync**: Before duplicating an analysis another agent might have done, search memory. The result may already be documented.

</best_practices>
</instructions>

<examples>
<usage_example title="Session start — re-establish context">

At the start of a long task or after a context compression event:

```bash
# What are the current known issues in this area?
node .claude/lib/memory/memory-search.cjs "hook execution errors"

# What patterns have been established for this domain?
node .claude/lib/memory/memory-search.cjs "routing table keyword patterns"

# Any decisions I should be aware of?
node .claude/lib/memory/memory-search.cjs "agent model selection ADR"
```

</usage_example>

<usage_example title="Debugging — check for known workarounds">

When stuck on an error:

```bash
# Search for the exact error message
node .claude/lib/memory/memory-search.cjs "Unable to locate module.exports insertion point"

# Or describe the symptom
node .claude/lib/memory/memory-search.cjs "routing table update fails silently"
```

If a result appears with >70% similarity, the error has been seen before and may have a documented fix.
</usage_example>

<usage_example title="Before making an architectural decision">

Before choosing between two approaches:

```bash
# What was decided previously about this tradeoff?
node .claude/lib/memory/memory-search.cjs "ESM vs CJS module format decision"

# Are there ADRs for this pattern?
node .claude/lib/memory/memory-search.cjs "async hook pattern ADR"
```

If a relevant ADR is found, follow it rather than re-litigating the decision.
</usage_example>

<usage_example title="Cross-agent knowledge retrieval">

When you need to know what another agent discovered:

```bash
# What did the reflection agent find recently?
node .claude/lib/memory/memory-search.cjs "reflection agent findings skills gap"

# What did the security audit reveal?
node .claude/lib/memory/memory-search.cjs "security audit prompt injection findings"
```

</usage_example>
</examples>

## Iron Laws

1. **ALWAYS run memory-search before assuming no prior context exists.** Never claim "there's no documented pattern for this" without first running a targeted search.

2. **NEVER use memory-search results as canonical ground truth.** They are summaries and previews. Always read the full source for decisions with material consequences.

3. **NEVER skip memory-search because "I already know about this."** Stale in-session assumptions are the primary cause of inconsistent multi-agent behavior.

4. **ALWAYS run multiple targeted queries, not one broad one.** A single broad query misses specific matches. Two or three focused queries are more effective.

5. **NEVER run memory-search with a query longer than ~10 words.** Over-specified queries degrade similarity matching. Extract the key concept.

## Anti-Patterns

| Anti-Pattern                               | Why It Fails                                                | Correct Approach                              |
| ------------------------------------------ | ----------------------------------------------------------- | --------------------------------------------- |
| `"everything about auth"` broad query      | Too generic — returns unrelated noise                       | `"JWT refresh token rotation"`                |
| Skipping search because "context is fresh" | In-session context is NOT the same as memory                | Always search at task start                   |
| Treating 200-char preview as full record   | Preview truncates at 200 chars — critical detail may be cut | Follow up with `Read` on the source file      |
| Running search AFTER making the decision   | Memory lookup must happen before your design choice         | Search first, decide second                   |
| Single query for multiple unknowns         | One query can't cover multiple semantic dimensions          | Run one query per knowledge gap               |
| Ignoring <60% results entirely             | Sometimes tangential info is still actionable               | Skim low-similarity results before discarding |

## Error Handling

| Error                                                             | Cause                                          | Resolution                                                                            |
| ----------------------------------------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------- |
| `Usage: node .claude/lib/memory/memory-search.cjs "search query"` | Query argument missing                         | Always pass a quoted query string                                                     |
| `Search failed: <error message>`                                  | Memory manager unavailable or index not built  | Check `.claude/lib/memory/memory-manager.cjs` and ensure memory system is initialized |
| `Found 0 results`                                                 | Query too specific or topic not yet documented | Rephrase query; fall back to direct file search                                       |
| Very slow response (>3s)                                          | Vector similarity computation on cold index    | Expected on first call; subsequent calls are faster                                   |

## Integration Patterns

### Mandatory Pre-Task Pattern (All Agents)

Every agent should run memory-search at task start for any non-trivial work:

```bash
# Pattern: topic-scoped recall before starting
node .claude/lib/memory/memory-search.cjs "known patterns for <your task domain>"
node .claude/lib/memory/memory-search.cjs "known issues in <your task area>"
```

### Error Recovery Pattern

When any tool or command fails unexpectedly:

```bash
# Paste the error message directly as the query
node .claude/lib/memory/memory-search.cjs "<exact error text>"
```

### Decision Gate Pattern

Before any architectural decision:

```bash
# Check for existing ADRs on this topic
node .claude/lib/memory/memory-search.cjs "ADR <decision topic>"
```

### Cross-Session Continuity Pattern

At the start of any continued session (especially after context compression):

```bash
node .claude/lib/memory/memory-search.cjs "recent decisions <project area>"
node .claude/lib/memory/memory-search.cjs "current known issues"
node .claude/lib/memory/memory-search.cjs "last session learnings"
```

## When to Use

| Trigger                                         | Query Strategy                              | Expected Benefit                         |
| ----------------------------------------------- | ------------------------------------------- | ---------------------------------------- |
| **Long-running session** — context may be stale | `"<domain> recent decisions"`               | Re-sync with documented state            |
| **New error encountered**                       | `"<exact error message>"`                   | Find documented workaround               |
| **Before architectural decision**               | `"ADR <topic>"` or `"<decision> trade-off"` | Avoid re-litigating settled decisions    |
| **After context compression**                   | `"<current task domain>"`                   | Restore working context                  |
| **Cross-agent handoff**                         | `"<previous agent task> findings"`          | Continue from where other agent left off |
| **Before writing a new pattern**                | `"<pattern name> existing"`                 | Avoid duplicating documented guidance    |

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
node .claude/lib/memory/memory-search.cjs "memory-search usage patterns"
```

**After completing:**

- New search pattern discovered → `.claude/context/memory/learnings.md`
- Memory index issue found → `.claude/context/memory/issues.md`
- Decision about when to use memory-search → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen. This skill exists to recover from exactly that situation.
