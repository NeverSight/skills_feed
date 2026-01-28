---
name: code-review-assistant
description: Perform structured, actionable code reviews for Python code with clear findings and suggestions.
---

# Code Review Assistant (Python)

## Quick start
- Read the full code to understand intent, architecture, and interactions before commenting.
- Check style, correctness, edge cases, efficiency, security, and maintainability.
- Provide concise, actionable feedback grouped into strengths, issues/risks, and suggestions.
- Include inline code snippets when helpful; ensure recommendations explain the why.
- Follow `references/code_review_rules.md` for the review checklist and output format.

## Workflow
1) **Understand**  
   - Identify the module’s purpose, main flows, and dependencies.  
   - Note assumptions, data shapes, and external interactions.

2) **Assess quality and correctness**  
   - Validate logic against intent; check edge cases, error handling, and state changes.  
   - Verify PEP 8 compliance, naming, imports, and type hints.  
   - Look for dead code, mutable defaults, and duplicated logic.

3) **Evaluate design and efficiency**  
   - Check function/class responsibilities, cohesion, and complexity.  
   - Consider algorithmic complexity and data structure choices; flag inefficiencies.  
   - Ensure configuration/secrets are not hardcoded and that dependencies are isolated.

4) **Security and safety**  
   - Identify risky patterns: unsafe I/O, injection risks, use of `eval/exec/pickle`, or leaked secrets.  
   - Recommend safer alternatives when applicable.

5) **Testing and output**  
   - Check test coverage, mocking of I/O, and CI hooks if visible.  
   - Produce the review using the output format in the rules doc with grouped strengths, risks, and suggestions.

## Reference
- `references/code_review_rules.md`: detailed checklist and response format for Python code reviews.
