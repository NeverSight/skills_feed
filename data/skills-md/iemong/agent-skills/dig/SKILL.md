---
name: dig
description: |
  Clarify ambiguities in plans with structured questions using the AskUserQuestion tool.
  使用タイミング: (1) 計画の曖昧な点を明確にしたい (2) 実装前に要件を詰めたい
  トリガーキーワード: 曖昧、不明確、要件確認、dig
metadata:
  version: "2.0.0"
allowed-tools: Write Edit Read Grep Glob TodoRead TodoWrite AskUserQuestion
---

# Dig - Plan Clarification Skill

Read the current plan file and interview me in detail using the AskUserQuestion tool about literally anything.
- Product Spec
- Technical detail
- UI/UX
- and anything

## Phases

1. Clarify unclear point
2. Ask user question for make decision
3. Apply decision to plan
4. Show the summary for user

Should be very in-depth and continue digging me until complete all of unclear point, then you will write the spec to the plan file.
After phase 3, you revisit to the plan file, and analyze them, you must to rise the unclear point with moving to phase 2.

### Phase 2: Generate Questions

<rules>
- Question count: **2-4** (adjust based on ambiguity level)
- Each question has **2-4 concrete options**
- Each option includes **pros/cons** briefly
- Avoid open-ended questions
- "Other" option is auto-added - don't include it
- Align options with existing patterns from CLAUDE.md (if available)
</rules>

### Phase 3: Post-Answer Processing

<output_format>
After receiving user answers, output:

## Decisions

| Item | Choice | Reason | Notes |
|------|--------|--------|-------|
| Data storage | Database | Scalability needs | Consider migration strategy |

## Next Steps

1. **First task**
   - Details...
2. **Second task**
   - Details...
</output_format>

---

## Important Notes

- **Must use AskUserQuestion tool** - Not conversational questions
- Each option must include **pros/cons**
- Use multiSelect sparingly (default: false)
- Read CLAUDE.md before generating questions to align with project patterns
