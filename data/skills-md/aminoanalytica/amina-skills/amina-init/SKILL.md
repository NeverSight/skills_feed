---
name: amina-init
description: >
  Foundation skill for autonomous protein engineering via the Amina CLI.
  Use at session start or after conversation compacting when working with
  AminoAnalytica's Amina CLI or when you need help using the Amina CLI to do protein engineering tasks like:
  protein design, structure prediction, binder design, docking, molecular dynamics, enzyme engineering,
  or any mention of Amina/amina-cli.
---

# Amina CLI

Run autonomous protein engineering workflows via AminoAnalytica's Amina CLI.

**Documentation**: [CLI](https://app.aminoanalytica.com/docs/cli) | [Tools](https://app.aminoanalytica.com/docs/tools)

## Reference Loading

This skill uses progressive disclosure. Load references based on context:

### At Session Start

When starting a new Amina session or first protein engineering request:

1. Read `references/setup.md` — Run through session initialization
2. Read `references/usage.md` — Load execution guidance for the session

### Mid-Session Refresh

When you need a reminder on CLI usage, execution patterns, or agent behavior:

- Read `references/usage.md` only

### When to Load References

| Trigger | Action |
|---------|--------|
| Session start, first Amina request | Load both setup.md and usage.md |
| "How do I use amina...", CLI questions | Load usage.md |
| Job submission, workflow execution | Load usage.md if not already loaded |
| Environment issues, auth problems | Load setup.md |

## Quick Reference

```bash
# Essential commands
amina tools list                              # List all tools
amina run <tool> --help                       # Show parameters
amina run <tool> [params] -o <dir>            # Sync execution
amina run <tool> --background --job-name <n>  # Async execution
amina jobs wait <id> && amina jobs download <id> -o ./
```

**Key principle**: Run commands automatically, complete workflows end-to-end, never ask unnecessary questions.
