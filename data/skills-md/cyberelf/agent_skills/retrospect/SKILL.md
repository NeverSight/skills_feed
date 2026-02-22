---
name: retrospect
description: This skill reviews the current chat session and GitHub Copilot instructions to identify user-reported issues that should become new lessons, detect violations of existing instructions, and update instructions accordingly to prevent future mistakes.
metadata:
  author: cyberelf
  version: "1.0"
---

# Retrospect Skill

This skill performs meta-analysis on the current conversation and project instructions to continuously improve code and process quality and adherence to established patterns.

## Purpose

This skill helps maintain and improve the quality of AI-assisted development by:
1. Identifying patterns where user corrections reveal gaps in instructions
2. Detecting violations of existing coding standards and conventions
3. Updating instructions to prevent repeating the same mistakes
4. Creating a feedback loop for continuous improvement

## When to Use This Skill

Use this skill when:
- A user points out a recurring mistake or anti-pattern
- Multiple corrections have been made during a session
- You want to ensure coding standards are being followed
- A user explicitly requests instruction review or updates
- After completing a significant feature or fix

## Retrospect Process

### Phase 1: Session Analysis

**Objective**: Review the current chat session to identify learning opportunities.

#### 1.1 Collect User Corrections

Scan the conversation history for:
- Direct corrections: "No, you should..." or "That's wrong, the correct way is..."
- Repeated mistakes: Same issue corrected multiple times
- Clarifications: "Actually, we use X instead of Y"
- New requirements: "From now on, always do X when Y"
- Anti-patterns: "Don't do X, prefer Y"

#### 1.2 Identify Instruction Gaps

For each correction, determine:
- Is this covered by existing instructions?
- Is this a new pattern that should be documented?
- Is this specific to this project or a general principle?
- Should this be a new rule, guideline, or example?

#### 1.3 Categorize Lessons

Classify lessons by domain and type:
- **Architecture**: Design patterns, system organization, separation of concerns
- **Process**: Workflows, procedures, operational patterns
- **Behavioral**: Agent decision-making, interaction patterns, role adherence
- **Communication**: Documentation standards, reporting formats, terminology
- **Domain-Specific**: Business logic, domain rules, specialized requirements
- **Quality**: Standards, conventions, validation patterns
- **Integration**: Cross-system patterns, API usage, external dependencies

### Phase 2: Constitution Review

**Objective**: Verify compliance with existing standards and constitutions.

#### 2.1 Load Current Constitutions

Read all relevant constitution and standards documents:
- `AGENTS.md` - Agent architecture, behavior patterns, and operational guidelines
- `SDD` files (Software Design Documents) - System design principles and requirements
- Project-specific constitution files (`.github/constitution.md`, `docs/constitution.md`)
- Domain-specific standards and guidelines
- Any `.copilot-instructions.md` or similar instruction files

**Document Discovery Strategy**:
1. Search for `AGENTS.md` in project root and docs folders
2. Search for SDD files (look for patterns: `*SDD.md`, `*design*.md`, `requirements.md`)
3. Search for constitution files in `.github/`, `docs/`, or root directory
4. Check for skill-specific constitution documents in skills folders

#### 2.2 Scan for Violations

Review actions and outputs from the session against constitutions:
- **Process violations**: Not following prescribed workflows or procedures
- **Principle violations**: Contradicting stated design principles or values
- **Standard violations**: Deviating from established patterns or conventions
- **Requirement violations**: Missing mandatory elements or constraints
- **Behavioral violations**: Acting inconsistently with agent role or responsibilities
- **Communication violations**: Not following documentation or reporting standards

#### 2.3 Cross-Reference with Corrections

Compare user corrections with existing constitutions:
- Was the constitution rule ignored or misunderstood?
- Was the constitution unclear or ambiguous?
- Does the constitution conflict with other guidelines?
- Is the constitution outdated or incorrect?
- Was the violation due to missing context or incomplete information?

### Phase 3: Constitution Update

**Objective**: Formalize lessons learned into actionable constitutions.

**Update Strategy**:
1. Identify the appropriate constitution document to update
2. Check if a skill exists for updating that document type
3. If a skill exists, invoke it with the update requirements
4. If no skill exists, perform in-place updates following document conventions

#### 3.1 Draft New Constitution Rules

For each identified gap or violation:

**Structure**:
```markdown
## [Category]: [Specific Rule]

**Context**: [When does this apply?]

**Rule**: [What should be done?]

**Rationale**: [Why is this important?]

**Example** (if helpful):
```code
// Bad
[anti-pattern]

// Good
[correct pattern]
```

**Related Instructions**: [Link to related rules]
```

#### 3.2 Update Existing Constitutions

**In-Place Update Process**:

For violations of existing constitution rules:
- Clarify ambiguous language
- Add concrete examples relevant to the domain
- Strengthen weak guidelines (e.g., "should" → "must")
- Add cross-references to related rules
- Add "Common Mistakes" or "Anti-Patterns" sections

**Skill-Based Updates** (if available):

1. **Check for update skills**: Search for skills related to the constitution document
   - `openspec-constitution-guard` for OpenSpec constitutions
   - `agents-constitution-updater` for AGENTS.md
   - Document-specific updater skills

2. **Invoke update skill**: If found, call the skill with:
   - The lesson learned
   - The violation context
   - Proposed update text
   - Rationale for the change

3. **Fallback to direct update**: If no skill exists, update the file directly

#### 3.3 Create New Constitution Entries

For lessons that don't fit existing documents, create or update appropriate constitution files:

**Location Options**:
- `.github/constitution.md` - General project principles
- `AGENTS.md` - Agent-specific behaviors and patterns
- `docs/constitution.md` - Domain-specific guidelines
- Skill-specific constitutions in `skills/[skill-name]/constitution.md`

**Format**:
```markdown
# Project Constitution

This document captures project-specific principles and lessons learned.

## [Principle Name]

**Date Added**: YYYY-MM-DD
**Origin**: [What situation led to this principle?]

**Principle**: [Clear statement of the rule]

**Application**: [How to apply this in practice]

**Examples**: [Concrete examples]
```

### Phase 4: Validation

**Objective**: Ensure updates are effective and non-disruptive.

#### 4.1 Review Changes

- Ensure new instructions don't contradict existing ones
- Verify examples are accurate and compilable
- Check that rationale is clear and convincing
- Confirm changes are actionable (specific, measurable)

#### 4.2 Test Instructions

- Review recent code against updated instructions
- Verify instructions would have prevented the mistake
- Check for unintended consequences or side effects

#### 4.3 Summarize Changes

Provide a summary:
```markdown
## Retrospect Summary

### Lessons Learned
1. [Lesson 1]: [What was learned and why]
2. [Lesson 2]: [What was learned and why]

### Instructions Updated
- **File**: [filename]
  - **Section**: [section name]
  - **Change**: [what was changed]
  - **Reason**: [why it was changed]

### New Violations Detected
1. [Violation 1]: [Description and location]
2. [Violation 2]: [Description and location]

### Recommendations
- [Action item 1]
- [Action item 2]
```

## Output Format

The retrospect process should produce:

1. **Retrospect Report** (printed to console):
   - Summary of lessons learned
   - List of instruction violations
   - Recommendations for improvement

2. **Updated Constitution Files**:
   - Modified `AGENTS.md` with updated agent behaviors and principles
   - Updated SDD files with refined design requirements
   - Modified `constitution.md` files with clarifications and new rules
   - Skill-specific constitution updates

3. **Action Items**:
   - Processes that need refinement
   - Behaviors that need adjustment
   - Documentation that needs updating
   - Skills that need to be created or modified

## Best Practices
Constitutions

1. **Be Specific**: "Validate inputs" → "All agent operations MUST validate input structure and constraints before any processing or state chang
1. **Be Specific**: "Use Pydantic models" → "Use Pydantic models instead of dict[str, Any] for all API request/response bodies"
2. **Explain Why**: Include rationale so the principle is understood, not just memorized
3. **Provide Examples**: Show both the wrong way and the right way
4. **Make it Actionable**: Instructions should be clear enough to follow without interpretation
5. **Prioritize**: Use "must", "should", "prefer" to indicate priority level

### Avoiding Over-Prescription

- Don't create rules for one-off situations
- Focus on patterns that repeat across multiple instances
- Leave room for judgment and context-specific decisions
- Balance between guidance and flexibility

### Maintaining Consistency

- Use consistent terminology across all instruction files
- Cross-reference related instructions
- Organize instructions hierarchically (general → specific)
- Keep a single source of truth for each concept

## Implementation Guidelines

### When Running Retrospect

1. **Start with analysis**: Don't jump to solutions
2. **Be thorough**: Review entire conversation history
3. **Stay objective**: Look for patterns, not just recent issues
4. **Think long-term**: Will this instruction scale as the project grows?
5. **Validate changes**: Test that new instructions would prevent the issue

### After Retrospect

1. **Apply updates immediately**: Update instruction files right away
2. **Communicate changes**: Summarize what changed and why
3. **Verify effectiveness**: Check if similar mistakes are prevented
4. **Iterate**: Retrospect is continuous, not one-time

## Example Scenarios

### Scenario 1: Workflow Process Violation

**User Correction**: "Don't skip the validation step - always validate inputs before processing"

**Analysis**: 
- Violation of established workflow in AGENTS.md or SDD
- Skipped mandatory process step

**Constitution Update** (AGENTS.md):
```markdown
### Input Validation Protocol

**Context**: All agent operations that accept external inputs

**Rule**: Input validation MUST occur before any processing or state changes.

**Rationale**: Prevents cascading errors and ensures data integrity throughout the system.

**Process**:
1. Receive input
2. Validate structure and constraints
3. Transform to internal representation
4. Process validated data

**Anti-Pattern**: Processing data before validation

**Related**: See "Error Handling Standards" and "State Management"
```

### Scenario 2: Agent Role Violation

**User Correction**: "This agent shouldn't be making decisions about deployment - that's the DevOps agent's responsibility"

**Analysis**:
- Violation of agent role boundaries defined in AGENTS.md
- Overstepping defined responsibilities

**Constitution Update** (AGENTS.md):
```markdown
### Agent Responsibility Boundaries

**Context**: Multi-agent system with defined roles

**Rule**: Each agent MUST operate only within its defined domain. Cross-domain decisions require delegation to the appropriate agent.

**[AgentName] Responsibilities**:
- [Primary responsibility 1]
- [Primary responsibility 2]

**NOT Responsible For**:
- Deployment decisions → DevOps Agent
- Security policies → Security Agent
- Resource allocation → Resource Manager Agent

**Delegation Protocol**: When encountering a task outside your domain:
1. Identify the appropriate agent
2. Format the delegation request
3. Hand off with full context
4. Wait for response or acknowledgment

**Rationale**: Maintains clear separation of concerns and prevents conflicting decisions.
```

## References

- Agent architecture: `AGENTS.md`
- System design: SDD files in `spec/` or `docs/`
- Constitution documents: `.github/constitution.md`, `docs/constitution.md`
- Update skills: `skills/openspec-constitution-guard/`, `skills/*/constitution.md`
- Workflow documentation: Project-specific process documents

## Continuous Improvement

This skill itself should evolve:
- Add new analysis patterns as they emerge
- Refine the instruction update format
- Improve violation detection accuracy
- Enhance the categorization of lessons

The meta-goal is to make AI-assisted development increasingly accurate and aligned with project standards over time.
