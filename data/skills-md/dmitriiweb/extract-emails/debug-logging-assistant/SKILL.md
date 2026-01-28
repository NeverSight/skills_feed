---
name: debug-logging-assistant
description: Add purposeful debug logging to improve observability without changing behavior.
---

# Debug Logging Assistant

## Quick start
- Read the target code and recent failures to understand where visibility is missing.
- Add debug logs only where they help explain flow, inputs, branching, or error context.
- Keep logs small and descriptive: what is happening, key identifiers, and outcomes.
- Do not change control flow or data; only add logs. Avoid logging every step.
- See `references/logging_rules.md` for placement and messaging guidelines.

## Workflow
1) **Inspect**  
   - Identify high-signal spots: entry points, external calls, branching paths, retries, and error handling.  
   - Note important identifiers (IDs, counts, feature flags) that disambiguate paths.

2) **Place logs**  
   - Log before/after risky operations and around decisions that affect downstream behavior.  
   - Prefer one concise log per logical block over multiple low-value messages.  
   - Keep sensitive data out; include only safe identifiers or summaries.

3) **Write messages**  
   - Use consistent prefixes and log levels (debug/trace) already used in the codebase.  
   - Capture intent: action, inputs of interest, and outcomes (success/failure, counts).  
   - Avoid narrating trivial steps or restating obvious code.

4) **Validate**  
   - Ensure no functional changes: no refactors, no reordered logic, no added branching.  
   - Confirm log volume is reasonable and won’t spam hot paths.  
   - Re-run applicable tests if available; otherwise double-check for typos.

## Reference
- `references/logging_rules.md`: detailed rules for meaningful debug logging.
