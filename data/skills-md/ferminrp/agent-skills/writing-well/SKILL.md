---
name: writing-well
description: >
  Audit and improve user-provided writing for clarity, concision, and impact.
  Use when the user asks to audit, review, improve, edit, or rewrite text.
  Apply seven checks (sentence length, clutter, unsupported modifiers, weasel
  words, jargon/acronyms, "so what", and flow), then return severity-ranked
  findings and a full rewrite suggestion.
---

# writing-well

## When to Use This Skill

Use this skill when:

- The user asks to "audit", "review", "improve", "edit", or "rewrite" text.
- The user shares writing and asks for feedback on clarity or impact.
- The user mentions this skill directly (`writing-well` or `writing audit`).

## Workflow

Run all 7 checks in order. For each finding:

- Quote the exact offending text.
- Explain why it is weak.
- Propose a tighter rewrite.

### Check 1: Sentence Length (max 30 words)

Flag sentences longer than 30 words.

Action: Split or tighten so each sentence carries one idea.

### Check 2: Clutter Phrases

Replace wordy phrases with simpler forms.

| Cluttered phrase | Replace with |
|---|---|
| with the possible exception of | except |
| due to the fact that | because |
| totally lacked the ability to | could not |
| until such time as | until |
| for the purpose of | for |
| in order to | to |
| it is important to note that | delete or rephrase |
| at the end of the day | delete or rephrase |
| in terms of | rephrase |
| a large number of | many |
| in the event that | if |
| at this point in time | now |
| has the ability to | can |
| on a daily basis | daily |
| the vast majority of | most |

Also flag any phrase where one word can do the same job.

### Check 3: Unsupported Adjectives/Adverbs

Flag subjective modifiers without evidence.

Examples:

- "Sales increased significantly in Q4" -> "Unit sales increased 40% in Q4 2024 vs Q4 2023"
- "We made the application much faster" -> "We reduced server-side p90 latency from 10 ms to 1 ms"
- "This will be extremely successful" -> "This will increase output by 2.5%"

Common words to flag: significantly, substantially, greatly, very, extremely, considerably, remarkably, tremendously, much, quite, really, incredibly, fairly, pretty (as adverb), a lot.

Action: Ask for a number; if none is available, remove or soften the claim.

### Check 4: Weasel Words

Flag non-committal language: would, might, should, could, arguably, nearly, practically, virtually, somewhat, relatively, potentially.

Action: Replace with a concrete commitment, specific number, or explicit uncertainty ("I don't know yet, and I will follow up").

### Check 5: Jargon, Acronyms, Accessibility

- Flag jargon not defined for non-experts.
- Expand acronyms on first use, e.g., "Non-Disclosure Agreement (NDA)".

Action: Define once, then use the short form.

### Check 6: "So What?" Test

For each paragraph, ask if the reader immediately sees relevance.

Action: Add implication, consequence, or numeric impact.

### Check 7: Flow and Rhythm

Check whether the text sounds natural when read aloud.

Flag:

- Repeated words/phrases in nearby sentences.
- Clunky sentences that signal unclear thinking.
- Monotonous sentence length/patterns.
- Ideas presented in an unnatural order.

Action: Reorder ideas and vary sentence rhythm to match idea complexity.

## Response Format

Use this structure:

```markdown
## Writing Audit Report

### Summary
[1-2 sentence assessment of strengths and top improvement area]

### Score: X/10
[Score based on how many checks pass cleanly]

### Findings

#### Critical
[Issues that severely hurt clarity or accuracy]

#### Important
[Issues that materially reduce quality]

#### Minor / Polish
[Flow and wording refinements]

### Rewrite Suggestion
[Full rewrite preserving intent and voice]
```

## Direct-Answer Rule

When text asks a question, prefer one of these forms:

1. Yes.
2. No.
3. A number.
4. I don't know (and will follow up).

## Principles

- Clarity is kindness.
- Data beats adjectives.
- If it sounds wrong, it is probably wrong.
- Keep subject-verb-object unless complexity demands otherwise.
- Respect the reader's time.
