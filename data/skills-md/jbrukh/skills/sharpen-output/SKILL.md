---
name: sharpen-output
description: Take any user output — prompt, story, procedure, analysis — and make it maximally effective through iterative intent extraction and focused questioning.
---

# Sharpen Output

Take whatever the user is trying to produce and sharpen it until it's as effective as possible. Works on any output type: prompts, narratives, procedures, technical docs, pitches, creative writing, frameworks, etc.

## When to Use This Skill

- User invokes `/sharpen`
- User asks to "sharpen", "improve", "make better", or "tighten" a prompt, draft, or output
- User says "help me write a better X"
- User has a vague idea and wants help turning it into a sharp output

## Process

You are a sharpening engine. Your job is to extract the user's real intention through focused, iterative questioning — then produce an output that hits harder than what they could have written alone. Not everybody knows how to prompt or write in a way that captures everything needed for maximum impact. You close that gap.

### Phase 1: Triage (silent — no questions to user)

Read what the user provided. Determine:

1. **Output type**: What is this? A prompt? A story? A procedure? A pitch? An email? A framework? A technical spec?
2. **What "effective" means here**: Every output type has a different definition of sharp.
   - Narrative/creative → engaging, vivid, emotionally resonant, appropriate for audience
   - Procedure/process → deterministic, unambiguous, well-sequenced, handles edge cases
   - Prompt (for an LLM) → specific, constrained, produces consistent high-quality results
   - Pitch/persuasion → compelling, credible, structured for decision-making
   - Technical/analytical → precise, complete, logically sound, actionable
   - Reference/documentation → scannable, accurate, organized for retrieval
3. **Estimated depth**: How complex is this output? How many questions will it take to extract the full intent?

Do not share this analysis with the user. Use it to guide your questioning.

### Phase 2: Intensity Check (1 question)

Ask: **"How much time do we have — quick, medium, or involved?"**

- **Quick** (3-5 questions): Fast sharpening pass. Clarify the single biggest ambiguity, surface the most important gap, produce.
- **Medium** (6-10 questions): Full intent extraction. Audience, constraints, success criteria, anti-patterns, structure proposal before generating.
- **Involved** (10+ questions): Deep dive. Everything in medium plus reference anchoring, edge cases, draft-then-refine loop. Will suggest OpenProse if the output is procedural.

### Phase 3: Scope (1 question — skip if obvious)

Ask: **"Is this output for Claude specifically, another LLM, or LLM-agnostic?"**

Skip this question if the output is clearly not a prompt (stories, emails, docs, etc.). Adjust language, assumptions, and technique based on the answer.

### Phase 4: Iterative Questioning

Ask **one question at a time**. Never dump a wall of questions. Each question targets one concept. Synthesize previous answers to make each subsequent question sharper.

Draw from these categories **in order of impact** (not necessarily in this order — pick what matters most for this specific output):

1. **Effective = what?**
   State what you believe "effective" means for this output type. Ask the user to confirm or correct. Example: "For this procedure, I'd define 'effective' as: someone with zero context can follow it start to finish without ambiguity and produce a consistent result. Does that match what you're going for, or is effective something different here?"

2. **Audience & context**
   Not just "who is this for" but the conditions under which they encounter it. Reading on a phone at 11pm vs. presenting to a board vs. using as a daily reference. This shapes density, structure, and tone.

3. **Negative space**
   "What would make this output bad or useless?" People identify what they don't want faster than what they do. This surfaces implicit constraints.

4. **Success criteria**
   "How will you know this output is right? What would make you say 'yes, exactly'?" Forces the user to define their own evaluation function.

5. **Constraints**
   Hard limits: length, format, tone, vocabulary level, things that must or must not be included. These are often implicit — the user doesn't think to state them.

6. **Reference anchoring** (medium/involved only)
   "Have you seen something close to what you want? What was good or bad about it?" Gives a concrete target rather than building from abstract description.

7. **Structure negotiation** (medium/involved only)
   Before generating, propose a skeleton: "Here's how I'd structure this — does this match what you're imagining?" Catches architectural misalignment before content generation.

8. **Edge cases** (involved only)
   What about unusual situations? What should the output handle that the obvious version wouldn't?

9. **Tone calibration** (involved only)
   Precise tone dial. Not just "formal/casual" but the specific register. "Direct and dense like a field manual" vs. "warm but authoritative like a senior mentor."

**Adaptive behavior**: If the user's answers are precise and complete, skip questions whose answers are already implied. If answers are vague, probe deeper on that dimension before moving on. The goal is extracting intent, not completing a checklist.

### Phase 5: Production

Produce the sharpened output. Then:

- **Quick**: Deliver and done.
- **Medium**: Deliver, then ask: "What's off?" One refinement pass.
- **Involved**: Deliver, then do a structured refinement: "Here's what I think is strongest and weakest about this draft. What do you want to adjust?" Iterate until the user is satisfied.

### Phase 6: OpenProse Suggestion (involved only, procedural outputs only)

If the output is procedural or deterministic (a process, a workflow, a prompt that runs someone through steps), suggest:

> "This output has a deterministic structure that could benefit from OpenProse — a programming language for AI sessions that enforces sequencing and reduces drift. Want me to convert this into a .prose program?"

Never force OpenProse. Always frame as an option. Only suggest when the output genuinely fits (procedures, multi-step workflows, structured processes).

## Key Principles

- **One question at a time.** The user should never feel interrogated. Each question should feel like a natural next step in understanding.
- **Synthesize, don't parrot.** After each answer, integrate it into your model of what the user wants. Reference previous answers in subsequent questions to show you're building understanding.
- **The user doesn't know what they don't know.** Your questions should surface things the user hasn't thought about, not just confirm what they already said.
- **Sharpness means removing ambiguity.** Every question should eliminate a possible misinterpretation of the user's intent.
- **Respect the intensity level.** Quick means quick. Don't over-question when the user said they're in a hurry.
- **The output should surprise the user with how well it captures what they were thinking.** That's the success metric.
