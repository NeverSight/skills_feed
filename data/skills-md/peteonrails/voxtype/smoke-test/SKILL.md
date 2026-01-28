---
name: smoke-test
description: Run interactive smoke tests for voxtype. Tests recording cycles, CLI overrides, signal handling, and service management. Use after installing a new build.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
  - TodoWrite
allowed-prompts:
  - tool: Bash
    prompt: run voxtype CLI commands
  - tool: Bash
    prompt: check voxtype daemon status
  - tool: Bash
    prompt: manage voxtype systemd service
  - tool: Bash
    prompt: read voxtype logs
  - tool: Bash
    prompt: send signals to voxtype daemon
  - tool: Bash
    prompt: check voxtype runtime files
  - tool: Bash
    prompt: read clipboard contents
  - tool: Bash
    prompt: backup and restore voxtype config
---

# Smoke Test

Interactive smoke tests for voxtype. Run after installing a new build to verify core functionality.

## Instructions

1. Read the test procedures from `docs/SMOKE_TESTS.md`
2. Use TodoWrite to create a checklist of all test sections
3. Run each test section in order, marking todos as completed
4. Report results in a summary table at the end

## Prerequisites

Before starting, verify:
- voxtype daemon is running: `systemctl --user status voxtype`
- Audio device is available
- Wayland session is active (for wtype/clipboard tests)

## Test Sections to Run

Read `docs/SMOKE_TESTS.md` and execute these test sections:

1. Basic Verification
2. Recording Cycle
3. CLI Overrides
4. Waybar JSON Output
5. Single Instance Enforcement
6. Config Validation
7. Signal Handling
8. Rapid Successive Recordings
9. Service Restart Cycle

## Results Summary

After running all tests, provide a summary table:

| Test | Result |
|------|--------|
| Basic verification | ✓/✗ |
| Recording cycle | ✓/✗ |
| CLI overrides | ✓/✗ |
| Waybar JSON | ✓/✗ |
| Single instance | ✓/✗ |
| Config validation | ✓/✗ |
| Signal handling | ✓/✗ |
| Rapid recordings | ✓/✗ |
| Service restarts | ✓/✗ |

## Known Issues to Watch For

- **Broken pipe panic**: If piping voxtype output through `head`, may see panic (cosmetic)
- **Language detection**: Without speech, Whisper may detect random languages (expected)
- **Empty transcription**: Normal when no actual speech is captured
- **Notification icon mismatch**: Parakeet binary with Whisper config may show wrong icon
