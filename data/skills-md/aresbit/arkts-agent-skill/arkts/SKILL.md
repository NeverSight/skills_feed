---
name: arkts
description: ArkTS Language Specification. ArkTS is a statically-typed programming language developed by Huawei for HarmonyOS, extending TypeScript with features from Java and Kotlin. Use for ArkTS syntax, types, classes, functions, and language features.
---

# Arkts Skill

Comprehensive assistance with arkts development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with arkts
- Asking about arkts features or APIs
- Implementing arkts solutions
- Debugging arkts code
- Learning arkts best practices

## Quick Reference

### Common Patterns

**Pattern 1:** Parentheses in types (where a type is a combination of array, function, or union types) are used to specify the required type structure. Without parentheses, the symbol ‘|’ that constructs a union type has the lowest precedence as presented in the following example:

```
|
```

**Pattern 2:** A compile-time error occurs if typeReference is not a class or interface type. The semantics of the keyof type is presented in the following example:

```
1 class A {
2    field: number
3    method() {}
4 }
5 type KeysOfA = keyof A // "field" | "method"
6 let a_keys: KeysOfA = "field" // OK
7 a_keys = "any string different from field or method"
8   // Compile-time error: invalid value for the type KeysOfA
```

### Example Code Patterns

**Example 1** (javascript):
```javascript
1 let b: boolean  // using primitive value type name
2 let n: number   // using primitive value type name
3 let o: Object   // using predefined class type name
4 let a: number[] // using array type
```

**Example 2** (javascript):
```javascript
1 let b: boolean  // using primitive value type name
2 let n: number   // using primitive value type name
3 let o: Object   // using predefined class type name
4 let a: number[] // using array type
```

**Example 3** (javascript):
```javascript
1 let b: boolean  // using primitive value type name
2 let n: number   // using primitive value type name
3 let o: Object   // using predefined class type name
4 let a: number[] // using array type
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **introduction.md** - Introduction documentation
- **language_basics.md** - Language Basics documentation
- **modules.md** - Modules documentation
- **other.md** - Other documentation
- **type_system.md** - Type System documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
