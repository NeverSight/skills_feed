---
name: refactor
description: |
  Meta-cognitive architecture optimization skill. Use when the user asks to
  "refactor the architecture", "optimize claude code", "evaluate components",
  or "run architecture audit". Also triggers automatically every 24 hours.
allowed-tools: Task, Read, Write, Edit, Grep, Glob, Bash, WebFetch, WebSearch, TodoWrite
model: opus
context: fork
agent: refactor-agent
user-invocable: true
---

# Refactor Skill

## Trigger Patterns

- "/refactor"
- "refactor the architecture"
- "optimize my claude code setup"
- "evaluate all components"
- "run architecture audit"
- "check for redundancies"
- "optimize token usage"

## Applicable Specialized Agents

- refactor-agent (primary orchestrator)
- component-architect-agent (validation)
- knowledge-domain-agent (learning integration)

## Infrastructure Dependencies

| Tool | Purpose | Health Check |
|------|---------|--------------|
| bv/bd | Graph orchestration | `bd --version` |
| tweakcc | System prompt editing | `ls ~/.tweakcc/` |
| claude-mem | Context optimization | `curl localhost:37777/health` |
| hookify | Validation hooks | `hookify --version` |

## Optimization Frameworks

1. **Homoiconic Renormalization** - Self-referential optimization
2. **BFO/GFO Ontology** - Formal type definitions
3. **Hegelian Dialectics** - Thesis-antithesis-synthesis
4. **Pareto Optimization** - Multi-objective efficiency

## 24-Hour Auto-Trigger

```xml
<!-- ~/.claude/launchd/com.claude.refactor.plist -->
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.refactor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>claude -p "/refactor --auto"</string>
    </array>
    <key>StartInterval</key>
    <integer>86400</integer>
</dict>
</plist>
```
