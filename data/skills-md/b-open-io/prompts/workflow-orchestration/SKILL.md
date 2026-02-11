---
name: workflow-orchestration
version: 1.0.0
description: This skill should be used when the user wants to orchestrate complex workflows using multiple subagents working in parallel. Use when breaking down large tasks into coordinated sub-tasks, managing parallel agent execution, or optimizing task completion time through parallelization.
---

# Workflow Orchestration

Orchestrate complex workflows by breaking them into parallel sub-tasks executed by specialized subagents, dramatically reducing completion time while maintaining quality.

## When to Use

- Complex multi-step tasks that can be decomposed
- Tasks requiring multiple domain expertise areas
- Time-sensitive operations needing parallel execution
- Work requiring research, implementation, testing, and documentation simultaneously
- Any task where "throwing more compute at it" via parallel agents makes sense

## Core Strategy

### 1. Task Decomposition

Break complex tasks into independent, parallel-executable subtasks:

**Example: Authentication System Implementation**

```
Sequential (5+ hours):
Research → Design → Code → Test → Document → Review

Parallel (1 hour):
├── research-specialist: OAuth 2.1 patterns research
├── auth-specialist: Core authentication implementation
├── test-specialist: Test suite creation
├── documentation-writer: API documentation
└── code-auditor: Security review
```

### 2. Agent Selection

Match subtasks to specialized agents:

| Task Type | Recommended Agent |
|-----------|------------------|
| Research | research-specialist |
| Authentication | auth-specialist |
| Security Review | code-auditor |
| API Integration | integration-expert |
| UI/UX Design | design-specialist |
| Documentation | documentation-writer |
| Testing | test-specialist |
| Architecture | architecture-reviewer |

### 3. Clear Boundaries

Define exactly what each agent should accomplish:

```markdown
## Agent Task Specification

**Agent**: research-specialist
**Task**: Research OAuth 2.1 PKCE flow
**Deliverable**: 
- Summary of PKCE benefits
- Code examples in TypeScript
- Security considerations
**Constraints**: Focus on browser-based flows only
```

## Implementation Pattern

### Step 1: Analyze and Decompose

```markdown
Original Task: "Build a complete SaaS billing system"

Decomposition:
1. Database schema design (db-specialist)
2. Stripe integration (payments-specialist)
3. Billing UI components (design-specialist)
4. Webhook handling (integration-expert)
5. Testing (test-specialist)
6. Documentation (documentation-writer)
```

### Step 2: Launch Parallel Agents

Use the Task tool to launch agents simultaneously:

```
Task 1: db-specialist - Design database schema
Task 2: payments-specialist - Set up Stripe integration
Task 3: design-specialist - Create billing UI components
Task 4: integration-expert - Implement webhooks
Task 5: test-specialist - Write test suite
Task 6: documentation-writer - Document the API
```

### Step 3: Coordinate Results

Collect all agent outputs and integrate:

```markdown
## Integration Checklist

- [ ] Database schema approved
- [ ] Stripe integration tested
- [ ] UI components match design system
- [ ] Webhooks properly secured
- [ ] Tests passing
- [ ] Documentation complete
```

## Best Practices

### DO
- Give each agent a single, focused task
- Provide detailed context in task descriptions
- Set clear deliverables and constraints
- Use 3-5 agents for most complex tasks
- Plan integration points before starting

### DON'T
- Overload one agent with multiple responsibilities
- Launch agents without clear deliverables
- Forget to plan how results will be integrated
- Use parallel execution for simple sequential tasks
- Skip the decomposition analysis phase

## Example Workflows

### Feature Implementation

```
Task: "Add user profiles with avatars"

Parallel:
├── design-specialist: Avatar upload UI
├── db-specialist: User profile schema
├── integration-expert: Image storage (S3/Cloudinary)
└── test-specialist: Profile update tests
```

### Security Audit

```
Task: "Audit authentication system"

Parallel:
├── code-auditor: Vulnerability scan
├── auth-specialist: Auth flow review
├── test-specialist: Penetration tests
└── documentation-writer: Security report
```

### Documentation Sprint

```
Task: "Document entire API"

Parallel:
├── documentation-writer: Endpoint docs
├── code-auditor: Code example verification
└── test-specialist: Test case documentation
```

## Error Handling

When a subagent fails:

1. **Retry**: Simple failures (timeouts, temporary errors)
2. **Reassign**: Task misalignment → different specialist
3. **Decompose further**: Task too large → break into smaller pieces
4. **Sequential fallback**: Dependencies discovered → reorder tasks

## Performance Tips

- **Agent Reuse**: Keep successful agents for related follow-up tasks
- **Context Preservation**: Pass key findings between related agents
- **Result Caching**: Store agent outputs for reuse in future tasks
- **Progress Tracking**: Monitor all agents' progress simultaneously

## Integration with Other Skills

- **reinforce-skills**: Persist workflow patterns to CLAUDE.md
- **critique**: Review parallel agent results for quality
- **confess**: Audit if parallel approach was optimal

## References

- [Parallel Agents Strategy](/references/development/parallel-agents.md)
- [Agent Collaboration Protocol](/references/development/collaboration-protocol.md)
- [Completion Reporting](/references/development/completion-reporting.md)
