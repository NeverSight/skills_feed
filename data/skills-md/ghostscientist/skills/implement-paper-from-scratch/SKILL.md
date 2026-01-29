---
name: implement-paper-from-scratch
description: Guides you through implementing a research paper step-by-step from scratch. Use when asked to implement a paper, code up a paper, reproduce research results, or build a model from a paper. Focuses on building understanding through implementation with checkpoint questions.
---

# Implement Paper From Scratch

The best way to truly understand a paper is to implement it. This skill guides you through that process methodically.

## Philosophy

- **No copy-pasting from reference implementations** - We build understanding, not just working code
- **Checkpoint questions verify understanding** - You should be able to answer "why" at each step
- **Minimal dependencies** - Use NumPy/PyTorch fundamentals, not high-level wrappers
- **Deliberate debugging** - Bugs are learning opportunities, not obstacles

## Process

### Phase 1: Pre-Implementation Analysis

Before writing any code:

1. **Identify the core algorithm** - Strip away ablations, extensions, bells and whistles. What's the minimal version?

2. **List the components** - Break into modules:
   - Data pipeline
   - Model architecture
   - Loss function(s)
   - Training loop
   - Evaluation metrics

3. **Find the tricky parts** - What's non-obvious?
   - Custom layers or operations
   - Numerical stability concerns
   - Hyperparameter sensitivity
   - Implementation details buried in appendices

4. **Gather reference numbers** - What should we expect?
   - Training loss trajectory
   - Validation metrics at convergence
   - Compute requirements (if stated)

### Phase 2: Scaffolded Implementation

Build up the implementation in this order:

#### Step 1: Data
```python
# Start with synthetic/toy data
# Verify shapes and types before touching real data
```

**Checkpoint:** Can you describe what each tensor represents and its expected shape?

#### Step 2: Model Architecture
```python
# Build layer by layer
# Print shapes at each stage
# Verify parameter counts match paper
```

**Checkpoint:** If you randomly initialize and do a forward pass, do the output shapes match what the paper describes?

#### Step 3: Loss Function
```python
# Implement exactly as described
# Test with known inputs/outputs
# Check gradient flow
```

**Checkpoint:** Can you explain each term in the loss and why it's there?

#### Step 4: Training Loop
```python
# Minimal loop first (no logging, checkpointing, etc.)
# Verify loss decreases on tiny overfit test
# Then add bells and whistles
```

**Checkpoint:** Can you overfit a single batch? If not, something is broken.

#### Step 5: Evaluation
```python
# Implement paper's exact metrics
# Compare against reported numbers
```

**Checkpoint:** On the same data split, how close are you to paper's numbers?

### Phase 3: The Debugging Gauntlet

When it doesn't work (and it won't at first):

1. **The Overfit Test**
   - Can you memorize 1 example? 10? 100?
   - If not, architecture or gradient bug

2. **The Gradient Check**
   - Are gradients flowing to all parameters?
   - Any NaN or exploding gradients?

3. **The Initialization Check**
   - Match paper's initialization exactly
   - This matters more than people think

4. **The Learning Rate Sweep**
   - Log scale: 1e-5 to 1e-1
   - Loss should decrease for some range

5. **The Ablation Debug**
   - Remove components until it works
   - Add back one at a time

### Phase 4: Checkpoint Questions

At each stage, you should be able to answer:

**Understanding:**
- Why does this component exist?
- What would happen without it?
- What alternatives were considered?

**Implementation:**
- Why this specific implementation choice?
- Where could numerical issues arise?
- What's the computational complexity?

**Debugging:**
- What would it look like if this was broken?
- How would you test this in isolation?
- What are the most likely bugs?

## Output Format

For each implementation session, provide:

```markdown
## Today's Implementation Goal
[Specific component we're building]

## Prerequisites Check
- [ ] Previous components working
- [ ] Understand what we're building
- [ ] Know expected behavior

## Implementation

### Code
[Code blocks with extensive comments]

### Checkpoint Questions
1. [Question]
   <details><summary>Answer</summary>[Answer]</details>

2. [Question]
   <details><summary>Answer</summary>[Answer]</details>

### Verification Steps
- [ ] Test 1: [What to check]
- [ ] Test 2: [What to check]

### Common Bugs at This Stage
1. [Bug pattern]: [How to identify and fix]

## What's Next
[Preview of next component and how it connects]
```

## Tips for Specific Paper Types

### Transformer-based
- Attention mask shapes are the #1 bug source
- Verify positional encoding is applied correctly
- Check layer norm placement (pre vs post)

### RL/Policy Gradient
- Sign errors in policy gradient are silent killers
- Advantage normalization matters
- Verify discount factor handling

### Generative Models
- KL term balancing is finicky
- Check latent space distribution
- Verify reconstruction looks reasonable before training

### Computer Vision
- Normalization (ImageNet stats, batch norm) is crucial
- Data augmentation can make or break results
- Verify input preprocessing matches paper exactly

## Success Criteria

You're done when:

1. **Numbers match** - Within reasonable variance of paper's results
2. **Understanding is deep** - You can explain every line of code
3. **You found the gotchas** - You know what breaks and why
4. **You could modify it** - Confident to try your own variations

## Anti-Patterns to Avoid

- ❌ Copying code you don't understand
- ❌ Skipping checkpoint questions
- ❌ Using pre-built components for core algorithm
- ❌ Ignoring discrepancies with paper
- ❌ Moving on before current step works
