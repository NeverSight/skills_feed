---
name: ralph-wiggum
description: Continuous iteration loop pattern for well-defined tasks with clear completion criteria. Use when getting tests to pass, implementing features with automatic verification, bug fixing with clear success conditions, or running automated development overnight. Provides prompt templates, safety guidelines, and integration patterns for ai-eng-system workflows.
version: 1.0.0
tags: [workflow, iteration, automation, continuous, looping]
---

# Ralph Wiggum Continuous Iteration

## Critical Importance

**Proper use of Ralph Wiggum loops is critical for achieving automated development success.** Poorly configured loops waste tokens, run forever without progress, or break your codebase. Well-configured loops enable autonomous development, overnight progress, and frictionless iteration. The loop's power comes from disciplined setup: clear completion criteria, safety caps, and verification mechanisms. Rushing loop setup guarantees cost overruns and broken builds.

## Systematic Approach

** approach Ralph Wiggum loops systematically.** Loop setup requires careful planning: define the task precisely, set verifiable success criteria, establish safety limits, and plan verification steps. Don't let loops run blindly—monitor progress, detect stuck states, and implement cancellation mechanisms. The loop is a tool, not a substitute for clear thinking. Configure it thoughtfully, monitor it actively, and trust it to handle the repetitive work.

## The Challenge

**The configure a loop that runs autonomously without getting stuck or burning excessive tokens, but if you can:**

- You'll unlock overnight productivity
- Features will complete while you sleep
- Test failures will disappear automatically
- You'll achieve continuous integration without babysitting

The challenge is setting completion criteria that are objective and achievable, while preventing infinite loops or token waste. Can you balance automation with safety?

## Loop Confidence Assessment

Before starting a Ralph Wiggum loop, rate your confidence from **0.0 to 1.0**:

- **0.8-1.0**: Task perfectly defined, completion criteria objective, safety measures in place, token budget acceptable
- **0.5-0.8**: Task clear but completion criteria somewhat fuzzy, reasonable safety measures, token usage unclear
- **0.2-0.5**: Task definition incomplete, completion criteria subjective, minimal safety measures, high token risk
- **0.0-0.2**: Task ambiguous, no objective success criteria, no safety caps, guaranteed problems

Identify uncertainty areas: Will the loop actually complete? What happens if it gets stuck? How many iterations will it need? What's the maximum token cost?

## Methodology

A while-loop pattern that keeps AI agents working on well-defined tasks until reaching a completion signal. Based on the proven technique from Claude Code community, adapted for ai-eng-system workflows.

## Core Philosophy

Ralph Wiggum embodies these principles:

1. **Iteration > Perfection** - Don't aim for perfect on first try. Let the loop handle refinement.
2. **Failures Are Data** - Deterministically bad failures are predictably informative. Feed them back into the next iteration.
3. **Operator Skill Matters** - Prompt quality determines success, not model capability. Write clear completion criteria.
4. **Persistence Wins** - Let the loop handle retry logic automatically. Walk away and let it work.

## When to Use Ralph Wiggum

### Ideal Scenarios ✅

Use Ralph Wiggum for well-defined tasks with clear, objective completion criteria:

- **TDD Implementation** - Write failing tests, loop until all tests pass
- **Bug Fixing** - Iteratively debug and fix until verification succeeds
- **Refactoring** - Incremental transformations with test safety
- **Feature Implementation** - Tasks with automatic verification (tests, linters, type checkers)
- **Quality Gate Passing** - Loop until code review, linting, or security scans pass
- **Overnight/Weekend Automation** - Run autonomous development while away
- **Greenfield Projects** - Complete features from scratch in one session

### When NOT to Use ❌

Avoid Ralph Wiggum for:

- **Tasks requiring human judgment** - Design decisions, UX choices, architectural trade-offs
- **Ambiguous tasks** - "Improve performance" (how much? what metric?)
- **One-shot operations** - Simple changes that don't need iteration
- **Tasks with external dependencies** - Needing approvals, manual configuration
- **Critical production systems** - Use manual control for safety
- **Long-running loops** - When context window limits would apply
- **Complex multi-phase workflows** - Use spec-driven workflow with explicit phase transitions instead

## Safety Measures

### Required Parameters

Always include these when using Ralph Wiggum loops:

1. **Max Iterations Cap** - Set 10-50 iterations based on complexity. Never run unlimited.
2. **Completion Promise** - Unique exact-match phrase like `<promise>COMPLETE</promise>` or `✅ ALL_TESTS_PASSING`
3. **Progress Monitoring** - Track iteration count and show last N outputs for visibility
4. **Cancellation Mechanism** - Ability to stop active loop and save iteration history

### Cost Management

- **Token Usage Tracking** - Monitor cumulative consumption throughout loop
- **Iteration Logging** - Save all outputs for post-mortem analysis
- **Stuck Detection** - Stop if no progress after 5-10 iterations
- **Context Window Management** - Prune irrelevant history between iterations

## Integration with ai-eng-system

Ralph Wiggum works as an **execution pattern** within ai-eng-system workflows:

```bash
# Direct agent invocation
@full-stack-developer "Implement authentication using TDD. Keep iterating until all tests pass. Output <promise>DONE</promise>."

# Within /work execution
/ai-eng/work "Implement user registration feature"

# In plan tasks:
tasks:
  - id: registration-feature
    agent: @full-stack-developer
    instruction: "Implement user registration using TDD. Output <promise>COMPLETE</promise> when all tests pass."
    loop:
      enabled: true
      max-iterations: 30
      completion-promise: "COMPLETE"
```

### Prompt Templates

See `templates/ralph-wiggum-prompts.md` for 5 detailed prompt templates:
1. TDD Implementation
2. Bug Fixing
3. Refactoring
4. Feature Implementation
5. Quality Gate Passing

Each template includes requirements, process steps, success criteria, and completion promises.

## Best Practices

### Prompt Writing

**Clear Completion Criteria**:
```markdown
Good:
Build a REST API for todos.
When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- README with API docs
- Output: <promise>COMPLETE</promise>

Bad:
Build a todo API and make it good.
```

**Incremental Goals**:
```markdown
Good:
Phase 1: User authentication (JWT, tests)
Phase 2: Product catalog (list/search, tests)
Phase 3: Shopping cart (add/remove, tests)
Output <promise>COMPLETE</promise> when all phases done.

Bad:
Create a complete e-commerce platform.
```

**Self-Correction Pattern**:
```markdown
Good:
Implement feature X following TDD:
1. Write failing tests
2. Implement feature
3. Run tests
4. If any fail, debug and fix
5. Refactor if needed
6. Repeat until all green
7. Output: <promise>COMPLETE</promise>

Bad:
Write code for feature X.
```

### Integration Patterns

#### Pattern 1: Single Agent Loop
```bash
# Simple iteration with one agent
@full-stack-developer "[TDD template above]"
```

#### Pattern 2: Multi-Agent Sequential
```bash
# Agent A creates implementation
@full-stack-developer "[Implementation template with COMPLETE promise]"

# Agent B reviews and iterates if needed
@code-reviewer "Review implementation. If issues found, output specific fixes needed. Output <promise>REVIEW_COMPLETE</promise> when code meets standards."

# Agent C adds tests if missing
@test-generator "Add tests for implementation until coverage > 80%. Output <promise>TESTS_COMPLETE</promise>."
```

#### Pattern 3: Git Worktree Parallel Loops
```bash
# See git-worktree skill for parallel development
git worktree add ../feature-auth -b feature/auth
git worktree add ../feature-api -b feature/api

# Loop 1: Authentication
cd ../feature-auth
@full-stack-developer "[Implementation template]"

# Loop 2: API (parallel execution)
cd ../feature-api
@api-builder-enhanced "[API implementation template]"
```

## Example Workflows

### Example 1: Getting Tests to Pass

**Scenario**: New feature tests are failing

```bash
# Use with @test-generator or @full-stack-developer
@full-stack-developer "Get all tests passing in src/auth.

Current Test Failures:
- ✗ auth.test.ts:45 - should validate JWT tokens
- ✗ auth.test.ts:78 - should reject expired tokens

Process:
1. Run failing test
2. Analyze error
3. Fix implementation
4. Re-run test
5. If still failing, analyze again
6. Repeat until all tests pass

Output <promise>ALL_TESTS_PASSING</promise> when done.

Keep iterating until auth.test.ts has all tests passing."
```

### Example 2: Complete Feature Implementation

**Scenario**: New user registration feature

```bash
# Use /ai-eng/work with loop instruction
/ai-eng/work "Implement user registration feature

Requirements:
- Email/password registration
- Password validation (min 8 chars, 1 uppercase, 1 number)
- Email verification token sent via email
- Password reset flow

Process:
[Use Template 4 above]

Integration with ai-eng-system:
- Use existing project patterns from CLAUDE.md
- Follow spec-driven workflow for planning
- Run /ai-eng/review after completion

Output <promise>COMPLETE</promise> when feature is ready."
```

### Example 3: Overnight Automation

**Scenario**: Run autonomous development while sleeping

```bash
# Set up with max-iterations for safety
@full-stack-developer "Implement complete CRUD API for products.

[Full template with detailed requirements]

Keep iterating until complete. This is an overnight automated run.

Safety Parameters:
- Max iterations: 50
- Checkpoint every 10 iterations
- Save progress to .checkpoint.json

Output <promise>OVERNIGHT_COMPLETE</promise> when done."
```

## Monitoring and Debugging

### Checking Loop Progress

Monitor active loops by tracking:
- **Iteration count** - How many iterations have run?
- **Recent outputs** - What happened in the last 3-5 iterations?
- **Stuck patterns** - Is the agent repeating the same approach?
- **Convergence** - Are results improving or cycling?

### Stuck Loop Detection

**Signs of stuck loops**: Same tests failing after 5+ iterations, repeated outputs, error cycling

**Rescue strategy**:
```markdown
If stuck after 5 iterations without progress:
1. Document what's not working
2. List all attempted approaches
3. Propose a different strategy
4. Output <promise>STUCK_REPORT</promise> with details
```

## Anti-Patterns to Avoid

- **Unlimited loops** - Always set max-iterations cap
- **Vague completion criteria** - Must be objectively verifiable
- **Ignoring context window** - Long loops can exceed token limits
- **Missing test safety** - Without tests, loops can break functionality
- **No progress visibility** - Don't run blind - monitor iterations
- **Overly complex single loop** - Break into multiple smaller loops
- **Skipping verification** - Always run tests/checks after each iteration
- **Ignoring cost** - Token usage accumulates quickly

## Quality Checklist

Before starting a Ralph Wiggum loop:

- [ ] Task has clear, objective success criteria
- [ ] Max-iterations cap is set (recommended: 10-50)
- [ ] Completion promise is unique and verifiable
- [ ] Tests or verification mechanism exists
- [ ] Task is well-defined, not requiring judgment
- [ ] Safety measures (stuck detection, cancellation) in place
- [ ] Token usage is acceptable for estimated iterations
- [ ] Appropriate agent is chosen for the task

## Integration with Spec-Driven Workflow

Ralph Wiggum enhances the `/ai-eng/work` phase:

```bash
/ai-eng/research "authentication patterns"
/ai-eng/specify "user authentication"
/ai-eng/plan --from-spec=specs/auth
/ai-eng/work "specs/auth/plan"  # Use Ralph Wiggum patterns here
/ai-eng/review
```

In `/ai-eng/work`, use Ralph Wiggum for:
- Getting tests to pass
- Implementing features with TDD
- Refactoring with test safety
- Passing quality gates

## Research-Based Foundations

- **Ralph Wiggum Pattern** - Original technique by Geoffrey Huntley
- **Claude Code Community Results** - Y Combinator Hackathon (6 repos overnight), $50k contract ($297 API costs), CURSED Language (3 months)
- **ai-eng-system Integration Research** - docs/research/2025-01-05-ralph-wiggum-loop-analysis.md

## Follow-Up Actions

After loop completes:
1. **Verify results** - Confirm completion criteria met
2. **Run comprehensive tests** - Full test suite, integration tests
3. **Code review** - Use `/ai-eng/review` for validation
4. **Document iteration history** - Save notable decisions and approaches
5. **Commit changes** - Clean commits with descriptive messages
6. **Update documentation** - Reflect changes in relevant docs

## External References

- [Awesome Claude - Ralph Wiggum](https://awesomeclaude.ai/ralph-wiggum) - Official documentation
- [Geoffrey Huntley's Blog](https://ghuntley.com/ralph/) - Original technique creator
- [Ralph Orchestrator](https://github.com/mikeyobrien/ralph-orchestrator) - Community management tool
