---
name: test-runner
description: Runs systematic tests on Claude Code customizations. Executes sample queries, validates responses, generates test reports, and identifies edge cases for agents, commands, skills, and hooks.
allowed-tools: [Read, Write, Glob, Grep, Bash, Skill]
# model: inherit
---

## Reference Files

This skill uses reference materials:

- [examples.md](examples.md) - Concrete test case examples for different customization types
- [common-failures.md](common-failures.md) - Catalog of common failure patterns

## Focus Areas

- **Sample Query Generation** - Creating realistic test queries based on descriptions
- **Expected Behavior Validation** - Verifying outputs match specifications
- **Regression Testing** - Ensuring changes don't break existing functionality
- **Edge Case Identification** - Finding unusual scenarios and boundary conditions
- **Integration Testing** - Validating customizations work together
- **Performance Assessment** - Analyzing context usage and efficiency

## Test Framework

### Test Types

#### Functional Tests

**Purpose**: Verify core functionality works as specified

**Process**:

1. Generate test queries from description/documentation
2. Execute customization with test input
3. Compare actual output to expected behavior
4. Record PASS/FAIL for each test case

#### Integration Tests

**Purpose**: Ensure customizations work together

**Process**:

1. Test hook interactions (PreToolUse, PostToolUse chains)
2. Verify skills can invoke sub-agents
3. Check commands delegate correctly
4. Validate settings.json configuration
5. Test tool permission boundaries

#### Usability Tests

**Purpose**: Assess user experience quality

**Process**:

1. Evaluate error messages (are they helpful?)
2. Check documentation completeness
3. Test edge cases (what breaks it?)
4. Assess output clarity
5. Verify examples work as shown

### Test Execution Strategy

#### For Skills

1. **Discovery Test**: Generate queries that should trigger the skill
2. **Invocation Test**: Actually invoke the skill with sample query
3. **Output Test**: Verify skill produces expected results
4. **Tool Test**: Confirm only allowed tools are used
5. **Reference Test**: Check that references load correctly

#### For Agents

1. **Frontmatter Test**: Validate YAML structure
2. **Invocation Test**: Invoke agent with test prompt
3. **Tool Test**: Verify agent uses appropriate tools
4. **Output Test**: Check output format and quality
5. **Context Test**: Measure context usage

#### For Commands

1. **Delegation Test**: Verify command invokes correct agent/skill
2. **Usage Test**: Test with valid and invalid arguments
3. **Documentation Test**: Verify usage instructions are accurate
4. **Output Test**: Check output format and clarity

#### For Hooks

1. **Input Test**: Verify JSON stdin handling
2. **Exit Code Test**: Confirm 0 (allow) and 2 (block) work correctly
3. **Error Handling Test**: Verify graceful degradation
4. **Performance Test**: Check execution speed
5. **Integration Test**: Test hook chain behavior

## Test Process

### Step 1: Identify Customization Type

Determine what to test:

- Agent (in agents/)
- Command (in commands/)
- Skill (in skills/)
- Hook (in hooks/)

### Step 2: Read Documentation

Use Read tool to examine:

- Primary file content
- Frontmatter/configuration
- Usage instructions
- Examples (if provided)

### Step 3: Generate Test Cases

Based on description and documentation:

**For Skills**:

- Extract trigger phrases from description
- Create 5-10 sample queries that should trigger
- Create 3-5 queries that should NOT trigger
- Identify edge cases from description

**For Agents**:

- Create prompts based on focus areas
- Generate scenarios agent should handle
- Identify scenarios outside agent scope

**For Commands**:

- Test with documented arguments
- Test with no arguments
- Test with invalid arguments

**For Hooks**:

- Create sample tool inputs that should pass
- Create inputs that should block
- Create malformed inputs to test error handling

### Step 4: Execute Tests

**Read-Only Testing** (default):

- Analyze whether customization would work
- Check configurations and settings
- Verify documentation accuracy
- Assess expected behavior

**Active Testing** (when appropriate):

- Actually invoke skills with sample queries
- Run commands with test arguments
- Trigger hooks with test inputs
- Record actual outputs

### Step 5: Compare Results

For each test:

- **Expected**: What should happen (from docs/description)
- **Actual**: What did happen (from testing)
- **Status**: PASS (matched) / FAIL (didn't match) / EDGE CASE (unexpected)

### Step 6: Generate Test Report

Create structured report following output format.

## Output Format

```markdown
# Test Report: {name}

**Type**: {agent|command|skill|hook}
**File**: {path}
**Tested**: {YYYY-MM-DD HH:MM}
**Test Mode**: {read-only|active}

## Summary

{1-2 sentence overview of what was tested and overall results}

## Test Results

**Total Tests**: {count}
**Passed**: {count} ({percentage}%)
**Failed**: {count} ({percentage}%)
**Edge Cases**: {count}

## Functional Tests

### Test 1: {test name}

- **Input**: {test input/query}
- **Expected**: {expected behavior}
- **Actual**: {actual behavior}
- **Status**: PASS | FAIL | EDGE CASE
- **Notes**: {observations}

### Test 2: {test name}

...

## Integration Tests

{If applicable - tests with other customizations}

### Integration 1: {integration name}

- **Components**: {what was tested together}
- **Expected**: {expected interaction}
- **Actual**: {actual interaction}
- **Status**: PASS | FAIL
- **Notes**: {observations}

## Usability Assessment

- **Documentation**: CLEAR | UNCLEAR | MISSING
- **Error Messages**: HELPFUL | CONFUSING | ABSENT
- **Examples**: WORKING | BROKEN | MISSING
- **Overall UX**: EXCELLENT | GOOD | NEEDS WORK | POOR

## Edge Cases Discovered

{Unusual scenarios or boundary conditions found during testing}

1. {edge case 1}
   - **Impact**: {severity}
   - **Recommendation**: {how to handle}

2. {edge case 2}
   ...

## Performance Metrics

{If applicable}

- **Context Usage**: ~{token estimate}
- **Execution Time**: {estimate or N/A}
- **Resource Impact**: LOW | MEDIUM | HIGH

## Failures and Issues

{Detailed analysis of failed tests}

### Failure 1: {test name}

- **Why It Failed**: {root cause}
- **Expected vs Actual**: {specific diff}
- **Fix Recommendation**: {how to resolve}

### Failure 2: {test name}

...

## Recommendations

### Priority 1 (Critical)

{Must-fix issues that prevent functionality}

1. {critical fix 1}
2. {critical fix 2}

### Priority 2 (Important)

{Should-fix issues that impact usability}

1. {important fix 1}
2. {important fix 2}

### Priority 3 (Nice-to-Have)

{Could-fix issues that polish the experience}

1. {enhancement 1}
2. {enhancement 2}

## Next Steps

{Specific actions to address failures and improve tests}
```

## Test Case Examples

For detailed test case examples for skills, agents, commands, and hooks, see [examples.md](examples.md).

## Best Practices for Testing

1. **Test Both Paths**: Success cases AND failure cases
2. **Edge Cases Matter**: Test boundaries and unusual inputs
3. **Clear Expected Behavior**: Document what should happen
4. **Realistic Queries**: Use natural language users would actually type
5. **Integration Testing**: Don't just test in isolation
6. **Performance Aware**: Note if tests are slow or heavy
7. **Regression Testing**: Re-test after changes
8. **Document Failures**: Explain why tests failed, not just that they did
9. **Actionable Recommendations**: Provide specific fixes
10. **Version Testing**: Note which version was tested

## Common Test Failures

For a catalog of common failure patterns by customization type, see [common-failures.md](common-failures.md).

## Tools Used

This skill uses these tools for testing:

- **Read** - Examine customization files
- **Write** - Generate and save test reports to files
- **Grep** - Search for patterns and configurations
- **Glob** - Find files and customizations
- **Bash** - Execute read-only commands for analysis
- **Skill** - Invoke skills for active testing

In read-only mode (default), no customizations are actually invoked - the skill analyzes configurations and documentation to assess expected behavior. In active mode, skills are invoked with test queries to verify actual behavior.

Test reports are written to `~/.claude/logs/evaluations/tests/` using the Write tool.
