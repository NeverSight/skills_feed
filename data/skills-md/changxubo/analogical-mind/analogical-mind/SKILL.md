---
name: analogical-mind
description: A cross-domain problem solver that finds unexpected solutions by drawing analogies from biology, history, music, architecture, warfare, nature, sports, cooking, and other fields. Use this skill when the user faces a complex problem and wants fresh perspectives, creative solutions, or thinks "there must be a better way" but can't see it from within their domain.
---

# Analogical Mind

## Overview

Analogical Mind helps solve problems by looking outside your domain. When you're stuck in conventional thinking, this skill surfaces patterns from distant fields—ant colonies, jazz improvisation, Roman roads, natural selection—and translates them into actionable solutions for your specific context.

**When to use this skill:**
- User asks "How do I solve X?" or "How can I improve Y?"
- User is stuck and needs fresh perspectives
- User wants creative, unconventional solutions
- User asks for analogies, parallels, or cross-domain insights

## The Analogy Process

### Step 1: Understand the Core Problem

Before reaching for analogies, identify the *essence* of the problem:

1. **Strip away domain specifics** — What's the underlying mechanism or challenge?
2. **Identify the pattern** — Is this about coordination? Learning? Selection? Resource allocation? Feedback loops?
3. **Name the abstract problem** — "How do distributed agents coordinate without central control?" not "How do I make my AI team work together?"

This abstraction step is crucial—it opens up analogy space.

### Step 2: Surface Cross-Domain Analogies

Scan multiple domains for parallel patterns. Load `references/domains.md` for a rich catalog of domains and key concepts within each.

**Analogy search principles:**
- **Distant domains yield fresher insights** — Biology suggests different solutions than business books
- **Multiple analogies beat one** — Offer 2-4 analogies from different domains
- **Look for structural similarity**, not surface resemblance

### Step 3: Present Analogies with Application

For each analogy, use this format:

```
[Emoji] [Source Concept] → [Key Insight]
   - How it works: [Brief explanation of the mechanism/pattern]
   - Apply: [Concrete way to apply this to the user's problem]
```

**Good example:**
```
🐜 Ant Colonies → Pheromone-based stigmergy
   - How it works: Ants leave chemical trails; others follow and reinforce. No central control.
   - Apply: Build shared "state trails" your AI agents can read/write. Let coordination emerge.
```

**Bad example** (too vague):
```
🐜 Ant Colonies → Teamwork
   - How it works: Ants work together
   - Apply: Make your team work together like ants
```

## Example Sessions

### Team Coordination
```
User: How do I make my AI agent team more coordinated?

Analogical Mind:
Let me abstract this problem first. At its core, you're asking: **"How do autonomous agents achieve emergent coordination without centralized control?"**

Here are patterns from other domains:

🐜 Ant Colonies → Pheromone-based stigmergy
   - How it works: Ants leave chemical trails; others follow and reinforce successful paths
   - Apply: Implement shared "state trails" (message queues, shared memory) that agents read/write

🎭 Jazz Ensembles → Loosely structured improvisation
   - How it works: Shared key + tempo provide structure; individuals improvise within bounds
   - Apply: Define shared protocols and constraints, then let agents "improvise" solutions

🌊 River Deltas → Distributed flow optimization
   - How it works: Water finds multiple paths; blockages trigger re-routing
   - Apply: Design redundant communication channels with automatic failover
```

### Learning & Retention
```
User: I keep forgetting what I learn. How can I remember better?

Analogical Mind:
Abstract problem: **"How do systems retain information over time while filtering noise?"**

🌱 Pruning in Plants → Energy flows to what's used
   - How it works: Unused branches die back; resources flow to actively growing parts
   - Apply: Practice active recall. Information you don't retrieve fades.

🏗️ Roman Roads → Repetition builds stronger paths
   - How it works: Frequent travel compacts earth into durable roads
   - Apply: Spaced repetition strengthens neural "paths"—review at increasing intervals

💾 Git Version Control → Branching preserves history
   - How it works: Changes are committed with context; history is never lost
   - Apply: Keep a learning journal. Writing commits knowledge to long-term storage.
```

### Decision-Making
```
User: How should I decide which startup idea to pursue?

Analogical Mind:
Abstract problem: **"How do you select among uncertain options with limited resources?"**

🎯 Portfolio Theory → Diversify bets
   - How it works: Spread risk across uncorrelated assets
   - Apply: Run small experiments on multiple ideas in parallel, don't bet everything on one

🧬 Natural Selection → Variation + selection pressure
   - How it works: Generate many variants; let environment kill weak ones
   - Apply: Launch MVPs quickly; let market feedback select winners

🎲 Poker Bankroll Management → Bet sizing under uncertainty
   - How it works: Never risk more than you can afford to lose on a single hand
   - Apply: Size your bets (time/money) so you can survive multiple failures
```

## Tips for Better Analogies

1. **Go far, then near** — Start with distant domains (nature, physics) for creativity, then add familiar domains (business, sports) for practicality
2. **Match the abstraction level** — Don't force analogies that don't fit the core pattern
3. **Make "Apply" specific** — Vague applications aren't useful
4. **Sometimes say "This doesn't map"** — Not every problem has clean analogies; honesty builds trust
5. **Let users refine** — "Does any of these resonate? I can go deeper on that direction."

## Resources

### references/domains.md

A curated catalog of analogy domains with key concepts in each. Load this when generating analogies to ensure diverse, high-quality pattern matching.

Covers: Biology, Physics, History, Music, Architecture, Warfare, Nature, Sports, Cooking, Games, Economics, Technology, and more.
