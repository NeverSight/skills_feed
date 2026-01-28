---
name: program-creation
description: Create training and nutrition programs. Activate when users want a workout routine, meal plan, or ask "what should I do?" for fitness goals.
---

# Program Creation

This skill creates evidence-based training and nutrition programs by synthesizing principles from the source books, with detail level adapted to user experience.

**Attribution**: All programming principles are derived from the domain skill source books. As an Amazon Associate I earn from qualifying purchases.

## Prerequisites

This skill orchestrates three domain skills. Ensure they are installed:

```bash
npx skills add borisghidaglia/science-based-lifter
```

If individual skills are missing, the program may be incomplete.

## When to Use This Skill

Activate when users:
- Want a training program or workout routine
- Want a nutrition plan or meal structure
- Ask "what should I do?" for fitness goals
- Request macro calculations or training splits
- Need a complete program (training + nutrition)

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
Before delivering programs:
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

Before creating any program, **first verify** the required skills are installed by checking these paths exist:
- `../israetel-training/`
- `../schoenfeld-hypertrophy/`
- `../rp-diet/`

If any are missing, tell the user: "This skill requires additional skills. Please run: `npx skills add borisghidaglia/science-based-lifter`" and stop.

Then read and apply principles from these files:

**Volume & Progression**:
- `../israetel-training/SKILL.md` - Volume landmarks (MEV to MRV range)
- `../israetel-training/references/02-overload.md` - Progressive overload methods

**Frequency & Recovery**:
- `../israetel-training/references/04-sra.md` - Frequency by muscle group
- `../israetel-training/references/03-fatigue-management.md` - Deload protocols

**Program Structure**:
- `../schoenfeld-hypertrophy/references/08-program-design.md` - Splits, exercise selection
- `../israetel-training/references/05-variation.md` - Exercise rotation

**Nutrition**:
- `../rp-diet/references/10-designing-your-diet.md` - 4-step diet design process
- `../rp-diet/references/09-nutritional-periodization.md` - Phase duration and rate limits
- `../rp-diet/references/03-macronutrients.md` - Macro ranges by goal

## Workflow

### Step 1: Understand Intent

Ask: "What are you looking for in a program? Tell me about your situation."

Don't jump to predefined questions. Let them share what matters first.

### Step 2: Gather Essentials

Based on their response, fill in gaps:
- Goal clarity
- Training history
- Practical constraints
- Preferences and past experiences

Use reference files as a guide, not a script.

### Step 3: Present Options

Before building, present:
- Recommended approach (split type, frequency, nutrition structure)
- Why you're recommending it (with source)
- Alternatives and trade-offs

Example: "Given your 5 days available and intermediate experience, I'd suggest either PPL (hitting everything 2x) or a 3 Full Body + 1 Upper + 1 Lower hybrid (4x frequency). PPL is more conventional; the hybrid gives slightly higher frequency. Which appeals to you?"

Ask: "Which direction feels right?"

### Step 4: Build & Explain

After agreement, create program with inline rationale:
- For each major decision, state what, why, and source
- Show volume per muscle group
- Show calorie/macro calculations

## Adaptive Detail Levels

Determine user's training age from `../israetel-training/references/07-individualization.md` and adjust accordingly:

### Beginners (0-2 years training)
- **Provide**: Detailed programs with specific exercises, sets, reps
- **Include**: Exercise demonstrations/cues, exact macro numbers
- **Rationale**: Need structure; can't yet self-regulate effectively

### Intermediates (2-5 years training)
- **Provide**: Structured frameworks with ranges
- **Include**: Volume targets, progression schemes, macro ranges
- **Rationale**: Can make micro-adjustments within structure

### Advanced (5+ years training)
- **Provide**: Strategic guidelines and principles
- **Include**: Periodization frameworks, autoregulation guidelines
- **Rationale**: Know their bodies; need concepts not prescriptions

## Output Formats

### Beginner Training Template
```
[Program Name] - [Days]/Week [Split Type]

Day 1: [Focus]
- Exercise 1: 3x8-12 @RPE 7-8
  *Why*: [reasoning] | *Source*: [book/chapter]
- Exercise 2: 3x10-15 @RPE 7-8
  *Why*: [reasoning] | *Source*: [book/chapter]
[etc.]

Weekly Volume Summary:
- Chest: X sets (MEV: Y, MAV: Z)
- Back: X sets (MEV: Y, MAV: Z)
[etc.]

Progression: Add weight when hitting top of rep range for all sets
Deload: Every 4-6 weeks, reduce volume 50%
```

### Beginner Nutrition Template
```
Daily Targets:
- Calories: [number]
  *Calculation*: [weight] × [multiplier] = [result] | *Source*: [book/chapter]
- Protein: [number]g
  *Calculation*: [g/lb] × [weight] = [result] | *Source*: [book/chapter]
- Carbs: [number]g
- Fat: [number]g

Meal Timing: [frequency] meals, protein distributed evenly
Training Days: Add [carbs] around workout
```

### Intermediate/Advanced Format
Provide ranges and guidelines rather than rigid prescriptions. Focus on:
- Volume targets per muscle group (with source)
- Progression principles (with source)
- Periodization structure (with source)
- Macro ranges with adjustment protocols (with source)

## Integration

If user hasn't completed an assessment, offer to run one first using the `assessment` skill for more personalized recommendations.

---

Sources:
- Scientific Principles of Hypertrophy Training by Dr. Mike Israetel et al. — https://www.amazon.com/Scientific-Principles-Hypertrophy-Training-Periodization/dp/B0924XX9P7?tag=borisfyi0f-20
- Science and Development of Muscle Hypertrophy by Brad Schoenfeld — https://www.amazon.com/dp/1718210868?tag=borisfyi0f-20
- The Renaissance Diet 2.0 by Dr. Mike Israetel et al. — https://www.amazon.com/dp/1782551905/?tag=borisfyi0f-20
