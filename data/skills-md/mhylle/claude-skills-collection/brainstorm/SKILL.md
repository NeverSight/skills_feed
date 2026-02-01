---
name: brainstorm
description: Interactive idea refinement using Socratic questioning methodology. This skill should be used when users want to explore an idea, find gaps in concepts, enhance proposals, or structure thoughts before implementation planning. Triggers on "brainstorm", "explore this idea", "find holes in", "help me think through", "what am I missing", or when presenting rough concepts that need refinement. Output integrates with create-plan skill.
context: fork
agent: Explore
---

# Brainstorm

## Overview

This skill provides structured brainstorming through Socratic questioning, multi-perspective analysis (Six Thinking Hats, SCAMPER), and proactive research. It helps users refine raw ideas into well-structured concepts ready for implementation planning.

## Initial Response

When this skill is invoked, respond:

> "I'm ready to help you explore and refine your idea. Share what you're thinking about, and I'll ask questions to help clarify, challenge assumptions, and identify opportunities. We'll continue the exploration until you're satisfied, then I'll research relevant patterns and structure the concept."

## Workflow (6 Phases)

### Phase 1: Idea Capture

Parse the user's initial idea/concept and identify:

| Element | Description |
|---------|-------------|
| **Core Concept** | The fundamental idea being proposed |
| **Stated Goals** | What the user explicitly wants to achieve |
| **Implied Constraints** | Limitations mentioned or implied |
| **Project Context** | Whether this relates to an existing codebase |

**Project Context Detection** - Flag for codebase research when:
- User mentions specific files, modules, or features
- User references "the current system" or "our codebase"
- User mentions extending/modifying existing functionality
- Context includes technical terms specific to a project domain

After parsing, summarize understanding and begin Phase 2.

### Phase 2: Socratic Clarification

Engage in iterative questioning until the user signals readiness to proceed.

**Question Categories** (reference: `references/questioning-frameworks.md`):

1. **Scope Questions**
   - "What boundaries should this have?"
   - "What's explicitly out of scope?"
   - "How does this fit with existing systems?"

2. **Assumption Questions**
   - "What are we taking for granted here?"
   - "What would happen if [assumption] wasn't true?"
   - "What implicit dependencies exist?"

3. **Alternative Questions**
   - "What other approaches could achieve this?"
   - "What's the opposite of this approach?"
   - "What would [different stakeholder] suggest?"

4. **Consequence Questions**
   - "What happens if this succeeds?"
   - "What happens if this fails?"
   - "What are the second-order effects?"

5. **Evidence Questions**
   - "What supports this approach?"
   - "How could we test this assumption?"
   - "What evidence would change your mind?"

**Continuation Protocol**:
- Ask 2-4 questions per round
- After each round, offer: "I have more questions if you'd like to continue exploring, or we can move to research and analysis. Your call."
- Continue until user explicitly signals readiness (e.g., "let's move on", "I'm ready", "that's enough questions")
- Do NOT rush this phase - thorough questioning produces better outcomes

### Phase 3: Context Gathering

Spawn parallel agents to gather context. Execute all relevant research in a single message with multiple Task tool calls.

**Always spawn - Web Research**:
```
Task(subagent_type="web-search-researcher",
     prompt="Research best practices, common patterns, and pitfalls for [idea topic].
             Find:
             1. Similar implementations and how they succeeded/failed
             2. Industry best practices and anti-patterns to avoid
             3. Common technical approaches and their trade-offs
             4. Lessons learned from comparable projects
             Focus on actionable insights, not just general information.")
```

**Spawn when project context detected - Codebase Research**:
```
Task(subagent_type="codebase-locator",
     prompt="Find all files related to [relevant feature area]. Include:
             - Core implementation files
             - Configuration and setup files
             - Test files
             - Documentation")

Task(subagent_type="codebase-analyzer",
     prompt="Analyze how [related functionality] is currently implemented.
             Trace the data flow and identify integration points.
             Include file:line references.")

Task(subagent_type="codebase-pattern-finder",
     prompt="Find implementation patterns for [type of implementation] in this codebase.
             Look for:
             - Similar features and how they're structured
             - Conventions for [relevant patterns]
             - Testing approaches used")
```

Wait for all agents to complete using AgentOutputTool before proceeding.

### Phase 4: Multi-Perspective Analysis

Apply structured frameworks to analyze the refined idea systematically.

**Six Thinking Hats Analysis**:

| Hat | Focus | Questions to Apply |
|-----|-------|-------------------|
| **White** | Facts | What facts do we have? What data is missing? What do we need to know? |
| **Red** | Intuition | What's the gut reaction? What feels risky? What's exciting about this? |
| **Black** | Risks | What could go wrong? What obstacles exist? What are the failure modes? |
| **Yellow** | Benefits | What benefits does this bring? What opportunities exist? What's the best case? |
| **Green** | Creativity | What creative alternatives exist? What's an unconventional approach? What if we combined this with something else? |
| **Blue** | Process | Is this the right problem to solve? Are we approaching this correctly? What's the next step? |

**SCAMPER Enhancement Scan**:

| Letter | Question | Application |
|--------|----------|-------------|
| **S**ubstitute | What could be replaced? | Alternative technologies, patterns, approaches |
| **C**ombine | What could be merged? | Related features, existing capabilities |
| **A**dapt | What could be adjusted from elsewhere? | Patterns from other domains |
| **M**odify | What could be amplified or reduced? | Scope, complexity, features |
| **P**ut to other use | What alternative applications exist? | Reusability, generalization |
| **E**liminate | What could be removed? | Unnecessary complexity, redundant features |
| **R**everse | What could be reorganized? | Order of operations, dependencies |

**Premortem Analysis**:

Apply this framework to identify preventable failure modes:

1. "Imagine this idea has completely failed 6 months from now."
2. "What went wrong?"
3. "What warning signs did we ignore?"
4. "What did we underestimate?"
5. "What external factors contributed?"
6. "Now: How do we prevent each of these?"

Document findings for each framework.

### Phase 5: Synthesis

Consolidate all findings into actionable insights:

**Validated Strengths**
- List strengths confirmed by analysis
- Include supporting evidence from research

**Identified Gaps**
- List gaps discovered through questioning and analysis
- Include suggested approaches for each gap

**Enhancement Opportunities**
- List improvements identified through SCAMPER
- Prioritize by impact and feasibility

**Risk Assessment**
- List risks from Black Hat and Premortem analysis
- Include mitigation strategies for each

**Key Decisions Required**
- List open questions that need user decision
- Provide options with trade-offs

### Phase 5b: Document Key Decisions (ADR)

**Before creating new ADRs**, check for existing related decisions:

```
# Tiered ADR reading (context conservation)
1. Read("docs/decisions/INDEX.md")              # Scan existing decisions
2. Read("docs/decisions/ADR-NNNN.md", limit=10) # Quick Reference of relevant ones
3. Only create new ADR if decision is genuinely new or supersedes existing
```

**When significant architectural decisions emerge** from the brainstorm analysis, invoke the ADR skill to document them:

```
Skill(skill="adr"): Document key decision from brainstorm.

Title: [Decision title]
Context: [Why this decision is needed - from brainstorm context]
Options Considered: [Alternatives from analysis]
Decision: [The recommended or chosen approach]
Rationale: [From Six Hats/SCAMPER analysis]
Consequences: [From premortem and risk assessment]
Status: Proposed (or Accepted if user confirmed)
```

The ADR skill will create the ADR file and update INDEX.md.

**Triggers for creating ADRs during brainstorming:**
- Clear winner emerges from option analysis
- User makes a definitive choice between approaches
- Technology or architecture decision crystallizes
- Pattern or convention is established for the project

**Multiple ADRs**: If the brainstorm identifies several distinct decisions, create separate ADRs for each. Reference them in the output's "Key Decisions" section.

**ADR Status**: Set to "Proposed" unless the user has explicitly confirmed the decision, in which case set to "Accepted".

### Phase 6: Structure & Output

Structure the concept into logical components and write results.

**Determine Output Location**:
- Default: `docs/brainstorms/YYYY-MM-DD-{topic-slug}.md`
- Create directory if it doesn't exist
- Use descriptive slug from core concept

**Write Structured Output** using this format:

```markdown
# Brainstorm: [Idea Name]

**Date**: YYYY-MM-DD
**Status**: Ready for Planning | Needs More Exploration

## Executive Summary
[2-3 sentence refined description of the idea after Socratic exploration]

## Idea Evolution

### Original Concept
[What the user initially described - preserve their words]

### Refined Understanding
[How the idea evolved through questioning - what became clearer]

### Key Clarifications Made
- [Clarification 1]
- [Clarification 2]

## Analysis Results

### Strengths (Yellow Hat)
- [Strength 1 with supporting evidence]
- [Strength 2 with supporting evidence]

### Risks & Concerns (Black Hat + Premortem)
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Strategy] |

### Gaps Identified
- [ ] **[Gap 1]** - Suggested approach: [...]
- [ ] **[Gap 2]** - Suggested approach: [...]

### Enhancement Opportunities (SCAMPER)
- **Substitute**: [Enhancement if applicable]
- **Combine**: [Enhancement if applicable]
- **Adapt**: [Enhancement if applicable]
- **Modify**: [Enhancement if applicable]
- **Put to other use**: [Enhancement if applicable]
- **Eliminate**: [Enhancement if applicable]
- **Reverse**: [Enhancement if applicable]

### Premortem Findings
- **Failure mode**: [Description] → **Prevention**: [Strategy]
- **Failure mode**: [Description] → **Prevention**: [Strategy]

## Structured Concept

### Component 1: [Name]
**Purpose**: [What it does]
**Scope**: [Boundaries]
**Dependencies**: [What it needs]
**Key Decisions**: [Decisions made or needed]

### Component 2: [Name]
[Continue pattern for each logical component...]

## Research Findings

### External Best Practices
[Synthesized findings from web-search-researcher]
- [Best practice 1 with source]
- [Best practice 2 with source]

### Anti-Patterns to Avoid
- [Anti-pattern 1]
- [Anti-pattern 2]

### Codebase Context (if applicable)
[Findings from codebase agents]
- Relevant files: [file:line references]
- Existing patterns to follow: [patterns]
- Integration points: [components]

## Architectural Decisions

### Documented ADRs
| ADR | Title | Status |
|-----|-------|--------|
| [ADR-NNNN](../decisions/ADR-NNNN-title.md) | [Title] | Proposed/Accepted |

### Pending Decisions (not yet documented)
- [Decision 1]: [Options being considered]
- [Decision 2]: [Options being considered]

## Recommended Next Steps
1. [Immediate next step]
2. [Follow-up step]
3. [Future consideration]

## Ready for Create-Plan
**[Yes/No]**

**If Yes**: The concept is well-defined and ready for implementation planning.
**If No**: [Specific reason - what needs more exploration]

### Suggested Plan Scope
[Brief description of what create-plan should focus on, including:
- Primary deliverables
- Key phases to consider
- Critical success factors]
```

**After Writing**:
1. Confirm file was saved successfully
2. Present summary to user
3. Offer to invoke create-plan skill if status is "Ready for Planning"

## Quality Checklist

Before finalizing output, verify:

- [ ] All Socratic clarifications were documented
- [ ] Web research was conducted and synthesized
- [ ] Codebase research was conducted (if project context detected)
- [ ] All six thinking hats were applied
- [ ] SCAMPER analysis was completed
- [ ] Premortem was conducted with prevention strategies
- [ ] Risks have mitigation strategies
- [ ] Gaps have suggested approaches
- [ ] Concept is structured into logical components
- [ ] Output file was successfully written
- [ ] Ready-for-plan status is accurate

## Best Practices

### Effective Questioning
- Ask open-ended questions, not yes/no
- Use "what" and "how" more than "why" (less confrontational)
- Build on previous answers
- Acknowledge good insights before probing deeper

### Avoiding Common Pitfalls
- Don't rush the Socratic phase - depth matters
- Don't criticize ideas during clarification - that's for analysis
- Don't skip frameworks - each provides unique perspective
- Don't present analysis without actionable next steps

### Integration with Create-Plan
The output format is designed to feed directly into create-plan:
- "Structured Concept" maps to implementation phases
- "Gaps" become tasks to address
- "Risks" become items in "Risks and Mitigations"
- "Research Findings" inform design decisions

## Resources

### references/
- `questioning-frameworks.md` - Detailed question templates for Socratic, Six Hats, SCAMPER, and Premortem frameworks
