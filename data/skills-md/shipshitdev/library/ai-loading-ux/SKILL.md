---
name: ai-loading-ux
description: Design AI loading, thinking, and progress indicator UX. Use when explicitly asked to improve AI waiting states, add thinking indicators, or design loading UX for AI interfaces. Covers reasoning display (chain-of-thought), progress steps, streaming states, and the "elevator mirror effect" for reducing perceived wait time.
---

# AI Loading UX

Design patterns for showing users what's happening while waiting for AI output.

## Decision Framework

First, identify which pattern category applies:

| User is waiting for... | Pattern Category | Key Goal |
|------------------------|------------------|----------|
| AI reasoning/thinking | **Reasoning Display** | Build trust through transparency |
| Multi-step task completion | **Progress Steps** | Show advancement toward goal |
| Content generation/streaming | **Streaming States** | Reduce perceived wait time |
| Background processing | **Status Indicators** | Confirm work is happening |

## Core Principles

### 1. The Elevator Mirror Effect

Users waiting for AI feel time pass slower. Give them something to watch/read—animated indicators reduce *perceived* wait time even when actual time is unchanged.

### 2. Progressive Disclosure

- Show condensed indicator by default ("Thinking...")
- Make details *available* but not forced
- Let curious users expand; don't burden everyone

### 3. More Transparency ≠ Better UX

Balance visibility with cognitive load. Users want answers, not reasoning—but they want to *trust* the answer came from good reasoning.

### 4. Signal Completion Clearly

Users must know when processing ends. Ambiguous end states frustrate users.

## Pattern Quick Reference

### Reasoning Display (Chain-of-Thought)

When AI is "thinking" through a problem. See [references/reasoning-patterns.md](references/reasoning-patterns.md).

**Best approach (Claude-style):**

- Hidden by default, expandable on demand
- Structured bullets when expanded
- Time counter or progress indicator
- Clear "done" state

**Anti-patterns:**

- Wall of streaming text (overwhelming)
- Scrolling too fast to read
- No expand option (feels opaque)
- No clear end state

### Progress Steps

When AI completes sequential tasks. See [references/progress-patterns.md](references/progress-patterns.md).

**Best approach:**

- Show current step + total steps
- Mark completed steps visually
- Show what's actively happening
- Allow step-level details on expand

### Streaming States

When content generates token-by-token. See [references/streaming-patterns.md](references/streaming-patterns.md).

**Best approach:**

- Typing cursor or text animation
- Smooth token appearance (not jarring)
- Skeleton for expected content shape
- "Stop generating" escape hatch

### Status Indicators

When background work happens. See [references/status-patterns.md](references/status-patterns.md).

**Best approach:**

- Subtle but visible animation
- Brief description of current action
- Don't block user from other actions
- Notify on completion

## Implementation Checklist

When implementing any AI loading state:

1. [ ] **Identify pattern category** from decision framework above
2. [ ] **Choose visibility level**: always visible, expandable, or minimal
3. [ ] **Add motion**: animation reduces perceived wait (but keep it subtle)
4. [ ] **Show progress**: time elapsed, steps completed, or content streamed
5. [ ] **Signal completion**: clear visual/state change when done
6. [ ] **Provide escape**: stop/cancel for long operations
7. [ ] **Handle errors**: don't leave user in permanent loading state
8. [ ] **Test on slow connections**: ensure graceful degradation

## Product Comparisons (Reference)

| Product | Approach | Strength | Weakness |
|---------|----------|----------|----------|
| Claude | Hidden reasoning, expandable, structured bullets | Low cognitive load | Can feel opaque |
| ChatGPT | Brief labels, auto-collapse | Unobtrusive | Less transparent |
| DeepSeek | Full streaming reasoning | Maximum transparency | Overwhelming |
| Gemini | User-scrolled, numbered steps | Clear structure | Unclear completion |

## Usage

Read the relevant reference file for your pattern category:

- [references/reasoning-patterns.md](references/reasoning-patterns.md) - Chain-of-thought, thinking indicators
- [references/progress-patterns.md](references/progress-patterns.md) - Step sequences, task completion
- [references/streaming-patterns.md](references/streaming-patterns.md) - Token streaming, content generation
- [references/status-patterns.md](references/status-patterns.md) - Background processing, polling states
