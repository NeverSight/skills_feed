---
name: tdd-workflow
description: Use this skill whenever you are implementing a feature using TDD.
---

The goal of this skill is to implement a true test driven development workflow. This means:

1. Writing the simplest test for ONE discrete piece of functionality.
2. Run the new test and verify that it fails as expected.
3. Write the minimal amount of code needed to make the test pass.
4. Run the test to verify it passes.
5. Once tests pass, look for opportunities to refactor.
6. Run tests once again to verify refactoring didn't break anything.

Repeat this until you've completed the functionality desired.

Remember to never do any of the following:
1. Write an entire test file up front.
2. Implement more than one discrete piece of functionality at a time.
