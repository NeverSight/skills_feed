---
name: plugin-optimization
description: Master plugin performance optimization, best practices, and marketplace readiness. Learn to optimize for speed, efficiency, and user satisfaction.
sasmp_version: "1.3.0"
bonded_agent: 05-plugin-optimizer
bond_type: PRIMARY_BOND
---

# Plugin Optimization

## Quick Start

Optimize your plugin:

```bash
# Get optimization recommendations
/optimize-plugin my-plugin

# Fix issues automatically
/optimize-plugin my-plugin --auto-fix

# Detailed optimization report
/optimize-plugin my-plugin --report
```

## Performance Optimization

### Response Time Targets

```
Agent invocation:     < 1 second
Skill loading:        < 500ms
Command execution:    < 2 seconds
Hook triggering:      < 100ms
Total workflow:       < 5 seconds
```

### Content Optimization

Before:
```markdown
This agent specializes in various aspects of the field,
including many different topics that are related to the
general area of expertise. The agent can help with many
different things such as...
```

After:
```markdown
Specializes in X, Y, Z with focus on ABC.
```

## Best Practices

### Agent Best Practices

```
✅ DO:
  ├─ Focus on single domain
  ├─ Provide 5-10 capabilities
  ├─ Document integrations
  ├─ Use clear language
  └─ Include status/date

❌ DON'T:
  ├─ Mix unrelated topics
  ├─ Create vague descriptions
  ├─ Ignore other agents
  ├─ Use technical jargon
  └─ Skip examples
```

### Skill Best Practices

```
✅ DO:
  ├─ Name lowercase-hyphenated
  ├─ Provide Quick Start code
  ├─ Explain core concepts
  ├─ Include real projects
  └─ Add usage guidelines

❌ DON'T:
  ├─ Use uppercase/underscores
  ├─ Skip working examples
  ├─ Theory only
  ├─ Ignore real-world use
  └─ Leave users confused
```

### Command Best Practices

```
✅ DO:
  ├─ Use verb-noun naming
  ├─ Document all options
  ├─ Show example output
  ├─ Suggest next steps
  └─ Clear error messages

❌ DON'T:
  ├─ Generic names
  ├─ Undocumented flags
  ├─ Missing output examples
  ├─ Leave guessing
  └─ Cryptic errors
```

## File Size Optimization

### Target Sizes

```
Agent files:    250-400 lines
Skill files:    200-300 lines
Command files:  100-150 lines
Total plugin:   < 50KB
```

### Optimization Techniques

```
Trim verbose sections
  → Remove redundant text
  → Link to external resources
  → Use clear headings

Consolidate examples
  → Use concise code
  → Remove verbose comments
  → Focus on essential cases

Organize content
  → Logical sections
  → Clear headings
  → Table formatting
```

## Marketplace Readiness

### Pre-Submission Checklist

```markdown
STRUCTURE ✅
  [✅] plugin.json valid
  [✅] Files exist and referenced
  [✅] Naming conventions followed
  [✅] No broken references

CONTENT ✅
  [✅] README comprehensive
  [✅] Examples working
  [✅] All commands documented
  [✅] Links verified

QUALITY ✅
  [✅] All tests passing
  [✅] No console errors
  [✅] Performance baseline met
  [✅] Error handling complete

STANDARDS ✅
  [✅] YAML frontmatter valid
  [✅] Markdown properly formatted
  [✅] JSON valid syntax
  [✅] No deprecated features
```

## Documentation Optimization

### README Structure

```markdown
# Plugin Name
[One-liner description]

## Features
[Key features]

## Installation
[One-liner install]

## Quick Start
[Get running in 30 seconds]

## Usage
[Command reference]

## Documentation
[Link to detailed docs]

## Contributing
[How to contribute]

## License
[MIT or other]
```

### Code Comments

Before:
```python
# Process the data and return enriched information
result = process_data(input)
```

After:
```python
# Process and return enriched data (Input: raw dict → Output: validated)
result = process_data(input)
```

## Performance Metrics

### Baseline Metrics

```
Load time:          < 500ms ✅
Skill load:         < 300ms ✅
Command response:   < 2s    ✅
Hook trigger:       < 100ms ✅

Test coverage:      > 90%   ✅
Error rate:         < 1%    ✅
Documentation:      100%    ✅
Best practices:     > 95%   ✅
```

### Monitoring

Track:
```
├─ Command usage patterns
├─ Agent popularity
├─ Skill effectiveness
├─ Error occurrence rate
├─ User feedback sentiment
└─ Performance trends
```

## Deployment Optimization

### Release Checklist

```
VERSION & DOCS
  [✅] Version bumped (1.0.0)
  [✅] CHANGELOG updated
  [✅] README updated

QUALITY
  [✅] All tests pass
  [✅] No warnings
  [✅] No console errors
  [✅] Performance ok

CODE
  [✅] All files present
  [✅] References valid
  [✅] Manifest valid
  [✅] Lint passes

DEPLOYMENT
  [✅] Git tagged
  [✅] Changes committed
  [✅] Marketplace ready
  [✅] Monitoring set up
```

## Optimization Priorities

### Critical (Fix Immediately)

```
❌ Broken functionality
❌ Invalid manifest
❌ Missing core features
❌ Security issues
```

### Important (Fix Soon)

```
⚠️  Performance below baseline
⚠️  Incomplete documentation
⚠️  Error handling gaps
⚠️  Unclear UX
```

### Nice-to-Have (Enhance Later)

```
💡 Performance optimization
💡 UX enhancements
💡 Documentation polishing
💡 Code organization
```

## Semantic Versioning

### Version Updates

```
1.0.0 → 1.0.1  (Bug fixes, patches)
1.0.0 → 1.1.0  (New features, backward compatible)
1.0.0 → 2.0.0  (Breaking changes)
```

### Commit Messages

```
feat: Add new command
fix: Correct agent description
docs: Update documentation
refactor: Improve structure
perf: Optimize loading
test: Add tests
```

## Quality Score Calculation

```
Structure:      30% (file org, manifest, naming)
Content:        30% (quality, completeness, clarity)
Functionality:  20% (working, integration, features)
Performance:    10% (speed, size, efficiency)
Documentation:  10% (README, examples, help)

Target: 95%+ for production
```

## Continuous Improvement

### Feedback Loop

```
Deploy
  ↓
Monitor metrics
  ↓
Gather user feedback
  ↓
Identify improvements
  ↓
Update plugin
  ↓
Deploy again
```

### Update Strategy

```
Weekly: Monitor metrics, collect feedback
Monthly: Fix bugs, update docs
Quarterly: Add features, optimize performance
Annually: Major improvements, breaking changes
```

---

**Use this skill when:**
- Optimizing performance
- Preparing for deployment
- Improving quality
- Following best practices
- Before marketplace submission

---

**Status**: ✅ Production Ready | **SASMP**: v1.3.0 | **Bonded Agent**: 05-plugin-optimizer
