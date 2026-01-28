---
name: skill-creator
description: Use when the user has a document (PDF, markdown, book notes, research paper, methodology guide) containing theoretical knowledge or frameworks and wants to convert it into an actionable, reusable skill. Invoke when the user mentions "create a skill from this document", "turn this into a skill", "extract a skill from this file", or when analyzing documents with methodologies, frameworks, processes, or systematic approaches that could be made actionable for future use.
---

# Skill Creator

## Table of Contents

- [Read This First](#read-this-first)
- [Workflow](#workflow)
  - [Step 1: Inspectional Reading](#step-1-inspectional-reading)
  - [Step 2: Structural Analysis](#step-2-structural-analysis)
  - [Step 3: Component Extraction](#step-3-component-extraction)
  - [Step 4: Synthesis and Application](#step-4-synthesis-and-application)
  - [Step 5: Skill Construction](#step-5-skill-construction)
  - [Step 6: Validation and Refinement](#step-6-validation-and-refinement)

---

## Read This First

### What This Skill Does

This skill helps you transform documents containing theoretical knowledge into actionable, reusable skills. It applies systematic reading methodology from "How to Read a Book" by Mortimer Adler to extract, analyze, and structure knowledge from documents.

### The Process Overview

The skill follows a **six-step progressive reading approach**:

1. **Inspectional Reading** - Quick overview to understand structure and determine if the document contains skill-worthy material
2. **Structural Analysis** - Deep understanding of what the document is about and how it's organized
3. **Component Extraction** - Systematic extraction of actionable components from the content
4. **Synthesis and Application** - Critical evaluation and transformation of theory into practical application
5. **Skill Construction** - Building the actual skill files (SKILL.md, resources, rubric)
6. **Validation and Refinement** - Scoring the skill quality and making improvements

### Why This Approach Works

This methodology prevents common mistakes like:
- Reading entire documents without structure (information overload)
- Missing key concepts by not understanding the overall framework first
- Extracting theory without identifying practical applications
- Creating skills that can't be reused because they're too specific or too vague

### Collaborative Process

**This skill is always collaborative with you, the user.** At decision points, you'll be presented with options and trade-offs. The final decisions always belong to you. This ensures the skill created matches your needs and mental model.

---

## Workflow

**COPY THIS CHECKLIST** and work through each step:

```
Skill Creation Workflow
- [ ] Step 0: Initialize session workspace
- [ ] Step 1: Inspectional Reading
- [ ] Step 2: Structural Analysis
- [ ] Step 3: Component Extraction
- [ ] Step 4: Synthesis and Application
- [ ] Step 5: Skill Construction
- [ ] Step 6: Validation and Refinement
```

**Step 0: Initialize Session Workspace**

Create working directory and global context file. See [resources/inspectional-reading.md#session-initialization](resources/inspectional-reading.md#session-initialization) for setup commands.

**Step 1: Inspectional Reading**

Skim document systematically, classify type, assess skill-worthiness. Writes to `step-1-output.md`. See [resources/inspectional-reading.md#why-systematic-skimming](resources/inspectional-reading.md#why-systematic-skimming) for skim approach, [resources/inspectional-reading.md#why-document-type-matters](resources/inspectional-reading.md#why-document-type-matters) for classification, [resources/inspectional-reading.md#why-skill-worthiness-check](resources/inspectional-reading.md#why-skill-worthiness-check) for assessment criteria.

**Step 2: Structural Analysis**

Reads `global-context.md` + `step-1-output.md`. Classify content, state unity, enumerate parts, define problems. Writes to `step-2-output.md`. See [resources/structural-analysis.md#why-classify-content](resources/structural-analysis.md#why-classify-content), [resources/structural-analysis.md#why-state-unity](resources/structural-analysis.md#why-state-unity), [resources/structural-analysis.md#why-enumerate-parts](resources/structural-analysis.md#why-enumerate-parts), [resources/structural-analysis.md#why-define-problems](resources/structural-analysis.md#why-define-problems).

**Step 3: Component Extraction**

Reads `global-context.md` + `step-2-output.md`. Choose reading strategy, extract terms/propositions/arguments/solutions section-by-section. Writes to `step-3-output.md`. See [resources/component-extraction.md#why-reading-strategy](resources/component-extraction.md#why-reading-strategy) for strategy selection, [resources/component-extraction.md#section-based-extraction](resources/component-extraction.md#section-based-extraction) for programmatic approach, [resources/component-extraction.md#why-extract-terms](resources/component-extraction.md#why-extract-terms) through [resources/component-extraction.md#why-extract-solutions](resources/component-extraction.md#why-extract-solutions) for what to extract.

**Step 4: Synthesis and Application**

Reads `global-context.md` + `step-3-output.md`. Evaluate completeness, identify applications, transform to actionable steps, define triggers. Writes to `step-4-output.md`. See [resources/synthesis-application.md#why-evaluate-completeness](resources/synthesis-application.md#why-evaluate-completeness), [resources/synthesis-application.md#why-identify-applications](resources/synthesis-application.md#why-identify-applications), [resources/synthesis-application.md#why-transform-to-actions](resources/synthesis-application.md#why-transform-to-actions), [resources/synthesis-application.md#why-define-triggers](resources/synthesis-application.md#why-define-triggers).

**Step 5: Skill Construction**

Reads `global-context.md` + `step-4-output.md`. Determine complexity, plan resources, create SKILL.md and resource files, create rubric. Writes to `step-5-output.md`. See [resources/skill-construction.md#why-complexity-level](resources/skill-construction.md#why-complexity-level), [resources/skill-construction.md#why-plan-resources](resources/skill-construction.md#why-plan-resources), [resources/skill-construction.md#why-skill-md-structure](resources/skill-construction.md#why-skill-md-structure), [resources/skill-construction.md#why-resource-structure](resources/skill-construction.md#why-resource-structure), [resources/skill-construction.md#why-evaluation-rubric](resources/skill-construction.md#why-evaluation-rubric).

**Step 6: Validation and Refinement**

Reads `global-context.md` + `step-5-output.md` + actual skill files. Score using rubric, present analysis, refine based on user decision. Writes to `step-6-output.md`. See [resources/evaluation-rubric.json](resources/evaluation-rubric.json) for criteria.

---

## Notes

- **File-Based Context:** Each step writes output files to avoid context overflow
- **Global Context:** All steps read `global-context.md` for continuity
- **Sequential Dependencies:** Each step reads previous step's output
- **User Collaboration:** Always present findings and get approval at decision points
- **Quality Standards:** Use evaluation rubric (threshold ≥ 3.5) before delivery
