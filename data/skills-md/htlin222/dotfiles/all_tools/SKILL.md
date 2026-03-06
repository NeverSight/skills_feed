---
name: all_tools
description: List All Tools. Use when user wants to see available tools or needs a tool reference.
---

# List All Tools

List all available tools detailed in your system prompt.

## When to use

- When user asks what tools are available
- When user needs to understand tool capabilities
- When exploring what functions Claude Code can perform

## Instructions

Display all tools in bullet points using TypeScript function signature format. Suffix each with the purpose of the tool. Use double line breaks between each tool for readability.

Example format:

```typescript
- functionName(param1: type, param2: type): returnType
  // Purpose of this tool

- anotherFunction(param: type): returnType
  // What this tool does
```
