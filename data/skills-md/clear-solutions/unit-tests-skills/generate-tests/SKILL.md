---
name: generate-tests
description: Generate high-quality unit tests from test cases. Applies proven testing principles like Given-When-Then structure, focused tests, clean test data, and behavior-driven testing. Supports multiple languages with specialized rules for Java.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Generate Tests Skill

You will create automated tests for a given method and its test cases.

## ⚠️ MANDATORY PREREQUISITE

**STOP! Before generating any test code, you MUST first run `/generate-test-cases`.**

This is NOT optional. The two-step process is REQUIRED:
1. **FIRST:** Run `/generate-test-cases <target>` - outputs the list of test cases
2. **THEN:** Run `/generate-tests <target>` - generates actual test code

**Why this matters:**
- Test cases ensure proper coverage based on INCLUDE/EXCLUDE rules
- Prevents missing edge cases and error scenarios
- Ensures consistent naming following conventions
- Allows review of test strategy before writing code

**If test cases were NOT generated first:**
You MUST invoke `/generate-test-cases` NOW before proceeding. Do NOT skip this step.

---

## Rules Reference

**CRITICAL: You MUST read and apply all relevant rules from the `./rules/tests/` directory:**

### General Rules (Always Apply)
- `general/test-case-generation-strategy.md` - INCLUDE/EXCLUDE criteria
- `general/naming-conventions.md` - Test naming format
- `general/general-principles.md` - Core testing principles (Given-When-Then, actual/expected)
- `general/technology-stack-detection.md` - Detect language and framework
- `general/what-makes-good-test.md` - Clarity, Completeness, Conciseness, Resilience
- `general/cleanly-create-test-data.md` - Use helpers and builders for test data
- `general/keep-cause-effect-clear.md` - Effects follow causes immediately
- `general/no-logic-in-tests.md` - KISS > DRY, avoid logic in assertions
- `general/keep-tests-focused.md` - One scenario per test
- `general/test-behaviors-not-methods.md` - Separate tests for behaviors
- `general/verify-relevant-arguments-only.md` - Only verify relevant mock arguments
- `general/prefer-public-apis.md` - Test public APIs over private methods

### Java Unit Tests
- `java/unit/java-test-template.md` - Basic template, FORBIDDEN annotations
- `java/unit/json-serialization.md` - Use explicit JSON literals
- `java/unit/argument-matching.md` - Use ArgumentCaptor, not any()
- `java/unit/logging-rules.md` - OutputCaptureExtension for logs
- `java/unit/domain-service-rules.md` - Mockito patterns

### Post-Generation
- `post-generation/compilation-verification.md` - Verify compilation

---

## Instructions

When this command is invoked, generate tests for the specified target:

**Target to test:** $ARGUMENTS

**Steps:**
1. **VERIFY test cases exist** - If `/generate-test-cases` was NOT run, STOP and run it first
2. **Read the relevant rules** from `./rules/tests/` based on code type
3. Read the source file/class/method specified above
4. Analyze the code to determine the type (controller, service, repository, messaging, etc.)
5. Apply the appropriate rules from the rules directory
6. Generate comprehensive tests following all rules and the test cases list
7. Create the test file(s) in the correct location using the Write tool
8. Run compilation and fix any issues until tests compile successfully