---
name: council
description: Query multiple AI agents in parallel for diverse perspectives. Use when you want multiple viewpoints on a question, to compare approaches, or to find consensus among AI models.
---

# AI Council - Multi-Agent Consultation

Get perspectives from multiple AI agents on the same question.

## Prerequisites

At least one of these CLIs installed:

### Claude CLI
```bash
npm install -g @anthropic-ai/claude-cli
# Set ANTHROPIC_API_KEY
```

### Codex CLI
```bash
npm install -g @openai/codex-cli
# Set OPENAI_API_KEY
```

### Gemini CLI
```bash
pip install google-generativeai
# Set GEMINI_API_KEY
```

## Individual Agent Commands

### Claude
```bash
# Ask Claude
claude -p --model opus "Your question here"

# Print mode (non-interactive)
claude --print "Your question"
```

### Codex
```bash
# Ask Codex
codex -q "Your question here"
```

### Gemini
```bash
# Ask Gemini
gemini -m pro -o text -e "" "Your question here"
```

## Parallel Consultation Pattern

### Basic Multi-Agent Query
```bash
# Query all agents in parallel
(
  echo "=== Claude ===" && claude --print "Your question" &
  echo "=== Gemini ===" && gemini -m pro -o text -e "" "Your question" &
  echo "=== Codex ===" && codex -q "Your question" &
  wait
)
```

### Structured Comparison Script
```bash
#!/bin/bash
QUESTION="$1"

# Query in parallel, save to temp files
claude --print "$QUESTION" > /tmp/claude-response.txt &
gemini -m pro -o text -e "" "$QUESTION" > /tmp/gemini-response.txt &
wait

echo "=== Claude's Response ==="
cat /tmp/claude-response.txt

echo ""
echo "=== Gemini's Response ==="
cat /tmp/gemini-response.txt

# Cleanup
rm -f /tmp/claude-response.txt /tmp/gemini-response.txt
```

## Use Cases

### Code Review Perspectives
```bash
# Get different review perspectives
CODE=$(cat mycode.ts)

claude --print "Review this code for best practices: $CODE"
gemini -m pro -o text -e "" "Review this code for security issues: $CODE"
```

### Architecture Decision
```bash
QUESTION="Should I use microservices or monolith for a startup MVP with 3 developers?"

# Get multiple perspectives
claude --print "$QUESTION"
gemini -m pro -o text -e "" "$QUESTION"
```

### Debugging Approaches
```bash
ERROR="TypeError: Cannot read property 'map' of undefined"
CONTEXT="React component fetching API data"

claude --print "Debug this error: $ERROR. Context: $CONTEXT"
gemini -m pro -o text -e "" "Explain and fix: $ERROR in $CONTEXT"
```

### Finding Consensus
After getting responses from multiple agents, ask one to synthesize:

```bash
# Save individual responses first, then:
gemini -m pro -o text -e "" "Here are responses from different AI agents about [topic]:

Response 1: [Claude's response]
Response 2: [Gemini's response]

Synthesize these into a consensus view, noting:
1. Where they agree
2. Where they differ
3. The most actionable recommendation"
```

## Role Presets

When querying, you can assign roles:

### Software Engineering Council
```bash
claude --print "As a software architect: [question]"
gemini -m pro -o text -e "" "As a security engineer: [question]"
```

### Code Review Council
```bash
claude --print "Review for maintainability: [code]"
gemini -m pro -o text -e "" "Review for performance: [code]"
```

### Creative Problem Solving
```bash
claude --print "Suggest conventional solutions for: [problem]"
gemini -m pro -o text -e "" "Suggest unconventional approaches for: [problem]"
```

## Debate Pattern

Have agents respond to each other:

```bash
# Round 1: Initial positions
R1_CLAUDE=$(claude --print "Argue FOR using TypeScript in a new project")
R1_GEMINI=$(gemini -m pro -o text -e "" "Argue AGAINST using TypeScript in a new project")

# Round 2: Rebuttals
R2_CLAUDE=$(claude --print "Respond to this argument against TypeScript: $R1_GEMINI")
R2_GEMINI=$(gemini -m pro -o text -e "" "Respond to this argument for TypeScript: $R1_CLAUDE")

# Synthesis
gemini -m pro -o text -e "" "Synthesize this debate:

FOR TypeScript: $R1_CLAUDE
Rebuttal: $R2_CLAUDE

AGAINST TypeScript: $R1_GEMINI
Rebuttal: $R2_GEMINI

Provide a balanced recommendation."
```

## Best Practices

1. **Use same question** - Consistent phrasing for fair comparison
2. **Run in parallel** - Background jobs with `&` for speed
3. **Capture output** - Save to files for comparison
4. **Note which agent** - Label responses clearly
5. **Synthesize at end** - Use one agent to summarize
6. **Match agent to task** - Claude for nuance, Gemini for facts, Codex for code
