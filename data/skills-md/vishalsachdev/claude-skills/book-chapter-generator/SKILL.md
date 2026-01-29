---
name: book-chapter-generator
description: This skill generates a structured chapter outline for intelligent textbooks by analyzing course descriptions, learning graphs, and concept dependencies. Use this skill after the learning graph has been created and before generating chapter content, to design an optimal chapter structure that respects concept dependencies and distributes content evenly across 6-20 chapters.
---

# Book Chapter Generator

## Overview

This skill creates a comprehensive chapter structure for intelligent textbooks by analyzing the course description, learning graph, and concept taxonomy. It designs an optimal chapter outline that ensures all concepts are covered exactly once, respects dependency relationships, and distributes content appropriately across chapters.

## When to Use This Skill

Use this skill when:
- A learning graph has been generated (learning-graph.json exists)
- The course description is finalized
- The concept taxonomy has been established
- Chapter content structure needs to be designed before writing begins

**Prerequisites:**
- `/docs/course-description.md` must exist
- `/docs/learning-graph/learning-graph.json` must exist with ~200 concepts
- `/docs/learning-graph/concept-taxonomy.md` should exist
- MkDocs project structure must be in place

**Do NOT use this skill if:**
- The learning graph hasn't been generated yet (use `learning-graph-generator` first)
- Chapter content already exists and just needs updating

## Chapter Generation Workflow

This skill follows a four-step sequential workflow with user approval before generating files.

### Step 1: Analyze Input Resources

Before designing chapters, analyze the following resources:

#### 1.1 Read Course Description

Read `/docs/course-description.md` to understand:
- Course title and target audience
- Learning objectives and outcomes
- Prerequisite knowledge
- Overall scope and goals

#### 1.2 Read Learning Graph

Read `/docs/learning-graph/learning-graph.json` to extract:
- Complete list of concepts (typically 200 concepts)
- Concept dependencies (which concepts require others as prerequisites)
- Concept groupings by taxonomy category
- Metadata about the course

Validate that:
- The graph structure is a valid DAG (no circular dependencies)
- All concepts have unique IDs
- Dependency references are valid

#### 1.3 Read Concept Taxonomy

Read `/docs/learning-graph/concept-taxonomy.md` (if it exists) to understand:
- Taxonomy categories and their meanings
- How concepts are grouped conceptually
- Any suggested ordering or progression

#### 1.4 Identify Design Constraints

Analyze the data to identify:
- **Foundational concepts**: Concepts with no dependencies (should appear early)
- **Advanced concepts**: Concepts with many dependencies (should appear later)
- **Dependency chains**: Long sequences of prerequisite relationships
- **Concept clusters**: Groups of related concepts that should stay together
- **Orphaned concepts**: Concepts that nothing depends on (can be placed flexibly)

### Step 2: Design Chapter Structure

Design an optimal chapter structure following these principles:

#### 2.1 Determine Chapter Count

Choose the appropriate number of chapters (6-20) based on:
- **Total concepts**: ~200 concepts typically need 10-15 chapters
- **Dependency complexity**: More complex dependencies may need more chapters
- **Taxonomy distribution**: Natural groupings suggest chapter boundaries
- **Target audience**: Introductory courses may need smaller chapters

**Guidelines:**
- Minimum 6 chapters (for very concise courses)
- Optimal range: 10-15 chapters
- Maximum 20 chapters (for comprehensive graduate-level content)
- Aim for 10-20 concepts per chapter on average

#### 2.2 Assign Concepts to Chapters

Design chapter assignments that satisfy these requirements:

**CRITICAL REQUIREMENTS:**
1. **Every concept appears in exactly one chapter** (no duplicates, no omissions)
2. **No concept appears before its dependencies** (respect the DAG structure)
3. **Balanced distribution** (avoid chapters with too many or too few concepts)

**OPTIMIZATION GOALS:**
- Keep related concepts (same taxonomy category) together when possible
- Create logical progression from foundational to advanced topics
- Balance chapter sizes (avoid chapters with <8 or >25 concepts)
- Group concepts that form natural learning units
- Consider cognitive load (mix difficulty levels within chapters)

#### 2.3 Create Chapter Titles

For each chapter, create a title that:
- Uses **Title Case** formatting
- Is **no longer than 200 characters** (to fit on one line)
- Clearly describes the chapter's main topic
- Uses standard educational terminology
- Avoids acronyms unless widely known

**Examples:**
- "Introduction to Graph Theory Fundamentals"
- "Binary Trees and Tree Traversal Algorithms"
- "Graph Coloring Problems and Applications"
- "Advanced Topics in Network Flow Optimization"

#### 2.4 Write Chapter Summaries

For each chapter, write a **single sentence** (20-40 words) that:
- Describes what the chapter covers
- Mentions key concepts or themes
- Indicates the chapter's role in the learning progression

### Step 3: Present Design to User for Approval

Before creating any files, present the chapter design to the user in this format:

```
## Proposed Chapter Structure

I've designed a [number]-chapter structure for your textbook covering [total] concepts.

### Chapters:

1. **[Chapter Title]** ([X] concepts)
   [One sentence summary]

2. **[Chapter Title]** ([X] concepts)
   [One sentence summary]

[... continue for all chapters ...]

### Design Challenges & Solutions:

[Discuss any challenges encountered and how the design addresses them, such as:]
- **Challenge**: Concept X has 15 dependencies, making placement difficult
  **Solution**: Placed in Chapter 8 after all prerequisites are covered in Chapters 1-7

- **Challenge**: Taxonomy category Y contains 45 concepts
  **Solution**: Split across Chapters 3, 6, and 9 to maintain logical flow

[... other challenges ...]

### Statistics:

- Total chapters: [X]
- Average concepts per chapter: [X.X]
- Range: [min]-[max] concepts per chapter
- All [total] concepts covered: ✓
- All dependencies respected: ✓
```

#### 3.1 Get User Approval

After presenting the design, ask:

```
Do you approve this chapter structure? (y/n)

If no, please specify what changes you'd like:
- Different number of chapters?
- Specific concepts moved to different chapters?
- Chapter titles revised?
- Different grouping strategy?
```

#### 3.2 Handle User Feedback

If the user says "no" or requests changes:
- Listen to their specific feedback
- Revise the chapter design accordingly
- Re-present the updated structure
- Continue iterating until approval is received

If the user says "yes":
- Proceed to Step 4 to generate the chapter files

### Step 4: Generate Chapter Directory Structure and Files

Once the user approves the design, create the chapter structure:

#### 4.1 Create URL Path Names

For each chapter, create a URL-friendly path name:

**Rules:**
- Use only **lowercase letters** and **dashes** (no other characters)
- Remove all special characters, punctuation, and numbers (except in numbered prefixes)
- Replace spaces with dashes
- Use abbreviations if needed to keep names short (<50 characters)
- Make names descriptive but concise

**Examples:**
```
"Introduction to Graph Theory Fundamentals" → "intro-to-graph-theory"
"Binary Trees and Tree Traversal Algorithms" → "binary-trees-traversal"
"Advanced Topics in Network Flow Optimization" → "advanced-network-flow"
```

#### 4.2 Create Directory Structure

Create the following directory structure:

```
/docs/chapters/
├── index.md
├── 01-[url-path-name]/
│   └── index.md
├── 02-[url-path-name]/
│   └── index.md
├── 03-[url-path-name]/
│   └── index.md
[... continue for all chapters ...]
```

**Implementation:**
```bash
mkdir -p /docs/chapters
mkdir -p /docs/chapters/01-[url-path-name]
mkdir -p /docs/chapters/02-[url-path-name]
# ... continue for all chapters
```

#### 4.3 Create Main Chapters Index

Create `/docs/chapters/index.md` with:

```markdown
# Chapters

This textbook is organized into [X] chapters covering [Y] concepts.

## Chapter Overview

1. [Chapter 1 Title](01-[url-path-name]/index.md) - [One sentence summary]
2. [Chapter 2 Title](02-[url-path-name]/index.md) - [One sentence summary]
[... continue for all chapters ...]

## How to Use This Textbook

[Add 2-3 sentences about how readers should progress through the chapters, noting that dependencies are respected and concepts build on each other]

---

**Note:** Each chapter includes a list of concepts covered. Make sure to complete prerequisites before moving to advanced chapters.
```

#### 4.4 Create Individual Chapter Index Files

For each chapter, create `/docs/chapters/[XX]-[url-path-name]/index.md` with this structure:

```markdown
# [Chapter Title]

## Summary

[Write a 2-4 sentence summary of what the chapter covers, expanding on the one-sentence version from the design. Include:]
- Main topics and themes
- How this chapter fits in the learning progression
- What students will be able to do after completing this chapter

## Concepts Covered

This chapter covers the following [X] concepts from the learning graph:

1. [Concept Name 1]
2. [Concept Name 2]
3. [Concept Name 3]
[... continue for all concepts in this chapter ...]

## Prerequisites

[If this is not the first chapter, list which previous chapters should be completed first:]

This chapter builds on concepts from:
- [Chapter X: Chapter Title](../[XX]-[url-path-name]/index.md)
- [Chapter Y: Chapter Title](../[YY]-[url-path-name]/index.md)

[If this is the first chapter or has no prerequisites within the book:]

This chapter assumes only the prerequisites listed in the [course description](../../course-description.md).

---

TODO: Generate Chapter Content
```

**Important formatting notes:**
- Always include a blank line before markdown lists (MkDocs requirement)
- Use relative paths for internal links
- Concept names should match exactly as they appear in learning-graph.json
- Maintain consistent heading hierarchy (# → ## → ###)

#### 4.5 Update MkDocs Navigation

After creating all chapter files, update `mkdocs.yml` to include the chapters in navigation:

```yaml
nav:
  - Home: index.md
  - Course Description: course-description.md
  - Chapters:
    - Overview: chapters/index.md
    - Chapter 1: chapters/01-[url-path-name]/index.md
    - Chapter 2: chapters/02-[url-path-name]/index.md
    # ... continue for all chapters
  - Learning Graph:
    - Introduction: learning-graph/index.md
    # ... existing learning graph pages
```

**Note:** Only update the `Chapters:` section. Do not remove or modify other navigation entries.

#### 4.6 Confirm Completion

After all files are created, inform the user:

```
✅ Chapter structure generated successfully!

Created:
- chapters/index.md (main chapter overview)
- [X] chapter directories with index files
- Updated mkdocs.yml navigation

Next steps:
1. Review the chapter structure: `mkdocs serve`
2. Navigate to the Chapters section to see all chapter outlines
3. Use the chapter content generation skill (when ready) to populate each chapter
4. Each chapter index.md has "TODO: Generate Chapter Content" as a placeholder

Statistics:
- Total chapters: [X]
- Total concepts assigned: [Y]
- All dependencies respected: ✓
```

## Design Principles

### Dependency Management

**Critical**: The chapter sequence must respect the DAG structure:
- If concept B depends on concept A, then A must appear in an earlier (or same) chapter than B
- Check all dependency relationships before finalizing chapter assignments
- Use topological sorting to verify the order is valid

### Content Balance

Aim for balanced chapter sizes:
- **Optimal**: 12-18 concepts per chapter
- **Acceptable**: 8-25 concepts per chapter
- **Avoid**: <8 concepts (too thin) or >25 concepts (too dense)

If a chapter is too large, consider splitting it into two chapters.
If a chapter is too small, consider merging it with a related chapter.

### Pedagogical Flow

Structure chapters to support learning:
- **Early chapters**: Foundational concepts, simple ideas, build confidence
- **Middle chapters**: Core content, increasing complexity, practical applications
- **Late chapters**: Advanced topics, integration, synthesis

Within each chapter, order concepts from:
1. Foundational to advanced (based on dependencies)
2. Simple to complex (based on cognitive load)
3. Abstract to concrete (when introducing new ideas)

### Cognitive Load

Consider student cognitive load:
- Don't overload early chapters (students are still building context)
- Mix difficulty levels within chapters when possible
- Group related concepts to reduce cognitive switching
- Ensure adequate scaffolding (prerequisite concepts in prior chapters)

## Common Challenges and Solutions

### Challenge: Taxonomy Category Too Large

**Problem**: A single taxonomy category contains 40+ concepts.

**Solutions**:
- Split the category across multiple chapters
- Use different aspects or sub-themes as chapter boundaries
- Interleave with other categories to maintain engagement

### Challenge: Long Dependency Chains

**Problem**: Concept Z depends on Y, which depends on X, which depends on W... (5+ levels deep).

**Solutions**:
- Spread the chain across multiple chapters
- Place earlier dependencies in multiple chapters if appropriate
- Consider creating a dedicated "foundations" chapter for deep dependency roots

### Challenge: Orphaned Concepts

**Problem**: Some concepts have no dependents (nothing builds on them).

**Solutions**:
- Place orphaned concepts at the end of related chapters
- Group orphaned concepts into "Additional Topics" or "Special Topics" chapters
- Consider whether these concepts are truly necessary (but don't remove them without user approval)

### Challenge: Cluster Splitting

**Problem**: A natural concept cluster (e.g., 5 tree traversal algorithms) is too large for one chapter but splitting it feels wrong.

**Solutions**:
- Split into "Part 1" and "Part 2" chapters with clear continuation
- Use dependency relationships to find a natural split point
- Group by complexity (basic vs. advanced) or application domain

### Challenge: Uneven Distribution

**Problem**: The dependency structure forces 30 concepts into Chapter 2 and only 8 concepts into Chapter 7.

**Solutions**:
- Split the large chapter into two chapters
- Merge the small chapter with an adjacent chapter
- Revisit chapter boundaries to find better balance
- Adjust the total number of chapters

## Validation Checklist

Before finalizing the chapter structure, verify:

- [ ] All concepts from learning-graph.json are assigned to exactly one chapter
- [ ] No concept appears before any of its dependencies
- [ ] Chapter sizes are within acceptable range (8-25 concepts)
- [ ] Chapter titles are Title Case and ≤200 characters
- [ ] URL path names contain only lowercase letters and dashes
- [ ] All files follow the specified directory structure
- [ ] MkDocs navigation is correctly updated
- [ ] All markdown files have proper formatting (blank lines before lists, etc.)
- [ ] Each chapter index.md includes all required sections
- [ ] User has approved the chapter design

## Example Usage

**User request:**
"Create chapters for my Graph Theory textbook"

**Skill workflow:**
1. Read course-description.md, learning-graph.json, and concept-taxonomy.md
2. Analyze 200 concepts and their dependencies
3. Design 12 chapters with balanced content distribution
4. Present chapter outline to user:
   - Chapter 1: Introduction (15 concepts)
   - Chapter 2: Graph Representations (18 concepts)
   - ... etc.
5. Get user approval (y/n)
6. Create directory structure and all index.md files
7. Update mkdocs.yml navigation
8. Confirm completion

## Notes

- This skill only creates the **structure and outlines** for chapters
- It does NOT generate actual chapter content (that requires a separate skill)
- The "TODO: Generate Chapter Content" marker indicates where content should be added later
- Always preserve the concept list in each chapter index.md for use by content generation skills
