---
name: har-debugger
description: Analyze HAR (.har) files alongside a bug description to identify slow, failed, or abnormal requests, correlate them to symptoms, and produce a concise root-cause report with evidence and next steps.
---

# HAR Debugger

## Overview
Analyze a HAR file plus a bug description to isolate problematic network requests and explain likely causes using only HAR evidence.

## Inputs
- `har_file`: Path to a `.har` file on disk.
- `bug_description`: Concise description of the bug symptoms.
- `start_time`: (optional) ISO timestamp or epoch ms for when the bug started.
- `end_time`: (optional) ISO timestamp or epoch ms for when the bug ended.
- `socket_map`: (optional) Inline list of socket-to-API mappings in the form `<socket-name>: <api-name>` to override defaults.

If the user provides raw HAR JSON instead of a file, accept it, but prefer a file path when possible. Use `start_time`/`end_time` to limit analysis to the incident window to save tokens.

## Workflow
1. Validate that `har_file` exists and ends with `.har`; if missing, ask for the file path.
2. If `start_time`/`end_time` provided, preprocess the HAR using the bundled parser at `./bin/har-parser`. Always run the command from the skill directory so the relative path works. If the working directory is different, use the absolute skill path (e.g., `/Users/<user-name>/.codex/skills/har-debugger/bin/har-parser`).
```
./bin/har-parser -- --file <har_file> --start "<start_time>" --end "<end_time>" --format har --out output.har
```
Use `output.har` for all remaining analysis. Time format must match the parser input, for example `10/02/2026 03:02:00`.
3. Parse the HAR JSON and confirm `log.entries` exists; if missing, ask for a complete HAR.
4. Flatten `log.entries` into a list of requests.
5. Extract for each entry: `request.method`, `request.url`, `response.status`, `response.statusText`, `time`, `timings`, `startedDateTime`, response headers (`response.headers`), and response body when available (`response.content.text`).
6. If present, capture response header time (e.g., `Date` header) as the server-reported response time.
7. Compute response received time as `startedDateTime + time` (milliseconds) to compare client vs server timestamps.
8. Load default socket map from `references/socket_map.md` and parse each line as `<socket-name>: <api-name>`. If `socket_map` input is provided, merge/override defaults with it.
9. If socket mappings exist, prioritize requests whose URL/path matches mapped API names related to the socket events in `bug_description`.
10. Flag suspicious entries:
- HTTP status >= 400
- Timeouts or errors indicated by `timings` or missing response
- Long `time` values (default threshold 3000 ms; adjust if the bug suggests a different baseline)
11. Match keywords from `bug_description` to URLs, methods, response content, and status text.
12. Correlate the most relevant entries to the symptom and infer likely root causes only from HAR evidence plus the bug description.

## Output
Provide a concise report that includes:
- A brief root-cause summary with confidence/uncertainty notes.
- A list of relevant requests (method, URL, status, time, response received time, response header time, key evidence).
- Evidence bullets explicitly tied to the bug description.
- Recommendations for next debugging steps (logs, backend metrics, repro checks).

## Constraints
- Do not fabricate or assume data not present in the HAR.
- Keep hypotheses grounded in the observed requests and timings.
