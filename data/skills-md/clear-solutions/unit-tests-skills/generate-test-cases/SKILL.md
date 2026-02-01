---
name: generate-test-cases
description: Analyze code and generate a structured list of test cases following battle-tested INCLUDE/EXCLUDE rules. Outputs Given-When-Then format covering all code branches. Use before writing actual tests.
allowed-tools: Read, Glob, Grep
---

# Generate Test Cases Skill

You will analyze code and generate a list of test cases that should be written for a given method/class.

**IMPORTANT:** This command should be run BEFORE `/generate-tests` to ensure test cases follow the rules.

---

## Rules Reference

**CRITICAL: You MUST read and apply all rules from the following files before generating test cases:**

### General Rules (Always Apply)
- `./rules/general/test-case-generation-strategy.md` - INCLUDE/EXCLUDE criteria for test cases
- `./rules/general/naming-conventions.md` - Test naming format
- `./rules/general/general-principles.md` - Core testing principles
- `./rules/general/what-makes-good-test.md` - Clarity, Completeness, Conciseness, Resilience
- `./rules/general/keep-tests-focused.md` - One scenario per test
- `./rules/general/test-behaviors-not-methods.md` - Separate tests for behaviors
- `./rules/general/prefer-public-apis.md` - Test public APIs over private methods

---

## Output Format

For each test case, provide:

```
## Test Cases for {ClassName}.{methodName}

### 1. {testMethodName}
- **Given:** {preconditions/input state}
- **When:** {action being tested}
- **Then:** {expected outcome}
- **Code branch:** {which code path this covers}

### 2. {testMethodName}
...
```

### Naming Convention
Test method name format: `{testedMethod}_{givenState}_{expectedOutcome}`

Examples:
- `calculateTotal_validProducts_returnsSum`
- `calculateTotal_emptyList_throwsIllegalArgumentException`
- `getUser_unauthorized_returns401`
- `getUser_forbidden_returns403`

---

## Instructions

When this command is invoked, generate test cases for the specified target:

**Target to analyze:** $ARGUMENTS

**Steps:**
1. **Read the rules** from `./rules/general/` directory
2. Read the source file/class/method specified above
3. Analyze ALL code branches, including:
   - Success paths
   - Error/exception paths
   - Validation logic
   - Private/protected methods called by the target
   - Security annotations (if present)
4. Apply the INCLUDE/EXCLUDE rules strictly
5. Output the list of test cases in the specified format
6. Do NOT generate actual test code - only the test case descriptions

---

## After Generating Test Cases

**If the original user request was "generate tests" (not just "generate test cases"):**
- After outputting test cases, use the **AskUserQuestion tool** to ask for permission:
  ```
  Question: "Test cases are ready. Proceed with generating test code?"
  Header: "Next step"
  Options:
    - Label: "Yes, generate tests" / Description: "Proceed to run /generate-tests and create test files"
    - Label: "No, stop here" / Description: "Review test cases first, generate tests later manually"
  ```
- If user selects "Yes", invoke `/generate-tests` with the same target
- If user selects "No", STOP

**If the original user request was only "generate test cases":**
- After outputting test cases, add a helpful note at the end:
  > "To generate actual test code from these test cases, run `/generate-tests <target>`"
- Do NOT use AskUserQuestion - just provide the hint as text