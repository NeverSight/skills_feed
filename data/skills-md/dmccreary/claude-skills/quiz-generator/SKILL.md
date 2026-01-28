---
name: quiz-generator
description: This skill generates interactive multiple-choice quizzes for each chapter of an intelligent textbook, with questions aligned to specific concepts from the learning graph and distributed across Bloom's Taxonomy cognitive levels to assess student understanding effectively. Use this skill after chapter content has been written and the learning graph exists.
license: MIT
---

# Quiz Generator for Intelligent Textbooks

**Version:** 0.2

## Overview 
1. For each markdown chapter, generate interactive multiple-choice quizzes for textbook chapters with and quality distractor analysis.
2. Generate quality reports in markdown format.
3. Updated mkdocs.yml navigation to include quizzes and reports.

## Purpose

This skill automates quiz creation for intelligent textbooks by analyzing chapter content to generate contextually relevant multiple-choice questions. Each quiz is aligned to specific concepts from the learning graph, distributed across Bloom's Taxonomy cognitive levels, and formatted using mkdocs-material question admonitions with upper-alpha (A, B, C, D) answer choices. The skill ensures quality distractors, balanced answer distribution, and comprehensive explanations for educational value.

## When to Use This Skill

Use this skill after:

1. Chapter content has been generated or written (1000+ words per chapter)
2. Learning graph exists with concept dependencies
3. Glossary is available (recommended for terminology questions)

Trigger this skill when:

- Creating quizzes for new chapters
- Updating quizzes after content revisions
- Building comprehensive quiz bank for entire textbook
- Exporting quiz data for LMS or chatbot integration

The skill can run incrementally (chapter by chapter) or in batch mode (entire textbook).

## Workflow

### Step 1: Assess Content Readiness

Indicate to the user that the Quiz Generator Skill (version) is running.

Calculate content readiness score (1-100) for each target chapter:

**Quality Checks:**

#### 1. **Chapter word count:**
   - 2000+ words = excellent (20 pts)
   - 1000-1999 words = good (15 pts)
   - 500-999 words = basic (10 pts)
   - <500 words = insufficient (5 pts)

#### 2. **Example coverage:**
   - 60%+ concepts with examples = excellent (20 pts)
   - 40-59% = good (15 pts)
   - 20-39% = basic (10 pts)
   - <20% = insufficient (5 pts)

#### 3. **Glossary coverage:**
   - 80%+ chapter concepts defined = excellent (20 pts)
   - 60-79% = good (15 pts)
   - 40-59% = basic (10 pts)
   - <40% = insufficient (5 pts)

#### 4. **Concept clarity:**
   - Clear explanations for all concepts (20 pts)
   - Most concepts clear (15 pts)
   - Some unclear concepts (10 pts)
   - Many unclear concepts (5 pts)

#### 5. **Learning graph alignment:**
   - All chapter concepts mapped (20 pts)
   - Most mapped (15 pts)
   - Some mapped (10 pts)
   - Few mapped (5 pts)

**Content Readiness Ranges:**

- 90-100: Rich content, excellent quiz quality possible
- 70-89: Good content, solid quiz possible
- 50-69: Basic content, limited quiz possible
- Below 50: Insufficient content for quality quiz

**User Dialog Triggers:**

- Score < 60: Ask "Chapter [X] has limited content ([N] words). Generate shorter quiz or skip?"
- No glossary: Ask "No glossary found. Definition questions will be limited. Proceed?"
- Concept gaps: Ask "[N] concepts in chapter not in learning graph. Continue with available concepts?"
- No learning outcomes: Ask "No Bloom's Taxonomy outcomes in course description. Use default distribution?"

### Step 2: Determine Target Distribution

Based on chapter type (introductory, intermediate, advanced), set target Bloom's Taxonomy distribution:

**Introductory Chapters:**
- 40% Remember
- 40% Understand
- 15% Apply
- 5% Analyze
- 0% Evaluate
- 0% Create

**Intermediate Chapters:**
- 25% Remember
- 30% Understand
- 30% Apply
- 15% Analyze
- 0% Evaluate
- 0% Create

**Advanced Chapters:**
- 15% Remember
- 20% Understand
- 25% Apply
- 25% Analyze
- 10% Evaluate
- 5% Create

Determine chapter type by:
- Position in textbook (first 3 chapters = introductory)
- Concept centrality in learning graph (high centrality = advanced)
- Explicit markers in chapter metadata
- User specification

Target question count: 8-12 per chapter (default: 10)

### Step 3: Identify Concepts to Test

Analyze chapter content and learning graph to prioritize concepts:

**Priority 1 (Must Test):**
- High-centrality concepts in learning graph
- Concepts mentioned in chapter title or introduction
- Concepts with dedicated sections
- Key terms emphasized in bold or glossary links

**Priority 2 (Should Test):**
- Supporting concepts with substantial explanation
- Concepts with examples
- Prerequisites reviewed in chapter
- Concepts from learning objectives

**Priority 3 (May Test):**
- Peripheral concepts mentioned briefly
- Related concepts for context
- Future topics previewed

Aim for 80%+ coverage of Priority 1 concepts.

### Step 4: Generate Questions by Bloom's Level

For each concept selected for testing, generate question at appropriate Bloom's level following target distribution.

**IMPORTANT FORMATTING REQUIREMENT:**

All questions MUST use the mkdocs-material question admonition format with upper-alpha list styling:

```markdown
#### 1. What is the primary purpose of a learning graph?

<div class="upper-alpha" markdown>
1. To create visual decorations for textbooks
2. To map prerequisite relationships between concepts
3. To generate random quiz questions
4. To organize files in a directory structure
</div>

??? question "Show Answer"
    The correct answer is **B**. A learning graph is a directed graph that maps prerequisite relationships between concepts, showing which concepts must be learned before others. This ensures proper scaffolding in educational content.

    **Concept Tested:** Learning Graph

    **See:** [Learning Graph Concept](../concepts/learning-graph.md)
```

**Formatting Rules:**

1. Use level-4 header (####) with question number
2. Write question as complete sentence ending with ?
3. Use `<div class="upper-alpha" markdown>` wrapper
4. Write 4 answer options as numbered list (1, 2, 3, 4)
5. Use `??? question "Show Answer"` admonition
6. Indent answer content with 4 spaces
7. Start with "The correct answer is **[LETTER]**."
8. Include concept name and link to source
9. Maintain blank line before and after div

**Question Writing Guidelines:**

**Remember Level:**
- Ask for definitions from glossary
- Test fact recall
- Identify terminology
- Example: "What is the definition of [concept]?"

**Understand Level:**
- Ask for explanations
- Test comprehension of relationships
- Compare/contrast concepts
- Example: "Which best describes the relationship between [A] and [B]?"

**Apply Level:**
- Present scenarios requiring concept application
- Test problem-solving using learned methods
- Example: "Given [scenario], which approach would you use?"

**Analyze Level:**
- Ask to identify patterns or causes
- Test ability to break down concepts
- Example: "What is the underlying reason for [phenomenon]?"

**Evaluate Level:**
- Ask for judgments based on criteria
- Test critical thinking
- Example: "Which approach would be most effective for [goal]?"

**Create Level:**
- Ask to design solutions
- Test synthesis of concepts
- Example: "How would you design a [system] that [requirements]?"

### Step 5: Write Quality Distractors

For each incorrect answer option (distractors), ensure:

**Plausibility:**
- Sounds reasonable to someone who hasn't learned the material
- Uses related terminology
- Avoids obviously wrong answers
- Similar length to correct answer

**Educational Value:**
- Addresses common misconceptions
- Tests understanding of related concepts
- Discriminates between levels of knowledge
- Not trick questions or word games

**Common Distractor Patterns:**

- Partial truth (correct in different context)
- Reversal (opposite of correct answer)
- Similar terminology (related but distinct concept)
- Common error (typical student mistake)

**Avoid:**
- "All of the above" or "None of the above"
- Jokes or nonsensical options
- Grammatically inconsistent options
- Answers that overlap or both could be correct

### Step 6: Write Explanations

For each question, write explanation that:

**Confirms Correct Answer:**
- State clearly: "The correct answer is **[LETTER]**."
- Explain why this answer is correct
- Reference chapter content or concept definition
- Target: 50-100 words

**Teaches (Optional but Recommended):**
- Briefly explain why distractors are incorrect
- Clarify common misconceptions
- Provide additional context
- Link to chapter section for more detail

**Example Explanation:**

```
The correct answer is **B**. A learning graph is a directed graph that maps
prerequisite relationships between concepts. Option A is incorrect because
learning graphs serve a structural purpose, not decorative. Option C is
incorrect because quiz generation is not the primary purpose. Option D
confuses learning graphs with file systems.

**Concept Tested:** Learning Graph

**See:** [Learning Graph Concept](../concepts/learning-graph.md#definition)
```

### Step 7: Ensure Answer Balance

Check that correct answers are distributed evenly across A, B, C, D:

**Target Distribution:**
- A: 25% (±5%)
- B: 25% (±5%)
- C: 25% (±5%)
- D: 25% (±5%)

**Avoid Patterns:**
- All C's in a row
- Alternating A-B-A-B
- Predictable sequences
- Position bias (first/last always correct)

**Randomization Strategy:**
- Generate random sequence before writing quiz
- Shuffle for each question
- Verify distribution after completion
- Adjust if imbalanced

### Step 8: Create Quiz File

Generate quiz file with proper structure:

**Option 1: Separate Quiz File** (`docs/[section]/[chapter-name]-quiz.md`):

```markdown
# Quiz: [Chapter Name]

Test your understanding of [chapter topic] with these questions.

---

#### 1. [Question text]?

<div class="upper-alpha" markdown>
1. [Option 1]
2. [Option 2]
3. [Option 3]
4. [Option 4]
</div>

??? question "Show Answer"
    The correct answer is **[LETTER]**. [Explanation]

    **Concept Tested:** [Concept Name]

    **See:** [Link to chapter section]

---

#### 2. [Question text]?

[Continue for all questions...]
```

**Option 2: Embedded in Chapter** (append to chapter file):

```markdown
[Chapter content...]

---

## Chapter Quiz

Test your understanding with these review questions.

#### 1. [Question text]?

[Continue with quiz questions...]
```

**Formatting Requirements:**
- Use horizontal rules (---) between questions
- Number questions sequentially (1, 2, 3...)
- Maintain consistent spacing
- Ensure all markdown renders correctly

### Step 9: Generate Metadata File

Create `docs/learning-graph/quizzes/[chapter-name]-quiz-metadata.json`:

```json
{
  "chapter": "Chapter Name",
  "chapter_file": "docs/section/chapter-name.md",
  "quiz_file": "docs/section/chapter-name-quiz.md",
  "generated_date": "YYYY-MM-DD",
  "total_questions": 10,
  "content_readiness_score": 85,
  "overall_quality_score": 78,
  "questions": [
    {
      "id": "ch1-q001",
      "number": 1,
      "question_text": "What is the primary purpose of a learning graph?",
      "correct_answer": "B",
      "bloom_level": "Understand",
      "difficulty": "medium",
      "concept_tested": "Learning Graph",
      "source_link": "../concepts/learning-graph.md",
      "distractor_quality": 0.85,
      "explanation_word_count": 67
    }
  ],
  "answer_distribution": {
    "A": 2,
    "B": 3,
    "C": 3,
    "D": 2
  },
  "bloom_distribution": {
    "Remember": 2,
    "Understand": 4,
    "Apply": 3,
    "Analyze": 1,
    "Evaluate": 0,
    "Create": 0
  },
  "concept_coverage": {
    "total_concepts": 12,
    "tested_concepts": 10,
    "coverage_percentage": 83
  }
}
```

### Step 10: Generate Quiz Bank (Aggregate)

Create or update `docs/learning-graph/quiz-bank.json` with all questions:

```json
{
  "textbook_title": "Building Intelligent Textbooks",
  "generated_date": "YYYY-MM-DD",
  "total_chapters": 20,
  "total_questions": 187,
  "questions": [
    {
      "id": "ch1-q001",
      "chapter": "Introduction to Learning Graphs",
      "question_text": "What is the primary purpose of a learning graph?",
      "options": {
        "A": "To create visual decorations for textbooks",
        "B": "To map prerequisite relationships between concepts",
        "C": "To generate random quiz questions",
        "D": "To organize files in a directory structure"
      },
      "correct_answer": "B",
      "explanation": "A learning graph is a directed graph...",
      "bloom_level": "Understand",
      "difficulty": "medium",
      "concept": "Learning Graph",
      "chapter_file": "docs/concepts/learning-graph.md",
      "source_section": "#definition",
      "tags": ["graph", "prerequisites", "scaffolding"]
    }
  ]
}
```

**Use Cases for Quiz Bank:**
- LMS export (Moodle, Canvas, Blackboard XML)
- Quiz randomization (select subset)
- Alternative quiz versions
- Chatbot integration (practice questions)
- Study app integration

### Step 11: Generate Quality Report

Create `docs/learning-graph/quiz-generation-report.md`:

```markdown
# Quiz Generation Quality Report

Generated: YYYY-MM-DD

## Overall Statistics

- **Total Chapters:** 20
- **Total Questions:** 187
- **Avg Questions per Chapter:** 9.4
- **Overall Quality Score:** 76/100

## Per-Chapter Summary

| Chapter | Questions | Quality Score | Bloom's Score | Coverage |
|---------|-----------|---------------|---------------|----------|
| Ch 1: Introduction | 10 | 82/100 | 24/25 | 83% |
| Ch 2: Learning Graphs | 12 | 78/100 | 22/25 | 90% |
| ... | ... | ... | ... | ... |

## Bloom's Taxonomy Distribution (Overall)

| Level | Actual | Target | Deviation |
|-------|--------|--------|-----------|
| Remember | 22% | 25% | -3% ✓ |
| Understand | 28% | 30% | -2% ✓ |
| Apply | 27% | 25% | +2% ✓ |
| Analyze | 18% | 15% | +3% ✓ |
| Evaluate | 4% | 4% | 0% ✓ |
| Create | 1% | 1% | 0% ✓ |

**Bloom's Distribution Score:** 24/25 (excellent)

## Answer Balance (Overall)

- A: 24% (45/187)
- B: 26% (49/187)
- C: 25% (47/187)
- D: 25% (46/187)

**Answer Balance Score:** 15/15 (perfect distribution)

## Concept Coverage

- **Total Concepts:** 198
- **Tested Concepts:** 156
- **Coverage:** 79%

**Coverage Score:** 16/20 (good)

## Question Quality Analysis

- **Well-formed questions:** 92% (172/187)
- **Quality distractors:** 88% avg
- **Clear explanations:** 100%
- **Valid links:** 98%

**Question Quality Score:** 28/30 (excellent)

## Recommendations

### High Priority

1. Increase coverage for 15 untested high-centrality concepts
2. Add 2-3 more Remember-level questions (+3%)
3. Fix 3 questions with ambiguous phrasing

### Medium Priority

1. Improve distractors for 12 questions (quality < 80%)
2. Add more Apply-level questions for Ch 5, 8, 12
3. Verify and update any broken links
4. Remove labels that do not point to valid document section headers

### Low Priority

1. Add alternative questions for popular concepts
2. Create study guide versions
3. Export to LMS-compatible formats

## Gaps by Chapter

**Chapters with low coverage (<70%):**

- Ch 7: Advanced Concepts (64% coverage) - Missing questions for: [list]
- Ch 14: Integration Patterns (58% coverage) - Missing questions for: [list]
```

### Step 12: Validate Quality

Perform comprehensive validation:

**1. No Ambiguity:**
- Each question has exactly one defensible correct answer
- Question stem is clear and complete
- No grammatical errors

**2. Distractor Quality:**
- All wrong answers are plausible
- Distractors test understanding, not just guessing
- Similar length and grammatical structure
- No overlapping answers

**3. Grammar & Clarity:**
- Professional writing throughout
- Consistent verb tense
- Proper punctuation
- No typos

**4. Answer Balance:**
- Correct answers distributed across A, B, C, D
- Within 20-30% per option (target: 25%)
- No predictable patterns

**5. Bloom's Distribution:**
- Matches target for chapter type
- Within ±15% acceptable
- Progressive difficulty through quiz

**6. Concept Coverage:**
- 75%+ of major concepts tested
- Important concepts have multiple questions
- No over-testing trivial concepts

**7. No Duplicates:**
- Unique questions across all quizzes
- No near-duplicates (>80% similar)

**8. Explanation Quality:**
- All questions have explanations
- Explanations teach, not just confirm
- 50-100 words target
- Reference chapter sections

**9. Link Validation:**
- All source links point to existing content
- Use section anchors where appropriate
- Links render correctly
- Do not place links in quiz.md files that do not work
- Do not use link labels to sections that do not exist

**10. Bias Check:**
- No cultural bias
- No gender bias
- No assumptions about background
- Accessible language

**Success Criteria:**
- Overall quality score > 70/100
- 8-12 questions per chapter
- Bloom's distribution within ±15% of target
- 75%+ concept coverage
- Answer balance within 20-30% per option
- 100% questions have explanations
- No duplicate questions
- All links valid

### Step 13: Generate Alternative Questions (Optional)

Create `docs/learning-graph/quizzes/alternative-questions.json` with 2-3 alternative questions per concept:

```json
{
  "alternatives": [
    {
      "concept": "Learning Graph",
      "questions": [
        {
          "question_text": "Which data structure is used to represent a learning graph?",
          "options": {
            "A": "Linked list",
            "B": "Directed acyclic graph",
            "C": "Binary tree",
            "D": "Hash table"
          },
          "correct_answer": "B",
          "bloom_level": "Remember"
        },
        {
          "question_text": "What problem does a learning graph solve?",
          "options": {
            "A": "Organizing files alphabetically",
            "B": "Determining concept learning order",
            "C": "Generating quiz questions",
            "D": "Creating visual diagrams"
          },
          "correct_answer": "B",
          "bloom_level": "Understand"
        }
      ]
    }
  ]
}
```

Use for:
- Quiz randomization
- Test variations (A/B versions)
- Practice mode (different questions each time)
- Adaptive difficulty

## Question Format Reference

### Complete Example with All Elements

```markdown
#### 3. Given a course with 50 concepts, what is the most important factor in organizing the learning graph?

<div class="upper-alpha" markdown>
1. Alphabetical order of concept names
2. Prerequisite relationships between concepts
3. The length of concept definitions
4. The visual appearance of the graph diagram
</div>

??? question "Show Answer"
    The correct answer is **B**. Prerequisite relationships are the most important factor because they determine the order in which concepts must be learned. A learning graph maps these dependencies to ensure students learn foundational concepts before advanced ones. Alphabetical order (A) and visual appearance (D) are organizational preferences, not educational requirements. Definition length (C) does not affect concept sequencing.

    **Concept Tested:** Learning Graph Structure

    **See:** [Learning Graph](../concepts/learning-graph.md#prerequisites)
```

### Formatting Checklist

- [ ] Level-4 header with question number
- [ ] Complete sentence ending with ?
- [ ] `<div class="upper-alpha" markdown>` wrapper
- [ ] Numbered list (1, 2, 3, 4) for options
- [ ] Closing `</div>` tag
- [ ] `??? question "Show Answer"` admonition
- [ ] 4-space indentation in answer block
- [ ] "The correct answer is **[LETTER]**." statement
- [ ] Explanation (50-100 words)
- [ ] **Concept Tested:** label
- [ ] **See:** link with proper path
- [ ] Blank lines before and after div

## Common Pitfalls to Avoid

**Format Errors:**
- ❌ Forgetting `<div class="upper-alpha" markdown>` wrapper
- ❌ Using letters (A, B, C, D) instead of numbers in list
- ❌ Incorrect indentation in answer block
- ❌ Missing closing `</div>` tag

**Question Quality:**
- ❌ Ambiguous questions with multiple correct answers
- ❌ "All of the above" or "None of the above" options
- ❌ Trick questions or word games
- ❌ Questions testing trivial facts

**Distractor Quality:**
- ❌ Obviously wrong answers
- ❌ Joke options or nonsense
- ❌ Distractors much longer/shorter than correct answer
- ❌ Options that overlap or contradict

**Explanation Quality:**
- ❌ Just restating the question
- ❌ No teaching value
- ❌ Missing or broken links
- ❌ Too brief (< 30 words) or too long (> 150 words)

## Output Files Summary

**Required (Per Chapter):**
1. Quiz markdown file (separate or embedded)
2. Quiz metadata JSON

**Recommended (Aggregate):**
3. `docs/learning-graph/quiz-bank.json` - All questions database
4. `docs/learning-graph/quiz-generation-report.md` - Quality metrics

**Optional:**
5. `docs/learning-graph/quizzes/alternative-questions.json` - Alternative questions
6. `docs/[section]/[chapter-name]-study-guide.md` - Study guide
7. Navigation updates to link quizzes

## Example Session

**User:** "Generate a quiz for Chapter 3"

**Claude (using this skill):**

1. Assesses Chapter 3 content readiness (score: 82/100)
2. Determines chapter type: intermediate
3. Sets target distribution: 25% Remember, 30% Understand, 30% Apply, 15% Analyze
4. Identifies 12 concepts to test (10 priority 1, 2 priority 2)
5. Generates 10 questions using question admonition format
6. Creates quality distractors
7. Ensures answer balance (A: 2, B: 3, C: 3, D: 2)
8. Writes explanations without links unless you can verify that the file and label target exist before you create links
9. Creates metadata JSON
10. Updates quiz bank
11. Reports: "Created 10-question quiz for Chapter 3. Quality score: 78/100. Bloom's distribution: 2 Remember, 3 Understand, 3 Apply, 2 Analyze. Concept coverage: 83%."

### Step 14: Update Site Navigation to Include Quizzes and Reports

Now update the `mkdocs.yml` file to include the quizzes in each chapter directory.

Use a format similar to this: where the chapter content in the index.md and the quiz
file each have a different line under the chapter.

```yml
nav:
  ...
  - Chapters:
    - Overview: chapters/index.md
    - 1. Introduction to AI and Intelligent Textbooks:
      - Content: chapters/01-intro-ai-intelligent-textbooks/index.md
      - Quiz: chapters/01-intro-ai-intelligent-textbooks/quiz.md
    - 2. Getting Started with Claude and Skills:
      - Content: chapters/02-getting-started-claude-skills/index.md
      - Quiz: chapters/02-getting-started-claude-skills/quiz.md
    - 3. Course Design and Educational Theory:
      - Content: chapters/03-course-design-educational-theory/index.md
      - Quiz: chapters/03-course-design-educational-theory/quiz.md
```

Note that the string "Chapter" should **not** be placed in the main chapter content label that points to the index.md file.

Next, update the `mkdocs.yml` to include the quiz quality reports that
have been placed in the learning-graph directory.

```yml
nav:
  ...
  Learning Graph:
    ...
    Quiz Generation Report: learning-graph/quiz-generation-report.md
```

### Step 15: Write Session Log File

Export the session information to `logs/quiz-generator-YYYY-MM-DD.md`
where YYYY-MM-DD is the current date.

### Step 15: Write Session Log File

Notify the user that the site navigation section of the `mkdocs.yml` file has 
been updated to include both the links to the new quizzes as well
as the quiz reports in the learning-graph.  Tell them that the session
has been logged to `logs/quiz-generator-YYYY-MM-DD.md`