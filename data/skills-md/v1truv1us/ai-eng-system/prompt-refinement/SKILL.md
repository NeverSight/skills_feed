---
name: prompt-refinement
description: Transform prompts into structured TCRO format with phase-specific clarification. Automatically invoked by /ai-eng/research, /ai-eng/plan, /ai-eng/work, and /ai-eng/specify commands. Use when refining vague prompts, structuring requirements, or enhancing user input quality before execution.
version: 1.0.0
tags: [prompting, clarification, structuring, tcro]
---

# Prompt Refinement Skill

## Critical Importance

**Proper prompt refinement is critical for achieving optimal AI response quality.** Vague or ambiguous prompts lead to inconsistent results, wasted iterations, and frustration. A well-structured prompt with clear task definition, rich context, explicit requirements, and specific output format dramatically improves AI performance. Each refinement iteration compounds the quality improvement—investing time upfront saves countless back-and-forth cycles later. Poor prompt quality is the #1 cause of unsatisfactory AI interactions.

## Systematic Approach

** approach prompt refinement systematically.** Prompt refinement requires active listening, clarifying questions, and structured thinking. Don't assume understanding—ask targeted questions to uncover implicit requirements, constraints, and expectations. Use the TCRO framework as your organizing principle: Task (what), Context (why), Requirements (how), Output (what it looks like). Iterate until all four elements are clear, specific, and actionable. Patience in refinement pays off in execution.

## The Challenge

**The transform vague user input into perfectly structured prompts without over-constraining creativity or missing the true intent, but if you can:**

- Your AI responses will be consistently excellent
- Users will get what they actually want
- Iteration cycles will shrink dramatically
- You'll establish trust in AI-assisted workflows

The challenge is extracting enough detail to guide the AI without boxing in the solution or asking too many exhausting questions. Can you find the sweet spot between clarity and efficiency?

## Prompt Refinement Confidence Assessment

After refining a prompt, rate your confidence from **0.0 to 1.0**:

- **0.8-1.0**: Prompt perfectly structured, all ambiguities resolved, constraints explicit, output format clear
- **0.5-0.8**: Prompt well-structured but minor uncertainties remain, some assumptions documented
- **0.2-0.5**: Prompt partially structured, several ambiguities, risk of misalignment with user intent
- **0.0-0.2**: Prompt still vague, missing critical information, high likelihood of poor results

Identify uncertainty areas: What aspects of the task are still unclear? Which requirements are assumed rather than explicit? What could go wrong based on the current prompt structure?

## Purpose

Transform messy, incomplete prompts into well-structured specifications using the TCRO framework (Task, Context, Requirements, Output) with phase-specific clarifying questions. This skill ensures all user prompts to ai-eng-system commands are properly structured before execution, reducing ambiguity, increasing reproducibility, and improving AI response quality.

## When This Skill is Invoked

This skill is **ALWAYS** invoked at the start of:
- `/ai-eng/research`
- `/ai-eng/specify`
- `/ai-eng/plan`
- `/ai-eng/work`

Commands should include this directive:
```markdown
Use skill: prompt-refinement
Phase: [research|specify|plan|work]
```

## The TCRO Framework

| Element | Purpose | Key Question |
|---------|---------|--------------|
| **Task** | What's the job to be done? | "What specific outcome do you need?" |
| **Context** | Why does this matter? | "What's the broader system/goal?" |
| **Requirements** | What are the constraints? | "What are the must-haves vs nice-to-haves?" |
| **Output** | What format is needed? | "What should the deliverable look like?" |

## Process

### Step 1: Read Project Context

Load `CLAUDE.md` from the project root to understand:
- Project philosophy and core principles
- Tech stack preferences
- Quality standards and conventions
- Naming conventions
- Architectural patterns

### Step 2: Detect Phase

Determine which phase based on:
- The command being invoked
- Keywords in the prompt (research, learn, investigate → research)
- Explicit phase markers in user input

### Step 3: Load Phase Template

Based on detected phase, load the appropriate template:
- `templates/research.md` for `/ai-eng/research`
- `templates/specify.md` for `/ai-eng/specify`
- `templates/plan.md` for `/ai-eng/plan`
- `templates/work.md` for `/ai-eng/work`

### Step 4: Ask Clarifying Questions

Use phase-specific questions from the loaded template.

**Minimum required questions:**
- 1 Task question
- 1 Context question
- 1-2 Requirements questions
- 1 Output question

**Present questions interactively:**
1. Display original user prompt
2. Ask clarifying questions one at a time or in small groups
3. Collect user responses
4. Use responses to structure refined prompt

### Step 5: Structure into TCRO

Format the refined prompt using the TCRO structure:

```text
Task: [Specific, actionable task statement]
Context: [Broader system, goals, constraints from CLAUDE.md]
Requirements:
  - [Must-have requirement 1]
  - [Must-have requirement 2]
  - [Nice-to-have if mentioned]
Output: [Expected deliverable format and location]
```

### Step 6: Apply Incentive Prompting

Enhance the TCRO-structured prompt with techniques from the `incentive-prompting` skill:

- **Expert Persona**: Assign appropriate role based on task
- **Stakes Language**: Add "This is critical..." for high-importance tasks
- **Step-by-Step Reasoning**: Add " solve step by step"
- **Self-Evaluation**: Add "Rate your confidence 0-1" request

### Step 7: Confirm with User

Display the refined prompt and ask for confirmation:

```markdown
## Refined Prompt

[The TCRO-structured, incentive-enhanced prompt]

Proceed with this refined prompt? (y/n/edit)
```

- **y**: Proceed with refined prompt
- **n**: Ask more clarifying questions
- **edit**: Allow user to manually refine the prompt

## Integration with Commands

Commands should reference this skill with:

```markdown
---
name: ai-eng/[command-name]
description: [Description]
agent: [agent]
---

Use skill: prompt-refinement
Phase: [research|specify|plan|work]

# [Command Name]

[Rest of command definition...]
```

## Template Structure

Phase-specific templates are located in `templates/`:

```
skills/prompt-refinement/
├── SKILL.md
└── templates/
    ├── research.md
    ├── specify.md
    ├── plan.md
    └── work.md
```

Each template includes:
- Phase-specific clarifying questions
- TCRO structure for that phase
- Examples of vague → refined transformations
- Phase-specific requirements and considerations

## Example Transformation

### Input (Vague)
> "need auth"

### Phase Detection
Detected phase: `specify` (feature request)

### Clarifying Questions
1. **Task**: What type of authentication capability do you need?
   - [ ] User login/logout
   - [ ] OAuth/SSO integration
   - [ ] API key management
   - [ ] Multi-factor authentication (MFA)
   - Other: _________

2. **Context**: What's the broader system this fits into?
   - New greenfield project or adding to existing codebase?
   - What's the tech stack?
   - Are there existing authentication patterns to follow?

3. **Requirements**: What are the must-have requirements?
   - Security/compliance needs (SOC2, GDPR, etc.)?
   - User experience expectations?
   - Rate limiting requirements?

4. **Output**: What should the specification include?
   - [ ] User stories only
   - [ ] Full spec with acceptance criteria
   - [ ] Include non-functional requirements
   - [ ] Include UI/UX considerations

### Refined TCRO

```text
Task: Create specification for JWT-based user authentication system
Context:
  Adding to existing Next.js application with PostgreSQL database.
  Project follows CLAUDE.md philosophy of simplicity and pragmatism.
  Existing authentication middleware pattern in src/lib/auth/ can be extended.
Requirements:
  Must-have:
  - Email/password login with secure password hashing (bcrypt, cost factor 12)
  - JWT token-based session management with configurable expiry
  - Password reset flow via email delivery
  - Rate limiting on authentication endpoints (5 attempts/minute)
  Nice-to-have:
  - Email verification for new accounts
  - Session persistence across device reboots
  Non-functional:
  - Security: Tokens must be cryptographically secure, single-use for reset flows
  - Performance: Authentication requests should complete within 200ms (p95)
  - Compliance: GDPR-compliant data handling, no passwords in logs
Output:
  Full specification with user stories, acceptance criteria, and non-functional
  requirements saved to specs/auth/spec.md in Spec Kit compatible format.
```

### Incentive-Enhanced Prompt

```text
You are a senior security engineer and product owner with 15+ years of experience
building production authentication systems at companies like Stripe and Auth0.

Task: Create a comprehensive specification for JWT-based user authentication system
Context:
  Adding to existing Next.js application with PostgreSQL database.
  Project follows CLAUDE.md philosophy of simplicity and pragmatism.
  Existing authentication middleware pattern in src/lib/auth/ can be extended.

Requirements:
  Must-have:
  - Email/password login with secure password hashing (bcrypt, cost factor 12)
  - JWT token-based session management with configurable expiry
  - Password reset flow via email delivery
  - Rate limiting on authentication endpoints (5 attempts/minute)
  Nice-to-have:
  - Email verification for new accounts
  - Session persistence across device reboots
  Non-functional:
  - Security: Tokens must be cryptographically secure, single-use for reset flows
  - Performance: Authentication requests should complete within 200ms (p95)
  - Compliance: GDPR-compliant data handling, no passwords in logs

Output:
  Full specification with user stories, acceptance criteria, and non-functional
  requirements saved to specs/auth/spec.md in Spec Kit compatible format.

 think through this specification systematically. Consider all
security implications, edge cases, and user experience flows before finalizing.

Rate your confidence in this specification from 0-1 after completion.
```

## Handling Edge Cases

### Prompt Already Structured
If user input is already well-structured:
1. Analyze prompt for TCRO elements
2. Identify any missing elements
3. Ask targeted questions to fill gaps (not full re-clarification)
4. Confirm if structure is sufficient or needs refinement

### User Refuses Clarification
If user declines clarifying questions:
1. Proceed with best-effort TCRO structure
2. Use `[NEEDS CLARIFICATION: ...]` markers for ambiguous items
3. Note which elements were assumed vs explicitly specified

### Incomplete Context
If CLAUDE.md doesn't exist or is incomplete:
1. Proceed without project-specific context
2. Ask basic context questions (tech stack, goals)
3. Note in refined prompt: "No project constitution found, using generic defaults"

## Quality Checklist

Before finalizing refined prompt, verify:
- [ ] Task is specific and actionable
- [ ] Context includes relevant project information
- [ ] Requirements distinguish must-have vs nice-to-have
- [ ] Output format is clearly specified
- [ ] Appropriate expert persona assigned
- [ ] Stakes language added for important tasks
- [ ] Clarification markers used for ambiguities

## Integration with incentive-prompting Skill

This skill builds on the `incentive-prompting` skill. Always load both skills together when refining prompts:

```markdown
Use skill: incentive-prompting
Use skill: prompt-refinement
```

The `incentive-prompting` skill provides the enhancement techniques
(Expert Persona, Stakes Language, Step-by-Step, Self-Evaluation).

This skill provides the structuring framework (TCRO) and phase-specific
clarification questions.

Together they produce prompts that are both well-structured and
enhanced for maximum AI response quality.
