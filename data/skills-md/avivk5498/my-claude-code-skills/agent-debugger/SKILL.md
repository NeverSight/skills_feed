---
name: agent-debugger
description: Systematic debugging toolkit for AI agentic workflows in customer support. Use when diagnosing issues with AI agents including wrong responses, tool/function calling problems, conversation loops, stuck states, or performance/latency issues. Works with any framework (LangChain, custom agents, Claude API) and accepts conversation logs, API logs, tool execution logs, and agent configurations.
---

# Agent Debugger

## Overview

Debug AI agent issues systematically using analysis scripts and proven debugging patterns. This skill helps identify root causes of common agent failures: incorrect responses, tool calling errors, conversation loops, performance problems, and more.

## When to Use This Skill

Trigger this skill when:
- Agent gives wrong or irrelevant responses
- Tools are not being called or are called incorrectly
- Conversation gets stuck in loops or repeated patterns
- Agent performance is slow or inconsistent
- Tool executions are failing or returning errors
- Need to analyze conversation logs or API traces

## Debugging Workflow

### Step 1: Gather Diagnostic Data

Collect these artifacts from the user:
- **Conversation logs** - Full transcript or chat history
- **API request/response logs** - Raw LLM API calls if available
- **Tool execution logs** - Records of tool calls and outputs
- **Agent configuration** - System prompts, tool schemas, settings
- **Description of the issue** - What's wrong and when it occurs

### Step 2: Run Automated Analysis

Use the appropriate analysis scripts based on symptoms:

**For general conversation issues:**
```bash
python scripts/analyze_conversation.py <log_file>
```
Analyzes role distribution, message patterns, detects potential issues, provides summary metrics.

**For suspected loops or stuck states:**
```bash
python scripts/detect_loops.py <log_file> [--threshold 2] [--window 5]
```
Detects exact loops, fuzzy patterns, stuck states, and ping-pong exchanges.

**For tool/function calling problems:**
```bash
python scripts/analyze_tool_calls.py <log_file> [--schema tool_schema.json]
```
Analyzes tool usage patterns, validates against schema, detects errors and retry loops.

**For performance/latency issues:**
```bash
python scripts/analyze_performance.py <log_file>
```
Calculates latency statistics, identifies slow responses, analyzes performance by role.

**Note:** Scripts accept JSON-formatted logs. For text logs, `analyze_conversation.py` can auto-detect and parse common formats.

### Step 3: Interpret Results

Review script outputs and identify patterns:
- Check for **warnings and issues** flagged by scripts
- Look at **metrics** (latency, token usage, tool call counts)
- Examine **repeated patterns** or anomalies
- Cross-reference with common failure modes

### Step 4: Match to Known Patterns

Consult the debugging patterns reference:

```
Read references/debugging-patterns.md
```

This comprehensive guide covers:
1. **Conversation Loops** - Symptoms, causes, solutions
2. **Tool Calling Failures** - Detection and fixes
3. **Context Window Exhaustion** - Management strategies
4. **Incorrect Responses** - Prompt engineering fixes
5. **Performance Issues** - Optimization techniques
6. **Tool Execution Errors** - Error handling approaches
7. **State Management Issues** - Tracking strategies

Each pattern includes:
- Observable symptoms
- Root causes
- Concrete solutions
- Detection methods

### Step 5: Recommend Solutions

Based on analysis and pattern matching:

1. **Identify root cause** - What's actually broken?
2. **Propose specific fixes** - Concrete changes to prompts, tools, or config
3. **Explain reasoning** - Why this will solve the problem
4. **Suggest testing** - How to verify the fix works
5. **Preventive measures** - How to avoid similar issues

### Step 6: Provide Best Practices

For broader improvements, reference:

```
Read references/agent-best-practices.md
```

Covers:
- System prompt design principles
- Tool design and implementation
- Conversation management strategies
- Error handling approaches
- Quality assurance and monitoring
- Optimization techniques

## Log Format Requirements

Scripts work best with structured JSON logs:

**Minimal format:**
```json
[
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

**With tool calls (OpenAI/Anthropic format):**
```json
[
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_123",
        "type": "function",
        "function": {
          "name": "search_kb",
          "arguments": "{\"query\": \"password reset\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_123",
    "content": "Article: How to reset your password..."
  }
]
```

**With timestamps and metadata:**
```json
[
  {
    "role": "user",
    "content": "Hello",
    "timestamp": "2024-01-15T10:30:00Z",
    "message_id": "msg_1"
  },
  {
    "role": "assistant",
    "content": "Hi there!",
    "timestamp": "2024-01-15T10:30:02Z",
    "usage": {
      "prompt_tokens": 50,
      "completion_tokens": 10,
      "total_tokens": 60
    }
  }
]
```

Scripts auto-detect format and extract available information.

## Quick Diagnostic Checklist

**Agent not responding:**
- [ ] Check API connectivity and auth
- [ ] Review error logs
- [ ] Verify configuration is valid
- [ ] Check rate limits

**Wrong/irrelevant responses:**
- [ ] Review system prompt clarity
- [ ] Check if appropriate tools are called
- [ ] Verify necessary context is present
- [ ] Test with clearer user input

**Conversation stuck/looping:**
- [ ] Run `detect_loops.py`
- [ ] Check for repeated tool errors
- [ ] Review last few agent responses
- [ ] Add explicit loop break conditions

**Tool calling issues:**
- [ ] Run `analyze_tool_calls.py` with schema
- [ ] Validate tool descriptions are clear
- [ ] Check tool implementation for bugs
- [ ] Test tools independently

**Performance problems:**
- [ ] Run `analyze_performance.py`
- [ ] Check token usage and context length
- [ ] Review tool execution times
- [ ] Consider model/infrastructure

## Example Debugging Session

**User reports:** "Agent keeps asking for the same information repeatedly"

**Analysis approach:**
1. Collect conversation log
2. Run `detect_loops.py` → Confirms ping-pong pattern detected
3. Run `analyze_conversation.py` → Shows high repeated content
4. Review conversation → Agent not retaining context from earlier messages
5. Consult `debugging-patterns.md` → Matches "State Management Issues"
6. **Solution:** Add explicit state tracking to system prompt, include conversation summary
7. **Test:** Verify agent now references earlier information
8. **Document:** Record fix and add to monitoring

## Resources

### scripts/
Analysis utilities that can be run directly on log files:
- `analyze_conversation.py` - General conversation analysis
- `detect_loops.py` - Loop and pattern detection
- `analyze_tool_calls.py` - Tool usage analysis and validation
- `analyze_performance.py` - Performance and latency analysis

### references/
In-depth debugging knowledge:
- `debugging-patterns.md` - Common failure modes and solutions (read when interpreting analysis results)
- `agent-best-practices.md` - Design and implementation best practices (read when providing recommendations)
