---
name: self-reflecting-chain
description: Sequential reasoning with deep self-reflection and backtracking. Use when problems have step-by-step dependencies, need careful logical reasoning, or require error correction. Each step includes self-reflection, and incorrect steps trigger backtracking. Ideal for debugging, mathematical proofs, sequential planning, or causal analysis where order matters.
license: MIT
---

# Self-Reflecting Chain Reasoning Methodology

**Purpose**: Sequential step-by-step reasoning with deep self-reflection at each step. Unlike parallel exploration (ToT/BoT), this follows a single logical chain, reflects on each step's validity, and backtracks when errors detected.

## When to Use Self-Reflecting Chain

**✅ Use when:**
- Steps have dependencies (Step N depends on Step N-1)
- Logical reasoning required (mathematical, causal, deductive)
- Need to trace exact reasoning path
- Error detection and correction critical
- Sequential planning (Step A must complete before Step B)
- Debugging (trace bug through execution flow)

**❌ Don't use when:**
- Multiple independent solution paths exist → Use ToT or BoT
- Need to explore many options in parallel → Use BoT
- Steps can execute in any order → Don't need sequential reasoning

**Examples**:
- "Debug this race condition by tracing execution step-by-step" ✅
- "Prove this mathematical theorem" ✅
- "Plan project where each phase depends on previous" ✅
- "Choose between 5 architectures" (parallel problem - use BoT) ❌

---

## Core Methodology: Chain-Reflect-Backtrack

### Step 1: Problem Decomposition

**Objective**: Break problem into sequential logical steps

**Actions**:
1. Identify starting state
2. Define goal state
3. List steps to get from start to goal (sequential order)
4. Number steps clearly (Step 1, 2, 3...)
5. Identify dependencies between steps

**Example** (Debugging):
```
Start: System crashes when user clicks "Submit"
Goal: Identify root cause

Steps:
1. Trace user action to event handler
2. Check event handler for errors
3. Trace data flow to backend
4. Check backend validation logic
5. Inspect database query execution
6. Identify exact failure point
```

---

### Step 2: Execute Step N with Deep Reflection

**For each step**:

1. **Execute**: Perform the reasoning/action for this step
2. **State Result**: What did you learn/discover?
3. **Self-Reflect**: Is this step correct?
4. **Check Validity**: Does logic hold? Any assumptions?
5. **Confidence**: How confident in this step (0-100%)?

**Step Template**:
```markdown
## Step [N]: [Action]

### Execution
[Perform the reasoning or analysis]

### Result
[What was discovered/concluded]

### Self-Reflection
- **Confidence**: [0-100]%
- **Assumptions**: [What assumptions does this step make?]
- **Logic Check**: [Is the reasoning sound?]
- **Dependencies**: [Does this depend on previous steps being correct?]
- **Potential Errors**: [What could be wrong with this step?]

### Decision
- ✅ **Proceed** to Step [N+1] (confidence ≥70%)
- ⚠️ **Low Confidence** but proceeding (60-69%)
- ❌ **Backtrack** to Step [N-X] (confidence <60%)
```

---

### Step 3: Backtracking Protocol

**Trigger backtracking when:**
- Step confidence <60%
- Logic error detected
- Assumption proven false
- Result contradicts known facts
- Dead end reached

**Backtracking Process**:
1. **Identify error point**: Which step was wrong?
2. **Return to that step**: Go back to Step N-X
3. **Try alternative**: Take different reasoning path
4. **Mark failed path**: Document why previous path failed
5. **Resume forward**: Continue from corrected step

**Backtracking Example**:
```markdown
## Step 5: [Attempted reasoning]
→ Result: Contradiction detected
→ Confidence: 25% (contradicts Step 3 result)

**Backtrack Decision**: Return to Step 3, try alternative interpretation

## Step 3 (Revised): [Alternative reasoning]
→ Result: New interpretation consistent
→ Confidence: 80%
→ Proceed to Step 4 with revised understanding...
```

---

### Step 4: Chain Validation

**At each step**, validate the entire chain so far:

1. **Forward Consistency**: Does Step N follow logically from Step N-1?
2. **Backward Consistency**: Do all previous steps still hold given new information?
3. **Assumption Check**: Have any assumptions been violated?
4. **Alternative Paths**: Should we backtrack and try different approach?

**Validation Checklist**:
- [ ] Each step's confidence ≥70%
- [ ] No logical contradictions
- [ ] All assumptions explicitly stated
- [ ] Dependencies satisfied
- [ ] No better alternative path obvious

---

### Step 5: Final Synthesis

**After completing chain**:

1. **Trace complete path**: List all steps from start to goal
2. **Confidence per step**: Show confidence for each step
3. **Overall confidence**: Minimum confidence across all steps
4. **Alternative paths explored**: Document backtracks and why
5. **Final answer**: Clear conclusion with reasoning trace

**Synthesis Template**:
```markdown
## Reasoning Chain Complete

### Complete Path
1. [Step 1] → Result: [X] (Confidence: 85%)
2. [Step 2] → Result: [Y] (Confidence: 90%)
3. [Step 3] → Result: [Z] (Confidence: 75%)
4. [Step 4] → Result: [A] (Confidence: 88%)
5. [Step 5] → Result: [B] (Confidence: 82%)

### Overall Confidence
**Minimum**: 75% (Step 3 was lowest)
**Chain Confidence**: 75% (limited by weakest link)

### Backtracks
- Backtracked from Step 4 to Step 2 (logic error)
- Alternative path tried at Step 3 (failed, original was correct)

### Final Conclusion
[Answer based on complete reasoning chain]

**Reasoning Trace**: Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Conclusion
```

---

## Self-Critique Checklist

- [ ] **Step Independence**: Is each step clearly defined?
- [ ] **Logical Flow**: Does each step follow from previous?
- [ ] **Reflection Depth**: Did I genuinely reflect on each step (not boilerplate)?
- [ ] **Backtracking Used**: Did I backtrack when confidence low?
- [ ] **Assumptions Explicit**: Are all assumptions stated clearly?
- [ ] **Weakest Link**: Is chain confidence based on weakest step?
- [ ] **Alternative Paths**: Did I consider other approaches when stuck?

---

## Common Mistakes

1. **Skipping Reflection**: Moving to next step without genuine self-reflection
2. **Ignoring Low Confidence**: Proceeding when confidence <60%
3. **Missing Dependencies**: Not checking if later steps depend on earlier ones
4. **No Backtracking**: Never questioning previous steps when contradictions arise
5. **False Confidence**: High confidence without justification
6. **Hidden Assumptions**: Not explicitly stating what you're assuming

---

## Sequential vs Parallel Decision Guide

| Problem Type | Use Self-Reflecting Chain | Use ToT/BoT |
|--------------|---------------------------|-------------|
| Dependencies | Sequential steps | Independent paths |
| Goal | Single logical conclusion | Explore options |
| Method | Step-by-step reasoning | Parallel branches |
| Backtracking | Return to previous step | Prune branches |
| Output | Reasoning trace | Multiple solutions |

---

## Summary

Self-Reflecting Chain is systematic methodology for:
1. **Sequential reasoning** (step-by-step)
2. **Deep self-reflection** (confidence at each step)
3. **Error detection** (validate logic continuously)
4. **Backtracking** (correct errors when found)
5. **Traceability** (clear reasoning path)

Use it when order matters, dependencies exist, and you need one correct answer with full reasoning trace.

**Remember**: Chain confidence = minimum step confidence. A 95% confident chain with one 60% step has 60% overall confidence. Strengthen the weakest link.
