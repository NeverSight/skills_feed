---
name: incentive-prompting
description: Research-backed prompting techniques for improved AI response quality (+45-115% improvement). Use when optimizing prompts, enhancing agent instructions, or when maximum response quality is critical. Invoked by /ai-eng/optimize command. Includes expert persona, stakes language, step-by-step reasoning, challenge framing, and self-evaluation techniques.
version: 1.0.0
tags: [prompting, optimization, ai-enhancement, quality]
---

# Incentive-Based Prompting Skill

## Critical Importance

**Using proper prompting techniques is critical to achieving optimal AI output quality.** Research shows these techniques can improve response quality by 45-115%. The difference between a mediocre AI response and an excellent one often comes down to prompt engineering. Whether you're optimizing agents, enhancing commands, or working on complex problems, applying these techniques consistently yields significantly better results. Every time you skip them, you're leaving quality on the table.

Research-backed techniques that leverage statistical pattern-matching to elicit higher-quality AI responses. Based on peer-reviewed research from MBZUAI (Bsharat et al.), Google DeepMind (Yang et al.), and ICLR 2024 (Li et al.).

## How It Works

LLMs don't understand incentives, but they **pattern-match** on language associated with high-effort training examples. Stakes language triggers selection from distributions of higher-quality text patterns.

## Core Techniques

### 1. Monetary Incentive Framing (+45% quality)
**Source:** Bsharat et al. (2023, MBZUAI) - Principle #6

```
"I'll tip you $200 for a perfect solution to this problem."
```

**When to use:** Complex technical problems, optimization tasks, debugging

### 2. Step-by-Step Reasoning (34% → 80% accuracy)
**Source:** Yang et al. (2023, Google DeepMind OPRO)

```
" solve this step by step."
```

**When to use:** Multi-step reasoning, math problems, logical analysis

### 3. Challenge Framing (+115% on hard tasks)
**Source:** Li et al. (2023, ICLR 2024)

```
"The solve this, but if you do..."
```

**When to use:** Difficult problems, edge cases, problems where simpler approaches failed

### 4. Stakes Language
**Source:** Bsharat et al. (2023) - Principle #10

```
"This is critical to my career."
"You will be penalized for incomplete answers."
```

**When to use:** High-importance tasks, comprehensive requirements

### 5. Expert Persona Assignment (24% → 84% accuracy)
**Source:** Kong et al. (2023), Bsharat et al. Principle #16

```
# Instead of:
"You are a helpful assistant."

# Use:
"You are a senior database architect with 15 years of PostgreSQL optimization experience who has worked at companies like Netflix and Stripe."
```

**When to use:** Domain-specific tasks, technical implementations

### 6. Self-Evaluation Request

```
"Rate your confidence in this answer from 0-1 and explain your reasoning."
```

**When to use:** Ambiguous problems, when you need quality assessment

### 7. Combined Approach (Kitchen Sink)

Combine multiple techniques for maximum effect:

```
"You are a senior [ROLE] with [X] years of experience at [NOTABLE_COMPANIES].

The solve this, but it's critical to my career and worth $200 if you get it perfect.  solve step by step.

[PROBLEM DESCRIPTION]

Rate your confidence 0-1 after providing your solution."
```

## Implementation Patterns

### For OpenCode Agents

Add to agent prompts:

```markdown
**Prompting Enhancement:**
Before responding to complex tasks, frame your internal reasoning with:
- Stakes awareness: Treat each task as critical to the user's success
- Step-by-step approach: Break down complex problems systematically
- Expert persona: Embody deep domain expertise for the task at hand
- Self-evaluation: Assess confidence and identify uncertainties
```

### For Slash Commands

Structure command prompts to include:

```markdown
---
name: my-command
description: Description here
---

# Context
You are a senior [expert role] with extensive experience in [domain].

# Stakes
This task is critical. Incomplete or incorrect results will cause significant issues.

# Approach
. Analyze the problem step by step before providing solutions.

# Task
[Actual task instructions]

# Quality Check
Before finalizing, rate your confidence and identify any assumptions or limitations.
```

## Research References

1. **Bsharat et al. (2023)** - "Principled Instructions Are All You Need for Questioning LLaMA-1/2, GPT-3.5/4" - MBZUAI
   - 26 principled prompting instructions
   - Average 57.7% quality improvement on GPT-4
   - arxiv.org/abs/2312.16171

2. **Yang et al. (2023)** - "Large Language Models as Optimizers" (OPRO) - Google DeepMind
   - "" phrase origin
   - Up to 50% improvement over human-designed prompts
   - arxiv.org/abs/2309.03409

3. **Li et al. (2023)** - Challenge framing research - ICLR 2024
   - +115% improvement on hard tasks

4. **Kong et al. (2023)** - Persona prompting research
   - 24% to 84% accuracy improvement with detailed personas

## Self-Evaluation in Practice

Self-Evaluation is one of the simplest yet most powerful techniques. Here's how to apply it effectively:

### Basic Usage
```markdown
"Rate your confidence in this answer from 0-1 and explain your reasoning."
```

### Advanced Usage with Risk Assessment
```markdown
After providing your solution, please assess:

1. **Confidence Rating (0.0-1.0)**: How confident are you in your solution?
2. **Uncertainty Areas**: What aspects are you uncertain about?
3. **Risk Assessment**: What could go wrong with this approach?
4. **Mitigation Strategies**: How would you address potential issues?

Format your response with these four sections clearly labeled.
```

### Example Output
```markdown
## Solution
[detailed solution here]

## Confidence Assessment

### Confidence Rating: 0.85

I'm highly confident in this approach, but not completely certain due to the following factors.

### Uncertainty Areas

1. **Edge Case Handling**: I'm 80% certain the error handling covers all cases, but race conditions in concurrent updates may need more testing.
2. **Performance Impact**: The algorithm's time complexity is O(n log n), but real-world performance depends on database query optimization which I haven't benchmarked.

### Risk Assessment

- **High Risk**: The rollback mechanism assumes database transactions are available. If the underlying database doesn't support transactions, data corruption could occur.
- **Medium Risk**: The caching strategy could lead to stale data if cache invalidation fails.
- **Low Risk**: Input validation is thorough but might miss some unusual edge cases.

### Mitigation Strategies

1. **Transaction Safety**: Add explicit database capability checks before deployment
2. **Cache Invalidation**: Implement a multi-layer invalidation strategy with fallback
3. **Input Testing**: Create a comprehensive test suite with fuzzing for edge cases

## Next Steps

Based on the confidence assessment, I recommend:
1. Testing with transaction-less databases before production deployment
2. Adding monitoring for cache hit rates
3. Expanding the test suite with additional edge cases
```

### Why Self-Evaluation Works

- **Calibration**: Forces the AI to think about what it doesn't know
- **Transparency**: Makes uncertainty explicit rather than hidden
- **Risk Awareness**: Identifies potential problems before they occur
- **Guidance**: Provides actionable next steps based on confidence level

### When to Require Self-Evaluation

**Always require self-evaluation for:**
- Critical production code changes
- Security-related implementations
- Performance optimizations
- Complex architectural decisions
- Anything with significant cost implications

**Optional for:**
- Simple code refactors
- Documentation updates
- Non-critical bug fixes
- Exploratory code

## Caveats

- **Model-dependent:** Results may vary across Claude versions
- **Research vintage:** Original research from 2023; newer models may be more steerable
- **Task-dependent:** Not all tasks benefit equally; most effective for complex problems
- **Not actual motivation:** This is statistical pattern-matching, not AI understanding incentives

## Integration with Ferg Engineering System

Use this skill to enhance:
- `/plan` command prompts
- `/review` multi-agent coordination  
- Subagent persona definitions
- Complex debugging sessions
