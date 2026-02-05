---
name: request-recorder
description: >-
  Recorder CLI skill that captures HTTP payloads during debugging sessions and allows to review and log recent requests quickly.
allowed-tools: Bash(node recorder-cli.js)
metadata:
  owner: viteinfinite
---

# Recorder CLI

## Purpose
Provide a Node.js (18+) CLI that uses PM2 to start/stop a lightweight HTTP service. The service stores up to N incoming payloads in-memory (FIFO), and a `log` command outputs the stored entries in reverse order (newest first) as JSONL.

**Always** stop the server when finishing a debugging session.

## Commands
- `start` runs the service under PM2 (daemonized).
- `serve` runs the HTTP server in the current process (for PM2 or local debugging).
- `stop` stops the PM2 service.
- `log` prints logs in JSONL format, newest first.
- `--help` prints usage and exits.

## Inputs
- `--port` (default `4105`)
- `--window` (default `100`)
- Env `PORT` (fallback if `--port` not set)
- Env `PAYLOAD_WINDOW` (fallback if `--window` not set)

## Usage
- `node recorder-cli.js start --port 4105`
- `node recorder-cli.js start --port 4105 --window 100`
- `node recorder-cli.js log --port 4105`
- `node recorder-cli.js stop`
- `node recorder-cli.js --help`

## Tool location
- The tool lives at `.claude/skills/lbp-create-check/recorder-cli.js`.

## Operational notes
- If the configured port is already in use by this service, attempt to stop it before starting again.
- All HTTP methods are recorded (POST, PUT, PATCH, DELETE, etc). Only `GET /_logs` is handled specially.
