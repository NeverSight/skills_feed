---
name: research-web
description: "Comprehensive multi-wave web research with strategic source selection. Gathers information from official docs, community resources, and advanced sources. Use for deep technical research, API documentation, best practices. Triggers: research web, deep research, comprehensive research, find documentation."
---

**User request**: $ARGUMENTS

Comprehensive multi-wave web research. Strategically selects sources, evaluates credibility, cross-references findings, and synthesizes actionable recommendations.

**Research log**: `/tmp/research-web-{YYYYMMDD-HHMMSS}-{topic-kebab-case}.md` - external memory for all findings.

## Phase 1: Research Planning

### 1.1 Parse Request

Extract from `$ARGUMENTS`:
- **Primary question**: What are we trying to learn?
- **Context**: Why do we need this? What decision does it inform?
- **Constraints**: Version requirements, platform limitations, etc.

**If vague or empty**: Ask user to clarify the specific question.

### 1.2 Create Research Log

Path: `/tmp/research-web-{YYYYMMDD-HHMMSS}-{topic-kebab-case}.md`

```markdown
# Web Research: {topic}
Started: {timestamp}

## Research Question
{Primary question}

## Context
{Why needed, what decision it informs}

## Initial Hypotheses
(populated in 1.3)

## Wave Results
(populated during research)

## Source Registry
(populated during research)

## Conflicts
(populated when sources disagree)

## Synthesis
(populated in Phase 4)
```

### 1.3 Form Initial Hypotheses

Before searching, document what you expect to find:

```markdown
## Initial Hypotheses

### H1: {Expected answer}
- Confidence: Low | Medium | High
- Would falsify: {what would prove this wrong}

### H2: {Alternative possibility}
- Confidence: Low | Medium | High
- Would falsify: {what would prove this wrong}
```

**Why hypotheses first**: Prevents confirmation bias. Search for evidence both supporting AND refuting.

### 1.4 Create Todo List

```
- [ ] Wave 1: Official documentation
- [ ] Wave 2: Community resources
- [ ] Wave 3: Advanced/specialized sources
- [ ] Cross-reference and resolve conflicts
- [ ] Synthesize findings
```

## Phase 2: Strategic Wave Research

### Wave Selection Strategy

| Wave | Source Type | Purpose | When to Use |
|------|-------------|---------|-------------|
| 1 | Official docs, GitHub repos | Canonical behavior, API specs | Always start here |
| 2 | Stack Overflow, tutorials, blogs | Practical examples, common issues | After official gaps identified |
| 3 | Academic papers, expert blogs, niche forums | Edge cases, advanced techniques | When waves 1-2 insufficient |

### 2.1 Wave 1: Official Sources

**Priority sources**:
1. Official documentation sites
2. GitHub repositories (README, docs/, wiki)
3. Official API references
4. Release notes and changelogs

**Search queries**:
- `{topic} official documentation`
- `{topic} github`
- `{technology} {feature} docs`

**Document each source**:
```markdown
### Source: {title}
**URL**: {url}
**Type**: Official Documentation | GitHub | API Reference
**Date**: {publication/update date}
**Credibility**: High (official)

**Key findings**:
- {Finding 1}
- {Finding 2}

**Evidence**:
> "{Relevant quote}"

**Supports/Refutes**: H1, H2
```

### 2.2 Wave 2: Community Resources

**Priority sources**:
1. Stack Overflow (recent, accepted answers)
2. Technical blogs (reputable authors)
3. Tutorial sites
4. Discussion forums

**Search queries**:
- `{topic} example`
- `{topic} tutorial`
- `{topic} best practices`
- `{technology} {error message}` (if troubleshooting)

**Credibility indicators**:
- High: Accepted answer, author is maintainer/contributor, multiple upvotes
- Medium: Popular answer, detailed explanation, includes code
- Low: Old answer, no engagement, no sources

### 2.3 Wave 3: Advanced Sources

Only proceed if waves 1-2 leave gaps.

**Sources**:
- Academic papers (for algorithms, protocols)
- Expert technical blogs
- Conference talks
- Specialized forums/communities
- Source code analysis

**Search queries**:
- `{topic} paper`
- `{topic} deep dive`
- `{topic} internals`

## Phase 3: Research Loop

### Memento Loop

For each wave:

1. Mark wave todo `in_progress`
2. Execute searches
3. Evaluate and document each source
4. **Write findings immediately** to research log
5. Update hypothesis status
6. Mark wave todo `completed`
7. Decide: proceed to next wave or sufficient?

**NEVER proceed without writing findings** — research log is external memory.

### 3.1 Source Credibility Evaluation

For each source, assess:

| Factor | High | Medium | Low |
|--------|------|--------|-----|
| Authority | Official, maintainer | Expert, educator | Anonymous, unknown |
| Recency | <6 months | <2 years | >2 years |
| Verification | Multiple sources agree | Some corroboration | Single source |
| Depth | Shows understanding | Practical focus | Surface level |

### 3.2 Update Hypotheses

As findings come in:

```markdown
### H1: {hypothesis}
- Status: CONFIRMED | REFUTED | UNCERTAIN
- Confidence: Low | Medium | High
- Evidence: {summary}
- Sources: {list}
```

### 3.3 Handle Conflicts

When sources disagree:

```markdown
## Conflicts

### {Topic of disagreement}
**Position A**: {claim}
- Sources: {list}
- Strength: {why credible}

**Position B**: {claim}
- Sources: {list}
- Strength: {why credible}

**Resolution**:
- {Your assessment based on source authority, recency, consensus}
- OR "Unresolved - present both options to user"
```

**Conflict resolution priority**:
1. Official docs > community
2. Recent > old
3. Multiple sources > single source
4. Code/specs > opinions

### 3.4 Wave Completion Criteria

**Stop wave when**:
- Primary question answered with high confidence
- Multiple authoritative sources agree
- Diminishing returns (same info repeating)

**Proceed to next wave when**:
- Gaps remain in understanding
- Only low-credibility sources found
- Conflicting information needs resolution

## Phase 4: Synthesis

### 4.1 Refresh Context

Read the full research log before synthesizing.

### 4.2 Cross-Reference Findings

Verify key claims appear in multiple independent sources:

```markdown
## Cross-Reference Matrix

| Finding | Official | Community | Expert |
|---------|----------|-----------|--------|
| {Finding 1} | ✓ source | ✓ source | - |
| {Finding 2} | ✓ source | ✓ source | ✓ source |
| {Finding 3} | - | ✓ source | - |
```

### 4.3 Write Synthesis

```markdown
## Synthesis

### Answer to Primary Question
{Direct answer}
**Confidence**: High | Medium | Low
**Based on**: {N} sources, {consensus level}

### Key Findings
1. {Finding with source citations}
2. {Finding with source citations}
3. {Finding with source citations}

### Hypothesis Resolution
- H1: {CONFIRMED/REFUTED} — {evidence}
- H2: {CONFIRMED/REFUTED} — {evidence}

### Caveats and Limitations
- {What we couldn't verify}
- {Where information was sparse}
- {Time-sensitivity concerns}

### Recommendations
1. {Primary recommendation with rationale}
2. {Alternative approach and when to use}
3. {What to avoid and why}

### Sources by Authority

**Official**:
- {Source with URL}

**Community (High credibility)**:
- {Source with URL}

**Other**:
- {Source with URL}
```

### 4.4 Present Summary

```
## Research Complete

**Question**: {Primary question}
**Confidence**: High | Medium | Low
**Waves completed**: {N}
**Sources consulted**: {N}

### Answer
{Concise direct answer}

### Key Findings
- {Finding 1}
- {Finding 2}
- {Finding 3}

### Recommendations
1. {What to do}
2. {What to avoid}

### Caveats
- {Key limitation}

### Top Sources
- {Most authoritative source}
- {Second source}

**Full research log**: /tmp/research-web-{...}.md
```

## Guidelines

### DO
- Document hypotheses BEFORE searching
- Record ALL sources, even unhelpful ones
- Note publication dates
- Cross-reference important claims
- Acknowledge uncertainty
- Update log after EACH source

### DON'T
- Trust single sources for important claims
- Ignore publication dates
- Present opinions as facts
- Skip synthesis step
- Make claims without citations
- Cherry-pick confirming sources

## Source Authority Hierarchy

1. **Official docs** — How things are supposed to work
2. **Source code** — How things actually work
3. **GitHub issues** — Real problems and workarounds
4. **Stack Overflow** — Community solutions (CHECK DATES!)
5. **Technical blogs** — Opinions and tutorials (verify claims)
6. **General articles** — Background only

## Time Sensitivity

| Domain | Information Half-life |
|--------|----------------------|
| Web frameworks | 6-12 months |
| Languages | 1-2 years |
| CS fundamentals | 5+ years |
| Security | 3-6 months |
| Cloud services | 6-12 months |

Always note when information might be outdated.

## Edge Cases

| Case | Action |
|------|--------|
| No relevant sources | Note in log, ask user for alternative terms |
| All sources outdated | Note prominently, recommend verifying with latest docs |
| Conflicting authoritative sources | Present both with evidence, let user decide |
| Topic too broad | Ask user to narrow scope |
| Paywalled content | Note limitation, search for alternatives |
