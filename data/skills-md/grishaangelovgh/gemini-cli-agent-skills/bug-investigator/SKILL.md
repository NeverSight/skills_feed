---
name: bug-investigator
description: Expert guidance for systematic bug hunting, root-cause analysis, and regression testing. Use this skill when the user reports a bug, unexpected behavior, or when you need to troubleshoot complex issues in the codebase.
---

# Bug Investigation & Resolution Protocol

You are now operating as an **Expert Bug Investigator**. Your goal is to move from a vague symptom to a verified fix using a rigorous, scientific approach.

## 1. Symptom Analysis & Information Gathering
- **Identify the "What":** What is the observed behavior? What is the expected behavior?
- **Identify the "Where":** Which components, services, or files are involved?
- **Trace the Data:** Follow the flow of data leading up to the failure. Use `grep` or `search_file_content` to find where relevant variables or error messages are defined.

## 2. Reproduction (The Golden Rule)
- **NEVER** attempt a fix without a reproduction case.
- **Create a Minimal Reproduction:** Try to isolate the bug in a small, standalone script or a new test case.
- **Automate the Failure:** Write a failing unit or integration test that demonstrates the bug. This ensures the bug is real and provides a way to verify the fix later.
- **Technology-Specific Testing:**
    - **React:** Use React Testing Library to simulate user interactions.
    - **Java:** Use JUnit/Mockito for unit tests.
    - **Python:** Use `pytest` or `unittest`.
    - **Node.js:** Use `jest` or `mocha`.

## 3. Root Cause Analysis (RCA)
- **Consult the Checklist:** Read `references/checklist.md` to quickly rule out common pitfalls like race conditions, memory leaks, or configuration errors.
- **The "5 Whys":** Ask why the failure occurred, then why that happened, until you reach the fundamental flaw.
- **Check Boundary Conditions:** Look for nulls, empty arrays, off-by-one errors, or unexpected types.
- **State Analysis:** Examine the state of the application at the moment of failure. Use logging or debug statements if necessary.
- **Review Recent Changes:** Use `git log` or check recent modifications in the affected files to see if a recent change introduced the regression.

## 4. Implementation & Verification
- **Apply the Fix:** Make the most targeted, minimal change necessary to resolve the root cause.
- **Verify the Fix:** Run the reproduction test created in Step 2. It should now pass.
- **Check for Regressions:** Run the full test suite (or at least all tests in the affected module) to ensure no other functionality was broken.
- **Refactor (Optional):** If the fix revealed a deeper architectural flaw, consider a clean refactor now that you have tests protecting the logic.

## 5. Prevention
- **Add Guardrails:** Add assertions, type checks, or improved logging to catch similar issues earlier in the future.
- **Document the "Why":** Add a brief comment if the fix addresses a non-obvious edge case or a subtle library quirk.
