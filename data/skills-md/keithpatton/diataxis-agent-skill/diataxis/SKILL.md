---
name: diataxis
description: Classify, validate, generate, and audit documentation using the Diátaxis framework. Enforces quadrant purity across tutorials, how-to guides, reference, and explanation. Use when creating documentation, reviewing docs, auditing doc sets, restructuring existing content, or when the user mentions Diátaxis, documentation structure, or doc quality.
license: CC-BY-SA-4.0
---

# Diátaxis Documentation Governance

This skill enforces the Diátaxis framework for documentation. Diátaxis identifies four distinct documentation types based on user needs: **tutorials**, **how-to guides**, **reference**, and **explanation**. Each serves a different purpose and must be written differently.

## Operating Modes

This skill operates in one of the following modes:

- **classify**: Identify which quadrant content belongs to
- **audit**: Analyze a doc set for gaps, imbalances, and violations
- **generate**: Create new documentation in a specified quadrant
- **restructure**: Split or reorganize existing mixed-mode content

The mode must be inferred from the user request or explicitly stated. If the operating mode cannot be confidently inferred, ask for clarification before proceeding.

Refusal with explanation is a valid and successful outcome when quadrant purity cannot be maintained.

### Generate Mode Policy

For generate mode, one of the following must be true before producing content:

- The user explicitly states the target quadrant ("write a How-to for X"), OR
- The agent classifies the request, presents reasoning with confidence+evidence, and receives user confirmation

## The Diátaxis Compass

Use this decision tree to classify content into exactly ONE quadrant:

| If content...     | ...and serves user's...   | ...then it belongs to... |
|-------------------|---------------------------|--------------------------|
| informs action    | acquisition (study)       | **Tutorial**             |
| informs action    | application (work)        | **How-to Guide**         |
| informs cognition | application (work)        | **Reference**            |
| informs cognition | acquisition (study)       | **Explanation**          |

**Two questions to ask:**

1. Does this inform **action** (doing) or **cognition** (knowing)?
2. Does this serve **acquisition** (learning/study) or **application** (working)?

## Quadrant Summary

### Tutorial (learning-oriented)

A lesson that takes the learner through a practical experience. The instructor is responsible for the learner's success. Focus on doing, not explaining. Deliver results early and often. Minimize explanation. No choices or alternatives.

- **Form**: Sequential lesson with concrete steps
- **Language**: "We will...", "First, do X", "You'll notice that..."
- **Not**: Teaching concepts, offering alternatives, explaining why

### How-to Guide (goal-oriented)

Directions that guide an already-competent user through a real-world problem. Assumes the reader knows what they want to achieve. Focused on work, not study.

- **Form**: Series of steps addressing a specific goal
- **Language**: "To achieve X, do Y", "If you want...", conditional imperatives
- **Not**: Teaching beginners, explaining concepts, describing machinery

### Reference (information-oriented)

Technical description of the machinery. Austere, neutral, accurate. Structure mirrors the thing being described. The user consults it, not reads it.

- **Form**: Structured descriptions, tables, specifications
- **Language**: "X is...", "The options are...", factual statements
- **Not**: Instructing, explaining why, narrative, opinions

### Explanation (understanding-oriented)

Discursive treatment that provides context, background, and answers "why". Makes connections, admits opinion, circles around the subject.

- **Form**: Prose discussion of a topic
- **Language**: "The reason for X is...", "This is because...", "Consider..."
- **Not**: Step-by-step procedures, technical specifications, teaching tasks

## Core Workflow

### For Classification

1. Read the content carefully
2. Apply the compass: action/cognition × acquisition/application
3. Identify the single quadrant
4. Report with confidence and evidence

### For Generation

1. Confirm the target quadrant (stated or inferred with confirmation)
2. Apply quadrant constraints strictly
3. Refuse to blend quadrants; recommend splitting if needed
4. Validate output against quadrant characteristics

### For Audit

1. Inventory all documentation
2. Classify each document
3. Identify gaps (missing quadrants)
4. Flag violations (mixed-mode, wrong quadrant)
5. Report imbalances (e.g., "reference-heavy, tutorial-poor")

### For Restructure

1. Classify the existing content
2. Identify quadrant violations
3. Propose splits (one document per quadrant)
4. Present plan for user confirmation before changes

## Output Requirements

When classifying or flagging violations, always provide:

- **Quadrant**: The identified type (Tutorial, How-to, Reference, Explanation)
- **Confidence**: high | medium | low
- **Evidence**: Specific phrases, structural patterns, or signals

Example:

> Classified as **How-to** (high confidence).
> Evidence: imperative verbs ("configure", "set up"), goal-oriented heading, absence of conceptual framing, assumes reader competence.

## Violation Detection

Flag these anti-patterns:

- **Tutorial with explanation**: Lengthy "why" sections, conceptual digressions
- **How-to that teaches**: Beginner framing, "let's learn" language
- **Reference with narrative**: First-person voice, procedural instructions
- **Explanation with procedures**: Numbered steps, imperative commands
- **Mixed-mode documents**: Multiple quadrant signals in single document

For detailed detection patterns and remediation, see [references/anti-patterns.md](references/anti-patterns.md).

## Non-Goals

This skill does not:

- Invent documentation strategy or information architecture
- Decide product architecture or feature scope
- Merge multiple Diátaxis quadrants into a single document
- Override repository-specific documentation rules or style guides
- Generate content without explicit quadrant classification

## Additional Resources

- **Detailed quadrant characteristics**: [references/quadrants.md](references/quadrants.md)
- **Classification decision tree**: [references/compass.md](references/compass.md)
- **Anti-patterns and fixes**: [references/anti-patterns.md](references/anti-patterns.md)

## Attribution

Diátaxis is the work of Daniele Procida. This skill encodes the Diátaxis framework for use by AI agents. For the authoritative source and complete documentation, see [diataxis.fr](https://diataxis.fr).

Licensed under CC-BY-SA 4.0. Citation metadata available at the [Diátaxis GitHub repository](https://github.com/evildmp/diataxis-documentation-framework).
