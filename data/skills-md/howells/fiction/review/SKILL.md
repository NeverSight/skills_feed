---
name: review
description: Review chapters for coherence, cheesiness, consistency, pace, tone, and character. Suggests specific rewrites.
argument-hint: "[chapter] [all] [3-7]"
---

Review chapters using the chapter-reviewer agent.

## What This Does

1. Identifies the chapter(s) to review
2. Gathers necessary context (character docs, previous chapter, project tone)
3. Runs a thorough review checking:
   - Coherence
   - Cheesiness
   - Consistency
   - Pace
   - Tone
   - Character voice
4. Provides specific feedback with suggested rewrites
5. Offers to apply rewrites and output revised chapter

## Usage

```
/fiction:review                    # Review most recent chapter
/fiction:review 5                  # Review chapter 5
/fiction:review all                # Review all drafted chapters
/fiction:review 3-7                # Review chapters 3 through 7
/fiction:review chapters/08.md     # Review specific file
```

If arguments provided: $ARGUMENTS

## Parallel Processing (Important for Large Manuscripts)

When reviewing multiple chapters ("all" or a range), **spawn chapter-reviewer agents in parallel** for efficiency:

1. Identify all chapters to review
2. Load shared context once (character docs, tone guide, project README)
3. Launch one chapter-reviewer agent per chapter using the Task tool
4. Pass shared context + specific chapter + previous chapter to each agent
5. Each agent reviews independently, produces verdict + issues
6. Aggregate results: compile verdicts, flag cross-chapter patterns
7. Update `progress.md` with all review results

**Example parallel approach for `/fiction:review all` with 20 chapters:**
- Spawn 20 chapter-reviewer agents in a single message
- Each receives: its chapter, previous chapter (for continuity), shared context
- Agents run concurrently
- Main conversation aggregates verdicts and highlights patterns
- Total time ~ time for 1-2 chapters instead of 20x

## How It Works (Single Chapter)

If no chapter is specified:
1. Check conversation history for recently written/discussed chapter
2. Or find the most recently modified chapter file in the project
3. Or ask the user which chapter to review

The review includes:
- What works (with specific quotes)
- What needs work (with suggested rewrites)
- Continuity flags
- Verdict (ready to move on / needs revision)

## After Review

If issues are found, you'll be asked: "Would you like me to apply these rewrites and output the revised chapter?"

Say yes to get the complete revised chapter with all changes applied.
