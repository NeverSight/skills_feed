---
name: council-of-five
description: Spawn 5 Opus subagents with randomly-generated distinct personas to debate a problem from multiple angles. Use when exploring UX decisions, architecture choices, or any decision that benefits from diverse perspectives arguing creatively.
---

# Council of Five

Spin up 5 parallel Opus agents, each with a **randomly generated** distinct persona, to explore a problem from radically different angles. They argue, then you synthesize.

## When to Use

- UX/design decisions with no obvious "right answer"
- Architecture trade-offs (speed vs. maintainability, etc.)
- Naming conventions, API design, workflow design
- Any decision where "outside the box" thinking helps

## Random Persona Generation

**Each invocation generates 5 fresh personas.** Pick randomly from diverse archetypes:

### Archetype Pool (sample, not exhaustive)

| Category | Example Personas |
|----------|------------------|
| **Reduction** | The Minimalist, The Deletionist, The "YAGNI" Zealot, The Haiku Master |
| **Narrative** | The Storyteller, The Novelist, The Stand-up Comic, The Documentary Filmmaker |
| **Visual** | The Dashboard Engineer, The Infographic Designer, The Color Theorist, The Whitespace Monk |
| **Verification** | The Paranoid Auditor, The Penetration Tester, The QA Gremlin, The "Trust No One" Agent |
| **Behavior** | The UX Researcher, The Cognitive Psychologist, The Lazy User Simulator, The Angry Customer |
| **Performance** | The Latency Hunter, The Memory Miser, The Big-O Obsessive, The Cache Whisperer |
| **Accessibility** | The Screen Reader Advocate, The Color Blind Designer, The Keyboard-Only Navigator |
| **Philosophy** | The Unix Philosopher, The Functional Purist, The "Worse is Better" Advocate, The Pragmatist |
| **Chaos** | The Edge Case Finder, The Chaos Monkey, The "What If" Catastrophist, The Entropy Embracer |
| **History** | The Legacy Code Archaeologist, The "We Tried That" Historian, The Pattern Recognizer |
| **Future** | The 10x Scale Predictor, The Deprecation Prophet, The "Your Future Self" Advocate |
| **Outsider** | The New Hire, The Non-Technical Stakeholder, The Customer Support Rep, The Intern |

### Generation Rules

1. **Pick 5 personas from different categories** (no two from same category)
2. **Invent new ones** if the pool feels stale—creativity encouraged
3. **Name them vividly** (e.g., "The Haiku Master" not "The Brevity Person")
4. **Give each a one-sentence philosophy** before they argue

## Invocation

### Basic

```
I need a council of five to debate [your problem/decision]
```

### With Context

```
Run a council-of-five on this UX problem:
[paste the current approach]

What I care about: [your priority, e.g., "clarity over completeness"]
```

### Seeded with a specific angle

```
Council of five, but make sure one persona is security-focused
```

## How It Works

1. **Generate**: Randomly select 5 personas from different categories (or invent new ones)
2. **Announce**: Tell the user which 5 personas were selected and their philosophies
3. **Launch**: 5 Opus subagents spin up in parallel (background tasks)
4. **Explore**: Each argues from their persona's angle, proposing alternatives
5. **Synthesize**: Results are gathered and presented as a comparison table
6. **Decide**: User picks an approach (or hybrid)

## Prompt Template for Each Agent

```
You are [RANDOMLY GENERATED PERSONA NAME].

Your core philosophy: [generate a one-sentence worldview that fits this persona]

The user is evaluating: [problem description]

Current approach:
[paste current solution]

Your task:
1. Critique the current approach from your unique angle
2. Propose an alternative that embodies your philosophy
3. Give a concrete example of your approach in action
4. Acknowledge one weakness of your approach

Be creative. Be opinionated. Argue your position strongly.
Push boundaries—surprise the user with an angle they haven't considered.
```

## Output Format

After all agents complete, present:

1. **Quick comparison table** (persona | core argument | proposed format)
2. **Synthesis** (where they agree, where they clash)
3. **Hybrid suggestion** (if applicable)
4. **Question to user**: "What resonates?"

## Example Session

**User**: "Council of five on my error message format"

**Generated personas**:
1. **The Haiku Master** (Reduction) — "If it can't fit in 17 syllables, it's not essential."
2. **The Stand-up Comic** (Narrative) — "If they're not smiling, they're not listening."
3. **The Color Theorist** (Visual) — "Meaning lives in hue and contrast, not words."
4. **The Angry Customer** (Behavior) — "I'm already frustrated. Don't make it worse."
5. **The Chaos Monkey** (Chaos) — "What happens when this fails at 3am on a holiday?"

**Result**:
| Persona | Argument | Proposal |
|---------|----------|----------|
| Haiku Master | "Too many words" | `Auth timed out. / Server took too long. / Try once more?` |
| Stand-up Comic | "Errors are traumatic" | "Well, that didn't work. The server ghosted us. Retry?" |
| Color Theorist | "Red isn't enough" | Amber background (warning, not failure), pulsing border |
| Angry Customer | "I don't care WHY" | Big retry button, tiny "details" link, no essay |
| Chaos Monkey | "What if retry also fails?" | Exponential backoff + "Contact support" after 3 attempts |

## Tips

- **Be specific** about what you care about (speed? clarity? memorability?)
- **Provide the current approach** so personas can critique something concrete
- **Ask for hybrids** if multiple approaches resonate
- **Request a reroll** if the random personas don't fit your problem domain
- **Seed with one persona** if you want to ensure a specific angle is covered

## Controlling Randomness

**Full random** (default):
```
Council of five on my API design
```

**Seeded** (guarantee one persona, randomize the rest):
```
Council of five on my auth flow, but make sure one is a Security persona
```

**Category bias** (weight toward certain categories):
```
Council of five on my mobile app, bias toward Behavior and Accessibility categories
```

**Reroll**:
```
Those personas didn't fit—reroll with completely different ones
```

## Inventing New Personas

Don't limit yourself to the pool. Invent wild ones:

- **The Time Traveler from 2035** — "This will look embarrassing in 10 years."
- **The Toddler** — "But WHY? But WHY? But WHY?"
- **The Poet Laureate** — "Does it have rhythm? Does it breathe?"
- **The Lawyer** — "What happens when someone sues over this?"
- **The Sleep-Deprived On-Call Engineer** — "Will I understand this at 3am?"
- **The Competitor's Product Manager** — "How would I exploit this weakness?"

The weirder the persona, the more unexpected the insight.
