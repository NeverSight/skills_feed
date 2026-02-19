---
name: artifact-integrator
description: Deep integration analysis for newly created artifacts
version: 1.0.0
category: workflow
agents:
  - architect
  - planner
  - developer
tools:
  - Read
  - Write
  - Edit
  - TaskCreate
  - TaskList
  - TaskUpdate
  - Bash
verified: false
lastVerifiedAt: 2026-02-19T05:29:09.098Z
---

# Artifact Integrator

## Purpose

Analyze newly created or modified artifacts for integration gaps and propose follow-up tasks to ensure full ecosystem integration.

## When to Use

- After any artifact creator skill completes
- When Router Step 0.5 detects unprocessed integration queue entries
- When manually checking integration health
- When reviewing artifacts for completeness

## Protocol

### Step 1: Read Integration Queue

Read `.claude/context/runtime/integration-queue.jsonl`
Filter for entries with `"processed": false`
If no unprocessed entries, check if `artifactId` argument was provided for direct analysis.

### Step 2: Analyze Each Artifact

For each unprocessed entry (or the directly specified artifact):

1. Load the artifact graph: `require('.claude/lib/workflow/artifact-graph.cjs')`
2. Load impact analyzer: `require('.claude/lib/workflow/integration-impact.cjs')`
3. Call `analyzeImpact({ artifactId, changeType, graphPath })`
4. Review the `missingIntegrations` and `proposedTasks`

### Step 3: Generate Integration Plan

For each artifact with missing integrations:

**Must-Have (P1) — Create tasks immediately:**

- Missing catalog entry → TaskCreate: "Add {name} to {catalog}"
- Missing agent assignment → TaskCreate: "Assign {name} to relevant agent"
- Missing routing entry → TaskCreate: "Update routing for {name}"
- Missing hook registration → TaskCreate: "Register {name} in settings.json"

**Should-Have (P2) — Create tasks with lower priority:**

- Missing documentation → TaskCreate: "Document {name} in {doc}"
- Missing enforcement hook → TaskCreate: "Create enforcement for {name}"
- Missing tests → TaskCreate: "Write tests for {name}"

**Nice-to-Have — Note but don't create tasks:**

- Missing templates, optional docs

### Step 3.1: Companion Matrix Analysis (Interwoven Creator Ecosystem)

For each artifact analyzed, run companion matrix validation to identify missing ecosystem companions:

**Analysis:**

1. Use `companion-check.cjs` from `.claude/lib/creators/companion-check.cjs`
2. Call `checkCompanions(artifactType, artifactName)` to get companion matrix
3. Parse the companion checklist into categories:
   - **Required companions** (must-have for artifact completeness)
   - **Recommended companions** (should-have for best practices)
   - **Optional companions** (nice-to-have for full integration)

**Task Generation:**

- For each **missing required companion** → Create P1 task: "Create {companion-type}:{companion-name} for {artifact-name}"
- For each **missing recommended companion** → Create P2 task: "Consider creating {companion-type}:{companion-name} for {artifact-name}"
- For **missing optional companions** → Note in report but don't create tasks

**Safety Limits (SEC-ICE-002):**

- **Max auto-spawned tasks per artifact**: 3 (prevent cascade creation)
- **Max total companion tasks per integration run**: 10 (prevent batch explosion)
- If limits exceeded, queue remaining companions for manual review with warning in report

**Example:**

```markdown
### Companion Matrix Analysis: skill:rate-limiter

**Required Companions (MISSING):**

- [ ] hook:rate-limit-validator (validates rate limit headers) — **TASK CREATED** (P1)
- [ ] schema:rate-limit-config (validates configuration) — **TASK CREATED** (P1)

**Recommended Companions (MISSING):**

- [ ] template:rate-limit-pattern (template for rate limiting implementations) — **TASK CREATED** (P2)

**Optional Companions (MISSING):**

- [ ] workflow:rate-limit-setup (onboarding workflow) — noted for future consideration

**Safety Check:**

- Auto-spawned tasks: 3 (within limit of 3 per artifact)
- Total companion tasks this run: 8 (within limit of 10)
```

**Integration with Companion Check:**

- Companion matrix data sourced from `ecosystem-impact-graph.json`
- Uses same `companion-check.cjs` library invoked by creator skills at Step 0.5
- Ensures bidirectional consistency: creators check companions at creation, integrator validates companions post-creation

### Step 3.5: Backward Propagation Processing (ADR-100 Phase 3.1-3.3)

When processing backward propagation signals from code-reviewer or architect:

**Detection:**

- Queue entries with `changeType: "backward-propagation"`
- Review findings containing `BACKWARD_PROPAGATION` section
- Pattern reports indicating systemic duplication

**Validation:**

1. **Verify the pattern exists** (check mentioned files/components)
   - Read each affected file to confirm pattern duplication
   - Count actual instances (not just claimed instances)
   - Validate pattern similarity (not just superficially similar)

2. **Assess if a new artifact is warranted**
   - Threshold: >= 3 instances of identical or near-identical pattern
   - Impact: Would artifact reduce duplication by 50%+ LOC?
   - Maintenance: Would centralization improve maintainability?

3. **If warranted, queue for creation:**
   - Write entry to `integration-queue.jsonl` with `changeType: "backward-propagation"`
   - Set `proposedArtifact` field with type and suggested name
   - Set priority based on impact:
     - P1 (3-5 instances, security/critical patterns)
     - P2 (6+ instances, quality/consistency patterns)
   - Include validation evidence (file paths, LOC counts, pattern excerpts)

4. **Report back in integration analysis report:**

```markdown
## Backward Propagation Analysis

**Pattern**: <validated pattern description>
**Instances Found**: <actual count> (claimed: <original count>)
**Proposed Artifact**: <type>:<name>
**Justification**: <why centralization is beneficial>
**Priority**: P1 | P2
**Next Steps**: Queued for creator skill invocation
```

**Example Queue Entry:**

```jsonl
{
  "artifactId": "hook:jwt-validation",
  "changeType": "backward-propagation",
  "timestamp": "2026-02-08T10:30:00Z",
  "processed": false,
  "source": "code-reviewer",
  "pattern": "Manual JWT validation logic duplicated in 4 route handlers",
  "affectedFiles": [
    "routes/auth.ts",
    "routes/api.ts",
    "routes/admin.ts",
    "routes/user.ts"
  ],
  "validatedInstances": 4,
  "estimatedLOCReduction": 120,
  "priority": "P1",
  "proposedArtifact": {
    "type": "hook",
    "name": "jwt-validation",
    "rationale": "Centralize JWT validation for consistent security enforcement"
  }
}
```

**Rejection Criteria:**

- Pattern found in < 3 files (insufficient duplication)
- Pattern variations are too different (not truly duplicated)
- Existing artifact already handles this pattern (orphaned/underutilized)
- LOC reduction < 30 lines (insufficient benefit)

**Integration with Creator Skills:**

- Validated backward propagation entries trigger creator skill invocation
- Creator skills (skill-creator, hook-creator, template-creator, schema-creator) consume queue entries
- After creation, artifact-integrator processes the newly created artifact for standard integrations

### Step 4: Update Graph

After creating integration tasks:

- Add edges for newly discovered relationships
- Update node `integrationStatus` based on current state
- Save the graph

### Step 5: Mark Queue Entries Processed

For each processed entry, update the JSONL to mark `processed: true`

### Step 6: Report

Output a summary:

```
## Integration Analysis Report

Processed: {count} artifacts
Tasks created: {count}
Must-have gaps: {count}
Should-have gaps: {count}

### Details
[artifact-by-artifact breakdown]
```

## Arguments

- `artifactId` (optional) — Analyze a specific artifact instead of queue
- `mode` (optional) — 'queue' (default) | 'single' | 'health-check'

## Integration Rules by Artifact Type

| Type     | Must-Have                   | Should-Have          |
| -------- | --------------------------- | -------------------- |
| Skill    | Catalog + agent assignment  | Hook, workflow ref   |
| Agent    | Registry + routing keywords | Skills, model config |
| Hook     | settings.json registration  | Docs entry           |
| Workflow | Registry + agent mapping    | Docs entry           |
| Template | Catalog entry               | Consumer ref         |
| Schema   | Catalog entry               | Consumer wiring      |

## Example Usage

```javascript
Skill({ skill: 'artifact-integrator' });
// Processes queue, creates tasks, updates graph

Skill({ skill: 'artifact-integrator', args: 'skill:rate-limiter' });
// Analyzes specific artifact
```

## Implementation Reference

**Core Libraries:**

- `.claude/lib/workflow/integration-impact.cjs` - Impact analysis and task generation
- `.claude/lib/workflow/artifact-graph.cjs` - Graph CRUD operations

**Data Sources:**

- `.claude/context/runtime/integration-queue.jsonl` - Queue of artifacts needing integration
- `.claude/context/data/artifact-graph.json` - Artifact relationship graph

**Integration Queue Format:**

```jsonl
{"artifactId":"skill:rate-limiter","changeType":"created","timestamp":"2026-02-07T10:30:00Z","processed":false}
{"artifactId":"agent:security-architect","changeType":"updated","timestamp":"2026-02-07T10:35:00Z","processed":false}
```

## Workflow Integration

This skill is invoked by:

- Router Step 0.5 (automatic when queue entries exist)
- Creator skills (after artifact creation)
- Manual health checks

**Auto-invoke pattern:**

```javascript
// Router Step 0.5 pseudocode
if (integrationQueueHasUnprocessedEntries()) {
  Task({
    task_id: 'task-1',
    subagent_type: 'developer',
    prompt: 'Invoke Skill({ skill: "artifact-integrator" })',
  });
}
```

## Related Skills

- `research-synthesis` - Research phase before artifact creation
- `agent-creator` - Creates agents (triggers integration analysis)
- `skill-creator` - Creates skills (triggers integration analysis)
- `hook-creator` - Creates hooks (triggers integration analysis)
- `workflow-creator` - Creates workflows (triggers integration analysis)

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New integration pattern → `.claude/context/memory/learnings.md`
- Issue found → `.claude/context/memory/issues.md`
- Decision made → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
