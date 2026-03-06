---
name: makefile-for-telegram
description: Generate a Makefile for Telegram bot projects with LaunchAgent service management. Use when setting up a new Telegram bot project or adding service management to an existing one.
---

# Makefile for Telegram Bot

Generate a production-ready Makefile for Telegram bot projects running on macOS with LaunchAgent background service support.

## When to Use

- Setting up a new Telegram bot project
- Adding macOS LaunchAgent service management
- Need quick start/stop/restart commands for a bot
- Want to manage bot as a background service

## Features Generated

### Quick Start

| Command      | Description                                  |
| ------------ | -------------------------------------------- |
| `make setup` | First-time setup (install deps, create .env) |
| `make run`   | Run bot in foreground                        |
| `make dev`   | Run with auto-reload (watch mode)            |

### Background Service (macOS LaunchAgent)

| Command          | Description                          |
| ---------------- | ------------------------------------ |
| `make start`     | Install and start background service |
| `make stop`      | Stop background service              |
| `make restart`   | Restart background service           |
| `make status`    | Check if service is running          |
| `make logs`      | Tail stdout logs                     |
| `make logs-err`  | Tail stderr logs                     |
| `make uninstall` | Remove background service            |

### Development

| Command          | Description                |
| ---------------- | -------------------------- |
| `make install`   | Install dependencies       |
| `make test`      | Run tests                  |
| `make typecheck` | Run TypeScript type check  |
| `make clean`     | Remove temp files and logs |

## Requirements

Before generating, ensure the project has:

1. **LaunchAgent plist template** at `launchagent/com.{project-name}.plist.template`
2. **Environment file template** at `.env.example`
3. **Bun** as the runtime (or modify for npm/node)

## Instructions

### Step 1: Gather Project Info

Ask user for:

- Project name (for plist label, e.g., `claude-telegram-ts`)
- Runtime command (default: `bun run src/index.ts`)
- Log file paths (default: `/tmp/{project-name}.log`)

### Step 2: Generate Makefile

Create `Makefile` with:

```makefile
# {Project Name} - Makefile
# Usage: make <target>

SHELL := /bin/bash

PLIST_NAME := com.{project-name}
PLIST_PATH := ~/Library/LaunchAgents/$(PLIST_NAME).plist
PLIST_TEMPLATE := launchagent/$(PLIST_NAME).plist.template
LOG_FILE := /tmp/{project-name}.log
ERR_FILE := /tmp/{project-name}.err

.PHONY: help install setup run dev stop start restart status logs logs-err clean typecheck test uninstall

help:
	@echo "{Project Name}"
	@echo ""
	@echo "Quick start:"
	@echo "  make setup      - First-time setup (install deps, create .env)"
	@echo "  make run        - Run bot in foreground"
	@echo "  make dev        - Run with auto-reload (watch mode)"
	@echo ""
	@echo "Background service (macOS LaunchAgent):"
	@echo "  make start      - Install and start background service"
	@echo "  make stop       - Stop background service"
	@echo "  make restart    - Restart background service"
	@echo "  make status     - Check if service is running"
	@echo "  make logs       - Tail stdout logs"
	@echo "  make logs-err   - Tail stderr logs"
	@echo "  make uninstall  - Remove background service"
	@echo ""
	@echo "Development:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make typecheck  - Run TypeScript type check"
	@echo "  make clean      - Remove temp files and logs"

install:
	bun install

setup: install
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "Created .env from template"; \
		echo ">>> Edit .env with your credentials"; \
	else \
		echo ".env already exists"; \
	fi

run:
	bun run start

dev:
	bun run dev

test:
	bun test

typecheck:
	bun run typecheck

start:
	@if [ ! -f .env ]; then \
		echo "Error: .env not found. Run 'make setup' first."; \
		exit 1; \
	fi
	@echo "Installing LaunchAgent..."
	@mkdir -p ~/Library/LaunchAgents
	@export $$(grep -v '^#' .env | xargs) && \
	sed -e "s|/Users/USERNAME/.bun/bin/bun|$$(command -v bun)|g" \
	    -e "s|/Users/USERNAME/Dev/{project-path}|$$(pwd)|g" \
	    -e "s|USERNAME|$$(whoami)|g" \
	    -e "s|your-bot-token-here|$${TELEGRAM_BOT_TOKEN}|g" \
	    -e "s|<string>123456789</string>|<string>$${TELEGRAM_ALLOWED_USERS}</string>|g" \
	    $(PLIST_TEMPLATE) > $(PLIST_PATH)
	@echo "Created $(PLIST_PATH) with values from .env"
	@launchctl unload $(PLIST_PATH) 2>/dev/null || true
	@launchctl load $(PLIST_PATH)
	@echo "Service started. Check 'make logs' for output."

stop:
	@launchctl unload $(PLIST_PATH) 2>/dev/null || echo "Service not running"
	@echo "Service stopped"

restart:
	@launchctl kickstart -k gui/$$(id -u)/$(PLIST_NAME) 2>/dev/null || \
		(echo "Service not loaded. Run 'make start' first." && exit 1)
	@echo "Service restarted"

status:
	@if launchctl list | grep -q $(PLIST_NAME); then \
		echo "Service: RUNNING"; \
		launchctl list $(PLIST_NAME); \
	else \
		echo "Service: NOT RUNNING"; \
	fi

uninstall: stop
	@rm -f $(PLIST_PATH)
	@echo "Service uninstalled"

logs:
	@if [ -f $(LOG_FILE) ]; then \
		tail -f $(LOG_FILE); \
	else \
		echo "No log file yet. Start the service first."; \
	fi

logs-err:
	@if [ -f $(ERR_FILE) ]; then \
		tail -f $(ERR_FILE); \
	else \
		echo "No error log yet."; \
	fi

clean:
	rm -f $(LOG_FILE) $(ERR_FILE) 2>/dev/null || true
	@echo "Cleaned temp files"
```

### Step 3: Customize sed Replacements

The `start` target needs sed patterns matching the plist template. Common patterns:

- `your-bot-token-here` → `${TELEGRAM_BOT_TOKEN}`
- `123456789` → `${TELEGRAM_ALLOWED_USERS}`
- `/Users/USERNAME` → `$(whoami)` expanded path
- Add more `-e "s|pattern|replacement|g"` for other env vars

### Step 4: Verify

```bash
make help
make setup
make run  # Test in foreground first
make start  # Then as service
make status
```

## Example

**Input:** "Create a Makefile for my telegram bot project"

**Output:** Generate complete Makefile, ask for project-specific values (name, paths), and customize sed patterns based on their plist template.
