---
name: prompt-improver
description: A skill for improving prompts by applying general LLM/agent best practices. When the user provides a prompt, this skill outputs an improved version, identifies missing information, and provides specific improvement points. Use when the user asks to "improve this prompt", "review this prompt", or "make this prompt better".
---

# Prompt Improver

## Overview

A skill that analyzes and improves prompts based on general LLM/agent best practices. It focuses on verifiability, clear scope, explicit constraints, and context economy so the agent can execute with minimal back-and-forth.

If you are running in Claude Code, also read `references/claude.md` and apply the additional Claude-specific techniques.
If you are running in Codex CLI, also read `references/codex.md` and apply the additional Codex-specific techniques.

When the input is a document that instructs an agent (e.g., plan files, AGENTS.md, system instruction docs), treat the document as the improvement target; identify issues and propose concrete improvements, and include a revised draft when helpful.

## Workflow

### Step 0: Classify Task and Complexity

Classify the task and decide whether an explicit exploration/planning phase should be recommended:

- Task type: bugfix, feature, refactor, research, UI/visual, docs, ops
- Complexity: single-file/small change vs multi-file/uncertain impact
- Risk: data safety, security, compatibility, performance
- Input type: prompt vs agent-instruction document (plan files, AGENTS.md, system instruction docs)

If the task is complex or ambiguous, the improved prompt should explicitly request an exploration/planning phase before implementation.

### Step 1: Analyze the Prompt

Analyze the user-provided prompt from the following perspectives:

1. **Verifiability**: Does it include means for Claude to verify its own work?
2. **Specificity**: Are files, scenarios, and constraints clearly specified?
3. **Context**: Is necessary background information provided?
4. **Scope**: Is the task scope appropriately defined?
5. **Expected Outcome**: Are success criteria clear?
6. **Constraints**: Are language/runtime versions, dependencies, security, or compatibility requirements specified?
7. **Context Economy**: Is the prompt concise and focused, without unnecessary information?
8. **Execution Preference**: Is it clear whether the model should implement, propose, or just analyze?

### Step 2: Identify Issues

Check for the following anti-patterns:

| Anti-pattern | Description |
|--------------|-------------|
| Vague instructions | Lacks specificity like "make it better" or "improve it" |
| No verification method | Missing tests, screenshots, or expected output |
| No verification commands | Missing how to run tests or check outputs |
| Overly broad scope | Asking for too many things at once |
| Insufficient context | Missing file paths, error messages, or references to existing patterns |
| Symptom-only description | Not requesting investigation of root cause |
| Missing constraints | No environment, dependency, or compatibility requirements |
| No exploration/planning cue | Complex tasks not asking for exploration/planning first |
| Context bloat | Unnecessary details that increase token usage |
| Ambiguous deliverable | Unclear whether to plan, implement, or only analyze |
| Unclear response format | Missing brevity/structure expectations |

### Step 3: Create Improved Prompt

Apply best practices to create an improved version:

#### Add Verifiability
```
Before: "implement a function that validates email addresses"
After: "write a validateEmail function. test cases: user@example.com is true, invalid is false, user@.com is false. run the tests after implementing"
```

#### Add Specific Context
```
Before: "fix the login bug"
After: "users report that login fails after session timeout. check the auth flow in src/auth/, especially token refresh. write a failing test that reproduces the issue, then fix it"
```

#### Add Reference to Existing Patterns
```
Before: "add a calendar widget"
After: "look at how existing widgets are implemented on the home page to understand the patterns. HotDogWidget.php is a good example. follow the pattern to implement a new calendar widget with month selection and pagination"
```

#### Add Context Economy
```
Before: "here is a long unrelated history ... fix the dropdown"
After: "fix the dropdown in src/ui/Dropdown.tsx. issue: keyboard navigation skips items. keep the prompt focused; omit unrelated history"
```

#### Add Rich Context Inputs
```
Before: "build fails"
After: "build fails with this error: [paste error]. run the smallest relevant test command. if needed, read the build script and package config"
```

#### Add Explicit Exploration/Planning When Needed
```
Before: "refactor auth to support OAuth"
After: "first explore src/auth and summarize current flow, then propose a plan. after approval, implement with tests"
```

When information is missing, include explicit questions inside the improved prompt and do not assume defaults.

#### Example: Bugfix
```
Before: "search is broken"
After: "users report search returns empty results for queries with hyphens. reproduce in src/search/. paste the error log if any. write a failing test for 'foo-bar' returning results, fix the root cause, run: pnpm test --filter search"
```

#### Example: UI/Visual
```
Before: "make the dashboard look better"
After: "implement the attached screenshot for the dashboard header in src/ui/DashboardHeader.tsx. match spacing and typography. take a new screenshot and list any differences. run: pnpm lint"
```

#### Example: Refactor
```
Before: "clean up the auth code"
After: "inspect src/auth and list duplication hotspots. propose a refactor plan scoped to one module. after approval, remove duplication without changing behavior. add a targeted test if coverage is missing. run the smallest relevant test command"
```

#### Example: Research
```
Before: "why is this API slow?"
After: "explore request flow around src/api/. summarize likely bottlenecks with evidence (logs, timings). propose 2-3 hypotheses and what data is needed to confirm. do not implement yet. if needed, ask for access to profiling output"
```

#### Example: Ops
```
Before: "deployment failed"
After: "deploy fails with error: [paste log]. identify the failing step in scripts/deploy.sh and related CI config. suggest a fix and a rollback plan. run: ./scripts/deploy.sh --dry-run (if available)"
```

#### Example: Docs
```
Before: "update the README"
After: "update README.md to include install + dev steps based on existing scripts. keep it concise. confirm commands exist and match actual scripts"
```

### Step 4: Output Format

Output in the following format:

```markdown
## Prompt Analysis

### Original Prompt
[User-provided prompt]

### Issues
- [Issue 1 and its impact]
- [Issue 2 and its impact]
...

### Missing Information (Questions to Ask)
The following questions should be answered to make the prompt more effective:
- [Question 1] (Why it is needed)
- [Question 2] (Why it is needed)
...

### Verification Plan
- Commands to run (tests, build, lint, screenshots)
- Expected results or acceptance criteria

### Exploration/Planning Recommendation
- Recommend exploration/planning first? [Yes/No] and why

### Execution Preference
- Implement now / propose plan only / analyze only
- Any constraints on response length or format

### Improved Prompt
[The improved prompt]

### Document Improvement Suggestions (if applicable)
- [Issue and concrete improvement for the instruction document]
- [Issue and concrete improvement for the instruction document]

### Revised Document (optional)
[A revised draft of the instruction document when helpful]

### Improved Prompt Template (optional)
Use this as a fill-in template if the user wants a reusable prompt format:
```
[Task]
- Goal:
- Target files/paths (@...):
- Constraints (runtime/version/deps/security/compat):
- Context (symptom, logs, repro, links):

[Verification]
- Commands:
- Expected results:
- UI checks (screenshots/visual diffs):

[Exploration/Planning]
- Do exploration/planning first? (Yes/No) + reason:

[Execution Preference]
- Implement now / plan only / analyze only
- Output format (concise report, patch summary, checklist, etc.)
```

### Short Prompt Template (optional)
Use this when the user wants the shortest effective prompt:
```
Goal: ...
Targets: path1/path2
Context: symptom + repro + logs
Constraints: runtime/deps/compat
Verify: command + expected result
Explore/Plan: yes/no (why)
Execute: implement / plan only / analyze only
Output: concise format
```

### Improvement Points
1. [Explanation of improvement 1]
2. [Explanation of improvement 2]
...

### Additional Recommendations (optional)
- [Whether to do exploration/planning first]
- [Whether to parallelize or delegate investigation]
- [Whether preliminary research is needed]
- [Ways to reduce context usage]
```

## Reference: Best Practices Checklist

Best practices to reference when improving prompts:

### Provide Verification Methods
- Include test cases
- Specify expected output
- For UI changes, request screenshot comparison
- Add "run the tests" or "verify the build succeeds"
- Include explicit commands to run

### Explore → Plan → Implement Order
- Use an exploration/planning phase first for complex tasks
- Create a plan before implementation
- Small fixes don't need a formal plan
- When uncertain, ask clarifying questions before coding

### Include Specific Context
- Paste error messages
- Specify existing patterns
- Clarify edge cases
- State environment constraints (runtime, language versions, dependencies)

### Use Rich Inputs
- Paste logs and stack traces
- Provide URLs for docs or API references
- Attach or paste large text outputs when needed

### Manage Context Window
- Keep prompts concise and focused
- Remove unrelated history or speculation
- Ask for missing info instead of guessing

### Leverage Parallelism/Delegation
- For research tasks: request parallel investigation or summaries
- For code review: request an independent review pass
- Keeps the main task focused

### Patterns to Avoid
- Vague instructions like "make it better" or "improve it"
- Implementation requests without verification methods
- Multiple unrelated tasks at once
- Requesting changes to files not yet read
- Large context dumps with no clear signal
