---
name: ts-js-relationship
description: Use when confused about TypeScript vs JavaScript. Use when migrating JS to TS. Use when explaining TypeScript to newcomers.
---

# Understand the Relationship Between TypeScript and JavaScript

## Overview

**TypeScript is a superset of JavaScript that adds static types.**

All valid JavaScript is valid TypeScript, but TypeScript adds type annotations and checking. Understanding this relationship is fundamental to using TypeScript effectively.

## When to Use This Skill

- Explaining TypeScript to JavaScript developers
- Migrating a JavaScript codebase
- Confused about what TypeScript adds to JavaScript
- Deciding whether to use TypeScript

## The Iron Rule

```
REMEMBER: TypeScript compiles to JavaScript. Types exist only at compile time.
```

**Key Facts:**
- All JavaScript is syntactically valid TypeScript
- TypeScript adds type annotations (`: string`, `: number`, etc.)
- Types are erased when compiling to JavaScript
- TypeScript catches errors statically, before runtime

## TypeScript as a Superset

```typescript
// This is valid JavaScript AND valid TypeScript:
let city = 'new york city';
console.log(city.toUpperCase());

// This is TypeScript (not valid JavaScript):
function greet(who: string) {
  console.log('Hello', who);
}
```

The `: string` is a type annotation - TypeScript-specific syntax.

## TypeScript Catches Errors Without Running Code

```typescript
let city = 'new york city';
console.log(city.toUppercase());
//              ~~~~~~~~~~~ Property 'toUppercase' does not exist on type
//                          'string'. Did you mean 'toUpperCase'?
```

TypeScript found the bug (typo in method name) without running the code.

## Type Annotations Clarify Intent

Without type annotations, TypeScript guesses:

```typescript
const states = [
  {name: 'Alabama', capitol: 'Montgomery'},  // 'capitol' - typo!
  {name: 'Alaska', capitol: 'Juneau'},
];

for (const state of states) {
  console.log(state.capital);  // TypeScript suggests 'capitol' - wrong!
}
```

With type annotations, TypeScript catches the real error:

```typescript
interface State {
  name: string;
  capital: string;  // Correct spelling
}

const states: State[] = [
  {name: 'Alabama', capitol: 'Montgomery'},
  //               ~~~~~~~ Did you mean to write 'capital'?
];
```

## TypeScript Models JavaScript Runtime Behavior

TypeScript allows quirky JavaScript that works at runtime:

```typescript
const x = 2 + '3';  // OK, result is "23"
const y = '2' + 3;  // OK, result is "23"
```

But flags things likely to be mistakes:

```typescript
const a = null + 7;
//        ~~~~ The value 'null' cannot be used here.

alert('Hello', 'TypeScript');
//             ~~~~~~~~~~~~ Expected 0-1 arguments, but got 2
```

## TypeScript Is Not Sound

Code can pass type checking but still throw at runtime:

```typescript
const names = ['Alice', 'Bob'];
console.log(names[2].toUpperCase());
// No type error, but throws: Cannot read properties of undefined
```

TypeScript assumes array access is within bounds - it isn't always.

## Pressure Resistance Protocol

### 1. "TypeScript Is a Different Language"

**Pressure:** "I'd have to rewrite everything for TypeScript"

**Response:** All your JavaScript is already valid TypeScript.

**Action:** Rename .js to .ts and incrementally add types.

### 2. "Types Are Extra Work"

**Pressure:** "I don't want to annotate everything"

**Response:** TypeScript infers most types. You only annotate what helps.

**Action:** Let inference work, add annotations where they add value.

## Red Flags - STOP and Reconsider

- Thinking types exist at runtime
- Expecting TypeScript to catch all runtime errors
- Avoiding TypeScript because "it's a different language"
- Over-annotating when inference would suffice

## Quick Reference

| JavaScript | TypeScript |
|------------|------------|
| Dynamic types (runtime) | Static types (compile time) |
| No type annotations | Type annotations optional |
| Errors at runtime | Many errors caught before runtime |
| `.js` extension | `.ts` extension |

## The Bottom Line

**TypeScript is JavaScript with types.**

All JavaScript programs are TypeScript programs. TypeScript adds optional type annotations that help catch errors before runtime. Types are erased during compilation - the output is plain JavaScript.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 1: Understand the Relationship Between TypeScript and JavaScript.
