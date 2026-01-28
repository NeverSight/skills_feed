---
name: gemini-frontend-assistant
description: A specialized skill for frontend development tasks using the Gemini CLI. It leverages Gemini's multimodal capabilities for generating UI code (React, Tailwind CSS) from descriptions or images (screenshots).
category: frontend
version: 1.1.0
---

# Gemini Frontend Assistant Skill

## Purpose

This skill integrates the Gemini CLI into your workflow to handle frontend development tasks. It is specifically optimized for generating React components, styling with Tailwind CSS, and converting visual references (screenshots) into code.

## When to Use This Skill

Use this skill when:
- You need to generate React components based on a text description.
- You want to convert a UI screenshot into code (using Gemini's vision capabilities).
- You need help with complex Tailwind CSS styling.
- You want to refactor or optimize existing frontend code.

## Core Capabilities

### 1. UI Code Generation

**Prompt:** "Create a [Component Name] that looks like [Description]"

**Action:**
The agent uses the `gemini-generate.sh` script to generate the code safely.

### 2. Vision-to-Code (Screenshot to UI)

**Prompt:** "Turn this screenshot [Path to Image] into a React component."

**Action:**
The agent uses the `gemini-generate.sh` script with the image path.

### 3. Code Refactoring & Optimization

**Prompt:** "Refactor this component [Path to File] to use [Pattern/Library]"

**Action:**
The agent uses the `gemini-refactor.sh` script to safely read file content and request refactoring.

## Usage Instructions

### Setup

Ensure you have the Gemini CLI installed and your API key configured.

```bash
# Check installation
gemini --version
```

### 1. UI Code Generation (New Component)

Use the `gemini-generate.sh` script to create new components. It automatically includes your project's coding standards.

```bash
# Usage: ./scripts/gemini-generate.sh "<description>"
.claude/skills/gemini-frontend-assistant/scripts/gemini-generate.sh "A responsive navigation bar with a logo, links, and a dark mode toggle."
```

### 2. Vision-to-Code (Screenshot to Component)

Pass an image path to the generation script to convert a screenshot into code.

```bash
# Usage: ./scripts/gemini-generate.sh "<description>" [image_path]
.claude/skills/gemini-frontend-assistant/scripts/gemini-generate.sh "Replicate this dashboard design pixel-perfectly." "ref-screenshots/dashboard.png"
```

### 3. Code Refactoring & Optimization

Use the `gemini-refactor.sh` script to improve existing files safely.

```bash
# Usage: ./scripts/gemini-refactor.sh <file_path> "<instructions>"
.claude/skills/gemini-frontend-assistant/scripts/gemini-refactor.sh "src/components/MyComponent.tsx" "Refactor to use the new glass-bar utility class and fix accessibility issues."
```

## Best Practices for Frontend Tasks

1.  **Be Specific:** When describing UI, mention colors (e.g., "zinc-900"), layout (e.g., "flex-row"), and interactivity.
2.  **Iterative Refinement:** Generate a base component first, then ask for specific changes (e.g., "Make the buttons rounded").
3.  **Context Awareness:** If you have a design system (like in `src/css/custom.css`), mention it in your prompt so Gemini generates compatible code.

## Integration with Other Skills

- **chatbot-widget-creator:** Use Gemini to generate specific sub-components for your chatbot.
- **book-content-writer:** Use Gemini to generate code snippets for your documentation.

**Note:** If you get api key error ask the user to give api key, or ask for skip.