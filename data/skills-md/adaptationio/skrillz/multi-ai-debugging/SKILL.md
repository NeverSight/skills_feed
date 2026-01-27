---
name: multi-ai-debugging
description: Systematic debugging using Claude, Gemini, and Codex as specialized agents. Multi-agent root cause analysis, log analysis, error classification, and auto-fix generation. Use when debugging production issues, analyzing error logs, performing root cause analysis, troubleshooting complex systems, or implementing self-healing patterns.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Debugging

## Overview

multi-ai-debugging provides systematic debugging workflows using multiple AI models as specialized agents. Based on 2024-2025 best practices for AI-assisted debugging with multi-agent architectures.

**Purpose**: Systematic root cause analysis and fix generation using AI ensemble

**Pattern**: Task-based (6 independent debugging operations)

**Key Principles** (validated by tri-AI research):
1. **Multi-Agent Council** - Specialized agents debate root causes before consensus
2. **Evaluator/Critic Loops** - Fix agent + critic agent verify solutions
3. **Trace-Aware Analysis** - Full execution context, not just error messages
4. **Semantic Log Analysis** - LLM understanding beyond regex matching
5. **Cross-Stack Correlation** - Connect frontend, backend, infra issues
6. **Auto-Remediation** - Self-healing patterns where safe

**Quality Targets**:
- Root Cause Identification: >80% accuracy
- Time to Diagnosis: <30 minutes for common issues
- Fix Generation Success: >60% for known patterns
- False Positive Rate: <20% on error classification

---

## When to Use

Use multi-ai-debugging when:

- Debugging production incidents
- Analyzing error logs and stack traces
- Performing root cause analysis (RCA)
- Troubleshooting complex multi-service systems
- Investigating performance degradation
- Understanding cascading failures
- Writing post-mortem reports

**When NOT to Use**:
- Simple syntax errors (IDE handles these)
- Clear compile-time errors
- Well-documented known issues

---

## Prerequisites

### Required
- Error information (logs, stack trace, error message)
- Access to relevant code

### Recommended
- Execution traces (if available)
- System metrics/observability data
- Recent change history (git log)
- Gemini CLI for web research
- Codex CLI for deep code analysis

### Integration
- OpenTelemetry traces (ideal)
- Log aggregation (CloudWatch, Datadog, etc.)
- APM tools (optional)

---

## Operations

### Operation 1: Quick Error Diagnosis

**Time**: 2-5 minutes
**Automation**: 70%
**Purpose**: Fast initial diagnosis for common errors

**Process**:

1. **Analyze Error**:
```
Diagnose this error:

Error: [PASTE ERROR MESSAGE]
Stack trace: [PASTE STACK TRACE]

Provide:
1. What type of error is this?
2. Most likely root cause (1-2 sentences)
3. Immediate fix suggestion
4. Prevention recommendation
```

2. **Verify with Gemini** (for web research):
```bash
gemini -p "Search for solutions to this error:
[ERROR MESSAGE]

Find:
- Common causes
- Stack Overflow solutions
- GitHub issues with fixes"
```

3. **Output**: Quick diagnosis with fix suggestion

---

### Operation 2: Root Cause Analysis (RCA)

**Time**: 15-45 minutes
**Automation**: 50%
**Purpose**: Deep root cause analysis for complex issues

**Process**:

**Step 1: Gather Context (Context Agent)**
```bash
# Recent changes
git log --oneline -20
git diff HEAD~5..HEAD --stat

# Related logs
grep -r "ERROR\|Exception\|WARN" logs/ | tail -100

# System state
# Check for relevant metrics, traces, etc.
```

**Step 2: Hypothesis Generation (Analysis Agent)**
```
Perform root cause analysis:

**Error/Symptom**: [DESCRIPTION]

**Context**:
- Recent changes: [GIT LOG]
- Logs: [RELEVANT LOG ENTRIES]
- System state: [METRICS/OBSERVATIONS]
- When started: [TIMESTAMP]
- Affected scope: [USERS/SERVICES]

**Tasks**:
1. List 3-5 probable root causes ranked by likelihood
2. For each hypothesis:
   - Evidence supporting it
   - Evidence against it
   - Confidence level (High/Medium/Low)
3. Recommend investigation steps for top hypothesis
```

**Step 3: Cross-Validate (Verification Agent)**
```
Verify this root cause hypothesis:

Hypothesis: [TOP HYPOTHESIS]
Evidence: [SUPPORTING EVIDENCE]

Tasks:
1. What would we expect to see if this is correct?
2. What would disprove this hypothesis?
3. Design a reproduction test
4. Confidence assessment (0-100)
```

**Step 4: Generate RCA Report**
```markdown
## Root Cause Analysis Report

**Incident**: [DESCRIPTION]
**Date**: [DATE]
**Duration**: [DURATION]
**Impact**: [USERS/SERVICES AFFECTED]

### Timeline
- HH:MM - First error observed
- HH:MM - Investigation began
- HH:MM - Root cause identified
- HH:MM - Fix deployed

### Root Cause
[DETAILED EXPLANATION]

### Contributing Factors
1. [FACTOR 1]
2. [FACTOR 2]

### Resolution
[FIX APPLIED]

### Prevention
1. [ACTION ITEM 1]
2. [ACTION ITEM 2]
```

---

### Operation 3: Log Analysis & Classification

**Time**: 5-15 minutes
**Automation**: 80%
**Purpose**: Analyze and classify error logs

**Process**:

1. **Cluster Log Patterns**:
```
Analyze these log entries:

[PASTE 50-100 LOG LINES]

Tasks:
1. Identify unique error patterns (cluster similar errors)
2. Classify each pattern:
   - Type: (Bug/Config/Network/Resource/Security/User Error)
   - Severity: (Critical/High/Medium/Low)
   - Impact: (Data Loss/Service Down/Degraded/Minor)
3. Count occurrences per pattern
4. Identify the root pattern (original error vs cascading)
5. Recommend priority order for investigation
```

2. **Semantic Analysis**:
```
Perform semantic analysis on these logs:

[LOG ENTRIES]

Looking for:
- Anomalies in timing/sequence
- Correlation between events
- Hidden dependencies
- Patterns human might miss
```

3. **Output**: Classified and prioritized error report

---

### Operation 4: Multi-Agent Council Debugging

**Time**: 20-60 minutes
**Automation**: 40%
**Purpose**: Complex issues requiring multiple perspectives

**Process**:

**Launch Parallel Agents**:

```
Launch 4 debugging agents for this issue:

Issue: [DESCRIPTION]
Code: [RELEVANT CODE]
Logs: [RELEVANT LOGS]

Agent 1 (Code Reviewer):
"Analyze the code for bugs. Focus on:
- Logic errors
- Edge cases
- Race conditions
- Resource leaks"

Agent 2 (Log Analyzer):
"Analyze the logs for clues. Focus on:
- Error sequences
- Timing patterns
- State changes
- External dependencies"

Agent 3 (System Analyst):
"Analyze system context. Focus on:
- Resource constraints
- Configuration issues
- Dependency problems
- Infrastructure state"

Agent 4 (Historical Analyst):
"Analyze history. Focus on:
- Recent changes that could cause this
- Similar past incidents
- Regression indicators
- Pattern matching to known issues"
```

**Council Deliberation**:
```
Synthesize findings from all debugging agents:

Agent 1 (Code): [FINDINGS]
Agent 2 (Logs): [FINDINGS]
Agent 3 (System): [FINDINGS]
Agent 4 (History): [FINDINGS]

Tasks:
1. Find consensus root cause (where 2+ agents agree)
2. Resolve conflicting hypotheses
3. Combine evidence for strongest theory
4. Rate overall confidence (0-100)
5. Propose fix with verification steps
```

---

### Operation 5: Auto-Fix Generation

**Time**: 10-30 minutes
**Automation**: 60%
**Purpose**: Generate and verify fixes

**Process**:

**Step 1: Generate Fix (Fixer Agent)**
```
Generate a fix for this issue:

Issue: [ROOT CAUSE]
Code: [AFFECTED CODE]

Requirements:
1. Minimal change (fix only the issue)
2. Include error handling
3. Add comments explaining the fix
4. Suggest test cases to verify

Output format:
- File: [path]
- Before: [original code]
- After: [fixed code]
- Explanation: [why this fixes it]
```

**Step 2: Critique Fix (Critic Agent)**
```
Critique this proposed fix:

Issue: [ORIGINAL ISSUE]
Proposed Fix: [FIX CODE]

Evaluate:
1. Does it actually fix the root cause?
2. Could it introduce new bugs?
3. Edge cases not handled?
4. Performance implications?
5. Security implications?

Verdict: APPROVE / NEEDS_REVISION / REJECT
```

**Step 3: Generate Regression Test**
```
Generate a regression test for this fix:

Original Bug: [DESCRIPTION]
Fix Applied: [FIX CODE]

Create test that:
1. Would have caught the original bug
2. Verifies the fix works
3. Tests edge cases
4. Can run in CI/CD
```

---

### Operation 6: Self-Healing Patterns

**Time**: Variable
**Automation**: 90%
**Purpose**: Automated detection and remediation

**Process**:

**Define Remediation Playbooks**:
```python
# Example: Auto-remediation patterns
PLAYBOOKS = {
    "disk_space_low": {
        "detection": "disk_usage > 90%",
        "actions": [
            "compress_old_logs",
            "clear_temp_files",
            "alert_if_still_high"
        ]
    },
    "memory_leak_detected": {
        "detection": "memory_growth > 10%/hour",
        "actions": [
            "capture_heap_dump",
            "graceful_restart",
            "alert_team"
        ]
    },
    "error_rate_spike": {
        "detection": "error_rate > 5%",
        "actions": [
            "check_recent_deploys",
            "consider_rollback",
            "alert_on_call"
        ]
    }
}
```

**Configure Circuit Breakers**:
```python
# Intelligent circuit breaking
class AICircuitBreaker:
    def should_open(self, metrics):
        """AI predicts cascading failure risk."""
        prompt = f"""
        Given these metrics:
        - Error rate: {metrics['error_rate']}
        - Latency p99: {metrics['latency_p99']}
        - Dependencies health: {metrics['deps']}

        Should we open the circuit breaker?
        Risk of cascade: (Low/Medium/High)
        Recommendation: (OPEN/CLOSED/HALF_OPEN)
        """
        return analyze(prompt)
```

---

## Multi-AI Coordination

### Agent Assignment Strategy

| Task | Primary | Verification | Strength |
|------|---------|--------------|----------|
| Log analysis | Gemini | Claude | Fast, large context |
| Code analysis | Claude | Codex | Deep understanding |
| Root cause | Claude | Gemini | Reasoning + search |
| Fix generation | Claude | Codex | Code + review |
| Research | Gemini | Claude | Web search |

### Coordination Commands

**Gemini for Log Search**:
```bash
gemini -p "Analyze these logs and identify anomalies:
[LOGS]"
```

**Claude for Root Cause**:
```
Given this debugging context, what's the root cause?
[CONTEXT]
```

**Codex for Fix Validation**:
```bash
codex "Review this fix for correctness and edge cases:
[FIX]"
```

---

## Decision Trees

### Error Type Classification

```
Error Type Decision Tree:

1. Is there a stack trace?
   ├── Yes → Go to Code Error Analysis
   └── No → Go to System Error Analysis

2. Code Error Analysis:
   ├── NullPointer/TypeError → Missing null check
   ├── IndexOutOfBounds → Boundary condition
   ├── Timeout → Resource/network issue
   ├── Permission denied → Auth/authz issue
   └── Unknown → Multi-agent analysis

3. System Error Analysis:
   ├── Connection refused → Service down
   ├── Disk full → Resource exhaustion
   ├── Out of memory → Memory leak/sizing
   ├── CPU spike → Performance issue
   └── Unknown → Multi-agent analysis
```

### Severity Assessment

```
Severity Decision:

CRITICAL (P1):
- Data loss occurring
- Security breach active
- Service completely down
- Revenue impact immediate

HIGH (P2):
- Service degraded significantly
- Errors affecting >10% users
- Potential data integrity issues

MEDIUM (P3):
- Errors affecting <10% users
- Workaround available
- Non-critical feature broken

LOW (P4):
- Cosmetic issues
- Edge case errors
- No user impact
```

---

## Integration with Observability

### OpenTelemetry Pattern

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

@tracer.start_as_current_span("debug_session")
def debug_with_tracing(error):
    """Debug with full trace context."""
    span = trace.get_current_span()

    # Add debugging context to trace
    span.set_attribute("error.type", type(error).__name__)
    span.set_attribute("error.message", str(error))

    # Gather trace context for AI
    context = {
        "trace_id": span.get_span_context().trace_id,
        "parent_spans": get_parent_spans(),
        "related_logs": get_correlated_logs()
    }

    return multi_agent_debug(context)
```

### Log Correlation

```python
def correlate_logs_for_debugging(trace_id, time_window="5m"):
    """Gather all logs related to an incident."""
    # Query logs with trace correlation
    logs = query_logs(f"""
        trace_id:{trace_id} OR
        (level:ERROR AND timestamp:[now-{time_window} TO now])
    """)

    # Feed to AI for analysis
    return analyze_logs_with_ai(logs)
```

---

## Example Debugging Session

```
User: My API is returning 500 errors intermittently

Claude: Let me run multi-agent debugging to diagnose this.

[Launches Context, Analysis, and Verification agents]

## Debugging Report: Intermittent 500 Errors

### Agent Findings

**Log Analyzer**:
- Pattern: Errors spike every 5 minutes
- Correlation: Occurs during background job runs
- Log cluster: "Connection pool exhausted"

**Code Reviewer**:
- Found: Database connections not returned to pool in /api/users.py:145
- Missing: try/finally block for connection cleanup

**System Analyst**:
- Connection pool max: 20
- Concurrent requests during spike: 25+
- Background job opens 10 connections

**Historical**:
- Started after commit abc123 (2 days ago)
- Commit added new background job without connection limit

### Consensus Root Cause (Confidence: 92%)
Connection pool exhaustion due to:
1. New background job consuming connections
2. Missing connection cleanup in API handler

### Proposed Fix
```python
# /api/users.py:145
# Before
def get_user(id):
    conn = pool.get_connection()
    result = conn.execute("SELECT * FROM users WHERE id = ?", id)
    return result  # Connection never returned!

# After
def get_user(id):
    conn = pool.get_connection()
    try:
        result = conn.execute("SELECT * FROM users WHERE id = ?", id)
        return result
    finally:
        pool.return_connection(conn)  # Always return
```

### Verification Steps
1. Add connection tracking metric
2. Run load test
3. Monitor pool usage during background job

### Prevention
1. Add connection timeout
2. Implement connection leak detection
3. Review all pool usage
```

---

## Related Skills

- **multi-ai-code-review**: Review fixes before deployment
- **multi-ai-verification**: Verify fix effectiveness
- **multi-ai-testing**: Generate regression tests
- **ecs-troubleshooting**: Container-specific debugging
- **railway-troubleshooting**: Railway platform debugging

---

## References

- `references/log-analysis-patterns.md` - Log analysis techniques
- `references/self-healing-playbooks.md` - Auto-remediation patterns
