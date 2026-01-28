---
name: gemini
description: Use Gemini AI for research, analysis, summarization, web search, and complex reasoning. Use when you need AI-powered research, code analysis, content summarization, or web search with synthesis.
---

# Gemini AI Assistant

Leverage Google's Gemini Pro model with its 1M context window for research, analysis, and reasoning tasks.

## Prerequisites

Install the Gemini CLI:
```bash
pip install google-generativeai
```

Set your API key:
```bash
export GEMINI_API_KEY=your_api_key
```

Get an API key at: https://makersuite.google.com/app/apikey

## CLI Reference

### Basic Usage
```bash
# Simple question
gemini -m pro "Your question here"

# With text output (no markdown)
gemini -m pro -o text "Your question"

# Disable extensions for programmatic use
gemini -m pro -o text -e "" "Your question"

# Pipe content as stdin
echo "content to analyze" | gemini -m pro -o text -e "" "Summarize this"
cat file.txt | gemini -m pro -o text -e "" "Analyze this code"
```

## Common Operations

### Research
Deep research with critical analysis:
```bash
gemini -m pro -o text -e "" "You are an expert research analyst. Research: [topic]. Provide specific facts, distinguish opinions from facts, note uncertainties, and give actionable insights."
```

### Summarization
```bash
cat document.txt | gemini -m pro -o text -e "" "Summarize this content, focusing on: [focus area]"
```

### Code Analysis
```bash
cat code.ts | gemini -m pro -o text -e "" "Analyze this code and answer: [question]"
```

### Web Search with Synthesis
```bash
gemini -m pro -o text -e "" "Search and synthesize: [query]. Include specific facts, dates, and distinguish confirmed from speculative information."
```

### Fact-Checking
```bash
gemini -m pro -o text -e "" "Fact-check this claim: [claim]. State true/false/partial, cite sources, note context."
```

### Step-by-Step Reasoning
```bash
gemini -m pro -o text -e "" "Think through this problem step by step: [problem]. Constraints: [constraints]. Provide reasoning and conclusion."
```

### Data Extraction
```bash
cat content.txt | gemini -m pro -o text -e "" "Extract [what to extract] from this content. Format as [json/list/table]."
```

### News Lookup
```bash
gemini -m pro -o text -e "" "Latest news about: [topic] from [timeframe]. Summarize important developments."
```

## Prompt Templates

### Research Prompt
```
You are an expert research analyst. Your goal is to provide genuinely useful, accurate research.

RESEARCH OBJECTIVE: [topic]

QUALITY STANDARDS:
- Be specific and concrete, not vague
- Distinguish between facts, expert opinions, and speculation
- Note when information is uncertain, contested, or evolving
- Identify what's NOT known or what gaps exist
- Provide actionable insights, not just information
```

### Analysis Prompt
```
Analyze the following and provide:
1. Key findings
2. Implications
3. Recommendations
4. Uncertainties or gaps

Content: [content]
```

## Best Practices

1. **Use `-o text -e ""`** for programmatic usage to get clean output
2. **Pipe large content** via stdin rather than command line args
3. **Be specific** in prompts - vague questions get vague answers
4. **Ask for structure** - request lists, tables, or JSON for parseable output
5. **Request citations** when accuracy matters
6. **Set timeouts** for long operations (gemini can take 30-120s)

## Error Handling

| Error | Solution |
|-------|----------|
| "command not found" | Install: `pip install google-generativeai` |
| "API key" / "unauthorized" | Set `GEMINI_API_KEY` environment variable |
| "rate limit" / "quota" | Wait and retry, or check quota at Google Cloud Console |
| Timeout | Break into smaller queries or increase timeout |
