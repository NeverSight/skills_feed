---
name: sentry-issue-resolver
description: "Analyze and resolve Sentry issues by fetching detailed issue information, performing deep root cause analysis, and providing actionable solutions. Use when the user asks to: (1) Analyze a Sentry issue, (2) Debug or investigate a Sentry error, (3) Fix a Sentry issue, (4) Get root cause analysis for application errors, (5) Resolve Sentry alerts. Works with Sentry URLs to fetch stack traces, error context, and event data."
---

# Sentry Issue Resolver

Fetch Sentry issues with complete stack traces, analyze root causes, and provide actionable solutions using Sentry REST API.

## Workflow

When the user requests Sentry issue analysis:

1. **Parse the Sentry URL**
   - Extract org slug from subdomain (e.g., `arcsite` from `arcsite.sentry.io`)
   - Extract issue ID from path (e.g., `7219768209` from `/issues/7219768209/`)

   Example URL: `https://arcsite.sentry.io/issues/7219768209/?project=1730879`

2. **Check Authentication**

   First verify that `SENTRY_AUTH_TOKEN` is set in the environment:
   ```bash
   echo $SENTRY_AUTH_TOKEN
   ```

   If not set, inform the user:
   "Please set your Sentry auth token: `export SENTRY_AUTH_TOKEN=your_token_here`"
   "You can create a token at: https://sentry.io/settings/account/api/auth-tokens/"

3. **Fetch Event List**

   Get the list of events for the issue to obtain event IDs:
   ```bash
   curl "https://sentry.io/api/0/organizations/<ORG_SLUG>/issues/<ISSUE_ID>/events/" \
     -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
   ```

   Example:
   ```bash
   curl "https://sentry.io/api/0/organizations/arcsite/issues/7219768209/events/" \
     -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
   ```

   If jq is available, extract event IDs:
   ```bash
   curl "..." | jq -r '.[].eventID'
   ```

   If jq is not available, that's fine - work with the raw JSON response.

4. **Fetch Complete Event Details**

   Get the full event details including stack trace for the latest event:
   ```bash
   curl "https://sentry.io/api/0/organizations/<ORG_SLUG>/issues/<ISSUE_ID>/events/<EVENT_ID>/" \
     -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
   ```

   Example:
   ```bash
   curl "https://sentry.io/api/0/organizations/arcsite/issues/7219768209/events/abc123/" \
     -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
   ```

   If jq is available, extract stack trace info:
   ```bash
   curl "..." | jq -r '.exception.values[]?.stacktrace.frames[] | "\(.filename):\(.lineno) \(.function)"'
   ```

   The response includes:
   - `exception.values[].stacktrace.frames[]` - Complete stack trace with file paths, line numbers, and function names
   - `exception.values[].type` and `exception.values[].value` - Error type and message
   - `tags`, `user`, `request` - Context data
   - `context` - Additional environment and runtime information

5. **Analyze the Issue**
   - Examine the stack trace for the error location
   - Identify the error type and message
   - Review the error context (request data, user actions, environment)
   - Look for patterns in the events (frequency, affected users, common paths)
   - Trace the execution flow to find the root cause

6. **Provide Deep Root Cause Analysis**

   Include in the analysis:
   - **Error Summary**: What went wrong (error type, message, affected file/function)
   - **Root Cause**: Why it happened (logical error, null reference, race condition, etc.)
   - **Context**: When/where it occurs (specific user actions, endpoints, environments)
   - **Impact**: Severity and user experience implications
   - **Code Location**: Specific file paths and line numbers from stack trace

7. **Suggest Solutions**

   Provide 1-2 actionable solutions:
   - **Solution 1**: The most direct fix (e.g., add null check, fix logic error)
   - **Solution 2**: Alternative approach or preventive measure (e.g., refactor, add validation)

   Each solution should include:
   - Clear description of the fix
   - Specific code changes or implementation steps
   - Trade-offs or considerations

8. **Output Format**

   Structure the response as:

   ```
   ## Sentry Issue Analysis: [ISSUE_ID]

   ### Error Summary
   [Brief description of what went wrong]

   ### Root Cause
   [Deep analysis of why this happened]

   ### Context
   - Frequency: [how often it occurs]
   - Affected: [users, endpoints, environments]
   - Trigger: [what action causes it]

   ### Impact
   [Severity and user experience impact]

   ### Code Location
   [File paths and line numbers from stack trace]

   ### Suggested Solutions

   #### Solution 1: [Direct Fix]
   [Description and implementation]

   #### Solution 2: [Alternative/Preventive]
   [Description and implementation]
   ```

## Sentry API Commands

**List events for an issue (get event IDs):**
```bash
curl "https://sentry.io/api/0/organizations/<ORG_SLUG>/issues/<ISSUE_ID>/events/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

With jq to extract just the event IDs:
```bash
curl "https://sentry.io/api/0/organizations/<ORG_SLUG>/issues/<ISSUE_ID>/events/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  | jq -r '.[].eventID'
```

**Get complete event details (including stack trace):**
```bash
curl "https://sentry.io/api/0/organizations/<ORG_SLUG>/issues/<ISSUE_ID>/events/<EVENT_ID>/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

With jq to extract stack trace:
```bash
curl "https://sentry.io/api/0/organizations/<ORG_SLUG>/issues/<ISSUE_ID>/events/<EVENT_ID>/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  | jq -r '.exception.values[]?.stacktrace.frames[] | "\(.filename):\(.lineno) \(.function)"'
```

**Extract specific information with jq (optional):**
```bash
# Get error message
jq -r '.exception.values[0].value'

# Get error type
jq -r '.exception.values[0].type'

# Get user context
jq -r '.user'

# Get request info
jq -r '.request'
```

**Note:** jq is optional. If the user doesn't have jq installed, work with the raw JSON response directly.

## Working with API Responses

**When jq is available:**
- Use it to extract and format specific fields for easier analysis
- Pipe curl output directly to jq for cleaner results

**When jq is NOT available:**
- Work with the raw JSON response
- Look for key fields manually in the JSON:
  - `exception.values[].type` - Error type
  - `exception.values[].value` - Error message
  - `exception.values[].stacktrace.frames[]` - Stack trace frames
  - Each frame has: `filename`, `lineno`, `function`, `context_line`, `pre_context`, `post_context`
- The latest event is typically most useful for analysis

**Typical Workflow:**
1. First, fetch the events list to get the latest event ID (usually first in the array)
2. Then fetch that event's full details
3. Extract stack trace from `exception.values[0].stacktrace.frames`
4. The frames are ordered from innermost (where error occurred) to outermost
5. Look at `context_line`, `pre_context`, and `post_context` for code context around the error

## Analysis Tips

**Common Error Patterns:**

- **Null/Undefined Reference**: Variable accessed before initialization or after it was set to null
- **Type Error**: Incorrect data type used (string vs number, missing property)
- **Network/Timeout**: Failed API calls, slow responses, connection issues
- **Race Condition**: Async operations completing in unexpected order
- **Logic Error**: Incorrect conditional logic or algorithm implementation
- **Missing Validation**: User input not properly validated or sanitized

**Root Cause Techniques:**

1. **Follow the Stack Trace**: Start from the top (where error was thrown) and trace backward
2. **Check Recent Changes**: Look for recent commits that touched the failing code
3. **Examine Context Data**: Request parameters, user state, environment variables
4. **Pattern Recognition**: Does it only happen for certain inputs, users, or environments?
5. **Timing Analysis**: Does it happen at specific times, after specific actions, or randomly?

## Prerequisites

- **SENTRY_AUTH_TOKEN** environment variable set with a valid Sentry auth token
  - Create a token at: https://sentry.io/settings/account/api/auth-tokens/
  - Set it: `export SENTRY_AUTH_TOKEN=your_token_here`
- **curl** (pre-installed on most systems)
- **jq** (optional, for easier JSON parsing)
  - Install: `brew install jq` (macOS) or `apt-get install jq` (Linux)
  - Not required - can work with raw JSON if jq is unavailable
- Access to the Sentry organization (typically arcsite)
