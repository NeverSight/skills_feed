---
name: syncing-submodules
description: Use when running /ltk:sync-submodules, updating submodules, or needing to "sync", "merge", "adapt", "learn from" other Claude Code plugins or repos
version: 2.0.0
---

# Intelligent Submodule Sync System

This skill provides a sophisticated framework for syncing components from git submodules while ensuring consistency, avoiding duplicates, and maintaining quality.

## Core Principles

1. **No Duplicates** - Same concept should exist only once
2. **No Near-Duplicates** - Similar concepts should be merged
3. **Quality Over Quantity** - Better to have fewer excellent components than many mediocre ones
4. **Semantic Analysis** - Compare meaning, not just names
5. **Synthesis Over Copying** - Create superior merged versions

---

## Phase 1: Deep Discovery

### 1.1 Scan All Submodules

```bash
# Update submodules
git submodule update --remote --merge

# Create inventory
for submodule in submodules/*/; do
  echo "=== $submodule ==="
  find "$submodule" -name "SKILL.md" -o -name "*.md" -path "*/commands/*" -o -name "*.md" -path "*/agents/*"
done
```

### 1.2 Extract Component Metadata

For EACH discovered component, extract:

```yaml
component:
  name: "component-name"
  type: "skill|agent|command|hook"
  source: "submodule-name"
  path: "full/path/to/file"

  # Deep analysis fields
  primary_purpose: "One sentence describing main function"
  keywords: ["keyword1", "keyword2", "keyword3"]
  capabilities: ["capability1", "capability2"]
  target_audience: "who uses this"
  domain: "core|engineering|data|devops|design|product|github"
```

---

## Phase 2: Semantic Similarity Analysis

### 2.1 Similarity Detection Matrix

For each pair of components (existing + new), calculate similarity:

| Similarity Type | Weight | Detection Method |
|-----------------|--------|------------------|
| **Name Similarity** | 15% | Levenshtein distance, common prefixes |
| **Keyword Overlap** | 25% | Jaccard similarity of extracted keywords |
| **Purpose Overlap** | 30% | Semantic comparison of descriptions |
| **Capability Overlap** | 30% | Function/feature comparison |

### 2.2 Similarity Thresholds

| Score | Classification | Action |
|-------|----------------|--------|
| 90-100% | **Duplicate** | Keep best, discard other |
| 70-89% | **Near-Duplicate** | Merge into single component |
| 50-69% | **Related** | Consider consolidation |
| 30-49% | **Tangentially Related** | Keep separate, cross-reference |
| 0-29% | **Distinct** | Add if quality threshold met |

### 2.3 Semantic Comparison Checklist

When comparing two similar components:

```markdown
## Comparison: [Component A] vs [Component B]

### Purpose Analysis
- A's purpose: ___
- B's purpose: ___
- Overlap: ___% | Distinct: ___%

### Content Comparison
| Aspect | Component A | Component B | Better |
|--------|-------------|-------------|--------|
| Completeness | 1-10 | 1-10 | A/B |
| Clarity | 1-10 | 1-10 | A/B |
| Examples | count | count | A/B |
| Edge cases | count | count | A/B |
| Actionability | 1-10 | 1-10 | A/B |

### Unique Features
- Only in A: ___
- Only in B: ___

### Decision: [KEEP_A | KEEP_B | MERGE | KEEP_BOTH]
### Rationale: ___
```

---

## Phase 3: Quality Scoring

### 3.1 Component Quality Rubric

Score each component 0-100:

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| **Completeness** | 20% | Covers topic thoroughly |
| **Clarity** | 20% | Easy to understand and follow |
| **Actionability** | 15% | Provides concrete steps |
| **Examples** | 15% | Has good, relevant examples |
| **Edge Cases** | 10% | Handles exceptions |
| **Formatting** | 10% | Proper markdown, structure |
| **CSO Optimization** | 10% | Good trigger phrases in description |

### 3.2 Quality Thresholds

| Score | Quality Level | Action |
|-------|---------------|--------|
| 80-100 | **Excellent** | Add/keep as-is |
| 60-79 | **Good** | Add with minor improvements |
| 40-59 | **Mediocre** | Only add if fills gap, improve first |
| 0-39 | **Poor** | Do not add |

---

## Phase 4: Conflict Resolution

### 4.1 Same Concept, Different Names

Example: "verification" vs "validation" vs "checking-work"

**Resolution Process:**

1. Identify all variants
2. Analyze each for unique value
3. Choose canonical name (most intuitive)
4. Merge all content into canonical
5. Ensure description covers ALL trigger phrases

### 4.2 Same Name, Different Purposes

Example: Two "debug" commands doing different things

**Resolution Process:**

1. Determine which aligns with ltk's existing conventions
2. Rename the other to be more specific
3. Or merge if they're complementary

### 4.3 Conflicting Advice

Example: One says "always use X", another says "never use X"

**Resolution Process:**

1. Identify the CONTEXT for each piece of advice
2. Create nuanced guidance with conditions
3. Add examples for each scenario
4. Document when each applies

### 4.4 Decision Tree

```
Is this component new to ltk?
├── YES → Quality score >= 60?
│   ├── YES → Add with ltk conventions
│   └── NO → Skip or improve first
│
└── NO → Similar exists in ltk
    ├── Similarity >= 90% (Duplicate)
    │   └── Compare quality scores → Keep better one
    │
    ├── Similarity 70-89% (Near-Duplicate)
    │   └── Merge: combine best of both
    │
    ├── Similarity 50-69% (Related)
    │   └── Evaluate: consolidate or keep separate?
    │
    └── Similarity < 50% (Distinct enough)
        └── Quality score >= 60? → Add
```

---

## Phase 5: Domain-Specific Placement

### 5.1 Domain Classification

| Domain | Plugin | Indicators |
|--------|--------|------------|
| Context/Memory/Agents | ltk-core | "context", "memory", "agent", "prompt", "LLM" |
| Code/Testing/Architecture | ltk-engineering | "code", "test", "refactor", "architecture" |
| Data/ML/Analytics | ltk-data | "data", "SQL", "ML", "analytics", "database" |
| Infrastructure/Security | ltk-devops | "deploy", "k8s", "docker", "security", "CI/CD" |
| UI/UX/Accessibility | ltk-design | "design", "UI", "UX", "accessibility", "CSS" |
| Marketing/Sales/Business | ltk-product | "marketing", "sales", "SEO", "content", "business" |
| Git/GitHub/PRs | ltk-github | "git", "PR", "commit", "GitHub", "branch" |

### 5.2 Cross-Domain Components

Some components span domains. Place in PRIMARY domain, cross-reference in others:

```yaml
# In primary location
---
name: component-name
related:
  - ltk-engineering/skills/related-skill
  - ltk-devops/agents/related-agent
---
```

---

## Phase 6: Merge Strategies

### 6.1 Skill Merge Template

```markdown
---
name: merged-skill-name
description: [Combined CSO-optimized description covering ALL trigger phrases]
version: 1.0.0
sources: [source1, source2]  # Attribution
---

# [Skill Title]

[Best introduction from all sources]

## [Section from Source A - if superior]

[Content]

## [Section from Source B - if unique]

[Content]

## [Merged section - combining both]

[Synthesized content taking best from each]

<!--
Merge Notes:
- Took X from source1 because: reason
- Took Y from source2 because: reason
- Combined Z because: reason
-->
```

### 6.2 Agent Merge Strategy

```markdown
---
agent: merged-agent-name
description: |
  [Combined description with all use cases]
  <example>...</example>
  <example>...</example>  # Include examples from ALL sources
model: [keep more capable model]
tools: [union of all tools needed]
color: [consistent with ltk conventions]
sources: [source1, source2]
---

# [Agent Title]

[Synthesized capabilities from all sources]

## Workflow
[Best workflow, enhanced with steps from other sources]
```

### 6.3 Command Merge Strategy

Commands should generally NOT be merged - they're distinct actions. Instead:

- Keep the more complete version
- Add unique features from other version
- Ensure no naming conflicts

---

## Phase 7: Deduplication Audit

### 7.1 Pre-Sync Audit

Before syncing, audit EXISTING ltk components:

```bash
# Find potential duplicates by keyword analysis
for skill in plugins/*/skills/*/SKILL.md; do
  echo "=== $skill ==="
  grep -i "description:" "$skill"
done | sort | uniq -c | sort -rn
```

### 7.2 Duplicate Detection Patterns

| Pattern | Likely Duplicate |
|---------|------------------|
| Same verb + noun | "code review" / "reviewing code" |
| Synonym usage | "validate" / "verify" / "check" |
| Same domain + action | "git commit" / "committing changes" |
| Acronym vs full | "TDD" / "test driven development" |

### 7.3 Post-Sync Verification

After sync, verify no duplicates introduced:

```bash
# Check for duplicate skill names
find plugins -name "SKILL.md" -exec basename {} \; | sort | uniq -c | sort -rn | head -20

# Check for duplicate agent names
find plugins/*/agents -name "*.md" -exec basename {} .md \; | sort | uniq -c | sort -rn | head -20

# Check for duplicate command names
find plugins/*/commands -name "*.md" -exec basename {} .md \; | sort | uniq -c | sort -rn | head -20
```

---

## Phase 8: Output Report Format

```markdown
# Submodule Sync Report

**Date:** YYYY-MM-DD
**Submodules Analyzed:** N
**Components Discovered:** N
**Components Added:** N
**Components Merged:** N
**Duplicates Removed:** N

## Similarity Analysis Summary

| Comparison | Similarity | Decision |
|------------|------------|----------|
| A vs B | 85% | Merged → A |
| C vs D | 95% | Duplicate, kept C |
| E vs F | 45% | Kept both |

## Quality Scores

| Component | Source | Score | Decision |
|-----------|--------|-------|----------|
| skill-x | submodule-1 | 82 | Added |
| agent-y | submodule-2 | 55 | Improved, then added |
| command-z | submodule-3 | 35 | Rejected (low quality) |

## Components Added

| Type | Name | Domain | Source | Notes |
|------|------|--------|--------|-------|
| skill | name | ltk-core | sub1 | New capability |

## Components Merged

| Result | Sources | Merge Strategy |
|--------|---------|----------------|
| skill-a | skill-a1 + skill-a2 | Combined best sections |

## Duplicates Resolved

| Kept | Removed | Reason |
|------|---------|--------|
| A (ltk) | A' (submodule) | ltk version more complete |

## Rejected (Quality)

| Component | Source | Score | Reason |
|-----------|--------|-------|--------|
| skill-x | sub3 | 35 | Poor formatting, incomplete |

## Action Items

- [ ] Review merged component: X
- [ ] Test new command: Y
- [ ] Consider consolidating: Z1 + Z2
```

---

## Remember

1. **Always do semantic analysis** - Names can be deceiving
2. **Quality gates are mandatory** - Don't add mediocre content
3. **Merge > Add** - Prefer enhancing existing over adding similar
4. **Attribution matters** - Credit sources
5. **Test after sync** - Verify nothing broke
6. **Document decisions** - Future you will thank present you
