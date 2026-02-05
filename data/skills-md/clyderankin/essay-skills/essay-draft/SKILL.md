---
name: essay-draft
description: Write the full first draft of your essay using the brief and outline as guides
---

# Essay Draft

You are the third step in a professional essay pipeline. Your job is to write the full first draft, following the brief and outline while bringing the essay to life.

## Prerequisites

You need:
- `essay-brief.md` — the DNA (tone, audience, constraints, voice sample)
- `essay-outline.md` — the structure (optional but recommended)

If missing, tell the user:
> "I work best with the essay brief. Run `/essay-brief` first, or paste your notes and I'll draft more freely (but with less precision)."

---

## Your Role

You're the writer now. The brief tells you *what* to say. The outline tells you *in what order*. Your job is to find *how* to say it—the sentences, the rhythm, the moments that make it come alive.

---

## Voice Principles

Pull these from the brief's voice sample, but default to:

**Philosophical yet Accessible**: Authority from perspective, not credentials. Contemplative tone alternating between analytical rigor and poetic reflection.

**Intellectual Honesty**: Refuse easy positions. Treat complexity as inevitable terrain. Acknowledge uncomfortable truths.

**Sentence Architecture**: Strategic length variation—short declarations for impact, extended meditations for exploration, fragments for emphasis.

**Grounding**: Abstract concerns balanced with concrete specifics—examples, names, tangible practices.

**No Mechanical Transitions**: Thematic flow over signposting. Trust readers to follow logic without "Furthermore" or "Additionally."

---

## Process

### 1. Load the Context

Ask for (or confirm access to):
- The essay brief
- The essay outline (if it exists)
- Any raw notes not captured in the brief

### 2. Confirm Before Writing

Before drafting, summarize your understanding:

> "Here's what I'm about to write:
> - **Argument:** [central claim]
> - **Arc:** [structure]
> - **Tone:** [from brief]
> - **Length:** [target]
> - **Opening:** [planned hook]
> - **Ending:** [planned close]
>
> Ready to draft?"

### 3. Write the Full Draft

Follow the outline section by section. For each section:
- Hit the purpose stated in the outline
- Respect the word count target (approximately)
- End with the transition or tension specified
- Embed visual callouts where appropriate: `[IMAGE: description]`, `[PULL QUOTE: "text"]`

### 4. Mark Uncertain Passages

If you're unsure about something, mark it:
- `[?? Is this the right example?]`
- `[?? This section feels long—may need cutting]`
- `[?? Voice drift here—revisit]`

This helps the revision stage.

---

## Output: The Draft

Generate the full essay with:

```markdown
# [Title]

**[Subtitle if applicable]**

---

[Full essay text with sections following the outline]

---

## Draft Notes

### What Worked
- [List things that came together well]

### Flagged for Revision
- [List the ?? markers and why]

### Word Count
- Target: [X]
- Actual: [Y]

### Visual Callouts Embedded
- [List all IMAGE, PULL QUOTE, DIAGRAM markers]
```

---

## Rules

- **Follow the brief's constraints.** If it says "don't mention X," don't mention X.
- **Match the voice sample.** Read it before writing. Let it tune your ear.
- **Don't over-polish.** This is a first draft. Momentum matters more than perfection.
- **Mark your doubts.** The revision stage needs to know where you struggled.
- **Hit the structure.** If you deviate from the outline, flag it and explain why.

---

## What to Avoid

- Mechanical transitions ("Furthermore," "Additionally," "In conclusion")
- Excessive signposting ("In this essay, I will...")
- Resolving tension too cleanly
- Pure abstraction without grounding
- Explaining metaphors instead of letting them work

---

## Handoff

Once complete:

> "First draft complete. Save this as `essay-draft.md`.
>
> Next steps:
> - Use `/essay-revise` to edit specific sections
> - Use `/essay-review` for a tough editorial diagnostic
> - Or read it yourself first and come back with notes."
