---
name: boardgame-design
description: Board game design workflow for creating fun, balanced games. Use when designing mechanics, balancing factions, analyzing resource economies, validating rules clarity, planning playtests, or iterating on game systems. Applies Eurogame principles and proven design methodology.
---

# Board Game Design Skill

## Overview

This skill provides comprehensive guidance for designing engaging board games, with emphasis on German-style Eurogame principles. It covers mechanical design, balance analysis, asymmetric faction design, resource economy systems, playtesting methodology, and rules documentation.

## Core Design Philosophy

### The Eurogame Approach

German-style Eurogames emphasize:

1. **Strategy Over Luck**: Minimize randomness; player decisions should drive outcomes
2. **No Player Elimination**: Everyone stays engaged until the end
3. **Indirect Conflict**: Competition through position, resources, and efficiency rather than direct attacks
4. **Multiple Paths to Victory**: No single dominant strategy
5. **Elegant Mechanics**: Maximum strategic depth from minimal rules complexity
6. **Bounded Play Time**: Built-in mechanisms to limit game length (fixed turns, resource depletion, scoring thresholds)

### What Makes Games Fun

- **Meaningful Decisions**: Every choice should have trade-offs and consequences
- **Appropriate Challenge**: Difficulty that creates satisfaction without frustration
- **Player Interaction**: Opponents' actions should matter to your strategy
- **Emergent Complexity**: Simple rules that create rich strategic possibilities
- **Steady Pacing**: Interesting events throughout; no "grinding" phases
- **Replayability**: Variability and multiple strategies encourage repeated play

## Key Design Workflows

### 1. Mechanical Design

When designing core mechanics:

- **Identify the Core Loop**: What is the most repeated action? It must be simple, fun, and have depth
- **Establish Core Constraints**: A central limitation that drives all decisions (e.g., Lift ≥ Weight in UP SHIP!)
- **Design Feedback Loops**: Actions should create cascading effects and player interaction
- **Create Tension Points**: Moments of meaningful scarcity and difficult choices
- **Balance Simplicity and Depth**: "Elegance" means rich strategy from few rules

### 2. Resource Economy Design

Resources are the lifeblood of strategic games:

- **Define Resource Types**: Money, actions, time, components, information
- **Create Scarcity**: Limited resources force meaningful choices
- **Design Flow**: Sources (generation), sinks (consumption), and conversion paths
- **Ebb and Flow**: Scarcity that changes over the game creates dynamic tension
- **Control = Power**: Whoever controls a scarce resource gains strategic advantage
- **Multiple Currencies**: Different resource types that don't directly convert create interesting trade-offs

**The Action Economy**: The most precious resource is often actions/turns. When designing:
- Make every action feel valuable
- Create opportunity cost between competing good options
- Consider: "I take it, opponent takes it, or it doesn't happen"

### 3. Asymmetric Faction Design

Asymmetry increases replayability but requires careful balance:

**Types of Asymmetry** (from subtle to extreme):
1. **Asymmetric Results**: Same rules, different outcomes from choices (Monopoly)
2. **Asymmetric Starting Positions**: Different initial resources/positions (Catan)
3. **Asymmetric Abilities**: Special powers that modify standard rules (Terra Mystica)
4. **Asymmetric Rules**: Fundamentally different gameplay for each faction (Root)

**Balance Principles**:
- Players should feel powerful, not restricted
- Each faction needs at least 3 viable strategic paths
- Trade-offs should be meaningful: strong at X, weaker at Y
- Theme should justify mechanical differences
- Consider self-balancing through player interaction (ganging up on leaders)
- "Dial down" extremes: moderate bonuses are easier to balance

**Testing Asymmetry**:
- Asymmetry creates combinatorial explosion of test cases
- Focus playtesting on faction vs. faction matchups
- Track win rates by faction over many games
- Watch for perceived imbalance vs. actual imbalance

### 4. Balance Analysis

Balance ensures fair competition and strategic viability:

**Pre-Playtest Balance**:
- Mathematical modeling of cost-benefit ratios
- Compare similar options: are costs proportional to power?
- Check for dominant strategies on paper
- Model income/resource generation over game length

**Balance Levers**:
- Costs (acquisition price, upkeep, opportunity cost)
- Power (immediate effect, ongoing benefit, win condition contribution)
- Availability (scarcity, prerequisites, timing)
- Risk (variance, dependencies, counter-play)

**Handling Runaway Leaders**:
- Catch-up mechanisms (bonus for trailing players)
- Diminishing returns on accumulated advantage
- Player interaction as natural balancing (targeting the leader)
- Hidden scoring until game end

### 5. Playtesting Methodology

Playtesting is iterative, time-consuming, and essential:

**Phase 1: Solo Testing**
- Test core loop alone
- Verify basic mechanics work
- Identify obvious broken strategies
- Goal: Does the game function?

**Phase 2: Guided Testing**
- Play with interested friends/colleagues
- Watch for dominant strategies and unexpected behavior
- Begin mechanical balancing
- Goal: Is the game playable and interesting?

**Phase 3: Blind Testing**
- External playtesters with no guidance
- Observe without intervening
- Test rulebook clarity
- Goal: Can people learn and enjoy it independently?

**Best Practices**:
- Observe behavior, don't just ask opinions (actions reveal more than words)
- Track specific metrics: game length, decision time, win rates
- Change one variable at a time when iterating
- Distinguish "perceived balance" from actual balance
- Feedback loop: implement → test → analyze → repeat

### 6. Rules Documentation

Clear rules prevent confusion and arguments:

- **Organize by Phase/Turn Structure**: Players should find rules in play order
- **Define Terms Early**: Establish vocabulary before using it
- **Handle Edge Cases**: Anticipate conflicts and provide resolution
- **Include Examples**: Concrete illustrations of abstract rules
- **Create Quick Reference**: Summary card for experienced players
- **Cross-Reference**: Link related sections for easy navigation
- **Playtest the Rulebook**: Rules are a product that needs testing too

## Supporting Resources

This skill includes reference files in `references/`:

- `eurogame-principles.md` - Deep dive on German-style design philosophy
- `balance-methodology.md` - Systematic approaches to game balance
- `design-checklist.md` - Validation checklist for complete game designs

## When This Skill Activates

Claude uses this skill when you:

- Request help designing a new game or game system
- Ask for balance analysis of existing mechanics
- Want to design or validate asymmetric factions
- Need help with resource economy design
- Ask for rules clarity review
- Request playtesting methodology guidance
- Ask about making a game "more fun" or "more engaging"

## Example Workflows

### Example: Designing a New Resource System

When asked "How should I design an engineer economy?":

1. Define the resource's role (what does it enable?)
2. Identify sources (how are engineers acquired?) and costs
3. Identify sinks (how are engineers consumed/spent?)
4. Create scarcity tension (never enough for everything)
5. Add trade-offs (using engineers for X means not using them for Y)
6. Model mathematically (income vs. consumption over game length)
7. Design focused playtest to validate

### Example: Balancing Asymmetric Factions

When asked "Is faction X balanced?":

1. List faction's unique abilities and constraints
2. Compare power level to other factions' abilities
3. Identify intended trade-offs (what's the cost of the benefit?)
4. Check for unintended synergies or exploits
5. Review win rate data if available
6. Suggest adjustments if needed (dial up/down specific abilities)
7. Design faction-focused playtest scenarios

### Example: Making a Mechanic More Engaging

When asked "This part of the game feels boring":

1. Identify the specific mechanic/phase in question
2. Analyze: Is there meaningful choice? Tension? Consequence?
3. Check pacing: Too slow? Too predictable?
4. Look for "grinding" (repetitive actions without interesting decisions)
5. Consider adding: scarcity, trade-offs, player interaction, or stakes
6. Propose targeted changes that preserve overall design
7. Plan A/B playtest comparing old vs. new version
