---
name: story-explanation
context: fork
model: sonnet
description: Create compelling story-format summaries using UltraThink to find the best narrative framing. Support multiple formats - 3-part narrative, n-length with inline links, abridged 5-line, or comprehensive. USE WHEN user says 'create story explanation', 'narrative summary', 'explain as a story', or wants content in Daniel's conversational first-person voice.
---

# Story Explanation - Narrative Summary with Creative Analysis

## 🎯 Load Full PAI Context

**Before starting any task with this skill, load complete PAI context:**

`read ${PAI_DIR}/skills/CORE/SKILL.md`

## Core Philosophy

**Standard approach:** Generate a generic summary of content.

**This skill:** Use UltraThink to analyze multiple narrative framings, then select the BEST one and present it in a compelling story format.

Based on:
- **UltraThink**: Deep content understanding across multiple perspectives and narrative angles
- **Best framing selection**: Choose the most compelling narrative angle from multiple options
- **Daniel Miessler voice**: First person, casual, direct, genuinely curious

**The Problem This Solves:**
- Generic summaries use obvious framing without exploring alternatives
- Mode collapse causes formulaic story explanations
- Best narrative angles get missed in favor of first-thought approaches
- Content needs to be explained in conversational, engaging way

## When to Activate This Skill

- User requests story explanations or narrative summaries
- User says "create a story explanation" or "explain this as a story"
- User says "narrative summary", "tell as story", or "explain in narrative"
- User wants content explained in conversational, engaging format
- Need to find the most compelling narrative hook for content
- User explicitly requests this skill
- Want to present content in Daniel's voice
- Format-specific requests: "story with links", "abridged story", "5-line summary", "CSE", "CSE5"
- Slash commands: `/create-story-explanation`, `/cse`, `/cse5`

**DO NOT use this skill when:**
- User wants comprehensive extraction (use research skill with fabric)
- User wants quick technical summary
- Speed matters more than narrative quality

## 🔀 Workflow Routing

This skill contains multiple workflows for different story explanation formats:

### Available Workflows:

1. **`workflows/create.md`** - Main 3-part narrative (default)
   - **Use when:** User wants standard story explanation format
   - **Triggers:** "create story explanation", "story explanation", default workflow
   - **Output:** 3-part format (opening 15-25 words → body 5-15 sentences → closing 15-25 words)

2. **`workflows/create-with-links.md`** - N-length format with inline source links
   - **Use when:** User wants comprehensive narrative with source attribution
   - **Triggers:** "story explanation with links", "narrative with sources", "with inline citations"
   - **Output:** N sentences (default 25) with inline links after each sentence

3. **`workflows/create-abridged.md`** - Ultra-concise 5-line format (5-12 words per line)
   - **Use when:** User wants abbreviated format from URL, YouTube, or text
   - **Triggers:** "create abridged story explanation", "5-line summary", command: `/create-abridged-story-explanation`
   - **Output:** 5 lines with strict word limits

4. **`workflows/cse.md`** - Comprehensive explanation
   - **Use when:** User wants detailed narrative explanation
   - **Triggers:** "run CSE", "explain this story", command: `/cse`
   - **Output:** Complete narrative explanation

5. **`workflows/cse5.md`** - Clean 5-line numbered format
   - **Use when:** User wants scannable, numbered breakdown
   - **Triggers:** "explain in 5 lines", "CSE5", command: `/cse5`
   - **Output:** 5 numbered lines, one concept per line

### Routing Decision Tree:

```
User request → Analyze intent:

├─ "with links" OR "inline sources" OR "with citations"
│  └─> workflows/create-with-links.md (N-length format with inline links)
│
├─ "abridged" OR "5-12 words per line"
│  └─> workflows/create-abridged.md
│
├─ "CSE5" OR "5 lines" OR "numbered"
│  └─> workflows/cse5.md
│
├─ "CSE" OR "comprehensive explanation"
│  └─> workflows/cse.md
│
└─ Default OR "story explanation"
   └─> workflows/create.md (3-part narrative)
```

### Command Routing:
- `/create-story-explanation` → `workflows/create.md`
- `/create-story-output-links` → `workflows/create-with-links.md`
- `/create-abridged-story-explanation` → `workflows/create-abridged.md`
- `/cse` → `workflows/cse.md`
- `/cse5` → `workflows/cse5.md`

## 📁 File Organization

**Working Directory:** `${PAI_DIR}/scratchpad/${CLAUDE_SESSION_ID}/story-explanation-[topic]/`

**Full details:** `references/file-organization.md`

## The Four-Step Process

### Step 1: Content Extraction

**For YouTube videos:**
```bash
fabric -y "YOUTUBE_URL"
```

**For URLs/articles:**
```typescript
WebFetch(url, "Extract full content of this article")
```

**For other content:**
- Paste text directly
- Read from files

### Step 2: Activate Be Creative Skill

**Load the be-creative skill for deep reasoning enhancement:**

This provides access to:
- **UltraThink**: Deep reasoning and quality analysis
- Enhanced techniques for finding the best narrative framing

### Step 3: Deep UltraThink Analysis (via Be Creative)

Before generating story explanation, engage in extended deep thinking:

**UltraThink Protocol:**
```
ULTRATHINK DEEP STORY ANALYSIS MODE:

Think deeply and extensively about this content:

1. CORE NARRATIVE - What's the fundamental story being told?
2. MULTIPLE FRAMINGS - What are 5-7 different ways to frame this story?
3. AUDIENCE ANGLES - How would different audiences understand this?
4. HOOK VARIETY - What are compelling but different entry points?
5. EMPHASIS OPTIONS - Which elements could be emphasized or de-emphasized?
6. STRUCTURAL APPROACHES - Chronological? Problem-solution? Comparison?
7. IMPACT FOCUS - What's the "wow" factor that makes this significant?
8. CONVERSATIONAL FLOW - How would Daniel explain this to a friend?
9. KEY INSIGHTS - What makes readers think "I get it now!"?
10. BEST FRAMING - Which narrative angle is most compelling?

Allow thinking to explore multiple narrative approaches.
Question assumptions about the "obvious" way to tell this story.
Look for the framing that would make readers stop and engage.
Consider: What would make someone excited to share this?
```

### Step 4: Multiple Framings + Best Selection (via UltraThink)

Use UltraThink to explore different framings, then select the BEST one:

**Framing Exploration Protocol:**
```
STEP 1 - GENERATE MULTIPLE FRAMINGS:
Generate 5 different narrative framings from your deep analysis,
exploring diverse approaches and perspectives.

For each framing option:
- Different hook/entry point
- Different emphasis on key elements
- Different structural approach
- Different "wow" factor

Explore creative and non-obvious narrative framings.
Avoid formulaic approaches.

STEP 2 - SELECT BEST FRAMING:
Choose the single most compelling narrative framing that:
- Has the strongest hook
- Best captures the "wow" factor
- Would make Daniel most excited to share
- Feels most natural in his voice
- Makes complex ideas accessible

STEP 3 - OUTPUT IN SELECTED FORMAT:
Use the selected framing to create the story explanation in the appropriate format.
```

## Output Formats & Voice

**Full guide:** `references/voice-style-guide.md`

**Key points:**
- **3-Part Narrative:** Opening (15-25 words) → Body (5-15 sentences) → Closing (15-25 words)
- **N-Length with Links:** User-specified sentences with inline source attribution
- **Daniel's Voice:** First person, casual, direct, genuinely curious
- **Avoid:** Cliches ("game-changer", "paradigm shift"), journalistic tone, extrapolation

## Comparison to Other Approaches

**/cse5 (single story explanation):**
- Fast, single output
- Quick technical summary
- No creative analysis

**research skill (insight extraction):**
- Comprehensive analysis and extraction
- Multiple perspectives and sources
- Analytical, not narrative format

**story-explanation (this skill):**
- Single BEST story explanation in chosen format
- Uses be-creative skill (UltraThink)
- Deep reasoning to explore and find best framing
- Daniel Miessler voice (first person, casual, direct)
- Explores multiple narrative angles, selects most compelling
- Specifically designed for engaging storytelling
- Prioritizes conversational flow and "wow" factor

## Integration with Qara

When this skill activates, Qara should:

1. **Determine format** - Based on user request, select appropriate workflow
2. **Create scratchpad directory** - `${PAI_DIR}/scratchpad/${CLAUDE_SESSION_ID}/story-explanation-[topic]/`
3. **Load be-creative skill** - Activate research-backed creativity framework
4. **Load content** via appropriate method (fabric -y, WebFetch, Read, or paste)
5. **Save raw content to scratchpad** - Store extracted content for reference
6. **Engage UltraThink mode** - Deep analysis across 10 narrative dimensions
7. **Save UltraThink notes to scratchpad** - Document narrative analysis process
8. **Explore multiple framings** - Use UltraThink to generate 5 different narrative framings
9. **Save framing explorations to scratchpad** - Document all 5+ framings considered
10. **Select best framing** - Choose the most compelling narrative angle
11. **Output in selected format** - 3-part, n-length with links, abridged, or Foundry format
12. **Save final output to scratchpad** - Store completed story explanation
13. **Use Daniel's voice** - First person, casual, direct, genuinely curious
14. **Optionally archive to history** - Only if analysis methodology is exceptionally valuable for future reference

**Critical:** The be-creative skill provides UltraThink framework ensuring we explore creative narrative framings that would otherwise be missed due to mode collapse, then select the single BEST one.

**File Organization:**
- All working files go to scratchpad (content, analysis, drafts, final output)
- Only exceptional analytical insights go to history
- Most story explanations are one-off outputs and remain in scratchpad

## Key Principles

1. **Use be-creative skill** - UltraThink framework for deep reasoning in exploring framings
2. **Think narratively first** - UltraThink about story possibilities before output
3. **Explore diverse framings** - Generate multiple creative narrative framings through deep analysis
4. **Select best framing** - Choose the most compelling narrative angle
5. **Format flexibility** - Multiple output formats for different use cases
6. **Daniel's voice** - First person, casual, direct, genuinely curious
7. **Conversational flow** - Vary sentence length (8-16 words), natural rhythm
8. **Avoid cliches** - No "game-changer", "paradigm shift", "revolutionary", etc.
9. **Stick to facts** - Don't extrapolate beyond the input
10. **Deliver "wow" factor** - Make significance clear without hyperbole

## Quality Guidelines

**See:** `references/voice-style-guide.md` for failure modes and success criteria.

**Quick check:** Does it read naturally spoken aloud? Does it feel like Daniel sharing something interesting with a friend?

## Quick Reference

**Four-step process:**
1. Activate be-creative skill (UltraThink)
2. Extract content (fabric -y, WebFetch, Read, paste)
3. Deep UltraThink (10-dimension narrative analysis)
4. Explore multiple framings (5 different narrative approaches) → Select BEST → Output in selected format

**Format selection:**
- Default: 3-part narrative (opening/body/closing)
- With links: N-length with inline source attribution
- Abridged: Ultra-concise 5-line format
- CSE/CSE5: comprehensive formats

**Voice:**
- First person (Daniel's perspective)
- Casual, direct, genuinely curious
- Natural conversational tone (like telling a friend)
- NO cliches, journalistic language, or flowery tone

**Remember:**
- Use be-creative skill for UltraThink deep reasoning
- Think deeply about narrative possibilities (UltraThink)
- Explore diverse framings to find the best narrative angle
- Select the single most compelling narrative angle
- Stick to facts - don't extrapolate beyond the input
- Deliver "wow" factor without hyperbole

## Relationship to Other Skills

**Works well with:**
- `research` - Deep insights extraction from same content (analytical complement)
- `social` - Turn story explanation into social media posts
- `writing` - Use story explanation as blog post draft or inspiration
- `media` - Generate hero image for the story explanation

**Use research skill instead when:**
- User wants comprehensive analysis with multiple sources
- Focus is on novel ideas and insights, not narrative storytelling
- Analytical extraction preferred over conversational explanation

---

**This skill provides compelling narrative explanations in Daniel's voice using research-backed creativity techniques to find the BEST framing from multiple possibilities.**
