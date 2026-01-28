---
name: consensus-voting
description: Byzantine consensus voting for multi-agent decision making. Implements voting protocols, conflict resolution, and agreement algorithms for reaching consensus among multiple agents.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
best_practices:
  - Require minimum quorum for decisions
  - Weight votes by agent expertise
  - Document dissenting opinions
  - Escalate unresolved conflicts
error_handling: graceful
streaming: supported
---

# Consensus Voting Skill

<identity>
Consensus Voting Skill - Implements voting protocols and conflict resolution algorithms for reaching consensus among multiple agents with potentially conflicting recommendations.
</identity>

<capabilities>
- Collecting votes from multiple agents
- Weighted voting based on expertise
- Conflict detection and resolution
- Quorum verification
- Decision documentation
</capabilities>

<instructions>
<execution_process>

### Step 1: Define Voting Parameters

Set up the voting session:

```yaml
voting_session:
  topic: 'Which database to use for the new service'
  options:
    - PostgreSQL
    - MongoDB
    - DynamoDB
  quorum: 3 # Minimum votes required
  threshold: 0.6 # 60% agreement needed
  weights:
    database-architect: 2.0 # Expert gets 2x weight
    security-architect: 1.0
    devops: 1.5
```

### Step 2: Collect Votes

Gather agent recommendations:

```markdown
## Vote Collection

### database-architect (weight: 2.0)

- Vote: PostgreSQL
- Rationale: Strong ACID guarantees, mature ecosystem
- Confidence: 0.9

### security-architect (weight: 1.0)

- Vote: PostgreSQL
- Rationale: Better encryption at rest, audit logging
- Confidence: 0.8

### devops (weight: 1.5)

- Vote: DynamoDB
- Rationale: Managed service, auto-scaling
- Confidence: 0.7
```

### Step 3: Calculate Consensus

Apply weighted voting:

```
PostgreSQL: (2.0 * 0.9) + (1.0 * 0.8) = 2.6
DynamoDB:   (1.5 * 0.7) = 1.05
MongoDB:    0

Total weight: 4.5
PostgreSQL: 2.6 / 4.5 = 57.8%
DynamoDB:   1.05 / 4.5 = 23.3%

Threshold: 60% → No clear consensus
```

### Step 4: Resolve Conflicts

When no consensus is reached:

**Strategy 1: Expert Override**

- If domain expert has strong opinion (>0.8 confidence), defer to expert

**Strategy 2: Discussion Round**

- Ask dissenting agents to respond to majority arguments
- Re-vote after discussion

**Strategy 3: Escalation**

- Present options to user with pros/cons from each agent
- Let user make final decision

### Step 5: Document Decision

Record the final decision:

```markdown
## Decision Record

### Topic

Which database to use for the new service

### Decision

PostgreSQL

### Voting Summary

- PostgreSQL: 57.8% (2 votes)
- DynamoDB: 23.3% (1 vote)
- Consensus: NOT REACHED (below 60% threshold)

### Resolution Method

Expert override - database-architect (domain expert)
had 0.9 confidence in PostgreSQL

### Dissenting Opinion

DevOps preferred DynamoDB for operational simplicity.
Mitigation: Will use managed PostgreSQL (RDS) to
reduce operational burden.

### Decision Date

2026-01-23
```

</execution_process>

<best_practices>

1. **Quorum Required**: Don't decide without minimum participation
2. **Weight by Expertise**: Domain experts get more influence
3. **Document Dissent**: Record minority opinions for future reference
4. **Clear Thresholds**: Define what constitutes consensus upfront
5. **Escalation Path**: Have a process for unresolved conflicts

</best_practices>
</instructions>

<examples>
<usage_example>
**Conflict Resolution Request**:

```
The architect wants microservices but the developer prefers monolith.
Resolve this conflict.
```

**Voting Process**:

```markdown
## Voting: Architecture Style

### Votes

- architect: Microservices (weight 1.5, confidence 0.8)
- developer: Monolith (weight 1.0, confidence 0.9)
- devops: Microservices (weight 1.0, confidence 0.6)

### Calculation

Microservices: (1.5 _ 0.8) + (1.0 _ 0.6) = 1.8
Monolith: (1.0 \* 0.9) = 0.9

Microservices: 66.7% → CONSENSUS REACHED

### Decision

Microservices, with modular monolith as migration path

### Dissent Mitigation

Start with modular monolith, extract services incrementally
to address developer's maintainability concerns.
```

</usage_example>
</examples>

## Rules

- Always require quorum before deciding
- Weight votes by domain expertise
- Document dissenting opinions for future reference

## Related Workflow

This skill has a corresponding workflow for complex multi-agent scenarios:

- **Workflow**: `.claude/workflows/consensus-voting-skill-workflow.md`
- **When to use workflow**: For critical multi-agent decisions requiring Byzantine fault-tolerant consensus with Queen/Worker topology (architectural decisions, security reviews, technology selection)
- **When to use skill directly**: For simple voting scenarios or when integrating consensus into other workflows

## Workflow Integration

This skill enables decision-making in multi-agent orchestration:

**Router Decision:** `.claude/workflows/core/router-decision.md`

- Router spawns multiple reviewers, then uses consensus to resolve conflicts
- Planning Orchestration Matrix triggers consensus voting for review phases

**Artifact Lifecycle:** `.claude/workflows/core/skill-lifecycle.md`

- Consensus voting determines artifact deprecation decisions
- Multiple maintainers vote on breaking changes

**Related Workflows:**

- `swarm-coordination` skill for parallel agent spawning before voting
- Enterprise workflows use consensus for design reviews
- Security reviews in `.claude/workflows/enterprise/` require security-architect consensus

---

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
