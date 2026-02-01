---
name: project-feature-explainer
description: Expert guidance for explaining project features. Use this skill when you need to provide a comprehensive explanation of how a specific feature works, including summaries, deep dives, usage examples, and sequence/workflow diagrams. This skill has references directory which contains additional instructions `checklist.md`, `example-output.md` and `explanation-template.md` that MUST be used for every analysis.
---

# Project Feature Explainer Skill

This skill provides a systematic approach to analyzing and explaining a specific feature within a codebase.

## Workflow

1.  **Identify Entry Points:** Locate the main functions, classes, or API endpoints that trigger the feature.
2.  **Trace Dependencies:** Identify the internal modules, services, or external APIs the feature relies on.
3.  **Analyze Data Flow:** Understand how data enters the feature, how it's transformed, and where it's stored or returned.
4.  **Draft Explanation:** Structure the explanation using the mandatory sections below.
5.  **Verify:** Cross-reference the draft with the `references/checklist.md` to ensure completeness.

## Mandatory Output Structure

### 1. Feature Summary
A high-level overview (1-2 paragraphs) explaining *what* the feature does and *why* it exists.

### 2. Deep Dive (Technical Details)
A detailed breakdown of the internal implementation.
- **Key Components:** List the main files/classes/functions involved.
- **Logic Flow:** Step-by-step description of the execution path.
- **State Changes:** Describe any side effects (e.g., database updates, cache invalidation).

### 3. Usage & Examples
Code snippets or CLI commands showing how to use the feature.
- Include common parameters and expected outputs.
- Provide a "Happy Path" example.

## Guidelines
- **Be Concise:** Focus on the "how" and "why" without repeating obvious code logic.
- **Reference Code:** Use specific file paths and symbol names.
- **Contextualize:** Explain how this feature fits into the broader system architecture.
