---
name: dev-terminal
description: Terminal/PTY automation with persistent sessions. Use to run and interact with TUI applications, debug terminal apps, automate CLI workflows, or any terminal interaction. Trigger phrases include "run the TUI", "start the app", "debug the terminal", "interact with", "send keys", "what's on screen".
---

# Dev Terminal Skill

Terminal automation that maintains PTY sessions across script executions. Run TUI applications, send keystrokes, capture screen output, and debug terminal apps - all with persistent state.

## Setup

Start the server in a background terminal:

```bash
cd dev-terminal && npm install && ./server.sh &
```

**Wait for the `Ready` message before running scripts.**

### Headed Mode (Optional)

For visual debugging, start with browser UI:

```bash
cd dev-terminal && ./server.sh --headed &
```

This opens a browser window showing all terminals in real-time. Useful for:

- Watching AI actions as they happen
- Manual intervention if needed
- Debugging TUI interactions

## Writing Scripts

Run scripts inline using heredocs from the `dev-terminal/` directory:

```bash
cd dev-terminal && npx tsx <<'EOF'
import { connect, sleep } from "./src/client.js";

const client = await connect();

// Create or get a named terminal
const term = await client.terminal("my-app", {
  command: "python",
  args: ["-m", "my_module"],
  cols: 120,
  rows: 40,
});

// Wait for app to start
await sleep(1000);

// Get screen snapshot
const snap = await term.snapshot();
console.log("=== SCREEN ===");
console.log(snap.text);

client.disconnect();
EOF
```

## Shell Defaults

By default, terminals use:

- **Shell**: User's default shell (`$SHELL` env var, e.g., zsh on macOS, bash on Linux)
- **Mode**: Login shell (`-l` flag) - loads full profile (`~/.zprofile`, `~/.bash_profile`)

This means your shell aliases, PATH, and environment are available.

**Override the shell:**

```typescript
// Use a specific shell
const term = await client.terminal("my-term", {
  command: "bash",
  args: ["-l"], // keep as login shell
});

// Non-login shell (only loads ~/.bashrc, not ~/.bash_profile)
const term = await client.terminal("my-term", {
  command: "bash",
  args: [], // no -l flag
});

// Run a command directly (not a shell)
const term = await client.terminal("my-term", {
  command: "python",
  args: ["-m", "my_app"],
});
```

## SSH Remote Terminals

Connect to remote servers via SSH. The API is identical to local terminals.

```typescript
import { connect } from "./src/client.js";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

const client = await connect();

// SSH with private key
const term = await client.terminal("remote-server", {
  ssh: {
    host: "192.168.1.100",
    username: "deploy",
    privateKey: fs.readFileSync(path.join(os.homedir(), ".ssh/id_rsa"), "utf8"),
  },
});

// SSH with password
const term = await client.terminal("remote-server", {
  ssh: {
    host: "example.com",
    username: "admin",
    password: "secret",
  },
});

// SSH with agent (uses SSH_AUTH_SOCK)
const term = await client.terminal("remote-server", {
  ssh: {
    host: "example.com",
    username: "admin",
    agent: process.env.SSH_AUTH_SOCK,
  },
});

// SSH with custom port and encrypted key
const term = await client.terminal("remote-server", {
  ssh: {
    host: "example.com",
    port: 2222,
    username: "admin",
    privateKey: fs.readFileSync("/path/to/key", "utf8"),
    passphrase: "key-passphrase",
  },
});
```

**SSH Options:**

| Option       | Type   | Description                      |
| ------------ | ------ | -------------------------------- |
| `host`       | string | Remote hostname or IP (required) |
| `port`       | number | SSH port (default: 22)           |
| `username`   | string | SSH username (required)          |
| `password`   | string | Password authentication          |
| `privateKey` | string | Private key content (not path)   |
| `passphrase` | string | Passphrase for encrypted keys    |
| `agent`      | string | Path to SSH agent socket         |

**Notes:**

- SSH terminals don't have a `pid` (it's `undefined`)
- All Terminal methods work the same (write, key, snapshot, etc.)
- The remote shell is determined by the server, not local settings

## Key Principles

1. **Small scripts**: Each script does ONE thing (start app, check screen, send key)
2. **Observe output**: Always check `snapshot()` to see current state
3. **Descriptive names**: Use `"claude-monitor"`, `"vim-edit"`, not `"term1"`
4. **Terminals persist**: `disconnect()` leaves terminals running for next script

## Workflow Loop

1. **Write a script** to perform one action
2. **Run it** and observe the screen output
3. **Evaluate** - what's displayed? Did it work?
4. **Decide** - send more input or task complete?
5. **Repeat** until done

## Client API

```typescript
const client = await connect();

// Get or create named terminal (uses default shell as login shell)
const term = await client.terminal("name");

// With options
const term = await client.terminal("name", {
  command: "python", // override shell/command
  args: ["-m", "my_app"], // override args (clears default -l flag)
  cols: 120,
  rows: 40,
  cwd: "/path/to/dir",
  env: { MY_VAR: "value" },
});

// List all terminal names
const names = await client.list();

// Close/kill a terminal
await client.close("name");

// Disconnect (terminals persist)
client.disconnect();
```

## Terminal Methods

```typescript
// Send raw input
await term.write("hello");

// Send special keys
await term.key("enter");
await term.key("up");
await term.key("ctrl+c");

// Send a line (adds Enter)
await term.writeLine("ls -la");

// Get screen state
const snap = await term.snapshot();
console.log(snap.text); // Plain text (no ANSI codes)
console.log(snap.lines); // Array of lines
console.log(snap.alive); // Process still running?

// Get SVG rendering (for visual analysis)
const svgSnap = await term.snapshot({ format: "svg" });
console.log(svgSnap.svg); // SVG string

// Resize
await term.resize(80, 24);

// Clear buffer
await term.clear();

// Wait for text to appear
const found = await term.waitForText("Ready", { timeout: 5000 });

// Wait for process to exit
const exitCode = await term.waitForExit({ timeout: 10000 });
```

## Special Keys

Use `term.key()` with these names:

| Category   | Keys                                                                                               |
| ---------- | -------------------------------------------------------------------------------------------------- |
| Arrows     | `up`, `down`, `left`, `right`                                                                      |
| Control    | `enter`, `tab`, `escape`, `backspace`, `delete`                                                    |
| Ctrl+X     | `ctrl+c`, `ctrl+d`, `ctrl+z`, `ctrl+l`, `ctrl+a`, `ctrl+e`, `ctrl+k`, `ctrl+u`, `ctrl+w`, `ctrl+r` |
| Function   | `f1` - `f12`                                                                                       |
| Navigation | `home`, `end`, `pageup`, `pagedown`, `insert`                                                      |

## Example: Debug a TUI App

```bash
cd dev-terminal && npx tsx <<'EOF'
import { connect, sleep } from "./src/client.js";

const client = await connect();

// Start the TUI
const term = await client.terminal("claude-monitor", {
  command: "../.venv/bin/python",
  args: ["-m", "claude_monitor"],
  cols: 120,
  rows: 40,
  cwd: "..",
});

// Wait for it to render
await sleep(2000);

// Capture screen
const snap = await term.snapshot();
console.log("=== SCREEN OUTPUT ===");
console.log(snap.text);
console.log("=== ALIVE:", snap.alive, "===");

client.disconnect();
EOF
```

## Example: Interactive Session

```bash
# Script 1: Start app
cd dev-terminal && npx tsx <<'EOF'
import { connect, sleep } from "./src/client.js";
const client = await connect();
const term = await client.terminal("my-tui", {
  command: "htop",
});
await sleep(1000);
const snap = await term.snapshot();
console.log(snap.text);
client.disconnect();
EOF

# Script 2: Send keys (terminal persists!)
cd dev-terminal && npx tsx <<'EOF'
import { connect, sleep } from "./src/client.js";
const client = await connect();
const term = await client.terminal("my-tui"); // Reconnect to existing
await term.key("down");
await term.key("down");
await sleep(500);
const snap = await term.snapshot();
console.log(snap.text);
client.disconnect();
EOF

# Script 3: Quit
cd dev-terminal && npx tsx <<'EOF'
import { connect } from "./src/client.js";
const client = await connect();
const term = await client.terminal("my-tui");
await term.write("q");
client.disconnect();
EOF
```

## Error Recovery

If something goes wrong, check the terminal state:

```bash
cd dev-terminal && npx tsx <<'EOF'
import { connect } from "./src/client.js";

const client = await connect();

// List all terminals
const terminals = await client.list();
console.log("Active terminals:", terminals);

// Check specific terminal
if (terminals.includes("my-app")) {
  const term = await client.terminal("my-app");
  const snap = await term.snapshot();
  console.log("Alive:", snap.alive);
  console.log("Exit code:", snap.exitCode);
  console.log("Last output:", snap.lines.slice(-20).join("\n"));
}

client.disconnect();
EOF
```

## Tips

- **TUI apps need time**: Use `sleep()` after starting to let them render
- **Check alive status**: TUI might crash - check `snap.alive`
- **Clear for fresh state**: Use `term.clear()` before important snapshots
- **Large output**: `snap.lines` gives the last ~120 lines (3x terminal height)
