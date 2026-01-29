---
name: claude-engineering-best-practices
description: General-purpose guidance for Claude Code (terminal) and Claude Dev (platform). Covers stable principles (progressive disclosure, hooks, security) and volatile details with lookup workflows.
---

# Claude Engineering Best Practices

## Quick Start

Use this Skill for:
- Claude Code configuration (plugins, hooks, sandboxing, settings)
- Claude Dev Agent SDK (tools, sessions, subagents, MCP)
- Plugin development and agent architecture
- Security patterns and best practices

**Lookup workflow** (verify volatile details):
```bash
# 1. Search for topic
rg -n "pattern" references/claude-*/**/*.md

# 2. Find official URL
rg -n "pattern" references/sources/llms_claude_*.txt

# 3. Fetch official doc
curl -sL "https://code.claude.com/docs/en/topic.md" | rg -A 5 "fieldName"
```

## Core Principles (Stable Patterns)

### 1. Progressive Disclosure
Information revealed in stages based on need:

| Level | What | Token Cost | When Loaded |
|-------|------|-----------|------------|
| **Metadata** | name + description | ~100 tokens | Always (startup) |
| **Instructions** | SKILL.md body | <5k tokens | On trigger |
| **Resources** | Bundled files | Unlimited | As needed (via bash) |

### 2. Hook-Based Architecture
Universal event system across Claude Code and SDK:

- **PreToolUse**: Validate/modify before execution
- **PostToolUse**: Log/validate after execution
- **SessionStart**: Initialize context
- **Stop**: Control completion criteria

### 3. Security-First Design
Multiple defensive layers:
- **Principle of least privilege**: Minimal permissions
- **Defense in depth**: Sandbox + IAM + hooks
- **Zero trust**: Verify at every layer

## Navigation Guide

### By Topic

**Plugin Architecture**
```bash
rg -n "plugin" references/claude-code/plugins.md
# Structure, manifest, caching, components
```

**Hooks & Events**
```bash
rg -n "PreToolUse\|PostToolUse" references/claude-code/hooks.md
# All events, types, schemas, patterns
```

**Sandboxing**
```bash
rg -n "sandbox\|network\|filesystem" references/claude-code/sandboxing.md
# Security, isolation, configuration
```

**Agent SDK**
```bash
rg -n "sessions\|hooks\|subagents" references/claude-dev/agent-sdk.md
# Sessions, hooks, tools, permissions
```

**Skills Authoring**
```bash
rg -n "progressive\|SKILL\.md" references/claude-dev/skills.md
# 3-tier architecture, best practices
```

### By Product

**Claude Code (Terminal)**
- `references/claude-code/plugins.md` - Plugin architecture
- `references/claude-code/hooks.md` - Hook system
- `references/claude-code/sandboxing.md` - Security isolation
- `references/claude-code/settings-permissions.md` - Configuration
- `references/claude-code/mcp-lsp.md` - MCP & LSP integration
- `references/claude-code/workflows.md` - Common workflows

**Claude Dev (Platform)**
- `references/claude-dev/agent-sdk.md` - SDK patterns
- `references/claude-dev/skills.md` - Skills architecture
- `references/claude-dev/tool-use.md` - Tool use patterns
- `references/claude-dev/prompt-engineering.md` - Prompting best practices
- `references/claude-dev/security-evaluation.md` - Security & testing

## Common Workflows

### Author Workflow (Design → Implement)
1. Identify capability needed (skill, agent, hook, plugin)
2. Check latest docs for current schema/patterns
3. Design with progressive disclosure (3-tier)
4. Implement with stable patterns
5. Test with verification hooks

### Operator Workflow (Use → Execute)
1. Determine tool/agent needed
2. Verify permissions & sandbox settings
3. Execute with appropriate oversight
4. Validate results via hooks/logs

### Reviewer/Auditor Workflow (Evaluate → Score)
1. Check objective completion (artifact/verdict)
2. Verify security compliance (permissions, sandbox, hooks)
3. Assess engineering quality (reproducibility, clarity)
4. Review documentation & patterns used

## Stable vs Volatile Information

### ✅ Stable Principles (Always Accurate)
- Progressive disclosure architecture
- Hook-based event system
- Plugin component structure
- Security design patterns
- Three-tier skill architecture

### ⚠️ Volatile Details (Look Up First)
These change frequently - **never hardcode**:
- API field names (exact JSON keys)
- Command flags (--debug, --resume, etc.)
- Hook event schemas (input/output structures)
- Plugin.json fields (required/optional)
- Tool permission lists
- Network domain allowlists

**Always verify volatile details**:
```bash
# Find correct URL
rg -n "topic.*\.md" references/sources/llms_claude_code.txt

# Fetch and extract
curl -sL "https://code.claude.com/docs/en/topic.md" | rg -A 5 "fieldName"
```

## Quick Reference

### Most Common Lookups

```bash
# Plugin.json required fields
curl -sL "https://code.claude.com/docs/en/plugins-reference.md" | rg -A 10 "Required fields"

# Hook events
curl -sL "https://code.claude.com/docs/en/hooks.md" | rg "^### "

# Agent SDK hooks
curl -sL "https://platform.claude.com/docs/en/agent-sdk/hooks.md" | rg -A 5 "PreToolUse"

# Sandbox configuration
curl -sL "https://code.claude.com/docs/en/sandboxing.md" | rg -A 10 "filesystem\|network"

# Structured outputs
curl -sL "https://platform.claude.com/docs/en/build-with-claude/structured-outputs" | rg -A 5 "json_schema"
```

### Decision Matrix

| Situation | Action |
|-----------|--------|
| curl succeeds, domain allowed | Use fetched data, cite source |
| curl succeeds, domain blocked | Document limitation, use local refs |
| curl fails (network error) | Use local refs, mark outdated |
| curl fails (403/permission) | Request permission, use local refs |
| Can't fetch docs | Use local reference files |

## Examples

### Example 1: Test Framework Architecture
```typescript
// Three-Agent Pattern
class TestRunner {
  // Agent A: Executor with hooks and sandbox
  async execute(task: string): Promise<void> {
    const options = {
      allowedTools: ['Read', 'Write', 'Edit', 'Bash'],
      permissionMode: 'acceptEdits',
      sandbox: { enabled: true },
      hooks: getHooks()  // PreToolUse, PostToolUse logging
    };
  }

  // Agent B: Simulator - generates tasks
  // Agent C: Evaluator - multi-step structured evaluation
}
```

### Example 2: Plugin Audit Checklist
```bash
# 1. Check structure
rg -n "\.claude-plugin\|plugin\.json" references/claude-code/plugins.md

# 2. Verify hooks pattern
rg -n "PreToolUse\|PostToolUse" references/claude-code/hooks.md

# 3. Check security settings
rg -n "sandbox\|permission" references/claude-code/sandboxing.md

# 4. Verify progressive disclosure
rg -n "3-tier\|progressive" references/claude-dev/skills.md
```

### Example 3: Agent SDK Configuration
```python
# Complete SDK pattern
options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep"],
    permission_mode="acceptEdits",
    session_persistence=True,
    hooks={
        "PreToolUse": [HookMatcher(...)],
        "PostToolUse": [HookMatcher(...)]
    },
    agents={
        "specialist": AgentDefinition(...)
    },
    setting_sources=["project"]
)
```

## Anti-Patterns (Avoid)

❌ **Hardcoding volatile details**
❌ **Missing progressive disclosure**
❌ **No validation hooks**
❌ **Hardcoded paths** (use env vars)
❌ **Overly verbose descriptions**
❌ **Deeply nested references** (keep one level deep)

## Official Documentation

### Master Indexes
- **Claude Code**: https://code.claude.com/docs/llms.txt
- **Claude Dev**: https://platform.claude.com/docs/llms.txt

### Key References
- **Agent SDK Overview**: https://platform.claude.com/docs/en/agent-sdk/overview.md
- **Agent Skills**: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md
- **Tool Use**: https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview.md
- **Hooks Reference**: https://code.claude.com/docs/en/hooks.md
- **Sandboxing**: https://code.claude.com/docs/en/sandboxing.md
- **Plugins**: https://code.claude.com/docs/en/plugins-reference.md

## Verification & Maintenance

**Last verified**: 2026-01-13

**Always verify volatile details** before implementation using the lookup workflow documented above.

**Monthly checks**:
- Review official documentation for updates
- Check for deprecated features
- Update local references if needed

---

**About this Skill**: This Skill applies progressive disclosure - only load what you need. Start with SKILL.md, reference thematic files for details, use lookup workflow for volatile information.
