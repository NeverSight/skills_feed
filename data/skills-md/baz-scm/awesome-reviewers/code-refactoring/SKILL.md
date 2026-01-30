---
name: code-refactoring
description: The practice of restructuring and simplifying code continuously – reducing complexity, improving design, and keeping codebases clean.
version: '1.0'
---
# Code Refactoring & Simplicity

Great developers continually refactor code to make it simpler and more efficient. Over time, software accumulates complexity; refactoring is the skill of untangling that complexity. By breaking down large functions and eliminating unnecessary logic, you improve readability and reduce technical debt. Simple designs are easier to test and evolve.

## Examples
- Splitting a 300-line function that does many things into smaller helper functions each focused on one task.
- Removing duplicate code by refactoring it into a reusable module or library.

## Guidelines
- **Decompose Large Functions:** If a function is doing too much or exceeds roughly 50 lines, split it into smaller, focused functions. Each function should ideally handle one responsibility. This makes the code easier to understand and test.
- **Simplify Complex Logic:** Reduce nesting and complexity in control flow. Apply the “exit early” principle to handle edge cases upfront and avoid deep nested `if`/`else` blocks. For example, return early on error conditions instead of wrapping the main logic in an else-clause.
- **Eliminate Redundancy:** Refactor to remove duplicate or convoluted code. Break down complex boolean expressions or chained operations into simpler steps. Simplifying tricky code by using clearer constructs or standard library functions makes it more approachable and reduces potential bugs.
