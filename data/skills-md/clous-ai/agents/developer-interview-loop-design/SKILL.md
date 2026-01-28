---
name: developer-interview-loop-design
description: This skill should be used when the user asks to "design an interview loop", "create interview process", "build interview rubric", "structure interviews by competency", "define interview stages", or "plan technical interviews". Designs structured, competency-based interview loops that assess technical, leadership, and collaboration skills while ensuring legal compliance and candidate experience.
version: 0.1.0
license: MIT
---

# Developer Interview Loop Design

Design structured, fair, and effective interview loops that assess engineering candidates across technical, leadership, and collaboration competencies.

## Purpose

Create interview loops that:
- Assess all competencies from role scorecard
- Minimize bias through structured questions
- Provide excellent candidate experience
- Enable data-driven hiring decisions
- Comply with employment law

## When to Use

Invoke when:
- Creating new interview process for role
- Redesigning existing interview loop
- Standardizing interviews across team
- Training new interviewers
- Ensuring legal compliance in assessments

## Core Process

### 1. Map Competencies to Interview Stages

Based on role scorecard, design loop structure:

**Standard Engineering Loop:**

| Stage | Duration | Competency | Interviewer(s) | Format |
|-------|----------|------------|----------------|--------|
| Recruiter Screen | 30 min | Basic fit, communication | Recruiter | Phone/Video |
| Technical Screen | 60 min | Technical (coding) | Engineer | Live coding |
| Coding Interview | 90 min | Technical (algorithms, problem-solving) | 2 Engineers | Whiteboard/CoderPad |
| System Design | 60 min | Technical (architecture) | Senior+ Engineer | Whiteboard |
| Behavioral | 45 min | Leadership, Collaboration | Hiring Manager | Structured Q&A |
| Team Fit | 45 min | Collaboration, Culture | Team member | Conversational |

**Total Time:** 5-6 hours

**Competency Coverage:**
- Technical: 70% (Screen + Coding + Design)
- Leadership: 15% (Behavioral)
- Collaboration: 15% (Behavioral + Team Fit)

### 2. Create Interview Rubrics

For each interview stage, define:

**Rubric Structure:**
```json
{
  "interview_stage": "System Design Interview",
  "duration_minutes": 60,
  "competencies_assessed": ["Technical Architecture", "Communication"],
  "evaluation_criteria": [
    {
      "criterion": "Problem decomposition",
      "weight": 0.3,
      "scoring": {
        "5": "Breaks down complex system into clear components with trade-offs",
        "3": "Identifies major components, some gaps in analysis",
        "1": "Struggles to decompose problem"
      }
    },
    {
      "criterion": "Scale considerations",
      "weight": 0.25,
      "scoring": {
        "5": "Proactively discusses scaling, bottlenecks, data volumes",
        "3": "Addresses scale when prompted",
        "1": "Does not consider scale"
      }
    },
    {
      "criterion": "Communication clarity",
      "weight": 0.2,
      "scoring": {
        "5": "Clearly explains thinking, uses diagrams effectively",
        "3": "Communicates adequately with some prompting",
        "1": "Difficult to follow reasoning"
      }
    },
    {
      "criterion": "Technical depth",
      "weight": 0.25,
      "scoring": {
        "5": "Deep understanding of databases, caching, queuing, etc.",
        "3": "Solid fundamentals, some depth",
        "1": "Surface-level understanding"
      }
    }
  ],
  "pass_threshold": 3.0,
  "strong_hire_threshold": 4.0
}
```

**Scoring Scale (1-5):**
- 5: Exceptional - exceeds expectations for level
- 4: Strong - clearly meets expectations
- 3: Adequate - meets minimum bar
- 2: Weak - concerns about fit
- 1: Poor - does not meet bar

### 3. Develop Structured Questions

Create question banks with consistent rubrics:

**Behavioral Interview Questions (STAR Method):**

Must assess: Leadership, Collaboration

**Leadership Questions:**
- "Tell me about a time you mentored a junior engineer. What was your approach?"
- "Describe a situation where you had to influence a technical decision you weren't directly responsible for."
- "Give an example of when you improved a team process or practice."

**Collaboration Questions:**
- "Describe a time you disagreed with a teammate on a technical approach. How did you resolve it?"
- "Tell me about working with a difficult stakeholder. How did you manage the relationship?"
- "Give an example of when you had to explain a complex technical concept to a non-technical audience."

**STAR Evaluation:**
- Situation: Context clearly described?
- Task: Responsibility/goal clear?
- Action: Specific actions taken?
- Result: Measurable outcome?

**Technical Questions (Coding):**

Create bank organized by difficulty:

```markdown
## Easy (Warm-up, Junior level)
- Two Sum
- Valid Palindrome
- Reverse String

## Medium (Core assessment, Mid-Senior)
- Longest Substring Without Repeating Characters
- Merge Intervals
- LRU Cache

## Hard (Senior+ differentiation)
- Serialize/Deserialize Binary Tree
- Word Ladder
- Design In-Memory File System
```

**Anti-Pattern:** Don't just test algorithm memorization. Assess:
- Problem-solving approach
- Code quality and organization
- Testing and edge cases
- Communication while coding

### 4. Train Interviewers

Ensure consistent, fair interviews:

**Interviewer Calibration:**
- Shadow 3-5 interviews before conducting independently
- Compare scores with experienced interviewers
- Attend calibration sessions quarterly
- Review unconscious bias training

**Interview Guidelines:**
- Use structured questions from question bank
- Take detailed notes during interview
- Score immediately after interview
- Don't be influenced by other interviewers' feedback until debrief

**Red Flags to Avoid:**
- Asking questions about protected characteristics
- Making hiring decisions based on "gut feeling"
- Asking different questions to different candidates
- Failing to document decision rationale

### 5. Plan Logistics

**Scheduling:**
- Book interview rooms/video links in advance
- Send calendar invites with prep materials
- Include 15-min buffer between interviews
- Provide candidate with schedule and interviewer info

**Candidate Experience:**
- Send confirmation email with loop details
- Provide parking/office directions
- Assign "candidate host" for day-of coordination
- Offer water, snacks, breaks
- Set expectations: duration, format, what to prepare

**Interviewer Preparation:**
- Share candidate resume 24hrs before interview
- Provide interview rubric and questions
- Clarify which competency to assess
- Set expectation to submit feedback within 24hrs

### 6. Conduct Debrief

**Debrief Structure:**
- Each interviewer presents score + rationale (2-3 min)
- Discuss discrepancies (if 2+ point difference)
- Hiring manager summarizes consensus
- Make decision: Strong Hire / Hire / No Hire / Strong No Hire

**Decision Framework:**
- Strong Hire: All interviews ≥ 4.0, move to offer immediately
- Hire: Average ≥ 3.5, no red flags
- No Hire: Average < 3.0 or any critical red flag
- Strong No Hire: Multiple poor interviews, clear misfit

**Anti-Bias Techniques:**
- Hiring manager speaks last (avoid anchoring)
- Focus on evidence, not impressions
- Reference specific rubric criteria
- Challenge "culture fit" concerns for specificity

### 7. Generate Loop Documentation

Output comprehensive interview guide:

```json
{
  "role": "Senior Backend Engineer",
  "loop_structure": [
    {
      "stage": "Recruiter Screen",
      "duration_minutes": 30,
      "interviewer_type": "Recruiter",
      "competencies": ["Basic qualification", "Communication"],
      "key_questions": ["Why interested in role?", "Salary expectations?"],
      "pass_criteria": "Meets must-haves, good communication"
    },
    {
      "stage": "Technical Screen",
      "duration_minutes": 60,
      "interviewer_type": "Engineer (any level)",
      "competencies": ["Coding fundamentals"],
      "problem": "Medium difficulty coding problem",
      "pass_criteria": "Solves problem with hints, clean code"
    }
  ],
  "rubrics": {
    "coding_interview": { /* detailed rubric */ },
    "system_design": { /* detailed rubric */ },
    "behavioral": { /* detailed rubric */ }
  },
  "interviewer_training": {
    "required_shadowing": 3,
    "calibration_frequency": "quarterly",
    "bias_training_required": true
  },
  "decision_criteria": {
    "strong_hire_threshold": 4.0,
    "hire_threshold": 3.5,
    "must_pass_all_competencies": true
  }
}
```

Save to `interview-loop-{role}-{date}.json`.

## Using Supporting Resources

### Templates
- **`templates/interview-rubric.json`** - Rubric schema with scoring
- **`templates/question-bank.md`** - STAR behavioral questions by competency
- **`templates/coding-problems.md`** - Technical problems by difficulty

### References
- **`references/legal-interview-questions.md`** - Permissible vs prohibited questions
- **`references/anti-bias-techniques.md`** - Structured interview best practices
- **`references/candidate-experience.md`** - Logistics, communication, follow-up

### Scripts
- **`scripts/validate-loop.py`** - Check competency coverage, time allocation
- **`scripts/generate-scorecard.py`** - Create interviewer scorecards

## Example Workflow

User: "Design interview loop for senior backend engineer position"

Steps:
1. Load role scorecard (technical 70%, leadership 20%, collaboration 10%)
2. Design 6-stage loop: Screen, Coding, System Design, Behavioral, Team Fit, Hiring Manager
3. Create rubrics for each stage with 3-5 criteria
4. Build question banks (STAR behavioral, coding problems by difficulty)
5. Define pass thresholds (3.5 average, all competencies ≥ 3.0)
6. Plan logistics (5-6 hour loop, virtual or onsite)
7. Generate loop documentation + interviewer training guide
8. Validate with loop validator script

Output: Complete interview loop ready for execution

## Legal Compliance

**Prohibited Questions:**
- Age, birthdate, graduation year
- Marital status, children, pregnancy
- Disability, health conditions
- Religion, national origin, race
- Arrest record (in most states)

**Best Practices:**
- Ask same questions to all candidates
- Focus on job-related scenarios
- Document scoring immediately
- Train interviewers on bias

See `references/legal-interview-questions.md` for detailed guidance.

---

**Progressive Disclosure:** Detailed question banks, anti-bias techniques, and legal compliance are in references/. Core loop design framework above covers standard engineering roles.
