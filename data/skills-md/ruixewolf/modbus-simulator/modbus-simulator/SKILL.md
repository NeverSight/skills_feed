---
name: modbus-simulator
description: Run and control an isolated Modbus TCP/RTU simulator for automated integration tests, including readiness, fixture writes, state reads, logs, and safe process cleanup.
author: Ruixe Wolf
---

# Modbus Simulator Automation

Use this skill when a test needs a disposable Modbus device controlled through the versioned HTTP API.

## Owned-process workflow

1. Choose replaceable high ports that do not collide with the application under test. The examples use HTTP `15000` and Modbus TCP `15020`; change both if occupied. Never terminate an existing process whose ownership is unknown.
2. Start a process you own and retain its process handle/PID:

   ```sh
   npx --yes @ruixe/modbus-simulator@latest --host 127.0.0.1 --port 15000 --tcp-host 127.0.0.1 --tcp-port 15020 --ready-output json --ready-timeout 30 --strict-ready
   ```

   `@latest` resolves to the newest release on the npm registry at execution time.

3. Wait for one `MODBUS_SIMULATOR_READY` JSON record before starting the tested client. Stop on `MODBUS_SIMULATOR_ERROR` or readiness timeout.
4. Use `node scripts/control.mjs wait --base-url http://127.0.0.1:15000`, then configure and reset the simulator. Set `MODBUS_API_TOKEN` in the helper environment when authentication is enabled.
5. Run the client test. Use `write`/`write-encoded` for fixtures, `read` for assertions, and cursor `logs` for diagnostics.
6. Collect final health and logs, then terminate only the simulator process created in step 2.

Read [references/api.md](references/api.md) for commands and v1 endpoints. Read [references/addressing.md](references/addressing.md) when converting register notation or encoding typed values. Read [references/troubleshooting.md](references/troubleshooting.md) for serial, container/LAN, port, authentication, or readiness failures.
