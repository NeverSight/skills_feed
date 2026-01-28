---
name: gemini-qa
description: Use Google Gemini CLI to answer questions about code, analyze files, or perform codebase exploration. Invoke this skill when the user asks to use Gemini, wants a second opinion from another AI, or wants to compare Claude's answer with Gemini's response.
---

# Gemini Q&A

Use Google's Gemini CLI to answer questions about the codebase.

## Prerequisites

Gemini CLI must be installed:
```bash
npm install -g @anthropic-ai/gemini-cli
# or follow installation at https://github.com/google-gemini/gemini-cli
```

Authentication must be configured (Google API key or Application Default Credentials).

## Usage

Spawn the `gemini-qa` subagent to handle the question:

```
Use the Task tool to spawn the gemini-qa agent with the user's question.
```

The subagent will:
1. Formulate a clear prompt for Gemini
2. Run `gemini -p "question"` in headless mode
3. Return Gemini's response

## Direct Usage (without subagent)

If you prefer to run Gemini directly:

```bash
gemini -p "your question here"
# or
gemini "your question here"
```

### Command Options

- **Basic query**: `gemini -p "question"`
- **Positional**: `gemini "question"`
- **Pipe input**: `cat file.txt | gemini -p "summarize this"`
- **JSON output**: `gemini -p "question" --output-format json`
- **File reference**: `gemini -p "@src/file.ts explain this"`

### File References with @

Gemini supports `@` syntax to include file context:

```bash
# Reference a specific file
gemini -p "@src/auth.ts Explain this module"

# Reference a directory
gemini -p "@src/ Summarize all code here"
```

## Common Use Cases

- **Code explanation**: "What does this function do?"
- **Architecture questions**: "How is the database layer structured?"
- **Finding patterns**: "Where is error handling implemented?"
- **Code review**: "Review this file for potential issues"
- **Comparison**: Get a second opinion on a code question

## Notes

- Use `-p` flag for headless (non-interactive) mode
- Gemini is git-aware and respects `.gitignore` for directory references
- For complex questions, use the subagent for better context isolation
