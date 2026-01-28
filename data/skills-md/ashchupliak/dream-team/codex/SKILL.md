---
name: codex
description: Delegate coding tasks to Codex CLI (OpenAI gpt-5-codex via JetBrains AI). Use when a task involves repetitive code generation, refactoring, or analysis that can be offloaded.
---

# Codex Skill - JetBrains AI Integration

Use Codex CLI to delegate coding tasks that benefit from parallel AI processing.

## When to Use Codex

**GOOD for Codex:**
- Large-scale refactoring across many files
- Repetitive code generation (boilerplate, tests)
- Code analysis and documentation
- Pattern-based transformations
- Exploring unfamiliar codebases

**KEEP in Claude:**
- Complex architectural decisions
- Security-sensitive code
- Tasks requiring deep context understanding
- Interactive problem-solving with user

## Configuration

Codex is pre-configured with JetBrains AI staging:
- Provider: `jbai-staging`
- Models: `gpt-4o-2024-11-20`, `o1-2024-12-17`, `o3-mini-2025-01-31`

## Usage Patterns

### Quick Analysis (read-only)
```bash
codex exec -c model_provider=jbai-staging --model "gpt-4o-2024-11-20" \
  --sandbox read-only \
  "Analyze the codebase and list all REST endpoints" 2>/dev/null
```

### Code Generation (workspace-write)
```bash
codex exec -c model_provider=jbai-staging --model "gpt-4o-2024-11-20" \
  --sandbox workspace-write --full-auto \
  "Generate unit tests for UserService.kt" 2>/dev/null
```

### Heavy Reasoning (o1/o3 models)
```bash
codex exec -c model_provider=jbai-staging --model "o3-mini-2025-01-31" \
  --sandbox read-only \
  "Review security vulnerabilities in auth module" 2>/dev/null
```

### Resume Previous Session
```bash
echo "continue with the refactoring" | codex exec --skip-git-repo-check resume --last 2>/dev/null
```

## Decision Framework

Before delegating to Codex, consider:

| Factor | Use Codex | Keep in Claude |
|--------|-----------|----------------|
| File count | Many files | Few files |
| Task type | Repetitive/mechanical | Creative/strategic |
| Context needed | Self-contained | Requires conversation context |
| User interaction | None needed | Back-and-forth required |

## Execution Protocol

1. **Announce intent**: Tell user you're delegating to Codex and why
2. **Choose model**:
   - `gpt-4o-2024-11-20` for fast tasks
   - `o1-2024-12-17` / `o3-mini-2025-01-31` for complex reasoning
3. **Choose sandbox**:
   - `read-only` for analysis
   - `workspace-write` for edits
4. **Run command** with `2>/dev/null` to suppress thinking tokens
5. **Report results** back to user
6. **Offer resume**: "Say 'codex resume' to continue this session"

## Safety Rules

- Always use `--skip-git-repo-check` flag
- Default to `read-only` sandbox unless edits needed
- Never use `danger-full-access` without explicit user permission
- Suppress stderr with `2>/dev/null` by default
