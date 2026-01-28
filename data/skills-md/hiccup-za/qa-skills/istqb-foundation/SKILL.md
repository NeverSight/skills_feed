---
name: istqb-foundation
description: |
  Comprehensive guide to ISTQB Foundation Level knowledge areas for QA testing. This skill provides
  detailed guidance on testing fundamentals, test techniques, test management, and static testing
  following the ISTQB Certified Tester Foundation Level (CTFL) syllabus. Use this when establishing
  standardized testing practices, designing test cases, selecting test techniques, or aligning team
  terminology with industry standards.

  Triggers on: establishing QA baselines, designing test cases, selecting test techniques, planning
  test activities, conducting reviews, managing test processes, or when standardized testing terminology
  and practices are needed.
metadata:
  version: "1.1.0"
---

# ISTQB Foundation

Comprehensive guide to applying ISTQB Foundation Level knowledge areas in QA work. This skill covers testing fundamentals, test techniques (black-box, white-box, experience-based), test management, static testing, and tool support following the ISTQB Certified Tester Foundation Level (CTFL) syllabus v4.0.1. Use this to establish standardized testing practices, design effective test cases, select appropriate test techniques, and align team terminology with industry standards.

## Overview

The ISTQB Foundation Level provides a standardized framework for software testing that establishes common terminology, principles, and practices. This skill covers:

- **Testing Fundamentals**: Core principles of testing, test process, and psychology of testing
- **Test Techniques**: Systematic approaches to test design including black-box, white-box, and experience-based techniques
- **Test Management**: Planning, estimation, monitoring, risk management, and defect management
- **Static Testing**: Early defect detection through reviews and static analysis
- **Test Levels and Types**: Understanding unit, integration, system, and acceptance testing
- **Tool Support**: Effective use of testing tools

This skill aligns with the ISTQB Certified Tester Foundation Level (CTFL) syllabus and provides actionable guidance for applying these concepts in real-world QA scenarios.

## When to Apply

Reference this skill when:
- Establishing a common QA baseline and terminology for a team
- Designing test cases and need to select appropriate test techniques
- Planning test activities and need structured approaches to estimation and risk management
- Conducting code or document reviews and need systematic review processes
- Aligning testing practices across different projects or teams
- Preparing for ISTQB Foundation Level certification
- Defining test strategies and need industry-standard approaches
- Managing defects and need structured defect lifecycle processes
- Selecting and implementing testing tools

**Preconditions:**
- Product or project context (requirements, specifications, or user stories)
- Understanding of software development lifecycle
- Access to testing tools and environments (when applicable)
- Team alignment on using ISTQB terminology and practices

## Quick Decision Trees

### "I need to design test cases for a feature"

```
What type of testing is needed?
├─ Functional testing with clear inputs/outputs → Use black-box techniques
│   ├─ Input validation → `equivalence-partitioning`, `boundary-value-analysis`
│   ├─ Business logic → `decision-table-testing`
│   ├─ State-based behavior → `state-transition-testing`
│   └─ User workflows → `use-case-testing`
├─ Code coverage requirements → Use white-box techniques
│   ├─ Basic coverage → `statement-coverage`
│   ├─ Branch testing → `branch-coverage`
│   └─ Complex conditions → `condition-coverage`
└─ Limited documentation or time → Use experience-based techniques
    ├─ Quick testing → `error-guessing`
    └─ Exploratory → `exploratory-testing`
```

### "I need to choose a test technique"

```
What information is available?
├─ Requirements/specifications available → Black-box techniques
│   ├─ Input ranges → `equivalence-partitioning`, `boundary-value-analysis`
│   ├─ Business rules → `decision-table-testing`
│   ├─ State machines → `state-transition-testing`
│   └─ User stories → `use-case-testing`
├─ Source code available → White-box techniques
│   ├─ Coverage goals → `statement-coverage`, `branch-coverage`
│   └─ Complex logic → `condition-coverage`
└─ Limited documentation → Experience-based techniques
    └─ `error-guessing`, `exploratory-testing`
```

### "I need to plan testing activities"

```
What aspect of test planning?
├─ Overall test strategy → `test-planning` (test levels, types, approach)
├─ Effort estimation → `test-planning` (estimation techniques)
├─ Risk prioritization → `risk-based-testing` (risk analysis, test prioritization)
├─ Test organization → `test-planning` (roles, responsibilities, independence)
└─ Progress tracking → `test-planning` (monitoring, metrics, control)
```

## Knowledge Areas / Categories

Organize by priority, impact, or topic area:

| Priority | Category | Impact | Prefix/Tag |
|----------|----------|--------|------------|
| 1 | Testing Fundamentals | CRITICAL | `fundamentals-` |
| 2 | Test Techniques | CRITICAL | `techniques-` |
| 3 | Test Management | HIGH | `management-` |
| 4 | Static Testing | HIGH | `static-` |
| 5 | Test Levels and Types | HIGH | `levels-` |
| 6 | Tool Support | MEDIUM | `tools-` |

### 1. Testing Fundamentals (CRITICAL)

- `testing-principles` - Apply the seven fundamental principles of testing
- `test-process` - Follow structured test process (planning, analysis, design, implementation, execution, completion)
- `psychology-of-testing` - Understand and apply principles of effective communication in testing

### 2. Test Techniques (CRITICAL)

- `equivalence-partitioning` - Divide input domain into equivalence classes
- `boundary-value-analysis` - Test boundary conditions and edge cases
- `decision-table-testing` - Test combinations of conditions and actions
- `state-transition-testing` - Test state-based behavior and transitions
- `use-case-testing` - Test user workflows and scenarios
- `statement-coverage` - Achieve statement-level code coverage
- `branch-coverage` - Test all decision outcomes (true/false branches)
- `condition-coverage` - Test all condition outcomes in boolean expressions

### 3. Test Management (HIGH)

- `test-planning` - Create comprehensive test plans with scope, approach, resources, schedule
- `risk-based-testing` - Prioritize testing based on risk analysis
- `defect-management` - Manage defect lifecycle from discovery to closure
- `test-estimation` - Estimate test effort using appropriate techniques
- `test-monitoring` - Monitor test progress and control test activities

### 4. Static Testing (HIGH)

- `static-testing-reviews` - Conduct formal and informal reviews (walkthroughs, technical reviews, inspections)
- `static-analysis` - Use static analysis tools to find defects in code

### 5. Test Levels and Types (HIGH)

- `test-levels` - Apply appropriate test levels (unit, integration, system, acceptance)
- `test-types` - Select appropriate test types (functional, non-functional, white-box, change-related)

### 6. Tool Support (MEDIUM)

- `test-tool-selection` - Select appropriate testing tools based on needs
- `test-tool-integration` - Integrate tools into test process effectively

## Critical Anti-Patterns

### Testing Shows Absence of Defects

**Problem:** Assuming that passing tests prove the software is defect-free or ready for production.

**Incorrect approach:**

```markdown
"We ran 1000 tests and they all passed, so the software is bug-free and ready to ship."
```

**Why this is wrong:**
- Testing can only show the presence of defects, not their absence
- Exhaustive testing is impossible (too many combinations)
- Tests may not cover all scenarios or edge cases
- Defects may exist in untested areas or combinations

**Correct approach:**

```markdown
"We ran 1000 tests covering critical paths, boundary conditions, and high-risk areas. 
All tests passed, which increases our confidence. However, we acknowledge that:
- We cannot test every possible combination
- Defects may still exist in untested areas
- We should monitor production for issues
- We'll continue testing in subsequent releases"
```

**Why this is better:**
- Sets realistic expectations about what testing can achieve
- Acknowledges limitations of testing
- Encourages ongoing monitoring and improvement
- Aligns with ISTQB principle: "Testing shows the presence of defects"

### Testing Too Late in the Lifecycle

**Problem:** Starting testing only after development is complete, missing opportunities for early defect detection.

**Incorrect:**

```markdown
Development Phase → Testing Phase → Release
(All code written) → (All testing) → (Ship)
```

**Correct:**

```markdown
Requirements → Design → Development → Testing (parallel)
     ↓            ↓          ↓           ↓
  Review      Review    Unit Test   Integration Test
  Static      Static    Code Review  System Test
```

**Why this is better:**
- Early defect detection is cheaper (cost increases exponentially over time)
- Static testing finds defects before code execution
- Testers can provide feedback during design phase
- Reduces rework and schedule delays

### Ignoring Test Levels

**Problem:** Treating all testing the same without understanding different test levels and their purposes.

**Incorrect:**

```markdown
"We test everything at the system level after integration."
```

**Correct:**

```markdown
"Unit tests verify individual components in isolation.
Integration tests verify interfaces between components.
System tests verify the complete system against requirements.
Acceptance tests verify business needs are met."
```

**Why this is better:**
- Each level has specific objectives and finds different types of defects
- Early levels catch defects before they propagate
- More efficient defect detection and isolation
- Better test coverage across different perspectives

### Not Using Test Techniques Systematically

**Problem:** Creating test cases ad-hoc without systematic test design techniques.

**Incorrect:**

```markdown
Test Case 1: Enter "test" in username field
Test Case 2: Enter "123" in username field
Test Case 3: Enter "abc123" in username field
(No clear rationale for selection)
```

**Correct:**

```markdown
Using Equivalence Partitioning:
- Valid: One valid username from valid equivalence class
- Invalid: Username too short (boundary: minimum length - 1)
- Invalid: Username too long (boundary: maximum length + 1)
- Invalid: Username with invalid characters

Using Boundary Value Analysis:
- Minimum length (e.g., 3 characters)
- Minimum length - 1 (2 characters)
- Minimum length + 1 (4 characters)
- Maximum length (e.g., 20 characters)
- Maximum length - 1 (19 characters)
- Maximum length + 1 (21 characters)
```

**Why this is better:**
- Systematic coverage of input domain
- Clear rationale for test case selection
- More efficient (fewer tests with better coverage)
- Reproducible and maintainable approach

## Common Patterns / Best Practices

### Risk-Based Test Prioritization

Prioritize testing based on risk analysis to focus effort where it matters most.

**When to use:**
- Limited time or resources for testing
- Need to maximize test effectiveness
- High-risk areas identified
- Release deadlines approaching

**Example:**

```markdown
Risk Analysis:
1. High Risk: Payment processing (high impact, high probability)
   → Comprehensive testing: All black-box techniques, security testing
2. Medium Risk: User profile management (medium impact, medium probability)
   → Standard testing: Equivalence partitioning, boundary value analysis
3. Low Risk: Help documentation (low impact, low probability)
   → Basic testing: Smoke tests, exploratory testing
```

**Benefits:**
- Focuses effort on areas most likely to have defects
- Maximizes test effectiveness within constraints
- Provides rationale for test coverage decisions
- Aligns testing with business priorities

### Test Levels Strategy

Apply appropriate test levels systematically to catch defects at the right stage.

**Example:**

```markdown
Unit Level:
- Developer writes unit tests for individual functions
- Achieves statement and branch coverage
- Catches logic errors early

Integration Level:
- Test interfaces between modules
- Verify data flow and API contracts
- Catch interface mismatches

System Level:
- Test complete system against requirements
- Verify end-to-end workflows
- Catch system-level defects

Acceptance Level:
- Verify business requirements are met
- User acceptance testing (UAT)
- Confirm system is fit for purpose
```

**Benefits:**
- Defects found early are cheaper to fix
- Each level provides different perspective
- Better defect isolation and root cause analysis
- Comprehensive coverage across system layers

### Static Testing Before Dynamic Testing

Use static testing (reviews, static analysis) before dynamic testing (execution) to find defects early.

**When to use:**
- Requirements and design documents available
- Code available for review
- Need to find defects before execution
- Want to improve code quality early

**Example:**

```markdown
Requirements Review:
- Check completeness, consistency, testability
- Identify ambiguities and missing information
- Find defects before development starts

Code Review:
- Check coding standards compliance
- Identify potential bugs and security issues
- Share knowledge and improve code quality

Static Analysis:
- Automated code analysis for common issues
- Security vulnerability scanning
- Code complexity analysis
```

**Benefits:**
- Finds defects before execution (cheaper)
- Improves code quality early
- Reduces defect propagation
- Knowledge sharing and team learning

## Detailed Instructions

### Step 1: Understand Testing Fundamentals

Establish the foundation by understanding core testing principles and the test process:

- **Review the seven testing principles:**
  - Testing shows the presence of defects
  - Exhaustive testing is impossible
  - Early testing saves time and money
  - Defects cluster together
  - Beware of the pesticide paradox
  - Testing is context dependent
  - Absence of errors is a fallacy

- **Understand the test process:**
  - Test planning and control
  - Test analysis and design
  - Test implementation and execution
  - Evaluating exit criteria and reporting
  - Test closure activities

- **Apply psychology of testing:**
  - Communicate findings constructively
  - Maintain independence in testing
  - Build positive relationships with developers

**Questions to resolve:**
- What is the testing objective for this project?
- What are the exit criteria for testing?
- What level of independence is appropriate?
- How will test results be communicated?

### Step 2: Select Appropriate Test Techniques

Choose test techniques based on available information and testing objectives:

- **For functional testing with specifications:**
  - Use black-box techniques (equivalence partitioning, boundary value analysis, decision tables, state transition, use case testing)
  - Start with equivalence partitioning to identify input classes
  - Apply boundary value analysis for edge cases
  - Use decision tables for complex business rules
  - Apply state transition testing for state-based behavior

- **For code coverage requirements:**
  - Use white-box techniques (statement, branch, condition coverage)
  - Start with statement coverage for basic coverage
  - Progress to branch coverage for decision testing
  - Use condition coverage for complex boolean expressions

- **For limited documentation or exploratory testing:**
  - Use experience-based techniques (error guessing, exploratory testing)
  - Apply error guessing based on common error patterns
  - Use exploratory testing for learning and discovery

**Common pitfalls:**
- Using only one technique (combine techniques for better coverage)
- Not considering boundary conditions (always test boundaries)
- Ignoring invalid inputs (test both valid and invalid partitions)
- Not documenting test case rationale (maintain traceability)

### Step 3: Plan and Manage Testing Activities

Create comprehensive test plans and manage testing throughout the lifecycle:

- **Test planning:**
  - Define test scope and objectives
  - Identify test levels and test types
  - Estimate test effort and schedule
  - Assign roles and responsibilities
  - Define test environment requirements
  - Establish entry and exit criteria

- **Risk-based testing:**
  - Identify and analyze risks
  - Prioritize tests based on risk
  - Allocate more effort to high-risk areas
  - Review and update risk assessment

- **Test monitoring and control:**
  - Track test progress against plan
  - Monitor test metrics (coverage, defects, execution)
  - Take corrective action when needed
  - Report test status regularly

- **Defect management:**
  - Log defects with complete information
  - Classify defects by severity and priority
  - Track defect lifecycle (new, assigned, fixed, verified, closed)
  - Analyze defect trends and root causes

**Verification checklist:**
- Test plan covers all required test levels and types
- Risk analysis completed and tests prioritized
- Test progress is being monitored and reported
- Defects are being tracked and managed
- Exit criteria are defined and measurable

## Inputs

Required artifacts, data, or access needed:

- **Requirements/Specifications:** Functional and non-functional requirements, user stories, or specifications that define what to test
- **Design Documents:** System design, architecture diagrams, interface specifications for understanding system structure
- **Source Code:** For white-box testing techniques and static analysis
- **Test Basis:** Any document from which test conditions and test cases can be derived
- **Risk Analysis:** Identified risks and their priorities for risk-based testing
- **Test Environment:** Access to test environments, test data, and testing tools
- **Historical Data:** Previous test results, defect data, and metrics for estimation and planning

## Outputs

What this skill produces:

- **Test Plans:** Comprehensive test plans with scope, approach, resources, schedule, and risks
- **Test Cases:** Systematically designed test cases using appropriate test techniques
- **Test Results:** Test execution results, coverage metrics, and defect reports
- **Test Reports:** Test summary reports with status, metrics, and recommendations
- **Defect Reports:** Detailed defect information with classification and tracking
- **Test Metrics:** Coverage metrics, defect metrics, and progress metrics

**Quality criteria:**
- Test cases are traceable to requirements or test basis
- Test techniques are applied systematically with clear rationale
- Test coverage meets defined objectives (statement, branch, functional)
- Defects are documented with sufficient detail for reproduction
- Test reports provide clear status and actionable information

## Reference Index

### Rules

| File | Impact | Tags |
|------|--------|------|
| [rules/testing-principles.md](./rules/testing-principles.md) | CRITICAL | fundamentals, principles |
| [rules/test-process.md](./rules/test-process.md) | CRITICAL | fundamentals, process |
| [rules/psychology-of-testing.md](./rules/psychology-of-testing.md) | HIGH | fundamentals, communication |
| [rules/test-levels.md](./rules/test-levels.md) | HIGH | levels, strategy |
| [rules/test-types.md](./rules/test-types.md) | HIGH | levels, types |
| [rules/static-testing-reviews.md](./rules/static-testing-reviews.md) | HIGH | static, reviews |
| [rules/static-analysis.md](./rules/static-analysis.md) | MEDIUM | static, tools |
| [rules/equivalence-partitioning.md](./rules/equivalence-partitioning.md) | CRITICAL | techniques, black-box |
| [rules/boundary-value-analysis.md](./rules/boundary-value-analysis.md) | CRITICAL | techniques, black-box |
| [rules/decision-table-testing.md](./rules/decision-table-testing.md) | HIGH | techniques, black-box |
| [rules/state-transition-testing.md](./rules/state-transition-testing.md) | HIGH | techniques, black-box |
| [rules/use-case-testing.md](./rules/use-case-testing.md) | HIGH | techniques, black-box |
| [rules/statement-coverage.md](./rules/statement-coverage.md) | HIGH | techniques, white-box |
| [rules/branch-coverage.md](./rules/branch-coverage.md) | HIGH | techniques, white-box |
| [rules/condition-coverage.md](./rules/condition-coverage.md) | MEDIUM | techniques, white-box |
| [rules/error-guessing.md](./rules/error-guessing.md) | MEDIUM | techniques, experience-based |
| [rules/exploratory-testing.md](./rules/exploratory-testing.md) | MEDIUM | techniques, experience-based |
| [rules/test-planning.md](./rules/test-planning.md) | HIGH | management, planning |
| [rules/test-estimation.md](./rules/test-estimation.md) | HIGH | management, estimation |
| [rules/risk-based-testing.md](./rules/risk-based-testing.md) | HIGH | management, risk |
| [rules/test-monitoring.md](./rules/test-monitoring.md) | HIGH | management, monitoring |
| [rules/defect-management.md](./rules/defect-management.md) | HIGH | management, defects |
| [rules/test-tool-selection.md](./rules/test-tool-selection.md) | MEDIUM | tools, selection |
| [rules/test-tool-integration.md](./rules/test-tool-integration.md) | MEDIUM | tools, integration |

## How to Use

This skill uses a rule-based structure with individual rule files in the `rules/` directory and actionable command workflows in the `command/` directory. Each rule provides:

- Clear explanation of the ISTQB concept
- Incorrect vs. correct examples
- When to apply the rule
- Additional context and considerations

Commands provide step-by-step workflows for executing specific testing activities, complementing the rule-based guidance.

### Using Rules

1. **For specific guidance:** Navigate to the relevant rule file based on your need (e.g., `equivalence-partitioning.md` for input validation testing)
2. **For comprehensive coverage:** Review all rules in a category (e.g., all black-box technique rules)
3. **For quick reference:** Use the Knowledge Areas section to find relevant rules
4. **For decision making:** Use the Quick Decision Trees to navigate to appropriate rules

### Rule File Structure

Each rule file follows this structure:
- Frontmatter with impact level and tags
- Explanation of the concept
- Incorrect example with explanation
- Correct example with explanation
- When to apply
- Additional context

### Using Commands

This skill provides actionable command workflows in the `command/` directory. Commands provide step-by-step instructions for executing specific testing activities:

1. **For actionable workflows:** Use commands when you need step-by-step guidance for specific activities
2. **For test planning:** Use `create-test-plan` command to create comprehensive test plans
3. **Commands complement rules:** Commands provide workflows while rules provide guidance on what to do/not do

**Available Commands:**
- `create-test-plan` - Step-by-step workflow for creating comprehensive test plans following ISTQB standards

Commands are automatically discovered from the `command/` directory and can be invoked when agents need actionable workflows for specific testing activities.

## Examples

### Example 1: Applying Equivalence Partitioning and Boundary Value Analysis

**Context:** Testing a login form with username field that accepts 3-20 alphanumeric characters.

**Approach:**
1. Apply equivalence partitioning to identify valid and invalid partitions:
   - Valid: 3-20 alphanumeric characters
   - Invalid: Less than 3 characters
   - Invalid: More than 20 characters
   - Invalid: Non-alphanumeric characters
2. Apply boundary value analysis to test boundaries:
   - Minimum boundary: 2, 3, 4 characters
   - Maximum boundary: 19, 20, 21 characters
3. Create test cases covering each partition and boundary value

**Result:** Systematic test coverage with clear rationale for each test case, ensuring all equivalence classes and boundaries are tested.

**Key takeaway:** Combining equivalence partitioning with boundary value analysis provides comprehensive coverage of input validation with minimal test cases.

### Example 2: Risk-Based Test Prioritization

**Context:** Limited time for testing a new e-commerce feature with payment processing, product catalog, and user reviews.

**Challenge:** Need to maximize test effectiveness within time constraints.

**Solution:**
1. Conduct risk analysis:
   - High Risk: Payment processing (financial impact, security concerns)
   - Medium Risk: Product catalog (business impact, moderate complexity)
   - Low Risk: User reviews (low business impact, simple functionality)
2. Allocate test effort proportionally:
   - 60% effort on payment processing (comprehensive testing)
   - 30% effort on product catalog (standard testing)
   - 10% effort on user reviews (basic testing)
3. Apply appropriate test techniques based on risk level

**Result:** Focused testing effort on high-risk areas, with documented rationale for coverage decisions.

**Key takeaway:** Risk-based testing helps maximize test effectiveness when resources are limited, providing clear justification for test coverage decisions.

## References

- [ISTQB Foundation Level Syllabus v4.0.1](https://www.istqb.org/sdm_downloads/istqb-certified-tester-foundation-level-syllabus-v4-0/)
- [ISTQB Glossary](https://glossary.istqb.org/)
- [ISTQB Official Website](https://www.istqb.org/)

## Notes

- This skill is based on ISTQB Certified Tester Foundation Level (CTFL) syllabus v4.0.1
- Terminology follows ISTQB Glossary definitions
- Techniques and practices are aligned with ISTQB standards
- For advanced topics, consider ISTQB Advanced Level certifications
- This skill complements other QA skills in the catalog (test strategy, test planning, etc.)
