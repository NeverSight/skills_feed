---
name: web-research
description: "Conduct structured web research with hypothesis tracking. Synthesizes information from multiple sources into actionable findings. Use for technical research, API docs, best practices. Triggers: web research, look up, search for, find documentation."
metadata:
  short-description: "Structured web research"
---

**User request**: $ARGUMENTS

Conduct structured web research to gather external information, synthesize findings, and provide actionable recommendations.

**Output file**: `/tmp/research-{YYYYMMDD-HHMMSS}-{topic-kebab-case}.md`

## Phase 1: Setup

### 1.1 Define Research Scope

Identify:
- **Primary question**: What are we trying to learn? (single clear question)
- **Context**: Why do we need this? What's the decision this informs?
- **Success criteria**: What would a good answer include?
- **Scope boundary**: What's explicitly NOT included in this research?

**If $ARGUMENTS is vague**: Ask user to clarify the primary question before proceeding.

### 1.2 Create Research Log

Path: `/tmp/research-{YYYYMMDD-HHMMSS}-{topic-kebab-case}.md`

```markdown
# Research Log: {topic}
Started: {timestamp}

## Research Question
{Primary question}

## Context
{Why we need this, what decision it informs}

## Success Criteria
{What a good answer includes}

## Hypotheses
(populated in 1.3)

## Sources Consulted
(populated during research)

## Findings
(populated during research)

## Conflicts
(populated when sources disagree)

## Synthesis
(populated in Phase 3)
```

### 1.3 Form Initial Hypotheses

Before searching, document initial hypotheses:

```markdown
## Hypotheses

1. H1: {What we think might be true}
   - Confidence: Low/Medium/High
   - Would falsify: {what evidence would disprove this}

2. H2: {Alternative possibility}
   - Confidence: Low/Medium/High
   - Would falsify: {what evidence would disprove this}

3. H3: {Another angle to consider}
   - Confidence: Low/Medium/High
   - Would falsify: {what evidence would disprove this}
```

**Why hypotheses first**: Prevents confirmation bias. You'll search for evidence both supporting AND refuting each hypothesis.

### 1.4 Create Todo List

Use `update_plan`:

```
- [ ] Research H1: {hypothesis}
- [ ] Research H2: {hypothesis}
- [ ] Research H3: {hypothesis}
- [ ] (expand as research reveals new angles)
- [ ] Synthesize findings
```

## Phase 2: Research Loop

### Memento Loop

For each hypothesis/question:
1. Mark todo `in_progress`
2. Search for evidence
3. **Write findings immediately** to research log
4. Update hypothesis status
5. Expand todos for new angles discovered
6. Mark todo `completed`
7. Repeat until all hypotheses resolved

**NEVER proceed without writing findings** — research log = external memory.

### 2.1 Search Strategically

For each hypothesis/question:

1. **Formulate search queries**
   - Start broad, then narrow based on results
   - Use technical terms and specific version numbers
   - Try multiple phrasings of the same concept
   - Include year for time-sensitive topics

2. **Source priority** (higher = more authoritative):

   | Priority | Source Type | Use For |
   |----------|-------------|---------|
   | 1 | Official documentation | Canonical behavior, API specs |
   | 2 | Source code (GitHub) | Ground truth implementation |
   | 3 | GitHub issues/discussions | Real-world problems, edge cases |
   | 4 | Stack Overflow (recent) | Common problems, solutions |
   | 5 | Technical blogs (reputable) | Tutorials, opinions, comparisons |
   | 6 | General articles | Background context only |

3. **Evaluate source quality**
   - Is it official/authoritative?
   - Is it current (check publication date)?
   - Does it cite sources or show evidence?
   - Do multiple independent sources agree?
   - Is the author credible in this domain?

### 2.2 Document Findings

After each source, update research log immediately:

```markdown
### Source: {title}
**URL**: {url}
**Date**: {publication date or "undated"}
**Authority**: Official | Expert | Community | Unknown
**Credibility**: High | Medium | Low
**Relevant to**: H1, H2

**Key findings**:
- {Finding 1}
- {Finding 2}

**Evidence**:
> "{Relevant quote}" — {source}

**Supports**: H1
**Refutes**: H2
**Conflicts with**: {other source, if any}
```

### 2.3 Update Hypotheses

As findings come in, update each hypothesis:

```markdown
### H1: {hypothesis}
- Status: CONFIRMED | REFUTED | UNCERTAIN | NEEDS MORE DATA
- Confidence: Low | Medium | High
- Evidence: {summary of supporting/refuting evidence}
- Sources: {list}
```

### 2.4 Handle Conflicting Information

When sources disagree:

1. **Check dates** — newer often supersedes older
2. **Check authority** — official > community > individual
3. **Check specificity** — exact version > general statement
4. **Check consensus** — 5 sources agreeing > 1 outlier
5. **Note the conflict** in research log:

```markdown
## Conflicts

### {Topic of disagreement}
**Position A**: {claim} — supported by {sources}
**Position B**: {claim} — supported by {sources}
**Resolution**: {your assessment} or "Unresolved - present both"
```

### 2.5 Know When to Stop

Stop researching when:
- Primary question is answered with high confidence
- Multiple authoritative sources agree
- Hypotheses are resolved (confirmed or refuted)
- Further searching yields diminishing returns
- You've hit time/effort limits

**Diminishing returns signals**:
- Same information appearing across sources
- No new hypotheses emerging
- Low-quality sources dominating results

## Phase 3: Synthesis

### 3.1 Refresh Context

Read the full research log before synthesizing. This restores all findings to recent context.

### 3.2 Write Synthesis

```markdown
## Synthesis

### Answer to Primary Question
{Direct answer with confidence level: High/Medium/Low}

### Key Findings
1. {Most important finding with source}
2. {Second finding with source}
3. {Third finding with source}

### Hypothesis Resolution
- H1: {CONFIRMED/REFUTED/UNCERTAIN} — {evidence summary}
- H2: {CONFIRMED/REFUTED/UNCERTAIN} — {evidence summary}
- H3: {CONFIRMED/REFUTED/UNCERTAIN} — {evidence summary}

### Evidence Summary
- {Finding} supported by {N} authoritative sources
- {Finding} has conflicting information: {explain disagreement}

### Caveats and Limitations
- {What we couldn't verify}
- {Where information was sparse}
- {Potential biases in sources}
- {Time-sensitivity of findings}

### Recommendations
1. {Actionable recommendation with rationale}
2. {Alternative approach and when to use}
3. {What to watch out for}

### Sources (by authority)
**Official**:
- {Source with URL}

**Expert/Community**:
- {Source with URL}

**Other**:
- {Source with URL}
```

### 3.3 Present Summary

```markdown
## Research Summary

**Question**: {Primary question}
**Confidence**: High | Medium | Low
**Research log**: /tmp/research-{...}.md

### Answer
{Concise direct answer}

### Key Findings
- {Finding 1}
- {Finding 2}
- {Finding 3}

### Recommendations
1. {What to do}
2. {What to avoid}
3. {What to monitor}

### Caveats
- {Key limitation or uncertainty}

### Top Sources
- {Most authoritative source with URL}
- {Second source with URL}
```

## Guidelines

### DO
- Document hypotheses BEFORE searching (reduces confirmation bias)
- Record ALL sources consulted, even unhelpful ones
- Note contradictions between sources explicitly
- Cite specific sources for claims
- Acknowledge uncertainty and limitations
- Update research log after EACH source
- Include publication dates for all sources

### DON'T
- Cherry-pick sources that confirm expectations
- Trust single sources for important claims
- Ignore publication dates (outdated info is dangerous)
- Present opinions as facts
- Skip the synthesis step
- Make claims without source attribution
- Assume first result is best result

### Source Authority Hierarchy

1. **Official docs** — Highest authority for how things are supposed to work
2. **Source code** — Ground truth for how things actually work
3. **GitHub issues** — Real-world problems, edge cases, workarounds
4. **Stack Overflow** — Community solutions (CHECK DATES!)
5. **Technical blogs** — Opinions and tutorials (verify claims)
6. **General articles** — Background only, never cite for specifics

### Time Sensitivity

For technical topics:
- Web frameworks: 6-12 months (rapidly changing)
- Languages: 1-2 years (slower changing)
- CS fundamentals: 5+ years (stable)
- Security: 3-6 months (actively exploited)

Always note when information might be outdated.

## Edge Cases

| Case | Action |
|------|--------|
| No relevant sources found | Note in log, ask user for more context or alternative terms |
| Conflicting authoritative sources | Present both positions with evidence, recommend user decide |
| Topic is too broad | Ask user to narrow scope before researching |
| All sources are outdated | Note prominently, recommend user verify with official docs |
| Research reveals scope was wrong | Ask user if they want to pivot or continue |
