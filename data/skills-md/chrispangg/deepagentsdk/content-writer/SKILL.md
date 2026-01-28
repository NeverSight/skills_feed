---
name: content-writer
description: Writing content across different platforms and styles. This skill should be used when creating blog posts, LinkedIn posts, X/Twitter threads, technical documentation, or other written content. It intelligently selects the appropriate writing style based on the platform, audience, and content type, then applies that style consistently throughout the piece.
---

# Content Writer

## Overview

This skill enables writing high-quality content across different platforms and audiences. It dynamically selects the appropriate writing style based on the task, then applies that style consistently. Available styles include deep technical blog posts, social media content (LinkedIn, X/Twitter), tutorials, and more.

## Style Selection

Before writing, determine the appropriate style based on these factors:

| Factor | Consider |
|--------|----------|
| **Platform** | Blog, LinkedIn, X/Twitter, documentation, newsletter |
| **Audience** | Engineers, executives, general tech audience, developers |
| **Depth** | Deep-dive technical, lightweight explainer, announcement |
| **Tone** | Authoritative, conversational, promotional, educational |
| **Length** | Long-form (2000+ words), medium (500-1500), short (<500), thread |

### Style Decision Tree

```
Is this for social media?
├─ Yes → LinkedIn or X/Twitter style
│   ├─ Professional/B2B → LinkedIn Style
│   └─ Tech community/casual → X/Twitter Style
│
└─ No → Is this a technical blog post?
    ├─ Yes → What voice/style?
    │   ├─ Karpathy-style (conversational, personal, pragmatic) → Karpathy Style
    │   ├─ Opinion-forward analysis → Deep Technical Style
    │   ├─ Lightweight explainer → Simplified Technical Style
    │   └─ Tutorial/how-to → Tutorial Style
    │
    └─ No → What type?
        ├─ Announcement → Announcement Style
        ├─ Newsletter → Newsletter Style
        └─ Documentation → Documentation Style
```

## Available Styles

### 1. Karpathy Style (Conversational Technical)

**Use when:** Writing technical content that feels personal and accessible. Best for blog posts about AI/ML, tutorials, or technical essays where you want the voice of an expert friend explaining things over coffee.

**Characteristics:**

- First-person, conversational tone ("I've found that...", "Here's what I learned...")
- Starts with personal experience or intriguing premise
- Progressive complexity (simple → detailed)
- Dry wit and occasional humor
- Honest about limitations and failures
- Pragmatic ("It only has to be right more often than not")
- Numbered frameworks and structured approaches
- Memorable, quotable lines

**Load:** `references/karpathy-style.md` for comprehensive guidance

**Core Philosophy:** "Don't be a hero. Start simple. Be patient."

**Opening Hooks (choose one):**

| Pattern | Example |
|---------|---------|
| Personal experience | "I still remember when I trained my first recurrent network..." |
| Intriguing premise | "We're going to feed 2 million selfies to a neural network and have it tell us what makes a selfie good." |
| Leaky abstraction | "Neural nets are not 'off-the-shelf' technology the second you deviate slightly from training an ImageNet classifier." |
| Strong observation | "Trees are solidified air." |

**Example opening:**
> "I've trained a lot of neural networks over the years and I've come to find that the process isn't nearly as simple as it seems. They are a leaky abstraction. Here's what I've learned."

**Tweet/X style (short-form):**
- Pithy observations that compress insight
- Strong statements (90% true, ignore counterexample police)
- Unexpected connections between domains
- Personal candor about struggles and discoveries

### 2. Deep Technical Style (Opinion-Forward Analysis)

**Use when:** Writing opinion-forward technical analysis about AI, LLMs, agents, or engineering topics. Best for content targeting senior engineers who want bold takes backed by evidence.

**Characteristics:**

- Contrarian, opinion-forward opening hooks
- "Do the simple thing first" philosophy
- Concrete examples with specific numbers
- Takes clear positions and makes predictions
- Varied sentence length, active voice

**Load:** `references/deep-technical-style.md` for comprehensive guidance

**Core Philosophy:** "Do the simple thing first."

- Embrace the black box: Focus on inputs/outputs, not internal mechanisms
- Domain expertise over technical knowledge
- Simplicity as virtue: Start simple, add complexity only when necessary
- Opinion-forward: Take clear positions and make predictions boldly

**Opening Hooks (choose one):**

| Pattern | Example |
|---------|---------|
| Contrarian position | "The death of prompt engineering has been greatly exaggerated." |
| Practical pain point | "So you need to hire someone to build your LLM multi-agent system..." |
| Challenge assumptions | "If you've been stuffing thousands of tokens thinking 'more context = better'..." |
| Surprising simplicity | "Claude Code isn't built on a complex multi-agent swarm. It's a single-threaded loop." |

**Example opening:**
> "Most AI architectures are overengineered. A single-threaded loop often outperforms elaborate multi-agent orchestrations."

### 3. LinkedIn Style

**Use when:** Writing professional content for LinkedIn—thought leadership, announcements, industry insights.

**Characteristics:**

- Hook in first line (appears before "see more")
- Short paragraphs (1-2 sentences each)
- Line breaks between paragraphs for mobile readability
- Personal angle or story
- Call-to-action or question at the end
- Strategic use of emojis (sparingly, professionally)
- 1300 characters ideal, 3000 max

**Structure:**

```
[Hook line that creates curiosity]

[Personal context or story - 2-3 short paragraphs]

[Key insight or lesson - bulleted if multiple points]

[Call-to-action or engaging question]

#relevanthashtags (3-5 max)
```

**Example:**

> Most AI features never make it to production.
>
> Not because the models aren't good enough.
>
> Because teams build for demos, not for users.
>
> After shipping 50+ AI features, here's what actually matters:
>
> → Start with the simplest possible implementation
> → Measure what users do, not what they say
> → Treat AI like any other code: test it, monitor it, iterate
>
> What's the biggest lesson you've learned shipping AI?

### 4. X/Twitter Style

**Use when:** Writing for X/Twitter—quick insights, hot takes, thread explainers, engagement posts.

**Characteristics:**

- Punchy, high-signal first tweet
- No filler words
- Threads: numbered, each tweet standalone valuable
- Contrarian takes perform well
- Code snippets or visuals boost engagement
- 280 characters per tweet, threads typically 5-15 tweets

**Thread structure:**

```
1/ [Bold claim or hook]

2/ [Context or "here's why"]

3-N/ [Key points, one per tweet]

N+1/ [Takeaway or call-to-action]

[Optional: link to longer content]
```

**Example:**

> Unpopular opinion: RAG is overengineered for most use cases.
>
> A well-crafted system prompt often outperforms a poorly designed RAG pipeline.
>
> Thread on when to use (and skip) RAG 🧵

### 5. Simplified Technical Style

**Use when:** Writing accessible technical content for broader audiences—explainers, introductions, "what is X" posts.

**Characteristics:**

- Start with the "why it matters" not the "what it is"
- Analogies to familiar concepts
- Avoid jargon or define it immediately
- Progressive complexity (simple → detailed)
- Concrete examples before abstract explanations

**Example opening:**

> Every time you ask ChatGPT a question, something interesting happens behind the scenes. The AI doesn't just "know" the answer—it builds one, word by word, based on patterns it learned from millions of conversations.

### 6. Tutorial Style

**Use when:** Writing step-by-step guides, how-tos, implementation walkthroughs.

**Characteristics:**

- Clear prerequisites upfront
- Numbered steps
- Code blocks with comments
- "What you'll learn" summary
- Troubleshooting section
- Working example at the end

**Structure:**

```
## What You'll Build
[One sentence + screenshot/diagram]

## Prerequisites
[Bulleted list]

## Steps
### Step 1: [Action verb]
[Explanation + code]

### Step 2: ...

## Troubleshooting
[Common issues + solutions]

## Next Steps
[Where to go from here]
```

### 7. Announcement Style

**Use when:** Announcing features, releases, milestones, company news.

**Characteristics:**

- Lead with the news, not the backstory
- What it is → Why it matters → How to use it
- Keep it concise
- Clear call-to-action
- Links to more detailed content

**Example:**

> We just shipped streaming support for Deep Agent.
>
> Now you can see your agent's thinking in real-time—tool calls, responses, everything—as it happens.
>
> Why it matters: Debugging agent loops is 10x easier when you can watch them run.
>
> Try it: `createDeepAgent({ model, onEvent: console.log })`

## Writing Workflow

### Step 1: Identify the Style

Ask these questions:

1. Where will this be published?
2. Who is the primary audience?
3. What action should readers take after reading?
4. How much time will readers spend on this?

### Step 2: Load Style Reference

For Deep Technical style, load `references/deep-technical-style.md` for detailed guidance including:

- 7 opening hook patterns with examples
- 5 argumentative structures
- 10+ rhetorical techniques
- 8 recurring themes to weave throughout
- Sentence-level craft patterns
- Pre-publication checklist

For other styles, refer to the characteristics above.

### Step 3: Draft with Style Constraints

Apply the chosen style's characteristics from the start. Don't write generically then "style" it later—the style should inform structure, not just tone.

### Step 4: Review Against Style Checklist

Each style has implicit requirements. Before finalizing:

**Karpathy Style:**

- [ ] First-person, conversational voice?
- [ ] Opens with personal experience or intriguing premise?
- [ ] Honest about limitations ("This might be wrong, but...")?
- [ ] Progressive complexity (simple → detailed)?
- [ ] Contains dry wit or memorable lines?
- [ ] Pragmatic advice, not theoretical?

**Deep Technical Style:**

- [ ] Contrarian or surprising opening?
- [ ] Specific numbers/examples?
- [ ] Clear position taken?
- [ ] Explains "why" not just "what"?
- [ ] Subheadings as mini-arguments?
- [ ] Active voice throughout?

**LinkedIn Style:**

- [ ] Hook visible before "see more"?
- [ ] Mobile-friendly spacing?
- [ ] Personal angle included?
- [ ] Ends with engagement prompt?

**X/Twitter Style:**

- [ ] First tweet standalone compelling?
- [ ] Each tweet <280 chars?
- [ ] No filler words?
- [ ] Thread numbered clearly?

## AI Slop Avoidance

**Critical:** All content must avoid patterns that signal AI-generated text. Load `references/ai-slop-avoidance.md` for comprehensive guidance.

### Quick Reference: Words to Ban

Never use these overused AI words:

| Category | Banned Words |
|----------|--------------|
| **Verbs** | delve, embark, unleash, harness, unlock, navigate, revolutionize, foster, elevate |
| **Adjectives** | vibrant, bustling, intricate, pivotal, crucial, cutting-edge, robust, seamless, meticulous |
| **Nouns** | tapestry, realm, landscape, paradigm, synergy, beacon, testament, game-changer |
| **Phrases** | "it's important to note", "in today's digital age", "dive into", "at its core", "a myriad of" |

### Quick Reference: Patterns to Avoid

| Pattern | Problem | Fix |
|---------|---------|-----|
| **Em-dashes (—)** | Strong AI signal, ban entirely | Use commas, parentheses, periods (hyphens/en-dashes OK) |
| Uniform sentences | All ~25-30 words | Mix 5-word punches with 40-word explanations |
| Excessive hedging | "might", "arguably", "perhaps" | Take clear positions |
| Immediate lists | Jump to bullets without narrative | Build tension first |
| Perfect grammar | Zero typos feels robotic | Occasional imperfection is human |
| Balanced both-sides | Artificial neutrality | Take a stance |

### AI Slop Checklist (Apply to All Content)

- [ ] Zero banned words from the list above?
- [ ] **Zero em-dashes (—) in the entire piece?**
- [ ] Sentence lengths vary dramatically (some <10 words, some >35)?
- [ ] Contains specific names, numbers, dates?
- [ ] Has personal voice or anecdotes?
- [ ] Takes clear positions without excessive hedging?
- [ ] Avoids "In conclusion" / "To summarize" closings?

## Resources

### references/

- `karpathy-style.md` - Guide for writing in Andrej Karpathy's conversational, pragmatic technical style with blog post patterns, tweet patterns, and recurring themes
- `deep-technical-style.md` - Comprehensive guide for opinion-forward technical blog posts with detailed examples, rhetorical techniques, and pre-publication checklist
- `ai-slop-avoidance.md` - Detailed guide to avoiding AI-generated content patterns

## Extending This Skill

To add new writing styles:

1. Analyze 5-10 examples of the target style
2. Extract patterns: opening hooks, structure, tone, length constraints
3. Create a reference file in `references/[style-name]-style.md`
4. Add the style to the decision tree and Available Styles section
5. Include a checklist for that style in the Review step
