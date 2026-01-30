---
name: testing-debugging
description: Ensuring software correctness and reliability by writing automated tests, using quality assurance tools, and systematically debugging issues.
version: '1.0'
---
# Testing & Debugging

Writing robust software requires verifying that it works as intended. Developers are expected to build automated tests for their code and use debugging skills to quickly isolate issues. Thorough testing (unit tests, integration tests, etc.) gives confidence that changes won’t break existing functionality. It’s far cheaper to catch bugs early with tests or static analysis than in production.

## Examples
- Implementing a suite of unit tests for each new feature, and running them in a CI pipeline on each commit.
- Using a debugger or logging to track down the root cause of a bug, then adding a test to prevent regression.

## Guidelines
- **Automated Testing:** Write tests to cover your code’s behavior – unit tests for individual functions, integration tests for components, etc. Aim for meaningful coverage of critical paths and edge cases. This ensures your code is correct and stays correct as it evolves.
- **Quality Tools:** Employ linters and formatters to catch issues and enforce standards automatically. For example, use ESLint or Prettier so style issues are fixed upfront, freeing code reviews to focus on logic. Use static analysis and security scanners to find flaws early.
- **Systematic Debugging:** When bugs arise, debug methodically. Reproduce issues in a controlled environment, use breakpoints or logging to inspect state, and bisect changes if necessary. Once fixed, add tests for those cases to avoid regressions. A disciplined debugging approach saves time and builds more reliable software.
