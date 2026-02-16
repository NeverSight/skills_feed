---
name: automation-scripts
description: Build automation, task runners, and scripting tools
domain: tools-integrations
version: 1.0.0
tags: [make, npm-scripts, bash, automation, turbo, nx]
triggers:
  keywords:
    primary: [automation, script, makefile, npm script, task runner, turbo, nx]
    secondary: [build, gulp, grunt, husky, lint-staged, pre-commit]
  context_boost: [workflow, ci, build, tooling]
  context_penalty: [frontend, ui, design]
  priority: medium
---

# Automation & Scripts

## Overview

Build automation, task runners, and scripting patterns for development workflows.

---

## npm Scripts

### Package.json Scripts

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "type-check": "tsc --noEmit",
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "db:migrate": "prisma migrate deploy",
    "db:generate": "prisma generate",
    "db:seed": "tsx prisma/seed.ts",
    "db:studio": "prisma studio",
    "prepare": "husky install",
    "precommit": "lint-staged",
    "validate": "npm run type-check && npm run lint && npm run test",
    "clean": "rm -rf .next node_modules/.cache",
    "analyze": "ANALYZE=true next build"
  }
}
```

### Script Composition

```json
{
  "scripts": {
    "check:all": "npm-run-all --parallel lint type-check test:unit",
    "build:all": "npm-run-all clean build test:e2e",
    "ci": "npm-run-all --serial lint type-check test build",
    "prerelease": "npm run validate",
    "release": "standard-version",
    "postrelease": "git push --follow-tags"
  }
}
```

---

## Makefile

```makefile
# Makefile
.PHONY: dev build test lint clean deploy help

# Default target
.DEFAULT_GOAL := help

# Variables
NODE_ENV ?= development
DOCKER_TAG ?= latest
PROJECT_NAME := myapp

# Development
dev: ## Start development server
	npm run dev

install: ## Install dependencies
	npm ci

# Build
build: ## Build for production
	npm run build

build-docker: ## Build Docker image
	docker build -t $(PROJECT_NAME):$(DOCKER_TAG) .

# Testing
test: ## Run all tests
	npm run test

test-watch: ## Run tests in watch mode
	npm run test:watch

test-coverage: ## Run tests with coverage
	npm run test:coverage

test-e2e: ## Run E2E tests
	npm run test:e2e

# Linting & Formatting
lint: ## Run linter
	npm run lint

lint-fix: ## Fix linting issues
	npm run lint:fix

format: ## Format code
	npm run format

type-check: ## Run type checking
	npm run type-check

# Database
db-migrate: ## Run database migrations
	npm run db:migrate

db-seed: ## Seed database
	npm run db:seed

db-reset: ## Reset database
	npm run db:reset

# Docker
docker-up: ## Start Docker services
	docker-compose up -d

docker-down: ## Stop Docker services
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

# Deployment
deploy-staging: ## Deploy to staging
	./scripts/deploy.sh staging

deploy-prod: ## Deploy to production
	./scripts/deploy.sh production

# Cleanup
clean: ## Clean build artifacts
	rm -rf dist .next coverage node_modules/.cache
	npm run clean

clean-all: clean ## Clean everything including node_modules
	rm -rf node_modules

# CI/CD
ci: lint type-check test build ## Run CI pipeline

# Help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
```

---

## Bash Scripts

### Build Script

```bash
#!/bin/bash
# scripts/build.sh

set -e  # Exit on error
set -o pipefail  # Exit on pipe failure

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
BUILD_DIR="dist"
NODE_ENV="${NODE_ENV:-production}"

# Functions
clean() {
    log_info "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
}

install_deps() {
    log_info "Installing dependencies..."
    npm ci
}

lint() {
    log_info "Running linter..."
    npm run lint
}

type_check() {
    log_info "Running type check..."
    npm run type-check
}

test() {
    log_info "Running tests..."
    npm run test -- --run
}

build() {
    log_info "Building for ${NODE_ENV}..."
    NODE_ENV=$NODE_ENV npm run build
}

# Main
main() {
    local start_time=$(date +%s)

    log_info "Starting build process..."

    clean
    install_deps
    lint
    type_check
    test
    build

    local end_time=$(date +%s)
    local duration=$((end_time - start_time))

    log_info "Build completed in ${duration}s"
}

# Run
main "$@"
```

### Deployment Script

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

ENVIRONMENT="${1:-staging}"
VERSION="${2:-$(git rev-parse --short HEAD)}"

log() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"; }

validate_environment() {
    case "$ENVIRONMENT" in
        staging|production)
            log "Deploying to $ENVIRONMENT"
            ;;
        *)
            log "Error: Invalid environment '$ENVIRONMENT'"
            log "Usage: $0 [staging|production] [version]"
            exit 1
            ;;
    esac
}

confirm_production() {
    if [ "$ENVIRONMENT" = "production" ]; then
        read -p "Are you sure you want to deploy to production? (yes/no) " -r
        if [ "$REPLY" != "yes" ]; then
            log "Deployment cancelled"
            exit 0
        fi
    fi
}

build_image() {
    log "Building Docker image..."
    docker build -t "myapp:$VERSION" .
    docker tag "myapp:$VERSION" "registry.example.com/myapp:$VERSION"
}

push_image() {
    log "Pushing image to registry..."
    docker push "registry.example.com/myapp:$VERSION"
}

deploy_kubernetes() {
    log "Deploying to Kubernetes..."

    # Update image tag in deployment
    kubectl set image deployment/myapp \
        myapp="registry.example.com/myapp:$VERSION" \
        -n "$ENVIRONMENT"

    # Wait for rollout
    kubectl rollout status deployment/myapp -n "$ENVIRONMENT" --timeout=5m
}

run_smoke_tests() {
    log "Running smoke tests..."

    local url
    case "$ENVIRONMENT" in
        staging)    url="https://staging.example.com" ;;
        production) url="https://example.com" ;;
    esac

    # Health check
    if curl -sf "$url/health" > /dev/null; then
        log "Health check passed"
    else
        log "Health check failed!"
        exit 1
    fi
}

notify_slack() {
    local status="$1"
    local webhook_url="$SLACK_WEBHOOK_URL"

    curl -X POST -H 'Content-type: application/json' \
        --data "{\"text\":\"Deployment to $ENVIRONMENT: $status (version: $VERSION)\"}" \
        "$webhook_url"
}

main() {
    validate_environment
    confirm_production

    log "Starting deployment of version $VERSION to $ENVIRONMENT"

    build_image
    push_image
    deploy_kubernetes
    run_smoke_tests

    notify_slack "Success"
    log "Deployment completed successfully"
}

# Error handling
trap 'notify_slack "Failed"; log "Deployment failed!"' ERR

main
```

---

## Monorepo Tools

### Turborepo

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**"]
    },
    "lint": {
      "outputs": []
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "deploy": {
      "dependsOn": ["build", "test", "lint"],
      "outputs": []
    }
  }
}
```

```bash
# Run build in all packages
turbo build

# Run dev in specific packages
turbo dev --filter=web --filter=api

# Run with caching
turbo build --cache-dir=.turbo

# Dry run to see what would execute
turbo build --dry-run
```

### Nx

```json
// nx.json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"]
    },
    "test": {
      "inputs": ["default", "^production"]
    }
  },
  "namedInputs": {
    "default": ["{projectRoot}/**/*"],
    "production": [
      "default",
      "!{projectRoot}/**/*.spec.ts",
      "!{projectRoot}/tsconfig.spec.json"
    ]
  }
}
```

```bash
# Run affected tests
nx affected:test

# Build specific project
nx build my-app

# Run task graph
nx graph

# Generate new library
nx generate @nx/js:library shared-utils
```

---

## Task Automation

### Gulp

```javascript
// gulpfile.js
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const autoprefixer = require('gulp-autoprefixer');
const cleanCSS = require('gulp-clean-css');
const terser = require('gulp-terser');
const imagemin = require('gulp-imagemin');
const del = require('del');

// Clean
gulp.task('clean', () => del(['dist']));

// Styles
gulp.task('styles', () =>
  gulp.src('src/styles/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(cleanCSS())
    .pipe(gulp.dest('dist/css'))
);

// Scripts
gulp.task('scripts', () =>
  gulp.src('src/js/**/*.js')
    .pipe(terser())
    .pipe(gulp.dest('dist/js'))
);

// Images
gulp.task('images', () =>
  gulp.src('src/images/**/*')
    .pipe(imagemin())
    .pipe(gulp.dest('dist/images'))
);

// Watch
gulp.task('watch', () => {
  gulp.watch('src/styles/**/*.scss', gulp.series('styles'));
  gulp.watch('src/js/**/*.js', gulp.series('scripts'));
  gulp.watch('src/images/**/*', gulp.series('images'));
});

// Build
gulp.task('build', gulp.series(
  'clean',
  gulp.parallel('styles', 'scripts', 'images')
));

// Default
gulp.task('default', gulp.series('build', 'watch'));
```

---

## Pre-commit Hooks

```javascript
// lint-staged.config.js
module.exports = {
  '*.{js,jsx,ts,tsx}': [
    'eslint --fix',
    'prettier --write',
    'vitest related --run',
  ],
  '*.{json,md,yml,yaml}': [
    'prettier --write',
  ],
  '*.css': [
    'stylelint --fix',
    'prettier --write',
  ],
};
```

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Test
        run: npm run test -- --run --coverage

      - name: Build
        run: npm run build
```

---

## Related Skills

- [[devops-cicd]] - CI/CD pipelines
- [[git-workflows]] - Git automation
- [[development-environment]] - Dev setup

