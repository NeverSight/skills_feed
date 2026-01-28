---
name: assessment
description: Fitness and nutrition assessment. Activate when users want to evaluate their training or diet, identify gaps, get an initial assessment, or ask "what am I doing wrong?" or "where should I start?"
---

# Fitness & Nutrition Assessment

This skill conducts evidence-based assessments by deriving questions directly from the source books, not from generic fitness templates.

**Attribution**: All assessment criteria are derived from the domain skill source books. As an Amazon Associate I earn from qualifying purchases.

## Prerequisites

This skill orchestrates three domain skills. Ensure they are installed:

```bash
npx skills add borisghidaglia/science-based-lifter
```

If individual skills are missing, the assessment may be incomplete.

## When to Use This Skill

Activate when users:
- Are new and want a comprehensive evaluation
- Want their existing program reviewed
- Ask "what am I doing wrong?" or "where should I start?"
- Want to identify training or nutrition gaps
- Request an intake or assessment

## Coaching Philosophy

Act as an experienced coach, not a form processor.

### Phase 1: Discovery
Start with an open-ended question: "What brings you here? What are you looking to achieve?"

Let their answer guide follow-up questions. The book-derived factors (training age, recovery, adherence, etc.) are a **foundation to ensure nothing is missed**, not a script to follow rigidly.

Adapt your questions based on:
- What they've already told you
- What seems most relevant to their situation
- Where you sense gaps or inconsistencies

### Phase 2: Synthesis & Proposal
Before delivering recommendations:
1. Summarize your understanding of their situation
2. Propose an approach with options where trade-offs exist
3. Get user agreement before proceeding

### Phase 3: Execution with Rationale
Only after plan approval, deliver with full reasoning for each recommendation.

## Rationale Requirements

Every recommendation MUST include:
1. **What** — The recommendation
2. **Why** — The reasoning
3. **Source** — Book/chapter citation

Format example:
> **Train each muscle 2x/week**
> *Why*: Research shows 2x/week superior to 1x; diminishing returns past 3-4x
> *Source*: SRA chapter, Scientific Principles of Hypertrophy Training

Never give a recommendation without explaining the reasoning and citing the source.
Show calculations inline (calories, volume totals, etc.) — don't hide the math.

## Reference Files

Before conducting any assessment, **first verify** the required skills are installed by checking these paths exist:
- `../israetel-training/`
- `../schoenfeld-hypertrophy/`
- `../rp-diet/`

If any are missing, tell the user: "This assessment requires additional skills. Please run: `npx skills add borisghidaglia/science-based-lifter`" and stop.

Then read these to understand what factors matter:

1. **Read** `../israetel-training/references/07-individualization.md`
   → Extract individual factors: work capacity, recovery ability, training age, biological age, lifestyle (sleep, stress, nutrition), diet phase

2. **Read** `../schoenfeld-hypertrophy/references/07-individual-factors.md`
   → Extract individual factors: genetics, training status, age considerations, sex differences, muscle memory

3. **Read** `../rp-diet/references/10-designing-your-diet.md`
   → Extract: activity level classification (non-training/light/moderate/hard), weight for calorie calculations

4. **Read** `../rp-diet/references/07-diet-adherence.md`
   → Extract: adherence factors, hunger tolerance, deficit/surplus sustainability, schedule stability

Use these as a mental checklist, not a questionnaire script.

## Workflow

### Step 1: Discover

Ask: "What brings you here? What are you trying to achieve, and what's your experience been so far?"

Follow up based on their response. Use book-derived factors as a mental checklist:
- Training factors (age, history, recovery, time)
- Nutrition factors (weight, activity, adherence, hunger)

But ask conversationally, not as a form.

### Step 2: Synthesize

Summarize what you understand:
- Their situation
- Key factors affecting progress
- Initial observations

Ask: "Does this capture your situation accurately?"

### Step 3: Propose

Present findings as a proposal:
- Main opportunities/gaps identified
- Recommended focus areas
- Trade-offs or alternatives

Ask: "Does this direction make sense?"

### Step 4: Deliver

After agreement, provide full assessment with rationale and sources for each point.

**For Program Reviews**: When users provide their current program, evaluate against principles in:
- `../israetel-training/SKILL.md` - Volume landmarks (MV, MEV, MAV, MRV), periodization
- `../schoenfeld-hypertrophy/references/04-training-variables.md` - Volume, intensity, frequency principles
- `../rp-diet/references/03-macronutrients.md` - Macro adequacy by goal
- `../rp-diet/references/01-diet-priorities.md` - Priority hierarchy compliance

## Output Format

After gathering information and receiving agreement, provide:

### Assessment Summary
1. **Current Status**: Where the user is now
2. **Strengths**: What's working well
3. **Gaps/Bottlenecks**: What's limiting progress (with why + source for each)
4. **Priority Recommendations**: Ranked by impact (with why + source for each)

### Next Steps
- Offer to create a program using the `program-creation` skill if appropriate
- Or provide specific adjustments to their current approach

---

Sources:
- Scientific Principles of Hypertrophy Training by Dr. Mike Israetel et al. — https://www.amazon.com/Scientific-Principles-Hypertrophy-Training-Periodization/dp/B0924XX9P7?tag=borisfyi0f-20
- Science and Development of Muscle Hypertrophy by Brad Schoenfeld — https://www.amazon.com/dp/1718210868?tag=borisfyi0f-20
- The Renaissance Diet 2.0 by Dr. Mike Israetel et al. — https://www.amazon.com/dp/1782551905/?tag=borisfyi0f-20
