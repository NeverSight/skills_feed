---
name: debug
description: Debug code by adding structured logging. Starts a local HTTP server for browser/remote logging and optionally a live log viewer. Use when debugging issues, tracking down bugs, or when the user says /debug.
---

# Debug Skill

Add structured logging to track down bugs. Uses a local log file in `/tmp` and an optional HTTP server for browser-side logging.

## Setup

### 1. Generate unique session ID and log file

```bash
DEBUG_ID=$(date +%s | tail -c 6)
LOG_FILE="/tmp/debug-${DEBUG_ID}.log"
touch $LOG_FILE
echo "Log file: $LOG_FILE"
```

### 2. Start the log server (if browser logging needed)

```bash
SKILL_DIR="$(dirname "$(realpath "$0")")" 2>/dev/null || SKILL_DIR="~/.cursor/skills/debug"
SERVER_PORT=$(node ${SKILL_DIR}/scripts/find-port.mjs)
node ${SKILL_DIR}/scripts/server.mjs $SERVER_PORT $LOG_FILE &
SERVER_PID=$!
echo "Log server port: $SERVER_PORT"
```

### 3. Track state

Keep track of:
- `LOG_FILE`: Path to the log file
- `SERVER_PORT` / `SERVER_PID`: Log server details (if started)
- `VIEWER_PORT` / `VIEWER_PID`: Log viewer details (if started later)

## Log Viewer (On-Demand)

Start the log viewer ONLY when the user asks to view logs, see logs, watch logs, or similar requests.

```bash
SKILL_DIR="$(dirname "$(realpath "$0")")" 2>/dev/null || SKILL_DIR="~/.cursor/skills/debug"
VIEWER_PORT=$(node ${SKILL_DIR}/scripts/find-port.mjs)
node ${SKILL_DIR}/scripts/viewer.mjs $VIEWER_PORT $LOG_FILE &
VIEWER_PID=$!
echo "Log viewer: http://127.0.0.1:${VIEWER_PORT}"
```

Tell the user: "Open http://127.0.0.1:{VIEWER_PORT} to see live logs"

## Adding Logs

### Server-side (Rust, Node.js, Python, etc.)

Write directly to the log file:

**Rust:**
```rust
use std::fs::OpenOptions;
use std::io::Write;

fn debug_log(data: &str) {
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open("LOG_FILE_PATH")
        .unwrap();
    writeln!(file, "[{}] {}", chrono::Utc::now().to_rfc3339(), data).ok();
}
```

**Node.js:**
```javascript
const fs = require('fs');
function debugLog(data) {
  fs.appendFileSync('LOG_FILE_PATH', `[${new Date().toISOString()}] ${JSON.stringify(data)}\n`);
}
```

**Python:**
```python
import json
from datetime import datetime

def debug_log(data):
    with open('LOG_FILE_PATH', 'a') as f:
        f.write(f"[{datetime.utcnow().isoformat()}] {json.dumps(data)}\n")
```

Replace `LOG_FILE_PATH` with the actual log file path.

### Browser-side (via HTTP server)

```javascript
async function debugLog(data) {
  await fetch('http://127.0.0.1:PORT/log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
}
```

Replace `PORT` with the actual server port number.

## Workflow

### Pre-Debug: Check Git Status

Before starting, check if git is clean:

```bash
git status --porcelain
```

If the output is empty (no uncommitted changes), note this. After extensive debugging iterations, if the final fix is small, you can use `git checkout -- .` or `git restore .` to reset all instrumentation instantly instead of manually removing debug code. This is much faster than cleanup.

### Steps

1. **Start**: Run setup commands
2. **Instrument**: Add logging calls at strategic points in the code
3. **Clear logs**: Before asking for reproduction, always clear the log file (`> $LOG_FILE`)
4. **Ask for reproduction**: Tell the user the steps to reproduce
5. **Analyze**: Read the log file (`cat $LOG_FILE`) or start viewer if user asks
6. **Iterate**: Add more logs if needed, remove red herrings
7. **Cleanup**: Once bug is found, proceed to cleanup (or use git reset if started clean)

## End of Message Reminder

At the end of EVERY message during debugging, include reproduction steps and prompt for next action.

**If in Cursor CLI (terminal-based):**

```
---
Reproduction steps:
1. [Step 1]
2. [Step 2]
3. [etc.]

[A] Issue reproduced → continue debugging
[B] Resolved → cleanup instrumentation
```

**If in Cursor IDE (has AskQuestion tool):**

Use the AskQuestion tool with:
- Option A: "Issue reproduced - continue debugging"
- Option B: "Resolved - cleanup instrumentation"
- Option C: "Other (please specify)"
- Allow freeform text input for additional context

Update the reproduction steps as you learn more about how to trigger the bug.

## Cleanup

Once the bug is identified (or before any git commit/push):

1. Remove all debug logging code you added
2. Kill any servers: `kill $SERVER_PID $VIEWER_PID` (whichever are running)
3. Delete the log file: `rm $LOG_FILE`

**IMPORTANT**: Always run cleanup before committing or pushing code. Never commit debug instrumentation.

## Tips

- Log function entry/exit with parameters and return values
- Log before and after suspect operations
- Include relevant variable state in log messages
- Use descriptive labels: `{ "location": "handleClick", "state": {...} }`
