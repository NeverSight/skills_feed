---
name: salvador
description: Autonomous p5.js visualization agent. It implements, inspects, critiques design/UX, fixes, and launches the result.
---

# Salvador Agent
Use this skill to visualize concepts using p5.js with a focus on **high-quality UX, aesthetics, and continuous motion**.

## Workflow
Follow this **strict loop** when asked to visualize a concept:

### Phase 1: Bootstrap
1.  **Check Context**: If `package.json` is missing, run `bash .claude/skills/salvador/scripts/setup.sh`.
2.  **Scaffold**: Ensure `index.html` and `src/main.js` exist.
3.  **Read p5.js Reference**: Read `resources/p5-missing-knowledge.md` for p5.js 2.x API changes before writing any code.
4.  **Read Responsive Design**: Read `resources/responsive-design.md` for the scale factor pattern.

### Phase 1.5: Concept Analysis (Before Coding!)

This visualization needs to teach and reflect the concept that I was asked to visualize.
Therefore, make sure to include details so the user (who can be a child, adult, expert, or novice) can understand the concept well.

Before writing any code, decompose the concept:

1. **Research the Domain**: Look up the actual facts (angles, counts, formulas, rules)
   - Don't guess scientific/mathematical details
   - Get the real values (e.g., H2O bond angle is 104.5°, not "about 109°")

2. **Break Into Stages**: Most concepts can be shown as a progression:
   - What is the "before" state?
   - What are the intermediate transformation steps?
   - What is the "final" state?
   - Aim for 3-5 stages that build understanding

3. **Identify Dynamic Elements**: What moves in this system?
   - Do NOT make a visualization of a static snapshot, everything moves in the Universe
   - Even if the concept has "stages," the actors must be alive (e.g., electrons orbiting, atoms vibrating, lists scanning).
   - be DETAILED. for example if certain electrons will be bonding, find out which ones (e.g., certain valence electrons) and highlight them visually. this of course does not just apply to Chemistry, but to any domain (e.g., in sorting algorithms, show which elements are being compared/swapped at each step)

4. **Identify What Needs Explanation**: What text/labels/diagrams would help?
   - Key terms to define
   - Quantities to show
   - Relationships to highlight

### Phase 1.6: Stage Design Principles

5. **Living Systems**: The system must breathe.
   - **Idle Animation**: Even when waiting for user input, nothing should be perfectly frozen.
   - **Continuous Time**: Use `draw()` to animate physics/logic continuously. `noLoop()` is forbidden.

6. **Granular Transitions**: Never skip the "moment of change"
   - BAD: "state A" → "state B" (viewer misses the transformation)
   - GOOD: "state A" → "approaching change" → "moment of change" → "state B"
   - Rule: if two stages feel like a big jump, add an intermediate stage
   - Examples:
     * Sorting algorithm: show each comparison/swap, not just "unsorted → sorted"
     * Chemical bond: show atoms approaching before showing them bonded
     * Mathematical proof: show each logical step, not just premise → conclusion

7. **Trackability**: When elements transform or move, viewers must follow them
   - Assign distinct colors to individual components at the start
   - Maintain those colors through all stages
   - Link details, configurations, numbers, strings, etc.. visually to their representations
   - Make it obvious which element went where, became what, or combined with whom
   - Examples:
     * In a merge sort: color the two halves differently so viewer tracks them through merges
     * In a state machine: color each state and show transitions with matching colors
     * In molecular bonding: color each atom's electrons to show which ones get shared

8. **Data Cards**: Show the underlying facts, not just the visual
   - Include domain notation (formulas, equations, configurations, pseudocode)
   - Display quantities, measurements, and labels using proper terminology
   - Cards can appear/disappear based on stage relevance
   - Examples:
     * Physics: show F=ma card when demonstrating force
     * Music: show chord notation (Cmaj7) alongside the visual
     * Chemistry: show electron configuration (1s² 2s² 2p⁴)
     * Algorithms: show Big-O complexity or current array state

### Phase 2: Autonomous Loop (The "Work")
Repeat this cycle until the visualization is **High Quality**:

1.  **Implement/Refine**: Write `src/main.js`.
    * *Constraint*: Use a modern color palette (avoid default pure RGB).
    * *Constraint*: For conceptual visualizations, use **progressive revelation**:
      - Build an interactive stepper (← →) through stages
      - Show info panels/cards explaining each stage
      - **Critical**: Animate transitions between states (slide/flow/morph)
    * *Constraint*: **Continuous Motion**: Ensure `draw()` runs continuously. Even in a "Step 1" static state, show micro-movements (vibration, orbit, pulse).
    * *Constraint*: Include **educational elements**:
      - Labels for key components
      - Brief text descriptions of what's happening
      - Visual indicators (badges, diagrams) for important values
    * *Constraint*: Use **domain-accurate** values, not approximations
    * *Constraint*: Ensure text is readable and has high contrast.
    * *Constraint*: Support interactions (mouse drag, click, or keyboard shortcuts).
    * *Constraint*: **Canvas sizing**: Use 850x540 or smaller to fit without scrolling
    * *Constraint*: **Keyboard handling**: Use `window.addEventListener('keydown')` for arrow keys (and map 'G' to `saveGif`).
    * *Constraint*: **Track elements visually**: Color-code components that transform and maintain those colors throughout all stages.
2.  **Inspect**: Run `node inspect.js`
3.  **Critique**:
    * **Logs**: Are there errors?
    * **Visual Audit**: Open *all* generated snapshots (e.g., `stage_1.png`, `stage_2.png` ... `final.png`) and strictly evaluate the sequence:
        * **Completeness**: Do not evaluate just the final frame. Check the evolution. Did the visualization break or glitch in the middle?
        * **Life Check**: Is it moving/evolving? (Reject if the sequence looks like a static slide).
        * **Composition**: Is the content centered? Is it cut off in *any* frame?
        * **Legibility**: Is there text overlap? Is the font size appropriate throughout?
        * **Aesthetics**: Does it look "engineered" or "designed"? (Aim for designed).
        * **UX**: Did I implement user controls (e.g., "Press 'R' to reset")?
4.  **Decide**:
    * *Errors?* -> Fix code -> **Repeat**.
    * *Static/Boring?* -> **Add Micro-Movement (vibration, orbits)** -> **Repeat**.
    * *Physics/Logic Broken?* (e.g. Gravity creates energy, sorting fails) -> **Fix Simulation Logic** -> **Repeat**.
    * *Missing Educational Context?* -> **Add Labels/Data Cards** -> **Repeat**.
    * *Amazing, Dynamic & Physically Accurate?* -> **Proceed to Phase 3**.

### Phase 3: Presentation (The "Reveal")
Once the loop is complete and the visualization is polished:
1.  **Launch**: Run `npx vite --open`.
2.  **Notify**: Tell the user "Visualization is ready. Controls: [List controls here]."
