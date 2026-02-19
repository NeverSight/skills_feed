---
name: launchdarkly-flag-cleanup
description: "Safely remove a feature flag from code while preserving production behavior. Use when the user wants to remove a flag from code, delete flag references, or create a PR that hardcodes the winning variation after a rollout is complete."
license: Apache-2.0
compatibility: Requires the remotely hosted LaunchDarkly MCP server
metadata:
  author: launchdarkly
  version: "1.0.0-experimental"
---

# LaunchDarkly Flag Cleanup

You're using a skill that will guide you through safely removing a feature flag from a codebase while preserving production behavior. Your job is to explore the codebase to understand how the flag is used, query LaunchDarkly to determine the correct forward value, remove the flag code cleanly, and verify the result.

If you haven't already identified which flag to clean up, use the [flag discovery skill](../launchdarkly-flag-discovery/SKILL.md) first to audit the landscape and find candidates.

## Prerequisites

This skill requires the remotely hosted LaunchDarkly MCP server to be configured in your environment.

**Required MCP tools:**
- `check-removal-readiness` — detailed safety check (orchestrates flag config, cross-env status, dependencies, code references, and expiring targets in parallel)
- `get-flag` — fetch flag configuration for a specific environment

**Optional MCP tools:**
- `archive-flag` — archive the flag in LaunchDarkly after code removal
- `delete-flag` — permanently delete the flag (irreversible, prefer archive)

## Core Principles

1. **Safety First**: Always preserve current production behavior.
2. **LaunchDarkly as Source of Truth**: Never guess the forward value. Query the actual configuration.
3. **Follow Conventions**: Respect existing code style and structure.
4. **Minimal Change**: Only remove flag-related code. No unrelated refactors.

## Workflow

### Step 1: Explore the Codebase

Before touching LaunchDarkly or removing code, understand how this flag is used in the codebase.

1. **Find all references to the flag key.** Search for the flag key string (e.g., `new-checkout-flow`) across the codebase. Check for:
   - Direct SDK evaluation calls (`variation()`, `boolVariation()`, `useFlags()`, etc.)
   - Constants/enums that reference the key
   - Wrapper/service patterns that abstract the SDK
   - Configuration files, tests, and documentation
   - See [SDK Patterns](references/sdk-patterns.md) for the full list of patterns by language

2. **Understand the branching.** For each reference, identify:
   - What code runs when the flag is `true` (or variation A)?
   - What code runs when the flag is `false` (or variation B)?
   - Are there side effects, early returns, or nested conditions?

3. **Note the scope.** How many files, components, or modules does this flag touch? A flag used in one `if` block is simpler than one threaded through multiple layers.

### Step 2: Run the Removal Readiness Check

Use `check-removal-readiness` to get a detailed safety assessment. This single tool call orchestrates multiple checks in parallel:
- Flag configuration and targeting state
- Cross-environment status
- Dependent flags (prerequisites)
- Expiring targets
- Code reference statistics

The tool returns a readiness verdict:

**`safe`** — No blockers or warnings. Proceed with removal.

**`caution`** — No hard blockers but warnings exist (e.g., code references in other repos, expiring targets scheduled, flag marked as permanent). Present warnings and let the user decide.

**`blocked`** — Hard blockers prevent safe removal (e.g., dependent flags, actively receiving requests, targeting is on with active rules). Present blockers — the user must resolve them first.

### Step 3: Determine the Forward Value

Use `get-flag` to fetch the flag configuration in each critical environment. The **forward value** is the variation that replaces the flag in code.

| Scenario | Forward Value |
|----------|---------------|
| All critical envs ON, same fallthrough, no rules/targets | Use `fallthrough.variation` |
| All critical envs OFF, same offVariation | Use `offVariation` |
| Critical envs differ in ON/OFF state | **NOT SAFE** — stop and inform the user |
| Critical envs serve different variations | **NOT SAFE** — stop and inform the user |

### Step 4: Remove the Flag from Code

Now execute the removal using what you learned in Step 1.

1. **Replace flag evaluations with the forward value.**
   - Preserve the code branch matching the forward value
   - Remove the dead branch entirely
   - If the flag value was assigned to a variable, replace the variable with the literal value or inline it

2. **Clean up dead code.**
   - Remove imports, constants, and type definitions that only existed for the flag
   - Remove functions, components, or files that only existed for the dead branch
   - Check for orphaned exports, hooks, helpers, styles, and test files
   - If the repo uses an unused-export tool (Knip, ts-prune, lint rules), run it and remove any flag-related orphans

3. **Don't over-clean.**
   - Only remove code directly related to the flag
   - Don't refactor, optimize, or "improve" surrounding code
   - Don't change formatting or style of untouched code

**Example transformation (boolean flag, forward value = `true`):**

```typescript
// Before
const showNewCheckout = await ldClient.variation('new-checkout-flow', user, false);
if (showNewCheckout) {
  return renderNewCheckout();
} else {
  return renderOldCheckout();
}

// After
return renderNewCheckout();
```

### Step 5: Create Pull Request

Use the template in [references/pr-template.md](references/pr-template.md) for a structured PR description. The PR should clearly communicate:
- What flag was removed and why
- What the forward value is and why it's correct
- The readiness assessment results (from `check-removal-readiness`)
- What code was removed and what behavior is preserved
- Whether other repos still reference this flag

### Step 6: Verify

Before considering the job done:

1. **Code compiles and lints.** Run the project's build and lint steps.
2. **Tests pass.** If the flag was used in tests, the tests should be updated to reflect the hardcoded behavior.
3. **No remaining references.** Search the codebase one more time for the flag key to make sure nothing was missed.
4. **PR is complete.** The description covers the readiness assessment, forward value rationale, and any cross-repo coordination needed.

## Edge Cases

| Situation | Action |
|-----------|--------|
| Flag not found in LaunchDarkly | Inform user, check for typos in the key |
| Flag already archived | Ask if code cleanup is still needed (flag is gone from LD but code may still reference it) |
| Multiple SDK patterns in codebase | Search all patterns: `variation()`, `boolVariation()`, `variationDetail()`, `allFlags()`, `useFlags()`, plus any wrappers |
| Dynamic flag keys (`flag-${id}`) | Warn that automated removal may be incomplete — manual review required |
| Different default values in code vs LD | Flag as inconsistency in the PR description |
| Orphaned exports/files remain after removal | Run unused-export checks and remove dead files |

## What NOT to Do

- Don't change code unrelated to flag cleanup.
- Don't refactor or optimize beyond flag removal.
- Don't remove flags still being actively rolled out.
- Don't guess the forward value — always query LaunchDarkly.

## After Cleanup

Once the PR is merged and deployed:
1. **Archive the flag in LaunchDarkly** using `archive-flag`. Archival is reversible; deletion is not. Always archive first.
2. **Notify other teams** if `check-removal-readiness` reported code references in other repositories.
3. **If the flag had targeting changes pending,** they can be ignored — the flag is being removed.

## References

- [PR Template](references/pr-template.md) — Structured PR description for flag removal
- [SDK Patterns](references/sdk-patterns.md) — Flag evaluation patterns by language/framework
- [Flag Discovery](../launchdarkly-flag-discovery/SKILL.md) — Find cleanup candidates before using this skill
- [Flag Targeting](../launchdarkly-flag-targeting/SKILL.md) — If you need to change targeting instead of removing
