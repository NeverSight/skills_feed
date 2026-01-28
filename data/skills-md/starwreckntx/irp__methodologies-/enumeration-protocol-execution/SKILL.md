---
name: enumeration-protocol-execution
description: Enforce a Divergent-Convergent Scan loop to overcome 'Prevalent Noun Bias' and statistical probability reflexes (System 1).
version: 1.0.0
---

## Description
This protocol serves as a "Cognitive Brake." It is invoked when high precision is required or when the initial answer seems "too obvious" (high probability/low compute). It forces the agent to suspend the final answer, scan the entire search space for low-probability candidates, and perform an inversion test before converging on a selection.

## Instructions

### Step 1: Divergent Scan (The Silent Survey)
Before formulating the final response, generate an internal list of 3-5 distinct candidates that fit the user's criteria.
* **Constraint:** You are FORBIDDEN from selecting the first candidate that comes to mind.
* **Search Target:** Look for "Background Objects," "Structural Elements," or "Counter-Intuitive Solutions."

### Step 2: Bias Identification
Review the generated list and identify the "Statistical Default."
* *Question:* "Which of these candidates would an average human or standard model pick 90% of the time?"
* *Action:* Flag this candidate as `[BIAS_DEFAULT]`.

### Step 3: The Inversion Test
Challenge the `[BIAS_DEFAULT]`.
* *Question:* "Why might this obvious answer be a decoy or incorrect?"
* *Action:* Check for exclusion criteria (e.g., user said 'Nope', context implies a trick, visual obstruction).

### Step 4: Convergence & Selection
Select the final answer based on **Contextual Fit** rather than **Saliency**.
* If the `[BIAS_DEFAULT]` survives the Inversion Test, output it.
* If it fails, promote the highest-ranked alternative (e.g., the 'Dolly' instead of the 'Hat').

## Examples

- "Engage enumeration protocol for this visual puzzle."
- "Execute enumeration scan to debug this code block (avoiding standard library assumptions)."
- "Run enumeration-protocol-execution on the error logs."
