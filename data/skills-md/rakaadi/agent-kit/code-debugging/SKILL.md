---
name: code-debugging
description: Guide for debugging issue on a specific code sections, pattern, or files. Used this skill when user asking for assistant when debugging an issues or explaining a code. 
---

# Code Debugging Skill

## Skill Purpose

This skill specializes in debugging React Native code issues within the Ecalyptus healthcare mobile application. When you encounter bugs, crashes, unexpected behavior, or error messages, this skill helps identify root causes, explains why problems occur in the React Native environment, and provides targeted fixes. Once bugs are resolved, it can suggest when deeper refactoring would improve code quality and recommend engaging the Refactoring Skill for comprehensive improvements.

## Core Philosophy

**Debug First, Review Later**: Critiquing code architecture while fundamental logic is broken is counterproductive. This skill prioritizes establishing working code before optimizing it. Think of it as ensuring a building's foundation is solid before renovating the interior.

**Simplicity Over Cleverness**: Readable, straightforward code is always preferred over advanced, complex solutions. When debugging, this skill focuses on reducing complexity first because complexity is often where bugs originate. Simple code fails in simple, obvious ways. Complex code fails in complex, hidden ways. A bug in a straightforward conditional is easy to spot and fix. A bug buried in nested abstractions, higher-order functions, or clever composition patterns takes hours to diagnose and days to fix safely. In a healthcare application where mistakes have real consequences, the developer debugging an issue at 2 AM needs to understand the code immediately, not spend time deciphering elegant but opaque logic.

**Fix the Bug, Then Improve the Pattern**: After resolving the immediate issue, assess whether a new code pattern would prevent similar bugs from recurring. Sometimes a bug reveals that the current approach is fundamentally fragile. In these cases, introduce a better pattern as part of the solution. But the pattern should serve clarity and maintainability, not showcase advanced techniques. Every new pattern must earn its place by making the code easier to understand and harder to break.

**Teach, Don't Just Fix**: Every bug is a learning opportunity. This skill explains the mental model behind issues so you understand not just what broke, but why it broke and how to prevent similar issues in the future.

**Context-Aware Analysis**: React Native has unique constraints compared to web development. This skill always explains why certain patterns fail in the React Native environment and suggests RN-compatible alternatives.

## Project Context Reference

This skill always refers to the Copilot Instructions at `.github/copilot-instructions.md` for project-specific patterns, architecture decisions, and conventions. Key patterns to remember:

**Intentional Patterns (Don't Flag These):**
- RTK Query mutations using `.then()` without `.catch()` blocks—error handling is centralized in `queryErrorLogger` middleware (`appSlice.ts`)
- Dynamic base URL switching via `dynamicBaseQuery` in production versus fixed URLs in staging
- Path aliases for all imports (`@components`, `@utils/*`, `@reducers/*`, etc.)—never relative paths
- Colors via `colors.palette.*` from `@theme`—no hardcoded hex values
- Typed Redux hooks from `@hooks/app`—never plain `useDispatch`/`useSelector`

**Architecture Anchors:**
- Dual RTK Query APIs: `mainApi` for healthcare, `backOfficeApi` for inventory
- React Native 0.79.5 with React 19 features available
- Expo SDK ~53 with New Architecture enabled (`newArchEnabled: true`)
- React Compiler enabled via `babel-plugin-react-compiler`

When uncertain about code intention or project patterns, always ask for clarification rather than making assumptions.

## Debugging Process

### Phase 1: Symptom Analysis

When you report a bug or unexpected behavior, the skill follows this investigation pattern:

**Gather Context:**
- What is the expected behavior?
- What actually happens instead?
- Are there error messages or stack traces?
- When does it occur (on mount, on interaction, on state change)?
- Which file and component are involved?

**Initial Hypothesis:**
Based on symptoms, form preliminary hypotheses about root causes. Common bug categories in React Native include:
- Async timing issues (race conditions, stale closures)
- State management problems (stale state, missing dependencies)
- React Native API misuse (web-only APIs, platform-specific behavior)
- Navigation state issues (unmounted component updates)
- Memory leaks (uncleared timers, subscriptions)
- RTK Query cache staleness or improper invalidation

### Phase 2: Root Cause Investigation

**Analyze the Problematic Code:**
The skill examines the specific code section you reference, looking for patterns that explain the symptoms. It considers:

**React Native Environment Constraints:**
- Does this code use web-only APIs that don't exist in React Native?
- Are there platform-specific behaviors (iOS vs Android differences)?
- Is this using deprecated React Native APIs?

**React Rules Violations:**
- Are hooks called conditionally or in loops?
- Are dependency arrays incomplete or incorrect?
- Is state being mutated directly instead of immutably?

**Async Patterns:**
- Are promises handled correctly with proper error handling?
- Could there be race conditions between multiple async operations?
- Are effects triggering updates on unmounted components?

**RTK Query Issues:**
- Is the query/mutation configured with proper cache tags?
- Are there missing `providesTags` or `invalidatesTags`?
- Is conditional fetching handled with `skipToken`?
- Could multiple components be triggering unnecessary refetches?

**Memory and Lifecycle:**
- Are subscriptions, timers, or listeners being cleaned up?
- Could this component be updating state after unmounting?
- Are there circular dependencies causing memory leaks?

### Phase 3: Root Cause Explanation

Once the issue is identified, the skill explains:

**What's Happening:** Describe the bug in terms of program execution flow. Walk through what the code is actually doing step-by-step.

**Why It's Happening:** Explain the underlying reason. This often involves explaining React's mental model, JavaScript's async behavior, or React Native's platform differences.

**Why This Pattern Fails in React Native:** If the issue is RN-specific, explain what React Native lacks compared to web (like DOM APIs, certain browser features, etc.) and why the pattern breaks.

**Example Root Cause Explanation:**

```
The crash occurs because you're calling `document.getElementById()` inside your 
component. This is a web-only API that doesn't exist in React Native.

Here's what's happening: React Native doesn't use a DOM (Document Object Model) 
like web browsers do. Instead, it renders native mobile components directly. 
When your code tries to call `document.getElementById()`, JavaScript throws a 
ReferenceError because the `document` object simply doesn't exist in the React 
Native runtime environment.

In web development, you use `document.getElementById()` to access DOM elements 
directly. In React Native, you should use refs instead, which work the same way 
across web and native platforms. The `useRef` hook gives you a reference to a 
component instance without relying on browser-specific APIs.
```

### Phase 4: Solution

**Provide a Targeted Fix:**
The solution should be:
- Minimal—only fix the bug, don't refactor unnecessarily
- Simple—prefer straightforward solutions over clever ones
- Clear—include code snippets showing exactly what to change
- Explained—clarify why this fix resolves the root cause
- RN-Compatible—verify the solution works in React Native
- Project-Aligned—use path aliases, typed hooks, project patterns

**Prioritize Simplification:** If the bug exists within complex code, consider whether simplifying the logic would both fix the bug and prevent future issues. Often, the act of simplifying complex code naturally eliminates entire categories of bugs because there are fewer interactions and edge cases to reason about.

**Example: Simplifying Complex Code**

```typescript
// Problem: Bug hidden in complex nested logic
const getPatientStatus = (patient: Patient) => {
  return patient.admissions
    .filter(a => a.active)
    .reduce((status, admission) => {
      const vitals = admission.vitals?.filter(v => v.timestamp > Date.now() - 86400000)
      return vitals?.some(v => v.critical) ? 'critical' : 
             vitals?.some(v => v.abnormal) ? 'warning' : status
    }, 'stable')
}

// The bug: Recent critical vitals from inactive admissions are ignored, 
// and the reduce function doesn't properly aggregate statuses

// Solution: Simplify the logic into clear, testable steps
const getPatientStatus = (patient: Patient) => {
  // Get only active admissions
  const activeAdmissions = patient.admissions.filter(a => a.active)
  
  // Collect all recent vitals from active admissions
  const oneDayAgo = Date.now() - 86400000
  const recentVitals = activeAdmissions.flatMap(admission => 
    admission.vitals?.filter(v => v.timestamp > oneDayAgo) ?? []
  )
  
  // Check for critical conditions first
  if (recentVitals.some(v => v.critical)) {
    return 'critical'
  }
  
  // Then check for warnings
  if (recentVitals.some(v => v.abnormal)) {
    return 'warning'
  }
  
  // Default to stable
  return 'stable'
}
```

**Why Simplification Fixes the Bug:**
The original code tried to do too much in a single reduce operation, mixing filtering, mapping, and conditional logic. This made it nearly impossible to reason about the data flow and easy to introduce bugs in the logic. By breaking the operation into discrete steps with clear variable names, each step becomes testable and the bug becomes obvious—we needed `flatMap` to aggregate vitals across admissions, not reduce over admissions while checking vitals. The simpler version is also easier to extend (like adding new status levels) without introducing new bugs.

**Example Targeted Fix:**

```typescript
// Problem: Using document.getElementById (web-only API)
const handleFocus = () => {
  const input = document.getElementById('patient-name')
  input?.focus()
}

// Solution: Use useRef (works in both web and React Native)
import { useRef } from 'react'

const inputRef = useRef<TextInput>(null)

const handleFocus = () => {
  inputRef.current?.focus()
}

// In your JSX:
<TextInput
  ref={inputRef}
  placeholder="Patient Name"
/>
```

**Why This Works:**
The `useRef` hook creates a mutable reference that persists across renders and works identically in React Native and web environments. By storing the reference when the component mounts, you can imperatively call methods like `focus()` without needing browser-specific APIs. This is the React-idiomatic way to interact with component instances directly.

### Phase 5: Prevention Guidance

After fixing the immediate bug, provide brief guidance on how to avoid similar issues:

**Mental Model:** Explain the correct way to think about this pattern in React Native.

**Common Pitfalls:** Highlight related mistakes that follow similar patterns.

**Best Practice:** Reference the project convention or React Native best practice that prevents this category of bugs.

## When to Recommend Refactoring

After resolving a bug, assess whether the code would benefit from broader improvements. Recommend calling the Refactoring Skill when:

**Complexity Breeds More Bugs:**
- The bug was hard to find because the code does too many things at once
- Fixing one bug reveals that similar bugs likely exist in related complex code
- The fix required understanding multiple layers of abstraction
- The code has grown organically complex without clear structure

**Structural Issues Emerge:**
- The bug fix reveals deeply nested conditionals that obscure logic
- Multiple similar bugs suggest a fragile pattern that needs restructuring
- The component has grown too large and responsibilities should be split
- State management is complex and error-prone

**Simplification Opportunity:**
- The code could be rewritten in a simpler way that makes bugs obvious
- Complex clever code could be replaced with straightforward readable code
- Advanced patterns (higher-order functions, complex composition) are obscuring intent
- The code would benefit from being broken into smaller, testable pieces

**Performance Concerns:**
- The component re-renders excessively after the fix
- Array operations in the fixed code could be optimized
- RTK Query usage could be improved with better cache management

**Maintainability Red Flags:**
- The fixed code is hard to understand or fragile
- Similar logic is duplicated across multiple locations
- The component violates single responsibility principle
- Future developers will struggle to understand the code at 2 AM

**Recommendation Pattern:**

```
The bug is now fixed—your component will no longer crash when the patient data 
updates. However, I notice this component has several interrelated issues beyond 
the immediate bug:

1. The conditional rendering logic is deeply nested (4 levels of ternaries)
2. The mapped list items maintain local state that gets lost on re-renders
3. RTK Query is fetching the entire patient object when you only need vitals
4. The complexity of these interactions is what allowed this bug to hide

These issues didn't cause the crash directly, but they created the environment 
where bugs thrive—complex code with many moving parts and hidden dependencies. 
I recommend engaging the Refactoring Skill to simplify this component now that 
it's working correctly. The refactoring would reduce complexity, make future 
bugs obvious instead of hidden, and improve both readability and performance.

The goal isn't to make the code more sophisticated, but to make it simpler and 
more obvious. Simple code is debuggable code.

Would you like me to hand this off to the Refactoring Skill, or would you prefer 
to address these issues later?
```

## React Native Specifics

### Web-Only APIs to Watch For

When debugging, be vigilant for these common web-only patterns that break in React Native:

**DOM APIs:**
- `document.getElementById()`, `querySelector()`, etc.
- `window.location`, `window.history`
- `localStorage`, `sessionStorage` (use `AsyncStorage` or `expo-secure-store` instead)
- `addEventListener('scroll')` on `window` (use React Native's `ScrollView` events)
- CSS properties like `cursor`, `position: fixed`, `z-index` on web elements

**Browser Features:**
- `fetch` with CORS options (React Native doesn't have same-origin policy)
- File system APIs like `FileReader` (use Expo's `FileSystem` instead)
- Clipboard API (use `expo-clipboard` instead)
- Media queries (use `Dimensions` or `useWindowDimensions` from React Native)

**Libraries with Web Assumptions:**
- Chart.js (use Victory Native or React Native Chart Kit)
- HTML parsers (use `react-native-render-html`)
- Web-specific utility libraries (verify RN compatibility first)

### Platform-Specific Behavior

Always explain when behavior differs between iOS and Android:

**Layout Differences:**
- Android has a bottom system navigation bar that affects safe areas
- iOS has dynamic island and notch considerations
- Status bar behavior differs (translucent on Android, opaque on iOS by default)

**Keyboard Behavior:**
- `KeyboardAvoidingView` behavior varies significantly between platforms
- Android's back button affects keyboard dismissal
- iOS keyboard accessories work differently than Android

**Navigation:**
- Stack transitions animate differently
- Back gesture support (iOS swipe, Android back button)
- Modal presentation styles

**Permission Handling:**
- Runtime permission flow differs between platforms
- Some permissions are Android-only or iOS-only

### Expo SDK Version Constraints

The project uses Expo SDK ~53. When suggesting solutions, verify they're supported:

**Check Version Compatibility:**
- Don't suggest APIs introduced in later SDK versions
- Be aware of deprecated APIs in SDK 53
- Know which Expo libraries require specific SDK versions

**Example Version Check:**

```
The `expo-image` library you're using is version 1.x in SDK 53, which doesn't 
support the `contentPosition` prop you're trying to use. That feature was added 
in version 2.x (SDK 54+).

For now, you can achieve similar positioning using the `contentFit` prop combined 
with `style` positioning. If you need the exact `contentPosition` behavior, 
consider whether upgrading to SDK 54 is feasible for your project.
```

## RTK Query Debugging Patterns

Many bugs in your codebase involve RTK Query misuse. Here are the most common patterns to investigate:

### Stale Cache Data

**Symptom:** Component shows old data after an update elsewhere.

**Root Cause:** The mutation doesn't invalidate relevant cache tags, so queries don't refetch.

**Investigation:**
- Check if the mutation has `invalidatesTags` configured
- Verify the tags match the query's `providesTags`
- Look for typos in tag names (case-sensitive)

**Fix Pattern:**
```typescript
// Mutation must invalidate tags
updatePatient: builder.mutation<Patient, UpdatePatientParams>({
  query: ({ id, data }) => ({
    url: `/patients/${id}`,
    method: 'PUT',
    body: data
  }),
  invalidatesTags: (result, error, { id }) => [
    { type: 'Patient', id },
    'PatientList' // Also invalidate list views
  ]
})

// Query must provide tags
getPatient: builder.query<Patient, string>({
  query: (id) => `/patients/${id}`,
  providesTags: (result, error, id) => [
    { type: 'Patient', id }
  ]
})
```

### Unnecessary Re-renders

**Symptom:** Component re-renders when unrelated data changes.

**Root Cause:** Query returns entire response object, so any field change triggers re-render.

**Fix Pattern:**
```typescript
// Over-fetching: Re-renders when any patient field changes
const { data: patient } = useGetPatientQuery(patientId)

// Optimized: Only re-renders when name changes
const { name } = useGetPatientQuery(patientId, {
  selectFromResult: ({ data }) => ({
    name: data?.name
  })
})
```

### Race Conditions in Sequential Queries

**Symptom:** Data inconsistency or incorrect state when multiple queries run.

**Root Cause:** Queries triggered simultaneously without proper coordination.

**Investigation:**
- Are multiple queries fetching interdependent data?
- Is one query depending on results from another?
- Are queries running on every render instead of conditionally?

**Fix Pattern:**
```typescript
// Problem: Both queries run immediately, but second needs first's result
const { data: patient } = useGetPatientQuery(patientId)
const { data: vitals } = useGetVitalsQuery(patient?.mrn) // mrn might be undefined

// Solution: Use skipToken to prevent second query until data is ready
import { skipToken } from '@reduxjs/toolkit/query'

const { data: patient } = useGetPatientQuery(patientId)
const { data: vitals } = useGetVitalsQuery(patient?.mrn ?? skipToken)
```

### Polling Memory Leaks

**Symptom:** App becomes slow over time, or queries continue in background.

**Root Cause:** Polling continues even when screen is unmounted or unfocused.

**Fix Pattern:**
```typescript
import { useFocusEffect } from '@react-navigation/native'
import { useCallback, useState } from 'react'

function MonitorScreen({ patientId }: Props) {
  const [pollingInterval, setPollingInterval] = useState(0)
  
  // Start polling when screen is focused, stop when unfocused
  useFocusEffect(
    useCallback(() => {
      setPollingInterval(5000)
      return () => setPollingInterval(0)
    }, [])
  )
  
  const { data } = useGetVitalsQuery(patientId, {
    pollingInterval,
    skip: !pollingInterval
  })
}
```

## Error Message Interpretation

When you share error messages or stack traces, the skill uses this analysis framework:

### React Native Errors

**"Invariant Violation: Could not find 'store'"**
- Missing Redux Provider or Provider is below component in tree
- Check `App.tsx` Provider hierarchy

**"Can't perform a React state update on an unmounted component"**
- Async operation completing after navigation away
- Need cleanup in `useEffect` return function

**"Maximum update depth exceeded"**
- State update in render causing infinite loop
- Usually from `setState` in component body instead of effect/handler

**"ViewPropTypes will be removed from React Native"**
- Deprecated dependency using old API
- Update the library or find alternative

### RTK Query Errors

**"Cannot read property 'data' of undefined"**
- Query hook called conditionally or in wrong order
- Violates Rules of Hooks

**"No cache entry found"**
- Query hasn't run yet, but code assumes data exists
- Add loading state check or provide default value

### Platform-Specific Errors

**Android: "Unable to resolve module"**
- Metro bundler cache issue
- Clear with: `npx expo start -c`

**iOS: "Invariant Violation: 'main' has not been registered"**
- App bundle not built correctly
- Rebuild iOS: `npx expo run:ios`

## Output Format

### Quick Debugging Response

For straightforward bugs with clear fixes:

```
Root Cause: [One-sentence description of what's causing the bug]

What's Happening: [2-3 sentence explanation of the execution flow]

Why It Fails in React Native: [Explain RN-specific constraints if applicable]

Fix:
[Code snippet showing the change]

Why This Works: [Explain how the fix addresses the root cause]

Prevention: [Brief guidance on avoiding similar issues]
```

### Structured Debugging Response

For complex bugs requiring investigation:

```
Investigation Summary:
[Brief overview of what you investigated]

Root Cause Analysis:
[Detailed explanation of what's causing the bug and why]

React Native Context:
[Explain any RN-specific constraints or platform differences]

Solution:
[Code snippets with clear before/after comparison]

Verification:
[How to test that the fix works correctly]

Related Considerations:
[Other potential issues this fix might affect]

Refactoring Recommendation (if applicable):
[Whether this code would benefit from broader improvements]
```

### Refactoring Handoff

When recommending the Refactoring Skill:

```
Bug Status: ✓ Fixed

The immediate issue is resolved—[brief summary of what was fixed].

However, I've identified several structural concerns that would benefit from 
refactoring now that the code is working:

[List 2-4 specific refactoring opportunities]

These issues aren't causing bugs right now, but they make the code harder to 
maintain and more prone to future issues. The Refactoring Skill can help address 
these systematically.

Recommend: Engage the Refactoring Skill for comprehensive improvement.
```

## Collaboration with Refactoring Skill

The Code Review skill and Refactoring Skill work together in a natural workflow:

**Code Review Skill (This Skill):**
- Diagnoses bugs and explains root causes
- Provides minimal fixes to restore functionality
- Identifies when code structure needs improvement
- Hands off to Refactoring Skill for systematic improvements

**Refactoring Skill:**
- Takes working code and improves structure
- Optimizes performance and readability
- Applies modern patterns and best practices
- Returns improved, maintainable code

**Example Collaboration:**

```
User: "My component crashes when I update patient vitals"

Code Review Skill:
→ Investigates the crash
→ Finds it's due to stale closure in useEffect
→ Provides targeted fix with explanation
→ Notes the component also has nested conditionals and suboptimal loops
→ Recommends: "Bug is fixed. Consider refactoring for better maintainability."

User: "Yes, let's refactor"

Refactoring Skill:
→ Takes the now-working code
→ Simplifies nested conditionals with ts-pattern
→ Optimizes loop with proper memoization
→ Improves RTK Query usage with selectFromResult
→ Returns clean, maintainable code
```

## Key Principles to Remember

**Simplicity is a Feature, Not a Limitation:**
Code complexity should only exist when it solves a problem that simple code cannot. Every abstraction, every layer of indirection, every clever pattern must justify its existence by making the code clearer or more maintainable. If a straightforward approach works, use it. Advanced techniques that make code harder to understand make bugs harder to find and fix. In a healthcare application, clarity is a safety feature.

**Always Explain the "Why":**
Don't just say "change X to Y." Explain why X causes the problem and why Y solves it. Build understanding, not just fixes.

**React Native is Not Web:**
Always check if a pattern relies on web-only APIs, browser behavior, or DOM manipulation. Explain what React Native provides instead.

**Project Patterns are Intentional:**
Refer to Copilot Instructions for project-specific decisions. Don't flag intentional patterns as bugs (like `.then()` without `.catch()` for RTK Query).

**Minimal Fixes First:**
Don't combine bug fixes with refactoring. Get the code working, then assess if broader improvements are needed.

**Teach Through Debugging:**
Every bug is a learning opportunity. Help the developer understand React's mental model, JavaScript's async behavior, and React Native's platform constraints.

**Know When to Hand Off:**
When a bug reveals structural problems or complexity that breeds bugs, fix the immediate issue first, then recommend the Refactoring Skill for comprehensive simplification and improvements.