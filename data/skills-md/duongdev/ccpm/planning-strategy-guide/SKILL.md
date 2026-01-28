---
name: planning-strategy-guide
description: Guides intelligent planning strategies with automatic phase detection and complexity assessment. Auto-activates when users mention epic breakdown, feature decomposition, scope estimation, dependency analysis, risk identification, or ask "how do I plan this complex task", "break down this feature", "what's the scope", "estimate effort", "identify dependencies", or "planning strategy". Provides interactive planning mode with 6 planning phases (complexity assessment, scope definition, dependency analysis, risk identification, task breakdown, effort estimation). Works with sequential-thinking for complex decomposition, docs-seeker for research, pm-workflow-guide for command suggestions, and linear-subagent-guide for Linear integration.
---

# Planning Strategy Guide

Expert planning assistant that helps you decompose complex tasks, assess complexity, identify dependencies, and create comprehensive implementation plans.

## When to Use

This skill auto-activates when:

- **Epic breakdown**: "Break down this epic into tasks"
- **Feature decomposition**: "How do I plan this complex feature?"
- **Scope estimation**: "What's the scope of this work?"
- **Complexity assessment**: "How complex is this task?"
- **Dependency analysis**: "What are the dependencies?"
- **Risk identification**: "What risks should I consider?"
- **Planning strategy**: "Help me structure this project"
- **Effort estimation**: "I need to estimate effort for this"

## Planning Phases

This skill guides you through **6 planning phases** for comprehensive task decomposition:

### Phase 1: Complexity Assessment

**Purpose**: Evaluate task complexity to determine planning approach

**Complexity Rubric**:
- **Simple** (1-2 files, clear scope)
  - Single component modification
  - Well-defined requirements
  - No external dependencies
  - Estimated: 1-4 hours

- **Medium** (3-8 files, some unknowns)
  - Multiple component changes
  - Some research needed
  - Few external dependencies
  - Estimated: 1-3 days

- **Complex** (9+ files, research needed, multiple systems)
  - Cross-system changes
  - Significant research required
  - Many dependencies and integrations
  - Estimated: 4+ days

**Questions to ask**:
1. How many files will be modified?
2. Are requirements fully understood?
3. Are there external system integrations?
4. How much research is needed?

### Phase 2: Scope Definition

**Purpose**: Clearly define boundaries and deliverables

**Key elements**:
- **In scope**: What will be implemented
- **Out of scope**: What will NOT be implemented
- **Acceptance criteria**: How to verify completion
- **Success metrics**: How to measure success

**Questions to ask**:
1. What is the minimal viable implementation?
2. What features can be deferred?
3. What defines "done"?
4. What are the acceptance criteria?

### Phase 3: Dependency Analysis

**Purpose**: Identify dependencies and proper execution order

**Dependency types**:
- **Hard dependencies**: Must complete A before B
- **Soft dependencies**: Prefer A before B, but not required
- **Parallel work**: Can execute simultaneously
- **Blocking dependencies**: External dependencies not in your control

**Questions to ask**:
1. What must be completed first?
2. What can run in parallel?
3. Are there external blockers?
4. What's the critical path?

### Phase 4: Risk Identification

**Purpose**: Identify potential challenges and mitigation strategies

**Common risk categories**:
- **Technical risks**: Unknown technologies, complex algorithms
- **Integration risks**: Third-party APIs, external systems
- **Performance risks**: Scalability, response time
- **Security risks**: Authentication, data protection
- **Timeline risks**: Underestimated effort, scope creep

**For each risk**:
- **Likelihood**: Low/Medium/High
- **Impact**: Low/Medium/High
- **Mitigation**: How to reduce or eliminate
- **Contingency**: Plan B if it occurs

### Phase 5: Task Breakdown

**Purpose**: Decompose feature into actionable subtasks

**Breakdown principles**:
- **Atomic**: Each task is a single, focused unit
- **Testable**: Each task has clear verification
- **Estimable**: Can reasonably estimate effort
- **Independent**: Minimal coupling between tasks
- **Ordered**: Logical execution sequence

**Example breakdown**:
```
Epic: User Authentication
├── Feature: Login Flow
│   ├── Task: Create login API endpoint
│   ├── Task: Add JWT token generation
│   ├── Task: Implement password validation
│   └── Task: Add login UI form
├── Feature: Session Management
│   ├── Task: Add token refresh logic
│   └── Task: Handle session expiration
└── Feature: Security
    ├── Task: Add rate limiting
    └── Task: Implement 2FA support
```

### Phase 6: Effort Estimation

**Purpose**: Estimate time and resources needed

**Estimation approaches**:
1. **T-shirt sizing**: XS/S/M/L/XL (relative sizing)
2. **Story points**: Fibonacci sequence (1, 2, 3, 5, 8, 13)
3. **Time-based**: Hours or days (absolute sizing)

**Factors to consider**:
- **Complexity**: How technically challenging
- **Uncertainty**: How much is unknown
- **Dependencies**: How many blockers
- **Experience**: Team familiarity with domain

**Buffer rule**: Add 20-30% buffer for unknowns

## Integration with CCPM

### Commands that Activate This Skill

This skill enhances the following CCPM commands:

1. **`/ccpm:plan`** - Smart planning with phase detection
   - Detects complexity automatically
   - Suggests appropriate planning depth
   - Provides interactive guidance

2. **`/ccpm:plan`** - Extended planning with research
   - Activates all 6 planning phases
   - Integrates with docs-seeker for research
   - Creates comprehensive Linear issue

3. **`/ccpm:plan`** - Plan modifications
   - Analyzes impact of changes
   - Re-evaluates complexity and scope
   - Provides side-by-side comparison

4. **`/ccpm:plan`** - Spec-first development
   - Helps structure spec sections
   - Identifies missing requirements
   - Ensures comprehensive coverage

5. **`/ccpm:plan`** - Epic/feature decomposition
   - Uses task breakdown phase
   - Analyzes dependencies
   - Creates properly ordered subtasks

### Skills that Work Alongside

This skill integrates with:

1. **sequential-thinking** - For complex task decomposition
   - Uses iterative reasoning
   - Explores alternative approaches
   - Shows thought process

2. **docs-seeker** - For research during planning
   - Finds relevant documentation
   - Provides code examples
   - Flags important caveats

3. **pm-workflow-guide** - For command recommendations
   - Suggests next actions
   - Shows workflow state
   - Prevents common mistakes

4. **linear-subagent-guide** - For updating Linear
   - Optimizes Linear operations
   - Uses caching effectively
   - Structures updates properly

5. **external-system-safety** - For Jira/Confluence reads
   - Confirms external writes
   - Shows exact content
   - Maintains audit trail

6. **workflow-state-tracking** - For state transitions
   - Visualizes workflow state
   - Validates transitions
   - Suggests next phase

## Instructions

### Step 1: Detect Planning Need

When user mentions planning-related keywords, activate and assess their need:

```
User: "I need to plan this complex payment integration"
       ↓
[planning-strategy-guide activates]
       ↓
Assess: Type of planning needed (epic breakdown? complexity assessment?)
```

### Step 2: Ask Clarifying Questions

Use AskUserQuestion to gather context:

```javascript
AskUserQuestion({
  questions: [{
    question: "What type of planning assistance do you need?",
    header: "Planning Type",
    multiSelect: false,
    options: [
      {
        label: "Break down large feature",
        description: "Decompose epic/feature into tasks"
      },
      {
        label: "Assess complexity",
        description: "Evaluate technical complexity and effort"
      },
      {
        label: "Identify dependencies",
        description: "Map task dependencies and order"
      },
      {
        label: "Analyze risks",
        description: "Identify potential challenges"
      }
    ]
  }]
});
```

### Step 3: Run Appropriate Planning Phases

Based on user's selection, run relevant phases:

**For epic breakdown**:
1. Run Phase 1 (Complexity Assessment)
2. Run Phase 5 (Task Breakdown)
3. Run Phase 3 (Dependency Analysis)
4. Run Phase 6 (Effort Estimation)

**For complexity assessment**:
1. Run Phase 1 (Complexity Assessment)
2. Run Phase 4 (Risk Identification)
3. Run Phase 6 (Effort Estimation)

**For scope definition**:
1. Run Phase 2 (Scope Definition)
2. Run Phase 1 (Complexity Assessment)
3. Run Phase 6 (Effort Estimation)

### Step 4: Integrate with Other Skills

Based on complexity, invoke complementary skills:

**Complex tasks** → Invoke sequential-thinking:
```
Task(sequential-thinking): "Break down this complex payment integration..."
```

**Research needed** → Invoke docs-seeker:
```
Skill: docs-seeker
Query: "Find Stripe API documentation and best practices"
```

**Command suggestion needed** → Let pm-workflow-guide activate:
```
[pm-workflow-guide auto-activates]
Suggests: "/ccpm:plan epic 'Payment Integration'"
```

### Step 5: Update Linear with Plan

Use linear-subagent-guide patterns:

```yaml
Task(ccpm:linear-operations): `
operation: update_issue_description
params:
  issueId: "${issueId}"
  description: |
    ## Implementation Checklist

    ${generatedChecklist}

    > **Complexity**: ${complexity} | **Estimated**: ${estimate}

    ## Dependencies

    ${dependencyList}

    ## Risks & Mitigation

    ${risksList}

    ---

    ${originalDescription}
context:
  command: "planning-strategy-guide"
  cache: true
`
```

### Step 6: Provide Next Actions

Show user what to do next:

```
✅ Planning Complete!

📊 Results:
  • Complexity: Medium
  • Tasks: 8 subtasks identified
  • Dependencies: 3 hard dependencies
  • Risks: 2 medium risks identified
  • Estimate: 2-3 days

💡 Next Steps:
  1. Review the plan in Linear
  2. Start implementation: /ccpm:work ${issueId}
  3. Create spec if complex: /ccpm:plan
```

## Examples

### Example 1: Complex Feature Breakdown

```
User: "Help me plan this payment gateway integration"

Claude: [planning-strategy-guide activates]

I'll help you plan the payment gateway integration. Let me start by assessing the complexity.

[Asks clarifying questions via AskUserQuestion]

Based on your answers, this is a **Complex** task (9+ files, external API integration).

Let me run the 6 planning phases:

**Phase 1: Complexity Assessment**
- External API integration (Stripe)
- Security considerations (PCI compliance)
- Multiple payment methods
- Webhook handling
→ Complexity: High

**Phase 2: Scope Definition**
In scope:
  • Credit card payments
  • Stripe integration
  • Basic webhook handling
Out of scope:
  • PayPal integration (defer to Phase 2)
  • Subscription management (defer)

**Phase 3: Dependency Analysis**
Hard dependencies:
  1. Stripe account setup (external)
  2. Security review approval (external)
  3. Database schema for payments

Parallel work:
  • Frontend payment form
  • Backend API endpoints
  • Webhook handlers

**Phase 4: Risk Identification**
1. **PCI Compliance** (High impact, Medium likelihood)
   - Mitigation: Use Stripe.js (no card data touches server)

2. **Webhook reliability** (Medium impact, Medium likelihood)
   - Mitigation: Implement idempotency keys

3. **API rate limits** (Low impact, Low likelihood)
   - Mitigation: Add exponential backoff

**Phase 5: Task Breakdown**
Epic: Payment Gateway Integration
├── Set up Stripe account and API keys
├── Implement payment API endpoints
│   ├── Create payment intent endpoint
│   ├── Confirm payment endpoint
│   └── Refund payment endpoint
├── Build frontend payment form
│   ├── Integrate Stripe.js
│   ├── Add card input component
│   └── Handle payment errors
├── Add webhook handlers
│   ├── payment_intent.succeeded
│   ├── payment_intent.failed
│   └── refund.updated
├── Add database schema
│   ├── payments table
│   └── payment_events table
├── Write tests
│   ├── API endpoint tests
│   ├── Webhook handler tests
│   └── Integration tests
└── Security review

**Phase 6: Effort Estimation**
- Total: 12 tasks
- Estimate: 5-7 days (with 20% buffer)
- Story points: 21 points

✅ Planning complete! Would you like me to:
1. Create Linear issue with this plan: /ccpm:plan
2. Create spec document: /ccpm:plan
3. Start implementation: /ccpm:work
```

### Example 2: Simple Task Complexity Assessment

```
User: "How complex is adding a logout button?"

Claude: [planning-strategy-guide activates - lightweight mode]

Let me assess the complexity:

**Phase 1: Complexity Assessment**
- Files to modify: 2 (logout button component, API endpoint)
- Clear requirements: Yes
- External dependencies: None
- Research needed: Minimal

→ **Complexity: Simple** (1-2 hours)

**Quick Plan**:
1. Add logout button to UI (30 min)
2. Call logout API endpoint (15 min)
3. Clear session/cookies (15 min)
4. Test (30 min)

**Estimate**: 1-2 hours

Since this is simple, you can start immediately:
/ccpm:plan "Add logout button"
```

### Example 3: Dependency Analysis for Parallel Work

```
User: "What order should I implement these features?"

Claude: [planning-strategy-guide activates - Phase 3]

Let me analyze the dependencies:

**Phase 3: Dependency Analysis**

Your features:
1. User authentication
2. Profile page
3. Settings page
4. Admin dashboard

Dependency graph:
```
┌─────────────────┐
│ Authentication  │ (Must be first)
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    │         │            │
┌───▼──┐  ┌───▼──┐  ┌─────▼──────┐
│Profile│  │Settings│ │Admin Dash│
└──────┘  └────────┘ └────────────┘
    (parallel work possible)
```

**Execution order**:
1. **First**: Implement authentication (blocker for all others)
2. **Then in parallel**:
   - Profile page (Team A)
   - Settings page (Team B)
   - Admin dashboard (Team C)

**Critical path**: Authentication → Any feature (all equal)

**Recommendation**:
- Start with: /ccpm:plan "User authentication"
- After auth done, all 3 can proceed in parallel
```

### Example 4: Risk Identification

```
User: "What could go wrong with this API migration?"

Claude: [planning-strategy-guide activates - Phase 4]

Let me identify risks for your API migration:

**Phase 4: Risk Identification**

**1. Breaking Changes** (High impact, High likelihood)
- Impact: Existing clients break
- Mitigation:
  • Implement API versioning (/v1, /v2)
  • Maintain backward compatibility
  • Provide migration guide
- Contingency: Rollback plan with feature flags

**2. Data Migration Issues** (High impact, Medium likelihood)
- Impact: Data loss or corruption
- Mitigation:
  • Test migration on staging
  • Backup all data before migration
  • Implement migration rollback scripts
- Contingency: Restore from backup

**3. Performance Degradation** (Medium impact, Medium likelihood)
- Impact: Slower API responses
- Mitigation:
  • Load test new API
  • Add caching layer
  • Optimize database queries
- Contingency: Scale infrastructure

**4. Third-party Dependencies** (Low impact, High likelihood)
- Impact: New libraries have bugs
- Mitigation:
  • Use stable versions
  • Test thoroughly
  • Have alternative libraries ready
- Contingency: Fall back to old implementation

**Recommendation**:
Create detailed migration plan with /ccpm:plan
Include rollback procedures and monitoring
```

### Example 5: Effort Estimation with T-Shirt Sizing

```
User: "Estimate effort for these 5 tasks"

Claude: [planning-strategy-guide activates - Phase 6]

**Phase 6: Effort Estimation**

Using T-shirt sizing:

| Task | Size | Effort | Reasoning |
|------|------|--------|-----------|
| Add search bar | **XS** | 1-2h | Simple UI component |
| Implement search API | **S** | 4-6h | Straightforward endpoint |
| Add search filters | **M** | 1-2d | Multiple filter types |
| Full-text search (Elasticsearch) | **L** | 3-5d | New tech, complex setup |
| Search analytics | **M** | 1-2d | Logging + dashboard |

**Total estimate**: 6-10 days (with 20% buffer: 7-12 days)

**Story points breakdown**:
- XS: 1 point → 1 point
- S: 2 points → 2 points
- M: 5 points → 10 points
- L: 8 points → 8 points

**Total**: 21 story points

**Recommendation**:
- Sprint 1: Search bar + API (3 points)
- Sprint 2: Filters + Analytics (10 points)
- Sprint 3: Elasticsearch (8 points)

Would you like me to create tasks in Linear?
/ccpm:plan (will break down into subtasks)
```

## Best Practices

### 1. Always Start with Complexity Assessment

Don't dive into detailed planning without understanding complexity:

❌ **Bad**: Immediately create 20 subtasks without assessment
✅ **Good**: Assess complexity first, then plan depth accordingly

### 2. Use Progressive Disclosure

Match planning depth to task complexity:

- **Simple tasks**: Quick assessment (Phase 1 + estimate)
- **Medium tasks**: Moderate planning (Phases 1, 2, 5, 6)
- **Complex tasks**: Full planning (All 6 phases)

### 3. Iterate and Refine

Planning is not one-and-done:

```
Initial plan → Implementation → Learning → Update plan
```

Use `/ccpm:plan` to refine plans based on learnings.

### 4. Document Assumptions

Make assumptions explicit:

```
**Assumptions**:
- Stripe API is stable (confirmed with docs)
- PCI compliance handled by Stripe.js (verified)
- Payment volume < 1000/day (confirmed with product)
```

### 5. Consider Multiple Approaches

For complex tasks, evaluate alternatives:

```
**Approach A: Use Stripe**
Pros: Well-documented, PCI compliant
Cons: Monthly fees, vendor lock-in

**Approach B: Use PayPal**
Pros: Wider adoption, familiar to users
Cons: Complex API, less flexible

**Recommendation**: Approach A (Stripe)
Rationale: Better developer experience, clearer documentation
```

### 6. Involve Stakeholders Early

For scope definition, ask:
- Product: What's the MVP?
- Design: What's the UX flow?
- Security: What are the requirements?
- DevOps: What's the deployment strategy?

### 7. Plan for Failure

Always include:
- Error handling tasks
- Monitoring and alerting
- Rollback procedures
- Testing edge cases

### 8. Use Visual Aids

Dependency graphs, workflow diagrams, and architecture sketches help:

```
[User] → [Frontend] → [API Gateway] → [Payment Service] → [Stripe]
                                            ↓
                                      [Database]
                                            ↓
                                      [Webhook Handler]
```

## Common Patterns

### Pattern 1: Epic Breakdown Strategy

**When**: Large feature spanning multiple sprints

**Phases to use**: 1, 2, 3, 5, 6

**Output**: Hierarchical task structure in Linear

**Integration**:
- Use `/ccpm:plan epic` first (create spec)
- Then `/ccpm:plan` (use this skill's Phase 5)

### Pattern 2: Complexity-First Planning

**When**: Unsure how complex a task is

**Phases to use**: 1, 4, 6

**Output**: Complexity rating + estimate + risks

**Integration**:
- Use `/ccpm:plan` (quick assessment)
- If complex → Invoke sequential-thinking

### Pattern 3: Dependency-Driven Planning

**When**: Multiple interconnected tasks

**Phases to use**: 3, 5

**Output**: Dependency graph + execution order

**Integration**:
- Use `/ccpm:work` (visualize)
- Create tasks in dependency order

### Pattern 4: Risk-Aware Planning

**When**: High-stakes or unfamiliar territory

**Phases to use**: 1, 4

**Output**: Risk register + mitigation strategies

**Integration**:
- Document in spec: `/ccpm:plan <doc-id> security`
- Add risks to Linear issue description

## Summary

The Planning Strategy Guide is your intelligent planning assistant, providing:

✅ **6 comprehensive planning phases** for thorough task analysis
✅ **Complexity assessment** to match planning depth to task needs
✅ **Dependency analysis** to identify proper execution order
✅ **Risk identification** to anticipate and mitigate challenges
✅ **Task breakdown** to create actionable, testable subtasks
✅ **Effort estimation** with multiple approaches (t-shirt, story points, time)

### Philosophy

**Plan smart, not hard**: Match planning depth to task complexity. Simple tasks get quick assessments, complex tasks get comprehensive analysis.

**Iterate and refine**: Planning is continuous. Use learnings from implementation to update plans.

**Integrate seamlessly**: Works alongside sequential-thinking, docs-seeker, pm-workflow-guide, and other CCPM skills.

**Stay practical**: Focus on actionable outputs that help you start coding, not just documentation.

### Quick Reference

**For quick complexity check**:
- "How complex is this task?"
- Auto-runs Phase 1 (Complexity Assessment)

**For epic breakdown**:
- "Break down this feature"
- Auto-runs Phases 1, 3, 5 (Assessment, Dependencies, Breakdown)

**For comprehensive planning**:
- "Plan this complex feature"
- Auto-runs all 6 phases

**Integration commands**:
- `/ccpm:plan` - Smart planning (uses this skill)
- `/ccpm:plan` - Spec-first (uses Phase 2, 5)
- `/ccpm:plan` - Refine plan (re-runs relevant phases)

---

**Remember**: Good planning makes implementation smooth. Take time to plan well, then execute confidently.
