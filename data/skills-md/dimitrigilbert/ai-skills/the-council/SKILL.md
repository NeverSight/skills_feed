---
name: the-council
description: Expert council facilitation for complex decision-making. Use when you need multiple specialist perspectives on a subject, requiring thorough analysis, research-backed opinions, and structured deliberation to reach consensus or properly present diverging views.
---

This skill facilitates structured deliberation by summoning a council of specialist subagents to analyze complex questions from multiple perspectives, conduct independent research, and reach informed decisions through consensus or structured debate.

## Quick Start

### When to summon a council

Use this skill when:
- A question requires expertise from multiple domains
- You need thorough analysis with proper research and sources
- A decision would benefit from multiple expert perspectives
- You need to identify and resolve conflicting viewpoints
- Complex trade-offs require structured evaluation

### When NOT to summon a council

Skip the council when:
- The question has a single domain of expertise (just use one specialist)
- You need a quick answer (council adds coordination overhead)
- The decision is already made and you're seeking validation
- Time constraints don't allow for thorough deliberation
- The question is straightforward with an obvious answer
- The user hasn't configured specialists relevant to the question

### Basic council summoning

```
Summon a council to analyze: [your question/topic]

Required specialists:
- [Specialist 1]: [their role/focus]
- [Specialist 2]: [their role/focus]
- [Specialist 3]: [their role/focus]
```

### Council composition examples

**Technical architecture decision:**
```
Specialists:
- Security architect: Analyze security implications
- Performance engineer: Evaluate performance impact
- DevOps specialist: Assess deployment and operations
- Backend architect: Review implementation complexity
```

**Product strategy question:**
```
Specialists:
- User experience advocate: Analyze user impact
- Business analyst: Evaluate business viability
- Technical feasibility expert: Assess implementation
- Market analyst: Consider competitive landscape
```

**Code review with complexity:**
```
Specialists:
- Security reviewer: Check for vulnerabilities
- Performance specialist: Identify bottlenecks
- Maintainability expert: Assess code quality
- Domain expert: Validate business logic
```

## Core Concepts

### The Council Structure

**Chair (You)**: Responsible for:
- Summoning appropriate specialists
- Gathering and synthesizing councillor analyses
- Identifying consensus and dissent
- Facilitating structured debates when needed
- Rendering final decisions or presenting diverging opinions

**Councillors (Specialist Subagents)**: Each councillor:
- Conducts independent preliminary analysis
- Researches using all available tools (Context7, WebSearch, etc.)
- Bases analysis on reality, artifacts, and provided tasks
- Saves complete analysis with cited sources to councillor file
- Uses existing skills when relevant to their expertise

### Council Workflow

```
1. SUMMON
   Identify required specialists based on the question domain
   Create councillor files directory: .council/[session-id]/

2. ANALYZE (Parallel)
   Each councillor:
   - Receives the full context/question
   - Conducts independent research
   - Writes preliminary analysis to .council/[session-id]/[specialist].md
   - Cites all sources (URLs, library+search query for Context7)

3. SYNTHESIZE
   Chair reads all councillor files
   Identifies areas of consensus and dissent
   Maps out the decision landscape

4. DELIBERATE (If needed)
   For areas of dissent:
   - Chair facilitates 1-on-1 or small group discussions
   - Councillors confront positions with evidence
   - Goal: Reach consensus OR clearly articulate diverging views

5. DECIDE
   Chair renders:
   - Final decision with rationale (if consensus reached)
   - Detailed presentation of diverging opinions (if no consensus)
```

### Councillor File Format

Each councillor saves their analysis to `.council/[session-id]/[specialist-name].md`:

```markdown
# [Specialist Name] Analysis

## Question
[Restate the question being analyzed]

## Preliminary Assessment
[Summary position: Support/Oppose/Conditional with key reasoning]

## Analysis
[Detailed analysis of the question/task]

## Evidence & Research
### Sources Consulted
- **[Source Type]:** [Name] - [URL or reference]
- **Context7:** [library-name] - [search query used]
- **Web Search:** [search query] - [key findings]

### Findings
[What the research reveals about the question]

## Recommendations
[Specific recommendations based on analysis and research]

## Confidence Level
[High/Medium/Low - with rationale]

## Open Questions
[Any aspects requiring further investigation or clarity]
```

## Guidelines

### Choosing Specialists

Select councillors based on:
- **Domains touched**: What expertise areas does this question involve?
- **Stakeholders**: Who would be affected by this decision?
- **Risks**: What could go wrong? (security, performance, ux, business)
- **Complexity**: What specialized knowledge is required?

**Aim for 3-7 specialists.** Too few = blind spots; too many = coordination overhead.

### Dynamic Specialist Selection

When summoning councillors, the Chair should:

1. **Identify domains** needed for the question (security, performance, UX, etc.)
2. **Check available agents** - Use the Task tool's available agent types
3. **Match domains to agents** - Select the most relevant specialized agent for each domain
4. **Fall back to `general`** - If no specialized agent exists for a domain, use `general` with a clear specialist persona

**Selection process:**
```
For each domain needed:
1. Is there a specialized agent that covers this domain? → Use it
2. No specialized agent? → Use `general` with domain-specific instructions
```

**Example domain-to-agent mapping:**
- Security concerns → Look for security-focused agents, or use `general` as "Security Analyst"
- Frontend/UI → Look for frontend agents, or use `general` as "Frontend Specialist"
- Architecture → Look for architecture agents, or use `general` as "Backend Architect"
- Operations → Look for devops agents, or use `general` as "DevOps Specialist"

The available agents depend on your environment. Check what's available and select appropriately. The specialist profiles in [SPECIALISTS.md](references/SPECIALISTS.md) provide detailed personas you can apply to any agent type.

### Chair Responsibilities

**Before summoning:**
- Clarify the question scope
- Identify what domains need representation
- Ensure the question is answerable (not too vague)

**During analysis:**
- Give councillors full context (artifacts, code, constraints)
- Set expectations for thoroughness and source citation
- Specify if there are deadlines or constraints

**During synthesis:**
- Read each councillor file completely before synthesis
- Look for agreement, disagreement, and missing perspectives
- Identify where dissent is fundamental vs. resolvable

**During deliberation:**
- Be neutral - facilitate, don't dominate
- Focus on evidence, not opinions
- Help councillors find common ground
- Know when to stop deliberation (diminishing returns)

**After decision:**
- Clearly state the decision and rationale
- Acknowledge dissenting views if consensus wasn't reached
- Document what would change the decision (new evidence, etc.)

### Avoiding Chair Bias

As Chair, you may have opinions. To avoid biasing the council:
- Summon councillors BEFORE forming your own conclusion
- Don't signal expected outcomes in the initial brief
- Weigh all councillor analyses equally, even if they differ from your view
- If you have strong opinions, explicitly state them AFTER councillors have weighed in
- Consider summoning a Devil's Advocate to challenge your position

### Councillor Re-engagement

When a councillor's analysis is insufficient:

**Targeted follow-up:**
```
Please expand your analysis on [specific aspect]. Consider:
- [Missing perspective 1]
- [Missing perspective 2]
- Additional research on [gap identified]
```

**Re-summon with refined brief:**
Launch the councillor again with more specific context about what was missing

**Add a specialist:**
If the gap is a different domain, summon an additional specialist instead

### Quick Council Mode

For simpler decisions that still need multiple perspectives:

**When to use:**
- Question is straightforward but benefits from expert input
- Decision is reversible or low-stakes
- Time is constrained
- You need a sanity check, not deep analysis

**Streamlined workflow:**
1. Summon 2-3 specialists (use specialized agent types if available)
2. Each provides brief analysis using concise template
3. Chair synthesizes immediately (skip deliberation phase)
4. Decision rendered with brief rationale

**What stays the same:**
- Multiple perspectives
- Evidence-based analysis
- Source citations

**What's skipped:**
- Extensive deliberation
- Deep research
- Detailed debate

### Integration with Other Skills

Councillors can invoke any available skills to enhance their analysis. Instruct them explicitly:

```
As the [Domain] councillor, use the [skill-name] skill if available to conduct your analysis. Save your findings to your councillor file.
```

The Chair should mention relevant skills when summoning councillors if they would benefit the analysis.

### Voting Mechanism

When consensus cannot be reached and a decision must be made:

**Weighted voting:**
- Each councillor assigns a score (1-5) to each option
- Chair calculates weighted average
- Select highest-scoring option

**Domain-weighted voting:**
- Certain domains get more weight for specific decision types
- Example: Security decisions give security specialist 2x weight
- Example: Performance decisions give performance specialist 2x weight

**Document the voting method and outcome in CHAIR.md**

### Councillor Best Practices

**Research standards:**
- Always cite sources (URLs, Context7 queries, WebSearch terms)
- Use primary sources when possible
- Note the currency of information (docs can be stale)
- Acknowledge uncertainty and limitations

**Analysis quality:**
- Base conclusions on evidence, not assumptions
- Consider counter-arguments to your position
- Be explicit about confidence levels
- Use existing skills when relevant to domain

**Communication:**
- Write clearly and concisely
- Structure analysis for readability
- Lead with key findings
- Support claims with evidence

### Deliberation Facilitation

When councillors disagree:

**1-on-1 discussions:**
```
Facilitate discussion between [Specialist A] and [Specialist B] on:

Topic: [Specific point of disagreement]

Each councillor should:
- Present their evidence on this specific point
- Address the other's arguments directly
- Identify what evidence would change their mind

Goal: Find common ground or clearly articulate the difference
```

**Small group debates:**
```
Convene [Specialist A], [Specialist B], [Specialist C] for structured debate:

Topic: [Question with multiple perspectives]

Format:
1. Each presents position (2-3 points max)
2. Each responds to others' positions
3. Chair identifies convergence/divergence
4. Final statements on whether minds changed

Goal: Reach consensus OR map the disagreement landscape clearly
```

**Identify when to stop deliberation:**
- Councillors are repeating points without new evidence
- Dissent is due to fundamental values/trade-offs (not facts)
- Additional discussion time cost > clarity value
- Chair has enough information to make informed decision

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Councillors agree too quickly | Ask each to explicitly identify risks/downsides of their position |
| Analysis lacks sources | Require councillors to cite specific URLs, docs, or search queries |
| Conflicting recommendations | Identify the specific point of disagreement and facilitate targeted discussion |
| Analysis is too shallow | Ask councillor to conduct deeper research on specific aspects |
| Can't reach consensus | Present diverging views with evidence - consensus isn't always possible |
| Councillor goes beyond expertise | Gently redirect to their domain or summon additional specialist |
| Analysis is too long | Ask for executive summary with supporting details in appendix |

## Examples

### Example 1: Technical Decision

**Question:** Should we migrate from REST to GraphQL?

**Specialists summoned:**
- API design specialist
- Frontend performance expert
- Backend scalability engineer
- Security analyst
- Developer experience advocate

**Process:**
1. Each councillor analyzes from their perspective with research
2. Chair identifies consensus (GraphQL better for complex data needs)
3. Chair identifies dissent (security complexity, caching challenges)
4. Chair facilitates discussion between frontend perf and backend scalability
5. Decision: Conditional migration - use GraphQL for specific services, keep REST elsewhere

### Example 2: Code Review Council

**Question:** Is this PR ready to merge? [Complex authentication system]

**Specialists summoned:**
- Security reviewer (OWASP specialist)
- Performance engineer
- Test coverage analyst
- Documentation specialist

**Process:**
1. Each councillor reviews the code independently
2. Security councillor finds vulnerability (token storage)
3. Performance councillor identifies N+1 query issue
4. Test councillor notes missing edge case coverage
5. Chair synthesizes: Not ready to merge - 3 blockers identified

### Example 3: Architecture Trade-off

**Question:** Monolith vs. Microservices for our use case?

**Specialists summoned:**
- Distributed systems architect
- DevOps specialist
- Team organization expert
- Cost/complexity analyst

**Process:**
1. All councillors analyze with research
2. Strong dissent: architect advocates microservices, devOps specialist warns of complexity cost
3. Chair facilitates debate focused on team size and deployment patterns
4. Decision: Modular monolith now, extract microservices when justified by specific pain points

## Your Approach

1. **Start with clarity**: Ensure the question is well-defined before summoning
2. **Choose specialists deliberately**: Cover all relevant domains, avoid over-staffing
3. **Provide full context**: Give councillors everything they need (artifacts, constraints)
4. **Require evidence**: Insist on cited sources and research-backed analysis
5. **Listen before synthesis**: Read all councillor files completely before forming views
6. **Deliberate strategically**: Only facilitate discussions on meaningful disagreements
7. **Document decisions**: Clear rationale that acknowledges dissent when present
8. **Know when to stop**: Not all disagreements can be resolved - present diverging views clearly

## Async Council Mode

For situations where councillors need extended time or work across sessions:

### When to Use Async
- Complex research requiring multiple tool calls
- Councillors need to analyze large codebases
- Decision spans multiple user sessions
- Some councillors finish faster than others

### Async Workflow
```
1. SUMMON (Session 1)
   - Create .council/[session-id]/ with CONTEXT.md
   - Launch councillors with "save to file when complete" instruction
   - Councillors may finish in same session or later

2. CHECK PROGRESS (Any session)
   - List .council/[session-id]/ to see completed analyses
   - Re-summon any councillors that haven't completed
   - Add new councillors if gaps identified

3. SYNTHESIZE (When all complete)
   - Chair reads all councillor files
   - Proceeds with normal synthesis/deliberation
   - Decision rendered when ready
```

### Key Differences from Sync
- **No waiting**: Chair can continue other work while councillors analyze
- **Incremental progress**: Check completion status across sessions
- **Resilient**: Session interruptions don't lose councillor work (it's in files)

### Async Councillor Instructions
```
You are [Specialist] analyzing [question] for the council.

This is an async council session. Take the time needed to:
1. Conduct thorough research
2. Analyze all relevant artifacts
3. Save your complete analysis to .council/[session-id]/[name].md

The Chair will collect your analysis when ready. Quality over speed.
```

## Quick Reference

### Minimal Council Setup
```
1. mkdir -p .council/[session-id]/
2. Launch 3-5 specialist agents in parallel (Task tool)
3. Each writes analysis to .council/[session-id]/[name].md
4. Chair reads all files, writes CHAIR.md with decision
```

### Councillor One-Liner Prompt
```
You are [Specialist]. Analyze [question] from your domain perspective.
Research thoroughly using available tools, cite all sources.
Save your analysis to .council/[session-id]/[name].md
```

### Councillor Quality Checklist
Before accepting a councillor's analysis, verify:
- [ ] Sources cited (URLs, Context7 queries, search terms)
- [ ] Clear position stated (Support/Oppose/Conditional)
- [ ] Confidence level included with rationale
- [ ] Risks and downsides acknowledged
- [ ] Recommendations are specific and actionable
- [ ] Analysis saved to correct file path

### Council Size Guide
| Decision Type | Specialists | Notes |
|--------------|-------------|-------|
| Quick sanity check | 2-3 | Skip deliberation |
| Standard decision | 3-5 | Full workflow |
| Critical/irreversible | 5-7 | Add Devil's Advocate |

## Progressive Disclosure

**Deep dive on council mechanics:**
- **Session management**: [SESSIONS.md](references/SESSIONS.md)
- **Councillor templates**: [TEMPLATES.md](references/TEMPLATES.md)
- **Deliberation patterns**: [DELIBERATION.md](references/DELIBERATION.md)
- **Specialist profiles**: [SPECIALISTS.md](references/SPECIALISTS.md)
- **Decision frameworks**: [DECISIONS.md](references/DECISIONS.md)
