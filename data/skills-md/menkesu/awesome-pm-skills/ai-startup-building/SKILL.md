---
name: ai-startup-building
description: Builds AI-native products using Dan Shipper's 5-product playbook and Brandon Chu's AI product frameworks. Use when implementing prompt engineering, creating AI-native UX, scaling AI products, or optimizing costs. Focuses on 2025+ best practices.
---

# AI-Native Startup Patterns

## When This Skill Activates

Claude uses this skill when:
- Building AI-first products
- Implementing prompt engineering
- Creating AI-native workflows
- Scaling AI products efficiently

## Core Frameworks

### 1. AI-Native Startup Playbook (Source: Dan Shipper - 5 products, 7-fig revenue, 100% AI)

**Key Principles:**
- Build fast with AI
- Test with real users immediately
- Iterate based on usage
- Focus on distribution, not just product

### 2. 2025 Prompt Engineering Best Practices

**Modern Approach:**
```
- Use structured outputs (JSON)
- Implement streaming
- Design for retry logic
- Plan for model switching
- Cache aggressively
```

### 3. Cost Optimization

**Strategies:**
1. **Caching:** 80% of queries can be cached
2. **Model routing:** Simple → small model, complex → large model
3. **Batching:** Group similar requests
4. **Prompt optimization:** Minimize tokens

---

## Action Templates

### Template: AI Product Implementation

```typescript
// Modern AI product pattern (2025)

interface AIFeature {
  // Streaming for responsiveness
  async *stream(prompt: string): AsyncGenerator<string> {
    const cached = await checkCache(prompt);
    if (cached) return cached;
    
    // Route to appropriate model
    const model = this.selectModel(prompt);
    
    for await (const chunk of model.stream(prompt)) {
      yield chunk;
    }
  }
  
  // Model selection (cost optimization)
  selectModel(prompt: string): Model {
    if (this.isSimple(prompt)) {
      return this.smallModel; // Fast, cheap
    } else {
      return this.largeModel; // Smart, expensive
    }
  }
  
  // Retry logic (reliability)
  async withRetry<T>(fn: () => Promise<T>): Promise<T> {
    for (let i = 0; i < 3; i++) {
      try {
        return await fn();
      } catch (e) {
        if (i === 2) throw e;
        await sleep(Math.pow(2, i) * 1000);
      }
    }
  }
}
```

### Template: AI Cost Budget

```markdown
# AI Cost Analysis: [Feature]

## Current Usage
- Daily requests: [X]
- Model: [GPT-4/Claude/etc.]
- Cost per 1K requests: [$X]
- Monthly cost: [$Y]

## Optimization Plan

### 1. Caching (Est. 80% hit rate)
- Before: [100]% paid calls
- After: [20]% paid calls
- Savings: [80]%

### 2. Model Routing
- Simple queries ([60]%): Small model
- Complex queries ([40]%): Large model
- Savings: [50]%

### 3. Batching
- Real-time: [X]% of requests
- Batchable: [Y]% of requests
- Savings: [Z]%

## Projected Cost
- Before optimization: [$X/month]
- After optimization: [$Y/month]
- Reduction: [Z]%
```

---

## Quick Reference

### 🤖 AI Startup Checklist

**Build:**
- [ ] Streaming implemented
- [ ] Retry logic added
- [ ] Model switching supported
- [ ] Structured outputs (JSON)

**Optimize:**
- [ ] Caching implemented
- [ ] Model routing (simple vs complex)
- [ ] Prompt tokens minimized
- [ ] Batch processing where possible

**Scale:**
- [ ] Cost per user < $X
- [ ] Latency < X seconds
- [ ] Error rate < X%
- [ ] Model swappable (not locked in)

---

## Real-World Examples

### Example: Dan Shipper's AI Products

**Approach:**
- Built 5 AI products in 12 months
- All using AI end-to-end
- Revenue: 7 figures
- Team: Small, AI-augmented

**Key Insights:**
- Ship fast, learn from users
- AI makes small teams powerful
- Distribution > perfect product

---

## Key Quotes

**Dan Shipper:**
> "AI doesn't replace PMs. It makes small PM teams as powerful as large ones."

**On Prompt Engineering:**
> "The best prompts in 2025 are structured, explicit, and tested with evals."

**Brandon Chu:**
> "Build for the AI you'll have in 6 months, not the AI you have today."

