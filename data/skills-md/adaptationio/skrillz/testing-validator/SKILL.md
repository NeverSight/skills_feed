---
name: testing-validator
description: Comprehensive testing validation for Claude Code skills through functional testing, example validation, integration testing, regression testing, and edge case testing. Task-based testing operations with automated example execution, manual scenario testing, and test reporting. Use when testing skill functionality, validating examples execute correctly, ensuring integration works, preventing regressions, or conducting comprehensive functional quality assurance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Testing Validator

## Overview

testing-validator provides comprehensive functional testing for Claude Code skills, validating that skills actually work correctly in practice through systematic testing operations.

**Purpose**: Functional validation - ensure skills work correctly, not just look good

**The 5 Testing Operations**:
1. **Functional Testing** - Core skill functionality works as intended
2. **Example Validation** - All code/command examples execute successfully
3. **Integration Testing** - Skills work correctly with dependencies and compositions
4. **Regression Testing** - Updates don't break existing functionality
5. **Edge Case Testing** - Handles unusual scenarios and boundary conditions

**Complement to review-multi**:
- **review-multi**: Quality assessment (structure, content, patterns, usability) - "Is it good?"
- **testing-validator**: Functional validation (does it work, examples execute, integrations function) - "Does it work?"
- **Together**: Complete validation (quality + functionality)

**Key Benefits**:
- Automated example execution (catch broken examples)
- Integration validation (ensure skills compose correctly)
- Regression prevention (detect breaks from updates)
- Edge case coverage (handle unusual scenarios)
- Systematic testing (consistent, repeatable)

## When to Use

Use testing-validator when:

1. **Pre-Deployment Testing** - Validate functionality before release
2. **Example Validation** - Ensure all examples execute correctly
3. **Integration Validation** - Test workflow skills and dependencies
4. **Post-Update Testing** - Regression testing after changes
5. **Comprehensive QA** - Combined with review-multi for complete validation
6. **CI/CD Integration** - Automated testing in pipelines
7. **Edge Case Validation** - Test boundary conditions and unusual scenarios
8. **Functional Certification** - Certify skills work correctly in practice

## Prerequisites

- Skill to test
- Ability to execute examples (appropriate environment)
- Time allocation:
  - Quick Check: 15-30 minutes
  - Single Operation: 20-90 minutes
  - Comprehensive Testing: 2-4 hours

## Operations

### Operation 1: Functional Testing

**Purpose**: Validate core skill functionality works as intended

**When to Use This Operation**:
- Testing if skill achieves stated purpose
- Validating core functionality
- Checking if instructions lead to successful outcomes
- Pre-deployment functional validation

**Automation Level**: 30% automated (script checks), 70% manual (scenario execution)

**Process**:

1. **Select Test Scenarios**
   - Choose 2-3 scenarios from "When to Use" section
   - Prioritize: primary use case + common case + edge case
   - Ensure scenarios cover main functionality

2. **Execute Scenarios**
   - Actually follow skill instructions
   - Complete the intended task
   - Document results (success/partial/failure)
   - Note any issues encountered

3. **Validate Outputs**
   - Does skill produce expected outputs?
   - Are outputs useful and correct?
   - Do outputs match documentation?

4. **Check Error Handling**
   - What happens with errors?
   - Are error messages helpful?
   - Can users recover from errors?

5. **Assess Functionality**
   - Does skill achieve stated purpose?
   - Is functionality complete?
   - Are there functional gaps?

**Validation Checklist**:
- [ ] Primary use case tested (from "When to Use")
- [ ] Common use case tested
- [ ] Edge case tested (if applicable)
- [ ] All scenarios completed successfully
- [ ] Outputs correct and useful
- [ ] Error handling works (if errors encountered)
- [ ] Functionality complete (no gaps)
- [ ] Skill achieves stated purpose

**Test Results**:
- **PASS**: All scenarios succeed, functionality complete
- **PARTIAL**: Some scenarios succeed, minor issues
- **FAIL**: Scenarios fail, functionality broken

**Outputs**:
- Test result (PASS/PARTIAL/FAIL)
- Scenario execution results
- Functional issues identified (if any)
- Recommendations for fixes

**Time Estimate**: 30-90 minutes

**Example**:
```
Functional Testing: skill-researcher
====================================

Test Scenarios:
1. Primary: Research GitHub API integration patterns
2. Common: Research for skill development planning
3. Edge: Research with no results found

Scenario 1: GitHub API Integration Research
- Executed: Operation 2 (GitHub Repository Research)
- Result: ✅ SUCCESS
- Time: 25 minutes
- Output: Found 5 repositories, extracted patterns
- Functionality: Achieved purpose (research complete)

Scenario 2: Skill Development Research
- Executed: All 5 operations (Web, GitHub, Docs, Synthesis)
- Result: ✅ SUCCESS
- Time: 60 minutes
- Output: Research synthesis with 4 sources, 3 patterns
- Functionality: Fully achieved purpose

Scenario 3: No Results Edge Case
- Executed: Web search for obscure topic
- Result: ✅ HANDLED
- Time: 10 minutes
- Output: "No results found" with guidance to adjust search
- Error Handling: Good (helpful message, suggests alternatives)

Overall Functional Test: ✅ PASS
- All scenarios succeeded
- Functionality complete
- Error handling works
- Achieves stated purpose
```

---

### Operation 2: Example Validation

**Purpose**: Verify all code/command examples in skill documentation execute correctly

**When to Use This Operation**:
- Validating documentation accuracy
- Ensuring examples are current and working
- Preventing broken example deployment
- Post-update example regression testing

**Automation Level**: 80% automated (example extraction and execution)

**Process**:

1. **Extract All Examples**
   - Scan SKILL.md for code blocks (```)
   - Extract examples with language tags
   - Identify executable vs informational examples
   - Count total examples

2. **Categorize Examples**
   - Shell/bash commands
   - Python code snippets
   - YAML/config samples
   - Informational (not executable)

3. **Execute Examples Automatically**
   ```bash
   python3 scripts/validate-examples.py /path/to/skill
   ```
   - Executes all bash/python examples
   - Captures output and errors
   - Compares to expected output (if documented)
   - Reports success/failure per example

4. **Manual Validation** (for non-automatable):
   - Configuration examples (check syntax)
   - Conceptual examples (check accuracy)
   - Workflow examples (check logic)

5. **Generate Example Report**
   - Total examples: X
   - Executable: Y (Z%)
   - Passed: A
   - Failed: B
   - Success rate: A/(A+B) × 100%

**Validation Checklist**:
- [ ] All examples extracted and counted
- [ ] Executable examples identified
- [ ] Automated validation run (bash/python examples)
- [ ] Non-executable examples checked manually
- [ ] All examples execute successfully OR expected failures documented
- [ ] Broken examples identified with fixes
- [ ] Success rate ≥90% (for production)

**Test Results**:
- **PASS**: ≥90% of executable examples work correctly
- **PARTIAL**: 70-89% examples work, some broken
- **FAIL**: <70% examples work, many broken

**Outputs**:
- Example inventory (total, executable, non-executable)
- Execution results per example
- Success rate
- Broken examples list with error messages
- Recommendations for fixes

**Time Estimate**: 20-45 minutes (mostly automated)

**Example**:
```
Example Validation: review-multi
=================================

Extraction Results:
- Total examples: 18
- Executable (bash): 12
- Executable (python): 3
- Informational (YAML): 3

Automated Execution:

Bash Examples (12 total):
✅ PASS: python3 scripts/validate-structure.py <path> (3 instances)
✅ PASS: python3 scripts/check-patterns.py <path>
✅ PASS: python3 scripts/generate-review-report.py <file>
✅ PASS: python3 scripts/review-runner.py <path>
⚠️ WARNING: Example uses placeholder <path> - works with substitution
- Success Rate: 12/12 (100%)

Python Examples (3 total):
✅ PASS: All 3 syntax-valid, execute correctly
- Success Rate: 3/3 (100%)

Manual Validation (3 YAML examples):
✅ PASS: All YAML examples valid syntax
✅ PASS: Frontmatter examples follow standards

Overall Example Validation: ✅ PASS
- Success Rate: 100% (18/18 examples work)
- Minor Note: Some examples use placeholders (acceptable with clear notes)

Recommendation: Examples excellent, all functional
```

---

### Operation 3: Integration Testing

**Purpose**: Test skills work correctly with other skills, especially in workflows and compositions

**When to Use This Operation**:
- Testing workflow skills (that compose others)
- Validating dependencies work correctly
- Checking skill integration points
- Testing data flow between skills

**Automation Level**: 20% automated (dependency checking), 80% manual (actual integration testing)

**Process**:

1. **Identify Integration Points**
   - Does skill depend on other skills?
   - Does skill compose with others (workflow)?
   - Are there data flows between skills?
   - Integration examples provided?

2. **Test Skill Dependencies**
   - Load required skills (can they be loaded?)
   - Execute dependent functionality
   - Verify dependency works as expected
   - Check version compatibility (if applicable)

3. **Test Workflow Compositions**
   - For workflow skills: execute multi-skill workflow
   - Verify data flows correctly between steps
   - Check each component skill integration
   - Validate output-to-input transitions

4. **Test Integration Examples**
   - Execute documented integration examples
   - Verify skills compose as documented
   - Check integration instructions accurate

5. **Assess Integration Quality**
   - Integrations smooth or problematic?
   - Data flows correctly?
   - Clear integration guidance?
   - Error handling across skill boundaries?

**Validation Checklist**:
- [ ] Integration points identified
- [ ] Dependencies tested (if applicable)
- [ ] Workflow composition tested (if workflow skill)
- [ ] Data flow validated (inputs/outputs correct)
- [ ] Integration examples execute successfully
- [ ] Cross-skill error handling works
- [ ] Integration guidance accurate
- [ ] No integration issues found

**Test Results**:
- **PASS**: All integrations work smoothly
- **PARTIAL**: Integrations work with minor issues
- **FAIL**: Integration broken or major issues
- **N/A**: Standalone skill with no integrations

**Outputs**:
- Integration test results
- Workflow execution results (if applicable)
- Data flow validation
- Integration issues (if any)
- Recommendations

**Time Estimate**: 30-90 minutes (varies by integration complexity, N/A for standalone skills)

**Example**:
```
Integration Testing: development-workflow
==========================================

Integration Type: Workflow Composition (5 component skills)

Dependencies Identified:
1. skill-researcher (Step 1)
2. planning-architect (Step 2)
3. task-development (Step 3, optional)
4. prompt-builder (Step 4)
5. todo-management (Step 5)

Integration Test Execution:

Step 1 → Step 2 Integration:
- Input to Step 2: research-synthesis.md from Step 1
- Test: Create research synthesis, feed to planning-architect
- Result: ✅ PASS (planning-architect correctly uses research findings)
- Data Flow: Smooth (outputs match expected inputs)

Step 2 → Step 3 Integration:
- Input to Step 3: skill-architecture-plan.md from Step 2
- Test: Create architecture plan, feed to task-development
- Result: ✅ PASS (task-development breaks down plan correctly)
- Data Flow: Smooth

Step 3 → Step 4 Integration:
- Input to Step 4: task-breakdown.md from Step 3
- Test: Create task breakdown, feed to prompt-builder
- Result: ✅ PASS (prompt-builder creates prompts for tasks)
- Data Flow: Smooth

Step 4 → Step 5 Integration:
- Input to Step 5: prompts-collection.md from Step 4
- Test: Create prompts, feed to todo-management
- Result: ✅ PASS (todo-management creates todos from tasks)
- Data Flow: Smooth

Workflow Execution Test:
- Executed: Complete workflow (all 5 steps)
- Result: ✅ SUCCESS (produced complete skill planning artifacts)
- Time: 4.5 hours (as documented)
- Quality: High (artifacts complete and usable)

Overall Integration Test: ✅ PASS
- All 5 integrations work smoothly
- Data flows correctly between steps
- Workflow achieves stated purpose
- No integration issues found
```

---

### Operation 4: Regression Testing

**Purpose**: Ensure updates don't break existing functionality

**When to Use This Operation**:
- After skill updates or improvements
- Before deploying changes
- Validating skill-updater changes
- Post-auto-updater verification

**Automation Level**: 60% automated (comparison, example re-execution), 40% manual

**Process**:

1. **Establish Baseline**
   - Before changes: run tests, document results
   - Save baseline test results
   - Note which examples/scenarios work

2. **Apply Changes**
   - Make updates to skill
   - Document what changed

3. **Re-Run Tests**
   - Re-execute same tests as baseline
   - Run example validation again
   - Test same scenarios

4. **Compare Results**
   - Before vs After comparison
   - Which tests changed status?
   - New failures? (regressions)
   - New successes? (improvements)
   - Unchanged? (stable)

5. **Identify Regressions**
   - Tests that passed before but fail now
   - Functionality that worked but now broken
   - Examples that executed but now error

**Validation Checklist**:
- [ ] Baseline tests documented (before changes)
- [ ] Changes applied and documented
- [ ] All baseline tests re-executed
- [ ] Results compared (before vs after)
- [ ] No new failures (no regressions)
- [ ] If failures: identified and documented
- [ ] Regression fixes applied (if needed)
- [ ] Final validation: all tests pass

**Test Results**:
- **PASS**: No regressions (all baseline tests still pass)
- **REGRESSION**: Some tests failed that previously passed
- **IMPROVED**: Some tests pass that previously failed (plus no regressions)

**Outputs**:
- Regression test report
- Before/after comparison
- Identified regressions (if any)
- Regression fixes (if applicable)
- Final test status

**Time Estimate**: 30-60 minutes

**Example**:
```
Regression Testing: planning-architect (after Quick Ref addition)
==================================================================

Baseline (Before Quick Reference):
- Structure validation: 5/5 (PASS)
- Example count: 8 examples
- All examples: Execute successfully
- Scenarios tested: 2 scenarios (both PASS)

Changes Applied:
- Added Quick Reference section (96 lines)
- Added tables, checklists, decision tree

Re-Run Tests (After Quick Reference):
- Structure validation: 5/5 (PASS) ✅ No regression
- Example count: 8 examples ✅ No change
- All examples: Execute successfully ✅ No regression
- Scenarios tested: 2 scenarios (both PASS) ✅ No regression
- NEW: Quick Reference detected ✅ Improvement

Comparison:
✅ All baseline tests still pass (no regressions)
✅ New functionality added (Quick Reference)
✅ Quality maintained (5/5 score)

Overall Regression Test: ✅ PASS (No Regressions)
Additional: ✅ IMPROVEMENT (Quick Reference added)

Recommendation: Changes safe to deploy
```

---

### Operation 5: Edge Case Testing

**Purpose**: Test skill handles unusual scenarios, boundary conditions, and edge cases correctly

**When to Use This Operation**:
- Testing robustness
- Validating error handling
- Checking boundary conditions
- Ensuring graceful degradation

**Automation Level**: 30% automated (known edge case checks), 70% manual (scenario thinking)

**Process**:

1. **Identify Edge Cases**
   - Empty inputs (what if no data?)
   - Maximum inputs (what if too much data?)
   - Invalid inputs (what if wrong format?)
   - Missing dependencies (what if skill not found?)
   - Boundary conditions (limits, thresholds)

2. **Design Edge Case Tests**
   - Create test scenarios for each edge case
   - Define expected behavior
   - Document pass criteria

3. **Execute Edge Case Tests**
   - Test with empty/minimal inputs
   - Test with maximum/excessive inputs
   - Test with invalid/malformed inputs
   - Test with missing dependencies
   - Test boundary conditions

4. **Evaluate Handling**
   - Does skill handle edge case gracefully?
   - Error messages clear and helpful?
   - No crashes or undefined behavior?
   - Appropriate fallbacks or defaults?

5. **Document Edge Case Behavior**
   - Which edge cases handled well?
   - Which edge cases cause issues?
   - Expected vs actual behavior
   - Recommendations for improvement

**Validation Checklist**:
- [ ] Edge cases identified (minimum 3-5)
- [ ] Each edge case tested
- [ ] Error handling assessed
- [ ] No crashes or undefined behavior
- [ ] Error messages helpful (if applicable)
- [ ] Graceful degradation (if applicable)
- [ ] Edge case handling documented
- [ ] Critical edge cases handled correctly

**Test Results**:
- **PASS**: All critical edge cases handled correctly
- **PARTIAL**: Most edge cases handled, some issues
- **FAIL**: Critical edge cases cause errors or crashes

**Outputs**:
- Edge case test results
- Handling quality assessment
- Issues identified
- Recommendations for robustness

**Time Estimate**: 30-90 minutes

**Example**:
```
Edge Case Testing: todo-management
===================================

Edge Cases Identified:
1. Empty task list (initialize with 0 tasks)
2. Single task (minimal usage)
3. 100+ tasks (maximum usage)
4. Starting non-existent task
5. Completing already completed task

Edge Case Tests:

Test 1: Empty Task List
- Scenario: Initialize with empty list
- Execution: todo-management Operation 1 with 0 tasks
- Result: ✅ PASS (handles gracefully, shows empty state)
- Error: None

Test 2: Single Task
- Scenario: List with 1 task only
- Execution: Complete workflow on 1 task
- Result: ✅ PASS (works correctly, minimal case handled)

Test 3: 100 Tasks
- Scenario: Large task list
- Execution: Report progress on 100-task list
- Result: ✅ PASS (handles large lists, performance acceptable)
- Note: Report generation ~5 seconds (good)

Test 4: Non-Existent Task
- Scenario: Start task #999 (doesn't exist)
- Execution: Operation 2 (Start Task 999)
- Result: ✅ PASS (clear error: "Task 999 not found")
- Error Handling: Excellent (specific error message)

Test 5: Double Complete
- Scenario: Complete task #5 twice
- Execution: Operation 3 twice on same task
- Result: ✅ PASS (second attempt shows "Already completed")
- Error Handling: Good (informative message)

Overall Edge Case Test: ✅ PASS
- All critical edge cases handled correctly
- Error messages clear and helpful
- No crashes or undefined behavior
- Graceful handling of unusual scenarios

Recommendation: Edge case handling excellent
```

---

## Testing Modes

### Comprehensive Testing Mode

**Purpose**: Complete functional validation across all 5 operations

**When to Use**:
- Pre-deployment (ensure everything works)
- Major updates (comprehensive regression testing)
- Quality certification (complete functional validation)

**Process**:
1. Run all 5 testing operations
2. Aggregate results
3. Generate comprehensive test report
4. Make deployment decision

**Time Estimate**: 2-4 hours

**Output**: Complete test report with PASS/FAIL for deployment

---

### Quick Check Mode

**Purpose**: Fast functional validation (examples only)

**When to Use**:
- During development (continuous testing)
- Quick validation (examples work?)
- Pre-commit checks

**Process**:
1. Run Operation 2 only (Example Validation)
2. Automated execution of all examples
3. Quick pass/fail report

**Time Estimate**: 15-30 minutes (automated)

**Output**: Example validation results

---

### Custom Testing Mode

**Purpose**: Select specific operations based on needs

**When to Use**:
- Targeted testing (only certain aspects)
- Time constraints (can't do comprehensive)
- Specific concerns (e.g., only integration testing)

**Process**:
1. Select operations to run (1-5)
2. Execute selected tests
3. Generate targeted report

---

## Best Practices

### 1. Test Early and Often
**Practice**: Run Quick Check during development, Comprehensive before deployment

**Rationale**: Early testing catches issues before they compound

**Application**: Quick Check daily, Comprehensive pre-deploy

### 2. Automate Example Validation
**Practice**: Use automated example validation (validate-examples.py)

**Rationale**: 80% automated, fast, catches broken examples instantly

**Application**: Run after any example changes

### 3. Test Real Scenarios
**Practice**: Use actual use cases for functional testing

**Rationale**: Real scenarios reveal issues documentation review misses

**Application**: Test scenarios from "When to Use" section

### 4. Regression Test After Updates
**Practice**: Always run regression tests after skill changes

**Rationale**: Prevents breaking existing functionality with improvements

**Application**: Before/after comparison for all updates

### 5. Document Test Results
**Practice**: Save test reports for comparison over time

**Rationale**: Track testing trends, identify patterns

**Application**: Generate test report for each comprehensive test

### 6. Fix Broken Examples Immediately
**Practice**: Don't deploy with broken examples

**Rationale**: Broken examples destroy user confidence

**Application**: Example validation must PASS before deploy

---

## Common Mistakes

### Mistake 1: Skipping Example Validation
**Symptom**: Users report broken examples after deployment

**Cause**: Not testing examples before release

**Fix**: Run Operation 2 (Example Validation) before every deployment

**Prevention**: Make example validation mandatory in deployment checklist

### Mistake 2: Only Testing Happy Path
**Symptom**: Skills break with unusual inputs or edge cases

**Cause**: Not testing edge cases

**Fix**: Run Operation 5 (Edge Case Testing)

**Prevention**: Include edge case testing in comprehensive mode

### Mistake 3: No Regression Testing
**Symptom**: Updates break previously working functionality

**Cause**: Not testing before/after updates

**Fix**: Run Operation 4 (Regression Testing) after changes

**Prevention**: Make regression testing mandatory for all updates

### Mistake 4: Not Testing Integrations
**Symptom**: Workflow skills break when actually composing other skills

**Cause**: Testing skills individually, not integrated

**Fix**: Run Operation 3 (Integration Testing) for workflow skills

**Prevention**: Always test integrations for workflow/composition skills

### Mistake 5: Manual Testing Only
**Symptom**: Testing takes too long, often skipped

**Cause**: Not using automation

**Fix**: Use validate-examples.py for automated example checking

**Prevention**: Automate where possible (examples, scripts, structure)

---

## Quick Reference

### The 5 Testing Operations

| Operation | Focus | Automation | Time | Pass Criteria |
|-----------|-------|------------|------|---------------|
| **Functional** | Core functionality works | 30% | 30-90m | Scenarios succeed |
| **Example Validation** | Examples execute correctly | 80% | 20-45m | ≥90% examples work |
| **Integration** | Skills work together | 20% | 30-90m | Integrations smooth |
| **Regression** | Updates don't break functionality | 60% | 30-60m | No new failures |
| **Edge Case** | Handles unusual scenarios | 30% | 30-90m | Critical edge cases handled |

### Testing Modes

| Mode | Time | Operations | Use Case |
|------|------|------------|----------|
| **Comprehensive** | 2-4h | All 5 operations | Pre-deployment, certification |
| **Quick Check** | 15-30m | Example validation only | During development |
| **Custom** | Variable | Selected operations | Targeted testing |

### Test Results

| Result | Meaning | Action |
|--------|---------|--------|
| **PASS** | All tests successful | Deploy with confidence |
| **PARTIAL** | Some issues, not critical | Fix issues, re-test, then deploy |
| **FAIL** | Critical issues | Fix before deployment |

### Integration with review-multi

**Use Both for Complete Validation**:
```
review-multi (quality) + testing-validator (functionality) = Complete Validation

review-multi: Is it good? (structure, content, patterns, usability)
testing-validator: Does it work? (functional, examples, integration)

Together: Ready to deploy? (quality + functionality validated)
```

### Automation Scripts

```bash
# Validate all examples automatically
python3 scripts/validate-examples.py /path/to/skill

# Run comprehensive test suite
python3 scripts/test-runner.py /path/to/skill --mode comprehensive

# Generate test report
python3 scripts/generate-test-report.py test-results.json --output report.md
```

### For More Information

- **Functional testing**: references/functional-testing-guide.md
- **Example validation**: references/example-validation-guide.md
- **Integration testing**: references/integration-testing-guide.md
- **Regression testing**: references/regression-testing-guide.md
- **Edge case testing**: references/edge-case-testing-guide.md
- **Test reports**: references/test-report-template.md

---

**testing-validator ensures skills work correctly through comprehensive functional testing, example validation, integration testing, regression testing, and edge case validation.**
