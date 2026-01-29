---
name: canvas-assignment-design
description: Design Canvas LMS assignments using evidence-based learning science principles from the Four Learning Design Pillars. Use when educators want to create pedagogically sound assignments, need help writing assignment descriptions with clear objectives, want rubric suggestions, or are creating quizzes/discussions/peer reviews. Integrates with canvas-mcp for direct Canvas creation.
---

# Canvas Assignment Design

Design Canvas assignments following evidence-based learning science principles.

## Skill Purpose

This skill guides educators through designing effective Canvas assignments by:
- Applying the Four Learning Design Pillars to assignment structure
- Generating assignment descriptions, rubrics, and settings
- Optionally creating assignments directly in Canvas via canvas-mcp

The skill ensures assignments are pedagogically sound, learner-centered, and aligned with established learning science research.

## Usage

```
/canvas-assignment-design
/canvas-assignment-design "peer review essay on climate change"
/canvas-assignment-design --type quiz --topic "cell biology"
```

**Arguments:**
- `[description]` - Optional brief description of the assignment you want to create
- `--type` - Assignment type: `assignment`, `quiz`, `discussion`, `peer_review`
- `--course` - Canvas course ID for direct creation
- `--no-canvas` - Design only, skip Canvas creation even if canvas-mcp is available

## Workflow

### Phase 1: Learning Objective Clarification

Ask the educator:
1. **What should students be able to do after completing this assignment?**
   - Use action verbs (analyze, create, evaluate, apply)
   - Connect to course-level learning outcomes

2. **What type of assignment best supports this objective?**
   - Standard assignment (papers, projects, submissions)
   - Quiz (knowledge checks, assessments)
   - Discussion (peer interaction, idea exchange)
   - Peer review (feedback skills, collaborative learning)

3. **What is the context?**
   - Course level (intro, intermediate, advanced)
   - Where in the course sequence (early, mid, capstone)
   - Estimated student time commitment

---

### Phase 2: Design Decisions by Pillar

Guide the educator through design choices, citing specific principles:

#### Pillar 1: Clear, Purposeful Structure

| Principle | Design Question | Canvas Implementation |
|-----------|-----------------|----------------------|
| **1.1.1 Small segments** | Can this be broken into smaller milestones or checkpoints? | Use multiple submissions or staged deadlines |
| **1.3.1 Clear objectives** | Are learning objectives stated at the top? | Add objectives in assignment description header |
| **1.3.3 Lesson alignment** | Does the assignment directly support course objectives? | Map to outcomes in Canvas |
| **1.3.4 Expectation setting** | Are success criteria crystal clear? | Attach detailed rubric; provide sample submissions |
| **1.2.2 Integrated format** | Are all resources the student needs accessible in one place? | Embed resources directly in assignment description |

**Structure Checklist:**
- [ ] Learning objectives stated clearly
- [ ] Broken into logical steps or phases
- [ ] Connected to prior modules/lessons
- [ ] Rubric attached with clear criteria

---

#### Pillar 2: Active, Engaging Learning Content

| Principle | Design Question | Canvas Implementation |
|-----------|-----------------|----------------------|
| **2.3.4 Storytelling** | Can you frame this as a scenario or case study? | Write assignment as a narrative with context |
| **2.3.7 Interest and relevance** | Is this connected to students' careers or interests? | Reference real-world applications |
| **2.2.2 Activity-based content** | Does this require active creation, not just consumption? | Focus on producing artifacts, not reading summaries |
| **3.1.5 Authentic practice** | Does this mirror real-world professional tasks? | Use industry scenarios, tools, or formats |
| **2.3.3 Activating prior knowledge** | How does this build on what students already know? | Include reflection on prior learning |

**Engagement Checklist:**
- [ ] Authentic, real-world context provided
- [ ] Active production required (not passive)
- [ ] Connected to student interests/careers
- [ ] Prior knowledge explicitly activated

---

#### Pillar 3: Continuous Practice & Feedback

| Principle | Design Question | Canvas Implementation |
|-----------|-----------------|----------------------|
| **3.1.1 Varied practice** | Does this offer a different format than prior assignments? | Vary between writing, multimedia, presentations |
| **3.1.6 Low-stakes practice** | Should this be low-stakes formative or high-stakes summative? | Practice quizzes with unlimited attempts vs. graded |
| **3.2.1 Targeted feedback** | What specific feedback will students receive? | Rubric with actionable criteria |
| **3.2.4 Worked examples** | Have you provided models or exemplars? | Link to sample submissions in description |
| **3.2.5 Clear instructions** | Are instructions unambiguous? | Step-by-step numbered instructions |
| **3.3.2 Generating explanations** | Does this prompt higher-order thinking? | Include reflection/explanation prompts |

**Feedback Checklist:**
- [ ] Rubric with specific, actionable criteria
- [ ] Sample/exemplar submission provided
- [ ] Clear instructions (numbered steps)
- [ ] Reflection or explanation component included

---

#### Pillar 4: Simple, Intuitive User Experience

| Principle | Design Question | Canvas Implementation |
|-----------|-----------------|----------------------|
| **4.3.2 Time estimates** | How long should this take students? | State estimated time in description |
| **4.2.3 Viewability** | Will this work on mobile? | Test embedded content responsiveness |
| **4.2.5 Minimalist design** | Is the description clear and uncluttered? | Use headers, bullets, white space |
| **4.1.3 Interactive clarity** | Are clickable elements obvious? | Clear button labels for submissions |

**UX Checklist:**
- [ ] Time estimate provided
- [ ] Scannable format (headers, bullets)
- [ ] Mobile-friendly resources
- [ ] No unnecessary complexity

---

### Phase 3: Generate Assignment Components

Based on the design decisions, generate:

#### 1. Assignment Description Template

```markdown
## Learning Objectives
By completing this assignment, you will be able to:
- [Objective 1 - action verb]
- [Objective 2 - action verb]

## Overview
[Brief engaging context - use storytelling/scenario framing]

**Estimated Time:** [X hours]

## Instructions
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Resources
- [Embedded resource 1]
- [Embedded resource 2]

## Submission Requirements
- [Format requirements]
- [File types accepted]
- [Length/scope expectations]

## Evaluation Criteria
See attached rubric. Key areas:
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

## Sample Submission
[Link to exemplar or description of what success looks like]
```

#### 2. Rubric Criteria

Generate rubric criteria aligned with learning objectives:

| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|-----------|---------------|----------------|----------------|---------------|
| [Objective 1] | [Description] | [Description] | [Description] | [Description] |
| [Objective 2] | [Description] | [Description] | [Description] | [Description] |
| [Objective 3] | [Description] | [Description] | [Description] | [Description] |

#### 3. Canvas Settings Recommendations

- **Submission Type:** [Online/File upload/Media/etc.]
- **Allowed Attempts:** [1/Multiple/Unlimited]
- **Due Date Strategy:** [Single date vs. milestone dates]
- **Peer Review:** [Enabled/Disabled, anonymous or not]
- **Turnitin:** [If applicable]
- **Points:** [Suggested point value]
- **Assignment Group:** [Suggested category]

---

### Phase 4: Canvas Creation (Optional)

If canvas-mcp is available and the educator confirms, create the assignment:

1. Confirm course ID and assignment group
2. Create assignment with generated description
3. Create and attach rubric
4. Set submission type and other settings
5. Return assignment URL

---

## Canvas MCP Integration

This skill integrates with [canvas-mcp](https://github.com/vishalsachdev/canvas-mcp) for direct Canvas LMS operations.

### Required Tools

| Tool | Purpose |
|------|---------|
| `list_courses` | Find target course ID |
| `list_assignments` | Review existing assignments for consistency |
| `create_assignment` | Create the new assignment |
| `update_assignment` | Modify existing assignments |
| `list_rubrics` | Check existing rubrics |
| `create_rubric` | Create aligned rubric |

### Integration Flow

```
1. Check canvas-mcp availability
   |
2. If available:
   +-- list_courses -> let educator select course
   +-- list_assignments -> review existing for consistency
   +-- create_assignment -> with generated content
   +-- create_rubric -> attach to assignment
   +-- Return assignment URL
   |
3. If not available:
   +-- Output assignment design for manual creation
   +-- Include copy-paste ready content
```

### Example canvas-mcp Tool Usage

```javascript
// Create assignment
create_assignment({
  course_id: "12345",
  name: "Climate Change Policy Analysis",
  description: "[Generated description with learning objectives, instructions, etc.]",
  submission_types: ["online_upload"],
  allowed_extensions: ["pdf", "docx"],
  points_possible: 100,
  due_at: "2024-02-15T23:59:00Z",
  published: false  // Draft first for review
})

// Create rubric
create_rubric({
  course_id: "12345",
  assignment_id: "67890",
  title: "Climate Change Policy Analysis Rubric",
  criteria: [
    {
      description: "Analysis Depth",
      points: 25,
      ratings: [
        { description: "Excellent", points: 25 },
        { description: "Proficient", points: 20 },
        { description: "Developing", points: 15 },
        { description: "Beginning", points: 10 }
      ]
    }
    // ... additional criteria
  ]
})
```

---

## Examples: Principles in Action

### Example 1: Research Paper Assignment

**Traditional approach:**
> "Write a 5-page research paper on a topic of your choice related to environmental science. Due in 3 weeks."

**Pillar-informed approach:**

> ## Learning Objectives
> By completing this assignment, you will be able to:
> - Evaluate scientific sources for credibility and relevance (aligns with course outcome 3)
> - Synthesize multiple perspectives on an environmental issue
> - Construct an evidence-based argument using APA format
>
> ## The Challenge
> You are a policy advisor for a city council considering new environmental regulations. The council has asked you to analyze ONE of the following issues and provide a research-backed recommendation:
> - Urban heat island mitigation strategies
> - Single-use plastic ban effectiveness
> - Electric vehicle adoption incentives
>
> **Estimated Time:** 8-10 hours over 3 weeks
>
> ## Milestones
> 1. **Week 1:** Topic selection + 3 source annotations (15 pts)
> 2. **Week 2:** Outline + thesis statement (15 pts)
> 3. **Week 3:** Final paper (70 pts)
>
> ## Resources
> - [Video: Evaluating Scientific Sources (8 min)]
> - [Sample policy brief from previous semester]
> - [APA formatting guide]

**Principles applied:**
- **1.1.1 Small segments:** Broken into 3 milestones
- **2.3.4 Storytelling:** Framed as policy advisor scenario
- **3.1.5 Authentic practice:** Real-world policy context
- **3.2.4 Worked examples:** Sample provided
- **4.3.2 Time estimates:** 8-10 hours stated

---

### Example 2: Quiz Design

**Traditional approach:**
> "Chapter 5 Quiz - 20 multiple choice questions, 1 attempt, 30 minutes"

**Pillar-informed approach:**

> ## Cell Biology Checkpoint
>
> **Purpose:** This practice quiz helps you identify which concepts from Chapter 5 you've mastered and which need more review before the unit exam.
>
> **Estimated Time:** 15-20 minutes
>
> ## Format
> - 15 questions mixing recall and application
> - **Unlimited attempts** - your highest score counts
> - Immediate feedback with explanations after each attempt
>
> ## Question Types
> - Recall: Identify organelle functions
> - Application: Predict what happens when cellular processes are disrupted
> - Analysis: Compare/contrast cell types
>
> ## After the Quiz
> Review any questions you missed. The linked resources will help:
> - [Organelle Functions Review Video (6 min)]
> - [Interactive Cell Diagram]

**Principles applied:**
- **3.1.6 Low-stakes practice:** Unlimited attempts
- **3.2.3 Immediate feedback:** Explanations after each attempt
- **3.1.1 Varied practice:** Mixed question types
- **2.3.2 Explaining features:** Purpose explained
- **4.3.2 Time estimates:** 15-20 minutes stated

---

### Example 3: Discussion Forum

**Traditional approach:**
> "Discuss chapter 3. Respond to at least 2 classmates."

**Pillar-informed approach:**

> ## Ethical Dilemmas in AI Development
>
> ## Learning Objective
> Apply ethical frameworks from Unit 2 to analyze real-world AI decisions.
>
> ## The Scenario
> Read this article: [Hiring Algorithm Bias Case Study]
>
> A company's AI hiring tool was found to disadvantage female candidates. You've been asked to advise the company's ethics board.
>
> ## Your Initial Post (by Wednesday)
> In 200-300 words:
> 1. Which ethical framework from our readings best applies here? Why?
> 2. What would this framework recommend the company do?
> 3. What are the limitations of applying this framework?
>
> **Estimated Time:** 30-45 minutes
>
> ## Peer Engagement (by Friday)
> Respond to TWO classmates whose posts used a DIFFERENT framework than yours:
> - What new perspective did their framework reveal?
> - Where do the frameworks conflict, and how might you resolve that?
>
> **Estimated Time:** 20-30 minutes
>
> ## Evaluation
> See rubric. Key criteria:
> - Accurate application of ethical framework
> - Quality of analysis (not just description)
> - Substantive peer engagement (not "I agree, great point!")

**Principles applied:**
- **2.3.4 Storytelling:** Real case scenario
- **3.3.2 Generating explanations:** "Why" and analysis required
- **3.3.4 Social learning:** Structured peer interaction
- **1.3.1 Clear objectives:** Stated at top
- **3.2.5 Clear instructions:** Specific word counts, deadlines

---

## Quick Reference: Pillar Checklist

Use this checklist during assignment design:

### Pillar 1: Structure
- [ ] Learning objectives stated explicitly
- [ ] Segmented into manageable parts
- [ ] Aligned with course outcomes
- [ ] Clear expectations and rubric

### Pillar 2: Engagement
- [ ] Authentic real-world context
- [ ] Active production (not passive)
- [ ] Prior knowledge activated
- [ ] Relevant to student interests

### Pillar 3: Practice & Feedback
- [ ] Varied from other assignments
- [ ] Appropriate stakes (formative/summative)
- [ ] Detailed rubric with actionable feedback
- [ ] Exemplars or worked examples provided

### Pillar 4: User Experience
- [ ] Time estimate included
- [ ] Scannable format (headers, bullets)
- [ ] All resources accessible in one place
- [ ] Mobile-friendly

---

## Related Skills

- `/learning-design-review` - Review existing content against all pillars
- `/canvas-course-audit` - Audit an entire course
- `/canvas-feedback-template` - Generate feedback templates

## References

Principles from `{SKILL_DIR}/../principles/learning-design-pillars.yaml`, synthesizing:
- Mayer, R. E. (2022). Multimedia Learning
- Cognitive Load Theory research
- Evidence-based instructional design practices

See the YAML file for complete citations and research basis for each principle.
