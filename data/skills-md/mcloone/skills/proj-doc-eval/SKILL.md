---
name: proj-doc-eval
description: Evaluate project documents (feature requests, initiatives, epics, etc.) against structured templates. Use when users need to assess document completeness, identify missing elements, or get improvement suggestions for project documentation. Supports markdown, PDF, and Word documents with built-in templates following the natural project flow (feature request → initiative → epic), plus custom template support.
metadata:
  author: McLoone
  version: "1.0.0"
---

# Project Document Evaluation

Evaluate project documents against structured templates to ensure completeness and quality.

## Document Workflow

This skill supports the natural project documentation flow:
1. **Feature Request** - Initial idea or user need
2. **Initiative** - Strategic response with solution proposal
3. **Epic(s)** - Planned implementation work (epics can depend on each other; planning happens outside epic descriptions)

## Operations

This skill supports the following operations:

### 1. Evaluate Document with Specified Template

User provides both a document and specifies which template to use.

**Examples:**
- "Evaluate docs/feature.md against the feature request template"
- "Check my epic using the epic template"
- "Use the initiative template to evaluate initiative.md"

### 2. Evaluate Document (Template Selection Prompt)

User provides a document but doesn't specify which template. The skill will ask which template to use.

**Examples:**
- "Evaluate docs/project-proposal.md"
- "Check this document for completeness"
- "Help me evaluate my project document"

### 3. Evaluate Document with Custom Template

User provides both a document and a custom template file.

**Examples:**
- "Evaluate docs/proposal.md using my-template.md as the template"
- "Compare this document against custom-template.md"

## Workflow

1. **Identify the document** - User specifies the document to evaluate (markdown, PDF, or Word file)
2. **Select template** - Choose from built-in templates or use a custom template (see Template Selection Guide below)
3. **Read the document** - Load and analyze the document content
4. **Evaluate against template** - Assess completeness, quality, and alignment with template criteria
5. **Generate report** - Provide evaluation results, missing elements, and specific improvement suggestions

## Template Selection Guide

### When Template is Specified

If the user explicitly specifies which template to use (e.g., "evaluate against the initiative template" or "use the epic template"), proceed directly with that template.

### When Template is NOT Specified

If the user provides a document to evaluate without specifying which template to use:

1. **Ask the user** which template to use via the AskUserQuestion tool
2. Present the three built-in template options with their descriptions:
   - **Feature Request** - For initial feature ideas and user needs
   - **Initiative** - For strategic initiatives with solution proposals
   - **Epic** - For planned implementation work
   - **Custom Template** - User provides their own template file path

3. After the user selects, proceed with the evaluation using the chosen template

**Example prompt when template is unclear:**

```
Which template should I use to evaluate this document?

Options:
- Feature Request: Best for initial feature ideas, user needs, and product enhancement proposals
- Initiative: Best for strategic initiatives with solution proposals and desired outcomes
- Epic: Best for planned implementation work with user stories and technical details
- Custom Template: You can provide the path to your own template file
```

## Template Selection

### Built-in Templates

Each template is independent but follows the natural project flow. Read the appropriate template from `references/`:

- `feature-request-template.md` - Initial feature ideas and user needs that start the process
- `initiative-template.md` - Strategic initiatives with solution proposals (often created from feature requests)
- `epic-template.md` - Planned implementation work (created from initiatives; epics can depend on each other)

### Custom Templates

If the user provides a custom template:
- Read the custom template file they specify
- Use the same evaluation workflow with their criteria

For guidance on creating custom templates, see `references/custom-template-guide.md`.

## Evaluation Process

For each template section:

1. **Check presence** - Is the section present in the document?
2. **Assess completeness** - Are all required elements included?
3. **Evaluate quality** - Does the content meet the quality criteria?
4. **Note gaps** - What specific elements are missing or weak?

## Output Format

Provide a structured evaluation report with:

### 1. Overall Assessment
Brief summary of document quality and readiness

### 2. Section-by-Section Evaluation
For each template section:
- **Status**: Complete ✓ | Partial ⚠ | Missing ✗
- **Findings**: What's present, what's missing, quality issues
- **Specific Improvements**: Concrete suggestions for enhancement

### 3. Priority Recommendations
Top 3-5 most critical improvements ranked by impact

### 4. Next Steps
Clear action items to address gaps

## Example Usage

```
User: "Help me evaluate docs/payment-system-initiative.md according to the initiative template"

Process:
1. Read references/initiative-template.md
2. Read docs/payment-system-initiative.md
3. Evaluate each section against criteria
4. Generate improvement suggestions
```

## Note on Document Flow

While templates are independent and can be used in any order, they naturally support this progression:
- **Feature Request** identifies a need or opportunity
- **Initiative** proposes a strategic solution (may reference the originating feature request)
- **Epic(s)** break down implementation (may reference the parent initiative; epics can depend on each other)
