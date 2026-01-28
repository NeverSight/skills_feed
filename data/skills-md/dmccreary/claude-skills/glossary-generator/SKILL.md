---
name: glossary-generator
description: This skill automatically generates a comprehensive glossary of terms from a learning graph's concept list, ensuring each definition follows ISO 11179 metadata registry standards (precise, concise, distinct, non-circular, and free of business rules). Use this skill when creating a glossary for an intelligent textbook after the learning graph concept list has been finalized.
license: MIT
---

# Glossary Generator

Generate a comprehensive glossary of terms from a learning graph's concept list with ISO 11179-compliant definitions.

## Purpose

This skill automates glossary creation for intelligent textbooks by converting concept labels from a learning graph into properly formatted glossary definitions. Each definition follows ISO 11179 metadata registry standards: precise, concise, distinct, non-circular, and free of business rules. The skill ensures consistency across terminology, validates cross-references, and produces alphabetically ordered entries with relevant examples.

Following a short definition you may provide a discussion of why the term is important in the textbook and an example of how the term is used.

## When to Use This Skill

Use this skill after the Learning Graph skill has completed and the concept list has been finalized.  All markdown content in the /docs area can also be scanned looking for words or phases that might not be clear to the average high-school student.

The glossary relies on having a complete, reviewed list of concepts from the learning graph's concept enumeration phase. Specifically, trigger this skill when:

- A concept list file exists (typically `docs/learning-graph/02-concept-list-v1.md`)
- The concept list has been reviewed and approved
- The course description exists with clear learning outcomes
- Ready to create or update the textbook's glossary

## Workflow

### Step 1: Validate Input Quality

Before generating definitions, assess the quality of the concept list:

1. Read the concept list file (typically `docs/learning-graph/02-concept-list-v1.md`)
2. Check for duplicate concept labels (target: 100% unique)
3. Verify Title Case formatting (target: 95%+ compliance)
4. Validate length constraints (target: 98% under 32 characters)
5. Assess concept clarity (no ambiguous terms)

Calculate a quality score (1-100 scale):

- 90-100: All concepts unique, properly formatted, appropriate length
- 70-89: Most concepts meet standards, minor formatting issues
- 50-69: Some duplicate concepts or formatting inconsistencies
- Below 50: Significant issues requiring manual review

**User Dialog Triggers:**

- If score < 70: Ask "The concept list has quality issues. Would you like to review and clean it before generating the glossary?"
- If duplicates found: Ask "Found [N] duplicate concepts. Should I remove duplicates automatically or would you like to review?"
- If formatting issues: Ask "Found [N] concepts with formatting issues. Auto-fix?"

### Step 2: Read Course Context

Read the course description file (`docs/course-description.md`) and any other markdonw files in `/docs/**/*.md` to understand:

- Target audience (for appropriate example complexity)
- Course objectives (for terminology alignment)
- Prerequisites (for background knowledge assumptions)
- Learning outcomes (for context on concept usage)

### Step 3: Generate Definitions

For each concept in the list, create a definition that follows ISO 11179 standards:

**Precision (25 points):** Accurately capture the concept's meaning

- Define the concept specifically in the context of the course
- Use terminology appropriate for the target audience
- Ensure the definition matches how the concept is used in the course

**Conciseness (25 points):** Keep definitions brief (target: 20-50 words)

- Avoid unnecessary words or explanations
- Get to the core meaning quickly
- Use clear, direct language

**Distinctiveness (25 points):** Make each definition unique and distinguishable

- Avoid copying definitions from other sources
- Ensure no two definitions are too similar
- Highlight what makes this concept different from related concepts

**Non-circularity (25 points):** Avoid circular dependencies

- Do not reference undefined terms in definitions
- Do not create circular chains (A depends on B, B depends on A)
- Use simpler, more fundamental terms in definitions

**Example Format:**

For a concept "Learning Graph":

```markdown
#### Learning Graph

A directed graph of concepts that reflects the order that concepts should be learned to master a new concept.

Learning graphs are the foundational data structure use for intelligent textbooks.  They are used to guide
intelligent agents and recommend learning paths for students.

**Example:** In a programming course, the learning graph shows that "Variables" must be understood before "Functions," which must be understood before "Recursion."
```

### Step 4: Add Examples (60-80% of terms)

For most concepts (target: 60-80%), include a relevant example:

- Start with "**Example:**" (no newline after colon)
- Provide a concrete illustration from the course domain
- Keep examples brief (1-2 sentences)
- Ensure examples clarify the concept without adding confusion

### Step 5: Add Cross-References

Where appropriate, reference related terms:

- Use "See also:" for related concepts
- Use "Contrast with:" for opposing concepts
- Ensure all cross-referenced terms exist in the glossary
- Keep cross-references to 1-3 per term

### Step 6: Create Glossary File

Generate `docs/glossary.md` with the following structure:

```markdown
# Glossary of Terms

#### [Term 1]

[Definition]

**Example:** [Example if applicable]

#### [Term 2]

[Definition]

**Example:** [Example if applicable]

[Continue alphabetically...]
```

Note: Do not put any `---` strings in the glossary.  They are not needed.

**Important formatting rules:**

- Sort all terms alphabetically (case-insensitive)
- Use level-4 headers (####) for term names
- Place definition in body text (no special formatting)
- Use "**Example:**" for examples (bold, with colon)
- Maintain consistent spacing between entries

### Step 7: Generate Quality Report

Create `docs/learning-graph/glossary-quality-report.md` with:

**ISO 11179 Compliance Metrics:**

For each definition, score on 4 criteria (25 points each):

1. Precision: Does it accurately capture the meaning?
2. Conciseness: Is it brief (20-50 words)?
3. Distinctiveness: Is it unique and distinguishable?
4. Non-circularity: No circular dependencies?

**Overall Quality Metrics:**

- Average definition length: [X] words
- Definitions meeting all 4 criteria: [X]%
- Circular definitions found: [X]
- Example coverage: [X]%
- Cross-references: [X] total, [X] broken

**Readability:**

- Flesch-Kincaid grade level: [X]
- Appropriate for target audience: Yes/No

**Recommendations:**

- List any definitions scoring < 70/100
- Identify circular dependencies to fix
- Suggest concepts needing examples
- Note any broken cross-references

### Step 8: Validate Output

Perform final validation:

1. Verify alphabetical ordering (100% compliance required)
2. Check all cross-references point to existing terms
3. Ensure all concepts from input list are included
4. Validate markdown syntax renders correctly
5. Confirm no circular definitions exist

**Success Criteria:**

- Overall quality score > 85/100
- Zero circular definitions
- 100% alphabetical ordering
- All terms from concept list included
- Markdown renders correctly in mkdocs

### Step 9: Update Navigation (Optional)

If `mkdocs.yml` does not already include the glossary:

1. Read `mkdocs.yml`
2. Check if "Glossary: glossary.md" exists in nav section
3. If missing, add it in an appropriate location
4. Preserve existing navigation structure

### Step 10: Generate Cross-Reference Index (Optional)

Create `docs/learning-graph/glossary-cross-ref.json` for semantic search:

```json
{
  "terms": [
    {
      "term": "Learning Graph",
      "related_terms": ["Concept Dependency", "Directed Acyclic Graph"],
      "contrasts_with": ["Linear Curriculum"],
      "category": "Educational Technology"
    }
  ]
}
```

This JSON file enables future features like:

- Semantic search across glossary
- Concept relationship visualization
- Automated suggestion of related terms

## Quality Scoring Reference

Use this rubric to score each definition (1-100 scale):

**85-100: Excellent**

- Meets all 4 ISO 11179 criteria (20+ pts each)
- Appropriate length (20-50 words)
- Includes relevant example
- Clear, unambiguous language
- No circular dependencies

**70-84: Good**

- Meets 3-4 ISO criteria
- Acceptable length (15-60 words)
- May lack example
- Generally clear
- No serious issues

**55-69: Adequate**

- Meets 2-3 ISO criteria
- Length issues (too short or too long)
- Missing example where helpful
- Some ambiguity
- Minor circular references

**Below 55: Needs Revision**

- Fails multiple ISO criteria
- Serious length issues
- Confusing or circular
- Missing context
- Requires complete rewrite

## Common Pitfalls to Avoid

**Circular Definitions:**

- Bad: "A Learning Graph is a graph that shows learning."
- Good: "A directed graph of concepts that reflects the order concepts should be learned."

**Too Vague:**

- Bad: "A thing used in education."
- Good: "A directed graph of concepts that reflects prerequisite relationships."

**Too Long:**

- Bad: "A learning graph is a specialized type of directed acyclic graph structure commonly used in educational technology and instructional design contexts to represent the hierarchical and sequential relationships between different conceptual elements that students need to master in order to achieve specific learning outcomes."
- Good: "A directed graph of concepts that reflects the order concepts should be learned to master a new concept."

**Business Rules:**

- Bad: "Students must complete prerequisites before advancing to dependent concepts."
- Good: "A directed graph showing prerequisite relationships between concepts."

**Undefined Terms:**

- Bad: "Uses a DAG structure" (if DAG not in glossary)
- Good: "Uses a directed acyclic graph structure"

## Output Files Summary

**Required:**

1. `docs/glossary.md` - Complete glossary in alphabetical order with ISO 11179-compliant definitions

**Recommended:**

2. `docs/learning-graph/glossary-quality-report.md` - Quality assessment and recommendations

**Optional:**

3. `docs/learning-graph/glossary-cross-ref.json` - JSON mapping for semantic search
4. Updates to `mkdocs.yml` navigation if glossary link missing

## Example Session

**User:** "Generate a glossary from my concept list"

**Claude (using this skill):**

1. Reads `docs/learning-graph/02-concept-list-v1.md`
2. Validates quality (checks for duplicates, formatting)
3. Reads `docs/course-description.md` for context
4. Generates ISO 11179-compliant definitions
5. Adds examples to 70% of terms
6. Sorts alphabetically
7. Creates `docs/glossary.md`
8. Generates quality report
9. Reports: "Created glossary with 187 terms. Overall quality score: 89/100. Added examples to 71% of terms. No circular definitions found."
