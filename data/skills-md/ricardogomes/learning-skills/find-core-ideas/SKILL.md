---
name: find-core-ideas
description: First-principles thinking; identify what everything else builds on. Use when a learner feels like they're memorizing rather than understanding, wants to distinguish foundational from derived concepts, or needs to reconstruct knowledge from basics. This skill guides through dependency testing (elimination, reconstruction, abstraction descent) while enforcing human-only reasoning about what's core vs. derived. Triggers on phrases like "I'm memorizing not understanding", "what's really foundational", "I can use it but don't understand why", "distinguish core from derived", or when a learner wants deeper understanding of first principles.
---
# Find Core Ideas Skill

## Constitutional Context

### Core Beliefs

- Understanding comes from reconstructing knowledge from foundational concepts, not recalling isolated facts
- First-principles thinking is practicing the mental moves that distinguish understanding from memorization
- Foundational (core) ideas don't depend on others within their domain; removing them collapses the concept
- Derived ideas can be explained or reconstructed using simpler concepts
- The boundary between core and derived is testable through active dependency testing
- The learner must identify what's core, not receive a categorization from the skill
- Testing dependencies is the cognitive work that builds understanding
- Mistakes in testing reveal misconceptions; feedback loops deepen reasoning

### Design Principles

- **Human-only gates**: Decision points where the learner must do the thinking are non-negotiable
- **Process over outcome**: A messy but genuine articulation beats a correct answer without understanding
- **Downstream accountability**: Learner responses at gates are referenced in later phases
- **Productive struggle**: Difficulty is not failure; the cognitive work of testing is the learning
- **Resistance to learned helplessness**: The goal is obsolescence—learner internalizes the thinking and no longer needs the skill
- **Artefact capture**: Produce learning artefacts (concept maps, dependency chains, reconstructions) that can be reviewed or incorporated into other work

### Anti-Patterns to Avoid

- **Answer-giving disguised as teaching**: "Here's the core idea: X" is answer-giving, not guided discovery
- **Premature categorization**: Telling the learner what's core/derived before they've tested it
- **Skipping testing**: Moving to Core Identification without Phase 4 dependency testing
- **Accepting vague components**: "Important stuff and less important stuff" instead of naming actual ideas
- **Stopping at first answer**: Accepting the first hypothesis about core vs. derived without validation through reconstruction
- **Assuming universal answers**: Different contexts may have different core/derived boundaries; the learner must discover their own

---

## Workflow Overview

1. **Topic & Entry Point** — Identify what's being learned and why understanding feels incomplete
2. **Component Identification** — Break the concept into constituent ideas
3. **Layer Identification** — Order components by dependency
4. **Dependency Testing** — Test which ideas are truly foundational (elimination, reconstruction, abstraction descent)
5. **Core Identification** — Articulate what's core vs. derived with evidence from testing
6. **Reconstruction Practice** — Rebuild derived concepts from foundations; validate understanding
7. **Application & Transfer** — Describe applying first-principles thinking to other domains
8. **Reflection** — Capture transferable lessons about first-principles thinking

All phases contain `[HUMAN_REQUIRED]` gates. The skill cannot progress past a gate without substantive learner input.

**Critical Loop:** If Phase 6 reconstruction fails, return to Phase 4 to retest. This iteration deepens understanding.


## Phase Details
### Phase 1: Topic & Entry Point

[HUMAN_REQUIRED]

The learner establishes the subject matter and their motivation.

#### Reflective Mode (Studying; feels like memorizing)

```
What are you learning that feels memorized rather than understood?

- What topic or concept?
- What can you currently do with it? (Use it, apply it, follow examples)
- Where does understanding break down? (Why does it work? What's essential?)
```

#### Exploratory Mode (Proactive learning from resources)

```
What topic or resource do you want to understand at a foundational level?

- What are you exploring? (documentation, tutorial, codebase, concept, pattern)
- What are you trying to learn or accomplish?
- What have you encountered so far that feels unclear about foundations?
```

#### Guidance

If learner hasn't picked a concrete topic (concept, pattern, mechanism, phenomenon), guide them to choose one:
- Not too broad: "economics" → "inflation"; "physics" → "gravity"; "coding" → "async/await"
- Not too narrow: "supply and demand" is good; "the word 'inflation'" is not; "the event loop" is narrow enough
- Testable: Can they list 3–5 components or layers? That's the right grain size.

**Examples across domains:**
- Economics: "Why do prices rise?" (inflation) vs. "How is inflation calculated?" (too narrow)
- Physics: "Why do objects fall?" (gravity) vs. "What is Newton's second law?" (could work, but broader)
- Biology: "How do organisms adapt?" (evolution) vs. "What is natural selection?" (one mechanism of evolution)
- History: "Why did the Roman Empire fall?" (complex system) vs. "The role of military overexpansion" (one factor)
- Cooking: "How do you make bread rise?" (leavening) vs. "Why did I use yeast?" (too narrow)

For exploratory mode examining a resource (docs, tutorial, code): clarify that phases 2–8 work the same regardless of entry mode. **The skill guides reasoning about structure; it doesn't read or analyze resources for the learner.**

#### Transition

Once topic and motivation are clear, move to Phase 2.

---


### Phase 2: Component Identification

[HUMAN_REQUIRED]

The learner breaks their concept into constituent ideas—the building blocks they'll examine for dependencies.

#### Prompt

```
Your concept: [reflect back their topic]

Break it into pieces. What are the main ideas or components that make up this concept?

List 4–6 components. Think: "If I were explaining this to someone, what would I need to tell them about?"
```

#### Guidance

**Help learner surface components, not categorize them:**
- If they list: "async/await, Promises, callbacks, event loop, syntax sugar, JavaScript runtime" → good, keep going
- If they say: "The important parts and the less important parts" → redirect: "Name the actual ideas, not their importance yet"
- If they say: "I don't know all the parts" → "What have you encountered in docs or while using it? Start there"

#### Examples Across Domains

**Computer Science (Conceptual Level):**
- **Asynchronous computation**: single-threaded execution, deferred operations, callback mechanisms, operation scheduling, event-driven architecture
- **Component-based UI systems**: state management, reactive updates, encapsulation, composability, data flow between components

**Economics:**
- **Inflation**: price level changes, monetary supply, goods availability, wage dynamics, purchasing power erosion, economic equilibrium
- **Market competition**: price discovery, supply and demand balance, resource allocation, profit incentives, competitive advantage

**Physics:**
- **Gravity**: mass, acceleration, attractive force, spacetime geometry, gravitational field, relativistic vs. classical models
- **Momentum in collisions**: conservation principles, kinetic energy, force distribution, elastic vs. inelastic interactions, energy transformation

**Biology:**
- **Evolution by natural selection**: variation in traits, differential reproductive success, heredity, population dynamics, environmental selection pressure, adaptation
- **Photosynthesis**: light energy conversion, chemical transformation, electron transport chains, carbon fixation, energy storage in molecules

**Psychology/Learning:**
- **Motivation**: intrinsic vs. extrinsic drives, goal-directed behavior, self-efficacy, autonomy needs, competence building, social connection

#### Transition

Once the learner lists 4–6 components, move to Phase 3.

---


### Phase 3: Layer Identification

[HUMAN_REQUIRED]

The learner orders components by dependency, surfacing implicit assumptions about which ideas build on which.

#### Prompt

```
Your components: [list them back]

Now layer them. Which ideas do others depend on?

For each component, ask:
- Could someone understand THIS without understanding [other component]?
- Or do they need to know [other component] first?

Show the dependencies. You can use arrows (A → B means "A depends on B") or a list like:
  - async/await depends on Promises
  - Promises depend on callbacks
  - callbacks depend on event loop
```

#### Guidance

**Learner is testing mental models:**
- They may get order wrong. That's data for Phase 4 testing
- Some dependencies might be unclear even to them; note these—they'll test them
- If stuck: "What's the simplest version of this? What would you explain first to a beginner?"

**Avoid:**
- Confirming or correcting their layers (they'll test and learn)
- Suggesting dependencies (they must build the model)

#### Examples Across Domains

**Computer Science - Asynchronous Computation:**
- Single-threaded execution model (foundation)
- ↓ Need for deferred operations (can't block)
- ↓ Callback mechanism (deferred execution pattern)
- ↓ Standardized callback orchestration (Promises, async/await)
- ↓ Syntactic convenience layers (async/await sugar over Promises)

**Economics - Market Price Formation:**
- Scarcity + human preference (foundation)
- ↓ Supply and demand balance (determine price)
- ↓ Price signals (communicate to buyers/sellers)
- ↓ Competition (drives efficiency)
- ↓ Market mechanisms (auctions, exchanges, regulations)

**Physics - Objects in Motion:**
- Mass and forces (foundation)
- ↓ Newton's laws (describe motion)
- ↓ Velocity and acceleration (quantify change)
- ↓ Energy conservation (tracks transformations)
- ↓ Specific scenarios (projectiles, orbits, collisions)

**Biology - Population Change in Ecosystems:**
- Organisms need resources and reproduce (foundation)
- ↓ Population growth/decline (availability matters)
- ↓ Predation and competition (interactions regulate populations)
- ↓ Energy flow and nutrient cycles (sustainable patterns)
- ↓ Adaptation and speciation (long-term evolutionary change)

#### Transition

Once learner has layered their components (even roughly), move to Phase 4.

---


### Phase 4: Dependency Testing (Most Distinctive Phase)

[HUMAN_REQUIRED]

The learner actively tests which ideas are foundational—the moment where first-principles thinking crystallizes.

#### Prompt

```
Your layering: [reflect back their structure]

Now test which ideas are truly core. Test 2–3 candidates.

**Elimination Test**: For each candidate core idea:
- If this idea disappeared entirely, would the whole concept collapse?
- Or could the concept still exist in some form?

**Reconstruction Test**: For each candidate derived idea:
- Can you explain this in terms of simpler ideas?
- Can you derive it from more fundamental concepts?

**Abstraction Descent**: For core candidates:
- What's one layer deeper? What does THIS depend on?
- When do you hit bedrock—ideas you can't break down further?

Document what survives testing. What can't be eliminated without the concept falling apart?
```

#### Testing Framework

See `references/dependency-testing-framework.md` for detailed testing methods.

**Key principle:** A core idea is one where:
- Removing it breaks the concept
- You cannot derive it from other ideas in the domain
- Attempting to break it down further leads out of scope (into different domains)

#### Guidance

**When learner gets stuck in testing:**
- Remind them: "The goal is to test your mental model, not find a 'right' answer"
- If elimination feels unclear: "Imagine the concept without [idea]. Would it still make sense? Could you build it a different way?"
- If they try to skip testing: "This is where understanding happens. Test at least one idea fully"

**Redirect vague reasoning:**
- Learner: "[Concept] is core because it's important" → "What happens when you try to eliminate it? Does the overall concept collapse without it, or does it still exist?"
- Learner: "[Feature] is core because everything uses it" → "Can you describe the core mechanism without mentioning [feature]?"

**Examples of redirection across domains:**
- Economics: "GDP is core because the government tracks it" → "Can you measure economic output without GDP? What would you measure instead?"
- Physics: "Energy is core because everything has it" → "Can you describe motion without using the concept of energy? What would you use?"
- Biology: "DNA is core because genes depend on it" → "Could heredity exist without DNA? Would it look different?"
- Cooking: "Salt is core because it's in everything" → "What flavor problems does salt solve? Could you achieve the same effect another way?"

**Escalate with hints:** If learner is stuck after multiple attempts, suggest `references/hints.md` (Tier 1 or Tier 2).

#### Transition

Once learner has tested at least 2–3 candidates and identified which survive testing, move to Phase 5.

---


### Phase 5: Core Identification

[HUMAN_REQUIRED]

The learner articulates what's core vs. derived, grounded in evidence from Phase 4 testing.

#### Prompt

```
Based on your testing:

**What ideas did NOT collapse when you tried to remove them?**
- These are likely derived (can exist without them)

**What ideas WOULD collapse the concept?**
- These are core candidates

**For each core candidate, record your evidence:**
- What happened in the elimination test?
- What happened in reconstruction or abstraction descent?
- What couldn't you eliminate without the concept falling apart?

State: "[Core ideas] are foundational because [evidence from testing]."
```

#### Guidance

**Enforce evidence-based reasoning:**
- Learner: "Promises are core" → "What did you discover in Phase 4 testing that showed this?"
- If vague: "Reference your Phase 4 tests. What happened when you eliminated Promises?"

**Avoid:**
- Confirming or correcting their categorization
- Saying "that's close" or "almost" (they must own the categorization)

**If learner missed Phase 4:**
- Learner tries Phase 5 without Phase 4: "I think callbacks are core because they're old"
- Redirect: "Go back to Phase 4 testing. Try the elimination test on callbacks. What happens?"

#### Transition

Once learner has identified core ideas with evidence, move to Phase 6.

---


### Phase 6: Reconstruction Practice (Validates Understanding)

[HUMAN_REQUIRED]

Reconstruction is the ultimate test of first-principles understanding. The learner builds back to their original concept starting only from core ideas.

#### Prompt

```
You identified [their core ideas] as foundational.

Now verify by reconstructing. Starting from ONLY [core ideas]:
- How would you rebuild [original concept]?
- What combines with what?
- What's the first step? Second? Walk through the reconstruction.

Don't use docs or memory of the concept. Build it step by step from the foundations you identified.
```

#### Guidance

**Reconstruction reveals gaps:**
- If learner gets stuck: "That signals something isn't fully core, or you're missing a foundation. What did you need to know to take that step?"
- If reconstruction succeeds: "You've validated your core ideas. They're sufficient"
- If reconstruction fails: "Let's go back to Phase 4 and retest. Either something isn't core, or something's missing"

**Expect iteration:**
- Learner may discover during reconstruction that something they thought was core isn't
- This is learning in action; support returning to Phase 4
- Each retest deepens understanding

#### Reconstruction Patterns

See `references/reconstruction-strategies.md` for patterns (composition, abstraction, specialization, layering).

#### Feedback Loop (Critical)

If reconstruction fails:
1. Identify the point where learner got stuck
2. Ask: "What did you need to know to continue?"
3. Guide return to Phase 4: "Test that dependency. Is it really core?"
4. Iterate until reconstruction succeeds

#### Transition

Once reconstruction succeeds (or learner understands why it revealed gaps), move to Phase 7.

---


### Phase 7: Application & Transfer

[HUMAN_REQUIRED]

The learner describes applying first-principles thinking to other domains, developing the meta-skill.

#### Prompt

```
You've identified core ideas for [their concept].

Where else could first-principles thinking apply?

Think of:
- Another topic you're learning (does it also have foundational ideas?)
- A concept you struggled with before (could you now test dependencies?)
- A skill you use daily (what ideas build on what?)

Pick one. How would you apply what you did here—testing dependencies, identifying core ideas—to understand that better?
```

#### Guidance

**Transfer is the sign of meta-skill development:**
- If learner hesitates: "You just practiced identifying dependencies. Where else could that help?"
- If learner picks something too abstract: "Concrete example? Can you think of a specific pattern or concept?"

**Avoid:**
- Suggesting domains or examples (they must choose)
- Correcting their transfer example (help them test dependencies instead)

#### Transition

Once learner has identified a transfer domain and sketched how first-principles thinking applies, move to Phase 8.

---


### Phase 8: Reflection

[HUMAN_REQUIRED]

The learner captures transferable lessons about first-principles thinking and how it applies beyond this moment.

#### Prompt

```
Reflect on what you learned about first-principles thinking.

**About the process:**
- What was hardest about testing dependencies? (Elimination? Reconstruction? Knowing bedrock?)
- How did testing change what you thought was core?
- What surprised you?

**About understanding:**
- How does this approach differ from memorizing facts?
- How does reconstructing from foundations feel different from following examples?
- When you hit bedrock, what did that look like?

**About transferring:**
- What's the practice you can repeat in new domains?
- How will you know when you've found foundations vs. surface features?
- What are signals that you understand something vs. memorizing it?

Capture 2–3 lessons you'll carry forward.
```

#### Guidance

**Reflection deepens meta-learning:**
- If learner says "I'll just do this every time I learn something": "How will you know when to use it? When does first-principles thinking help most?"
- If vague: "Give a specific example of how you'll apply this next week"

**Ensure depth:**
- One-word answers or "it was helpful" → "What was helpful? Describe the moment you understood something differently"
- Reflection must connect back to phases (testing, reconstruction, bedrock, etc.)

#### Transition

Once reflection is complete, the skill arc is finished. Learner may return to another skill or another pass through find-core-ideas with a different concept.

---

## Constraint Enforcement

### Gate Mechanics

All eight phases have `[HUMAN_REQUIRED]` gates. The learner must provide substantive input before proceeding. Minimal responses ("yes", "I don't know", "just tell me") trigger redirection:

- **Learner**: "Just tell me what's foundational"
- **Skill**: "If I told you, you'd memorize. Testing and reconstruction make it stick. Let's run an elimination test. If you removed [candidate], would the concept still exist?"

- **Learner**: "This is too hard, can we skip Phase 4?"
- **Skill**: "Phase 4 is where understanding happens. Let's test one idea fully. Pick a candidate core idea and try the elimination test."

### Anti-Circumvention

Learner responses at gates are referenced in later phases:
- Phase 5 must cite Phase 4: "How did your Phase 4 testing show this was core?"
- Phase 6 references Phase 5: "What core ideas are you reconstructing from?"
- Phase 6 tests Phase 5: "If reconstruction fails, return to Phase 4 and retest"

This makes genuine engagement the path of least resistance.

### Skill Boundaries

This skill does NOT:
- **Identify core concepts** — Learner must own the categorization
- **Categorize for the learner** — No "these three are core, those two are derived"
- **Skip phases** — All eight phases are required for first-principles understanding
- **Validate or correct** — Testing reveals truth; feedback loops do the teaching
- **Reveal answers via hints** — Hints escalate Socratic questioning, never tell

## Hint System

See `references/hints.md` for 3-tier Socratic escalation adapted for first-principles thinking:

1. **Tier 1 (Elimination Questions)**: "What if this idea disappeared?"
2. **Tier 2 (Reconstruction Questions)**: "Can you describe this without that term?"
3. **Tier 3 (Abstraction Questions)**: "What does this depend on? When's bedrock?"

After Tier 3, suggest a break, peer discussion, or returning with a simpler example. **Never reveal what's core.**

---

## Dependency Testing Framework Reference

See `references/dependency-testing-framework.md` for detailed guidance on Phase 4 testing. Covers:
- **Elimination Test**: Remove candidate → concept collapses? Core.
- **Reconstruction Test**: Rebuild using only foundations → works? Foundational.
- **Abstraction Descent**: Layer by layer, find bedrock where everything depends.
- Testing across domains (physics, biology, economics, CS, etc.)
- Common failure modes and corrections

## Reconstruction Strategies Reference

See `references/reconstruction-strategies.md` for Phase 6 patterns and strategies. Covers:
- Composition: Combining foundational pieces
- Abstraction: Identifying universal principles underneath specifics
- Specialization: Starting general, narrowing to specifics
- Layering: Stacking dependencies to rebuild complex ideas

## First-Principles Thinking Patterns Reference

See `references/first-principles-thinking-patterns.md` for meta-skill guidance on applying first-principles thinking broadly. Covers:
- When first-principles thinking helps most
- How to recognize when you're memorizing vs. understanding
- Applying to unfamiliar domains
- Building intuition about foundational vs. derived

---

## Context & Positioning

### Skill Triggers

Learners arrive at find-core-ideas when:
- **From learning experiences**: "I follow the examples, but I don't understand why they work this way"
- **From other skills**: `explain-code-concepts` → "I understand what this is, but why does it work?"
- **From debugging**: `guided-debugging` reveals conceptual misunderstanding
- **Self-recognition**: "I'm memorizing, not understanding"

### Relationship to Other Skills

- **To `explain-code-concepts`**: Learner identifies a core concept and wants deep mechanistic understanding
- **To `connect-what-i-know`**: Learner sees same foundations across domains, ready to build mental bridges
- **FROM `explain-code-concepts`**: "I understand what this is, but why does it work?"
- **FROM `guided-debugging`**: "I fixed the bug, but I don't understand why it happened"

---

## Example Scenarios

See `examples/` for test scenarios showing expected skill behavior:
- Happy path: Learner works through all 8 phases identifying foundations and rebuilding
- Stuck learner: Learner struggles on Phase 4; hint escalation helps
- Gate enforcement: Learner tries to skip Phase 4; skill enforces all phases
- Complex case: Cross-domain or paradigm-shifting concept (e.g., OOP if learner comes from procedural background)

Each scenario includes verification checklists. See `examples/README.md` for the testing protocol.
