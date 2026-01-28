---
name: qa-test-planner
description: Generate comprehensive test plans, manual test cases, regression test suites, and bug reports for QA engineers. Includes Figma MCP integration for design validation.
---

# QA Test Planner

A comprehensive skill for QA engineers to create test plans, generate manual test cases, build regression test suites, validate designs against Figma, and document bugs effectively.

## What This Skill Does

Helps QA engineers with:
- **Test Plan Creation** - Comprehensive test strategy and planning
- **Manual Test Case Generation** - Detailed step-by-step test cases
- **Regression Test Suites** - Critical path and smoke test suites
- **Figma Design Validation** - Compare implementation against designs (requires Figma MCP)
- **Bug Report Templates** - Clear, reproducible bug documentation
- **Test Coverage Analysis** - Identify gaps in testing
- **Test Execution Tracking** - Monitor testing progress

## Why You Need This Skill

**Without structured testing:**
- Inconsistent test coverage
- Missed edge cases
- Poor bug documentation
- No regression safety net
- Design implementation gaps
- Unclear test strategy

**With this skill:**
- Comprehensive test coverage
- Repeatable test cases
- Systematic regression testing
- Design-implementation validation
- Professional bug reports
- Clear testing roadmap

## Core Components

### 1. Test Plan Generator
- Test scope and objectives
- Testing approach and strategy
- Test environment requirements
- Entry/exit criteria
- Risk assessment
- Resource allocation
- Timeline and milestones

### 2. Manual Test Case Generator
- Step-by-step instructions
- Expected vs actual results
- Preconditions and setup
- Test data requirements
- Priority and severity
- Edge case identification

### 3. Regression Test Suite Builder
- Smoke test cases
- Critical path testing
- Integration test scenarios
- Backward compatibility checks
- Performance regression tests

### 4. Figma Design Validation (with MCP)
- Compare UI implementation to designs
- Identify visual discrepancies
- Validate spacing, colors, typography
- Check component consistency
- Flag design-dev mismatches

### 5. Bug Report Generator
- Clear reproduction steps
- Environment details
- Expected vs actual behavior
- Screenshots and evidence
- Severity and priority
- Related test cases

## Test Case Structure

### Standard Test Case Format

```markdown
## TC-001: [Test Case Title]

**Priority:** High | Medium | Low
**Type:** Functional | UI | Integration | Regression
**Status:** Not Run | Pass | Fail | Blocked

### Objective
[What are we testing and why]

### Preconditions
- [Setup requirement 1]
- [Setup requirement 2]
- [Test data needed]

### Test Steps
1. [Action to perform]
   **Expected:** [What should happen]

2. [Action to perform]
   **Expected:** [What should happen]

3. [Action to perform]
   **Expected:** [What should happen]

### Test Data
- Input: [Test data values]
- User: [Test account details]
- Configuration: [Environment settings]

### Post-conditions
- [System state after test]
- [Cleanup required]

### Notes
- [Edge cases to consider]
- [Related test cases]
- [Known issues]
```

## Test Plan Template

### Executive Summary
- Feature/product being tested
- Testing objectives
- Key risks
- Timeline overview

### Test Scope

**In Scope:**
- Features to be tested
- Test types (functional, UI, performance, etc.)
- Platforms and environments
- User flows and scenarios

**Out of Scope:**
- Features not being tested (deferred)
- Known limitations
- Third-party integrations (if applicable)

### Test Strategy

**Test Types:**
- Manual testing
- Exploratory testing
- Regression testing
- Integration testing
- User acceptance testing
- Performance testing (if applicable)

**Test Approach:**
- Black box testing
- Positive and negative testing
- Boundary value analysis
- Equivalence partitioning

### Test Environment
- Operating systems
- Browsers and versions
- Devices (mobile, tablet, desktop)
- Test data requirements
- Backend/API environments

### Entry Criteria
- [ ] Requirements documented
- [ ] Designs finalized
- [ ] Test environment ready
- [ ] Test data prepared
- [ ] Build deployed to test environment

### Exit Criteria
- [ ] All high-priority test cases executed
- [ ] 90%+ test case pass rate
- [ ] All critical bugs fixed
- [ ] No open high-severity bugs
- [ ] Regression suite passed
- [ ] Stakeholder sign-off

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to mitigate] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to mitigate] |

### Test Deliverables
- Test plan document
- Test cases
- Test execution reports
- Bug reports
- Test summary report

## Test Types and Approaches

### 1. Functional Testing

**What:** Verify features work as specified

**Test Cases:**
- Happy path scenarios
- Error handling
- Input validation
- Business logic
- Data integrity

**Example:**
```
TC: User Login with Valid Credentials
1. Navigate to login page
2. Enter valid email and password
3. Click "Login" button
Expected: User redirected to dashboard, welcome message shown
```

### 2. UI/Visual Testing

**What:** Verify visual appearance and layout

**Test Cases:**
- Layout and alignment
- Responsive design
- Color and typography
- Component states (hover, active, disabled)
- Cross-browser compatibility

**With Figma MCP:**
- Compare implementation to Figma designs
- Verify spacing (padding, margins)
- Check font sizes and weights
- Validate color values
- Ensure icon accuracy

**Example:**
```
TC: Homepage Hero Section Visual Validation
1. Open homepage in browser
2. Compare against Figma design [link]
3. Verify:
   - Heading font: 48px, bold, #1A1A1A
   - CTA button: 16px padding, #0066FF background
   - Image aspect ratio: 16:9
   - Spacing: 64px margin-bottom
Expected: All visual elements match Figma exactly
```

### 3. Regression Testing

**What:** Ensure existing functionality still works

**When to Run:**
- Before each release
- After bug fixes
- After new features
- Weekly smoke tests

**Suite Components:**
- Smoke tests (critical paths)
- Full regression (comprehensive)
- Targeted regression (affected areas)

**Example:**
```
Regression Suite: User Authentication
- Login with valid credentials
- Login with invalid credentials
- Password reset flow
- Session timeout handling
- Multi-device login
- Social login (Google, GitHub)
```

### 4. Integration Testing

**What:** Verify different components work together

**Test Cases:**
- API integration
- Database operations
- Third-party services
- Cross-module interactions
- Data flow between components

**Example:**
```
TC: Checkout Payment Integration
1. Add item to cart
2. Proceed to checkout
3. Enter payment details (Stripe)
4. Submit payment
Expected:
- Payment processed via Stripe API
- Order created in database
- Confirmation email sent
- Inventory updated
```

### 5. Exploratory Testing

**What:** Unscripted, creative testing

**Approach:**
- Charter-based exploration
- User persona simulation
- Edge case discovery
- Usability evaluation

**Session Template:**
```
Exploratory Testing Session
Charter: Explore [feature] as [user type]
Time: 60 minutes
Focus: [Area to explore]

Findings:
- [Bug/issue discovered]
- [UX concern]
- [Improvement suggestion]

Follow-up:
- [Test cases to create]
- [Bugs to file]
```

## Figma MCP Integration

### Design Validation Workflow

**Prerequisites:**
- Figma MCP server configured
- Design file access
- Figma URLs available

**Validation Process:**

1. **Get Design Specs from Figma**
```
"Get the button specifications from Figma file [URL]"
- Component: Primary Button
- Width: 120px
- Height: 40px
- Border-radius: 8px
- Background: #0066FF
- Font: 16px, Medium, #FFFFFF
```

2. **Compare Implementation**
```
TC: Primary Button Visual Validation
1. Inspect primary button in browser dev tools
2. Compare against Figma specs:
   - Dimensions: 120x40px ✓ / ✗
   - Border-radius: 8px ✓ / ✗
   - Background color: #0066FF ✓ / ✗
   - Font: 16px Medium #FFFFFF ✓ / ✗
3. Document discrepancies
```

3. **Create Bug if Mismatch**
```
BUG: Primary button color doesn't match design
Severity: Medium
Expected (Figma): #0066FF
Actual (Implementation): #0052CC
Screenshot: [attached]
Figma link: [specific component]
```

### Design-Dev Handoff Checklist

**Using Figma MCP:**
- [ ] Retrieve spacing values from design
- [ ] Verify color palette matches
- [ ] Check typography specifications
- [ ] Validate component states (hover, active, disabled)
- [ ] Confirm breakpoint behavior
- [ ] Review iconography and assets
- [ ] Check accessibility annotations

## Bug Reporting Best Practices

### Effective Bug Report Template

```markdown
# BUG-[ID]: [Clear, specific title]

**Severity:** Critical | High | Medium | Low
**Priority:** P0 | P1 | P2 | P3
**Type:** Functional | UI | Performance | Security
**Status:** Open | In Progress | Fixed | Closed

## Environment
- **OS:** [Windows 11, macOS 14, etc.]
- **Browser:** [Chrome 120, Firefox 121, etc.]
- **Device:** [Desktop, iPhone 15, etc.]
- **Build:** [Version/commit]
- **URL:** [Page where bug occurs]

## Description
[Clear, concise description of the issue]

## Steps to Reproduce
1. [Specific step]
2. [Specific step]
3. [Specific step]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Visual Evidence
- Screenshot: [attached]
- Video: [link if applicable]
- Console errors: [paste errors]
- Network logs: [if relevant]

## Impact
- **User Impact:** [How many users affected]
- **Frequency:** [Always, Sometimes, Rarely]
- **Workaround:** [If one exists]

## Additional Context
- Related to: [Feature/ticket]
- First noticed: [When]
- Regression: [Yes/No - if yes, since when]
- Figma design: [Link if UI bug]

## Test Cases Affected
- TC-001: [Test case that failed]
- TC-045: [Related test case]
```

### Bug Severity Definitions

**Critical (P0):**
- System crash or data loss
- Security vulnerability
- Complete feature breakdown
- Blocks release

**High (P1):**
- Major feature not working
- Significant user impact
- No workaround available
- Should fix before release

**Medium (P2):**
- Feature partially working
- Workaround available
- Minor user inconvenience
- Can ship with fix in next release

**Low (P3):**
- Cosmetic issues
- Rare edge cases
- Minimal impact
- Nice to have fixed

## Test Coverage Analysis

### Coverage Metrics

**Feature Coverage:**
```
Total Features: 25
Tested: 23
Not Tested: 2
Coverage: 92%
```

**Requirement Coverage:**
```
Total Requirements: 150
With Test Cases: 142
Without Test Cases: 8
Coverage: 95%
```

**Risk Coverage:**
```
High-Risk Areas: 12
Tested: 12
Medium-Risk: 35
Tested: 30
```

### Coverage Matrix

| Feature | Requirements | Test Cases | Status | Gaps |
|---------|--------------|------------|--------|------|
| Login | 8 | 12 | ✓ Complete | None |
| Checkout | 15 | 10 | ⚠ Partial | Payment errors |
| Dashboard | 12 | 15 | ✓ Complete | None |

## Regression Test Suite Structure

### Smoke Test Suite (15-30 min)
**Run:** Before every test cycle, daily builds

**Critical Paths:**
- User login/logout
- Core user flow (e.g., create order)
- Navigation and routing
- API health checks
- Database connectivity

**Example:**
```
SMOKE-001: Critical User Flow
1. Login as standard user
2. Navigate to main feature
3. Perform primary action
4. Verify success message
5. Logout
Expected: All steps complete without errors
```

### Full Regression Suite (2-4 hours)
**Run:** Weekly, before releases

**Coverage:**
- All functional test cases
- Integration scenarios
- UI validation
- Cross-browser checks
- Data integrity tests

### Targeted Regression (30-60 min)
**Run:** After bug fixes, feature updates

**Coverage:**
- Affected feature area
- Related components
- Integration points
- Previously failed tests

## Test Execution Tracking

### Test Run Template

```markdown
# Test Run: [Release Version]

**Date:** 2024-01-15
**Build:** v2.5.0-rc1
**Tester:** [Name]
**Environment:** Staging

## Summary
- Total Test Cases: 150
- Executed: 145
- Passed: 130
- Failed: 10
- Blocked: 5
- Not Run: 5
- Pass Rate: 90%

## Test Cases by Priority

| Priority | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| P0 (Critical) | 25 | 23 | 2 | 0 |
| P1 (High) | 50 | 45 | 3 | 2 |
| P2 (Medium) | 50 | 45 | 3 | 2 |
| P3 (Low) | 25 | 17 | 2 | 1 |

## Failures

### Critical Failures
- TC-045: Payment processing fails
  - Bug: BUG-234
  - Status: Open

### High Priority Failures
- TC-089: Email notification not sent
  - Bug: BUG-235
  - Status: In Progress

## Blocked Tests
- TC-112: Dashboard widget (API endpoint down)
- TC-113: Export feature (dependency not deployed)

## Risks
- 2 critical bugs blocking release
- Payment integration needs attention
- Email service intermittent

## Next Steps
- Retest after BUG-234 fix
- Complete remaining 5 test cases
- Run full regression before sign-off
```

## Using This Skill

### Generate Test Plan

```bash
./scripts/generate_test_plan.sh
```

Interactive workflow for creating comprehensive test plans.

### Generate Manual Test Cases

```bash
./scripts/generate_test_cases.sh
```

Create manual test cases for features with step-by-step instructions.

### Build Regression Suite

```bash
./scripts/build_regression_suite.sh
```

Create smoke and regression test suites.

### Validate Design with Figma

**With Figma MCP configured:**
```
"Compare the login page implementation against the Figma design at [URL] and generate test cases for visual validation"
```

### Create Bug Report

```bash
./scripts/create_bug_report.sh
```

Generate structured bug reports with all required details.

### Access Templates

```
references/test_case_templates.md - Various test case formats
references/bug_report_templates.md - Bug documentation templates
references/regression_testing.md - Regression testing guide
references/figma_validation.md - Design validation with Figma MCP
```

## QA Process Workflow

### 1. Planning Phase
- [ ] Review requirements and designs
- [ ] Create test plan
- [ ] Identify test scenarios
- [ ] Estimate effort and timeline
- [ ] Set up test environment

### 2. Test Design Phase
- [ ] Write test cases
- [ ] Review test cases with team
- [ ] Prepare test data
- [ ] Build regression suite
- [ ] Get Figma design access

### 3. Test Execution Phase
- [ ] Execute test cases
- [ ] Log bugs with clear reproduction steps
- [ ] Validate against Figma designs (UI tests)
- [ ] Track test progress
- [ ] Communicate blockers

### 4. Reporting Phase
- [ ] Compile test results
- [ ] Analyze coverage
- [ ] Document risks
- [ ] Provide go/no-go recommendation
- [ ] Archive test artifacts

## Best Practices

### Test Case Writing

**DO:**
- ✅ Be specific and unambiguous
- ✅ Include expected results for each step
- ✅ Test one thing per test case
- ✅ Use consistent naming conventions
- ✅ Keep test cases maintainable

**DON'T:**
- ❌ Assume knowledge
- ❌ Make test cases too long
- ❌ Skip preconditions
- ❌ Forget edge cases
- ❌ Leave expected results vague

### Bug Reporting

**DO:**
- ✅ Provide clear reproduction steps
- ✅ Include screenshots/videos
- ✅ Specify exact environment details
- ✅ Describe impact on users
- ✅ Link to Figma for UI bugs

**DON'T:**
- ❌ Report without reproduction steps
- ❌ Use vague descriptions
- ❌ Skip environment details
- ❌ Forget to assign priority
- ❌ Duplicate existing bugs

### Regression Testing

**DO:**
- ✅ Automate repetitive tests when possible
- ✅ Maintain regression suite regularly
- ✅ Prioritize critical paths
- ✅ Run smoke tests frequently
- ✅ Update suite after each release

**DON'T:**
- ❌ Skip regression before releases
- ❌ Let suite become outdated
- ❌ Test everything every time
- ❌ Ignore failed regression tests

## Figma MCP Setup

### Configuration

**Install Figma MCP server:**
```bash
# Follow Figma MCP installation instructions
# Configure with your Figma API token
# Set file access permissions
```

**Usage in test planning:**
```
"Analyze the Figma design file at [URL] and generate visual validation test cases for:
- Color scheme compliance
- Typography specifications
- Component spacing
- Responsive breakpoints
- Interactive states"
```

**Example queries:**
```
"Get button specifications from Figma design [URL]"
"Compare navigation menu implementation against Figma design"
"Extract spacing values for dashboard layout from Figma"
"List all color tokens used in Figma design system"
```

## Test Case Examples

### Example 1: Login Flow

```markdown
## TC-LOGIN-001: Valid User Login

**Priority:** P0 (Critical)
**Type:** Functional
**Estimated Time:** 2 minutes

### Objective
Verify users can successfully login with valid credentials

### Preconditions
- User account exists (test@example.com / Test123!)
- User is not already logged in
- Browser cookies cleared

### Test Steps
1. Navigate to https://app.example.com/login
   **Expected:** Login page displays with email and password fields

2. Enter email: test@example.com
   **Expected:** Email field accepts input

3. Enter password: Test123!
   **Expected:** Password field shows masked characters

4. Click "Login" button
   **Expected:**
   - Loading indicator appears
   - User redirected to /dashboard
   - Welcome message shown: "Welcome back, Test User"
   - Avatar/profile image displayed in header

### Post-conditions
- User session created
- Auth token stored
- Analytics event logged

### Visual Validation (with Figma)
- Compare dashboard layout against Figma design [link]
- Verify welcome message typography: 24px, Medium, #1A1A1A
- Check avatar size: 40x40px, border-radius 50%

### Edge Cases to Consider
- TC-LOGIN-002: Invalid password
- TC-LOGIN-003: Non-existent email
- TC-LOGIN-004: SQL injection attempt
- TC-LOGIN-005: Very long password
```

### Example 2: Responsive Design Validation

```markdown
## TC-UI-045: Mobile Navigation Menu

**Priority:** P1 (High)
**Type:** UI/Responsive
**Devices:** Mobile (iPhone, Android)

### Objective
Verify navigation menu works correctly on mobile devices

### Preconditions
- Access from mobile device or responsive mode
- Viewport width: 375px (iPhone SE) to 428px (iPhone Pro Max)

### Test Steps
1. Open homepage on mobile device
   **Expected:** Hamburger menu icon visible (top-right)

2. Tap hamburger icon
   **Expected:**
   - Menu slides in from right
   - Overlay appears over content
   - Close (X) button visible

3. Tap menu item
   **Expected:** Navigate to section, menu closes

4. Compare against Figma mobile design [link]
   **Expected:**
   - Menu width: 280px
   - Slide animation: 300ms ease-out
   - Overlay opacity: 0.5, color #000000
   - Font size: 16px, line-height 24px

### Breakpoints to Test
- 375px (iPhone SE)
- 390px (iPhone 14)
- 428px (iPhone 14 Pro Max)
- 360px (Galaxy S21)
```

## Summary

This QA Test Planner skill provides:
- **Structured test planning** - Comprehensive test strategies
- **Manual test case generation** - Detailed, repeatable tests
- **Regression testing** - Protect against breaking changes
- **Figma validation** - Design-implementation verification
- **Bug documentation** - Clear, actionable reports
- **Coverage analysis** - Identify testing gaps

**Remember:** Quality is everyone's responsibility, but QA ensures it's systematically verified.

---

**"Testing shows the presence, not the absence of bugs." - Edsger Dijkstra**

**"Quality is not an act, it is a habit." - Aristotle**
