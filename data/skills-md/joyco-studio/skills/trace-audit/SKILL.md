---
name: trace-audit
description: Analyze a Chrome DevTools Performance trace JSON file for performance anomalies, producing a structured audit report with critical issues, warnings, metrics, timeline hotspots, and actionable recommendations.
user-invocable: true
argument-hint: <trace-file.json>
---

# Chrome DevTools Trace Audit

Analyze a Chrome DevTools Performance trace and produce a comprehensive performance audit report.

## Usage

```
/trace-audit <path-to-trace.json>
```

The argument is the absolute path to a Chrome DevTools trace JSON file (exported from the Performance panel).

## Workflow

Follow these steps in order. Use parallel tool calls wherever noted.

### Step 1 — Validate the trace file

Read the first 100 lines of the file using the Read tool. Confirm it is a valid Chrome DevTools trace by checking for:
- A top-level `traceEvents` array, **or** a bare JSON array starting with `[`
- Event objects with `name`, `cat`, `ph`, `ts` fields
- Presence of `__metadata` or `TracingStartedInBrowser` events

If validation fails, tell the user this doesn't appear to be a Chrome DevTools trace and stop.

### Step 2 — Extract metadata

Use Grep on the trace file to extract (run these in parallel):
1. **Site URL** — grep for `TracingStartedInBrowser` or `navigationStart` or `FrameCommittedInBrowser` and look for a URL in the `args`
2. **Process names** — grep for `process_name` or `thread_name` to identify renderer, browser, GPU processes
3. **Trace time range** — grep for the first and last `"ts":` values to compute trace duration

### Step 3 — Run detection passes

Refer to `detection-heuristics.md` for the full set of patterns and thresholds. Run all detection categories **in parallel** using Grep. For each category:
- Use the specified grep pattern on the trace file
- Collect matching lines with surrounding context where helpful (`-C 1` or `-C 2`)
- Count matches and extract durations/values from the matched JSON

The detection categories are:
1. Long Tasks (`RunTask` with dur > 50000)
2. Layout Thrashing (`InvalidateLayout` → `Layout` pairs)
3. Forced Reflows (`Layout` events with `stackTrace`)
4. rAF Ticker Loops (`RequestAnimationFrame` frequency)
5. Style Recalc Storms (`UpdateLayoutTree` with dur > 5000)
6. Paint Storms (`Paint` events with dur > 3000)
7. GC Pressure (`MajorGC` / `V8.GC_MARK_COMPACTOR`)
8. CLS (`LayoutShift` cumulative score)
9. INP (`EventTiming` max duration)
10. Network Errors (`ResourceReceiveResponse` with statusCode >= 400)
11. Redundant Fetches (same URL fetched multiple times)
12. Script Eval (`EvaluateScript` / `CompileScript` with dur > 50000)
13. Long Animation Frames (`LoAF` / `LongAnimationFrame`)

### Step 4 — Aggregate findings

For each detection category:
- Compute total count of flagged events
- Extract the worst offender (max duration or highest score)
- Classify severity: **Critical** (red) or **Warning** (yellow) based on the thresholds in `detection-heuristics.md`
- Skip categories with zero findings

### Step 5 — Identify timeline hotspots

Group flagged events by timestamp into time windows (e.g., 500ms buckets). Identify windows where multiple issue categories overlap — these are **hotspot ranges** that represent the most problematic sections of the trace.

### Step 6 — Generate report

Output the report using the structure defined in `report-format.md`. The report should be:
- Actionable — every issue links to a concrete fix
- Scannable — use tables, severity badges, and clear headings
- Complete — cover all categories, even if just to say "no issues found"
