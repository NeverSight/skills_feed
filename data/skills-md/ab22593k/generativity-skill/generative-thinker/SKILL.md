---
name: generative-thinker
description: Guides the agent to apply Generativity Theory to solve problems by building high-leverage, open-ended systems. Use this skill when the user asks for "out of the box" ideas, platform strategies, or when a task benefits from enabling others to innovate rather than providing a narrow, single-purpose fix.
---

# Generative Thinker

## Overview

This skill enables you to apply the principles of **Generativity Theory** to shift from "solving a specific problem" to "building a platform for others to solve problems." It is based on the philosophy of "The Generativity Advantage," which prioritizes unpredicted value creation through open, adaptable, and high-leverage systems.

## Core Principles

When using this skill, you must prioritize these "Generative Filters":

1.  **Meta-Problem Solving**: Instead of asking "How do I fix X?", ask "How do I create a system where *anyone* can fix X (and Y, and Z)?"
2.  **Surprise as a Feature**: Success is defined by users doing things with your solution that you never predicted.
3.  **Low Barrier, High Ceiling**: Make it trivial to start (Ease of Mastery) but powerful enough to support complex innovation (Leverage).
4.  **Embrace the Mess**: Accept that uncoordinated innovation is noisy and uncontrolled. Do not "over-optimize" for a single use case if it limits others.

## Generative Workflow

Follow these steps when tasked with "generative" or "out-of-the-box" thinking:

### 1. Evaluate Against the 6 Dimensions
Refer to [references/generativity_concepts.md](references/generativity_concepts.md) for detailed definitions. Rate your proposed solution on:
- **Leverage**: Can it be used for 10+ different things?
- **Adaptability**: How hard is it for a user to change its behavior?
- **Ease of Mastery**: Can a beginner get a "win" in 5 minutes?
- **Accessibility**: Is it free/open/accessible?
- **Transferability**: Can users share their "remixes"?
- **Profitability**: Can the user make money or gain status from their innovation?

### 2. Identify the "Laundry Buddy" Moment
In "The Generativity Advantage," OpenAI's creators were surprised by "Laundry Buddy" (a simple use case for a complex AI). 
- Identify a "mundane" or "silly" use case for your solution. If your solution *can't* do something mundane, it might be too narrow.
- Ensure your architecture doesn't block "GPT Wrappers"—simple layers of value on top of your tool.

### 3. Design the Flywheel
Plan how the solution will grow:
1.  **Attract**: What is the "hook" for innovators?
2.  **Innovate**: What "boundary resources" (API, documentation, templates) do they need?
3.  **Capture**: How do you ensure the platform stays sustainable while the innovators get rich?

## Examples of Generative Thinking

### Case A: Narrow vs. Generative Code
- **Narrow Fix**: Write a script to rename all `.txt` files to `.md`.
- **Generative Fix**: Write a generic "File Transformer" framework that takes a "Matching Pattern" and a "Transformation Function." Provide 3 examples (renaming, header injection, content cleanup).

### Case B: Narrow vs. Generative UI
- **Narrow UI**: A dashboard with 5 fixed charts.
- **Generative UI**: A "Widget Canvas" where users can drag-and-drop components and connect them to data sources via a simple JSON config.

## Resources

### references/
- [generativity_concepts.md](references/generativity_concepts.md): Core definitions of Leverage, Adaptability, Flywheels, and Market Architecture.
