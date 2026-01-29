---
name: course-generator
description: |
  Convert a course outline into a fully fleshed out intelligent textbook. Use when:
  (1) User provides a URL containing a course outline/syllabus
  (2) User asks to "generate a course" or "create a textbook" from an outline
  (3) User wants to expand a course description into full learning materials

  Generates: learning graph, chapter structure, MicroSim specifications, quizzes, glossary, and FAQ following the intelligent textbooks framework and evidence-based learning design principles.
---

# Course Generator

Convert course outlines into complete intelligent textbook courses.

## Prerequisites

Read the teaching philosophy context before generating any content:
- `/Users/vishal/admin/teaching-philosophy-context.md`

This provides the pedagogical principles that guide all content generation.

## Workflow

### Phase 0: Customization Questions

Before generating, ask these questions to customize the output:

```
1. TARGET AUDIENCE
   - Who is this course for? (students, professionals, self-learners)
   - What's their background/prerequisite knowledge?
   - Age/education level? (high school, college, graduate, professional)

2. FORMAT & DELIVERY
   - Self-paced online textbook? Live cohort? Hybrid?
   - Approximate total hours for completion?
   - Any specific platform constraints? (Canvas, MkDocs, other)

3. DEPTH & SCOPE
   - Full course or condensed version?
   - Which topics to emphasize or skip?
   - Include hands-on projects? What tools available?

4. ASSESSMENT STYLE
   - Quiz-heavy or project-based?
   - Include peer review components?
   - Public presentation/portfolio requirements?
```

Use AskUserQuestion tool with these as options, or gather through conversation.

### Phase 1: Parse & Analyze

#### URL Parsing Strategy

**For simple/static pages** (documentation sites, GitHub, simple HTML):
```
Use WebFetch to retrieve content
```

**For JS-heavy pages** (Maven, Coursera, Udemy, course platforms):
```
Use Chrome browser automation:
1. mcp__claude-in-chrome__tabs_context_mcp (get/create tab)
2. mcp__claude-in-chrome__navigate to URL
3. mcp__claude-in-chrome__computer action=wait duration=3
4. mcp__claude-in-chrome__read_page to get accessibility tree
5. Click "expand" buttons for syllabus/curriculum sections
6. mcp__claude-in-chrome__get_page_text or screenshot as needed
```

#### Extract Key Elements
- Course title and description
- Target audience and prerequisites
- Learning objectives (if stated)
- Topic list or module structure (expand collapsed sections!)
- Any existing assessments or projects

#### Identify Course Level
| Level | Glossary/Chapter | MicroSim Complexity |
|-------|------------------|---------------------|
| Junior high | ~10 terms | Simple, single-parameter |
| Senior high | ~15 terms | Moderate, 2-3 parameters |
| College | ~20 terms | Full treatment |
| Graduate | ~25 terms | Research connections |

---

## Parallel Subagent Execution

**Cost optimization**: Use haiku for structured/repetitive tasks, sonnet for creative/complex tasks.

### Phase 2-5: Launch Subagents in Parallel

After Phase 1 parsing and user approval of chapter structure, launch these subagents **in parallel** using a single message with multiple Task tool calls:

```
Task(subagent_type="general-purpose", model="haiku", prompt="[learning graph task]")
Task(subagent_type="general-purpose", model="haiku", prompt="[glossary task]")
Task(subagent_type="general-purpose", model="haiku", prompt="[quiz task]")
Task(subagent_type="general-purpose", model="sonnet", prompt="[chapter content task]")
Task(subagent_type="general-purpose", model="sonnet", prompt="[microsim spec task]")
```

### Subagent Task Assignments

#### Learning Graph Agent (haiku)
```
Generate a learning graph JSON for "[Course Name]".

Context: [paste parsed course outline]

REQUIREMENTS:

1. CONCEPT ENUMERATION (150-250 concepts)
   - Each concept label: Title Case, max 32 characters
   - Entity names only (not questions like "What is X")
   - Cover full breadth of course material

2. TAXONOMY CATEGORIZATION
   Assign each concept to exactly one category:
   - FOUND: Foundation concepts with NO dependencies (entry points)
   - BASIC: Build directly on foundations
   - INTER: Intermediate, build on basics
   - ADV: Advanced, build on intermediate
   - APP: Application/synthesis of multiple concepts

3. DEPENDENCY MAPPING (DAG structure)
   Critical validation rules:
   - NO circular dependencies (A→B→C→A is invalid)
   - NO self-dependencies (concept cannot depend on itself)
   - FOUND concepts have empty dependencies array
   - All other concepts have at least one dependency
   - Prefer multiple learning pathways over linear chains
   - Avoid long single-dependency chains (>5 concepts)

4. QUALITY METRICS TO ACHIEVE
   - Foundational concepts (zero dependencies): 10-15% of total
   - Orphaned nodes (nothing depends on them): <20% (except APP category)
   - Average dependencies per concept: 1.5-3.0
   - No disconnected subgraphs (all concepts reachable)

Output: learning-graph.json content only, valid JSON per schema
```

#### Glossary Agent (haiku)
```
Generate glossary entries for "[Course Name]".

Concepts to define: [list from learning graph]
Course level: [junior-high/senior-high/college/graduate]
Terms per chapter target: [10/15/20/25 based on level]

ISO 11179 DEFINITION STANDARDS (mandatory):

Each definition must be:
1. PRECISE: Exact meaning, no ambiguity, specific to course context
2. CONCISE: 20-50 words target, as brief as possible while complete
3. DISTINCT: Differentiates from similar terms
4. NON-CIRCULAR: Never use the term being defined in its definition
5. NO BUSINESS RULES: Definition only, not how it's used

QUALITY RUBRIC (aim for 85+ per definition):
- Precision (25 pts): Accurately captures meaning
- Conciseness (25 pts): Within 20-50 words
- Distinctiveness (25 pts): Unique, not copied
- Non-circularity (25 pts): No self-reference or undefined terms

FORMAT:
#### [Term]

[Definition in 1-2 sentences]

**Example:** [Concrete illustration from course domain]

REQUIREMENTS:
- Sort alphabetically (case-insensitive)
- 60-80% of terms should have examples
- Use simpler terms in definitions (avoid undefined jargon)

BAD: "A learning graph is a graph used for learning."
GOOD: "A directed graph of concepts showing prerequisite relationships for mastering a topic."

Output: glossary.md content only
```

#### Quiz Agent (haiku)
```
Generate quiz questions for "[Course Name]" Chapter [N]: [Title].

Chapter type: [introductory/intermediate/advanced]
Concepts covered: [list from learning graph]
Learning objectives: [from chapter structure]

BLOOM'S TAXONOMY DISTRIBUTION (adjust by chapter type):

Introductory chapters:
- 40% Remember, 40% Understand, 15% Apply, 5% Analyze

Intermediate chapters:
- 25% Remember, 30% Understand, 30% Apply, 15% Analyze

Advanced chapters:
- 15% Remember, 20% Understand, 25% Apply, 25% Analyze, 10% Evaluate, 5% Create

QUESTION STEMS BY LEVEL:
- Remember: Define..., List..., What is..., Name...
- Understand: Explain..., Describe..., Why does..., Summarize...
- Apply: How would you use..., Calculate..., Demonstrate...
- Analyze: Compare..., What is the relationship..., Why might...
- Evaluate: Assess..., Which is better..., Justify...
- Create: Design..., Propose..., How might you...

ANSWER BALANCE (critical):
- Distribute correct answers: A=25%, B=25%, C=25%, D=25% (±5%)
- Avoid patterns (not A-B-A-B, not all C's in a row)

DISTRACTOR QUALITY:
- All wrong answers must be plausible (sound reasonable)
- Similar length to correct answer
- No "All of the above" or "None of the above"
- No jokes or obviously wrong options
- Address common misconceptions

FORMAT (mkdocs-material):
#### 1. [Question text]?

<div class="upper-alpha" markdown>
1. [Option A]
2. [Option B]
3. [Option C]
4. [Option D]
</div>

??? question "Show Answer"
    The correct answer is **[LETTER]**.

    [Explanation 50-100 words: why correct, why others wrong]

    **Concept:** [Concept name]

Generate 8-12 questions per chapter.
Output: quiz.md content only
```

#### Chapter Content Agent (sonnet)
```
Generate chapter content for "[Course Name]" Chapter [N]: [Title].

Learning objectives: [list with Bloom's verbs]
Concepts to cover: [from learning graph, in dependency order]
Target word count: 1500-2500 words

TEACHING PHILOSOPHY (apply throughout):
- Low floor, high ceiling: Accessible entry, unlimited depth
- Concrete before abstract: Examples and stories before theory
- Intrinsic motivation: Connect to real problems students care about
- Socratic coaching: Reflection questions, not just content delivery

REQUIRED STRUCTURE:

## Learning Objectives
By the end of this chapter, you will be able to:
1. [Bloom's verb] [specific outcome]
2. [Bloom's verb] [specific outcome]
3. [Bloom's verb] [specific outcome]

## Introduction
[Hook: Story, question, or real-world scenario that motivates the topic]
[Why this matters - connect to student's world]

## Section 1: [Foundation Concept]
[Concrete example FIRST, then abstract principle]

### Key Idea
[Core concept in 1-2 sentences]

### Example
[Worked example with step-by-step explanation]

### Try It
[Low-stakes practice opportunity - something student can do now]

## Section 2: [Building Concept]
[Build on Section 1, introduce complexity]

## Section 3: [Application]
[Real-world use cases, synthesis]

## Reflection Questions
1. [Socratic question prompting deeper thinking]
2. [Question connecting to student's own experience]
3. [Question about assumptions or limitations]

## Summary
- [3-5 bullet points of key takeaways]

## Next Steps
[Preview next chapter, how concepts connect]

Output: index.md content only
```

#### MicroSim Spec Agent (sonnet)
```
Generate MicroSim specifications for "[Course Name]" Chapter [N].

Concepts to visualize: [list abstract concepts that benefit from interactivity]
Course level: [junior-high/senior-high/college/graduate]

FOR EACH MICROSIM, SPECIFY:

## MicroSim: [Name]

### Concept Visualized
- **Concept:** [From learning graph]
- **Learning Goal:** Students will understand [X] by manipulating [Y] and observing [Z]
- **Difficulty:** [Beginner/Intermediate/Advanced]

### Controls (Right Panel)
| Control | Type | Range | Default | Effect |
|---------|------|-------|---------|--------|
| [Name] | slider | [min]-[max] | [val] | [What changes] |
| [Name] | button | - | - | [What happens on click] |
| [Name] | dropdown | [options] | [val] | [What changes] |

### Visualization (Left Panel)
- What is drawn (shapes, graphs, animations)
- How it responds to control changes
- Color/size encoding (if any)
- Animation behavior

### The "Aha" Moment
When the student [does specific action], they see [specific result],
which demonstrates [principle/insight].

### Technical Notes
- Canvas: Responsive, min 400px width
- Frame rate: 30fps (or specify if different)
- Library: p5.js
- Mobile: Touch-friendly controls required

### Assessment Integration
After using this MicroSim, students should be able to answer:
1. [Quiz question this prepares them for]
2. [Another related question]

COMPLEXITY BY LEVEL:
- Junior high: 1-2 controls, simple cause-effect
- Senior high: 2-3 controls, moderate relationships
- College: 3-4 controls, complex interactions
- Graduate: 4+ controls, research-level visualizations

Output: spec.md content for each MicroSim
```

#### FAQ Agent (haiku)
```
Generate FAQ for "[Course Name]".

Course description: [summary]
Target audience: [from customization]
Prerequisites: [list]
Chapter topics: [list]
Common misconceptions in this domain: [if known]

REQUIREMENTS:

Generate 15-25 questions across these categories:

1. CONCEPTUAL CLARIFICATIONS (30%)
   - "What is the difference between X and Y?"
   - "Why is X important in this field?"
   - "How does X relate to Y?"

2. COMMON MISCONCEPTIONS (25%)
   - "Is it true that X always causes Y?"
   - "Why do people think X when actually Y?"
   - Address errors students typically make

3. PRACTICAL APPLICATIONS (25%)
   - "How do I apply X in real situations?"
   - "When should I use X vs Y?"
   - "What tools/resources help with X?"

4. PREREQUISITES & NEXT STEPS (20%)
   - "What should I know before starting?"
   - "What should I learn after this course?"
   - "How does this connect to [related field]?"

ANSWER GUIDELINES:
- 2-4 sentences per answer (concise but complete)
- Reference specific chapter when helpful: "See Chapter 3 for details"
- Use concrete examples where possible
- Avoid jargon not defined in glossary

FORMAT:
## [Category Name]

### Q: [Question]?

[Answer in 2-4 sentences]

Output: faq.md content only
```

---

## Orchestration Flow

```
┌─────────────────────────────────────────────────────────────┐
│ PHASE 1: Parse URL (main agent)                             │
│ - Use Chrome for JS-heavy pages                             │
│ - Extract course structure                                  │
│ - Identify level                                            │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ USER CHECKPOINT: Approve chapter structure                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 2-5: Parallel Subagents (single message)              │
│                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │Learning Graph│ │   Glossary   │ │    Quizzes   │        │
│  │   (haiku)    │ │   (haiku)    │ │   (haiku)    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
│                                                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │   Chapters   │ │ MicroSim Spec│ │     FAQ      │        │
│  │   (sonnet)   │ │   (sonnet)   │ │   (haiku)    │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ PHASE 6: Assembly (main agent)                              │
│ - Compile outputs into course structure                     │
│ - Generate mkdocs.yml                                       │
│ - Validate cross-references                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Output Structure

```
course-name/
├── docs/
│   ├── index.md                    # Course home page
│   ├── course-description.md       # Full course description
│   ├── chapters/
│   │   ├── 01-chapter-name/
│   │   │   ├── index.md            # Chapter content
│   │   │   └── quiz.md             # Chapter quiz
│   │   └── ...
│   ├── sims/
│   │   ├── sim-name/
│   │   │   ├── index.md            # MicroSim documentation
│   │   │   └── spec.md             # Implementation spec
│   │   └── ...
│   ├── learning-graph/
│   │   └── learning-graph.json     # Concept dependency graph
│   ├── glossary.md                 # Master glossary
│   └── faq.md                      # FAQ
└── mkdocs.yml                      # MkDocs configuration
```

## Phase 6: Assembly & Validation

After subagents complete, validate and assemble outputs:

### Quality Checklist

#### Learning Graph Validation
- [ ] Valid JSON (parse without errors)
- [ ] 150-250 concepts present
- [ ] No circular dependencies (DAG structure)
- [ ] Foundational concepts (zero deps): 10-15%
- [ ] All categories used (FOUND, BASIC, INTER, ADV, APP)
- [ ] No disconnected subgraphs

#### Glossary Validation
- [ ] All terms from learning graph included
- [ ] Alphabetically sorted
- [ ] Definitions 20-50 words average
- [ ] 60%+ have examples
- [ ] No circular definitions (term used in own definition)

#### Quiz Validation
- [ ] 8-12 questions per chapter
- [ ] Answer distribution balanced (A/B/C/D within 20-30% each)
- [ ] Bloom's levels present (Remember, Understand, Apply, Analyze)
- [ ] All questions have explanations
- [ ] mkdocs format correct (upper-alpha div, question admonition)

#### Chapter Content Validation
- [ ] 1500-2500 words per chapter
- [ ] Learning objectives present
- [ ] Hook/Introduction engaging
- [ ] Examples before abstract concepts
- [ ] "Try It" sections present
- [ ] Reflection questions (not just recall)

#### Cross-Reference Validation
- [ ] Glossary terms align with learning graph concepts
- [ ] Quiz concepts reference learning graph
- [ ] Chapter sections cover assigned concepts
- [ ] MicroSims reference specific concepts

### Assembly Steps

1. Create directory structure per Output Structure
2. Write each file to appropriate location
3. Generate mkdocs.yml with navigation
4. Run `mkdocs build` to verify no broken links
5. Report summary to user:
   - Total concepts: X
   - Total glossary terms: X
   - Total quiz questions: X
   - Chapters generated: X
   - MicroSim specs: X

---

## Key Principles (from Teaching Philosophy)

Apply throughout generation:

1. **Low floor, high ceiling**: Accessible entry points, unlimited depth
2. **Intrinsic motivation**: Connect to real problems students care about
3. **Build → Present → Feedback → Iterate**: Design projects with public output
4. **Socratic coaching**: Include reflection questions, not just content
5. **Concrete before abstract**: Stories and examples before theory
6. **Friction as signal**: Include peer review, public presentation requirements

## Reference Files

- [Output Formats](references/output-formats.md) - JSON schemas and markdown templates for all artifacts
