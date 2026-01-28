---
name: debugging
description: Systematic debugging that identifies root causes rather than treating symptoms. Uses sequential thinking for complex analysis, web search for research, and structured investigation to avoid circular reasoning and whack-a-mole fixes.
---

# Debugging

## Quickstart

1. Capture exact repro, scope, and recent changes
2. Isolate components/files; trace path to failure
3. Research exact error; check official docs
4. Compare failing vs working patterns; form a testable hypothesis
5. Verify with minimal test; apply minimal fix across all instances; validate

## When to Use This Skill

Use debugging when:
- A bug has no obvious cause or has been "fixed" before but returned
- Error messages are unclear or misleading
- Multiple attempted fixes have failed
- The issue might affect multiple locations in the codebase
- Understanding the root cause is critical for proper resolution

Skip this skill for:
- Simple syntax errors with obvious fixes
- Trivial typos or missing imports
- Well-understood, isolated bugs with clear solutions

## Core Anti-Patterns to Avoid

Based on documented failures in AI debugging, explicitly avoid:

1. **Circular Reasoning**: Never propose the same fix twice without learning why it failed
2. **Premature Victory**: Always verify fixes were actually implemented and work
3. **Pattern Amnesia**: Maintain awareness of established code patterns throughout the session
4. **Context Overload**: Use the 50% rule - restart conversation when context reaches 50%
5. **Symptom Chasing**: Resist fixing error messages without understanding root causes
6. **Implementation Before Understanding**: Never jump to code changes before examining existing patterns

## UNDERSTAND (10-step checklist)

- Understand: capture exact repro, scope, and recent changes
- Narrow: isolate components/files; trace path to failure
- Discover: research exact error (WebSearch → Parallel Search, Context7:get-library-docs)
- Examine: compare against known-good patterns in the codebase
- Reason: use SequentialThinking:process_thought and 5 Whys to reach root cause
- Synthesize: write a falsifiable hypothesis with predictions
- Test: add logs/tests to confirm the mechanism
- Apply: minimal fix for root cause, across all occurrences, following patterns
- Note: record insights, warnings, decisions
- Document: update comments/docs/tests as needed

## Progress Tracking with TodoWrite

Use TodoWrite to track debugging progress through the UNDERSTAND checklist:

1. **At start**: Create todos for each applicable step:
   ```
   ☐ U - Capture exact repro and scope
   ☐ N - Isolate failing component
   ☐ D - Research error message
   ☐ E - Compare with working patterns
   ☐ R - Root cause analysis (5 Whys)
   ☐ S - Write falsifiable hypothesis
   ☐ T - Verify with minimal test
   ☐ A - Apply fix across all occurrences
   ☐ N - Record insights
   ☐ D - Update docs/tests
   ```

2. **During debugging**: Mark steps in_progress → completed as you work through them

3. **When stuck**: TodoWrite makes it visible which step is blocked - helps identify if you're skipping steps or going in circles

4. **Skip steps only if**: Bug is simple enough that checklist is overkill (see "Skip this skill for" above)

## Tool Decision Tree

- Know exact text/symbol? → grep
- Need conceptual/semantic location? → codebase_search
- Need full file context? → read_file
- Unfamiliar error/behavior? → Context7:get-library-docs, then WebSearch → Parallel Search
- Complex multi-hypothesis analysis? → SequentialThinking:process_thought

## Context Management

- Restart at ~50% context usage to avoid degraded reasoning
- Before restart: summarize facts, hypothesis, ruled-outs, next step
- Start a fresh chat with just that summary; continue

## Decision Framework

**IF** same fix proposed twice → Stop; use SequentialThinking:process_thought
**IF** error is unclear → Research via WebSearch → Parallel Search; verify with docs
**IF** area is unfamiliar → Explore with codebase_search; don't guess
**IF** fix seems too easy → Confirm it addresses root cause (not symptom)
**IF** context is cluttered → Restart at 50% with summary
**IF** multiple hypotheses exist → Evaluate explicitly (evidence for/against)
**IF** similar code works → Find and diff via codebase_search/read_file
**IF** declaring success → Show changed lines; test fail-before/pass-after
**IF** fix spans multiple files → Search and patch all occurrences
**IF** library behavior assumed → Check Context7:get-library-docs

## Quality Checks Before Finishing

Before declaring a bug fixed, verify:

- [ ] Root cause identified and documented
- [ ] Fix addresses cause, not symptom
- [ ] All occurrences fixed (searched project-wide)
- [ ] Follows existing code patterns
- [ ] Original symptom eliminated
- [ ] No regressions introduced
- [ ] Tests/logs verify under relevant conditions
- [ ] Docs/tests updated (comments, docs, regression tests)

## References

- `reference/root-cause-framework.md`
- `reference/antipatterns.md`
