---
name: changelog-writer
description: Create user-focused, SEO-optimized changelog entries for software releases. Use when writing release notes, version updates, product changelogs, or "what's new" documentation for developer tools.
allowed-tools: Read, Grep, Glob, Write, Edit
---

# Changelog Writer

Create clear, accurate changelog entries that help developers understand what's new in Lightfast releases.

## Critical: Fact-Check First

Before writing anything, verify against `docs/architecture/implementation-status/README.md`:

1. **Check implementation status** to verify:
   - What's actually completed vs planned
   - Current limitations and known gaps
   - Technical accuracy of claims

2. **Never oversell:**
   - Use specific names: "GitHub File Sync (File Contents)" not "GitHub Integration"
   - Disclose limitations: "Currently supports X; Y coming in vZ"
   - Be honest about conditionals: "when 3+ customers request"

3. **Verify every claim:**
   - If you cite a number, confirm it's in implementation docs
   - If you mention a feature, confirm it exists in production
   - When uncertain, ask for clarification

## Writing Guidelines

1. **Concise & scannable**: 1-3 sentences per feature (Cursor-style brevity)
2. **Lead with benefit**: Start with what users can do, then how
3. **Be transparent**: Mention beta status, rollout timelines, limitations
4. **User-focused but technical**: Balance benefits with specifics developers need
5. **Active voice**: "You can now..." not "Users are able to..."
6. **No emoji**: Professional tone
7. **Specific examples**: Include config snippets, API calls
8. **SEO-conscious**: Use target keywords naturally
9. **AEO-conscious**: Write `tldr` for AI citation engines, `excerpt` for listings
10. **FAQ quality**: Questions must match real search queries, answers must be complete

## Workflow

1. **Gather input**: PR numbers, URLs, or manual change list
2. **Read implementation status** for fact-checking
3. **Draft following** [templates](resources/templates.md)
4. **Cross-check claims** against implementation reality
5. **Add SEO elements** per [seo-requirements](resources/seo-requirements.md)
6. **Review with** [checklist](resources/checklist.md)

## Quick Reference

### Do
- "GitHub File Sync (File Contents)" with limitations disclosed
- "When 3+ customers request: Linear integration"
- Include code examples for every major feature
- Link to 3-5 related docs

### Don't
- "GitHub Integration" (vague - what does it cover?)
- "Coming soon: Linear, Notion, Slack!" (when at 0%)
- Long paragraphs (keep to 1-3 sentences per feature)
- Claims without verification

## Output

Save drafts to: `thoughts/changelog/{title-slug}-{YYYYMMDD-HHMMSS}.md`

### Required Frontmatter Fields

Every draft MUST include:
- `title`, `slug`, `publishedAt` (core)
- `excerpt`, `tldr` (AEO)
- `seo.metaDescription`, `seo.focusKeyword` (SEO)
- `_internal.status`, `_internal.source_prs` (traceability)

### Slug Format

Always use: `0-<version>-lightfast-<feature-slug>`

Examples:
- `0-1-lightfast-github-file-sync-semantic-search`
- `0-2-lightfast-pr-metadata-linear-integration`

Recommended:
- `seo.secondaryKeyword`, `seo.faq[]` (enhanced SEO)

The frontmatter structure maps directly to `ChangelogEntryInput` type. Use `/publish_changelog` to publish drafts to BaseHub.

See `resources/templates.md` for complete frontmatter template.

## Resources

- [Document Templates](resources/templates.md)
- [SEO Requirements](resources/seo-requirements.md)
- [Examples](resources/examples.md)
- [Pre-Publish Checklist](resources/checklist.md)
