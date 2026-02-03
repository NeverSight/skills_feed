---
name: rnv
description: Chain-of-Verification (CoVe) prompting system. Converts lazy prompts into rigorous 4-stage verified output. Use for any code generation, debugging, or implementation task. Automatically invoked by wavybaby for medium/high complexity tasks. Reduces hallucinations and catches subtle bugs.
disable-model-invocation: false
user-invocable: true
argument-hint: "[your task or lazy prompt]"
---

# Chain-of-Verification (CoVe) System

You are operating in **CoVe Mode** - a rigorous verification framework that separates generation from verification to eliminate hallucinations and subtle errors.

## Core Principle

> "LLM-assisted code review, not LLM-generated code."
> Generation is cheap. Verification is where correctness lives.

---

## THE 4-STAGE COVE PROTOCOL

When given ANY task, you MUST execute all 4 stages in order:

### ═══════════════════════════════════════════════════════════════
### STAGE 1: INITIAL SOLUTION (Unverified Draft)
### ═══════════════════════════════════════════════════════════════

Generate the best possible solution to: **$ARGUMENTS**

**Rules for Stage 1:**
- Produce a complete, working implementation
- This output is INTENTIONALLY UNTRUSTED
- Do not self-censor or hedge - give your best attempt
- Mark this clearly as `[UNVERIFIED DRAFT]`

```
## [UNVERIFIED DRAFT]

[Your initial implementation here]
```

### ═══════════════════════════════════════════════════════════════
### STAGE 2: VERIFICATION PLANNING
### ═══════════════════════════════════════════════════════════════

**WITHOUT re-solving the problem**, enumerate everything that must be verified.

Create a checklist using this template:

```
## Verification Plan

### Critical Claims to Verify
- [ ] Claim 1: [specific assertion from Stage 1]
- [ ] Claim 2: [specific assertion from Stage 1]

### API/Library Correctness
- [ ] [API name]: [specific usage to verify]
- [ ] [Library]: [version compatibility, correct method signature]

### Edge Cases
- [ ] [Edge case 1]: [what could break]
- [ ] [Edge case 2]: [what could break]

### Concurrency & State
- [ ] [Race condition risk]: [where it could occur]
- [ ] [State mutation]: [potential issues]

### Type Safety
- [ ] [Type assertion 1]: [verify correctness]
- [ ] [Implicit any or unsafe cast]: [location]

### Environment Assumptions
- [ ] [Runtime]: [Node version, browser, etc.]
- [ ] [Database]: [engine, isolation level]
- [ ] [Dependencies]: [version requirements]

### Performance Claims
- [ ] [Complexity claim]: [O(n), O(n log n), etc.]
- [ ] [Memory usage]: [any concerns]

### Security Considerations
- [ ] [Input validation]: [where needed]
- [ ] [Injection risks]: [SQL, XSS, command]
- [ ] [Auth/authz]: [any assumptions]
```

### ═══════════════════════════════════════════════════════════════
### STAGE 3: INDEPENDENT VERIFICATION
### ═══════════════════════════════════════════════════════════════

**CRITICAL: Do not rely on Stage 1 reasoning. Verify each item INDEPENDENTLY.**

For each checklist item, provide:

```
## Independent Verification

### ✓ PASSED | ✗ FAILED | ⚠ WARNING

#### [Item Name]
- **Verdict**: ✓ PASSED / ✗ FAILED / ⚠ WARNING
- **Evidence**: [Concrete proof or counterexample]
- **If Failed**: [Specific fix required]
```

**Verification Techniques to Use:**

1. **Constraint-Driven Verification**
   - Verify against explicit environment constraints
   - Check version compatibility
   - Validate type correctness

2. **Adversarial Verification**
   - Attempt to construct inputs that break the code
   - Focus on: race conditions, off-by-one, null paths, stale closures

3. **Differential Reasoning**
   - Compare to naive/brute-force alternatives
   - Explain tradeoffs

4. **Line-by-Line Semantic Audit** (for critical paths)
   - Explain what each line does
   - Flag any line whose removal wouldn't change behavior

### ═══════════════════════════════════════════════════════════════
### STAGE 4: FINAL VERIFIED SOLUTION
### ═══════════════════════════════════════════════════════════════

**Only after ALL verifications**, produce the final result.

```
## [VERIFIED SOLUTION]

### Changes from Draft
- [Change 1]: [Why it was needed]
- [Change 2]: [Why it was needed]

### Verification Summary
- Total items checked: [N]
- Passed: [X]
- Failed & Fixed: [Y]
- Warnings acknowledged: [Z]

### Final Implementation

[Corrected code here]

### Remaining Caveats
- [Any known limitations]
- [Assumptions that couldn't be verified]
```

---

## LAZY PROMPT CONVERSION

When the user provides a lazy/simple prompt, AUTOMATICALLY expand it using this template:

**User says:** "add a delete button"

**CoVe converts to:**

```
Task: Add a delete button to [inferred component/location]

Stage 1 - Initial Solution:
- Implement the delete button with proper UI
- Add click handler with confirmation
- Call appropriate API/mutation
- Handle loading/error states
- Update cache/state after deletion

Stage 2 - Verification Plan:
- [ ] Button placement follows design system
- [ ] Confirmation prevents accidental deletion
- [ ] API endpoint exists and is correct
- [ ] Optimistic update handles rollback on failure
- [ ] Cache invalidation is complete
- [ ] Loading state prevents double-clicks
- [ ] Error state is user-friendly
- [ ] Accessibility (aria-label, keyboard nav)

Stage 3 - Independent Verification:
[Verify each item]

Stage 4 - Final Verified Solution:
[Corrected implementation]
```

---

## STACK-SPECIFIC VERIFICATION CHECKLISTS

### React / Next.js
```
- [ ] useEffect dependency array is complete
- [ ] useMemo/useCallback dependencies are correct
- [ ] No stale closures in event handlers
- [ ] Keys are stable and unique
- [ ] Server/Client component boundary is correct
- [ ] Suspense boundaries handle loading
- [ ] Error boundaries catch failures
```

### TanStack Query / React Query
```
- [ ] Query keys are consistent and follow pattern
- [ ] Mutations invalidate correct queries
- [ ] Optimistic updates have proper rollback
- [ ] Stale time / cache time are appropriate
- [ ] Infinite queries handle page boundaries
- [ ] Prefetching doesn't cause waterfalls
```

### tRPC
```
- [ ] Procedure types match (query vs mutation)
- [ ] Input validation is complete (Zod schema)
- [ ] Error handling uses TRPCError
- [ ] Context has required auth/session
- [ ] Batching is considered for multiple calls
```

### Prisma / Database
```
- [ ] Transactions wrap related operations
- [ ] Isolation level is appropriate
- [ ] N+1 queries are avoided (include/select)
- [ ] Unique constraints are enforced
- [ ] Cascade deletes are intentional
- [ ] Indexes exist for query patterns
```

### TypeScript
```
- [ ] No `any` types (explicit or implicit)
- [ ] Null/undefined handled properly
- [ ] Type narrowing is sound
- [ ] Generics are constrained appropriately
- [ ] Return types are explicit for public APIs
```

### Async / Concurrency
```
- [ ] Promise.all used for independent operations
- [ ] Race conditions are prevented
- [ ] Cleanup functions in useEffect
- [ ] AbortController for cancellable requests
- [ ] Debounce/throttle where appropriate
```

---

## ADVERSARIAL PROMPTS FOR STAGE 3

Use these to stress-test your Stage 1 solution:

### For Async Code
```
Attempt to construct a sequence of events that would cause:
1. Race condition between two concurrent calls
2. Stale data displayed after mutation
3. Memory leak from uncancelled subscription
4. Deadlock or infinite loop
```

### For State Management
```
Attempt to reach an invalid state by:
1. Rapid successive user actions
2. Network failure mid-operation
3. Component unmount during async operation
4. Browser back/forward navigation
```

### For API Endpoints
```
Attempt to break this endpoint with:
1. Missing or malformed input
2. Unauthorized access
3. SQL/NoSQL injection
4. Excessive payload size
5. Concurrent conflicting requests
```

### For React Components
```
Attempt to cause incorrect rendering by:
1. Props changing faster than render cycle
2. Parent re-rendering with same props
3. Context value changing mid-render
4. Suspense boundary resolution order
```

---

## WHEN TO USE COVE

**Always use for:**
- Any stateful code
- Concurrency/async logic
- Database operations
- Authentication/authorization
- Financial calculations
- Data transformations with edge cases

**Skip only for:**
- Trivial one-liners
- Pure stylistic changes
- Throwaway prototypes
- README/docs updates

---

## EXAMPLE: Full CoVe Flow

**User prompt:** "add pagination to the users table"

### Stage 1: [UNVERIFIED DRAFT]
```typescript
// Initial implementation
const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
  queryKey: ['users'],
  queryFn: ({ pageParam = 0 }) => fetchUsers({ offset: pageParam, limit: 20 }),
  getNextPageParam: (lastPage) => lastPage.nextOffset,
})
```

### Stage 2: Verification Plan
```
- [ ] Query key includes filter/sort params
- [ ] Offset calculation is correct at boundaries
- [ ] Loading state shown during fetch
- [ ] Empty state handled
- [ ] Error state handled
- [ ] Total count displayed correctly
- [ ] Page size is configurable
- [ ] URL state synced with pagination
- [ ] Keyboard navigation works
- [ ] Screen reader announces page changes
```

### Stage 3: Independent Verification
```
✗ FAILED: Query key includes filter/sort params
  - Evidence: queryKey is just ['users'], doesn't include filters
  - Fix: queryKey: ['users', { filters, sort }]

✗ FAILED: URL state synced with pagination
  - Evidence: Page state is local, lost on refresh
  - Fix: Use URL search params or router state

✓ PASSED: Offset calculation
  - Evidence: getNextPageParam correctly returns nextOffset from API

⚠ WARNING: Total count displayed
  - Evidence: API returns total but we don't display it
  - Recommendation: Show "Page X of Y" or "Showing 1-20 of 156"
```

### Stage 4: [VERIFIED SOLUTION]
```typescript
// Corrected implementation with all fixes applied
const [searchParams, setSearchParams] = useSearchParams()
const page = Number(searchParams.get('page')) || 0

const { data, fetchNextPage, hasNextPage, isLoading, error } = useInfiniteQuery({
  queryKey: ['users', { filters, sort, page }],
  queryFn: ({ pageParam = page }) => fetchUsers({
    offset: pageParam * PAGE_SIZE,
    limit: PAGE_SIZE
  }),
  getNextPageParam: (lastPage, allPages) =>
    lastPage.hasMore ? allPages.length : undefined,
})

// Sync to URL
const goToPage = (newPage: number) => {
  setSearchParams({ page: String(newPage) })
}
```

---

## Integration with /wavybaby

`/wavybaby` automatically invokes CoVe for non-trivial tasks. You can also invoke `/cove` directly when you want verification without the full wavybaby toolkit analysis.

```
/wavybaby [task] → native dispatch + skill discovery + CoVe
/cove [task]     → just the 4-stage verification protocol
```

---

Now executing CoVe protocol for: **$ARGUMENTS**
