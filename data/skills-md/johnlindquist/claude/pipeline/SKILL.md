---
name: pipeline
description: Chain multiple operations together in pipelines. Use for multi-step workflows, combining research with analysis, and complex automated tasks.
---

# Pipeline Orchestration

Chain multiple tools and operations together.

## Basic Pipelines

### Research → Summarize

```bash
# Research a topic then summarize
RESEARCH=$(gemini -m pro -o text -e "" "Research: [topic]. Be comprehensive.")
SUMMARY=$(echo "$RESEARCH" | gemini -m pro -o text -e "" "Summarize this research in 5 bullet points")
echo "$SUMMARY"
```

### Code → Review → Fix

```bash
# Read code, get review, apply fixes
CODE=$(cat src/module.ts)
REVIEW=$(echo "$CODE" | gemini -m pro -o text -e "" "Review this code for issues")
FIXES=$(echo "$CODE\n\nReview:\n$REVIEW" | gemini -m pro -o text -e "" "Provide fixed code")
```

### Multi-Agent Pipeline

```bash
# Get perspectives from multiple agents
QUESTION="Best approach for state management in React?"

CLAUDE=$(claude --print "$QUESTION" 2>/dev/null)
GEMINI=$(gemini -m pro -o text -e "" "$QUESTION")

SYNTHESIS=$(gemini -m pro -o text -e "" "Synthesize these perspectives:

Claude: $CLAUDE

Gemini: $GEMINI

Provide a unified recommendation.")
```

## Pipeline Patterns

### Transform Chain

```bash
#!/bin/bash
# transform.sh - Chain of transformations

INPUT=$1

# Step 1: Extract
EXTRACTED=$(echo "$INPUT" | gemini -m pro -o text -e "" "Extract key points")

# Step 2: Structure
STRUCTURED=$(echo "$EXTRACTED" | gemini -m pro -o text -e "" "Organize as JSON")

# Step 3: Validate
VALIDATED=$(echo "$STRUCTURED" | gemini -m pro -o text -e "" "Validate and fix any JSON issues")

echo "$VALIDATED"
```

### Conditional Pipeline

```bash
#!/bin/bash
# conditional.sh - Branch based on analysis

INPUT=$1

# Analyze type
TYPE=$(echo "$INPUT" | gemini -m pro -o text -e "" "Is this a bug report, feature request, or question? Answer with one word.")

case $TYPE in
  bug*)
    gemini -m pro -o text -e "" "Analyze this bug report and suggest debugging steps: $INPUT"
    ;;
  feature*)
    gemini -m pro -o text -e "" "Break down this feature request into tasks: $INPUT"
    ;;
  question*)
    gemini -m pro -o text -e "" "Answer this question: $INPUT"
    ;;
esac
```

### Parallel Pipeline

```bash
#!/bin/bash
# parallel.sh - Run analysis in parallel

INPUT=$1

# Run in parallel
echo "$INPUT" | gemini -m pro -o text -e "" "Technical analysis" > /tmp/technical.txt &
echo "$INPUT" | gemini -m pro -o text -e "" "Business analysis" > /tmp/business.txt &
echo "$INPUT" | gemini -m pro -o text -e "" "Risk analysis" > /tmp/risk.txt &
wait

# Combine results
gemini -m pro -o text -e "" "Combine these analyses:

Technical:
$(cat /tmp/technical.txt)

Business:
$(cat /tmp/business.txt)

Risk:
$(cat /tmp/risk.txt)

Provide integrated recommendation."
```

## Common Pipelines

### Code Review Pipeline

```bash
#!/bin/bash
# code-review.sh FILE

FILE=$1
CODE=$(cat "$FILE")

# Step 1: Static analysis
echo "=== Linting ===" > /tmp/review.txt
npx eslint "$FILE" 2>&1 >> /tmp/review.txt

# Step 2: Type check
echo "" >> /tmp/review.txt
echo "=== Type Check ===" >> /tmp/review.txt
npx tsc --noEmit "$FILE" 2>&1 >> /tmp/review.txt

# Step 3: AI review
echo "" >> /tmp/review.txt
echo "=== AI Review ===" >> /tmp/review.txt
gemini -m pro -o text -e "" "Review this code:

$CODE

Check for:
- Bugs
- Security issues
- Performance problems
- Best practices violations" >> /tmp/review.txt

cat /tmp/review.txt
```

### Documentation Pipeline

```bash
#!/bin/bash
# document.sh FILE

FILE=$1
CODE=$(cat "$FILE")

# Generate docs
DOCS=$(gemini -m pro -o text -e "" "Generate documentation for:

$CODE

Include:
- Overview
- Function descriptions
- Parameter docs
- Examples")

# Generate README section
README=$(echo "$DOCS" | gemini -m pro -o text -e "" "Convert to README.md format")

# Generate inline comments
COMMENTED=$(gemini -m pro -o text -e "" "Add JSDoc comments to:

$CODE")

echo "=== Documentation ==="
echo "$DOCS"
echo ""
echo "=== Commented Code ==="
echo "$COMMENTED"
```

### Research Pipeline

```bash
#!/bin/bash
# research.sh TOPIC

TOPIC=$1

# Step 1: Initial research
echo "Researching: $TOPIC"
INITIAL=$(gemini -m pro -o text -e "" "Research: $TOPIC. Focus on practical aspects.")

# Step 2: Find gaps
GAPS=$(echo "$INITIAL" | gemini -m pro -o text -e "" "What questions remain unanswered?")

# Step 3: Fill gaps
FOLLOWUP=$(echo "$GAPS" | gemini -m pro -o text -e "" "Answer these remaining questions about $TOPIC")

# Step 4: Synthesize
gemini -m pro -o text -e "" "Create comprehensive summary:

Initial Research:
$INITIAL

Follow-up:
$FOLLOWUP

Provide:
1. Key findings
2. Recommendations
3. Next steps"
```

## Error Handling

### With Retry

```bash
#!/bin/bash
# retry-pipeline.sh

retry() {
  local n=1
  local max=3
  local delay=2
  while true; do
    "$@" && return 0
    if [[ $n -lt $max ]]; then
      ((n++))
      echo "Retry $n/$max in ${delay}s..."
      sleep $delay
    else
      return 1
    fi
  done
}

# Use in pipeline
retry gemini -m pro -o text -e "" "Your prompt"
```

### With Fallback

```bash
#!/bin/bash
# fallback-pipeline.sh

# Try Claude, fallback to Gemini
result=$(claude --print "Question" 2>/dev/null) || \
result=$(gemini -m pro -o text -e "" "Question")

echo "$result"
```

## Best Practices

1. **Save intermediate results** - Debug easier
2. **Add timeouts** - Prevent hanging
3. **Handle errors** - Check return codes
4. **Log progress** - Track long pipelines
5. **Test incrementally** - Verify each step
6. **Use temp files** - For complex data
7. **Clean up** - Remove temp files after
