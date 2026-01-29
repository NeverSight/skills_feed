---
name: skill-from-book
description: |
  Create Claude skills from book content (markdown files). Transforms long-form book knowledge into structured, context-efficient skill packages with granular reference files, workflows, and use-case guidelines.
  
  Use this skill when:
  - Converting a book (markdown) into a reusable Claude skill
  - Creating knowledge bases from technical books, guides, or documentation
  - Building skills that need progressive disclosure of large content
  - Structuring book knowledge for efficient context loading
---

# Skill From Book

Transform book content into structured, context-efficient Claude skills.

## Overview

This skill guides you through converting a book (in markdown format) into a well-organized skill with:
- Granular knowledge files (one concept per file)
- Workflows for repeatable tasks
- Use-case guidelines (mapping tasks to relevant files)
- Progress tracking for multi-session work
- Subagent extraction tasks

## CRITICAL INSTRUCTIONS

**YOU MUST FOLLOW THIS WORKFLOW STRICTLY. DO NOT SKIP OR REORDER PHASES.**

1. **DO NOT read the book markdown file content before starting Phase 1**
2. **MUST read each reference file BEFORE starting its corresponding phase**
3. **MUST complete each phase before moving to the next**
4. **MUST use subagents for extraction tasks**
5. **MUST propose workflows to user before finalization**

---

## Workflow

### Phase 1: Analysis

**STOP! Before proceeding, you MUST:**
1. Read `references/analysis-guide.md` completely
2. Only then proceed with the steps below

**Phase 1 Steps:**

1. **Extract TOC and outline ONLY** (DO NOT read full book content)
   ```bash
   # Count total lines
   wc -l book.md
   
   # Extract headers/TOC - THIS IS ALL YOU NEED
   grep -E "^#{1,3} " book.md
   ```

2. **Identify knowledge categories from outline**
   - Core principles/philosophy
   - Rules and guidelines
   - Examples (good vs bad)
   - Patterns and anti-patterns
   - Checklists and quick references

3. **Define use cases**
   - Who will use this skill?
   - What tasks will they perform?
   - What questions will they ask?

4. **Ask user to confirm** the identified categories and use cases before proceeding

---

### Phase 2: Planning

**STOP! Before proceeding, you MUST:**
1. Read `references/extraction-patterns.md` completely
2. Read `references/file-templates.md` completely
3. Only then proceed with the steps below

**Phase 2 Steps:**

1. **Design file structure with required files per category**

   Each category MUST contain these 3 basic files:
   - `knowledge.md` - Core concepts, definitions, and foundational understanding
   - `rules.md` - Specific guidelines, do's and don'ts
   - `examples.md` - Good/bad code examples, before/after comparisons

   Additional files as needed:
   - `patterns.md` - Reusable solutions
   - `smells.md` - Anti-patterns and what to avoid
   - `checklist.md` - Quick reference checklists

   ```
   skill-name/
   ├── SKILL.md
   ├── progress.md
   ├── guidelines.md
   ├── workflows/           # NEW: Step-by-step processes
   │   ├── [task-1].md
   │   └── [task-2].md
   └── references/
       ├── category-1/
       │   ├── knowledge.md    # REQUIRED
       │   ├── rules.md        # REQUIRED
       │   ├── examples.md     # REQUIRED
       │   ├── patterns.md     # Optional
       │   └── checklist.md    # Optional
       └── category-2/
           ├── knowledge.md    # REQUIRED
           ├── rules.md        # REQUIRED
           ├── examples.md     # REQUIRED
           └── smells.md       # Optional
   ```

2. **Create progress.md**
   - List ALL files to create (required + optional)
   - Group by phase/priority
   - Track completion status

3. **Plan extraction tasks**
   - One task per knowledge file
   - Define input (book section with line ranges) and output (file path)
   - Identify dependencies between tasks

4. **Ask user to confirm** the file structure and extraction plan before proceeding

---

### Phase 3: Extraction

**STOP! Before proceeding, you MUST:**
1. Have completed Phase 1 and Phase 2
2. Have user confirmation on the plan
3. Only then proceed with extraction

**CRITICAL: You MUST use subagents (Task tool) for extraction. One subagent per topic - each subagent creates ALL files for that topic.**

#### Main Agent Instructions for Phase 3

**YOU MUST follow these steps:**

1. **One subagent per topic** - Each subagent reads a book section ONCE and creates all files for that topic (knowledge.md, rules.md, examples.md, plus any optional files)
2. **Prepare the subagent prompt** by filling in the template below with specific values
3. **Calculate line ranges** from your Phase 1 analysis (TOC with line numbers)
4. **Create the complete prompt** - do NOT leave placeholders unfilled
5. **Launch subagents in parallel** for different topics
6. **Update progress.md** after all subagents complete

#### Subagent Prompt Template

**IMPORTANT: Copy this template and replace ALL bracketed placeholders with actual values before launching subagent.**

```markdown
## Task: Extract [TOPIC] Knowledge Base

You are extracting knowledge from a book section to create a complete topic reference.

### Prerequisites - Read These Files First:
1. `skills/skill-from-book/references/file-templates.md` - Templates for all file types
2. `skills/skill-from-book/references/extraction-patterns.md` - Extraction rules

### Source Material:
- **Book**: [BOOK_PATH]
- **Section**: [CHAPTER/SECTION_NAME]
- **Line range**: Read with offset=[START_LINE], limit=[LINE_COUNT]

### Output Directory: [OUTPUT_TOPIC_PATH]

### Files to Create (in this order):

#### 1. knowledge.md (REQUIRED)
Core concepts, definitions, and foundational understanding.
- Extract: definitions, terminology, key concepts, how things relate
- Use the "Knowledge File" template

#### 2. rules.md (REQUIRED)
Specific guidelines, do's and don'ts.
- Extract: explicit rules, guidelines, best practices, exceptions
- Use the "Rules File" template

#### 3. examples.md (REQUIRED)
Good/bad code examples, before/after comparisons.
- Extract: all code samples, refactoring examples, comparisons
- Use the "Examples File" template

#### 4. [OPTIONAL_FILES - list any additional files needed]
[e.g., patterns.md, smells.md, checklist.md - specify what each should contain]

### Your Instructions:
1. Read the two prerequisite files FIRST to understand templates and extraction rules
2. Read the book section ONCE using: offset=[START_LINE], limit=[LINE_COUNT]
3. From that single read, extract content for ALL files listed above
4. For each file:
   - Transform content (prose → bullets, extract rules, include examples)
   - Format using the appropriate template from file-templates.md
   - Keep each file under 200 lines
   - Write to [OUTPUT_TOPIC_PATH]/[filename].md
5. Create files in order: knowledge.md → rules.md → examples.md → optional files

### Content Guidance:
[SPECIFIC_GUIDANCE - what to focus on, what to skip]

### Language Conversion (if applicable):
- Source: [SOURCE_LANG or "N/A"]
- Target: [TARGET_LANG or "N/A"]
- Convert ALL code examples to target language
```

#### Example: Filled Subagent Prompt

```markdown
## Task: Extract Functions Knowledge Base

You are extracting knowledge from a book section to create a complete topic reference.

### Prerequisites - Read These Files First:
1. `skills/skill-from-book/references/file-templates.md` - Templates for all file types
2. `skills/skill-from-book/references/extraction-patterns.md` - Extraction rules

### Source Material:
- **Book**: /path/to/clean-code.md
- **Section**: Chapter 3 - Functions
- **Line range**: Read with offset=450, limit=380

### Output Directory: skills/clean-code/references/functions

### Files to Create (in this order):

#### 1. knowledge.md (REQUIRED)
Core concepts, definitions, and foundational understanding.
- Extract: what makes a function clean, key terminology (side effects, arguments, abstraction levels), how functions relate to other concepts
- Use the "Knowledge File" template

#### 2. rules.md (REQUIRED)
Specific guidelines, do's and don'ts.
- Extract: size rules, argument limits, naming conventions, single responsibility, do one thing principle
- Use the "Rules File" template

#### 3. examples.md (REQUIRED)
Good/bad code examples, before/after comparisons.
- Extract: all code samples showing good vs bad functions, refactoring walkthroughs
- Use the "Examples File" template

#### 4. checklist.md (OPTIONAL)
Quick reference for reviewing functions.
- Create a checklist from the rules for code review

### Your Instructions:
1. Read the two prerequisite files FIRST to understand templates and extraction rules
2. Read the book section ONCE using: offset=450, limit=380
3. From that single read, extract content for ALL files listed above
4. For each file:
   - Transform content (prose → bullets, extract rules, include examples)
   - Format using the appropriate template from file-templates.md
   - Keep each file under 200 lines
   - Write to skills/clean-code/references/functions/[filename].md
5. Create files in order: knowledge.md → rules.md → examples.md → checklist.md

### Content Guidance:
Focus on practical, actionable content. Skip author anecdotes and historical context. Prioritize rules that are universally applicable.

### Language Conversion:
- Source: Java
- Target: TypeScript
- Convert ALL code examples to TypeScript
```

#### Parallel Extraction Strategy

**Run in parallel**: Different topics (each handled by one subagent)
- Subagent 1: functions/ (Chapter 3)
- Subagent 2: naming/ (Chapter 2)
- Subagent 3: classes/ (Chapter 10)

**Must wait**: guidelines.md and workflows creation waits for ALL topic subagents to complete

#### Main Agent Checklist Before Launching Subagent

- [ ] All placeholders replaced with actual values
- [ ] Line offset and limit calculated from Phase 1 TOC
- [ ] Output directory path follows naming convention
- [ ] All required files (knowledge.md, rules.md, examples.md) listed
- [ ] Optional files specified with clear content guidance
- [ ] Content guidance is specific to this topic
- [ ] Language conversion specified if needed

---

### Phase 4: Guidelines Creation

**STOP! Before proceeding, you MUST:**
1. Have completed all extraction tasks in Phase 3
2. Read `references/guidelines-template.md` completely
3. Only then proceed with guidelines creation

**Phase 4 Steps:**

Create `guidelines.md` that maps:
- Tasks → relevant files (and workflows)
- Code elements → relevant files
- Symptoms/problems → relevant files
- Decision trees for common scenarios

---

### Phase 5: Workflow Proposal

**STOP! Before proceeding, you MUST:**
1. Have completed Phase 4 (Guidelines)
2. Read `references/workflow-templates.md` completely
3. Only then proceed with workflow proposal

**Phase 5 Steps:**

1. **Identify potential workflows** from the book content

   Look for:
   - Process descriptions ("how to do X")
   - Repeated tasks (mentioned multiple times)
   - Checklists in the book
   - Anti-pattern sections (imply correct process)
   - Multi-step procedures

2. **Propose workflows to user**

   Present a list of potential workflows:
   ```
   Based on the book content, I recommend these workflows:
   
   | Workflow | Purpose | Key Steps |
   |----------|---------|-----------|
   | [name] | [what it does] | [brief step summary] |
   | [name] | [what it does] | [brief step summary] |
   ```

3. **Ask user to select** which workflows to create

   ```
   Which workflows would you like me to create?
   - Select from the list above
   - Suggest additional workflows
   - Skip workflow creation
   ```

4. **Create selected workflows**

   For each selected workflow:
   - Use the template from `references/workflow-templates.md`
   - Include cross-references to relevant knowledge files
   - Add checkboxes for each step
   - Define clear exit criteria

5. **Update guidelines.md** to include workflow references

   Add a "Workflows" section at the top of guidelines.md:
   ```markdown
   ## Workflows
   
   | Task | Workflow |
   |------|----------|
   | [task description] | `workflows/[name].md` |
   ```

---

### Phase 6: Finalization

**Phase 6 Steps:**

1. Review all files for consistency
2. Update progress.md (mark complete)
3. Test with sample queries
4. Refine guidelines based on testing
5. Ask user to review the final skill

---

## Key Principles

### Granularity
- One concept per file
- Files should be 50-200 lines
- Split large topics into subtopics

### Context Efficiency
- Only load what's needed
- Guidelines file routes to specific knowledge
- Avoid duplication across files

### Actionable Content
- Rules over explanations
- Examples over theory
- Checklists for quick reference
- **Workflows for repeatable tasks**

### Subagent-Friendly
- Each extraction task is independent
- Clear input/output specification
- Can run multiple extractions in parallel

## File Naming Conventions

```
skill-name/
├── SKILL.md
├── guidelines.md
├── progress.md
├── workflows/                # Step-by-step processes
│   ├── [verb]-[noun].md      # e.g., code-review.md, bug-fix.md
│   └── ...
└── references/
    ├── [category]/           # Noun, plural (e.g., functions, classes)
    │   ├── knowledge.md      # REQUIRED: Core concepts and definitions
    │   ├── rules.md          # REQUIRED: Specific guidelines
    │   ├── examples.md       # REQUIRED: Good/bad examples
    │   ├── patterns.md       # Optional: Reusable solutions
    │   ├── smells.md         # Optional: Anti-patterns
    │   └── checklist.md      # Optional: Quick reference
```

## Progress Tracking

Always maintain `progress.md`:

```markdown
# [Skill Name] - Creation Progress

## Status: [X/Y files complete]

## Phase 1: Foundation
- [x] SKILL.md
- [x] progress.md
- [ ] guidelines.md

## Phase 2: Workflows
- [ ] workflows/[name].md
- [ ] workflows/[name].md

## Phase 3: [Category Name]
- [ ] category/knowledge.md   # REQUIRED
- [ ] category/rules.md       # REQUIRED
- [ ] category/examples.md    # REQUIRED
- [ ] category/patterns.md    # Optional
...
```

## Quick Start

1. User provides the book markdown file path
2. **DO NOT read the book content yet**
3. Run Phase 1: Analysis (extract TOC only)
4. Get user confirmation
5. Run Phase 2: Planning
6. Get user confirmation
7. Run Phase 3: Extraction (use subagents)
8. Run Phase 4: Guidelines Creation
9. Run Phase 5: Workflow Proposal (get user selection)
10. Run Phase 6: Finalization
