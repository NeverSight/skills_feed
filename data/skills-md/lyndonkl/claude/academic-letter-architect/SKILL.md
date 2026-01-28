---
name: academic-letter-architect
description: Use when writing recommendation letters, reference letters, or award nominations for students, postdocs, or colleagues. Invoke when user mentions recommendation letter, reference, nomination, letter of support, endorsement, or needs help with strong advocacy, comparative statements, or evidence-based character assessment.
---

# Academic Letter Architect

## Table of Contents
- [Purpose](#purpose)
- [When to Use](#when-to-use)
- [Core Principles](#core-principles)
- [Workflow](#workflow)
- [Letter Structure](#letter-structure)
- [Tone and Language](#tone-and-language)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

This skill guides the creation of effective academic recommendation letters that provide evidence-based advocacy. Strong letters combine concrete examples, meaningful comparisons, and genuine enthusiasm to differentiate candidates and support their applications for positions, awards, or opportunities.

## When to Use

Use this skill when:

- **Student recommendations**: Graduate school applications, fellowship applications, job applications
- **Postdoc recommendations**: Faculty position applications, grant applications
- **Colleague recommendations**: Promotion letters, award nominations
- **Award nominations**: Prize nominations, recognition letters
- **Letters of support**: Collaboration letters, grant support letters

Trigger phrases: "recommendation letter", "reference letter", "nomination", "write a letter for", "letter of support", "endorse", "vouch for"

**Do NOT use for:**
- Personal statements (use `career-document-architect`)
- Cover letters to journals (use `scientific-email-polishing`)
- Grant proposals (use `grant-proposal-assistant`)

## Core Principles

**1. Show, don't tell**: Concrete examples beat adjectives
- ❌ "She is brilliant"
- ✅ "She independently developed a novel assay that our lab now uses routinely"

**2. Comparisons give context**: Readers need reference points
- ❌ "He is a strong student"
- ✅ "He is among the top 5% of graduate students I've mentored in 20 years"

**3. Enthusiasm is evidence**: Tone conveys conviction
- Lukewarm letters damage candidates
- Genuine enthusiasm must come through

**4. Address what matters**: Match content to opportunity
- Academic job: Research potential, teaching, mentorship
- Industry job: Practical skills, teamwork, adaptability
- Award: Specific achievements matching award criteria

## Workflow

Copy this checklist and track your progress:

```
Letter Architect Progress:
- [ ] Step 1: Gather context (candidate, opportunity, relationship)
- [ ] Step 2: Collect evidence (specific examples, achievements)
- [ ] Step 3: Draft opening (credibility, relationship, expectation)
- [ ] Step 4: Build body (evidence paragraphs, comparisons)
- [ ] Step 5: Craft closing (strong endorsement, availability)
- [ ] Step 6: Calibrate tone (enthusiasm level, superlatives)
- [ ] Step 7: Final polish (length, format, signature)
```

**Step 1: Gather Context**

Identify: Who is the candidate? What opportunity? Your relationship (advisor, collaborator, instructor)? How long have you known them? In what capacity? See [resources/methodology.md](resources/methodology.md#context-gathering) for information checklist.

**Step 2: Collect Evidence**

List 3-5 specific examples demonstrating excellence: Research achievements, intellectual contributions, professional qualities, overcoming challenges. Quantify where possible. See [resources/methodology.md](resources/methodology.md#evidence-collection) for evidence types.

**Step 3: Draft Opening**

Establish your credibility (position, experience). State relationship to candidate (role, duration, context). Set expectation (strong recommendation signal). See [resources/template.md](resources/template.md#opening-template) for opening structure.

**Step 4: Build Body**

Structure evidence into 2-4 paragraphs covering different dimensions (research, intellect, character). Include comparative statements ("top 5%", "best I've seen"). Connect evidence to opportunity requirements. See [resources/template.md](resources/template.md#body-structure) for paragraph templates.

**Step 5: Craft Closing**

Provide unambiguous endorsement statement. Offer availability for follow-up. Include professional signature with title/contact. See [resources/template.md](resources/template.md#closing-template) for closing structure.

**Step 6: Calibrate Tone**

Ensure enthusiasm matches actual assessment. Check superlative use (too many dilutes impact). Verify letter reads as advocacy, not obligation. See [resources/methodology.md](resources/methodology.md#tone-calibration) for calibration guide.

**Step 7: Final Polish**

Check length (typically 1-2 pages). Ensure formal formatting. Verify all specific claims are accurate. Validate using [resources/evaluators/rubric_academic_letter.json](resources/evaluators/rubric_academic_letter.json). **Minimum standard**: Average score ≥ 3.5.

## Letter Structure

### Opening Paragraph

**Purpose:** Establish credibility and relationship

```
Elements:
1. Your identity and position
2. How you know the candidate (role, context)
3. Duration of relationship
4. Capacity of observation (direct supervision, collaboration)
5. Clear statement of recommendation
```

**Example:**
"I am writing to provide my strongest recommendation for Dr. Jane Smith for the position of Assistant Professor. As the Director of the Structural Biology Center at X University, I have had the privilege of working closely with Jane for the past four years, first as her postdoctoral mentor and subsequently as a research collaborator. During this time, I have observed her exceptional scientific abilities, intellectual creativity, and professional maturity firsthand."

### Body Paragraphs

**Purpose:** Provide evidence-based assessment

**Paragraph 1: Research/Technical Excellence**
- Specific project achievements
- Technical skills demonstrated
- Independent thinking
- Problem-solving ability
- Publications/outputs

**Paragraph 2: Intellectual Contributions**
- Creativity and innovation
- Scientific insight
- Critical thinking
- Ability to ask important questions
- Conceptual contributions

**Paragraph 3: Professional Qualities**
- Work ethic and reliability
- Collaboration and teamwork
- Communication skills
- Mentorship of others
- Leadership potential

**Paragraph 4: Comparative Assessment**
- Direct comparison to peers
- Ranking in your experience
- Prediction of future success

### Closing Paragraph

**Purpose:** Summarize and endorse

```
Elements:
1. Overall assessment statement
2. Specific recommendation (enthusiastic, unambiguous)
3. Prediction for future success
4. Offer of availability for follow-up
5. Professional sign-off
```

**Example:**
"In summary, Jane is an outstanding scientist with exceptional research abilities, intellectual depth, and professional maturity. I give her my highest and most enthusiastic recommendation without reservation. She will make an excellent faculty member and I am confident she will develop an impactful, independent research program. Please do not hesitate to contact me if you require any additional information."

## Tone and Language

### Enthusiasm Levels

**Highest ("absolutely top"):**
- "My strongest possible recommendation"
- "Without reservation"
- "The best I have mentored in 20 years"
- "Truly exceptional"

**Strong ("top tier"):**
- "Highly recommend"
- "Outstanding"
- "Top 5-10% of students"
- "Excellent"

**Moderate ("good but not stellar"):**
- "I recommend"
- "Strong"
- "Above average"
- "Solid"

**Lukewarm (damaging):**
- "I am pleased to recommend"
- "Adequate"
- "Met expectations"
- "Did fine work"

### Comparative Statements

**Strong comparisons:**
- "Among the top 2-3 students I've trained in my career"
- "The most creative thinker I've mentored"
- "Will outperform 95% of candidates you consider"
- "Best [X] I've seen in [Y] years"

**Weak comparisons (avoid):**
- "One of our better students"
- "Above average"
- "Compares favorably to peers"

### Specificity Examples

| Vague (Weak) | Specific (Strong) |
|--------------|-------------------|
| "Productive researcher" | "Published 5 first-author papers including 2 in Nature journals" |
| "Good communicator" | "Regularly invited to present at lab meetings and gave a talk at the Gordon Conference" |
| "Works well with others" | "Mentored 3 undergraduate students, all of whom went to top graduate programs" |
| "Technically skilled" | "Independently established our lab's CRISPR screening platform" |

## Guardrails

**Critical requirements:**

1. **Truthfulness**: Only write what you genuinely believe. Dishonest letters harm candidates and your reputation.

2. **Evidence-based**: Every claim should have a supporting example. "Smart" means nothing without evidence.

3. **Appropriate comparison**: Compare to relevant reference class (other postdocs, not all scientists ever).

4. **Match content to opportunity**: Emphasize research for academic jobs, practical skills for industry.

5. **Candidate voice preservation**: Reflect the candidate's actual achievements, not fabricated ones.

6. **Cultural awareness**: US letters are more superlative than other cultures. Calibrate appropriately.

**Common pitfalls:**
- ❌ **Lukewarm language**: "Adequate", "met expectations" - these hurt
- ❌ **No comparisons**: Reader can't calibrate "excellent" without context
- ❌ **Generic adjectives**: "Brilliant, creative, hardworking" with no evidence
- ❌ **Too short**: Brief letters signal lack of enthusiasm
- ❌ **Wrong focus**: Research focus for teaching position
- ❌ **Damning with faint praise**: "Did everything asked" sounds minimal

## Quick Reference

**Key resources:**
- **[resources/methodology.md](resources/methodology.md)**: Context gathering, evidence collection, tone calibration
- **[resources/template.md](resources/template.md)**: Opening, body, closing templates
- **[resources/evaluators/rubric_academic_letter.json](resources/evaluators/rubric_academic_letter.json)**: Quality scoring

**Letter length guidelines:**
- Graduate school: 1-1.5 pages
- Faculty position: 1.5-2 pages
- Award nomination: 1-2 pages (check requirements)
- Brief reference: 0.5-1 page

**Information to gather from candidate:**
- CV/resume
- Personal statement or cover letter
- Position/opportunity description
- Specific points they'd like emphasized
- Any concerns to address proactively

**Time estimates:**
- Strong letter (well-known candidate): 1-2 hours
- Standard letter (good candidate): 30-60 minutes
- Brief reference: 15-30 minutes

**Inputs required:**
- Candidate information (CV, statement)
- Opportunity details (position, institution)
- Your relationship context (duration, capacity)
- Specific examples of excellence

**Outputs produced:**
- Complete recommendation letter
- (Optional) Commentary on strength calibration
