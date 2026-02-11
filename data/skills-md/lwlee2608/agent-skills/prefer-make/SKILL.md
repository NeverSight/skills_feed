---
name: prefer-make
description: Use when building, testing, linting, or running Go code in projects that have a Makefile. Prefer make targets over calling go commands directly.
user-invocable: true
---

# Build with Make

This project uses a Makefile. **Always prefer `make` targets over running `go` commands directly.**

## Rules

1. Before running any `go build`, `go test`, `go run`, `go vet`, `go fmt`, or `golangci-lint` command, check the Makefile for a corresponding target.
2. Use the Makefile target instead of the raw `go` command. For example:
   - `make build` instead of `go build ./...`
   - `make test` instead of `go test ./...`
   - `make lint` instead of `golangci-lint run`
   - `make run` instead of `go run main.go`
   - `make fmt` instead of `go fmt ./...`
3. If you need to discover available targets, run `make help` first. If that fails, read the Makefile directly.
4. Only fall back to raw `go` commands if no relevant Makefile target exists for the task.
