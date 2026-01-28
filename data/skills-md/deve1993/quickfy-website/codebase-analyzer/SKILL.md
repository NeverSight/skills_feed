---
name: codebase-analyzer
description: Analyze codebases for patterns, anti-patterns, code duplication, performance issues, security vulnerabilities, and technical debt. Updated for React 19, Next.js 16.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Codebase Analyzer

Expert skill for comprehensive codebase analysis and quality assessment. Specializes in pattern detection, code duplication, performance optimization, dependency auditing, and automated code review.

## Technology Stack (2025)

### Analysis Tools
- **ESLint 9** - Flat config, React 19 rules
- **TypeScript 5.9** - Type checking
- **Biome** - Fast linting and formatting
- **jscpd** - Copy-paste detection
- **depcheck** - Unused dependencies

### Security
- **npm audit** / **Snyk** - Vulnerability scanning
- **socket.dev** - Supply chain security
- **secretlint** - Secret detection

### Performance
- **Lighthouse** - Web vitals
- **Bundle analyzer** - Size analysis
- **source-map-explorer** - Bundle composition

## Core Capabilities

### 1. Pattern Detection
- React 19 patterns (Server Components, use API)
- Anti-patterns (God components, prop drilling)
- Architectural patterns
- Code smells

### 2. Code Duplication Analysis
- Exact code duplication
- Similar code blocks
- Copy-paste detection
- DRY violations

### 3. Performance Analysis
- React 19 performance patterns
- Server vs Client component usage
- Bundle size optimization
- Core Web Vitals

### 4. Dependency Analysis
- Unused dependencies
- Outdated packages
- Security vulnerabilities
- Circular dependencies

### 5. Code Quality Metrics
- Cyclomatic complexity
- Code coverage
- Maintainability index
- Technical debt

## Analysis Commands

### Quick Analysis Scripts

```bash
# Type checking
npx tsc --noEmit

# Linting with ESLint 9
npx eslint src/ --fix

# Find unused dependencies
npx depcheck

# Security audit
npm audit
npx snyk test

# Find code duplication
npx jscpd src/ --min-lines 5 --format markdown

# Bundle analysis
npm run build && npx source-map-explorer dist/**/*.js

# Outdated packages
npm outdated
```

### ESLint 9 Flat Config
```javascript
// eslint.config.js
import js from '@eslint/js'
import typescript from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'
import react from 'eslint-plugin-react'
import reactHooks from 'eslint-plugin-react-hooks'

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
      '@typescript-eslint': typescript,
      'react': react,
      'react-hooks': reactHooks,
    },
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
        ecmaFeatures: { jsx: true },
      },
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': 'error',
      'complexity': ['warn', { max: 10 }],
      'max-lines-per-function': ['warn', { max: 50 }],
      'max-depth': ['warn', { max: 4 }],
    },
  },
]
```

## Health Report Generator

```typescript
// analyze-codebase.ts
import { glob } from 'glob'
import { readFileSync } from 'fs'

interface HealthReport {
  overview: {
    totalFiles: number
    totalLines: number
    components: number
    serverComponents: number
    clientComponents: number
  }
  quality: {
    typeErrors: number
    lintErrors: number
    complexity: string
    duplication: string
  }
  dependencies: {
    total: number
    outdated: number
    vulnerable: number
    unused: number
  }
  recommendations: Recommendation[]
}

interface Recommendation {
  category: string
  priority: 'high' | 'medium' | 'low'
  issue: string
  solution: string
}

async function analyzeCodebase(): Promise<HealthReport> {
  const files = await glob('src/**/*.{ts,tsx}')

  // Count file types
  const tsxFiles = files.filter(f => f.endsWith('.tsx'))
  const serverComponents = tsxFiles.filter(f => {
    const content = readFileSync(f, 'utf-8')
    return !content.includes("'use client'")
  })
  const clientComponents = tsxFiles.filter(f => {
    const content = readFileSync(f, 'utf-8')
    return content.includes("'use client'")
  })

  // Generate recommendations
  const recommendations: Recommendation[] = []

  if (clientComponents.length > serverComponents.length) {
    recommendations.push({
      category: 'Performance',
      priority: 'medium',
      issue: 'More Client Components than Server Components',
      solution: 'Consider moving data fetching to Server Components',
    })
  }

  return {
    overview: {
      totalFiles: files.length,
      totalLines: files.reduce((acc, f) =>
        acc + readFileSync(f, 'utf-8').split('\n').length, 0
      ),
      components: tsxFiles.length,
      serverComponents: serverComponents.length,
      clientComponents: clientComponents.length,
    },
    quality: {
      typeErrors: 0,
      lintErrors: 0,
      complexity: 'Good',
      duplication: 'Low',
    },
    dependencies: {
      total: 0,
      outdated: 0,
      vulnerable: 0,
      unused: 0,
    },
    recommendations,
  }
}
```

## Anti-Patterns to Detect

### React 19 Anti-Patterns
1. **Unnecessary Client Components**: Using 'use client' when not needed
2. **Missing Suspense**: No loading states for async data
3. **Prop Drilling**: Passing props through many levels
4. **God Components**: Components doing too much
5. **Inline Functions**: Creating functions on every render (less critical with React Compiler)
6. **Missing use API**: Not using new `use` hook for promises/context

### General Anti-Patterns
1. **Magic Numbers**: Hard-coded values
2. **Copy-Paste Code**: Duplicated blocks
3. **Long Functions**: Functions over 50 lines
4. **Deep Nesting**: More than 4 levels
5. **Too Many Parameters**: Functions with 5+ parameters
6. **Tight Coupling**: High dependencies between modules

## Performance Checklist

### React 19 / Next.js 16
- [ ] Server Components for data fetching
- [ ] Client Components only when interactive
- [ ] Proper Suspense boundaries
- [ ] Streaming for large data
- [ ] Proper caching with `cache()`
- [ ] Image optimization with next/image
- [ ] Font optimization with next/font

### Bundle Optimization
- [ ] Tree-shaking enabled
- [ ] Code splitting by route
- [ ] Dynamic imports for heavy components
- [ ] External large dependencies
- [ ] Minification enabled

## Security Checklist

- [ ] No secrets in code
- [ ] Dependencies audited
- [ ] No known vulnerabilities
- [ ] Input sanitization
- [ ] CORS properly configured
- [ ] CSP headers set

## Report Format

```markdown
## Codebase Health Report

### Overview
- Total Files: 150
- Lines of Code: 12,500
- Components: 45
  - Server Components: 30 (67%)
  - Client Components: 15 (33%)

### Quality Metrics
- TypeScript Errors: 0
- ESLint Warnings: 12
- Test Coverage: 85%
- Complexity Score: Good

### Dependencies
- Total: 25
- Outdated: 3
- Vulnerabilities: 0
- Unused: 2

### Recommendations

#### High Priority
1. **Security**: Update lodash to fix CVE-2024-xxxx
2. **Performance**: Add Suspense boundaries

#### Medium Priority
1. **Code Quality**: Refactor UserProfile (300+ LOC)
2. **Dependencies**: Remove unused `moment`

#### Low Priority
1. **Style**: Consistent naming conventions
```

## When to Use This Skill

Activate when you need to:
- Analyze codebase quality
- Find performance bottlenecks
- Detect code duplication
- Audit dependencies
- Review architectural patterns
- Identify technical debt
- Prepare for refactoring
- Security audit

## Output Format

Provide:
1. **Executive Summary**: Key findings
2. **Detailed Analysis**: By category
3. **Metrics Dashboard**: Visual health indicators
4. **Recommendations**: Prioritized action items
5. **Implementation Plan**: Steps to fix issues
