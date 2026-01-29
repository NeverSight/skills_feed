---
name: makefile
description: GNU Make automation and build system guidance
version: 2.0.0
release_date: "2023-02-26"
---

# Makefile Skill

Guidance for creating and maintaining GNU Make build automation.

## Quick Navigation

| Topic                         | Reference                               |
| ----------------------------- | --------------------------------------- |
| Rules, prerequisites, targets | [syntax.md](references/syntax.md)       |
| Variable types and assignment | [variables.md](references/variables.md) |
| Built-in functions            | [functions.md](references/functions.md) |
| Special and phony targets     | [targets.md](references/targets.md)     |
| Recipe execution, parallel    | [recipes.md](references/recipes.md)     |
| Implicit and pattern rules    | [implicit.md](references/implicit.md)   |
| Common practical patterns     | [patterns.md](references/patterns.md)   |

---

## Core Concepts

### Rule Structure

```makefile
target: prerequisites
        recipe
```

**Critical:** Recipe lines MUST start with TAB character.

### File vs Phony Targets

```makefile
# File target - creates/updates a file
build/app.o: src/app.c
        $(CC) -c $< -o $@

# Phony target - action, not a file
.PHONY: clean test install

clean:
        rm -rf build/
```

### Variable Assignment

| Operator | Name        | When Expanded           |
| -------- | ----------- | ----------------------- |
| `:=`     | Simple      | Once, at definition     |
| `?=`     | Conditional | If not already set      |
| `=`      | Recursive   | Each use (late binding) |
| `+=`     | Append      | Adds to existing value  |

```makefile
CC := gcc              # Immediate
CFLAGS ?= -O2          # Default, overridable
DEBUG = $(VERBOSE)     # Late binding
CFLAGS += -Wall        # Append
```

### Automatic Variables

| Variable | Meaning                         |
| -------- | ------------------------------- |
| `$@`     | Target                          |
| `$<`     | First prerequisite              |
| `$^`     | All prerequisites (unique)      |
| `$?`     | Prerequisites newer than target |
| `$*`     | Stem in pattern rules           |

---

## Essential Patterns

### Self-Documenting Help

```makefile
.DEFAULT_GOAL := help

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync

test: ## Run tests
	uv run pytest
```

### Platform Detection

```makefile
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
    OPEN := open
else ifeq ($(UNAME_S),Linux)
    OPEN := xdg-open
endif
```

### Build Directory

```makefile
BUILDDIR := build
SOURCES := $(wildcard src/*.c)
OBJECTS := $(patsubst src/%.c,$(BUILDDIR)/%.o,$(SOURCES))

$(BUILDDIR)/%.o: src/%.c | $(BUILDDIR)
	$(CC) -c $< -o $@

$(BUILDDIR):
	mkdir -p $@
```

### Environment Export

```makefile
export PYTHONPATH := $(PWD)/src
export DATABASE_URL

test:
	pytest tests/  # sees exported variables
```

---

## Common Targets

### Quality Checks

```makefile
.PHONY: lint format check test

lint: ## Run linters
	ruff check .
	mypy src/

format: ## Format code
	ruff format .

check: format lint test ## All quality checks
```

### Cleanup

```makefile
.PHONY: clean clean-all

clean: ## Remove build artifacts
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

clean-all: clean ## Remove all generated files
	rm -rf .venv .pytest_cache .mypy_cache
```

### Docker Integration

```makefile
IMAGE := myapp
VERSION := $(shell git describe --tags --always)

docker-build: ## Build Docker image
	docker build -t $(IMAGE):$(VERSION) .

docker-run: ## Run container
	docker run -d -p 8000:8000 $(IMAGE):$(VERSION)
```

---

## Recipe Execution

### Each Line = Separate Shell

```makefile
# Won't work - cd lost between lines
bad:
	cd subdir
	pwd           # Still in original dir!

# Correct - combine commands
good:
	cd subdir && pwd

# Or use line continuation
also-good:
	cd subdir && \
	pwd && \
	make
```

### Silent and Error Handling

```makefile
target:
	@echo "@ suppresses command echo"
	-rm -f maybe.txt    # - ignores errors
```

### Parallel Execution

```bash
make -j4              # 4 parallel jobs
make -j4 lint test    # Run lint and test in parallel
```

---

## Output Discipline

**One line in, one line out.** Avoid echo spam.

```makefile
# ❌ Too chatty
start:
	@echo "Starting services..."
	docker compose up -d
	@echo "Waiting..."
	@sleep 3
	@echo "Done!"

# ✅ Concise
start: ## Start services
	@echo "Starting at http://localhost:8000 ..."
	@docker compose up -d
	@echo "Logs: docker compose logs -f"
```

---

## Conditionals

```makefile
DEBUG ?= 0

ifeq ($(DEBUG),1)
    CFLAGS += -g -O0
else
    CFLAGS += -O2
endif

ifdef CI
    TEST_FLAGS := --ci
endif
```

---

## Including Files

```makefile
# Required include (error if missing)
include config.mk

# Optional include (silent if missing)
-include local.mk
-include .env
```

---

## Common Pitfalls

| Pitfall               | Problem                                 | Solution                 |
| --------------------- | --------------------------------------- | ------------------------ |
| Spaces in recipes     | Recipes need TAB                        | Use actual TAB character |
| Missing .PHONY        | `make test` fails if `test` file exists | Declare `.PHONY: test`   |
| cd in recipes         | Each line is new shell                  | Use `cd dir && command`  |
| `=` vs `:=` confusion | Unexpected late expansion               | Use `:=` by default      |
| Unexported vars       | Subprocesses don't see vars             | `export VAR`             |
| Complex shell in make | Hard to maintain                        | Move to external script  |

---

## Quick Reference

```makefile
# Makefile Template
.DEFAULT_GOAL := help
SHELL := /bin/bash
.SHELLFLAGS := -ec

.PHONY: help install test lint format clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install dependencies
	uv sync --extra dev

test: ## Run tests
	uv run pytest tests/ -v

lint: ## Run linters
	uv run ruff check .

format: ## Format code
	uv run ruff format .

clean: ## Clean artifacts
	rm -rf build/ dist/ .pytest_cache
```

---

## See Also

- [GNU Make Manual](https://www.gnu.org/software/make/manual/make.html)
- [patterns.md](references/patterns.md) - Extended patterns and recipes
