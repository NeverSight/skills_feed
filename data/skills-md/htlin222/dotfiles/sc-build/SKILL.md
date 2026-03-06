---
name: sc-build
description: Build, compile, and package projects with error handling and optimization. Use when user needs to build, compile, or package a project.
---

# Project Building

Build, compile, and package projects with comprehensive error handling and optimization.

## When to use

- User needs to build or compile a project
- Build errors need diagnosis and resolution
- Production build or optimization required
- Clean build or rebuild needed
- Build configuration analysis requested

## Instructions

### Usage

```
/sc:build [target] [--type dev|prod|test] [--clean] [--optimize]
```

### Arguments

- `target` - Project or specific component to build
- `--type` - Build type (dev, prod, test)
- `--clean` - Clean build artifacts before building
- `--optimize` - Enable build optimizations
- `--verbose` - Enable detailed build output

### Execution

1. Analyze project structure and build configuration
2. Validate dependencies and environment setup
3. Execute build process with error monitoring
4. Handle build errors and provide diagnostic information
5. Optimize build output and report results

### Claude Code Integration

- Uses Bash for build command execution
- Leverages Read for build configuration analysis
- Applies TodoWrite for build progress tracking
- Maintains comprehensive error handling and reporting
