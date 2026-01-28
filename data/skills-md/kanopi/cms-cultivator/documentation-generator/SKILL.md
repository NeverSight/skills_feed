---
name: documentation-generator
description: Automatically generate documentation when user mentions needing API docs, README files, user guides, developer guides, or changelogs. Analyzes code and generates appropriate documentation based on context. Invoke when user mentions "document", "docs", "README", "API documentation", "guide", "changelog", or "how to document".
---

# Documentation Generator

Automatically generate documentation for code, APIs, and projects.

## Philosophy

Good documentation is as critical as good code.

### Core Beliefs

1. **Code Documents What, Docs Explain Why**: Documentation provides context code cannot
2. **Documentation Enables Adoption**: Well-documented code gets used, undocumented code gets replaced
3. **Up-to-Date Beats Comprehensive**: Better to have accurate basics than stale details
4. **Multiple Audiences Need Different Docs**: Users need guides, developers need API references

### Why Documentation Matters

- **Onboarding**: New team members get productive faster
- **Maintenance**: Future developers (including yourself) understand intent
- **Adoption**: Users can actually use your features
- **Professional Quality**: Documentation signals production-ready software

## When to Use This Skill

Activate this skill when the user:
- Says "I need to document this"
- Asks "how do I write docs for this API?"
- Mentions "README", "documentation", or "user guide"
- Shows code and asks "what docs should I write?"
- Says "need API documentation"
- Asks about changelog or release notes
- Mentions "developer guide" or "setup instructions"

## Decision Framework

Before generating documentation, determine:

### What Type of Documentation Is Needed?

1. **API Documentation** - Code interfaces, parameters, return values → PHPDoc/JSDoc
2. **User Guide** - End-user instructions, screenshots → Markdown guide
3. **Developer Documentation** - Setup, architecture, contributing → README + guides
4. **Changelog** - Release notes, version history → Keep a Changelog format
5. **Inline Documentation** - Code comments, function docs → Language-specific format
6. **Documentation Site** - Multi-page documentation with search and navigation → Zensical site

### Who Is the Audience?

- **Developers** - Technical details, code examples, architecture
- **End Users** - Simple language, step-by-step instructions, screenshots
- **Contributors** - Setup instructions, coding standards, PR process
- **Stakeholders** - High-level overview, features, roadmap

### What's the Scope?

- **Single function/class** → Inline PHPDoc/JSDoc
- **Module/component** → Component documentation
- **Feature** → User guide + API docs
- **Entire project** → README + developer guide + API reference
- **Release** → Changelog entry

### What Already Exists?

**Check for**:
- Existing README → Update vs. create new
- Existing API docs → Append vs. regenerate
- CHANGELOG.md → Add new entry vs. create file
- Documentation site → Match existing format

### What Level of Detail?

- **Minimal** - Function signature, brief description → Quick reference
- **Standard** - Parameters, return values, usage example → Full API docs
- **Comprehensive** - Architecture, examples, edge cases, troubleshooting → Complete guide

### Decision Tree

```
User requests documentation
    ↓
Identify documentation type
    ↓
Determine audience (dev/user/contributor)
    ↓
Check for existing docs
    ↓
Assess scope (function/module/project)
    ↓
Generate appropriate documentation
    ↓
Format for platform (CMS-specific if needed)
```

## Workflow

### 1. Determine Documentation Type

**API Documentation** - For code interfaces:
- Functions, methods, classes
- Parameters and return types
- Examples and usage

**README** - For project overview:
- Installation instructions
- Quick start guide
- Features and requirements

**User Guide** - For end users:
- How to use features
- Screenshots and examples
- Troubleshooting

**Developer Guide** - For contributors:
- Architecture overview
- Setup and development
- Coding standards

**Changelog** - For releases:
- Version history
- What changed
- Migration guides

### 2. Analyze the Code/Project

**For API Docs**:
- Scan function signatures
- Identify parameters and return types
- Find existing comments
- Detect dependencies

**For README**:
- Check for package managers (composer.json, package.json)
- Identify framework (Drupal, WordPress, etc.)
- Find entry points and main features

**For Guides**:
- Understand user workflows
- Identify key features
- Note prerequisites

## Documentation Templates

Complete templates are available for reference:

- **[API Documentation Templates](templates/api-docs.md)** - PHPDoc/JSDoc for Drupal & WordPress
- **[README Template](templates/readme.md)** - Complete project README structure
- **[User Guide Template](templates/user-guide.md)** - End-user documentation
- **[Changelog Template](templates/changelog.md)** - Version history (Keep a Changelog format)

Use these templates as starting points, customizing for the specific project needs.

## Documentation Site Generation

For comprehensive documentation sites, use **Zensical** - a modern static site generator from the creators of Material for MkDocs.

### When to Use Zensical

- **Multi-page documentation** - Organize docs across multiple pages
- **Search functionality** - Built-in search for documentation
- **Modern theming** - Professional appearance with customization
- **Navigation** - Organized navigation with sections and subsections
- **GitHub Pages deployment** - Automated deployment via GitHub Actions

### Zensical Setup

**Install:**
```bash
pip install zensical
```

**Create new project:**
```bash
zensical new my-documentation
```

**Configuration (`zensical.toml`):**
```toml
[project]
site_name = "Project Name"
site_description = "Brief description"
site_url = "https://yoursite.github.io/project/"
docs_dir = "docs"
site_dir = "site"

nav = [
  {"Home" = "index.md"},
  {"Getting Started" = [
    "installation.md",
    "quick-start.md"
  ]},
  {"API Reference" = "api/index.md"}
]

[project.theme]
variant = "modern"
```

**Build and serve:**
```bash
# Local preview
zensical serve

# Production build
zensical build --clean
```

**GitHub Actions deployment:**
```yaml
name: Deploy Documentation
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install zensical
      - run: zensical build --clean
      - uses: actions/upload-pages-artifact@v4
        with:
          path: ./site
```

## Generation Strategy

### 1. Gather Information

Ask clarifying questions:
- "What documentation type do you need?"
- "Who is the audience? (developers, end users, admins?)"
- "What specific features should be documented?"

### 2. Analyze Code

For API docs:
- Read function signatures
- Extract existing comments
- Identify dependencies
- Find usage examples

### 3. Structure Document

Follow standard patterns:
- Overview/introduction
- Prerequisites
- Main content (organized logically)
- Examples
- Troubleshooting
- Resources

### 4. Add Examples

Include:
- Code examples
- Screenshots (placeholder references)
- Before/after comparisons
- Common use cases

## Integration with CMS Cultivator

This skill complements the `/docs-generate` slash command:

- **This Skill**: Automatically triggered during conversation
  - "How do I document this function?"
  - "Need docs for this API"
  - Quick single-function documentation

- **`/docs-generate` Command**: Explicit batch generation
  - Generate full project documentation
  - Create comprehensive README
  - Build complete user guides

## Quick Response Patterns

### For API Documentation

When user shows a class or function:

1. Identify the type (Drupal service, WordPress function, JS module)
2. Generate appropriate docblock format
3. Include:
   - Description of purpose
   - Parameter documentation
   - Return type documentation
   - Usage example in @code block
   - Related functions (@see tags)

### For README

When user asks for project documentation:

1. Scan project structure (composer.json, package.json)
2. Identify platform (Drupal/WordPress/standalone)
3. Generate sections in order:
   - Title and description
   - Features list
   - Requirements
   - Installation (Composer first)
   - Quick start example
   - Links to detailed docs

### For User Guides

When user needs end-user documentation:

1. Ask about target audience
2. Identify main workflows
3. Structure with:
   - Overview
   - Prerequisites checklist
   - Step-by-step instructions
   - Screenshots placeholders
   - Troubleshooting section
   - FAQs

### For Changelogs

When user needs version history:

1. Use Keep a Changelog format
2. Categories: Added, Changed, Deprecated, Removed, Fixed, Security
3. Include version numbers and dates
4. Link to GitHub comparisons

## Example Interactions

**Example 1: API documentation**
```
User: "I need to document this service class"
[Shows DataProcessor class]

Skill: "I'll generate API documentation for your DataProcessor service.
I see it has 3 public methods and uses dependency injection.
I'll create docblocks with:
- Class description with usage example
- Constructor documentation
- Method documentation with @param and @return
- @code examples for each method

[Generates documented code following Drupal standards]

This follows Drupal documentation standards. Each method includes
parameter types, return types, and usage examples."
```

**Example 2: README**
```
User: "Need a README for my custom module"

Skill: "I'll create a comprehensive README for your module.
Let me check the project structure...

I see:
- Drupal 10 module
- Composer-based
- Custom services and admin routes

I'll generate a README with:
- Installation via Composer
- Feature list
- Configuration steps
- API usage examples
- Links to extended docs

[Generates README.md]"
```

**Example 3: Changelog Entry**
```
User: "What should I add to CHANGELOG for this release?"

Skill: "Based on your recent commits, I'll generate a changelog entry
following Keep a Changelog format:

## [1.2.0] - 2025-01-15

### Added
- User profile export functionality (#234)
- Bulk operations support

### Changed
- Improved query performance (30% faster)

### Fixed
- Permission check on admin pages (#145)

Would you like me to add this to your CHANGELOG.md?"
```

## Best Practices

1. **Clear and Concise** - Write for your audience's level
2. **Examples** - Always include working code examples
3. **Up to Date** - Document current functionality, not planned features
4. **Structured** - Use consistent headings and format
5. **Searchable** - Include keywords users will search for
6. **Complete** - Cover common use cases and edge cases

## Platform-Specific Guidelines

### Drupal Documentation
- Use PHPDoc format with @param, @return, @throws
- Include @code examples in docblocks
- Document services with usage examples
- Reference related APIs with @see tags
- Follow Drupal API documentation standards

### WordPress Documentation
- Use PHPDoc with @since tags
- Document hooks and filters
- Include usage examples in docblocks
- Reference WordPress functions
- Follow WordPress inline documentation standards

### JavaScript Documentation
- Use JSDoc format
- Document parameters and return types
- Include examples
- Document React components with PropTypes
- Follow project-specific standards (ESDoc, TSDoc)

### Markdown Style for Zensical Documentation

When generating markdown documentation for Zensical sites (like this plugin's documentation), follow these guidelines for proper rendering:

#### Use Headings, Not Bold Lists

**DON'T:**
```markdown
1. **Category Name**
   - Sub-item 1
   - Sub-item 2
```

**DO:**
```markdown
### Category Name

- Sub-item 1
- Sub-item 2
```

#### Use Headings for Section Titles

**DON'T:**
```markdown
**Section Title:**
- Item 1
- Item 2
```

**DO:**
```markdown
#### Section Title

- Item 1
- Item 2
```

#### Heading Hierarchy

- `#` - Document title (once at top)
- `##` - Major sections
- `###` - Subsections
- `####` - Categories, steps, or sub-subsections

#### For Step-by-Step Instructions

**DON'T:**
```markdown
1. **Step Name**: Description
   - Detail 1
   - Detail 2
```

**DO:**
```markdown
#### 1. Step Name

Description

- Detail 1
- Detail 2
```

**Complete style guide:** See [Markdown Style Guide](../docs/reference/markdown-style-guide.md) for full details and examples.

## Resources

- [Write the Docs](https://www.writethedocs.org/)
- [Drupal Documentation Standards](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards)
- [WordPress Inline Documentation Standards](https://developer.wordpress.org/coding-standards/inline-documentation-standards/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
