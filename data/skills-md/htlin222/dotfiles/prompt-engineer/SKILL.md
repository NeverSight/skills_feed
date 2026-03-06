---
name: prompt-engineer
description: Optimize prompts for LLMs and AI systems. Use when building AI features, improving agent performance, or crafting system prompts.
---

# Prompt Engineering

Craft effective prompts for LLM applications.

## When to Use

- Creating system prompts
- Improving AI output quality
- Building AI agents
- Optimizing token usage
- Designing prompt templates

## Core Techniques

### Role Setting

```
You are an expert [role] with [X] years of experience in [domain].
Your task is to [specific goal].
```

### Chain of Thought

```
Think through this step by step:
1. First, analyze [aspect 1]
2. Then, consider [aspect 2]
3. Finally, determine [conclusion]

Show your reasoning before giving the final answer.
```

### Few-Shot Examples

```
Here are examples of the expected format:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now process this input:
Input: {user_input}
Output:
```

### Structured Output

```
Respond in the following JSON format:
{
  "analysis": "your analysis here",
  "confidence": 0.0-1.0,
  "recommendations": ["item1", "item2"]
}

Return valid JSON only, no additional text.
```

## Prompt Templates

### Code Review

```
You are a senior code reviewer. Review the code for:
1. Security vulnerabilities
2. Performance issues
3. Code quality and readability
4. Best practices violations

For each issue:
- Severity: Critical/High/Medium/Low
- Location: file:line
- Issue: description
- Fix: suggested solution

Code to review:
{code}
```

### Data Extraction

```
Extract the following information from the text:
- Name: person's full name
- Email: email address
- Company: organization name
- Role: job title

If information is not found, use "NOT_FOUND".
Return as JSON.

Text:
{text}
```

### Classification

```
Classify the following text into one of these categories:
- POSITIVE
- NEGATIVE
- NEUTRAL

Consider tone, sentiment, and overall message.
Respond with only the category name.

Text: {text}
Category:
```

## Best Practices

| Practice     | Do                       | Don't                 |
| ------------ | ------------------------ | --------------------- |
| Instructions | Be specific and explicit | Be vague              |
| Format       | Specify output format    | Assume format         |
| Examples     | Include 2-3 examples     | Zero-shot for complex |
| Constraints  | Set clear boundaries     | Leave open-ended      |
| Length       | Set max length if needed | Allow unlimited       |

## Testing Prompts

1. Test with edge cases
2. Try adversarial inputs
3. Check consistency across runs
4. Measure output quality
5. Track token usage

## Examples

**Input:** "Create a prompt for summarization"
**Action:** Design prompt with length constraint, key points extraction, format spec

**Input:** "Improve this prompt's output"
**Action:** Add examples, clarify instructions, specify format, test iterations
