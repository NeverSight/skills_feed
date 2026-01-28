---
name: research
description: Comprehensive research combining web search and AI synthesis. Use for deep research on topics, comparing technologies, investigating libraries, and finding GitHub issues related to problems.
---

# Research - Deep Investigation

Thorough research combining multiple sources and AI synthesis.

## Prerequisites

- `gh` CLI for GitHub searches
- `gemini` CLI for AI synthesis

```bash
brew install gh
pip install google-generativeai
gh auth login
export GEMINI_API_KEY=your_api_key
```

## Research Operations

### Deep Research
Comprehensive multi-angle investigation:

```bash
# Step 1: Gather information from multiple angles
TOPIC="your research topic"
OBJECTIVE="what you're trying to learn"

# Web search synthesis
gemini -m pro -o text -e "" "Research '$TOPIC' comprehensively.

OBJECTIVE: $OBJECTIVE

Provide:
1. Executive summary (3-5 bullet points)
2. Key findings with sources
3. Different perspectives and debates
4. Knowledge gaps and uncertainties
5. Actionable recommendations"
```

### Quick Research
Fast answers for straightforward questions:

```bash
gemini -m pro -o text -e "" "Quick research: [question]

Provide:
- Direct answer
- Key facts
- Important caveats
- Actionable next step"
```

### Technology Comparison
```bash
gemini -m pro -o text -e "" "Compare these technologies for [use case]:

CANDIDATES:
1. [Tech A]
2. [Tech B]
3. [Tech C]

CRITERIA:
- Performance
- Learning curve
- Community/ecosystem
- Maintenance burden
- Production readiness

Include real-world adoption examples and common pitfalls."
```

### Library Investigation
```bash
# GitHub search for the library
gh search repos "[library name]" --json fullName,description,stargazersCount,updatedAt --limit 5

# Check issues
gh search issues "[library] bug" --json title,url,state --limit 10

# AI analysis
gemini -m pro -o text -e "" "Evaluate [library] for production use:

1. Maturity and stability
2. Maintenance status
3. Common issues
4. Alternatives to consider
5. Recommendation"
```

### GitHub Issues Search
Find related issues for debugging:

```bash
# Search GitHub issues
gh search issues "[error message]" --json repository,title,url,state --limit 20

# Search in specific repo
gh search issues "[error]" --repo owner/repo --json title,url,state

# Search with labels
gh search issues "[topic]" --label "bug" --state open
```

## Research Patterns

### Before Adopting a Library
```bash
#!/bin/bash
LIB="$1"

echo "=== GitHub Presence ==="
gh search repos "$LIB" --json fullName,stargazersCount,updatedAt --limit 3

echo ""
echo "=== Open Issues ==="
gh search issues "$LIB bug" --state open --json title,url --limit 5

echo ""
echo "=== AI Evaluation ==="
gemini -m pro -o text -e "" "Should I use $LIB in production? Consider maintenance, alternatives, and common issues."
```

### Debugging with External Search
```bash
ERROR="your error message"

# Search for similar issues
gh search issues "$ERROR" --json repository,title,url,state --limit 10

# Search discussions
gh search issues "$ERROR" type:discussion --limit 5

# AI analysis of error
gemini -m pro -o text -e "" "Explain this error and likely causes: $ERROR"
```

### Architectural Research
```bash
gemini -m pro -o text -e "" "Research best practices for: [architecture topic]

Specifically:
1. What do industry leaders (FAANG, etc.) do?
2. What are the tradeoffs?
3. Common mistakes to avoid
4. When to use vs. when to avoid
5. Concrete implementation guidance"
```

### Staying Current
```bash
# Recent news on a topic
gemini -m pro -o text -e "" "What are the latest developments in [technology] as of 2024? Include version updates, new features, and ecosystem changes."

# Recent GitHub activity
gh search repos "[technology]" --created ">2024-01-01" --sort stars --json fullName,description,stargazersCount --limit 10
```

## Output Synthesis

### Standard Research Output
```
## Executive Summary
- Key point 1
- Key point 2
- Key point 3

## Detailed Findings
### Finding 1
[Details and evidence]

### Finding 2
[Details and evidence]

## Critical Analysis
- What's contested or uncertain
- What biases might exist
- What's missing

## Recommendations
1. Immediate action
2. Further investigation needed
3. Decisions to make
```

### Comparison Output
```
## Quick Verdict
[1-2 sentence recommendation]

## Detailed Comparison
| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| Performance | ... | ... | ... |
| Ease of use | ... | ... | ... |

## Recommendation
[Detailed reasoning]
```

## Best Practices

1. **State objective clearly** - What decision are you trying to make?
2. **Use multiple sources** - GitHub + web + AI synthesis
3. **Check recency** - Technology changes quickly
4. **Verify claims** - AI can hallucinate; cross-reference
5. **Save valuable research** - Store in memory for future reference
6. **Follow up gaps** - Research what's uncertain
