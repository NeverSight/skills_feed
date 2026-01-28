---
name: faq-generator
description: This skill generates a comprehensive set of Frequently Asked Questions (FAQs) from the course description, course content, learning graphs, concept lists, MicroSims, and glossary terms to help students understand common questions and prepare content for chatbot integration. Use this skill after course description, learning graph, glossary, and at least 30% of chapter content exist.
license: MIT
---

# FAQ Generator

Generate comprehensive, categorized FAQs from textbook content and chatbot-ready JSON exports.  Place the
FAQs into the file docs/faq.md.  Log the results of the session to `logs/faq.md`.

## Purpose

This skill automates FAQ creation for intelligent textbooks by analyzing course content, learning graphs, and glossary terms to generate relevant questions and answers. The skill organizes questions by category and difficulty, ensures Bloom's Taxonomy distribution across cognitive levels, provides answers with links to source content, and exports structured JSON data ready for RAG system integration.

## When to Use This Skill

Use this skill after the following artifacts exist:

1. Course description has been finalized with a quality score above 70
2. Learning graph has been created
3. Glossary has been generated
4. At least 30% of chapter content has been written

Having these prerequisites ensures the FAQ generator has sufficient context to create meaningful, relevant questions. Trigger this skill when:

- Building initial FAQ for a new textbook
- Updating FAQ after significant content additions
- Preparing content for chatbot or AI assistant integration
- Identifying knowledge gaps in existing content

## Markdown Formatting

1. Use markdown header level one (#) for the FAQ title
2. Use markdown header level two (##) for each category
3. Use markdown header level three (###) for each individual question
4. Place the answer in the body text

Use the faq-template.md in the skill references section as your template.

## Workflow

### Step 1: Assess Content Completeness

Calculate a content completeness score (1-100 scale) to determine FAQ generation feasibility:

**Required Inputs:**

1. Read `docs/course-description.md`
   - Check for: title, audience, prerequisites, learning outcomes
   - Verify Bloom's Taxonomy outcomes present
   - Score: 25 points if complete

2. Read `docs/learning-graph/03-concept-dependencies.csv`
   - Validate DAG structure (no cycles)
   - Count concepts and dependencies
   - Score: 25 points if valid DAG with good connectivity

3. Read `docs/glossary.md`
   - Count terms (50+ = good, 100+ = excellent)
   - Score: 15 points for 100+, 10 for 50-99, 5 for <50

4. Scan all `docs/**/*.md` files
   - Calculate total word count
   - Target: 10,000+ words for comprehensive FAQ
   - Score: 20 points for 10k+, 15 for 5k-10k, 10 for <5k

5. Calculate concept coverage
   - What % of learning graph concepts have related chapter content?
   - Score: 15 points for 80%+, 10 for 60-79%, 5 for <60%

**Content Completeness Score Ranges:**

- 90-100: All inputs present with high quality
- 70-89: Core inputs present, some content gaps
- 50-69: Missing optional inputs or low word count
- Below 50: Critical inputs missing

**User Dialog Triggers:**

- Score < 60: Ask "Limited content available for FAQ generation. Continue with basic FAQ or wait for more content?"
- No glossary: Ask "No glossary found. Generate FAQ anyway (limited technical questions) or create glossary first?"
- Low word count: Ask "Only [N] words of content found. FAQ quality may be limited. Proceed?"

If user agrees to proceed with score < 60, generate FAQ but include disclaimer in quality report about limited content.

### Step 2: Analyze Content for Question Opportunities

Read and analyze all content sources to identify common question patterns:

**From Course Description:**

- "What is this course about?" (scope)
- "Who is this course for?" (audience)
- "What will I learn?" (outcomes)
- "What do I need to know first?" (prerequisites)

**From Learning Graph:**

- "What is [concept]?" (definition questions)
- "How does [concept A] relate to [concept B]?" (relationship questions)
- "What do I need to know before learning [concept]?" (prerequisite questions)
- "What comes after [concept]?" (progression questions)

**From Glossary:**

- "What does [term] mean?" (terminology questions)
- "What's the difference between [term A] and [term B]?" (comparison questions)
- "Can you give an example of [term]?" (application questions)

**From Chapter Content:**

- Identify recurring themes or topics
- Note areas where students might struggle (complex concepts)
- Extract common misconceptions if mentioned
- Find practical application examples

**From Existing FAQ (if present):**

- Read `docs/faq.md` if it exists
- Preserve manually curated questions
- Merge with new generated questions
- Remove duplicates, keeping manual version when conflict

### Step 3: Generate Question Categories

Create 6 standard categories aligned with learning progression:

**1. Getting Started Questions (10-15 questions)**

Target Bloom's levels: 60% Remember, 40% Understand

- Course overview and objectives
- Prerequisites and preparation
- How to use the textbook
- Navigation and structure
- Time commitment and difficulty

**2. Core Concept Questions (20-30 questions)**

Target Bloom's levels: 20% Remember, 40% Understand, 30% Apply, 10% Analyze

- Key concepts from learning graph (prioritize high-centrality nodes)
- Fundamental principles
- Concept relationships and dependencies
- How concepts build on each other

**3. Technical Detail Questions (15-25 questions)**

Target Bloom's levels: 30% Remember, 40% Understand, 20% Apply, 10% Analyze

- Terminology from glossary
- Definitions and explanations
- Technical comparisons
- Specification details

**4. Common Challenges (10-15 questions)**

Target Bloom's levels: 10% Remember, 30% Understand, 40% Apply, 20% Analyze

- Difficult concepts requiring extra explanation
- Common misconceptions
- Troubleshooting scenarios
- Error resolution

**5. Best Practice Questions (10-15 questions)**

Target Bloom's levels: 10% Understand, 40% Apply, 30% Analyze, 15% Evaluate, 5% Create

- How to apply concepts effectively
- Recommended approaches
- When to use specific techniques
- Real-world applications

**6. Advanced Topics (5-10 questions)**

Target Bloom's levels: 10% Apply, 30% Analyze, 30% Evaluate, 30% Create

- Complex integrations
- Edge cases
- Performance optimization
- Future directions

### Step 4: Generate Questions and Answers

For each category, generate questions following these guidelines:

**Question Format:**

- Use level-2 headers (##)
- Write as actual questions (end with ?)
- Make questions specific and searchable
- Use terminology from glossary
- Keep questions concise (5-15 words)

**Answer Format:**

- Use a level 3 markdown header (###) for each question
- Write complete, standalone answers
- Include examples for 40% of answers
- Link to relevant sections (target: 60%+ linked)
- Target length: 100-300 words
- Use clear, direct language
- Address the question fully

**Bloom's Taxonomy Guidelines:**

**Remember:** Recall facts, terms, basic concepts

- "What is [concept]?"
- "What does [term] mean?"
- "What are the components of [system]?"

**Understand:** Explain ideas or concepts

- "How does [concept] work?"
- "Why is [concept] important?"
- "What is the difference between [A] and [B]?"

**Apply:** Use information in new situations

- "How do I [perform task]?"
- "When should I use [technique]?"
- "What's an example of [concept] in practice?"

**Analyze:** Draw connections among ideas

- "What is the relationship between [A] and [B]?"
- "How does [concept] relate to [other concept]?"
- "What are the underlying causes of [issue]?"

**Evaluate:** Justify a decision or stance

- "Which approach is best for [scenario]?"
- "What are the trade-offs of [technique]?"
- "How do I choose between [A] and [B]?"

**Create:** Produce new or original work

- "How would I design a [system] that [requirements]?"
- "What's the best way to combine [concepts]?"
- "How can I adapt [technique] for [new context]?"

**Answer Quality Checklist:**

- [ ] Use correct markdown headers for title, categories and questions
- [ ] Directly answers the question
- [ ] Uses terminology from glossary consistently
- [ ] Includes example if concept is abstract (40% target)
- [ ] Links to relevant chapter/section (60% target)
- [ ] Appropriate length (100-300 words)
- [ ] Clear and understandable for target audience
- [ ] Accurate based on textbook content
- [ ] No jargon unless defined in glossary

### Step 5: Create FAQ File

Generate `docs/faq.md` with proper structure:

```markdown
# [Course Name] FAQ

## Getting Started Questions

### What is this course about?

[Answer with overview, linking to course description]

### Who is this course for?

[Answer describing target audience]

[Continue with 10-15 Getting Started questions...]

## Core Concepts

### What is a [Key Concept]?

[Answer with definition and example, linking to chapter]

[Continue with 20-30 Core Concepts questions...]

## Technical Detail Questions

[Continue with terminology and technical questions...]

## Common Challenge Questions

[Continue with troubleshooting questions...]

## Best Practice Questions

[Continue with application questions...]

## Advanced Topic Questions

[Continue with advanced questions...]
```

**Formatting Requirements:**

- Use level-1 header for title
- Use level-2 headers for category names
- Use level-3 headers for questions
- Use body text for answers
- Use markdown links: `[text](path.md#section)`
- Use bold for emphasis: `**important term**`
- Use code blocks for code: ` ```language ```
- Maintain consistent spacing

### Step 6: Generate Chatbot Training JSON

Create `docs/learning-graph/faq-chatbot-training.json` for RAG integration:

```json
{
  "faq_version": "1.0",
  "generated_date": "YYYY-MM-DD",
  "source_textbook": "Course Name",
  "total_questions": 87,
  "questions": [
    {
      "id": "faq-001",
      "category": "Getting Started",
      "question": "What is this course about?",
      "answer": "Full answer text here...",
      "bloom_level": "Understand",
      "difficulty": "easy",
      "concepts": ["Course Overview", "Learning Objectives"],
      "keywords": ["course", "overview", "objectives", "goals"],
      "source_links": [
        "docs/course-description.md",
        "docs/index.md"
      ],
      "has_example": false,
      "word_count": 142
    },
    {
      "id": "faq-002",
      "category": "Core Concepts",
      "question": "What is a Learning Graph?",
      "answer": "A Learning Graph is...",
      "bloom_level": "Understand",
      "difficulty": "medium",
      "concepts": ["Learning Graph", "Concept Dependency"],
      "keywords": ["learning graph", "dependencies", "prerequisites"],
      "source_links": [
        "docs/concepts/learning-graph.md",
        "docs/glossary.md#learning-graph"
      ],
      "has_example": true,
      "word_count": 218
    }
  ]
}
```

**JSON Schema Requirements:**

- Each question has unique ID (faq-001, faq-002, etc.)
- Category matches one of 6 standard categories
- Bloom level from 6-level taxonomy
- Difficulty: easy, medium, hard
- Concepts list from learning graph
- Keywords for search optimization
- Source links to original content
- Boolean flag for example presence
- Word count for answer

### Step 7: Generate Quality Report

Create `docs/learning-graph/faq-quality-report.md`:

```markdown
# FAQ Quality Report

Generated: YYYY-MM-DD

## Overall Statistics

- **Total Questions:** 87
- **Overall Quality Score:** 82/100
- **Content Completeness Score:** 78/100
- **Concept Coverage:** 73% (145/198 concepts)

## Category Breakdown

### Getting Started
- Questions: 12
- Avg Bloom's Level: Remember/Understand
- Avg Word Count: 156

[Continue for all categories...]

## Bloom's Taxonomy Distribution

Actual vs Target:

| Level | Actual | Target | Deviation |
|-------|--------|--------|-----------|
| Remember | 18% | 20% | -2% ✓ |
| Understand | 32% | 30% | +2% ✓ |
| Apply | 24% | 25% | -1% ✓ |
| Analyze | 16% | 15% | +1% ✓ |
| Evaluate | 7% | 7% | 0% ✓ |
| Create | 3% | 3% | 0% ✓ |

Overall Bloom's Score: 25/25 (excellent distribution)

## Answer Quality Analysis

- **Examples:** 38/87 (44%) - Target: 40%+ ✓
- **Links:** 54/87 (62%) - Target: 60%+ ✓
- **Avg Length:** 187 words - Target: 100-300 ✓
- **Complete Answers:** 87/87 (100%) ✓

Answer Quality Score: 24/25

## Concept Coverage

**Covered (145 concepts):** [list]

**Not Covered (53 concepts):**
- [Concept 1] - Priority: High (high centrality in learning graph)
- [Concept 2] - Priority: Medium
- [Concept 3] - Priority: Low

Coverage Score: 22/30 (73% coverage)

## Organization Quality

- Logical categorization: ✓
- Progressive difficulty: ✓
- No duplicates: ✓
- Clear questions: ✓

Organization Score: 20/20

## Overall Quality Score: 82/100

- Coverage: 22/30
- Bloom's Distribution: 25/25
- Answer Quality: 24/25
- Organization: 20/20

## Recommendations

### High Priority
1. Add questions for high-centrality concepts: [list top 10]
2. Slightly increase Remember-level questions (+2%)

### Medium Priority
1. Add examples to 3 more answers (to reach 47%)
2. Link 5 more answers to source content

### Low Priority
1. Consider adding 2-3 more Advanced Topics questions
2. Review question phrasing for searchability

## Suggested Additional Questions

Based on concept gaps, consider adding:

1. "What is [Uncovered Concept 1]?" (Core Concepts)
2. "How does [Uncovered Concept 2] work?" (Technical Details)
[Continue with top 10 suggestions...]
```

### Step 8: Generate Coverage Gaps Report

Create `docs/learning-graph/faq-coverage-gaps.md`:

```markdown
# FAQ Coverage Gaps

Concepts from learning graph not covered in FAQ.

## Critical Gaps (High Priority)

High-centrality concepts (many dependencies) without FAQ coverage:

1. **[Concept Name]**
   - Centrality: High (12 dependencies)
   - Category: Core Concepts
   - Suggested Question: "What is [Concept] and why is it important?"

[Continue for all high-priority gaps...]

## Medium Priority Gaps

Moderate-centrality concepts without FAQ coverage:

[Continue...]

## Low Priority Gaps

Leaf nodes or advanced concepts without FAQ coverage:

[Continue...]

## Recommendations

1. Add questions for all critical gaps (15 concepts)
2. Consider adding questions for medium priority (23 concepts)
3. Low priority can be addressed in future updates (15 concepts)
```

### Step 9: Validate Output Quality

Perform comprehensive validation:

**1. Uniqueness Check:**

- Scan all questions for duplicates
- Check for near-duplicates (>80% similar)
- Report any duplicates found

**2. Link Validation:**

- Extract all markdown links from answers
- Verify each link target exists
- Report broken links

**3. Bloom's Distribution:**

- Calculate actual distribution across all questions
- Compare to target distribution
- Score based on deviation (±10% acceptable)

**4. Reading Level:**

- Calculate Flesch-Kincaid grade level for answers
- Verify appropriate for target audience
- Flag answers that are too complex or too simple

**5. Answer Completeness:**

- Check each answer addresses the question
- Verify no partial or incomplete answers
- Ensure proper context provided

**6. Technical Accuracy:**

- Cross-reference terminology with glossary
- Verify consistency with chapter content
- Flag any contradictions or inaccuracies

**Success Criteria:**

- Overall quality score > 75/100
- Minimum 40 questions generated
- At least 60% concept coverage
- Balanced Bloom's Taxonomy distribution (within ±15%)
- All answers include source references
- Chatbot JSON validates against schema
- Zero duplicate questions
- All internal links valid

### Step 10: Update Navigation Section in mkdocs.yml (Optional)

If FAQ not in `mkdocs.yml`:

1. Read `mkdocs.yml`
2. Check if "FAQ: faq.md" exists in nav
3. If missing, add in appropriate location (typically near end of the nav structure)
4. Preserve existing structure

```yml
nav:
...
  - FAQ: faq.md
  - Glossary: glossary.md
  - License: license.md
  - References: references.md
  - Contact: contact.md
```

If quality reports were created in the learning-graph directory
also add these to the mkdocs.yml file in appropriate places.

```yml
nav:
  ...
  - Learning Graph:
    ...
    - FAQ Quality Report: learning-graph/faq-quality-report.md
    - FAQ Coverage Gaps: learning-graph/faq-coverage-gaps.md
```

## Quality Scoring Reference

Use this rubric to calculate overall FAQ quality score (1-100):

**Coverage (30 points):**

- 80%+ concepts: 30 points
- 70-79%: 25 points
- 60-69%: 20 points
- 50-59%: 15 points
- <50%: 10 points

**Bloom's Taxonomy Distribution (25 points):**

Calculate deviation from target for each level, sum absolute deviations:

- Total deviation 0-10%: 25 points
- Total deviation 11-20%: 20 points
- Total deviation 21-30%: 15 points
- Total deviation >30%: 10 points

**Answer Quality (25 points):**

- Examples: 40%+ = 7 pts, 30-39% = 5 pts, <30% = 3 pts
- Links: 60%+ = 7 pts, 50-59% = 5 pts, <50% = 3 pts
- Length: 100-300 words avg = 6 pts, acceptable range = 4 pts
- Completeness: 100% = 5 pts, 95-99% = 4 pts, <95% = 2 pts

**Organization (20 points):**

- Logical categorization: 5 pts
- Progressive difficulty: 5 pts
- No duplicates: 5 pts
- Clear questions: 5 pts

## Common Pitfalls to Avoid

**Duplicate Questions:**

- Don't ask the same question in different categories
- Vary phrasing for related concepts
- Merge similar questions into one comprehensive answer

**Incomplete Answers:**

- Don't leave questions partially answered
- Don't use "See chapter X for details" without summary
- Always provide standalone context

**Missing Links:**

- Don't forget to link answers to source content
- Use specific section anchors, not just page links
- Verify all links before finalizing

**Poor Question Phrasing:**

- Avoid vague questions like "How does it work?"
- Use specific terminology from glossary
- Make questions searchable

**Bloom's Imbalance:**

- Don't over-focus on Remember/Understand
- Include higher-order thinking questions
- Balance across all 6 levels

## Output Files Summary

**Required:**

1. `docs/faq.md` - Complete FAQ with categorized questions and answers

**Recommended:**

2. `docs/learning-graph/faq-quality-report.md` - Quality metrics and recommendations
3. `docs/learning-graph/faq-chatbot-training.json` - Structured data for RAG systems

**Optional:**

4. `docs/learning-graph/faq-coverage-gaps.md` - Concepts without FAQ coverage
5. Updates to `mkdocs.yml` navigation if FAQ link missing

## Example Session

**User:** "Generate an FAQ for my textbook"

**Claude (using this skill):**

1. Assesses content completeness (score: 78/100)
2. Reads course description, learning graph, glossary, chapters
3. Identifies question opportunities
4. Generates 87 questions across 6 categories
5. Creates answers with 44% examples, 62% links
6. Exports chatbot training JSON
7. Generates quality report (score: 82/100)
8. Creates coverage gaps report (53 uncovered concepts)
9. Reports: "Created FAQ with 87 questions covering 73% of concepts. Overall quality: 82/100. Added 38 examples and 54 links. See quality report for recommendations."
