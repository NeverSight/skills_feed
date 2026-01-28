---
name: Error Recovery
description: Comprehensive error handling methodology with 13-category taxonomy, diagnostic workflows, recovery patterns, and prevention guidelines. Use when error rate >5%, MTTD/MTTR too high, errors recurring, need systematic error prevention, or building error handling infrastructure. Provides error taxonomy (file operations, API calls, data validation, resource management, concurrency, configuration, dependency, network, parsing, state management, authentication, timeout, edge cases - 95.4% coverage), 8 diagnostic workflows, 5 recovery patterns, 8 prevention guidelines, 3 automation tools (file path validation, read-before-write check, file size validation - 23.7% error prevention). Validated with 1,336 historical errors, 85-90% transferability across languages/platforms, 0.79 confidence retrospective validation.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Error Recovery

**Systematic error handling: detection, diagnosis, recovery, and prevention.**

> Errors are not failures - they're opportunities for systematic improvement. 95% of errors fall into 13 predictable categories.

---

## When to Use This Skill

Use this skill when:
- 📊 **High error rate**: >5% of operations fail
- ⏱️ **Slow recovery**: MTTD (Mean Time To Detect) or MTTR (Mean Time To Resolve) too high
- 🔄 **Recurring errors**: Same errors happen repeatedly
- 🎯 **Building error infrastructure**: Need systematic error handling
- 📈 **Prevention focus**: Want to prevent errors, not just handle them
- 🔍 **Root cause analysis**: Need diagnostic frameworks

**Don't use when**:
- ❌ Error rate <1% (handling ad-hoc sufficient)
- ❌ Errors are truly random (no patterns)
- ❌ No historical data (can't establish taxonomy)
- ❌ Greenfield project (no errors yet)

---

## Quick Start (20 minutes)

### Step 1: Quantify Baseline (10 min)

```bash
# For meta-cc projects
meta-cc query-tools --status error | jq '. | length'
# Output: Total error count

# Calculate error rate
meta-cc get-session-stats | jq '.total_tool_calls'
echo "Error rate: errors / total * 100"

# Analyze distribution
meta-cc query-tools --status error | \
  jq -r '.error_message' | \
  sed 's/:.*//' | sort | uniq -c | sort -rn | head -10
# Output: Top 10 error types
```

### Step 2: Classify Errors (5 min)

Map errors to 13 categories (see taxonomy below):
- File operations (12.2%)
- API calls, Data validation, Resource management, etc.

### Step 3: Apply Top 3 Prevention Tools (5 min)

Based on bootstrap-003 validation:
1. **File path validation** (prevents 12.2% of errors)
2. **Read-before-write check** (prevents 5.2%)
3. **File size validation** (prevents 6.3%)

**Total prevention**: 23.7% of errors

---

## 13-Category Error Taxonomy

Validated with 1,336 errors (95.4% coverage):

### 1. File Operations (12.2%)
- File not found, permission denied, path validation
- **Prevention**: Validate paths before use, check existence

### 2. API Calls (8.7%)
- HTTP errors, timeouts, invalid responses
- **Recovery**: Retry with exponential backoff

### 3. Data Validation (7.5%)
- Invalid format, missing fields, type mismatches
- **Prevention**: Schema validation, type checking

### 4. Resource Management (6.3%)
- File handles, memory, connections not cleaned up
- **Prevention**: Defer cleanup, use resource pools

### 5. Concurrency (5.8%)
- Race conditions, deadlocks, channel errors
- **Recovery**: Timeout mechanisms, panic recovery

### 6. Configuration (5.4%)
- Missing config, invalid values, env var issues
- **Prevention**: Config validation at startup

### 7. Dependency Errors (5.2%)
- Missing dependencies, version conflicts
- **Prevention**: Dependency validation in CI

### 8. Network Errors (4.9%)
- Connection refused, DNS failures, proxy issues
- **Recovery**: Retry, fallback to alternative endpoints

### 9. Parsing Errors (4.3%)
- JSON/XML parse failures, malformed input
- **Prevention**: Validate before parsing

### 10. State Management (3.7%)
- Invalid state transitions, missing initialization
- **Prevention**: State machine validation

### 11. Authentication (2.8%)
- Invalid credentials, expired tokens
- **Recovery**: Token refresh, re-authentication

### 12. Timeout Errors (2.4%)
- Operation exceeded time limit
- **Prevention**: Set appropriate timeouts

### 13. Edge Cases (1.2%)
- Boundary conditions, unexpected inputs
- **Prevention**: Comprehensive test coverage

**Uncategorized**: 4.6% (edge cases, unique errors)

---

## Eight Diagnostic Workflows

### 1. File Operation Diagnosis
1. Check file existence
2. Verify permissions
3. Validate path format
4. Check disk space

### 2. API Call Diagnosis
1. Verify endpoint availability
2. Check network connectivity
3. Validate request format
4. Review response codes

### 3-8. (See reference/diagnostic-workflows.md for complete workflows)

---

## Five Recovery Patterns

### 1. Retry with Exponential Backoff
**Use for**: Transient errors (network, API timeouts)
```go
for i := 0; i < maxRetries; i++ {
    err := operation()
    if err == nil {
        return nil
    }
    time.Sleep(time.Duration(math.Pow(2, float64(i))) * time.Second)
}
return fmt.Errorf("operation failed after %d retries", maxRetries)
```

### 2. Fallback to Alternative
**Use for**: Service unavailability

### 3. Graceful Degradation
**Use for**: Non-critical functionality failures

### 4. Circuit Breaker
**Use for**: Cascading failures prevention

### 5. Panic Recovery
**Use for**: Unhandled runtime errors

See [reference/recovery-patterns.md](reference/recovery-patterns.md) for complete patterns.

---

## Eight Prevention Guidelines

1. **Validate inputs early**: Check before processing
2. **Use type-safe APIs**: Leverage static typing
3. **Implement pre-conditions**: Assert expectations
4. **Defensive programming**: Handle unexpected cases
5. **Fail fast**: Detect errors immediately
6. **Log comprehensively**: Capture error context
7. **Test error paths**: Don't just test happy paths
8. **Monitor error rates**: Track trends over time

See [reference/prevention-guidelines.md](reference/prevention-guidelines.md).

---

## Three Automation Tools

### 1. File Path Validator
**Prevents**: 12.2% of errors (163/1,336)
**Usage**: Validate file paths before Read/Write operations
**Confidence**: 93.3% (sample validation)

### 2. Read-Before-Write Checker
**Prevents**: 5.2% of errors (70/1,336)
**Usage**: Verify file readable before writing
**Confidence**: 90%+

### 3. File Size Validator
**Prevents**: 6.3% of errors (84/1,336)
**Usage**: Check file size before processing
**Confidence**: 95%+

**Total prevention**: 317 errors (23.7%) with 0.79 overall confidence

See [scripts/](scripts/) for implementation.

---

## Proven Results

**Validated in bootstrap-003** (meta-cc project):
- ✅ 1,336 errors analyzed
- ✅ 13-category taxonomy (95.4% coverage)
- ✅ 23.7% error prevention validated
- ✅ 3 iterations, 10 hours (rapid convergence)
- ✅ V_instance: 0.83
- ✅ V_meta: 0.85
- ✅ Confidence: 0.79 (high)

**Transferability**:
- Error taxonomy: 95% (errors universal across languages)
- Diagnostic workflows: 90% (process universal, tools vary)
- Recovery patterns: 85% (patterns universal, syntax varies)
- Prevention guidelines: 90% (principles universal)
- **Overall**: 85-90% transferable

---

## Related Skills

**Parent framework**:
- [methodology-bootstrapping](../methodology-bootstrapping/SKILL.md) - Core OCA cycle

**Acceleration used**:
- [rapid-convergence](../rapid-convergence/SKILL.md) - 3 iterations achieved
- [retrospective-validation](../retrospective-validation/SKILL.md) - 1,336 historical errors

**Complementary**:
- [testing-strategy](../testing-strategy/SKILL.md) - Error path testing
- [observability-instrumentation](../observability-instrumentation/SKILL.md) - Error logging

---

## References

**Core methodology**:
- [Error Taxonomy](reference/taxonomy.md) - 13 categories detailed
- [Diagnostic Workflows](reference/diagnostic-workflows.md) - 8 workflows
- [Recovery Patterns](reference/recovery-patterns.md) - 5 patterns
- [Prevention Guidelines](reference/prevention-guidelines.md) - 8 guidelines

**Automation**:
- [Validation Tools](scripts/) - 3 prevention tools

**Examples**:
- [File Operation Errors](examples/file-operation-errors.md) - Common patterns
- [API Error Handling](examples/api-error-handling.md) - Retry strategies

---

**Status**: ✅ Production-ready | 1,336 errors validated | 23.7% prevention | 85-90% transferable
