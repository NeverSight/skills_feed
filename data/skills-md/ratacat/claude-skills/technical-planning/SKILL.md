---
name: technical-planning
description: Plans technical projects with risk-first development, milestone structuring, and managed deferral. Use when planning software projects, defining milestones, structuring development phases, or breaking down complex tasks into manageable iterations.
---

# Technical Planning

## Core Principles

**Focus on "What" Not "How"**: Define deliverable outcomes, not implementation details. Specify constraints and success criteria, but leave implementation choices flexible.

**Last Responsible Moment**: Defer decisions until you have enough information to make them well, but not so late that they block progress. Make reversible decisions quickly; delay irreversible ones until necessary.

**Risk-First Development**: Address highest-risk technical challenges first. Build proof-of-concepts before full implementation. Ship working but imperfect solutions to validate core assumptions early.

**Managed Deferral**: Explicitly document what's being deferred and when it will be addressed. Distinguish between core value delivery and polish/optimization.

### Progress Tracking with TodoWrite

Use TodoWrite to track planning progress through the four phases:

1. **At start**: Create todos for each phase:
   ```
   ☐ Phase 1: Requirements & Risk Analysis
   ☐ Phase 2: Milestone Planning
   ☐ Phase 3: Implementation Strategy
   ☐ Phase 4: Execution Framework
   ```

2. **During planning**: Mark phases in_progress → completed as you work through them. Add sub-todos for key deliverables:
   ```
   ☐ Extract core requirements (2-3 user journeys)
   ☐ Identify technical risks (high/integration/performance/architecture)
   ☐ Define milestones with success criteria
   ☐ Document deferred items with rationale
   ```

3. **For complex projects**: Track clarifying questions and their resolutions as todos - prevents proceeding with incomplete information

### Decision Timing Framework

**Decide Early (Requirements Phase)**:
- User problems being solved
- Success criteria and measurement
- Hard constraints (security, compliance, performance SLAs)
- Critical integrations and dependencies
- Technology choices that affect architecture

**Defer to Implementation (Execution Phase)**:
- Specific algorithms or data structures
- Internal API design details
- Code organization patterns
- Library choices (when multiple options work)
- Performance optimizations (until proven necessary)
- UI/UX details (until user testing)

**Why**: Early decisions should enable work without locking in details. Implementation decisions become clearer with hands-on experience and often reveal better alternatives than upfront planning suggests.

## Agent Guidelines

**Seek Clarity Before Proceeding**: Never assume unclear requirements, technical constraints, or business priorities. Only proceed when you have 80%+ confidence on critical aspects. Ask specific questions about:

- User problems being solved (not just features requested)
- Success criteria and measurement approaches
- Technical constraints and existing system dependencies
- Team capabilities and technology preferences
- Timeline constraints and priority trade-offs
- Performance and scalability requirements

## Phase 1: Requirements & Risk Analysis

### Prerequisites Check

Verify:

- What user problems are being solved?
- Who are the primary users and their workflows?
- How will success be measured?
- What are the technical and business constraints?

### Extract Core Requirements

1. Identify fundamental user problems being solved
2. Map primary user journeys (focus on 2-3 critical paths)
3. Define project success metrics

### Identify Technical Risks

1. **High-Impact Risks**: Technical unknowns that could invalidate the approach
2. **Integration Risks**: External system dependencies and compatibility concerns
3. **Performance Risks**: Scalability bottlenecks and algorithmic challenges
4. **Architecture Risks**: Fundamental design decisions with broad implications

### Risk Prioritization Matrix

- **Critical + Unknown**: Must be addressed in Milestone 1 with proof-of-concepts
- **Critical + Known**: Address in early milestones with established patterns
- **Non-Critical**: Defer to later milestones or eliminate

## Phase 2: Milestone Planning

### Prerequisites Check

Verify:

- Priority order of technical risks identified in Phase 1
- Team capacity and available timeline
- Dependencies between different components
- Definition of "working functionality" for this project

### Milestone Structure

- **Timeline**: 4-8 week cycles based on project complexity
- **Deliverable**: Each milestone must produce working, testable functionality
- **Risk Focus**: Sequence milestones to tackle highest-risk items first

### For Each Milestone, Define:

**Goal**: One-sentence description of milestone outcome

**Core Tasks**: 4-6 main implementation tasks following Last Responsible Moment principle:
- Define clear outcomes and constraints
- Identify dependencies and integration points
- Provide context and considerations (not step-by-step instructions)
- Leave implementation details flexible
- Flag questions to resolve during execution

**Success Criteria**:
- Minimum Viable Success (must achieve for milestone completion)
- Complete Success (ideal outcome including polish)

**Risk Mitigation**: Specific unknowns to be resolved in this milestone

**Deferred Items**: What's intentionally left out and target milestone for inclusion

### Task Breakdown Guidelines

When breaking down tasks, provide **guidance not prescription**:

**✓ Good Task Definition** (outcome-focused):
- Goal: "Enable users to authenticate securely"
- Constraints: "Must integrate with existing session middleware; <100ms response time"
- Guidance: "Consider session vs. token auth; review existing patterns in src/middleware/"
- Validation: "Users can log in, sessions persist, tests pass"

**✗ Poor Task Definition** (overly prescriptive):
- Step 1: "Create file auth.js with bcrypt import"
- Step 2: "Write hashPassword function using bcrypt.hash with 10 rounds"
- Step 3: "Create Express middleware checking req.session.userId"

**Why**: Good definitions let the implementer choose the best approach based on what they learn. Poor definitions lock in choices before understanding the context, often leading to rework.

### Example Milestone Definition

**Goal**: Validate user authentication and basic data retrieval from external API

**Core Tasks**:
1. Implement OAuth flow with provider
2. Create user session management
3. Build API client with error handling
4. Add basic user profile display

**Success Criteria**:
- Minimum: Users can log in and see their profile data
- Complete: Include profile editing and session persistence

**Risk Mitigation**: Confirm API rate limits and response time under load

**Deferred**: Advanced profile features, password reset flow (Milestone 3)

## Phase 3: Implementation Strategy

### Development Approach

- **Prototype First**: Build throwaway versions to test risky assumptions
- **Core Before Polish**: Implement functional features before UI refinements
- **Integration Early**: Test external system connections in first milestone
- **Measure Continuously**: Track performance and user metrics from day one

### Technology Selection Criteria

1. **Team Expertise**: Prefer technologies your team knows well
2. **Proven Reliability**: Choose mature, battle-tested options for core systems
3. **Integration Capability**: Ensure compatibility with existing tools/systems
4. **Scalability Path**: Technology should support anticipated growth

### Quality Gates

- All code must have basic test coverage
- Performance benchmarks must be met for core user journeys
- Security review required for authentication and data handling
- Accessibility standards met for user-facing features

## Phase 4: Execution Framework

### Sprint Planning

1. **Risk Assessment**: Identify unknowns in upcoming work
2. **Exploration Time**: Reserve 20-30% of sprint for prototyping/learning
3. **Definition of Done**: Must include working functionality, not just completed code
4. **Continuous Validation**: Regular stakeholder feedback on core user journeys

### Deferral Management

- **Regular Review**: Evaluate deferred items each milestone for continued relevance
- **Categories**: Technical debt, UX polish, edge cases, performance optimization, advanced features
- **Scheduling**: Plan deferred items into appropriate future milestones
- **Elimination**: Some deferred items may become unnecessary

### Documentation Requirements

- Technical specification focusing on deliverable outcomes
- Risk register with mitigation plans
- Deferred items registry with target scheduling
- Architecture decision records for major choices

## Decision Framework for Agents

**IF** project has unknown technical feasibility → Schedule proof-of-concept in Milestone 1
**IF** project requires external integrations → Test minimal integration in first milestone
**IF** project has performance requirements → Establish benchmarks and test core algorithms early
**IF** team lacks expertise in chosen technology → Include learning/exploration time in early milestones
**IF** project has tight deadlines → Focus on minimum viable success criteria and defer polish
**IF** project is greenfield → Spend extra time on architecture decisions and foundational setup
**IF** project is enhancement → Focus on integration points and backward compatibility

### When Unclear - Ask These Questions

**WHEN** requirements are vague → "What specific user problem does this solve? How will we measure success?"
**WHEN** technical scope is undefined → "What are the must-have vs. nice-to-have technical capabilities?"
**WHEN** timeline is unrealistic → "What are the non-negotiable deadlines and what flexibility exists?"
**WHEN** team capabilities are unknown → "What technologies does the team have experience with? What are the skill gaps?"
**WHEN** integration points are unclear → "What existing systems must this connect to? What are the data formats and API constraints?"
**WHEN** performance needs are unspecified → "What are the expected user loads and response time requirements?"
**WHEN** success criteria are missing → "How will we know this milestone is complete and successful?"

## Common Pitfalls to Avoid

- **Making assumptions instead of asking clarifying questions** when requirements are unclear
- **Proceeding with incomplete information** rather than requesting necessary details
- **Creating overly prescriptive task definitions** with step-by-step instructions instead of outcome-focused guidance
- **Making implementation decisions too early** when they could be deferred to execution
- Spending time on low-risk features while deferring critical unknowns
- Over-engineering solutions before validating core assumptions
- Planning implementation details instead of focusing on deliverable outcomes
- **Guessing at user needs** instead of understanding specific problems being solved
- Failing to document deferral decisions and rationale
- Optimizing prematurely instead of proving core functionality first
- **Locking in technology choices** before understanding the full context
