---
name: reference-generator
description: This skill generates curated, verified reference lists for textbooks with level-appropriate resources (10 for junior-high, 20 for senior-high, 30 for college, 40 for graduate). References are formatted with links, publication details, and relevance descriptions. Use this skill when working with intelligent textbooks that need academic references, either book-level or chapter-level.
---

# Reference Generator

## Overview

Generate high-quality, verified reference lists for educational textbooks with level-appropriate content and quantity. The skill analyzes course descriptions to determine the target audience and creates references that match the readers' level, from fun and engaging resources for junior-high students to authoritative peer-reviewed papers for graduate students.

## When to Use This Skill

Use this skill when:

- Creating a new intelligent textbook that needs a comprehensive reference list
- Adding references to an existing textbook
- Updating or expanding references for educational content
- A user explicitly requests reference generation

## Reference Generation Workflow

### Step 1: Analyze the Course Description

Read the `/docs/course-description.md` file to determine:

- **Grade level** or target audience (junior-high, senior-high, college, graduate)
- **Prerequisites** - indicates reader sophistication
- **Subject matter** - determines reference topics
- **Learning objectives** - guides reference selection

The grade level determines:

- **Junior-high (middle school)**: 10 references - fun, engaging, visual resources
- **Senior-high (high school)**: 20 references - mix of accessible and academic sources
- **College (undergraduate)**: 30 references - more academic, some peer-reviewed papers
- **Professional Development**: 30 references - more academic, some peer-reviewed papers
- **Graduate (masters/PhD)**: 40 references - heavily peer-reviewed, authoritative sources

### Step 2: Check for Chapter-Level Content

Before generating references, search for chapter content in the textbook:

```bash
# Look for the chapters directory
find /docs/chapters
# Look for chapter files
find /docs -name "chapter*.md" -o -name "*-chapter-*.md"
```

If chapter content exists, use the AskUserQuestion tool to ask:
- "Would you like book-level references (in /docs/references.md) or chapter-level references (at the end of each chapter)?"

### Step 3: Generate References with Verification

For each reference, perform the following:

1. **Search for authoritative sources** using WebSearch tool
2. **Verify each URL** using WebFetch to ensure the link is valid and accessible
3. **Format according to the standard template** (see Format Specification below)

**Quality Guidelines by Level:**

**Junior-High (10 references):**
- Educational websites with interactive content
- Videos from reputable educational channels
- Visual resources, infographics, and animations
- Age-appropriate articles from educational publishers
- Museums, science centers, and educational organizations

**Senior-High (20 references):**
- Mix of educational websites and academic sources
- Reputable news organizations and science journalism
- Educational videos and documentaries
- Introduction to academic journals (more accessible papers)
- Government and NGO educational resources

**College (30 references):**
- Peer-reviewed journal articles (50%+ of references)
- Academic textbooks and monographs
- University course materials and lectures
- Research institution publications
- Industry white papers and technical reports

**Graduate (40 references):**
- Heavily weighted toward peer-reviewed journals (70%+ of references)
- Seminal papers in the field
- Recent research (last 5 years) showing current state of field
- Meta-analyses and systematic reviews
- Academic books from university presses

### Step 4: Format Each Reference

Use the following format for every reference:

```markdown
1. [Link Title](URL) - YYYY-MM-DD - Publication Name - Brief description of resource and specific relevance to the textbook topic.
```

**Format Specifications:**
- **Link Title**: Exact title of the article, paper, video, or resource
- **URL**: Verified, working link (use WebFetch to confirm)
- **Date**: Publication date in YYYY-MM-DD format (use YYYY-MM or YYYY if day/month unavailable)
- **Publication Name**: Journal, website, organization, or publisher
- **Description**: 1-2 sentences explaining what the resource covers and why it's relevant to this specific textbook

**Example References:**

```markdown
1. [How Neural Networks Really Work](https://distill.pub/2020/circuits/zoom-in/) - 2020-03-10 - Distill - Interactive visualization explaining the inner workings of neural networks through explorable explanations, perfect for visual learners beginning their ML journey.

2. [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - 2017-06-12 - arXiv - Seminal paper introducing the Transformer architecture that revolutionized natural language processing and forms the foundation for modern LLMs like GPT and BERT.

3. [Khan Academy: Introduction to Algorithms](https://www.khanacademy.org/computing/computer-science/algorithms) - 2024-01-15 - Khan Academy - Free, interactive course covering fundamental algorithms including sorting and searching, with visualizations and practice exercises suitable for high school students.
```

### Step 5: Write References to File

**For book-level references:**
Create or overwrite `/docs/references.md` with:

```markdown
# References

This textbook draws upon the following high-quality resources:

[Generated numbered list of references]

---
*References last updated: [Current Date]*
```

**For chapter-level references:**
Append to each chapter file (e.g., `/docs/chapters/01-introduction/index.md`):

```markdown

## References

[Generated numbered list of references for this chapter]
```

### Step 6: Validation and Reporting

After generating references:

1. **Count the references** to ensure correct quantity for level
2. **Verify all URLs** were checked with WebFetch
3. **Report summary** to user:
   - Number of references generated
   - Target level identified
   - File location
   - Any URLs that failed verification (if any)

## URL Verification Process

**Critical**: Every URL must be verified before inclusion.

```python
# Use WebFetch for each URL
WebFetch(url=reference_url, prompt="Is this page accessible? Provide the title and a brief description of the content.")
```

If a URL returns an error or redirect:
- Try to find an updated or archived version
- Use Internet Archive / Wayback Machine if appropriate
- Skip the reference if no valid URL exists
- Note in the report any references that couldn't be verified
- For academic papers, the full document might be behind a paywall.  Just reference the citation for these resources.  Prefer references on reputable sites like Google Scholar.
- For academic textbooks, prefer references that have many citations.

## Reference Quality Checklist

Before finalizing references, ensure:
- [ ] Correct quantity for target level (10/20/30/40)
- [ ] All URLs verified and accessible
- [ ] Publication dates included
- [ ] Mix of resource types (articles, videos, papers)
- [ ] Descriptions explain relevance to textbook
- [ ] Academic rigor matches target audience
- [ ] No duplicate sources
- [ ] Proper formatting throughout

## Example Usage Scenarios

**Scenario 1: New textbook**

```
User: "Generate references for my textbook"
→ Read /docs/course-description.md
→ Identify level (e.g., college)
→ Check for chapters (none found)
→ Generate 30 verified references
→ Write to /docs/references.md
```

**Scenario 2: Existing textbook with chapters**

```
User: "Add references to my course"
→ Read /docs/course-description.md
→ Find chapter files exist
→ Ask: "Book-level or chapter-level references?"
→ User selects chapter-level
→ Generate references for each chapter
→ Append to each chapter file
```

## Finish

- Report the number of references generated and indicate the number of working links
- Tell the user that for academic papers, a citation graph skill can be used create a list of the most highly sited papers that influence this topic

## Resources

This skill uses web-based verification tools built into Claude Code:
- **WebSearch**: Find authoritative sources on topics
- **WebFetch**: Verify URLs are accessible and extract metadata
- **AskUserQuestion**: Clarify book-level vs chapter-level preference

No additional scripts, references, or assets are required for this skill.
