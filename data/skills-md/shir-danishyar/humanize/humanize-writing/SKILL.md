---
name: humanize-writing
description: Use when writing or editing prose an audience will read — emails, blog posts, articles, marketing and website copy, LinkedIn or social posts, cover letters, newsletters, product descriptions, reports, essays — and when the user asks to humanize text, make it sound natural or less robotic, remove AI patterns, or clean up an AI-generated draft. Applies by default to any audience-facing writing task. Do not use for code, commit messages, config files, or legal documents where formulaic precision is required.
---

# Humanize Writing

Removes the statistical fingerprints of LLM-generated text, as catalogued by Wikipedia's "Signs of AI writing" (WikiProject AI Cleanup) and measured by the corpus studies that page cites (Kobak et al. 2025, *Science Advances*; Juzek & Ward 2025; Reinhart et al. 2025, *PNAS*).

Two principles drive everything below.

**Density, not existence.** No single pattern proves anything; humans use all of them. What exposes AI text is several patterns clustered in one passage. Write so the cluster never forms.

**Specific beats generic.** Wikipedia describes the mechanism as regression to the mean: a model replaces the specific, unusual fact with a generic, important-sounding one, so the subject becomes "simultaneously less specific and more exaggerated". Humanizing reverses that. Put the specific back, take the exaggeration out.

## Two modes

**Generation mode (default).** You are writing new prose. Apply the rules while drafting so the text comes out human the first time.

**Rewrite mode.** The user pastes existing text and asks you to clean it. Strip AI patterns while preserving everything else:

- Never alter direct quotes. Quoted third-party text stays verbatim, even if it contains banned patterns.
- Never change citations, numbers, statistics, dates, URLs, or proper nouns.
- Preserve the author's meaning and claims exactly. If removing a pattern would change what the text asserts, keep the assertion and change only the phrasing.
- Don't "improve" content they didn't ask you to change. Strip patterns; don't editorialize.
- When editing a file, change only the prose. Leave code blocks, front matter, data, and link targets untouched.

Enter rewrite mode when the user provides text to fix; otherwise stay in generation mode.

## No invented facts

This rule applies in both modes and outranks every style rule. Never add a fact, name, number, date, quote, statistic, or citation that did not come from the source text or the user. "Concrete" means concrete *with what you actually have*. If a claim needs a specific you don't have, ask the user for it or write the sentence without it. A made-up number is worse than a vague sentence, because it is wrong. Fiction is the one exception.

## Detect the register first

A cold email, a LinkedIn post, a blog article, and a formal report should not be humanized identically. Before applying any rule, infer the register from the user's request and context:

| Register | Contractions | Fragments | Em dashes | Example contexts |
|----------|--------------|-----------|-----------|------------------|
| Social | yes | yes | rare | LinkedIn, X/Twitter, Slack, chat |
| Email | yes | sparingly | rare | cold email, follow-ups, newsletters |
| Editorial | yes | rarely | max 1/300 words | blog posts, articles, essays |
| Formal | no | no | avoid | reports, proposals, formal docs, academic |

All other rules apply in every register. When the register is ambiguous, ask yourself who receives the text and default to the closest row.

## Workflow

1. Detect mode (generation vs rewrite) and register.
2. If a `voice-profile.md` exists in the project, or the user offers samples of their own writing, read `references/voice.md` and apply their profile instead of the generic clean voice.
3. Draft (or rewrite) with the core rules below in mind.
4. Run the self-audit checklist against the draft. Fix every violation.
5. Deliver only the text. Never add a "what I changed" preamble unless asked.

Read the reference files when you need depth:

- `references/patterns.md`: the full numbered catalog (39 patterns, each with a before/after pair that adds no facts), plus Wikipedia's list of signs of *human* writing. Read it in rewrite mode, or whenever the self-audit flags something and you need the precise fix.
- `references/vocabulary.md`: the banned-word list with plain replacements, grouped by category, with the era-by-era shifts.
- `references/voice.md`: voice calibration, extracting a profile from user samples and persisting it.

## Core rules

The most damaging patterns, always in effect. Numbers refer to `references/patterns.md`.

**Structure (P1–P12).** Never write negative parallelism ("It's not X, it's Y", "This isn't about speed. It's about trust.", "X rather than Y") and never answer an objection nobody raised. State the positive claim. Break the rule of three: one strong word or two, not "innovative, efficient, and scalable". No false ranges ("from startups to enterprises"). No trailing participles that editorialize ("...reflecting its growing importance", "...ensuring..."): state the fact and stop. Use plain "is/has" instead of "serves as", "stands as", "boasts", "features", "offers". Call a thing the same name twice instead of cycling synonyms. No staccato drama fragments. Collapse hedging stacks ("could potentially help" → "may help"); a single hedge is fine and human. Vary sentence length.

**Framing (P13–P20).** No summary closers ("In conclusion", "Overall", a final paragraph restating the piece): end on your last substantive point. Cut "It's important to note", "Notably", "Interestingly". Name your sources or own the claim yourself, no "experts say", "studies show", "widely regarded as". No significance inflation ("pivotal moment", "enduring legacy", "setting the stage for"). No "Despite challenges... the future looks bright" scaffolds. Don't open with a definition, a restatement of the prompt, or an announcement ("Let's dive in"). Open with the most useful true thing.

**Conversational artifacts (P21–P26).** Strip anything a chatbot says to its user: "Great question!", "You're absolutely right", "Honestly?", "I hope this helps!", "Let me know if...", "Would you like me to...", "As of my last update...", "While specific details are not widely documented..." followed by a guess, and unfilled placeholders like "[Insert name]". None of these may appear inside a deliverable.

**Formatting (P27–P34).** At most one em dash per ~300 words, unspaced, and only where a comma or parentheses genuinely wouldn't work. No bold mid-sentence for emphasis. No "**Term:** definition" bullets. Default to prose; bullets only when the user asks or the content is truly enumerable. No emoji in headings, ever. No headings at all under ~400 words, no title heading repeating the document name, no "Awards and recognition" style "X and Y" headings, no horizontal rules between sections. Sentence case for headings. Keep quotation marks consistent (don't mix curly and straight). No two-row tables for facts that belong in a sentence.

**Vocabulary (P35–P36).** Avoid the AI word list: delve, tapestry, intricate, interplay, pivotal, crucial, key (adjective), underscore, highlight (verb), emphasize (trailing), landscape (abstract), foster, enhance, align with, enduring, testament, boast, meticulous, realm, showcase, leverage, robust, seamless, elevate, embark, journey (metaphorical), navigate (metaphorical), unlock, harness, empower, game-changer, cutting-edge, groundbreaking, transformative, comprehensive, holistic, streamline, synergy, paradigm, myriad, plethora, vibrant, valuable insights, ever-evolving, deep dive, "in today's fast-paced world", "at the end of the day", unless the user's own text uses them or no plain alternative exists. Full list and replacements in `references/vocabulary.md`.

**Newer tells (P37–P39).** Don't prove importance by describing the coverage ("featured in national media outlets", "maintains an active social media presence"); say what was said. Don't gesture at relationships with "associated with" or "in connection with"; name them (founded, taught, member of). No small tables for two facts.

**Write like a person.** Wikipedia's signs of human writing: simple "is/has" sentences; plain verbs (wrote, moved, used, tried, died); definite statements when they are true ("was the first"); the odd unglamorous detail; uneven sentence lengths. Prefer the specific you have ("replies within two hours") over the abstraction ("prompt communication"). Say each idea once.

## Self-audit checklist

Before delivering any prose, scan the draft for:

1. Any fact, number, name, date, or quote that wasn't in the source or the brief → remove it (the one non-negotiable check)
2. Any "not X, but Y" / "isn't just X, it's Y" / "X rather than Y" construction (P1–P2) → rewrite as a direct claim
3. Em dashes: more than 1 per 300 words, or spaced (P27)? → replace with commas or parentheses
4. Any banned-vocabulary word (P35) → replace with the plain alternative
5. Triplet lists (P3) → cut to one or two, or expand honestly
6. Final paragraph (P13, P19) → does it summarize or forecast instead of end? Replace with the last specific point
7. Trailing "-ing" significance clauses (P5) → delete
8. "It's important to note" and cousins (P14), chatbot phrases (P21–P26) → delete
9. Bold mid-prose, "Term: definition" bullets, emoji headings, tiny tables (P28–P31, P39) → strip
10. Unnamed "experts/studies", "featured in outlets", "associated with" (P15, P37, P38) → name the source or the relationship, or cut
11. Read three consecutive sentences aloud: same length and rhythm? → break one up

Optional mechanical check: run `scripts/ai_pattern_lint.py` on the draft; it reports pattern hits per 1000 words.

## False-positive guard

These patterns are statistical signals, not proof of anything. Apply them with judgment:

- **The user wins.** If they explicitly ask for bullets, em dashes, bold terms, or any banned element, their instruction overrides this skill. It sets defaults, not handcuffs.
- **Quotes are untouchable.** Never "fix" quoted third-party text, in either mode.
- **Precision beats style.** Never sacrifice factual accuracy, a necessary technical term, or a legally required phrase to dodge a pattern. If "comprehensive" is the accurate word, keep it.
- **Humans use these too.** An em dash or a three-item list is not a crime; the density of many patterns together is the tell. Fix the cluster, not every isolated instance.
- **Not signs at all.** Wikipedia's list of ineffective indicators: perfect grammar, a mix of casual and formal register, prose that merely feels bland, formal vocabulary in general, one transition word, unsourced claims, curly quotes alone. Leave them.
- **Wordiness is human.** "In order to" and "the fact that" are more common in human text than AI text. Trim them for concision if you like; don't mistake it for humanizing.
