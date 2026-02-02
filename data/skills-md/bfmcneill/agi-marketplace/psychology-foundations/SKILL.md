---
name: psychology-foundations
description: Use when you need to understand WHY certain UX patterns work. Covers cognitive psychology, behavioral science, and neuroscience foundations that underpin satisfying experiences.
---

# Psychology Foundations

Understanding *why* patterns work lets you apply them to new situations. These are the research foundations beneath UX practice.

## About This Skill

This skill contains **research-backed principles only**. Each concept includes:
- The original researcher(s)
- Year of key publication(s)
- What the research actually showed
- Limitations or caveats where relevant

---

## 1. Dopamine and Anticipation

**Researchers:** Wolfram Schultz (1990s), Robert Sapolsky
**Field:** Neuroscience

### What Research Shows

Dopamine neurons fire in response to **prediction of reward**, not reward itself. When a reward is expected and received, dopamine levels don't spike at reward time—they spike at the cue predicting the reward.

Schultz's experiments with monkeys showed:
- Unexpected reward → dopamine spike at reward
- Expected reward (after learning) → dopamine spike at predictor, not reward
- Expected reward that doesn't come → dopamine dip (disappointment)

### UX Implication

Progress indicators work because they signal approaching reward. The anticipation phase is neurologically active.

**Source:** Schultz, W. (1998). Predictive reward signal of dopamine neurons. *Journal of Neurophysiology*.

---

## 2. Peak-End Rule

**Researchers:** Daniel Kahneman, Barbara Fredrickson
**Field:** Behavioral economics, Psychology
**Recognition:** Nobel Prize in Economics (2002)

### What Research Shows

In studies of colonoscopies and other experiences, participants rated overall experience based on:
1. The **peak** moment (most intense)
2. The **end** moment

Duration had little effect ("duration neglect"). A longer painful experience ending gently was rated better than a shorter one ending abruptly.

### UX Implication

- Create one memorable positive peak
- End interactions well
- A graceful error recovery can redeem a frustrating experience

**Source:** Kahneman, D. et al. (1993). When more pain is preferred to less. *Psychological Science*.

---

## 3. Loss Aversion

**Researchers:** Daniel Kahneman, Amos Tversky
**Field:** Behavioral economics
**Recognition:** Foundational to Prospect Theory (Nobel Prize 2002)

### What Research Shows

Losses loom larger than gains. In experiments, losing $10 felt roughly **2x as bad** as gaining $10 felt good. This asymmetry affects decision-making: people take irrational risks to avoid losses.

### UX Implication

- Data loss is disproportionately frustrating
- Auto-save, undo, and preservation matter more than features
- Frame choices in terms of what users might lose

**Source:** Kahneman, D. & Tversky, A. (1979). Prospect Theory: An Analysis of Decision under Risk. *Econometrica*.

---

## 4. Flow State

**Researcher:** Mihaly Csikszentmihalyi
**Field:** Positive psychology
**Timeline:** Research from 1970s, book *Flow* published 1990

### What Research Shows

Csikszentmihalyi interviewed hundreds of experts (artists, athletes, surgeons, chess players) about their optimal experiences. Common characteristics:

| Condition | Description |
|-----------|-------------|
| Clear goals | Know what success looks like |
| Immediate feedback | See results of actions |
| Challenge-skill balance | Task matches ability |
| Sense of control | Autonomy over actions |

When conditions are met, people report:
- Deep concentration
- Loss of self-consciousness
- Distorted time perception
- Intrinsic reward from the activity itself

### Limitations

- Original research was qualitative (interviews, experience sampling)
- "Challenge-skill balance" is hard to operationalize
- Neurophysiological validation is still emerging

**Source:** Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*.

---

## 5. Cognitive Load Theory

**Researcher:** John Sweller
**Field:** Educational psychology
**Timeline:** Theory developed 1988

### What Research Shows

Working memory has limited capacity. Sweller identified three types of cognitive load:

| Type | Description | Reducible? |
|------|-------------|------------|
| **Intrinsic** | Complexity inherent to the task | No (task-dependent) |
| **Extraneous** | Load from poor presentation | **Yes** (design target) |
| **Germane** | Load that aids learning | Desirable |

Instructional design should minimize extraneous load to free capacity for intrinsic and germane processing.

### UX Implication

- Reduce visual clutter
- Group related information
- Use familiar patterns
- Don't make users remember across screens

**Source:** Sweller, J. (1988). Cognitive load during problem solving. *Cognitive Science*.

---

## 6. Miller's Law (Working Memory Limits)

**Researcher:** George Miller
**Field:** Cognitive psychology
**Year:** 1956

### What Research Shows

Miller's famous paper "The Magical Number Seven, Plus or Minus Two" found people can hold approximately 7±2 "chunks" in working memory.

### Limitations

**Important:** Modern research suggests the number may be closer to **4±1 chunks** for novel information (Cowan, 2001). Miller's "7" applies to well-practiced, chunked material.

### UX Implication

- Limit simultaneous options
- Group items into meaningful chunks
- Don't rely on users remembering many items

**Sources:**
- Miller, G.A. (1956). The magical number seven. *Psychological Review*.
- Cowan, N. (2001). The magical number 4 in short-term memory. *Behavioral and Brain Sciences*.

---

## 7. Serial Position Effect

**Researcher:** Hermann Ebbinghaus
**Field:** Memory research
**Year:** 1885

### What Research Shows

When recalling lists, people remember:
- **First items** (primacy effect) — transferred to long-term memory
- **Last items** (recency effect) — still in working memory
- Middle items are poorly recalled

### UX Implication

- Put important items first or last
- Don't bury critical information in the middle
- First impressions and final interactions matter most

**Source:** Ebbinghaus, H. (1885). *Über das Gedächtnis* (On Memory).

---

## 8. Zeigarnik Effect

**Researcher:** Bluma Zeigarnik
**Field:** Gestalt psychology
**Year:** 1927

### What Research Shows

Interrupted tasks are remembered better than completed ones. The mind keeps incomplete tasks "open" in memory.

### Limitations

**Caution:** Replication studies have been mixed. The effect appears real but smaller and more context-dependent than originally claimed.

### UX Implication

- Progress indicators leverage incompleteness
- Unfinished onboarding motivates return
- But: incomplete tasks also create cognitive burden

**Source:** Zeigarnik, B. (1927). Über das Behalten von erledigten und unerledigten Handlungen. *Psychologische Forschung*.

---

## 9. Choice Overload (Paradox of Choice)

**Researchers:** Sheena Iyengar, Mark Lepper
**Field:** Decision-making psychology
**Year:** 2000

### What Research Shows

The famous "jam study": shoppers shown 24 jam varieties were less likely to purchase than those shown 6 varieties. More choice led to decision paralysis.

### Limitations

**Important:** Meta-analyses (Scheibehenne et al., 2010) found the effect is **smaller and more context-dependent** than popularized. Choice overload occurs under specific conditions:
- Unfamiliar domain
- Difficult to compare options
- No clear preference
- High decision stakes

### UX Implication

- Reduce options when users lack expertise
- Provide smart defaults
- But: experts may want more choices

**Sources:**
- Iyengar, S. & Lepper, M. (2000). When choice is demotivating. *Journal of Personality and Social Psychology*.
- Scheibehenne, B. et al. (2010). Can there ever be too many options? *Journal of Consumer Research*.

---

## Laws of UX (Quick Reference)

These are practitioner heuristics with varying levels of research backing:

| Law | Principle | Evidence Level |
|-----|-----------|----------------|
| **Hick's Law** | Decision time increases with options | [Research] |
| **Fitts's Law** | Larger, closer targets are easier to hit | [Research] |
| **Miller's Law** | ~7±2 items in working memory | [Research] (with caveats) |
| **Jakob's Law** | Users expect familiar patterns | [Expert] NNg |
| **Aesthetic-Usability** | Pretty things seem more usable | [Research] |
| **Postel's Law** | Be liberal in input, strict in output | [Expert] |

**Source:** [Laws of UX](https://lawsofux.com/)

---

## Key Sources

- Schultz, W. (1998). Predictive reward signal of dopamine neurons.
- Kahneman, D. & Tversky, A. (1979). Prospect Theory.
- Kahneman, D. (1993). When more pain is preferred to less.
- Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*.
- Sweller, J. (1988). Cognitive load during problem solving.
- Miller, G.A. (1956). The magical number seven.
- Cowan, N. (2001). The magical number 4 in short-term memory.
- Ebbinghaus, H. (1885). *Über das Gedächtnis*.
- Iyengar, S. & Lepper, M. (2000). When choice is demotivating.
- Scheibehenne, B. et al. (2010). Can there ever be too many options?
