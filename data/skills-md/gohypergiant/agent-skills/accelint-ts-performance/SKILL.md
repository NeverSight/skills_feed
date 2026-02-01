---
name: accelint-ts-performance
description: "Systematic JavaScript/TypeScript performance audit and optimization using V8 profiling and runtime patterns. Use when: (1) Users say 'optimize performance', 'audit performance', 'this is slow', 'reduce allocations', 'improve speed', 'check performance', (2) Analyzing code for performance anti-patterns (O(n²) complexity, excessive allocations, I/O blocking, template literal waste), (3) Optimizing functions regardless of current usage context - utilities, formatters, parsers are often called in hot paths even when they appear simple, (4) Fixing V8 deoptimization (monomorphic/polymorphic issues, inline caching). Audits ALL code for anti-patterns and reports findings with expected gains. Covers loops, caching, batching, memory locality, algorithmic complexity fixes with ❌/✅ patterns."
license: Apache-2.0
metadata:
  author: accelint
  version: "1.0"
---

# TypeScript Performance Optimization

Systematic performance optimization for JavaScript/TypeScript codebases. Combines audit workflow with expert-level optimization patterns for runtime performance.

## NEVER Do When Optimizing Performance

**Note:** For general best practices (type safety with `any`/`enum`, avoiding `null`, not mutating parameters), use the `accelint-ts-best-practices` skill instead. This section focuses exclusively on performance-specific anti-patterns.

- **NEVER assume code is cold path** - Utility functions, formatters, parsers, and validators appear simple but are frequently called in loops, rendering pipelines, or real-time systems. Always audit ALL code for performance anti-patterns. Do not make assumptions about usage frequency or skip auditing based on perceived simplicity.

- **NEVER apply all optimizations blindly** - Performance patterns have trade-offs. Balance optimization gains against code complexity. When conducting audits, identify ALL anti-patterns through systematic analysis and report them with expected gains. Let users decide which optimizations to apply based on their specific context.

- **NEVER ignore algorithmic complexity** - Optimizing O(n²) code with micro-optimizations is futile. For n=1000, algorithmic fix (O(n² → O(n)) yields 1000x speedup; micro-optimizations yield 1.1-2x at best. Fix algorithm first: use Maps/Sets for O(1) lookups, eliminate nested iterations, choose appropriate data structures.

- **NEVER sacrifice correctness for speed** - Performance bugs are still bugs. Optimizations frequently break edge cases: off-by-one errors in manual loops, wrong behavior for empty arrays, null handling issues. Verify behavior matches before and after. Add comprehensive tests covering edge cases before optimizing—catching bugs in production costs far more than any performance gain.

- **NEVER optimize code you don't own** - Shared utilities, library internals, or code actively developed by others creates merge conflicts, duplicates effort, and confuses ownership. Performance changes affect all callers; coordinate with owners or defer optimization until code stabilizes.

- **NEVER ignore memory vs CPU trade-offs** - Caching trades memory for speed. Unbounded memoization causes memory leaks in long-running applications. A 2x CPU speedup that increases memory 10x can trigger OOM crashes or frequent GC pauses (worse than original slowness). Profile memory usage alongside CPU; set cache size limits; use WeakMap for lifecycle-bound caches.

- **NEVER assume performance across environments** - V8 optimizations differ between Node.js versions (v18 vs v20), browsers (Chrome vs Safari), and architectures (x64 vs ARM). An optimization yielding 3x speedup in Chrome may regress 1.5x in Safari. Profile in ALL target environments before shipping; maintain fallback implementations for environment-specific optimizations.

- **NEVER chain array methods** (.filter().map().reduce()) - Each method creates intermediate arrays and iterates separately. For arrays with 10k items, `.filter().map()` allocates 10k + 5k items (if 50% pass filter) and iterates twice. Use single `reduce` pass to iterate once with zero intermediate allocations, yielding 2-5x speedup in hot paths.

- **NEVER use `Array.includes()` for repeated lookups** - Array.includes() is O(n) linear search. Checking 1000 items against array of 100 is O(n×m) = 100k operations. Use `Set.has()` instead: O(1) lookup via hash table, reducing 100k operations to 1000 for ~100x speedup. Build Set once upfront; amortized cost is negligible.

- **NEVER await before checking if you need the result** - `await` suspends execution immediately, even if the value isn't needed. Move `await` into conditional branches that actually use the result. Example: `const data = await fetch(url); if (condition) { use(data); }` wastes I/O time when condition is false. Better: `if (condition) { const data = await fetch(url); use(data); }` skips fetch entirely when unneeded.

- **NEVER recompute constants inside loops** - Recomputing invariants wastes CPU in every iteration. For 10k iterations, `array.length` lookup (even if cached by engine) or `Math.max(a, b)` runs 10k times unnecessarily. Hoist invariants outside loops: `const len = array.length; for (let i = 0; i < len; i++)` or curry functions to precompute constant parameters once.

- **NEVER create unbounded loops or queues** - Prevents runaway resource consumption from bugs or malicious input. Set explicit limits (`for (let i = 0; i < Math.min(items.length, 10000); i++)`) or timeouts. Unbounded loops can freeze UI threads; unbounded queues cause OOM crashes. Fail fast with clear limits rather than degrading gracefully into unusability.

- **NEVER place `try/catch` in hot paths** - V8 cannot inline functions containing try-catch blocks and marks entire function as non-optimizable. Single try-catch in hot loop causes 3-5x slowdown by preventing inlining, escape analysis, and other optimizations. Validate inputs before hot paths using type guards; move try-catch outside loops to wrap entire operation; use Result types for expected errors.

## Before Optimizing Performance, Ask

Apply these tests to focus optimization efforts effectively:

### Impact Assessment
- **Is this code actually slow?** When profiling data is available, use it to inform prioritization. When unavailable, audit all code for anti-patterns.
- **What percentage of runtime does this represent?** When profiling data is available, flame graphs help identify the highest-impact issues. When unavailable, report all anti-patterns found.
- **Raw performance matters** - Audit ALL code for performance anti-patterns regardless of current usage context. Utility functions, formatters, parsers, and data transformations are frequently called in loops, rendering pipelines, or real-time systems even when they appear simple.

### Correctness Verification
- **Do I have tests covering this code?** Performance bugs are subtle. Comprehensive tests catch regressions from optimizations. Add tests before optimizing.
- **What are the edge cases?** Off-by-one errors, empty arrays, null/undefined values become more likely with manual loop optimizations. Test exhaustively.

### Complexity vs Benefit
- **Is the algorithmic complexity optimal?** O(n) → O(1) is 1000x speedup. Micro-optimizations are 1.1-2x at best. Fix algorithm first.
- **Will this optimization persist?** If the code changes frequently, optimization may be discarded soon. Optimize stable code first.
- **What's the readability cost?** Manual loops are faster but harder to maintain than `.map()`. Balance performance with team velocity.

## How to Use

This skill uses **progressive disclosure** to minimize context usage:

### 1. Start with the Workflow (SKILL.md)
Follow the 4-phase audit workflow below for systematic performance analysis.

### 2. Reference Performance Rules Overview (AGENTS.md)
Load [AGENTS.md](AGENTS.md) to scan compressed rule summaries organized by category.

### 3. Load Specific Performance Patterns as Needed
When you identify specific performance issues, load corresponding reference files for detailed ❌/✅ examples.

## Performance Optimization Workflow

**Copy this checklist to track progress:**

```
- [ ] Phase 1: Profile - Identify actual bottlenecks using profiling tools
- [ ] Phase 2: Analyze - Categorize issues by impact and optimization category
- [ ] Phase 3: Optimize - Apply performance patterns from references/
- [ ] Phase 4: Verify - Measure improvements and validate correctness
```

### Phase 1: Profile to Identify Bottlenecks

**CRITICAL: Audit ALL code for performance anti-patterns.** Do not skip code based on assumptions about usage frequency. Utility functions, formatters, parsers, validators, and data transformations are frequently called in loops, rendering pipelines, or real-time systems even if their implementation appears simple.

**When profiling tools are available**, use them to establish baseline measurements:
- **Browser**: Chrome DevTools Performance tab
- **Node.js**: `node --prof script.js && node --prof-process isolate-*.log`

**Whether profiling data is available or not**: Perform systematic static code analysis to identify ALL performance anti-patterns:
- O(n²) complexity (nested loops, repeated searches)
- Excessive allocations (template literals, object spreads, array methods)
- Template literal allocation when String() would suffice
- Array method chaining (.filter().map())
- Blocking async operations
- Try/catch in loops

**Output**: Complete list of ALL identified anti-patterns with their locations and expected performance impact. Do not filter based on "severity" or "priority" - report everything found.

### Phase 2: Analyze and Categorize Issues

For EVERY issue identified in Phase 1, categorize by optimization type:

**Categorize ALL issues by optimization type:**

| Issue Type | Category | Expected Gain |
|------------|----------|---------------|
| Nested loops, O(n²) complexity | Algorithmic optimization | 10-1000x |
| Repeated expensive computations | Caching & memoization | 2-100x |
| Allocation-heavy code | Allocation reduction | 1.5-5x |
| Sequential access violations | Memory locality | 1.5-3x |
| Excessive I/O operations | I/O optimization | 5-50x |
| Blocking async operations | I/O optimization | 2-10x |
| Property access in loops | Caching & memoization | 1.2-2x |

**Quick reference for mapping issues:**

Load [references/quick-reference.md](references/quick-reference.md) for detailed issue-to-category mapping and anti-pattern detection.

**Output:** Categorized list of ALL issues with their optimization categories. Do not filter or prioritize - list everything found in Phase 1.

### Phase 3: Optimize Using Performance Patterns

**Step 1: Identify your bottleneck category** from Phase 2 analysis.

**Step 2**: Load MANDATORY references for your category. Read each file completely with no range limits.

| Category | MANDATORY Files | Optional | Do NOT Load |
|----------|----------------|----------|-------------|
| **Algorithmic** (O(n²), nested loops, repeated lookups) | reduce-looping.md<br>reduce-branching.md | — | memoization, caching, I/O, allocation |
| **Caching** (property access in loops, repeated calculations) | memoization.md<br>cache-property-access.md | cache-storage-api.md (for Storage APIs) | I/O, allocation |
| **I/O** (blocking async, excessive I/O operations) | batching.md<br>defer-await.md | — | algorithmic, memory |
| **Memory** (allocation-heavy, GC pressure) | object-operations.md<br>avoid-allocations.md | — | I/O, caching |
| **Locality** (sequential access violations, cache misses) | predictable-execution.md | — | all others |
| **Safety** (unbounded loops, runaway queues) | bounded-iteration.md | — | all others |
| **Micro-opt** (hot path fine-tuning, 1.1-2x improvements) | currying.md<br>performance-misc.md | — | all others (apply only after algorithmic fixes) |

**Notes**:
- If bottleneck spans multiple categories, load references for all relevant categories
- Only apply micro-optimizations if: bottleneck is in hot path, algorithmic optimization already applied, need additional 1.1-2x performance

---

**Step 3: Scan for quick reference during optimization**

Load [AGENTS.md](AGENTS.md) to see compressed rule summaries organized by category. Use as a quick lookup while implementing patterns from the detailed reference files above.

**Apply patterns systematically:**

1. **Load the reference file** for the identified issue category
2. **Scan the ❌/✅ examples** to find matching patterns
3. **Apply the optimization** with minimal changes to preserve correctness
4. **Add comments** explaining the optimization and referencing the pattern

**Example optimization:**
```typescript
// ❌ Before: O(n²) - nested iteration
for (const user of users) {
  const items = allItems.filter(item => item.userId === user.id);
  process(items);
}

// ✅ After: O(n) - single pass with Map lookup
// Performance: reduce-looping.md - build lookup once pattern
const itemsByUser = new Map<string, Item[]>();
for (const item of allItems) {
  if (!itemsByUser.has(item.userId)) {
    itemsByUser.set(item.userId, []);
  }
  itemsByUser.get(item.userId)!.push(item);
}

for (const user of users) {
  const items = itemsByUser.get(user.id) ?? [];
  process(items);
}
```

### Phase 4: Verify Improvements

**Measure performance gain:**
1. Re-run profiler with same inputs
2. Compare before/after runtime percentages
3. Document speedup factor (e.g., "2.3x faster")

**Verify correctness:**
1. Run existing test suite - all tests must pass
2. Add new tests for edge cases affected by optimization
3. Manual testing for user-facing functionality

**Document optimization:**
```typescript
// Performance optimization applied: 2026-01-28
// Issue: Nested iteration causing O(n²) complexity with 10k items
// Pattern: reduce-looping.md - Map-based lookup
// Speedup: 145x faster (5200ms → 36ms)
// Verified: All tests pass, manual QA complete
```

**Deciding whether to keep the optimization:**
- **>10x speedup:** Always keep if tests pass
- **2-10x speedup:** Keep if tests pass and code remains maintainable
- **1.2-2x speedup:** Keep for hot paths (>1000 executions/sec) or real-time systems
- **1.05-1.2x speedup:** Keep only if trivial change or critical rendering/animation loop
- **<1.05x speedup:** Revert unless it also improves readability

**Real-time systems (60fps rendering, live data visualization):**
Even 1.05x improvements matter in critical hot paths. Use frame timing profiler to verify impact on frame budget (16.67ms for 60fps).

**If tests fail:** Fix the optimization or revert. Performance bugs are still bugs.

## Freedom Calibration

**Calibrate guidance specificity to optimization impact:**

| Optimization Type | Freedom Level | Guidance Format | Example |
|------------------|---------------|-----------------|---------|
| **Algorithmic (10x+ gain)** | Medium freedom | Multiple valid approaches, pick based on constraints | "Use Map for O(1) lookup or Set for deduplication" |
| **Caching (2-10x gain)** | Medium freedom | Pattern with examples, cache invalidation strategy | "Memoize with WeakMap if lifecycle matches source objects" |
| **Micro-optimization (1.1-2x)** | Low freedom | Exact pattern from reference, measure first | "Cache array.length in loop: `for (let i = 0, len = arr.length; ...)`" |

**The test:** "What's the speedup and maintenance cost?"
- 10x+ speedup → Worth complexity, medium freedom with patterns
- 2-10x speedup → Justify with measurements, medium freedom
- 1.2-2x speedup → Valuable for hot paths and real-time systems, low freedom with exact patterns
- 1.05-1.2x speedup → Only if trivial change or critical hot path (60fps rendering, etc.)

## Important Notes

- **Audit everything philosophy** - Audit ALL code for performance anti-patterns. Utility functions, formatters, parsers, and validators are frequently called in loops or real-time systems even when they appear simple. Do not make assumptions about usage frequency.
- **Report all findings** - Whether profiling data is available or not, perform systematic static analysis to identify and report ALL anti-patterns with their expected gains. Do not filter based on "severity" or "priority."
- **Reference files are authoritative** - The patterns in references/ have been validated. Follow them exactly unless measurements prove otherwise.
- **Hot path definition** - Code executed >1000 times per user interaction or >100 times per second in server contexts. For real-time systems (60fps rendering, live visualization), hot paths are functions in the critical rendering loop consuming >1ms per frame.
- **Real-time systems have stricter requirements** - 60fps = 16.67ms frame budget. 120fps = 8.33ms. Even 1.05x improvements in hot paths are valuable. Profile with frame timing, not just total execution time.
- **Regression testing** - Performance optimizations frequently introduce subtle bugs in edge cases. Add tests before optimizing.
- **Memory profiling matters** - Some optimizations (memoization, caching) trade memory for speed. Monitor memory usage in production, especially for long-running real-time applications.

## Quick Decision Tree

Use this table to rapidly identify which optimization category applies.

**Audit everything**: Identify ALL performance anti-patterns in the code regardless of current usage context. Report all findings with expected gains.

| If You See... | Root Cause | Optimization Category | Expected Gain |
|---------------|------------|----------------------|---------------|
| Nested `for` loops over same data | O(n²) complexity | Algorithmic (reduce-looping) | 10-1000x |
| `.filter()` followed by `.find()` or `.map()` | Multiple passes over data | Algorithmic (reduce-looping) | 2-10x |
| Repeated `array.find()` or `.includes()` | O(n) linear search | Algorithmic (reduce-looping, use Set/Map) | 10-100x |
| Many `if/else` chains on same variable | Branch-heavy code | Algorithmic (reduce-branching) | 1.5-3x |
| Same function called with same inputs repeatedly | Redundant computation | Caching (memoization) | 2-100x |
| `obj.prop.nested.deep` accessed multiple times in loop | Property access overhead | Caching (cache-property-access) | 1.2-2x |
| `localStorage.getItem()` or `sessionStorage` in loop | Expensive I/O in loop | Caching (cache-storage-api) | 5-20x |
| Multiple `await fetch()` in sequence | Sequential I/O blocking | I/O (batching, defer-await) | 2-10x |
| `await` before conditional that might not need result | Premature async suspension | I/O (defer-await) | 1.5-3x |
| Many object spreads `{...obj}` or `[...arr]` | Allocation overhead | Memory (avoid-allocations) | 1.5-5x |
| Creating objects/arrays inside hot loops | GC pressure from allocations | Memory (avoid-allocations) | 2-5x |
| `Object.assign()` or spread when mutation is safe | Unnecessary immutability cost | Memory (object-operations) | 1.5-3x |
| Accessing array elements non-sequentially | Cache locality issues | Memory Locality (predictable-execution) | 1.5-3x |
| `while(true)` or unbounded queue growth | Runaway resource usage | Safety (bounded-iteration) | Prevents crashes |
| Function called with mostly same first N params | Repeated parameter passing | Micro-opt (currying) | 1.1-1.5x |
| `try/catch` inside hot loop | V8 deoptimization | Micro-opt (performance-misc) | 3-5x |
| String concatenation in loop with `+` | Quadratic string copying | Micro-opt (performance-misc) | 2-10x |

**How to use this table:**
1. Identify the pattern from profiler bottleneck
2. Find matching row in "If You See..." column
3. Jump to corresponding Optimization Category in Phase 3
4. Load MANDATORY reference files for that category
