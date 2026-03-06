---
name: dx-optimizer
description: Improve developer experience, tooling, and workflows. Use when setting up projects or reducing development friction.
---

# Developer Experience

Optimize tooling and workflows for productivity.

## When to use

- New project setup
- Onboarding improvements
- Build time optimization
- Workflow automation
- Tooling configuration

## Quick wins

### Package.json scripts

```json
{
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --fix",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage",
    "prepare": "husky",
    "validate": "npm run typecheck && npm run lint && npm run test"
  }
}
```

### Git hooks (husky + lint-staged)

```json
// package.json
{
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yml}": ["prettier --write"]
  }
}
```

```bash
# .husky/pre-commit
npm run lint-staged

# .husky/commit-msg
npx commitlint --edit $1
```

### VS Code settings

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "typescript.preferences.importModuleSpecifier": "relative",
  "files.associations": {
    "*.css": "tailwindcss"
  }
}
```

```json
// .vscode/extensions.json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-typescript-next"
  ]
}
```

## Makefile

```makefile
.PHONY: help dev build test clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

dev: ## Start development server
	npm run dev

build: ## Build for production
	npm run build

test: ## Run tests
	npm run test

lint: ## Run linter
	npm run lint

clean: ## Clean build artifacts
	rm -rf .next node_modules/.cache

setup: ## Initial project setup
	npm install
	cp .env.example .env.local
	@echo "Setup complete! Run 'make dev' to start."
```

## Environment setup

```bash
# .env.example (template)
DATABASE_URL=postgresql://localhost:5432/myapp
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key-here

# Check for required env vars
check_env() {
  local missing=()
  for var in DATABASE_URL API_KEY; do
    if [[ -z "${!var}" ]]; then
      missing+=("$var")
    fi
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Missing env vars: ${missing[*]}"
    exit 1
  fi
}
```

## Success metrics

- Clone to running: <5 minutes
- Build time: <30 seconds
- Test suite: <60 seconds
- Hot reload: <500ms

## Checklist

- [ ] One-command setup (`make setup`)
- [ ] Automatic formatting on save
- [ ] Pre-commit hooks for quality
- [ ] Clear error messages
- [ ] Up-to-date README

## Examples

**Input:** "Speed up our dev workflow"
**Action:** Add parallel tasks, caching, incremental builds

**Input:** "New developer can't set up project"
**Action:** Simplify setup, add better docs, create setup script
