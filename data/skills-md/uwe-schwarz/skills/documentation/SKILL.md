---
name: documentation
description: Automated documentation generation and management. Use for creating, updating, and maintaining project documentation including README files, API docs, and inline code comments.
license: MIT
metadata:
  author: your-name
  version: "1.0.0"
---

# Documentation Skill

Automated documentation generation and management guidelines.

## When to Apply

Use these guidelines when:
- Creating new documentation
- Updating existing docs
- Documenting APIs
- Adding inline comments
- Maintaining README files

## Documentation Types

### 1. README Files

Every project should have a README.md with:
- Project title and description
- Installation instructions
- Usage examples
- Contributing guidelines
- License information

### 2. API Documentation

Document all public APIs with:
- Function signatures
- Parameter descriptions
- Return value types
- Usage examples
- Error conditions

### 3. Code Comments

Add comments for:
- Complex algorithms
- Non-obvious logic
- Workarounds and hacks
- TODO/FIXME items
- Performance considerations

### 4. Inline Documentation

Use JSDoc/Docstring style:
```javascript
/**
 * Calculate the factorial of a number
 * @param {number} n - The number to calculate factorial for
 * @returns {number} The factorial of n
 * @throws {Error} If n is negative
 */
function factorial(n) {
  if (n < 0) throw new Error('Negative input');
  if (n === 0) return 1;
  return n * factorial(n - 1);
}
```

## Documentation Standards

### Style Guidelines

- Use clear, concise language
- Write in present tense
- Use active voice
- Avoid jargon when possible
- Include examples

### Formatting

- Use markdown for docs
- Consistent heading levels
- Code blocks for examples
- Links to related resources
- Tables for structured data

### Versioning

- Document breaking changes
- Maintain changelog
- Tag documentation versions
- Reference specific versions

## Automation

Use scripts in `scripts/` directory to:
- Generate API documentation
- Validate documentation coverage
- Check for outdated docs
- Format documentation

## Best Practices

- Keep docs up to date with code
- Write docs for future maintainers
- Include both high-level and detailed info
- Use diagrams for complex systems
- Provide troubleshooting sections
