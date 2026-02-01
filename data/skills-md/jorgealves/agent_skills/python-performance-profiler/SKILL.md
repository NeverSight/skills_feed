---
name: python-performance-profiler
description: Identify CPU and memory bottlenecks in Python code using cProfile or memory_profiler. Use to optimize mission-critical Python services.
---
# Python Performance Profiler

## Purpose and Intent
Identify CPU and memory bottlenecks in Python code using cProfile or memory_profiler. Use to optimize mission-critical Python services.

## When to Use
- **Project Setup**: When initializing a new Python project.
- **Continuous Integration**: As part of automated build and test pipelines.
- **Legacy Refactoring**: When updating older Python codebases to modern standards.

## When NOT to Use
- **Non-Python Projects**: This tool is specialized for the Python ecosystem.

## Error Conditions and Edge Cases
- **Missing Requirements**: If the project lacks a requirements.txt or pyproject.toml.
- **Incompatible Versions**: If the project uses a Python version not supported by the tools.

## Security and Data-Handling Considerations
- All analysis is performed locally.
- No source code or credentials are ever transmitted externally.
