---
name: Start Orchestrator
description: Starts the Orchestrator 3 Stream application (backend + frontend) in background mode. Use when the user asks to start orchestrator, launch orchestrator, run orchestrator, or open the orchestrator UI. Supports --session and --cwd flags for backend.
---

# Start Orchestrator

Launches the Orchestrator 3 Stream application with both backend (FastAPI) and frontend (Vue/Vite) servers.

## Prerequisites

- The orchestrator application is located at `apps/orchestrator_3_stream/`
- Backend requires Python with uv (Astral UV)
- Frontend requires Node.js with npm
- PostgreSQL database should be running

## Configuration

Default ports (configurable via `.env`):
- **Backend**: Port 8002 (default fallback: 9403)
- **Frontend**: Port 5175

## Backend Flags

The backend script (`start_be.sh`) accepts:

| Flag | Description | Priority |
|------|-------------|----------|
| `--cwd <path>` | Working directory for the orchestrator | CLI > .env (`ORCHESTRATOR_WORKING_DIR`) > current dir |
| `--session <id>` | Session ID to resume | CLI > .env (`ORCHESTRATOR_SESSION_ID`) > new session |

## Workflow

### 1. Start Backend (with optional flags)

Run in background by default:

```bash
# Basic start (new session, current directory)
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh &

# With session ID (resume existing session)
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh --session <session-id> &

# With custom working directory
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh --cwd /path/to/project &

# With both flags
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh --cwd /path/to/project --session <session-id> &
```

### 2. Start Frontend

Run in background:

```bash
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_fe.sh &
```

### 3. Open UI in Chrome

After both services are running, open the frontend URL:

```bash
open -a "Google Chrome" "http://127.0.0.1:5175"
```

## Complete Example Commands

**Start both in background (new session):**
```bash
# Start backend
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh &

# Wait for backend to initialize
sleep 3

# Start frontend
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_fe.sh &

# Wait for frontend to initialize
sleep 2

# Open in Chrome
open -a "Google Chrome" "http://127.0.0.1:5175"
```

**Resume a session:**
```bash
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh --session abc123-def456 &
sleep 3
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_fe.sh &
sleep 2
open -a "Google Chrome" "http://127.0.0.1:5175"
```

## Foreground Mode

If user requests foreground mode, do NOT use `&` suffix and run each command sequentially, starting frontend first in background then backend in foreground:

```bash
# Frontend in background (so we can run backend in foreground)
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_fe.sh &

# Backend in foreground (to see logs)
cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh --cwd /path/to/project
```

## Stopping Services

To stop the services:

```bash
# Find and kill backend
lsof -ti:8002 | xargs kill -9

# Find and kill frontend
lsof -ti:5175 | xargs kill -9
```

## Troubleshooting

- **Port in use**: The scripts automatically kill processes using their ports before starting
- **Database not running**: Ensure PostgreSQL is running before starting backend
- **Missing dependencies**: Run `uv sync` in backend directory, `npm install` in frontend directory

## Examples

### Example 1: Basic Start

User request:
```
Start the orchestrator
```

You would:
1. Start backend in background:
   ```bash
   cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh &
   ```
2. Wait 3 seconds for backend to initialize
3. Start frontend in background:
   ```bash
   cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_fe.sh &
   ```
4. Wait 2 seconds for frontend to initialize
5. Open Chrome:
   ```bash
   open -a "Google Chrome" "http://127.0.0.1:5175"
   ```

### Example 2: Resume Session with Custom CWD

User request:
```
Start orchestrator with session abc123 and working directory /Users/me/myproject
```

You would:
1. Start backend with flags:
   ```bash
   cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh --cwd /Users/me/myproject --session abc123 &
   ```
2. Wait, then start frontend and open Chrome as above

### Example 3: Foreground Mode

User request:
```
Start orchestrator in foreground so I can see logs
```

You would:
1. Start frontend in background first:
   ```bash
   cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_fe.sh &
   ```
2. Wait 2 seconds
3. Start backend in foreground (no `&`):
   ```bash
   cd /path/to/agent-experts/apps/orchestrator_3_stream && ./start_be.sh
   ```
4. Note: Chrome opening should happen after frontend is ready but before backend foreground command
