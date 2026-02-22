---
name: wsl-embedded-debugging
description: Run embedded build/flash/debug workflows from WSL by invoking Windows executables that own USB/JTAG access (for example `cargo.exe`, `probe-rs.exe`, or `openocd.exe`). Use when an agent must reproduce firmware behavior on hardware, flash an MCU, collect bounded runtime logs, or debug probe connectivity from a WSL workspace.
---

# WSL Embedded Debugging

## Overview

Use Windows-side toolchains from WSL so code stays in the Linux workspace while USB-capable flashing and runtime logging happen through Windows executables.

## Codex Sandbox and Setup Requirements

Require an execution mode that can launch Windows executables from WSL:

- Prefer full-access sandboxing (for example `danger-full-access`) when running flash/debug commands from this skill.
- If sandbox policy blocks `*.exe` or `/mnt/c/...` binaries, stop and switch to a less restricted mode before continuing.

Require Windows tools to be callable from the WSL shell:

- Invoke by name when PATH bridging is configured (`cargo.exe`, `probe-rs.exe`, `openocd.exe`).
- Invoke by explicit path when PATH bridging is not configured (for example `/mnt/c/Users/<user>/.cargo/bin/cargo.exe`).
- Verify setup quickly with `cargo.exe --version` and `probe-rs.exe --version`.
- Use `wslpath -w <linux-path>` when a Windows-native tool requires Windows-style paths.

## Core Workflow

1. Confirm that the hardware step needs Windows USB access.
2. Run the command through `scripts/run_windows_embedded.sh`.
3. Use a bounded timeout to capture useful logs quickly.
4. Treat timeout exit `124` as expected log capture, not automatic failure.
5. Iterate with adjusted timeout, bin target, and command flags.

## Run Commands

Use this wrapper as the default execution path:

```bash
./scripts/run_windows_embedded.sh --timeout 15 -- cargo.exe run --bin <firmware-bin> --release
```

Capture logs to a file for later inspection:

```bash
./scripts/run_windows_embedded.sh --timeout 20 --log /tmp/embedded-run.log -- cargo.exe run --bin <firmware-bin> --release
```

Use log-only mode when log frequency is high and terminal/context noise is expensive:

```bash
./scripts/run_windows_embedded.sh --timeout 20 --log /tmp/embedded-run.log --log-only -- cargo.exe run --bin <firmware-bin> --release
```

Use artifacts mode when you want reproducible run bundles (`run.log` + `run.json`):

```bash
./scripts/run_windows_embedded.sh --timeout 20 --artifacts-dir /tmp/embedded-run --log-only --tail 40 -- cargo.exe run --bin <firmware-bin> --release
```

Run environment checks before long debugging loops:

```bash
./scripts/run_windows_embedded.sh --check -- cargo.exe run --bin <firmware-bin> --release
```

Pass any Windows executable command after `--` (for example `probe-rs.exe run ...`, `openocd.exe ...`, or vendor CLI tools).

## Choose Output Mode

Agents should intentionally choose output mode based on expected verbosity and run duration:

- Use raw terminal output for short, low-frequency logs where live feedback is valuable.
- Use `--log` for balanced runs that need both live stream and saved artifacts.
- Use `--log --log-only` for noisy/long sessions to avoid blowing context while preserving complete logs for targeted inspection.
- Use `--artifacts-dir` when reproducibility matters; this saves both `run.log` and `run.json` metadata.
- Use `--tail N` with `--log-only` when you still need a compact end-of-run preview.

`--log-only` is an intended first-class option, not a workaround.

## Interpret Exit Codes

- `0`: Command completed before timeout.
- `124`: Timeout reached; treat as successful bounded capture for long-running firmware sessions.
- Any other non-zero code: Treat as a real error and debug.

## Debug Loop

1. Start with 10–20 second timeout.
2. Confirm flash + early boot logs appear.
3. Increase timeout only when deeper runtime phases are needed.
4. Keep command explicit (`--bin`, `--release`, feature flags).
5. Repeat with focused changes between runs.

## Troubleshoot

- If `cargo.exe` is missing, verify Windows Rust toolchain installation and PATH exposure to WSL.
- If flashing fails with probe errors, verify the device is visible to Windows and no other process owns the probe.
- If no runtime logs appear, confirm logger transport settings and runtime command configuration.

Use `references/wsl-windows-embedded-troubleshooting.md` for detailed checks and alternatives.
