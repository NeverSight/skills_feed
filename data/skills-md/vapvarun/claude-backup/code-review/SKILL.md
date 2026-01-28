---
name: code-review
description: Perform thorough code reviews focusing on security, performance, best practices, and maintainability. Use when reviewing PRs, checking code quality, or auditing existing code.
---

# Code Review

Systematic code review methodology for identifying issues, security vulnerabilities, and optimization opportunities.

## Team Review Guidelines

### Communication Style

When providing review feedback:

1. **Be friendly and constructive**
   - Good: "What do you think about using X here? It might help with Y."
   - Good: "Nice solution! One small suggestion..."
   - Avoid: "This is wrong."
   - Avoid: "You should have done X."

2. **Ask before assuming**
   - Good: "I'm curious about this approach - could you explain the reasoning?"
   - Avoid: "Why didn't you just...?"

3. **Acknowledge good work**
   - "Great catch on the edge case!"
   - "Clean and readable!"
   - "I learned something from this."

### Double Verification Process

Every PR requires TWO passes:

**Pass 1 - Security (Blocking)**
- All security checklist items MUST pass
- Any security issue = Request Changes

**Pass 2 - Quality (Advisory)**
- Standards, performance, maintainability
- These are suggestions, not blockers (unless severe)

## Review Phases

### Phase 1: Preparation

1. **Understand Context**
   - Read PR description and linked issues
   - Understand the feature/fix being implemented
   - Check if there are related changes in other PRs
   - Review the commit history for context

2. **Identify Standards**
   - Check project's coding standards
   - Review existing patterns in the codebase
   - Note any specific requirements (performance, security)

### Phase 2: Systematic Analysis

Work through each category methodically:

## Security Review

### Input Validation

\`\`\`javascript
// BAD: No validation
app.post('/user', (req, res) => {
  db.query(\`SELECT * FROM users WHERE id = \${req.body.id}\`);
});

// GOOD: Parameterized + validated
app.post('/user', (req, res) => {
  const schema = z.object({ id: z.number().positive() });
  const { id } = schema.parse(req.body);
  db.query('SELECT * FROM users WHERE id = ?', [id]);
});
\`\`\`

### Authentication & Authorization

\`\`\`javascript
// BAD: Missing auth check
app.delete('/api/posts/:id', async (req, res) => {
  await Post.findByIdAndDelete(req.params.id);
});

// GOOD: Verify ownership
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  const post = await Post.findById(req.params.id);
  if (post.authorId !== req.user.id && !req.user.isAdmin) {
    return res.status(403).json({ error: 'Forbidden' });
  }
  await post.delete();
});
\`\`\`

### Security Checklist

- [ ] SQL/NoSQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding, CSP headers)
- [ ] CSRF protection in place
- [ ] Sensitive data not logged or exposed
- [ ] API keys/secrets not hardcoded
- [ ] File uploads validated and sanitized
- [ ] Rate limiting on sensitive endpoints
- [ ] Proper error messages (no stack traces in production)

## Performance Review

### N+1 Query Detection

\`\`\`javascript
// BAD: N+1 queries
const posts = await Post.find();
for (const post of posts) {
  const author = await User.findById(post.authorId); // Query per post!
}

// GOOD: Eager loading
const posts = await Post.find().populate('author');
\`\`\`

### Performance Checklist

- [ ] No N+1 queries (use eager loading)
- [ ] Expensive operations cached appropriately
- [ ] Database queries use proper indexes
- [ ] Large datasets paginated
- [ ] Async operations properly awaited
- [ ] No unnecessary re-renders (React)
- [ ] Memory leaks prevented (cleanup handlers)
- [ ] Heavy computations memoized or offloaded

## Code Quality Checklist

- [ ] Clear, descriptive naming conventions
- [ ] Functions are single-purpose (< 30 lines ideal)
- [ ] Cyclomatic complexity reasonable (< 10)
- [ ] No code duplication (DRY principle)
- [ ] Proper error handling throughout
- [ ] Edge cases considered
- [ ] Magic numbers/strings extracted to constants
- [ ] Comments explain "why", not "what"

## Edge Cases Checklist

Always verify these scenarios are handled:

### Data Edge Cases
- [ ] Empty arrays/collections
- [ ] Null or undefined values
- [ ] Zero values (especially in division)
- [ ] Negative numbers where only positive expected
- [ ] Empty strings vs null vs undefined
- [ ] Unicode and special characters in strings

### User Input Edge Cases
- [ ] Missing required fields
- [ ] Fields with only whitespace
- [ ] Duplicate submissions (double-click)
- [ ] Concurrent updates to same resource
- [ ] Invalid date formats
- [ ] Timezone handling
- [ ] File upload with no file selected

### API Edge Cases
- [ ] Network timeout handling
- [ ] Rate limit exceeded responses
- [ ] API returns unexpected data structure
- [ ] Partial success in batch operations
- [ ] Graceful degradation when service unavailable

### WordPress-Specific Edge Cases
- [ ] Post with no featured image
- [ ] User with no display name
- [ ] Taxonomy with no posts
- [ ] Widget in empty sidebar
- [ ] Shortcode with no attributes
- [ ] Multisite subdirectory vs subdomain
- [ ] Translation missing for locale
- [ ] Cron job running during high traffic
- [ ] Option not yet saved (first install)
- [ ] Meta value of 0 vs meta not existing
- [ ] get_post() returning null
- [ ] WP_Query with no results
- [ ] Current user not logged in (ID = 0)

## Language-Specific Checks

### PHP/WordPress

- [ ] Escaping output (esc_html, esc_attr, etc.)
- [ ] Nonces for form submissions
- [ ] Capability checks for actions
- [ ] Prepared statements for queries
- [ ] WordPress coding standards followed
- [ ] Cron hooks: No name collision between cron hook and internal do_action()
- [ ] Cron scheduling: Events scheduled on activation, cleared on deactivation
- [ ] Hook callbacks: No recursive/self-triggering patterns
- [ ] Settings sanitization handles unchecked checkboxes
- [ ] Transient expiration set appropriately
- [ ] Object cache checked before expensive queries
- [ ] REST endpoints have permission_callback
- [ ] AJAX handlers verify nonce and capability

### JavaScript/TypeScript

- [ ] === used instead of ==
- [ ] Proper TypeScript types (no any abuse)
- [ ] async/await error handling
- [ ] No prototype pollution risks
- [ ] ESLint/Prettier rules followed

### React

- [ ] Hooks rules followed
- [ ] Keys provided for lists
- [ ] useEffect dependencies correct
- [ ] No state mutations
- [ ] Proper component composition

## Review Output Format

Structure feedback as:

### Critical Issues (Must Fix)
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration
- Failing tests

### Warnings (Should Fix)
- Performance concerns
- Code maintainability
- Missing error handling

### Suggestions (Nice to Have)
- Refactoring opportunities
- Better naming
- Additional documentation

### Positive Notes
- Good patterns followed
- Clean code
- Thorough testing
