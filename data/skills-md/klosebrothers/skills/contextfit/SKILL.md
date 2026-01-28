---
name: contextfit
description: >
  Guides users to a clear desired outcome, gathers focused context via MCQs,
  and derives concrete solution options and ready-to-use results.
version: 1.2.0
author: daw
---

# ContextFit

## Purpose

ContextFit helps you achieve **high-quality AI outputs quickly** without writing large prompts.
Instead, it first clarifies the desired outcome, then sharpens decisions through
**multiple-choice questions**, and finally produces **concrete solution options**
and fully worked results.

Core idea:

**Desired Outcome → Context Decisions → Solution Options → Final Results**

---

## Workflow

### Phase 0 — Clarify the Desired Outcome (lightweight)

Start every session with **one short, open question**:

> **What do you want to have at the end of this session?**  
> (e.g. “an actionable plan”, “a decision memo”,  
> “working code”, “a clear structure”, “several solution options to choose from”)

The goal is **not perfection**, but:
- clarity about the **type of artifact**
- a rough sense of **scope and depth**

If the answer is very vague:
- ask **one short follow-up** to sharpen it
- then move on

---

### Phase 1 — Derive the Goal

Translate the desired outcome into a clear goal:

- **Goal:** Why does this outcome matter?  
  What decision, action, or impact should it enable?

(1–2 short sentences)

---

### Phase 2 — Gather Context via MCQ Interview (5–10 questions)

Ask **5–10 multiple-choice questions**, each with **3–4 options**.

**Rules:**
- No open-ended questions
- Each question must force a decision
- Answers are letters only

**Accepted answer formats (show this to the user):**

```
A, C, B, A
```

or

```
1A 2C 3B 4A
```

---

### Phase 3 — Propose Solution Options and Let the User Choose

Use the goal and MCQ answers to propose **1–4 clearly distinct solution options**.

For each option include:
- a short title
- 2–4 bullet points explaining:
  - the core idea
  - focus and trade-offs
  - when this option is a good fit

Example structure:

- **Option A – Fast & Pragmatic**
- **Option B – Clean & Scalable**
- **Option C – Exploratory / Experimental**

Then ask:

> **Please select one or more options (e.g. A or A+C).**

---

### Phase 5 — Make a detailed plan for each selected option

Ask the user if he wants a detailed plan your will follow for each option or only on of those options.

For each selected option:
- if a file reference (documents or code) was given, please review those files thoroughly
- then produce a **detailed plan** of what changes your will want to make

---

### Phase 5 — Deliver Fully Worked, Standalone Results

For each plan:
- ask the user which plan he prefers and if he sees some adjustments you should make
- then **produce a fully worked result**

---

## Best Practices

- Move quickly toward clarity instead of perfection
- Use MCQs only where decisions actually matter
- Make solution options clearly distinguishable
- Always produce outputs that work **on their own**

---

## Example Short Prompt

```
Use ContextFit.
Help me briefly clarify my desired outcome.
Then interview me with 7 MCQs (answers A/B/C/D only).
Propose 2–3 solution options and fully work out the selected ones.
```
