---
name: playwright-trace-debugging
description: Debug Playwright test failures by analyzing trace files using pwtrace CLI. Use this skill after Playwright tests fail and you have a trace.zip file. Teaches systematic debugging workflow from overview to detailed inspection (show → step → dom → console → screenshot → network).
---

# Playwright Trace Debugging

Debug failed Playwright tests systematically using trace file analysis with `pwtrace`.

## When to Use This Skill

- After Playwright test failures when you have a `trace.zip` file
- Debugging flaky or intermittent test failures
- Understanding CI/CD test failures
- When the Playwright Trace Viewer GUI isn't available
- Getting LLM-friendly text output from trace files

## Prerequisites

```bash
npm install -g pwtrace
# or use: npx pwtrace <command> trace.zip
```

## Core Philosophy: Progressive Disclosure

Start broad and drill down only as needed. The workflow follows this pattern:

```
show → step → dom/console/screenshot/network
 ↓       ↓           ↓
Which  What     Why did it fail?
failed? happened?
```

**Always start with `pwtrace show trace.zip`** to identify which step(s) failed, then use targeted commands to investigate.

For command syntax and options, use:
```bash
pwtrace --help                    # Overview and workflow
pwtrace <command> --help          # Command-specific options
```

## Debugging Decision Tree

Use this to quickly decide which command to run next:

**❌ Test failed** → `pwtrace show` → identify failed step(s)

**🔍 Step N failed** → `pwtrace step N` → understand what happened

**📄 Selector issues** → `pwtrace dom --step N --interactive` → see available elements
- Element not found? Use `--selector button` to find similar elements
- Wrong element? Check attributes and state (disabled, hidden)

**🐛 JavaScript errors** → `pwtrace console --level error` → find exceptions
- Errors around specific step? Add `--step N`

**🌐 Network issues** → `pwtrace network --failed` → find failed requests
- Check for 4xx/5xx errors, timeouts, CORS issues

**👁️ Visual confirmation** → `pwtrace screenshot --step N --list` → choose screenshot
- Then extract with `--index <N>`

**⏱️ Timing/flaky tests** → Compare DOM across steps
- `pwtrace dom --step N` vs `--step N-1`
- Look for loading states, animations, async operations

## Complete Example

Login test times out. Here's the investigation:

```bash
pwtrace show trace.zip          # Step 4 failed (click "Sign In")
pwtrace step trace.zip 4         # See console error
pwtrace dom --step 4 --interactive  # Button exists but is disabled
pwtrace console --step 4 --level error  # JS validation error
pwtrace network --failed         # API /validate-email returned 500
# Root cause: Backend validation API failing
```

## Tips

- **Always start with `show`** - Don't skip straight to debugging a specific step
- **Check DOM before screenshots** - DOM is searchable and text-based
- **Use `--interactive` frequently** - Quickly filters to actionable elements  
- **Most commands support `--format json`** - Pipe to `jq` or analyze programmatically
- **Compare before/after states** - Use `dom` on both successful and failed steps
