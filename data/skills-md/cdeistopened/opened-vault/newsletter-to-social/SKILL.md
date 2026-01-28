---
name: newsletter-to-social
description: Extract standalone snippets from newsletters and route to social platforms using parallel sub-agents. Transforms one newsletter into 6-9 platform-optimized social posts.
---

# Newsletter to Social Router

Transform a single newsletter into multiple social posts using the framework fitting method.

## When to Use

- After publishing a daily or weekly newsletter
- When repurposing newsletter content for social
- For batch social scheduling from newsletter source

## The Process

```
NEWSLETTER
    │
    ├─→ THOUGHT segment → Extract hot take
    │       ├─→ LinkedIn (Contrarian template)
    │       ├─→ X (Paradox Hook)
    │       └─→ Instagram (Quote card)
    │
    ├─→ TREND segment → Extract stat + interpretation
    │       ├─→ LinkedIn (Authority template)
    │       └─→ X (Commentary)
    │
    └─→ TOOL segment → Extract recommendation
            ├─→ LinkedIn (List/How-to)
            └─→ X (Thread: tool + benefits)
```

## Phase 1: Snippet Extraction

Read the newsletter and extract standalone snippets from each segment.

**From THOUGHT segment (contrarian take):**
- Core opinion (1-2 sentences)
- Why it matters
- Snippet type: `hot_take`

**From TREND segment (data/research):**
- Key stat or finding
- OpenEd interpretation
- Snippet type: `stat`

**From TOOL segment (practical advice):**
- Recommendation
- Why it helps
- Snippet type: `how_to`

**Output format:**
```markdown
## Extracted Snippets

### Snippet 1 (from THOUGHT)
**Type:** hot_take
**Content:** [1-2 sentence opinion]
**Context:** [why this matters]

### Snippet 2 (from TREND)
**Type:** stat
**Content:** [stat + interpretation]
**Source:** [if external]

### Snippet 3 (from TOOL)
**Type:** how_to
**Content:** [recommendation]
**Benefit:** [what it enables]
```

## Phase 2: Parallel Sub-Agents

For each snippet, spawn parallel platform sub-agents.

**Load for all sub-agents:**
1. TEMPLATE_INDEX.md (lightweight index)
2. opened-identity (brand voice)
3. ai-tells (hard blocks)

**Sub-agent prompt pattern:**

```
You are a [PLATFORM] content specialist for OpenEd.

SNIPPET: [extracted snippet]
TYPE: [hot_take|stat|how_to]

Match to 2-3 best templates from TEMPLATE_INDEX.md.
Generate draft options.
Apply voice constraints.
Return for selection.
```

**Platform-specific routing:**

| Snippet Type | LinkedIn | X | Instagram | Facebook |
|--------------|----------|---|-----------|----------|
| hot_take | Contrarian, Story | Paradox Hook, Binary | Quote card | Agree/Disagree |
| stat | Authority, Commentary | Commentary, Thread | Carousel | Question post |
| how_to | List, Tips | Thread | Carousel | Fill-blank |

## Phase 3: Quality Gate

Apply Lite Quality Loop (3-judge):
1. AI-Tell Judge (BLOCKING)
2. Voice Judge (BLOCKING)
3. Platform Judge (ADVISORY)

## Phase 4: Nearbound Check

Before finalizing, check if any people are mentioned:
1. Search Nearbound Pipeline/people/ for name
2. If found, add @handle to post
3. If not found, note for future profile creation

## Phase 5: Schedule

Output approved posts to Social_Scheduling.md or directly to GetLate.

**Expected output per newsletter:**
- 2-3 LinkedIn posts
- 2-3 X posts/threads
- 1-2 Instagram posts (with visual direction)
- 1-2 Facebook posts

**Total: 6-9 social posts from one newsletter**

---

## Quick Reference

### Snippet Type → Template Mapping

| Type | Best Templates |
|------|----------------|
| hot_take | Contrarian, Paradox Hook, Binary Framing, Call BS |
| stat | Authority, Commentary, Data Story |
| how_to | List, Thread, Tips, Do's/Don'ts |
| quote | Quote + Hot Take, Commentary |
| story | Transformation, Day-in-Life |

### Voice Constraints (Always Apply)

- NO correlatives
- NO AI-isms
- Hyphens with spaces
- Brand account voice

---

## Related Skills

- `text-content` - Full template library
- `quality-loop` - Quality gates
- `opened-daily-newsletter-writer` - Newsletter source
- `x-posting` - X/Twitter scheduling
