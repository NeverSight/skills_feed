---
name: rp-why
description: Gas Town × DOK Framework - A two-dimensional model for analyzing AI collaboration maturity and cognitive complexity to reveal growth opportunities.
author: dakotafabro
version: "3.0"
tags:
  - reflection
  - growth
  - ai-collaboration
  - self-assessment
  - productivity
  - learning
---

# rp-why: Gas Town × DOK Framework

## Overview

The **rp-why** skill is a self-reflection framework that helps AI practitioners measure and improve their AI collaboration practice. It combines two powerful dimensions:

- **Horizontal Axis: Gas Town Stages** — Measures AI tool adoption maturity from basic chatbots to multi-agent orchestration
- **Vertical Axis: DOK Levels** — Measures the cognitive complexity of prompts from simple recall to extended thinking

The intersection of these dimensions reveals growth opportunities and helps users maximize the value they extract from their AI tools.

---

## How to Use This Skill

### Installation

Install the skill using the skills CLI:

```bash
npx skills add https://github.com/block/agent-skills --skill rp-why
```

Make sure you have the built-in skills extension enabled in your agent (Goose, Claude Desktop, etc.).

### Using Slash Commands

Once the skill is loaded, you can use slash commands directly in your conversation:

```
You: /rp-why current
```

Goose will analyze your current session and provide:
- Your Gas Town stage assessment
- DOK distribution breakdown
- Quadrant position
- Growth nudges

### Available Commands

| Command | What It Does |
|---------|--------------| 
| `/rp-why current` | Analyze the current session |
| `/rp-why init` | Generate a baseline from your history |
| `/rp-why compare` | Compare current session to baseline |

### Alternative: Natural Language

You don't have to use slash commands. You can also just ask naturally:

```
You: Analyze my AI collaboration patterns using the Gas Town DOK framework
You: What's my DOK distribution for this session?
You: How does this session compare to my baseline?
```

The skill will recognize these requests and provide the same analysis.

### When to Use

- **End of session**: Run `/rp-why current` to reflect on your work
- **Weekly**: Run `/rp-why compare` to track progress
- **First time**: Run `/rp-why init` to establish your baseline

---

## Problem Statement

Many AI practitioners face a hidden inefficiency: a mismatch between tool sophistication and task cognitive complexity.

| Anti-Pattern | Impact |
|--------------|--------|
| Using powerful autonomous agents for simple "what is X?" queries | Unrealized potential |
| Asking deep strategic questions through basic chatbot interfaces | Bottlenecked thinking |
| No visibility into personal AI usage patterns | Stagnant growth |
| No framework for intentional growth in AI collaboration skills | Missed opportunities |

Without measurement, there's no improvement. Users need a mirror to see their AI collaboration patterns clearly.

---

## The Framework

### Yegge's 8 Gas Town Stages (AI Tool Adoption)

From Steve Yegge's "Welcome to Gas Town" (January 2026):

| Stage | Name | Description |
|-------|------|-------------|
| 8 | Full Gas Town | Complete AI-native development ecosystem |
| 7 | Agentic Workflows | Automated pipelines with agent coordination |
| 6 | Multi-Agent | Orchestrating multiple specialized agents |
| 5 | CLI Single Agent, YOLO | Terminal-based autonomous agent (e.g., Goose) |
| 4 | Chat IDE | Integrated chat in development environment |
| 3 | Copilot | Using AI code completion, inline suggestions |
| 2 | Curious | Experimenting with basic chatbots occasionally |
| 1 | Observer | Watching and evaluating AI tools, not yet actively using |

### Webb's DOK Levels (Cognitive Complexity)

From Norman Webb's Depth of Knowledge framework (1997):

| Level | Name | Description | Prompt Indicators |
|-------|------|-------------|-------------------|
| 4 | Extended Thinking | Complex investigation, multiple sessions | "Research and synthesize...", "Create a framework...", "Investigate over time..." |
| 3 | Strategic Thinking | Reasoning, planning, analysis, synthesis | "Design...", "Analyze...", "What if...", "Develop a strategy..." |
| 2 | Application | Apply concepts, make decisions, compare | "How would you...", "Compare...", "Explain why..." |
| 1 | Recall | Facts, definitions, simple procedures | "What is...", "List...", "Define..." |

### Integration Matrix (Stage × DOK)

The intersection creates six distinct zones:

```
              DOK 1        DOK 2         DOK 3          DOK 4
            (Recall)   (Application) (Strategic)   (Extended)
           ┌──────────┬──────────────┬────────────┬────────────┐
Stage 6-8  │   Over-  │    Over-     │ Underutil- │  Frontier  │
(Multi/    │  powered │   powered    │   izing    │            │
 Agentic)  │          │              │            │            │
           ├──────────┼──────────────┼────────────┼────────────┤
Stage 5    │   Over-  │  Underutil-  │  Expected  │  Growing   │
(CLI YOLO) │  powered │    izing     │            │            │
           ├──────────┼──────────────┼────────────┼────────────┤
Stage 3-4  │   Over-  │   Expected   │  Growing   │  Frontier  │
(Copilot/  │  powered │              │            │            │
 Chat IDE) │          │              │            │            │
           ├──────────┼──────────────┼────────────┼────────────┤
Stage 1-2  │ Expected │   Growing    │  Thinking  │  Thinking  │
(Observer/ │          │              │   Ahead    │   Ahead    │
 Curious)  │          │              │            │            │
           └──────────┴──────────────┴────────────┴────────────┘
```

**Zone Definitions:**

| Zone | Description | Action |
|------|-------------|--------|
| **Frontier** | Pushing boundaries of both tool and cognition | Celebrate & Document |
| **Thinking Ahead** | High cognitive work with basic tools | Upgrade tools |
| **Growing** | Stretching into higher complexity, positive trajectory | Encourage |
| **Expected** | Appropriate match of tool sophistication to task complexity | Maintain |
| **Underutilizing** | Sophisticated tools for simpler tasks | Increase DOK |
| **Overpowered** | Tools exceed task needs—opportunity to level up your questions | Realign |

---

## Commands

### `/rp-why current`

Analyze the current session's Gas Town stage and DOK distribution.

**Output includes:**
- Stage assessment with confidence level
- DOK distribution breakdown with percentages
- Quadrant position visualization
- Contextual growth nudges
- Reflection prompt

### `/rp-why init`

Generate a baseline from your conversation history (analyzes available sessions).

**Output includes:**
- Historical analysis period and session count
- Baseline DOK distribution
- Typical Gas Town stage
- Growth targets
- Baseline saved to `~/.config/goose/rp-why-baseline.json`

### `/rp-why compare`

Compare current session against your established baseline.

**Output includes:**
- Side-by-side DOK comparison (baseline vs current)
- Quadrant movement visualization
- Progress toward growth targets
- Trajectory analysis

---

## Sample Output

```
╔══════════════════════════════════════════════════════════════════╗
║                    rp-why: CURRENT SESSION                       ║
╚══════════════════════════════════════════════════════════════════╝

GAS TOWN STAGE: 5 (CLI Single Agent, YOLO)

DOK DISTRIBUTION
────────────────────────────────────────────────────────────────────
DOK 1 (Recall):      ████░░░░░░░░░░░░░░░░  17%
DOK 2 (Application): ████████████░░░░░░░░  52%
DOK 3 (Strategic):   ██████░░░░░░░░░░░░░░  26%
DOK 4 (Extended):    █░░░░░░░░░░░░░░░░░░░   5%

QUADRANT: Underutilizing
────────────────────────────────────────────────────────────────────
You're using powerful autonomous tools—there's an opportunity to
match your questions to that power.

GROWTH NUDGES
────────────────────────────────────────────────────────────────────
1. Shift 2-3 DOK 2 prompts to DOK 3 by adding "analyze trade-offs"
2. Before simple queries, ask: "Can I make this more strategic?"
3. Try one DOK 4 extended investigation this week

🪞 REFLECTION
────────────────────────────────────────────────────────────────────
What complex challenge could benefit from your agent's full
capabilities today?
```

---

## Target User Profiles

| Profile | Typical Stage | DOK Distribution | Characteristics |
|---------|---------------|------------------|-----------------|
| Traditional | 1-2 | DOK1: 60%, DOK2: 30%, DOK3: 10% | Minimal AI use |
| Adopter | 3-4 | DOK1: 40%, DOK2: 40%, DOK3: 15%, DOK4: 5% | Growing comfort |
| Practitioner | 5 | DOK1: 25%, DOK2: 45%, DOK3: 25%, DOK4: 5% | Autonomous agents |
| Advanced | 5-6 | DOK1: 15%, DOK2: 35%, DOK3: 35%, DOK4: 15% | Strategic use |
| Frontier | 7-8 | DOK1: 10%, DOK2: 25%, DOK3: 40%, DOK4: 25% | Agentic workflows |

---

## Growth Nudge Reference

### Frontier (High Stage, High DOK)
- "You're pushing boundaries—document what you learn"
- "Share patterns with others; teach what works"
- "Explore the edges: what's not yet possible?"

### Thinking Ahead (Low Stage, High DOK)
- "Your thinking exceeds your tools—time to upgrade!"
- "Explore CLI agents or IDE integration"
- "Your DOK is strong; let better tools amplify it"

### Underutilizing (High Stage, Lower DOK)
- "Powerful tools deserve powerful questions"
- "Before each prompt, ask: Can this be more strategic?"
- "Batch simple queries; save the agent for complex work"

### Learning Zone (Low Stage, Low DOK)
- "This is a natural starting point—focus on learning the tools"
- "Try one new AI capability each session"
- "Don't worry about DOK yet—get comfortable first"

### Overpowered (High Stage, Low DOK)
- "Your tools exceed your task needs—opportunity to level up your questions"
- "Consider: Is this query worth an autonomous agent?"
- "Batch simple lookups; reserve agent for strategic work"

---

## Upgrading Your Prompts

| DOK Level | Prompt Pattern | Example |
|-----------|----------------|---------|
| 1 → 2 | Add "how" or "why" | "What is a mutex?" → "How would I use a mutex here?" |
| 2 → 3 | Add "trade-offs" or "design" | "How do I implement caching?" → "Design a caching strategy considering our constraints" |
| 3 → 4 | Extend across sessions | "Analyze this architecture" → "Research caching patterns over multiple sessions and synthesize recommendations" |

---

## Attribution

- **Gas Town Stages**: Steve Yegge, "Welcome to Gas Town" (January 2026)
  https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04

- **Depth of Knowledge (DOK)**: Norman Webb (1997)
  Webb, N. L. (1997). Criteria for alignment of expectations and assessments in mathematics and science education. Council of Chief State School Officers.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2026-02 | Quadrant visualization, growth nudges, reflection prompts, updated terminology |
| 2.x | 2026-01 | Integration matrix, target profiles, baseline comparison |
| 1.x | 2025-12 | Initial Gas Town stages, basic DOK tracking |
