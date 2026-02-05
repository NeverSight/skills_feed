---
name: liberal-accept-strict-return
description: Use when designing function signatures. Use when creating APIs. Use when parameters have optional fields but return types feel too broad.
---

# Be Liberal in What You Accept and Strict in What You Produce

## Overview

**Accept broad input types, return narrow output types.**

This is Postel's Law applied to TypeScript: functions should be flexible about what they accept but precise about what they return. This makes APIs easier to use and types more useful.

## When to Use This Skill

- Designing function parameters and return types
- Creating reusable APIs or libraries
- Function returns feel too broad for callers to use
- Want to accept multiple input formats
- Struggling with optional fields that shouldn't be optional in output

## The Iron Rule

```
ALWAYS make input types broader than output types.
```

**Remember:**
- Parameters: optional fields, union types, multiple formats OK
- Return types: required fields, specific types, single format
- Input flexibility helps callers
- Output precision helps consumers

## Detection: The "Too Broad Return" Problem

If callers have to do extra work to use your function's return value, your return type is too broad:

```typescript
// ❌ Return type is as broad as input type
declare function viewportForBounds(bounds: LngLatBounds): CameraOptions;

function focusOnFeature(f: Feature) {
  const camera = viewportForBounds(calculateBoundingBox(f));
  const {center: {lat, lng}, zoom} = camera;
  //             ~~~  Property 'lat' does not exist on type 'LngLat | undefined'
  //             ~~~  Property 'lng' does not exist on type 'LngLat | undefined'
  zoom;
  // ^? const zoom: number | undefined
}
```

## The Postel's Law Pattern

### Broad Input Types

```typescript
// Accept multiple formats for convenience
type LngLat =
  | { lng: number; lat: number }
  | { lon: number; lat: number }
  | [number, number];

type LngLatBounds =
  | { northeast: LngLat; southwest: LngLat }
  | [LngLat, LngLat]
  | [number, number, number, number];

// Input: Many ways to specify bounds
declare function setCamera(camera: CameraOptions): void;
```

### Strict Output Types

```typescript
// Return a single, precise format
interface Camera {
  center: { lng: number; lat: number };  // Not optional, not union
  zoom: number;                           // Not optional
  bearing: number;
  pitch: number;
}

// Output: One clear format
declare function viewportForBounds(bounds: LngLatBounds): Camera;
```

## Complete Example

```typescript
// LIBERAL INPUT: Accept many formats
interface CameraOptions {
  center?: LngLat;      // Optional
  zoom?: number;        // Optional
  bearing?: number;     // Optional  
  pitch?: number;       // Optional
}

// STRICT OUTPUT: Return precise types
interface Camera {
  center: { lng: number; lat: number };  // Required, canonical format
  zoom: number;                           // Required
  bearing: number;                        // Required
  pitch: number;                          // Required
}

declare function setCamera(camera: CameraOptions): void;      // Liberal input
declare function viewportForBounds(bounds: LngLatBounds): Camera;  // Strict output
```

Now callers can use the output directly:

```typescript
function focusOnFeature(f: Feature) {
  const camera = viewportForBounds(calculateBoundingBox(f));
  setCamera(camera);  // Works! Camera is assignable to CameraOptions
  
  const {center: {lat, lng}, zoom} = camera;  // No errors!
  window.location.search = `?v=@${lat},${lng}z${zoom}`;
}
```

## Why This Works

Broader types are subtypes of narrower types (see types-as-sets skill):

```typescript
// Camera (all required) is a SUBTYPE of CameraOptions (all optional)
// So Camera is assignable to CameraOptions

const camera: Camera = viewportForBounds(bounds);
setCamera(camera);  // OK! Camera ⊆ CameraOptions
```

## Applying the Pattern

### For Functions

```typescript
// ❌ Input and output have same optionality
function process(options: Options): Options { ... }

// ✅ Input liberal, output strict
function process(options: Options): ProcessedOptions { ... }
```

### For Classes

```typescript
class DataProcessor {
  // Liberal: accept various formats
  constructor(data: RawData | FormattedData | string) { ... }
  
  // Strict: return precise types
  getResult(): ProcessedResult { ... }
}
```

### For APIs

```typescript
interface CreateUserInput {
  email: string;
  name?: string;           // Optional input
  preferences?: UserPrefs; // Optional input
}

interface User {
  id: string;              // Always present in output
  email: string;
  name: string;            // Defaulted if not provided
  preferences: UserPrefs;  // Defaulted if not provided
  createdAt: Date;         // Added by system
}

function createUser(input: CreateUserInput): User { ... }
```

## Separate Input/Output Types

A common pattern is to have distinct types for input and output:

```typescript
// Input type (liberal)
interface CreatePostInput {
  title: string;
  body: string;
  tags?: string[];
  draft?: boolean;
}

// Output type (strict)
interface Post {
  id: string;
  title: string;
  body: string;
  tags: string[];      // Always present (defaults to [])
  draft: boolean;      // Always present (defaults to false)
  createdAt: Date;
  updatedAt: Date;
}

function createPost(input: CreatePostInput): Post { ... }
```

## Pressure Resistance Protocol

### 1. "Just Use the Same Type"

**Pressure:** "It's simpler to have one type for input and output"

**Response:** It shifts complexity to every caller.

**Action:** Create separate input/output types when they differ.

### 2. "Optional Output Fields Are Fine"

**Pressure:** "Callers can just check for undefined"

**Response:** That's unnecessary work that accumulates.

**Action:** Make output fields required with sensible defaults.

## Red Flags - STOP and Reconsider

- Return types with many optional fields
- Callers doing null checks on return values
- Union return types where one type would suffice
- Input and output types identical despite different needs

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "Same type is simpler" | It makes every call site more complex |
| "DRY means one type" | Input/output types have different purposes |
| "Users can handle optionals" | They shouldn't have to |

## Quick Reference

| Aspect | Input (Parameters) | Output (Returns) |
|--------|-------------------|------------------|
| Optional fields | OK | Avoid |
| Union types | OK | Use sparingly |
| Multiple formats | OK | Single canonical format |
| Undefined values | OK | Avoid |

## The Bottom Line

**Be generous in what you accept, precise in what you return.**

Input types should accommodate callers. Output types should serve consumers. When in doubt, make input optional and output required. This makes your functions easier to call and their results easier to use.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 30: Be Liberal in What You Accept and Strict in What You Produce.
