---
name: process-manager
description: Safely start, monitor, and stop processes by PID across platforms. Use when managing background servers, finding running processes, or ensuring clean process termination.
---

# Process Manager

## Instructions

### When to Invoke This Skill
- Starting background servers for testing
- Finding running processes on specific ports
- Stopping test servers after testing
- Diagnosing port conflicts
- Cleaning up orphaned processes
- Verifying process termination

### CRITICAL RULES

**DO:**
- ✅ Always kill processes by PID (Process ID)
- ✅ Verify PID before killing
- ✅ Use platform-specific commands correctly
- ✅ Confirm process stopped after kill command

**DON'T:**
- ❌ NEVER kill by process name (`pkill`, `killall`, `taskkill /IM`)
- ❌ NEVER kill by command pattern (`pkill -f`)
- ❌ NEVER assume process is gone without verification
- ❌ NEVER use generic kill commands without PID

**Why?** Killing by name/pattern can terminate unrelated processes, including user's production services.

### Platform-Specific Commands

#### Windows

**Find Process by Port:**
```bash
netstat -ano | findstr ":<port>"
```
Output format:
```
TCP    0.0.0.0:8001    0.0.0.0:0    LISTENING    12345
                                                  ^^^^^
                                                  PID
```

**Kill Process by PID:**
```bash
cmd //c taskkill //PID <PID> //F
```
- `/F` = Force termination (use `//F` in Git Bash to prevent path conversion)
- Replace `<PID>` with actual process ID
- **Git Bash Users**: Use `cmd //c` wrapper to prevent Git Bash from converting `/PID` to a Windows path

**Verify Process Stopped:**
```bash
netstat -ano | findstr ":<port>"
```
Should return no results.

**List All Python Processes:**
```bash
tasklist | findstr python.exe
```

#### Unix/Linux/macOS

**Find Process by Port (Method 1 - lsof):**
```bash
lsof -i :<port>
```
Output format:
```
COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python   12345 user    3u  IPv4  0x123      0t0  TCP *:8001 (LISTEN)
         ^^^^^
         PID
```

**Find Process by Port (Method 2 - netstat):**
```bash
netstat -tulpn | grep :<port>
```
Output format:
```
tcp  0  0  0.0.0.0:8001  0.0.0.0:*  LISTEN  12345/python
                                            ^^^^^
                                            PID
```

**Kill Process by PID:**
```bash
kill <PID>
```
Or if process won't die:
```bash
kill -9 <PID>
```
- `kill` sends SIGTERM (graceful)
- `kill -9` sends SIGKILL (immediate)
- Replace `<PID>` with actual process ID

**Verify Process Stopped:**
```bash
lsof -i :<port>
# or
ps aux | grep <PID>
```
Should return no results.

**List All Python Processes:**
```bash
ps aux | grep python
```

### Standard Workflows

#### Starting Background Process

**Windows:**
```bash
start /B <command>
```
Example:
```bash
start /B uv run python main.py --port 8001
```

**Unix/Linux/macOS:**
```bash
<command> &
```
Example:
```bash
uv run python main.py --port 8001 &
```

**Capture PID on Start (Unix/Linux/macOS):**
```bash
<command> & echo $!
```
The `$!` variable contains the PID of the last background process.

#### Finding Running Process

**By Port:**
```bash
# Windows
netstat -ano | findstr ":<port>"

# Unix/Linux/macOS
lsof -i :<port>
```

**By Name:**
```bash
# Windows
tasklist | findstr <name>

# Unix/Linux/macOS
ps aux | grep <name>
```

**By PID:**
```bash
# Windows
tasklist /FI "PID eq <PID>"

# Unix/Linux/macOS
ps -p <PID>
```

#### Stopping Process

**1. Find PID** (using methods above)

**2. Record PID** - Write it down or store in variable

**3. Kill by PID:**
```bash
# Windows
cmd //c taskkill //PID <PID> //F

# Unix/Linux/macOS
kill <PID>
# or for force kill:
kill -9 <PID>
```

**4. Verify Stopped:**
```bash
# Windows
netstat -ano | findstr ":<port>"

# Unix/Linux/macOS
lsof -i :<port>
```

#### Handling Port Conflicts

**Scenario:** Can't start server because port is in use.

**1. Find What's Using Port:**
```bash
# Windows
netstat -ano | findstr ":<port>"

# Unix/Linux/macOS
lsof -i :<port>
```

**2. Identify the Process:**
- Is it your test server from previous run?
- Is it production server?
- Is it unrelated process?

**3. Decide Action:**
- **Your test server**: Kill it by PID
- **Production server**: Use different port for testing
- **Unrelated process**: Use different port or investigate

**4. If Killing:**
Use PID-based kill commands above.

### Error Scenarios

#### "Address already in use"
```
Error: [Errno 48] Address already in use
```

**Solution:**
1. Find process on that port
2. Verify it's safe to kill
3. Kill by PID
4. Retry starting server

#### "Permission denied" (Unix/Linux/macOS)
```
Operation not permitted
```

**Cause:** Trying to kill process owned by another user

**Solution:**
- Use `sudo kill <PID>` (if you have permission)
- Or use different port
- Or ask process owner to stop it

#### "Access denied" (Windows)
```
ERROR: Access is denied
```

**Cause:** Process requires admin privileges to kill

**Solution:**
- Run command prompt as Administrator
- Or use Task Manager (Ctrl+Shift+Esc)
- Or use different port

#### Process Won't Die (Zombie Process)

**Unix/Linux/macOS:**
```bash
# Try graceful first
kill <PID>

# Wait a few seconds
sleep 3

# If still running, force kill
kill -9 <PID>
```

**Windows:**
```bash
# Already using /F flag which is force kill
cmd //c taskkill //PID <PID> //F

# If still fails, use Task Manager
```

### Monitoring Processes

#### Check if Process is Running

**By PID:**
```bash
# Windows
tasklist /FI "PID eq <PID>"

# Unix/Linux/macOS
ps -p <PID>
```
Exit code 0 = running, non-zero = not running

#### Watch Process Resource Usage

**Windows:**
```bash
# Open Task Manager
taskmgr

# Or command line
wmic process where ProcessId=<PID> get ProcessId,Name,WorkingSetSize,PercentProcessorTime
```

**Unix/Linux/macOS:**
```bash
# Interactive monitoring
top -p <PID>

# One-time check
ps -p <PID> -o pid,ppid,%cpu,%mem,cmd
```

#### Check Process Logs

If process is server with logging:
```bash
# Tail logs in real-time
tail -f <log-file>

# Check specific log directory
ls -lt test_data/logs/
cat test_data/logs/error.log
```

## Examples

### Example 1: Start and stop test server

**Windows:**
```bash
# Start
start /B uv run python main.py --port 8001

# Find PID
netstat -ano | findstr ":8001"
# Output: ... LISTENING    12345

# Stop
cmd //c taskkill //PID 12345 //F

# Verify
netstat -ano | findstr ":8001"
# No output = success
```

**Unix/Linux/macOS:**
```bash
# Start
uv run python main.py --port 8001 &
# Capture PID: echo $!
# Output: 12345

# Or find later
lsof -i :8001
# Output: ... 12345 ...

# Stop
kill 12345

# Verify
lsof -i :8001
# No output = success
```

### Example 2: Diagnose port conflict

```
Problem: Can't start on port 8001

# Find what's using it
# Windows:
netstat -ano | findstr ":8001"
# Unix/Linux/macOS:
lsof -i :8001

# Identify process
# Windows:
tasklist /FI "PID eq 12345"
# Unix/Linux/macOS:
ps -p 12345

# If it's old test server, kill it
# Windows:
cmd //c taskkill //PID 12345 //F
# Unix/Linux/macOS:
kill 12345

# Retry starting server
```

### Example 3: Clean up multiple test processes

```
Scenario: Multiple test servers running from previous tests

# List all on test port
# Windows:
netstat -ano | findstr ":8001"
# Unix/Linux/macOS:
lsof -i :8001

# For each PID found, kill individually
# Windows:
cmd //c taskkill //PID 12345 //F
cmd //c taskkill //PID 12346 //F
# Unix/Linux/macOS:
kill 12345 12346

# Verify all stopped
# Windows:
netstat -ano | findstr ":8001"
# Unix/Linux/macOS:
lsof -i :8001
```

### Example 4: Graceful shutdown with fallback

**Unix/Linux/macOS:**
```bash
# Try graceful first
kill <PID>

# Wait 5 seconds
sleep 5

# Check if still running
if ps -p <PID> > /dev/null 2>&1; then
  echo "Process still running, force killing..."
  kill -9 <PID>
else
  echo "Process terminated gracefully"
fi

# Verify
ps -p <PID>
```
