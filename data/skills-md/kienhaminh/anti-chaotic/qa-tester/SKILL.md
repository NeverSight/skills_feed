---
name: qa-tester
description: Use when planning tests, creating test cases, reporting bugs, or executing Unit/E2E/Security/Performance tests.
version: "1.3"
allowed-tools: read_file list_dir search_web browser_subagent
---

# QA Testing Standards

This skill provides expert QA standards and workflows for ensuring high-quality software delivery through comprehensive test strategies, plans, and cases.

## CRITICAL: Source of Truth

1.  **Docs First**: You **MUST** strictly base all your testing work (plans, cases, bug reports) on the documentation found in the `docs/` folder of the current project.
2.  **Verify**: Read all files in `docs/` before proposing any test strategy.
3.  **Missing/Conflict**: If the `docs/` folder is missing, empty, or contradicts the code significantly, you **MUST STOP and CONFIRM** with the user immediately using `notify_user`. Do not assume requirements.

## Core Capabilities

You are capable of defining and guiding the implementation of:

1.  **Test Execution**: Reading existing test cases (`docs/035-QA/Test-Cases/`) and executing them via `browser_subagent` or automation.
2.  **Detailed Test Cases**: Creating step-by-step, reproducible test scripts.
3.  **Unit Tests**: Logic verification (e.g., specific functions, utils).
4.  **E2E Tests**: User flow verification (e.g., checkout, login).
5.  **Security Tests**: Vulnerability assessments (OWASP, Auth flaws).
6.  **Performance Tests**: Load and responsiveness checks.
7.  **Full-Stack Automation**: Writing production-ready test code (Playwright, Jest, etc.).
8.  **Human Simulation**: Using the `browser_subagent` for exploratory testing and visual verification.
9.  **Autonomous Loop**: Self-correcting test execution and reporting.

## Workflow

### 1. Test Discovery & Planning

Before writing new tests, **CHECK** if they already exist.

1.  **Search**: Look in `docs/035-QA/Test-Cases/` (or similar standard paths).
2.  **Found?**: If test case files exist (e.g., `TC-Login-001.md`), read them. Your goal is to **Execute** these steps.
3.  **Not Found?**: Analyze `docs/` requirements and **Generate** new test cases using `references/test_case_standards.md`.

### 2. Execution Strategy (The How-To)

Don't just read; analyze using these specific techniques:

- **Technique A: Noun-Verb Extraction**
  - Scan docs for **Nouns** (Entities like "User", "Order", "Cart") and **Verbs** (Actions like "Register", "Checkout", "Add").
  - _Output_: A list of objects and the actions that can be performed on them. Each Action = At least 1 Test Case.
- **Technique B: Keyword Permutations**
  - Look for constraints: "MUST", "CANNOT", "ONLY IF", "MAXIMUM".
  - _Action_: Create a test for the constraint being met, AND a test for the constraint being violated.
- **Technique C: State Transition Mapping**
  - If an entity has states (e.g., Order: Pending -> Paid -> Shipped), draw the flow.
  - _Test_: Verify valid transitions (Pending -> Paid) AND invalid transitions (Shipped -> Pending).
- **Step 1.4 - Gap Analysis**: Identify missing definitions. If a flow is mentioned but not detailed (e.g., "User pays subscription"), **STOP and CONFIRM** with the user before assuming logic.

### 2. Comprehensive Test Design

You MUST use the **Standard Test Case Format** defined in `references/test_case_standards.md`.

**For each identified requirement, generate a detailed test case including:**

- **ID**: `TC-[Module]-[Number]` (e.g., `TC-AUTH-001`)
- **Pre-conditions**: Exact state required (e.g., "User is logged in as Admin").
- **Test Data**: Specific inputs (e.g., "Email: test@example.com", not "valid email").
- **Steps**: Numbered, atomic actions.
- **Expected Result**: Verifiable outcome for _each_ critical step.

**Coverage Rules**:

- **Happy Path**: The "Golden Flow" (e.g., User logs in with valid creds).
- **Negative Path**: The "Rainy Day" (e.g., User logs in with wrong password).
- **Boundary** (Unit/Logic): Off-by-one errors (0 items, 1 item, Max items).
- **Edge Cases** (System): Network timeout, Database down, Concurrent edits.

**Cross-Module Logic (Integration)**:

- Explicitly define test cases that span multiple modules.
- _Example_: "Create Order (Order Module) -> Reduce Inventory (Inventory Module) -> Charge Card (Payment Module) -> Email User (Notification Module)".
- **Transactional Integrity**: Verify that if step 3 fails, steps 1 and 2 are rolled back.

### 3. Execution & Autonomy (The Loop)

**Execution Workflow**:

1.  **Select Method**:
    - **Manual/Ad-hoc**: Use `browser_subagent` to physically click through the steps defined in the Test Case.
    - **Automated**: Convert the Markdown Test Case into a Playwright script (refer to `references/automation/playwright.md`).
2.  **Run It**: Execute the subagent or the script.
3.  **Analyze Failure**:
    - If `browser_subagent` fails: Report the visual/interactive issue.
    - If code fails: Fix the script or report the bug.
4.  **Report**: Log results in `docs/035-QA/Reports/` using `test_report_template.md`.

### 4. Advanced & Niche Testing

**Refer to the dedicated guides in `references/` for detailed philosophy and patterns:**

- **Detailed Standards**: [Test Case Standards](references/test_case_standards.md) - _Core Philosophy: "No Ambiguity"_
- **Unit Tests**: [Unit Testing Guide](references/unit_testing.md) - _Core Philosophy: "Test Behavior, Not Implementation"_
- **Integration Tests**: [Integration Testing Guide](references/integration_testing.md) - _Core Philosophy: "Verify the Handshake"_
- **E2E Tests**: [E2E Testing Guide](references/e2e_testing.md) - _Core Philosophy: "Simulate the Real User"_
- **Security Tests**: [Security Testing Guide](references/security_testing.md) - _Core Philosophy: "Trust No Input"_
- **Performance Tests**: [Performance Testing Guide](references/performance_testing.md) - _Core Philosophy: "Performance is a Feature"_
- **Automation Practices**: [Best Practices](references/automation/best_practices.md) - _Core Philosophy: "Robust & Resilient"_
- **Human Simulation**: [Agent Browser Guide](references/agent_browser.md) - _Core Philosophy: "See what the user sees"_
- **(Optional) Accessibility**: [Accessibility Guide](references/accessibility_testing.md)
- **(Optional) Visual**: [Visual Testing Guide](references/visual_testing.md)

## Deliverable Quality

- **Bug Reports**: Must include "Steps to Reproduce", "Expected Result" (citing doc), and "Actual Result".
- **Final Report**: Use [Test Report Template](references/test_report_template.md) for cycle summaries.
- **Code Examples**: When generating test code, match the existing project's style and frameworks.

## Templates

| Template | Path                    | Purpose                                                                                     |
| -------- | ----------------------- | ------------------------------------------------------------------------------------------- |
| UAT Plan | `templates/uat-plan.md` | UAT Plan - test strategy, test cases, defect log, sign-off. Use for User Acceptance Testing |
