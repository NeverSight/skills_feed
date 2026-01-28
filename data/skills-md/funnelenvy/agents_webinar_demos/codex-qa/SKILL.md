---
name: codex-qa
description: Use OpenAI Codex CLI to answer questions about code, analyze files, or perform read-only codebase exploration. Invoke this skill when the user asks to use Codex, wants a second opinion from another AI agent, or wants to compare Claude's answer with Codex's response.
---

# Codex Q&A

Use OpenAI's Codex CLI to answer questions about the codebase.

## Prerequisites

Codex CLI must be installed and configured:
```bash
npm install -g @openai/codex
# or
brew install --cask codex
```

An OpenAI API key must be configured (OPENAI_API_KEY environment variable or via `codex` initial setup).

## Usage

Spawn the `codex-qa` subagent to handle the question:

```
Use the Task tool to spawn the codex-qa agent with the user's question.
```

The subagent will:
1. Formulate a clear prompt for Codex
2. Run `codex exec "question"` in read-only mode
3. Return Codex's response

## Direct Usage (without subagent)

If you prefer to run Codex directly:

```bash
codex exec "your question here"
```

### Command Options

- **Basic query**: `codex exec "question"`
- **With image**: `codex -i image.png exec "question about image"`
- **JSON output**: `codex exec --json "question"`
- **Longer timeout**: `codex exec --timeout 300000 "complex question"`

## Common Use Cases

- **Code explanation**: "What does this function do?"
- **Architecture questions**: "How is the database layer structured?"
- **Finding patterns**: "Where is error handling implemented?"
- **Code review**: "Review this file for potential issues"
- **Comparison**: Get a second opinion on a code question

## Notes

- Codex exec runs in **read-only mode** by default - it cannot modify files
- Activity streams to stderr, final answer goes to stdout
- For complex questions, use the subagent for better context isolation
