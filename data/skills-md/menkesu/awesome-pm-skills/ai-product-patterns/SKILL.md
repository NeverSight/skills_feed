---
name: ai-product-patterns
description: Builds AI-native products using OpenAI's development philosophy and modern AI UX patterns. Use when integrating AI features, designing for model improvements, implementing evals as product specs, or creating AI-first experiences. Based on Kevin Weil (OpenAI CPO) on building for future models, hybrid approaches, and cost optimization.
---

# AI-Native Product Building

## When This Skill Activates

Claude uses this skill when:
- Integrating AI features (search, recommendations, generation, etc.)
- Designing product experiences around AI capabilities
- Implementing evals and quality measurement
- Optimizing AI costs and latency
- Building for model improvements over time

## Core Frameworks

### 1. Build for Future Models (Source: Kevin Weil, CPO of OpenAI)

**The Exponential Improvement Mindset:**
> "The AI model you're using today is the worst AI model you will ever use for the rest of your life. What computers can do changes every two months."

**Core Principle:**
- Don't design around current model limitations
- Build assuming capabilities will 10x in 2 months
- Edge cases today = core use cases tomorrow
- Make room for model to get smarter

**How to Apply:**
```
DON'T:
- "AI can't do X, so we won't support it"
- Build fallbacks that limit model capabilities
- Design UI that assumes current limitations

DO:
- Build interfaces that scale with model improvements
- Design for the capability you want, not current reality
- Test with future models in mind
- Make it easy to swap/upgrade models
```

**Example:**
```
Feature: "AI code review"

❌ Current-Model Thinking:
- "Models can't catch logic bugs, only style"
- Limit to linting and formatting
- Don't even try complex reasoning

✅ Future-Model Thinking:
- Design for full logic review capability
- Start with style, but UI supports deeper analysis
- As models improve, feature gets better automatically
- Progressive: Basic → Advanced → Expert review
```

---

### 2. Evals as Product Specs (Source: Kevin Weil, OpenAI)

**Test Cases = Product Requirements:**
> "At OpenAI, evals are the product spec. If you can define what good looks like in test cases, you've defined the product."

**The Approach:**

**Traditional PM:**
```markdown
Requirement: "Search should return relevant results"
```

**AI-Native PM:**
```javascript
// Eval as Product Spec
const searchEvals = [
  {
    query: "best PM frameworks",
    expectedResults: ["RICE", "LNO", "Jobs-to-be-Done"],
    quality: "all3InTop5",
  },
  {
    query: "how to prioritize features",
    expectedResults: ["Shreyas Doshi", "Marty Cagan"],
    quality: "relevantInTop3",
  },
  {
    query: "shiip prodcut",  // typo
    correctAs: "ship product",
    quality: "handleTypos",
  },
];
```

**How to Write Evals:**
```
1. Define Success Cases:
   - Input: [specific user query/action]
   - Expected: [what good output looks like]
   - Quality bar: [how to measure success]

2. Define Failure Cases:
   - Input: [edge case, adversarial, error]
   - Expected: [graceful handling]
   - Quality bar: [minimum acceptable]

3. Make Evals Runnable:
   - Automated tests
   - Run on every model change
   - Track quality over time
```

**Example:**
```typescript
// Product Requirement as Eval
describe("AI Recommendations", () => {
  test("cold start: new user gets popular items", async () => {
    const newUser = { signupDate: today, interactions: [] };
    const recs = await getRecommendations(newUser);
    
    expect(recs).toIncludePopularItems();
    expect(recs.length).toBeGreaterThan(5);
  });

  test("personalized: returning user gets relevant items", async () => {
    const user = { interests: ["PM", "AI", "startups"] };
    const recs = await getRecommendations(user);
    
    expect(recs).toMatchInterests(user.interests);
    expect(recs).toHaveDiversity();  // Not all same topic
  });

  test("quality bar: recommendations >70% click rate", async () => {
    const users = await getTestUsers(100);
    const clickRate = await measureClickRate(users);
    
    expect(clickRate).toBeGreaterThan(0.7);
  });
});
```

---

### 3. Hybrid Approaches (Source: Kevin Weil)

**AI + Traditional Code:**
> "Don't make everything AI. Use AI where it shines, traditional code where it's reliable."

**When to Use AI:**
- Pattern matching, recognition
- Natural language understanding
- Creative generation
- Ambiguous inputs
- Improving over time

**When to Use Traditional Code:**
- Deterministic logic
- Math, calculations
- Data validation
- Access control
- Critical paths

**Hybrid Patterns:**

**Pattern 1: AI for Intent, Code for Execution**
```javascript
// Hybrid: AI understands, code executes
async function processUserQuery(query) {
  // AI: Understand intent
  const intent = await ai.classify(query, {
    types: ["search", "create", "update", "delete"]
  });
  
  // Traditional: Execute deterministically
  switch(intent.type) {
    case "search": return search(intent.params);
    case "create": return create(intent.params);
    // ... reliable code paths
  }
}
```

**Pattern 2: AI with Rule-Based Fallbacks**
```javascript
// Hybrid: AI primary, rules backup
async function moderateContent(content) {
  // Fast rules-based check first
  if (containsProfanity(content)) return "reject";
  if (content.length > 10000) return "reject";
  
  // AI for nuanced cases
  const aiModeration = await ai.moderate(content);
  
  // Hybrid decision
  if (aiModeration.confidence > 0.9) {
    return aiModeration.decision;
  } else {
    return "human_review";  // Uncertain → human
  }
}
```

**Pattern 3: AI + Ranking/Filtering**
```javascript
// Hybrid: AI generates, code filters
async function generateRecommendations(user) {
  // AI: Generate candidates
  const candidates = await ai.recommend(user, { count: 50 });
  
  // Code: Apply business rules
  const filtered = candidates
    .filter(item => item.inStock)
    .filter(item => item.price <= user.budget)
    .filter(item => !user.previouslyPurchased(item));
  
  // Code: Apply ranking logic
  return filtered
    .sort((a, b) => scoringFunction(a, b))
    .slice(0, 10);
}
```

---

### 4. AI UX Patterns

**Streaming:**
```javascript
// Show results as they arrive
for await (const chunk of ai.stream(prompt)) {
  updateUI(chunk);  // Immediate feedback
}
```

**Progressive Disclosure:**
```
[AI working...]  →  [Preview...]  →  [Full results]
```

**Retry and Refinement:**
```
User: "Find PM articles"
AI: [shows results]
User: "More about prioritization"
AI: [refines results]
```

**Confidence Indicators:**
```javascript
if (result.confidence > 0.9) {
  show(result);  // High confidence
} else if (result.confidence > 0.5) {
  show(result, { disclaimer: "AI-generated, verify" });
} else {
  show("I'm not confident. Try rephrasing?");
}
```

**Cost-Aware Patterns:**
```javascript
// Progressive cost
if (simpleQuery) {
  return await smallModel(query);  // Fast, cheap
} else {
  return await largeModel(query);  // Slow, expensive
}
```

---

## Decision Tree: When to Use AI

```
FEATURE DECISION
│
├─ Deterministic logic needed? ────YES──→ TRADITIONAL CODE
│  (math, validation, access)
│  NO ↓
│
├─ Pattern matching / NLP? ────────YES──→ AI (with fallbacks)
│  (understanding intent, ambiguity)
│  NO ↓
│
├─ Creative generation? ───────────YES──→ AI (with human oversight)
│  (writing, images, ideas)
│  NO ↓
│
├─ Improves with more data? ───────YES──→ AI + ML
│  (recommendations, personalization)
│  NO ↓
│
└─ Use TRADITIONAL CODE ←──────────────────┘
   (More reliable for this use case)
```

## Action Templates

### Template 1: AI Feature Spec with Evals

```markdown
# AI Feature: [Name]

## What It Does
User goal: [describe job to be done]
AI capability: [what AI makes possible]

## Evals (Product Spec)

### Success Cases
```javascript
test("handles typical user query", async () => {
  const input = "[example]";
  const output = await aiFeature(input);
  expect(output).toMatch("[expected]");
});

test("handles edge case", async () => {
  // Define edge cases as tests
});
```

### Quality Bar
- Accuracy: [X%]
- Latency: [<X ms]
- Cost: [<$X per 1000 calls]

## Hybrid Approach
- AI handles: [list]
- Traditional code handles: [list]
- Fallback: [when AI uncertain]

## Model Improvement Plan
- Today's capability: [current]
- Expected in 3 months: [future]
- Design accommodates: [how UI scales]
```

### Template 2: AI Cost Optimization

```markdown
# AI Feature: [Name]

## Cost Structure
- Model: [GPT-4, Claude, etc.]
- Cost per call: [$X]
- Expected volume: [X calls/day]
- Monthly cost: [estimate]

## Optimization Strategies

### 1. Caching
- [ ] Cache common queries
- [ ] Cache user context
- [ ] Expiry: [duration]

### 2. Model Routing
- [ ] Simple queries → small model
- [ ] Complex queries → large model
- [ ] Threshold: [define]

### 3. Batching
- [ ] Group similar requests
- [ ] Process in batches
- [ ] Update frequency: [timing]

### 4. Prompt Optimization
- [ ] Minimize token count
- [ ] Reusable system prompts
- [ ] Structured outputs (JSON)

### 5. Hybrid Approaches
- [ ] Rules-based preprocessing
- [ ] AI only when needed
- [ ] Fallback to deterministic
```

### Template 3: AI UX Implementation

```markdown
# Feature: [Name]

## UX Patterns

### Streaming Response
```javascript
// Show results as they arrive
for await (const chunk of stream) {
  appendToUI(chunk);
}
```

### Loading States
- Initial: "Thinking..."
- Progress: "Analyzing..." (if possible)
- Complete: [show results]

### Error Handling
- Model error: "Something went wrong, try again"
- Timeout: "This is taking longer than expected..."
- Rate limit: "Too many requests, please wait"

### Confidence Display
- High (>0.9): Show results directly
- Medium (0.5-0.9): Show with disclaimer
- Low (<0.5): Ask user to clarify

### Refinement Loop
- Show initial results
- "Refine" button
- Conversational refinement
```

## Quick Reference Card

### 🤖 AI Product Checklist

**Before Building:**
- [ ] Evals written (test cases = product spec)
- [ ] Hybrid approach defined (AI + traditional code)
- [ ] Model improvement plan (design for future capabilities)
- [ ] Cost estimate (per call, monthly)
- [ ] Quality bar defined (accuracy, latency, cost)

**During Build:**
- [ ] Implementing streaming (for responsiveness)
- [ ] Adding confidence indicators
- [ ] Building retry/refinement flows
- [ ] Caching common queries
- [ ] Fallbacks for failures

**Before Ship:**
- [ ] Evals passing (quality bar met)
- [ ] Cost within budget
- [ ] Error states handled
- [ ] Model swappable (not locked to one provider)
- [ ] Monitoring in place

---

## Real-World Examples

### Example 1: OpenAI's ChatGPT Memory

**Challenge:** Users want persistent context

**AI-Native Approach:**
- Built for models that would improve memory
- Started simple, designed for sophisticated future
- Evals: "Remembers facts across sessions"
- Hybrid: Explicit memory + AI interpretation

**Result:** Feature improves as models improve

---

### Example 2: AI Search Implementation

**Challenge:** Traditional search missing intent

**Hybrid Approach:**
```javascript
async function search(query) {
  // Traditional: Exact matches (fast, cheap)
  const exactMatches = await traditionalSearch(query);
  if (exactMatches.length > 10) return exactMatches;
  
  // AI: Semantic search (smart, expensive)
  const semanticResults = await aiSearch(query);
  
  // Hybrid: Combine and rank
  return dedupe([...exactMatches, ...semanticResults]);
}
```

---

### Example 3: Cost Optimization

**Challenge:** AI costs too high

**Solution:**
- Cached 80% of common queries
- Routed simple queries to small model
- Batched recommendations (not real-time)
- Reduced cost 10x while maintaining quality

---

## Common Pitfalls

### ❌ Mistake 1: AI for Everything
**Problem:** Using AI where traditional code is better
**Fix:** Use hybrid approach - AI where it shines, code where it's reliable

### ❌ Mistake 2: Designing for Current Limitations
**Problem:** "Models can't do X, so we won't support it"
**Fix:** Build for future capabilities, room to grow

### ❌ Mistake 3: No Evals
**Problem:** Subjective quality, no measurement
**Fix:** Evals as product specs - define good in test cases

### ❌ Mistake 4: Ignoring Costs
**Problem:** Expensive AI calls without optimization
**Fix:** Cache, batch, route to smaller models

---

## Related Skills

- **zero-to-launch** - For AI-first MVP scoping
- **quality-speed** - For balancing AI quality vs latency
- **exp-driven-dev** - For A/B testing AI features
- **metrics-frameworks** - For measuring AI quality

---

## Key Quotes

**Kevin Weil:**
> "If you're building and the product is right on the edge of what's possible, keep going. In two months, there's going to be a better model."

**On Evals:**
> "At OpenAI, we write evals as product specs. If you can define good output in test cases, you've defined the product."

**On Model Improvements:**
> "The AI model you're using today is the worst AI model you will ever use for the rest of your life."

---

## Further Learning

- **references/openai-ai-first-philosophy.md** - Full AI-native methodology
- **references/evals-examples.md** - Sample evals for common features
- **references/hybrid-patterns.md** - AI + traditional code patterns
- **references/ai-cost-optimization.md** - Cost reduction strategies

