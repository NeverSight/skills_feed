---
name: code-dedup
description: Comprehensive code analysis for duplicate detection, dead code elimination, and structure optimization
---

# Code Dedup

An AI-friendly code analysis platform that detects duplicate code, identifies dead code, and suggests structural improvements.

## Use Cases

- **Code Review**: Automatically find duplicate code patterns during PR reviews
- **Refactoring**: Identify unused functions and variables before cleanup
- **Quality Gates**: Integrate into CI/CD to enforce code quality standards
- **Technical Debt**: Track and prioritize code quality improvements
- **Code Audit**: Analyze large codebases for maintainability issues

## Installation

```bash
npm install
```

## Usage

### Analyze a Project

```bash
# Run all analyses
node src/cli.js analyze ./src

# Run specific analysis
node src/cli.js analyze ./src --analyses dedup,deadCode

# Generate JSON report for AI processing
node src/cli.js analyze ./src --format json --output report.json
```

### Programmatic API

```javascript
import { analyzeCode, checkDuplicates, checkDeadCode, checkStructure } from './index.js';

// Comprehensive analysis
const result = await analyzeCode('./src', {
  analyses: ['dedup', 'deadCode', 'structure'],
  format: 'json'
});

console.log(result.summary);
// { status: 'success', filesAnalyzed: 42, issuesFound: 15, durationMs: 234 }

// Individual checks
const duplicates = await checkDuplicates('./src', {
  minSimilarity: 0.85
});

const deadCode = await checkDeadCode('./src', {
  ignoreExports: true,
  ignoreTestFiles: true
});

const structure = await checkStructure('./src', {
  maxComplexity: 10,
  maxFunctionLength: 50
});
```

## Output Format

### JSON Output

```json
{
  "summary": {
    "status": "success",
    "filesAnalyzed": 42,
    "issuesFound": 15,
    "durationMs": 234
  },
  "results": {
    "duplicates": [
      {
        "file1": "src/auth.js",
        "file2": "src/user.js",
        "similarity": 0.92,
        "type": "approximate",
        "lines": 45
      }
    ],
    "deadCode": [
      {
        "symbol": "unusedFunction",
        "file": "src/utils.js",
        "line": 23,
        "type": "function"
      }
    ],
    "structure": {
      "complexFunctions": [
        {
          "name": "processData",
          "file": "src/api.js",
          "complexity": 15,
          "line": 45
        }
      ]
    }
  },
  "recommendations": [
    {
      "type": "refactor",
      "priority": "high",
      "description": "Extract duplicate validation logic",
      "files": ["src/auth.js", "src/user.js"]
    }
  ]
}
```

## Configuration

### Duplicate Detection

- `minLines`: Minimum lines for duplicate detection (default: 5)
- `minSimilarity`: Similarity threshold 0-1 (default: 0.85)
- `ignoreWhitespace`: Ignore whitespace differences (default: true)
- `ignoreComments`: Ignore comments (default: true)

### Dead Code Detection

- `ignoreExports`: Ignore exported symbols (default: true)
- `ignoreTestFiles`: Ignore test files (default: true)
- `testPatterns`: Custom test file patterns (default: ['**/*.test.js', '**/*.spec.js'])
- `whitelistPatterns`: Symbol patterns to ignore (default: [])

### Structure Analysis

- `maxComplexity`: Max cyclomatic complexity (default: 10)
- `maxFunctionLength`: Max function lines (default: 50)
- `maxParameters`: Max function parameters (default: 5)
- `maxNestingDepth`: Max nesting depth (default: 4)

## CLI Commands

```bash
# Analyze with custom options
node src/cli.js analyze ./src \
  --min-similarity 0.9 \
  --max-complexity 8 \
  --format json \
  --output report.json

# Quick duplicate check
node src/cli.js check-dup ./src

# Quick dead code check
node src/cli.js check-dead ./src

# Quick structure check
node src/cli.js check-struct ./src

# Format code
node src/cli.js format ./src --output formatted.md
```

## Features

### O(n) Duplicate Detection

Uses MinHash LSH algorithm for fast approximate duplicate detection:
- **Exact matching**: MD5 hashing for identical code blocks
- **Approximate matching**: MinHash + LSH for similar code (Type-2 clones)
- **Scalable**: Analyzes 1000+ files in seconds, not minutes

### AST-Based Dead Code Detection

Static analysis to find unused code:
- Detects unused functions, variables, and imports
- Builds reference graph to track symbol usage
- Configurable whitelist patterns
- Smart export/test file filtering

### Structure Metrics

Code complexity and maintainability analysis:
- **Cyclomatic complexity**: Decision points per function
- **Function length**: Lines of code per function
- **Nesting depth**: Maximum indentation levels
- **Parameter count**: Number of function parameters

## Performance

| Project Size | Files | Duration |
|--------------|-------|----------|
| Small        | <100  | <2s      |
| Medium       | 100-1K| <10s     |
| Large        | >1K   | <30s     |

## Supported Languages

- JavaScript (ES6+)
- TypeScript
- JSX/TSX
- Python (experimental)

## Examples

### Find High-Similarity Duplicates

```javascript
const duplicates = await checkDuplicates('./src', {
  minSimilarity: 0.95  // Only near-duplicates
});

duplicates.forEach(dup => {
  console.log(`${dup.file1} ↔ ${dup.file2}: ${dup.similarity * 100}%`);
});
```

### Find Unused Exports

```javascript
const deadCode = await checkDeadCode('./src', {
  ignoreExports: false  // Include exports in analysis
});

const unusedExports = deadCode.filter(item => item.exported);
console.log(`Found ${unusedExports.length} unused exports`);
```

### Enforce Complexity Limits

```javascript
const structure = await checkStructure('./src', {
  maxComplexity: 8,
  maxFunctionLength: 30
});

const violations = structure.complexFunctions.filter(
  fn => fn.complexity > 8 || fn.length > 30
);

if (violations.length > 0) {
  console.error('Complexity violations found:', violations);
  process.exit(1);
}
```

## Integration

### CI/CD Pipeline

```yaml
# .github/workflows/code-quality.yml
- name: Check code quality
  run: |
    node src/cli.js analyze ./src --format json --output report.json
    if [ $(jq '.issuesFound' report.json) -gt 0 ]; then
      echo "Code quality issues found"
      exit 1
    fi
```

### Pre-commit Hook

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "node src/cli.js analyze ./src --format json"
    }
  }
}
```

## Tips

1. **Start with defaults**: The default settings work well for most projects
2. **Adjust thresholds**: Tighten similarity thresholds to reduce false positives
3. **Use whitelist**: Add framework patterns to avoid false positives
4. **Regular analysis**: Run weekly to track technical debt
5. **Combine with formatters**: Use with Prettier/ESLint for best results

## Limitations

- **Static analysis**: May miss dynamically accessed code
- **Best effort**: Dead code detection has ~90% accuracy
- **Language support**: Currently optimized for JavaScript/TypeScript
- **Large files**: Files >10MB are skipped for performance
