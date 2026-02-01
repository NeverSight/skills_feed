---
name: agents-md-generator
description: Automatically generate comprehensive AGENTS.md files that teach AI agents how to work with a repository's structure, conventions, and guidelines
allowed-tools: bash_tool,view,str_replace,create_file
---

# AGENTS.MD Generator

## Purpose
Generate AGENTS.md files that serve as onboarding documentation for AI coding agents. This file teaches agents about project structure, coding conventions, build processes, and development workflows.

## Prerequisites
- Access to the target repository
- Understanding of the project's technology stack
- Write permissions to create AGENTS.md at repository root

## Instructions

### Step 1: Analyze Repository Structure

Use bash and view tools to explore repository contents.

### Step 2: Identify Project Type

Determine if it's a full-stack app, API, mobile app, library, or CLI tool.

### Step 3: Generate AGENTS.md Structure

Create sections for Overview, Tech Stack, Project Structure, Development Setup, Coding Standards, Testing, and Deployment.

### Step 4: Customize by Project Type

Add type-specific guidance based on the project category.

### Step 5: Add Decision Trees

Include decision flows for common development scenarios.

### Step 6: Validate and Refine

Ensure completeness and clarity.

## Best Practices

1. Keep it current with architectural changes
2. Include actual examples from the codebase
3. Think from an AI agent's perspective
4. Explain the "why" not just "what"
