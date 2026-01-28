---
name: pgvector
description: pgvector - PostgreSQL extension for vector similarity search. Use for embedding storage, cosine similarity, IVFFlat indexes, and HNSW indexes.
---

# Pgvector Skill

Comprehensive assistance with pgvector development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with pgvector
- Asking about pgvector features or APIs
- Implementing pgvector solutions
- Debugging pgvector code
- Learning pgvector best practices

## Quick Reference

### Common Patterns

**Pattern 1:** To run an example:

```
cd examples/openai
createdb pgvector_example
dart pub get
dart run example.dart
```

**Pattern 2:** To run an example:

```
cd examples/loading
createdb pgvector_example
cmake -S . -B build
cmake --build build
build/example
```

**Pattern 3:** To run an example:

```
cd examples/openai
createdb pgvector_example
dub run
```

**Pattern 4:** To run an example:

```
cd examples/openai
createdb pgvector_example
sbcl --noinform --non-interactive --load example.lisp
```

**Pattern 5:** To run an example:

```
cd examples/openai
createdb pgvector_example
cmake -S . -B build
cmake --build build
build/example
```

**Pattern 6:** To run an example:

```
cd examples/loading
mix deps.get
createdb pgvector_example
mix run example.exs
```

**Pattern 7:** To run an example:

```
cd examples/openai
createdb pgvector_example
crystal examples/openai/example.cr
```

**Pattern 8:** To run an example:

```
cd examples/Loading
createdb pgvector_example
dotnet run
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **pgvector.md** - Pgvector documentation

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
