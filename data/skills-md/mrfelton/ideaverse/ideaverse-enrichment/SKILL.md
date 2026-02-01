---
name: ideaverse-enrichment
description: Systematically add new knowledge to Ideaverse vaults while maintaining consistency. Use when assimilating new information, extracting concepts from sources, processing research, integrating learned knowledge, detecting duplicates, or classifying knowledge types. Triggers on requests like "add this to my vault", "process this article", "integrate this knowledge", "what type of knowledge is this", or "check for duplicates".
---

# Ideaverse Enrichment Skill

Use the ARC enrichment workflow to add new knowledge while maintaining consistency, detecting duplicates, and choosing appropriate structures. Assume familiarity with the core Ideaverse methodology.

## The ARC Enrichment Workflow

All knowledge enrichment follows the ARC pattern: **Add → Relate → Communicate**.

### Phase 1: ADD (Capture Without Friction)

```
1. Capture the raw information quickly
   ├── To daily log (if temporal)
   ├── To fleeting note (if needs processing)
   └── Direct to Atlas (if clearly permanent)

2. Include source attribution
   └── Where did this come from?

3. Don't organize yet
   └── Processing happens in RELATE phase
```

**Key principle**: Speed of capture matters. Don't let organization concerns prevent getting ideas into the system.

### Phase 2: RELATE (Connect & Integrate)

This is where enrichment quality is determined.

```
Step 2.1: Search Before Creating
    ↓
    ├── Search for existing notes on this concept
    ├── Check related MOCs for similar ideas
    └── If exists → Update existing note instead

Step 2.2: Classify Knowledge Type
    ↓
    ├── Concept? → Use concept extraction pattern
    ├── Process? → Use process documentation pattern
    ├── Entity? → Use entity profile pattern
    └── Principle? → Use principle articulation pattern

Step 2.3: Extract Atomic Notes
    ↓
    ├── One note per distinct concept
    ├── Keep notes focused and atomic
    └── Add proper frontmatter (up, related, created)

Step 2.4: Establish Connections
    ↓
    ├── Set up: property to relevant MOC
    ├── Add related: links to connected concepts
    ├── Add note to parent MOC
    └── Add back-links from related notes

Step 2.5: Validate Consistency
    ↓
    ├── Frontmatter complete?
    ├── Links working?
    └── No duplicates created?
```

### Phase 3: COMMUNICATE (Express & Use)

```
1. Use new knowledge in output
   ├── Reference in daily logs
   ├── Include in projects
   └── Build on for future work

2. Track completion
   └── Note in daily log that enrichment happened
```

## Knowledge Classification

Different types of knowledge require different structures. Classify before extracting.

### Type 1: Concepts

**What**: Abstract ideas, frameworks, mental models, theories

**Characteristics**:
- Stands alone as an idea
- Has relationships to other concepts
- Can be applied across domains

**Structure pattern**:
```markdown
# [Concept Name]

Brief definition in 1-2 sentences.

## Core Idea
What is this concept fundamentally about?

## Key Principles
- Principle 1
- Principle 2

## Connections
How does this relate to [[Related Concept]]?

## Applications
Where/when does this apply?

## Examples
Concrete instances of this concept.
```

**Use the prompt**: `ideaverse-enrichment-concepts.prompt`

### Type 2: Processes

**What**: Procedures, workflows, how-to knowledge, sequences

**Characteristics**:
- Has steps or phases
- Produces an outcome
- Can be followed repeatedly

**Structure pattern**:
```markdown
# [Process Name]

Brief description of what this process accomplishes.

## When to Use
Triggers or conditions for this process.

## Prerequisites
What's needed before starting?

## Steps
1. Step one
2. Step two
3. Step three

## Decision Points
If [condition], then [action].

## Common Variations
Alternative approaches when [situation].

## Failure Modes
What can go wrong and how to recover.
```

**Use the prompt**: `ideaverse-enrichment-processes.prompt`

### Type 3: Entities

**What**: People, organizations, tools, products, places

**Characteristics**:
- Specific instance, not abstract
- Has attributes and relationships
- Changes over time

**Structure pattern**:
```markdown
# [Entity Name]

Brief one-line description.

## Identity
What/who is this? Core attributes.

## Relationships
- Connected to [[Person/Org]]
- Uses [[Tool]]
- Part of [[System]]

## Context
Role, function, or purpose in your world.

## History
Key events, changes, timeline (if relevant).

## Notes
Additional observations.
```

**Use the prompt**: `ideaverse-enrichment-entities.prompt`

### Type 4: Principles

**What**: Rules, heuristics, guidelines, maxims

**Characteristics**:
- Prescriptive (tells you what to do)
- Has conditions of application
- May have exceptions

**Structure pattern**:
```markdown
# [Principle Name]

The principle stated clearly in one sentence.

## Definition
What does this principle mean in practice?

## When It Applies
Conditions where this principle is relevant.

## How to Apply
Practical guidance for using this principle.

## Counter-Examples
When does this NOT apply? What are the exceptions?

## Why It Matters
The reasoning behind this principle.

## Related Principles
- [[Similar Principle]]
- [[Contrasting Principle]]
```

**Use the prompt**: `ideaverse-enrichment-principles.prompt`

## Duplicate Detection

Before creating any new note, check for existing coverage.

### Search Strategy

```
1. Exact match search
   └── Search: [[concept name]]

2. Synonym search
   └── What other terms describe this?

3. MOC review
   └── Browse relevant MOC for similar concepts

4. Semantic scan
   └── What notes discuss related ideas?
```

### Duplicate Resolution

When a duplicate is found:

```
If new info < existing info:
    └── Add link to existing, don't create new

If new info supplements existing:
    └── Update existing note with new info

If notes are genuinely different:
    └── Create separate notes, add related: links

If unclear:
    └── Create new note, flag for later dedup review
```

### Merge Process

When consolidating duplicates:

```
1. Choose primary note (better structured/more complete)
2. Copy unique content from secondary to primary
3. Update links pointing to secondary → point to primary
4. Update MOCs to reference only primary
5. Delete secondary (or archive if uncertain)
```

## Enrichment Workflows

### Workflow: Article/Book Processing

```
1. Read/consume the source
    ↓
2. Capture key ideas to daily log
    - Use bullet points
    - Note source and page/location
    ↓
3. Identify distinct concepts (usually 2-5 per article)
    ↓
4. For each concept:
    a. Classify type (concept/process/entity/principle)
    b. Check for existing notes
    c. Create or update note
    d. Add to relevant MOC
    ↓
5. Create source note (optional)
    - Link to all extracted concepts
    - Add to Sources MOC
```

### Workflow: Experience Processing

```
1. Capture raw thoughts/observations
    ↓
2. Let it sit (optional - allows reflection)
    ↓
3. Identify the generalizable insight
    - What can I learn from this that applies elsewhere?
    ↓
4. Extract as principle or concept note
    ↓
5. Link to specific experience in daily log
```

### Workflow: Research Integration

```
1. Gather sources on topic
    ↓
2. Create temporary synthesis note
    - List all sources
    - Note key points from each
    ↓
3. Identify gaps in existing vault knowledge
    ↓
4. Create atomic notes to fill gaps
    ↓
5. Update relevant MOC with new structure
    ↓
6. Archive or keep synthesis note as overview
```

## Best Practices

### Quality Over Quantity
- Better to have 10 well-linked notes than 100 orphans
- Take time in the RELATE phase
- Verify connections are meaningful

### Source Attribution
- Always note where knowledge came from
- Makes future verification possible
- Helps trace your thinking

### Incremental Enrichment
- Don't try to capture everything at once
- Regular small additions beat occasional large dumps
- Let structure emerge naturally

### Validation Checklist

Before considering enrichment complete:
- [ ] Frontmatter has `up:` and `created:`
- [ ] Note added to relevant MOC
- [ ] At least one related: link if applicable
- [ ] No broken links introduced
- [ ] No duplicate created (or duplicates merged)

## Reference Documentation

For detailed patterns and extraction templates, see:
- [references/enrichment-workflow.md](references/enrichment-workflow.md) - Complete ARC workflow details
- [references/knowledge-classification.md](references/knowledge-classification.md) - Deep dive on knowledge types
- [references/extraction-templates.md](references/extraction-templates.md) - Type-specific extraction templates, guidelines, and quality signals
- [references/duplicate-detection.md](references/duplicate-detection.md) - Finding and handling duplicates

All extraction workflows are contained within this skill—no external prompts needed.