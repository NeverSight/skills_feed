---
name: chapter-content-generator
description: This skill generates comprehensive chapter content for intelligent textbooks after the book-chapter-generator skill has created the chapter structure. Use this skill when a chapter index.md file exists with title, summary, and concept list, and detailed educational content needs to be generated at the appropriate reading level with rich non-text elements including diagrams, infographics, and MicroSims. (project, gitignored)
---

# Chapter Content Generator

**Version:** 0.03

## Overview

This skill generates detailed educational content for individual textbook chapters, transforming chapter outlines (title, summary, concept list) into comprehensive learning material with appropriate reading level, rich visual elements, and interactive components. The skill is designed to run after the `book-chapter-generator` skill has created the chapter structure.

## When to Use This Skill

Use this skill when:
- The `book-chapter-generator` skill has created chapter directories with index.md files
- A chapter index.md contains: title, summary, and concepts covered list
- Detailed chapter content needs to be generated
- Content should be adapted to a specific reading level (junior high, senior high, college, graduate)
- Rich non-text elements (diagrams, MicroSims, infographics) are desired

Do NOT use this skill when:
- Chapter structure hasn't been created yet (use `book-chapter-generator` first)
- Content already exists and just needs editing (use Edit tool directly)
- Generating other types of content (prompts, glossaries, etc.)

## Workflow

### Step 1: Verify Chapter File Exists

Verify that the input chapter name or path to the chapter file is present.

**Expected input format:**
- Chapter name: "01-intro-to-itil-and-config-mgmt" or "Chapter 1"
- Full path: "/docs/chapters/01-intro-to-itil-and-config-mgmt/index.md"
- Relative path: "chapters/01-intro-to-itil-and-config-mgmt/index.md"

**Chapter directory structure:**
```
/docs/chapters/NN-lowercase-name/index.md
```

Where:
- `NN` = Two-digit chapter number with leading zero (e.g., "01", "07", "12")
- `lowercase-name` = URL-friendly lowercase name with dashes, no spaces

**Actions:**
1. If chapter name is provided, search for matching directory in `/docs/chapters/`
2. If path is provided, verify file exists at that location
3. If file not found, ask user to specify correct chapter name or path
4. Read the chapter index.md file

### Step 2: Verify Chapter Content is Correct

Open the chapter file and check for required elements.

**Required elements:**

1. **Title** in header 1 (# Title)
2. **Summary** in level 2 header (## Summary)
3. **Concepts Covered** in level 2 header (## Concepts Covered) with numbered list

**Actions:**
1. Parse the chapter index.md file
2. Extract:
   - Chapter title
   - Summary text
   - List of concepts covered (numbered list)
3. If any element is missing, ask user to provide the content as text
4. Store concepts list for verification in Step 5

### Step 3: Get the Reading Level

Extract the grade reading level from the `/docs/course-description.md` file.

**Reading level indicators in course description:**

- "junior-high", "junior high", "grades 7-9", "middle school" → Junior High
- "senior-high", "senior high", "grades 10-12", "high school" → Senior High
- "college", "undergraduate", "bachelor" → College
- "graduate", "master", "masters", "master's", "PhD", "doctoral" → Graduate

**Actions:**
1. Read `/docs/course-description.md`
2. Search for reading level indicators in:
   - Course title
   - Target audience section
   - Prerequisites section
   - Course overview
3. If not found, ask user: "What grade-level should be used to generate the content?"
4. Default to Grade 10 (Senior High) if not specified

**Reading level characteristics:**
- **Junior High (Grades 7-9):** Simple sentences (12-18 words), common vocabulary, concrete examples, frequent visual aids
- **Senior High (Grades 10-12):** Mixed sentence complexity (15-22 words), technical vocabulary with definitions, balance of concrete and abstract
- **College:** Academic style (18-25 words), technical terminology, case studies, research context
- **Graduate:** Sophisticated prose (20-30+ words), full jargon, theoretical depth, research literature

See `references/reading-levels.md` for detailed guidelines on adapting content for each level.

### Step 4: Generate Detailed Chapter Content

Add metadata to the top of the index file that indicates that a DRAFT of this
chapter was created by this skill, the name of the skill, the date it was generated and the version of this skill.

```markdown
---
title: Chapter Title
description: Short description of title
generated_by: claude skill generate-chapter-content
date: YYYY-MM-DD HH-MM-SS
version: 0.03
---
```

### Step 5: Generate Detailed Chapter Content

Generate comprehensive educational content based on the chapter outline, concept list, and reading level.

**Content generation principles:**

1. **Reading level adaptation:**
   - Apply appropriate sentence complexity, vocabulary, and explanation style
   - See `references/reading-levels.md` for specific guidelines

2. **Concept ordering:**
   - Present simple concepts first, complex concepts last
   - Follow natural pedagogical progression
   - Do NOT necessarily follow the order in "Concepts Covered" list
   - Build on previously explained concepts

3. **Non-text elements:**
   - Goal: No more than 3 paragraphs of pure text without a non-text element.
   - Use diverse element types (don't repeat the same type).
   - Place special focus on interactive elements (infographics, MicroSims).
   - We appropriate, render equations in LaTeX surrounded by single dollar signs.
   - See the math-equations.md file in the references for proper formatting of equations.

**Non-text element types:**

Elements embedded directly in markdown (no `<details markdown="1">` block):

1. **Markdown lists** (bullet or numbered) - ALWAYS put blank line before list
2. **Markdown tables** - ALWAYS put blank line before table

Elements requiring diagram header and `<details markdown="1">` specification blocks:

3. **Diagrams/drawings** - System architectures, relationships, data flows
4. **Interactive infographics** - Clickable concept maps, progressive disclosure, hovers with definitions appearing in tooltips consistent with the glossary
5. **MicroSims** - p5.js simulations with interactive controls
6. **Charts** - Bar, line, pie charts with quantitative data
7. **Timelines** - Historical progression, sequential events
8. **Maps** - Geographic distribution with movement arrows
9. **Workflow diagrams** - Business processes with hover text
10. **Graph data models** - Entity relationships using vis-network
11. **Causal Loop Diagrams** - used in systems thinking and explaining causality

For each `<details markdown="1">` block element, use this structure:

```markdown
#### Diagram: [Brief descriptive title]

<details markdown="1">
<summary>[Brief descriptive title]</summary>
Type: [element-type]

[Detailed specification following guidelines in references/content-element-types.md]

Implementation: [Technology/approach]
</details>
```

Do not indent any text within a `<details markdown="1">` block.  Do not put
any leading spaces or tabs on newlines within a `<details markdown="1">` block.

Make SURE to put the level 4 header with the prefix `#### Diagram:` before the details.  This is REQUIRED!

**Specification requirements:**
- Detailed enough that another skill or developer can implement without additional context
- Include all visual elements, data, labels, colors, interactions
- Specify canvas sizes, layout, default parameters
- Specify that the visual elements must have a responsive design that must respond to window resize events
- For MicroSims: describe learning objective, controls, visual elements, behavior
- See `references/content-element-types.md` for complete specification guidelines for each element type

**Content structure:**

1. Start with introductory paragraphs connecting to chapter summary
2. Present concepts in pedagogical order (simple to complex)
3. Integrate non-text elements naturally throughout
4. Use markdown lists and tables frequently (with blank lines before them)
5. Include `<details markdown="1">` blocks for complex visual/interactive elements
6. Place a level 4 markdown header before each `details` block
   ```#### Diagram: [Diagram Name]```
6. End with summary or key takeaways section

**Interactive elements emphasis:**
- Prioritize MicroSims and infographics that enable:
  - Student interaction tracking
  - Progress gauging
  - Personalized content recommendations
- Each interactive element should have clear **Learning objectives:**
- Reference a section of the 2001 Bloom Taxonomy when you describe a learning objective:
   - **Remembering:** Recalling facts, terms, basic concepts, and answers without necessarily understanding their meaning.
   - **Understanding:** Explaining ideas or concepts, demonstrating comprehension by summarizing or rephrasing information.
   - **Applying:** Using acquired knowledge to solve problems in new or unfamiliar situations.
   - **Analyzing:** Breaking down information into parts to understand its structure and relationships, and drawing comparisons.
   - **Evaluating:** Making judgments about information based on set criteria or standards, requiring critical thinking and justification.
   - **Creating:** Producing new or original work by combining elements to form a novel whole or solution. 

### Step 6: Verify Completeness

After generating chapter content, verify all concepts have been covered.

**Verification process:**
1. Review the generated content
2. Check that each concept from "Concepts Covered" list appears in the content
3. Create a checklist showing which concepts were covered
4. If any concepts missing:
   - Add content covering those concepts
   - Integrate them naturally into existing structure
5. Update the chapter index.md file with the complete generated content
6. Make **Absolutely Sure** that the content has been written to the chapter index.md file.  Do a word count to make sure that **ALL* the content is present and that the TODO has been removed.

**Actions:**
- Replace the "TODO: Generate Chapter Content" placeholder with generated content
- Keep the existing title, summary, concepts list, and prerequisites sections
- Add the new detailed content after the prerequisites section

### Step 7: Report Summary to User

Provide a concise summary of the content generation results.

**Report should include:**
1. Confirmation that chapter content has been generated and the version of the skill
2. Reading level used
3. Word count or approximate length
4. Count of non-text elements by type:
   - Markdown lists: X
   - Markdown tables: X
   - Admonitions
   - Diagrams: X
   - Infographics: X
   - MicroSims: X
   - Charts: X
   - Timelines: X
   - Maps: X
   - Workflows: X
   - Graph models: X
5. Number of interactive elements requiring skill execution
6. Confirmation that all concepts were covered

!!! Note
   For admonitions to work, your mkdocs.yml must have admonition and pymdownx.details enabled.

**Example report:**

```
✅ Chapter content generated successfully!

Chapter: 01-intro-to-itil-and-config-mgmt
Reading level: Graduate
Content length: ~3,500 words

Non-text elements:
- 6 markdown lists
- 3 markdown tables
- 2 diagrams (CMDB architecture, ITIL process flow)
- 1 interactive timeline (ITIL evolution)
- 1 MicroSim (Configuration drift simulator)
- 1 workflow diagram (Change management process)

Interactive elements: 2 (timeline, MicroSim)
Skills required: 2 (microsim-p5 for MicroSim, infographic-generator for timeline)

All 20 concepts covered: ✓
```

## Resources

This skill includes reference files that provide detailed guidelines for content generation:

### references/content-element-types.md

Comprehensive specifications for all non-text element types (3-10 above). Includes:
- When to use each element type
- Required information for specifications
- Implementation approaches
- Example specifications in `<details markdown="1">` block format
- Place a level 4 Diagram header before each `details` element

```markdown
#### Diagram: [Diagram Name]
```

Load this reference when generating content to ensure proper specification of diagrams, MicroSims, infographics, charts, timelines, maps, workflows, and graph models.

### references/reading-levels.md

Detailed guidelines for adapting content to different reading levels. Includes:
- Sentence structure and length guidelines
- Vocabulary choices
- Explanation styles
- Example complexity
- Assumed background knowledge
- Example text at each level

Load this reference when determining how to write content at the appropriate reading level.

## Best Practices

1. **Always read references:** Load `references/content-element-types.md` and `references/reading-levels.md` before generating content

2. **Maintain blank lines:** Always place blank line before markdown lists and tables (MkDocs requirement)

3. **Pedagogical ordering:** Don't feel constrained by concept list order - teach concepts in the most effective sequence

4. **Visual variety:** Mix different types of non-text elements rather than using the same type repeatedly

5. **Interactive emphasis:** Prioritize MicroSims and infographics that enable student engagement tracking

6. **Detailed specifications:** Make `<details markdown="1">` blocks comprehensive enough for implementation without additional context

7. **Concept integration:** Weave concepts together naturally rather than treating them as isolated topics

8. **Appropriate depth:** Match explanation depth to reading level (more scaffolding for junior high, more theory for graduate)

9. **Verification:** Always check that all concepts from "Concepts Covered" list appear in generated content

10. **Consistent style:** Maintain consistent voice, terminology, and visual style throughout chapter
