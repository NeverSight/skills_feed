---
name: extracting-code-structure
description: Extracts file structure (functions, classes, exports) efficiently without reading entire files, using ast-grep, Dart/Flutter analyzer, ctags, or other language-specific tools to get outlines and signatures. Use this skill when listing all methods, functions, or classes in a file, exploring unfamiliar code, getting API overviews, or deciding what to read selectively
---

# Code Structure Exploration Tools

**Always invoke extracting-code-structure skill to extract file structure - do not execute bash commands directly.**

## Recognizing Structure Questions

**These keywords mean use structure tools, NOT grep/search:**
- "all the methods/functions/classes in..."
- "list of function signatures"
- "what functions/exports/API..."
- "package API" or "module exports"
- "method signatures with receivers" (Dart/Flutter, TypeScript)
- "what's available in..."

**These keywords mean use search (Grep tool or extracting-code-structure skill):**
- "where is X defined"
- "find calls to X"
- "search for pattern Y"

## Before You Choose a Tool

Ask yourself:
1. Am I listing/exploring what exists? → Structure tools
2. Am I finding WHERE something is? → Search tools (Grep or ast-grep)
3. Am I understanding HOW something works? → Read

## When to Get File Outline vs Read

**Get outline/index when:**
- File is large (>500 lines)
- Need to see what's available (functions, classes, exports)
- Exploring unfamiliar code
- Want to decide what to read in detail
- **Saves 90%+ context** vs reading entire file

**Just use Read when:**
- File is small (<500 lines)
- Already know what you're looking for
- Need to understand implementation details
- extracting-code-structure pattern already targets what you need

## Anti-Patterns

**DON'T use grep/rg/Grep tool for:**
- Extracting function/method lists
- Getting API overviews
- Finding all exports/public members
- Getting signatures/interfaces

These are STRUCTURE queries, not SEARCH queries.

## Default Strategy

**Invoke extracting-code-structure skill** for extracting file structure (functions, classes, exports) efficiently without reading entire files.

Use ast-grep patterns, Dart/Flutter analyzer, ctags, or language-specific tools to get outlines and signatures. Dart/Flutter and JavaScript/TypeScript support have highest priority.

## Exploration Strategy

**Tiered approach (try in order):**

1. **ast-grep with known patterns** - Fast, targeted (highest priority)
   - Extract exports, functions, classes with specific patterns
   - See [code structure guide](./reference/code-structure-guide.md) for patterns, including comprehensive Dart/Flutter support

2. **Toolchain-specific approaches** - When available
   - **Dart/Flutter analyzer** - Comprehensive structure extraction for .dart files
     - See [code structure guide](./reference/code-structure-guide.md) for Dart/Flutter patterns
   - **ctags/universal-ctags:** Symbol index across languages
   - See [code structure guide](./reference/code-structure-guide.md) for examples

3. **Read file** - Last resort for exploration
   - Sometimes necessary to understand structure

## Key Principle

**Use structure tools to decide what to read, then read selectively.**

Don't read 1000-line files blind. Get an outline first, then read the 50 lines you actually need.

## Skill Combinations

### For Discovery and Exploration
- **extracting-code-structure → fd**: Find files of a specific type, then get structure
- **extracting-code-structure → ripgrep**: Understand structure, then search for specific patterns
- **extracting-code-structure → analyzing-code-structure**: Get outline, then perform structural refactoring
- **extracting-code-structure → jq/yq**: Understand API structures before extracting data

### In Refactoring Workflows
- **extracting-code-structure → fzf → analyzing-code-structure**: Interactive selection of components to refactor
- **extracting-code-structure → ripgrep → sd**: Find patterns and perform replacements

### For Documentation and Analysis
- **extracting-code-structure → tokei**: Get statistics for specific code components
- **extracting-code-structure → bat**: View structure with syntax highlighting

### Multi-Skill Workflows
- **extracting-code-structure → ripgrep → analyzing-code-structure → bat**: Complete code analysis and refactoring pipeline
- **extracting-code-structure → fd → jq/yq**: Find and analyze configuration structures
- **extracting-code-structure → fzf → sd**: Interactive selection and modification of code elements

### Integration Examples
```bash
# Get structure and find all methods
ast-grep -r 'function $FUNC($$$ARGS) {$$$BODY}' src/ | fzf | cut -d: -f1 | xargs -I {} bat {}

# Understand API and extract usage
yq '.endpoints' api.yml | fzf | ripgrep -A 10 -B 5
```

## Detailed Patterns

For language-specific extraction patterns, ast-grep examples, ctags usage, and integration strategies, load [code structure guide](./reference/code-structure-guide.md) when needing:
- Dart/Flutter specific patterns and analyzer usage
- Language-specific extraction strategies
- ctags configuration and usage
- Comprehensive workflow examples
- Tool selection guidance for different languages
