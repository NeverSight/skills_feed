---
name: parallel-code-review
description: This skill should be used when performing comprehensive code reviews using multiple specialized review agents in parallel. It provides patterns for concurrent execution, decision tracking to prevent redundancy, and consolidated reporting. Use when needing thorough review coverage from multiple perspectives (security, architecture, performance) or when reviewing large changesets.
---

# Parallel Code Review

This skill provides guidance for launching multiple specialized code review agents in parallel for comprehensive, efficient analysis from different perspectives.

## Purpose

Parallel code reviews maximize efficiency and coverage by running multiple specialized reviewers simultaneously. Instead of sequential reviews that take time proportional to the number of reviewers, parallel execution completes in the time of the slowest reviewer while providing comprehensive feedback from all perspectives.

## When to Use This Skill

Use this skill when:
- Performing comprehensive code review before merging
- Need multiple specialized perspectives (security, architecture, performance)
- Want faster review by parallelizing analysis
- Reviewing large changesets that benefit from division of labor
- Implementing continuous review practices

## Benefits of Parallel Reviews

**Speed:** 2+ specialized reviews complete in the time of 1
**Depth:** Each agent focuses on specific expertise area
**Comprehensive Coverage:** Security + Architecture + Performance simultaneously

## Core Workflow

### Phase 1: Prepare for Review

**1. Check Decision Log (Prevent Redundancy)**

```bash
# Search memory for previous code review decisions
mcp__memory__search_nodes query:"code_review_decision"

# Read decision log file
cat code_review_decisions.md
```

**Decision log format:**
```markdown
# Code Review Decisions

## 2025-01-15: Result Pattern Required

**Decision**: All service objects must return Result objects
**Rationale**: Explicit success/failure handling improves error management
**Status**: Accepted standard pattern
```

**2. Get Code Changes**

```bash
# Get diff for review
git diff main...HEAD

# Or specific branch
git diff main...feature-branch
```

### Phase 2: Launch Parallel Reviewers

**Use Task tool to launch multiple agents concurrently:**

Example: Launch 2 reviewers in parallel by sending a SINGLE message with MULTIPLE Task tool calls:

```javascript
Task({
  subagent_type: "cybersecurity-expert",
  description: "Security review of changes",
  prompt: "Review git diff for security vulnerabilities..."
})

Task({
  subagent_type: "rails-backend-expert",
  description: "Architecture review of changes",
  prompt: "Review git diff for code quality..."
})
```

**Key principle:** One message with multiple tool calls = true parallelism

### Phase 3: Define Review Specializations

#### Security Review Agent

**Focus areas:**
- Authentication and authorization vulnerabilities
- Input validation and injection attacks
- Sensitive data exposure
- Cryptographic weaknesses
- Access control flaws
- Rate limiting and DoS prevention

#### Architecture/Best Practices Review Agent

**Focus areas:**
- Design patterns (SOLID, DRY, KISS)
- Framework conventions
- Code organization
- Dependency management
- Error handling patterns
- Test quality

#### Performance Review Agent (Optional)

**Focus areas:**
- Database query optimization (N+1, missing indexes)
- Memory usage patterns
- Algorithmic complexity
- Caching opportunities

### Phase 4: Consolidate Findings

**1. Collect agent outputs**

Wait for all parallel agents to complete.

**2. Merge and deduplicate**

If multiple agents flag the same issue, consolidate into single item and credit all reviewers.

**3. Organize by severity**

**Priority hierarchy:**
- **Critical**: Security vulnerabilities, data loss risks
- **High**: Major code smells, performance issues
- **Medium**: Minor refactoring opportunities
- **Low**: Suggestions, nice-to-haves

**4. Create consolidated report**

```markdown
# Code Review - PR #123

## Executive Summary
Reviewed 15 files with 342 lines changed. Found 2 critical issues, 5 high priority items.

## Critical Issues (Immediate Action Required)

### 1. SQL Injection Vulnerability
- **File**: app/services/search_service.rb:23
- **Reviewers**: Security, Architecture
- **Action**: Use parameterized queries immediately

## High Priority
[...]

## Positive Observations
- Good test coverage
- Clear naming conventions

## Recommended Action Plan
1. **Before merge**: Fix critical SQL injection (15 min)
2. **This sprint**: Address high priority refactoring (2 hours)
```

### Phase 5: Decision Tracking

Update decision log for new patterns:

```markdown
## 2025-01-20: Parameterized Queries Required

**Decision**: All database queries must use parameterized queries
**Rationale**: Prevent SQL injection vulnerabilities
**Status**: Enforced
**Reference**: Security review PR #123
```

Add to memory system:

```javascript
mcp__memory__create_entities({
  entities: [{
    name: "Parameterized Queries Required",
    entityType: "code_review_decision",
    observations: [
      "All database queries must use parameterized queries",
      "Decided during PR #123 security review"
    ]
  }]
})
```

## Review Configurations

### Two-Agent Review (Common)

```
Agent 1: Security Focus
Agent 2: Architecture/Quality Focus

Best for: Most code reviews, balanced coverage
```

### Three-Agent Review (Comprehensive)

```
Agent 1: Security
Agent 2: Architecture
Agent 3: Performance

Best for: Large features, production-critical code
```

### Four-Agent Review (Full Coverage)

```
Agent 1: Security
Agent 2: Architecture
Agent 3: Performance
Agent 4: Testing/Documentation

Best for: Major releases, API changes
```

## Framework Adaptations

### Ruby on Rails

**Specialized Agents:**
- Security: Rails-specific vulnerabilities (mass assignment, CSRF)
- Architecture: Rails conventions, service objects, Result pattern
- Performance: ActiveRecord optimization, caching

### Python/Django

**Specialized Agents:**
- Security: Django security middleware, SQL injection, XSS
- Architecture: Django patterns, class-based views
- Performance: ORM query optimization

### JavaScript/Node.js

**Specialized Agents:**
- Security: npm vulnerabilities, prototype pollution
- Architecture: Module patterns, async/await
- Performance: Event loop blocking, memory leaks

## Best Practices

### Preventing Review Fatigue

Decision tracking prevents:
- Repeated suggestions for accepted patterns
- Debates over settled conventions
- Wasted time on known trade-offs

### Effective Agent Prompts

**Good prompt structure:**
```
[Role]: You are a [security/architecture] expert
[Context]: Reviewing code diff for [feature]
[Scope]: Focus on: [specific areas]
[Constraints]: Respect decisions in code_review_decisions.md
[Output]: Return findings with file:line, severity, recommendations
```

### Consolidation Strategy

**Remove duplicates:** Consolidate identical findings from multiple agents
**Prioritize by impact:** Security > user-facing bugs > refactoring
**Balance feedback:** Include positive observations

## Summary

Parallel code review maximizes efficiency and coverage:
- ✅ Multiple specialized perspectives simultaneously
- ✅ Faster review through parallelization
- ✅ Decision tracking prevents redundancy
- ✅ Consolidated reporting for actionable feedback
- ✅ Adaptable to any language or framework

**Key workflow:**
Check decision log → Launch parallel agents → Consolidate findings → Report with priorities → Update decision log

The goal is comprehensive coverage with minimal redundancy. Let each agent focus on their specialty, then synthesize insights into actionable, prioritized feedback.
