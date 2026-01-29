---
name: makefile
description: >
  Use when creating or amending Makefiles for process lifecycle management. Best for
  projects needing background process management, PID tracking, logging, and status
  monitoring. Triggers on: "use makefile mode", "makefile", "create makefile",
  "process management", "background jobs", "start/stop services".
  Full access mode - can create/modify Makefiles and supporting files.
---

# Makefile Mode

Create and manage Makefiles optimized for AI agent interaction and process lifecycle management.

## Core Philosophy

> "Start clean. Stop clean. Log everything. Know your state."

**Principles**:

- **AI-agent first**: Outputs readable programmatically (no interactive prompts)
- **Background by default**: Services run detached; read logs, don't spawn terminals
- **Comprehensive logging**: All output to files at `.logs/` - nothing lost
- **Process hygiene**: Clean starts, clean stops, no orphan processes
- **Adaptable patterns**: Works for any service topology

## Pre-Implementation Discovery

Before creating a Makefile, determine:

### Service Topology

- [ ] What services exist? (backend, frontend, workers, etc.)
- [ ] Do any services depend on others? (start order)
- [ ] Are there external dependencies? (databases, emulators, etc.)

### Startup Requirements

- [ ] What commands start each service?
- [ ] What environment variables are needed?
- [ ] What ports are used? (must be unique per-service)
- [ ] Any initialization steps? (migrations, seeds, etc.)

### Testing & Quality

- [ ] What test commands exist? (unit, integration, e2e)
- [ ] What prerequisites for tests? (docker, emulators, etc.)
- [ ] What linting/formatting tools? (eslint, ruff, mypy, etc.)

### Project Context

- [ ] Language/framework? (affects conventions)
- [ ] Development vs Production behavior?
- [ ] Team conventions? (existing practices to preserve)

## Makefile Architecture

Standard structure (in order):

```makefile
# 1. Configuration Variables
# 2. Directory Setup
# 3. Service Lifecycle Targets (run-*, stop-*)
# 4. Combined Operations (run, stop, restart)
# 5. Testing & Quality (test, lint)
# 6. Utility Targets (logs, status, help)
# 7. .PHONY declarations
```

## Core Patterns Library

### A. Starting a Service (Background with PID Tracking)

```makefile
run-backend:
	@mkdir -p .pids .logs
	@if lsof -ti:$(BACKEND_PORT) > /dev/null 2>&1; then \
		echo "❌ Backend already running on port $(BACKEND_PORT)"; \
		exit 1; \
	fi
	@echo "🚀 Starting backend on port $(BACKEND_PORT)..."
	@nohup $(BACKEND_CMD) > .logs/backend.log 2>&1 & echo $$! > .pids/backend.pid
	@echo "✅ Backend started (PID: $$(cat .pids/backend.pid))"
```

### B. Stopping a Service (Process Group Cleanup)

```makefile
stop-backend:
	@if [ -f .pids/backend.pid ]; then \
		PID=$$(cat .pids/backend.pid); \
		if ps -p $$PID > /dev/null 2>&1; then \
			echo "🛑 Stopping backend (PID: $$PID)..."; \
			kill -TERM -- -$$PID 2>/dev/null || kill $$PID; \
			rm .pids/backend.pid; \
			echo "✅ Backend stopped"; \
		else \
			echo "⚠️  Backend process not found, cleaning up PID file"; \
			rm .pids/backend.pid; \
		fi \
	else \
		echo "ℹ️  Backend not running"; \
	fi
```

### C. Status Checking

```makefile
status:
	@echo "📊 Service Status:"
	@echo ""
	@for service in backend frontend; do \
		if [ -f .pids/$$service.pid ]; then \
			PID=$$(cat .pids/$$service.pid); \
			if ps -p $$PID > /dev/null 2>&1; then \
				echo "✅ $$service: running (PID: $$PID)"; \
			else \
				echo "❌ $$service: stopped (stale PID file)"; \
			fi \
		else \
			echo "⚪ $$service: not running"; \
		fi; \
	done
```

### D. Log Tailing

```makefile
logs:
	@if [ -f .logs/backend.log ] || [ -f .logs/frontend.log ]; then \
		tail -n 50 .logs/*.log 2>/dev/null; \
	else \
		echo "No logs found"; \
	fi

logs-follow:
	@tail -f .logs/*.log 2>/dev/null
```

### E. Combined Operations

```makefile
run: run-backend run-frontend
stop: stop-frontend stop-backend  # Reverse order for clean shutdown
restart: stop run
```

### F. Testing with Prerequisites

```makefile
test: test-setup
	@echo "🧪 Running tests..."
	@$(TEST_CMD)

test-setup:
	@if [ -n "$(DOCKER_COMPOSE_FILE)" ] && [ -f "$(DOCKER_COMPOSE_FILE)" ]; then \
		docker-compose -f $(DOCKER_COMPOSE_FILE) up -d; \
	fi
```

### G. Help Target (Self-Documenting)

```makefile
.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo ""
	@echo "  make run              Start all services"
	@echo "  make stop             Stop all services"
	@echo "  make restart          Restart all services"
	@echo "  make status           Show service status"
	@echo "  make logs             Show recent logs"
	@echo "  make logs-follow      Follow logs in real-time"
	@echo "  make test             Run all tests"
	@echo "  make lint             Run linters and formatters"
	@echo ""
	@echo "Individual services:"
	@echo "  make run-backend      Start backend only"
	@echo "  make run-frontend     Start frontend only"
	@echo "  make stop-backend     Stop backend only"
	@echo "  make stop-frontend    Stop frontend only"
```

## Adaptation Patterns

| Scenario            | Adaptation                                                    |
| ------------------- | ------------------------------------------------------------- |
| Multiple backends   | Use suffix naming: `run-api`, `run-worker`, etc.              |
| Database migrations | Add `migrate` target, make `run-backend` depend on it         |
| Emulators           | Treat like any other service with PID tracking                |
| Docker Compose      | Wrap docker-compose commands, track container IDs             |
| Monorepo            | Use subdirectory variables: `cd $(API_DIR) && ...`            |
| Multiple test types | Separate targets: `test-unit`, `test-integration`, `test-e2e` |
| Watch modes         | Use separate watch targets, don't mix with regular run        |

## Best Practices Checklist

Before completing a Makefile, verify:

- [ ] All targets are `.PHONY` (or appropriately not)
- [ ] Port numbers are configurable via variables
- [ ] Unique ports per service (no conflicts)
- [ ] All logs go to `.logs/` directory
- [ ] All PIDs go to `.pids/` directory
- [ ] Process group killing (handles child processes)
- [ ] Port conflict detection before start
- [ ] Human-readable output (colors/emojis)
- [ ] `help` target is default (listed first or `.DEFAULT_GOAL`)
- [ ] Variables use `:=` (simple expansion)
- [ ] Error messages are clear and actionable
- [ ] Status command shows actual state
- [ ] Clean shutdown on stop (SIGTERM first)
- [ ] Idempotent operations (safe to run twice)

## Common Issues & Solutions

| Problem                              | Solution                                    |
| ------------------------------------ | ------------------------------------------- |
| PID file exists but process dead     | Check `ps -p $PID` before using PID file    |
| Child processes survive parent kill  | Use `kill -TERM -- -$PID` (process group)   |
| Port already in use                  | Check with `lsof -ti:$PORT` before start    |
| Logs interleaved/unreadable          | Separate log files per service              |
| Service starts but immediately exits | Redirect stderr: `2>&1`, check `.logs/`     |
| Make variables not evaluated         | Use `:=` not `=`, check `$$` vs `$`         |
| Colors don't show in logs            | Use `unbuffer` or configure service for TTY |
| Can't stop service (permission)      | Run make with same user that started it     |

## Implementation Workflow

### Creating a New Makefile

1. **Discovery**: Ask questions (see Discovery section)
2. **Configuration**: Set up variables (ports, commands, paths)
3. **Core services**: Implement run/stop for each service
4. **Combined ops**: Add run/stop/restart for all services
5. **Utilities**: Add status, logs, help
6. **Testing**: Add test targets with prerequisites
7. **Quality**: Add lint/format targets
8. **Validation**: Test each target, verify idempotency
9. **Documentation**: Ensure help is complete and accurate

### Amending an Existing Makefile

1. **Read current Makefile**: Understand existing structure
2. **Identify gaps**: Compare against best practices checklist
3. **Plan changes**: Determine what to add/modify
4. **Preserve conventions**: Keep existing naming/style
5. **Incremental changes**: Add features one at a time
6. **Test each change**: Verify nothing breaks
7. **Update help**: Reflect new targets

## Complete Template

A minimal working template for a full-stack app:

```makefile
# =============================================================================
# Configuration
# =============================================================================
BACKEND_PORT := 3001
FRONTEND_PORT := 3000
BACKEND_CMD := npm run dev --prefix backend
FRONTEND_CMD := npm run dev --prefix frontend
TEST_CMD := npm test

# =============================================================================
# Directory Setup
# =============================================================================
$(shell mkdir -p .pids .logs)

# =============================================================================
# Service Lifecycle
# =============================================================================
run-backend:
	@if lsof -ti:$(BACKEND_PORT) > /dev/null 2>&1; then \
		echo "❌ Backend already running on port $(BACKEND_PORT)"; \
		exit 1; \
	fi
	@echo "🚀 Starting backend on port $(BACKEND_PORT)..."
	@nohup $(BACKEND_CMD) > .logs/backend.log 2>&1 & echo $$! > .pids/backend.pid
	@echo "✅ Backend started (PID: $$(cat .pids/backend.pid))"

run-frontend:
	@if lsof -ti:$(FRONTEND_PORT) > /dev/null 2>&1; then \
		echo "❌ Frontend already running on port $(FRONTEND_PORT)"; \
		exit 1; \
	fi
	@echo "🚀 Starting frontend on port $(FRONTEND_PORT)..."
	@nohup $(FRONTEND_CMD) > .logs/frontend.log 2>&1 & echo $$! > .pids/frontend.pid
	@echo "✅ Frontend started (PID: $$(cat .pids/frontend.pid))"

stop-backend:
	@if [ -f .pids/backend.pid ]; then \
		PID=$$(cat .pids/backend.pid); \
		if ps -p $$PID > /dev/null 2>&1; then \
			echo "🛑 Stopping backend (PID: $$PID)..."; \
			kill -TERM -- -$$PID 2>/dev/null || kill $$PID; \
			rm .pids/backend.pid; \
			echo "✅ Backend stopped"; \
		else \
			echo "⚠️  Backend not found, cleaning up PID file"; \
			rm .pids/backend.pid; \
		fi \
	else \
		echo "ℹ️  Backend not running"; \
	fi

stop-frontend:
	@if [ -f .pids/frontend.pid ]; then \
		PID=$$(cat .pids/frontend.pid); \
		if ps -p $$PID > /dev/null 2>&1; then \
			echo "🛑 Stopping frontend (PID: $$PID)..."; \
			kill -TERM -- -$$PID 2>/dev/null || kill $$PID; \
			rm .pids/frontend.pid; \
			echo "✅ Frontend stopped"; \
		else \
			echo "⚠️  Frontend not found, cleaning up PID file"; \
			rm .pids/frontend.pid; \
		fi \
	else \
		echo "ℹ️  Frontend not running"; \
	fi

# =============================================================================
# Combined Operations
# =============================================================================
run: run-backend run-frontend
stop: stop-frontend stop-backend
restart: stop run

# =============================================================================
# Testing & Quality
# =============================================================================
test:
	@echo "🧪 Running tests..."
	@$(TEST_CMD)

lint:
	@echo "🔍 Running linters..."
	@npm run lint 2>&1 || true

# =============================================================================
# Utilities
# =============================================================================
status:
	@echo "📊 Service Status:"
	@echo ""
	@for service in backend frontend; do \
		if [ -f .pids/$$service.pid ]; then \
			PID=$$(cat .pids/$$service.pid); \
			if ps -p $$PID > /dev/null 2>&1; then \
				echo "✅ $$service: running (PID: $$PID)"; \
			else \
				echo "❌ $$service: stopped (stale PID file)"; \
			fi \
		else \
			echo "⚪ $$service: not running"; \
		fi; \
	done

logs:
	@tail -n 50 .logs/*.log 2>/dev/null || echo "No logs found"

logs-follow:
	@tail -f .logs/*.log 2>/dev/null

clean:
	@rm -rf .pids .logs
	@echo "🧹 Cleaned up PID and log files"

# =============================================================================
# Help
# =============================================================================
.DEFAULT_GOAL := help

help:
	@echo "Available targets:"
	@echo ""
	@echo "  make run           Start all services"
	@echo "  make stop          Stop all services"
	@echo "  make restart       Restart all services"
	@echo "  make status        Show service status"
	@echo "  make logs          Show recent logs (last 50 lines)"
	@echo "  make logs-follow   Follow logs in real-time"
	@echo "  make test          Run tests"
	@echo "  make lint          Run linters"
	@echo "  make clean         Remove PID and log files"
	@echo ""
	@echo "Individual services:"
	@echo "  make run-backend   Start backend only"
	@echo "  make run-frontend  Start frontend only"
	@echo "  make stop-backend  Stop backend only"
	@echo "  make stop-frontend Stop frontend only"

# =============================================================================
# .PHONY
# =============================================================================
.PHONY: run run-backend run-frontend stop stop-backend stop-frontend \
        restart status logs logs-follow test lint clean help
```

## Gitignore Additions

Remind users to add these to `.gitignore`:

```
.pids/
.logs/
```
