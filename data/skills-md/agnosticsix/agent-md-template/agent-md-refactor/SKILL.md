---
name: agent-md-refactor
description: Refactor bloated AGENTS.md, CLAUDE.md, or similar agent instruction files to follow progressive disclosure principles. Splits monolithic files into organized, linked documentation. Use when (1) agent context files are too large or unwieldy, (2) need to separate project context from executable skills, (3) want to create modular documentation structure, (4) refactoring existing documentation for better organization, or (5) creating new agent context documentation from scratch.
---

# Agent Context Documentation - Refactor & Template

This skill helps you refactor large, monolithic agent instruction files (AGENTS.md, CLAUDE.md, etc.) into a well-structured, modular documentation system following progressive disclosure principles.

## What This Skill Does

1. **Analyzes** existing agent instruction files to identify areas for improvement
2. **Separates** project context (AGENTS.md) from executable capabilities (SKILLS.md)
3. **Generates** structured templates for both documentation types
4. **Creates** comprehensive documentation for frontend and backend projects
5. **Establishes** clear separation of concerns between "what the project is" and "what the agent can do"

## When to Use This Skill

Use this skill when you encounter:
- Large AGENTS.md or CLAUDE.md files (>1000 lines) that are hard to navigate
- Mixed content (context + procedures) in a single file
- Need to document a new project for AI agents
- Want to create reusable documentation templates
- Setting up agent context for team collaboration
- Converting README-style docs to agent-optimized format

## Documentation Structure

This skill creates a two-file system:

### AGENTS.md (Project Context)
**Purpose**: Defines WHAT the project is and HOW it's structured

**Contains**:
- ✅ Project identification and tech stack
- ✅ Architecture and SOLID principles
- ✅ Layer structure and design patterns
- ✅ Data domain and entities
- ✅ Code conventions and naming
- ✅ Configuration and environment variables
- ✅ Critical rules and constraints
- ✅ Cross-references to SKILLS.md

**Does NOT contain**:
- ❌ Step-by-step procedures
- ❌ Command execution examples
- ❌ Detailed task checklists

### SKILLS.md (Agent Capabilities)
**Purpose**: Defines WHAT the agent CAN DO and HOW to execute tasks

**Contains**:
- ✅ Backend skills (Database, API, Business Logic, Testing, etc.)
- ✅ Frontend skills (Components, State, Routing, Forms, UI/UX, etc.)
- ✅ Transversal skills (Auth, Error Handling, Config, etc.)
- ✅ Step-by-step procedures
- ✅ Command quick reference
- ✅ Code examples and templates
- ✅ Verification checklists
- ✅ Skill matrix for quick lookup

**Does NOT contain**:
- ❌ Project-specific architecture details
- ❌ Entity relationships and schemas
- ❌ Environment configuration

## Templates Provided

This skill includes three template files:

1. **AGENTS_TEMPLATE.md** - Comprehensive template for project context
2. **SKILLS_TEMPLATE.md** - Comprehensive template for agent capabilities  
3. **SKILL.md** (this file) - Skill registration for skills.sh

## Basic Skills Coverage

### Backend Projects
- Database Management (migrations, queries, optimization)
- API Development (REST/GraphQL endpoints)
- Business Logic Implementation
- Integration & External Services
- Testing & Quality Assurance
- Performance Optimization

### Frontend Projects
- Component Development
- State Management
- API Integration & Data Fetching
- Routing & Navigation
- Form Handling & Validation
- UI/UX & Styling
- Performance & Optimization

### Transversal (Both)
- Authentication & Authorization
- Error Handling
- Configuration Management

## Usage Examples

### Example 1: Refactor Existing Documentation
```
User: "My AGENTS.md is 2000 lines and hard to navigate. Can you refactor it?"
Agent: [Uses this skill to split into AGENTS.md + SKILLS.md]
```

### Example 2: Create Documentation for New Project
```
User: "I have a new Next.js + FastAPI project. Create agent documentation."
Agent: [Uses templates to generate both files with appropriate frontend/backend skills]
```

### Example 3: Add Skills to Existing AGENTS.md
```
User: "I have AGENTS.md but need to document procedures. Add a SKILLS.md file."
Agent: [Generates SKILLS.md complementing existing AGENTS.md]
```

## Key Principles

### Progressive Disclosure
- Start with essential information
- Link to detailed procedures when needed
- Avoid overwhelming with all details upfront

### Separation of Concerns
- **Context** (AGENTS.md): Describes the "shape" of the code
- **Capabilities** (SKILLS.md): Describes how to work with the code

### Cross-Referencing
- Both files reference each other
- No information duplication
- Clear navigation between related concepts

### Technology Agnostic
- Templates work for any language/framework
- Sections can be customized or removed
- Extensible for project-specific needs

## Customization

When generating documentation from templates:

1. **Analyze the project** thoroughly (package.json, pom.xml, etc.)
2. **Determine project type** (Backend, Frontend, Fullstack, CLI, Library)
3. **Select relevant sections** - remove what doesn't apply
4. **Add project-specific sections** as needed
5. **Include real code examples** from the actual project
6. **Verify all commands** actually work
7. **Remove template comments** and instructions
8. **Update cross-references** between files

## Best Practices

### For AGENTS.md
- Be specific about versions and tools
- Include real examples from the project
- Document actual conventions observed in code
- List all critical rules that must never be violated
- Reference SKILLS.md for procedural details

### For SKILLS.md
- Focus on actionable procedures
- Include verified commands that work
- Provide code examples that can be copied
- Add verification checklists
- Reference AGENTS.md for context

### Integration
- Ensure consistency between both files
- Use same terminology
- Keep cross-references updated
- Avoid duplication - each piece of info in one place only

## File Structure Output

After using this skill, you'll have:

```
project-root/
├── AGENTS.md           # Project context and structure
├── SKILLS.md           # Agent capabilities and procedures
├── README.md           # (existing) Human-readable documentation
└── [project files...]
```

## Verification Checklist

After generating documentation, verify:

- [ ] AGENTS.md covers project context comprehensively
- [ ] SKILLS.md includes all relevant procedures
- [ ] No information duplication between files
- [ ] Cross-references work correctly
- [ ] All code examples are from the actual project
- [ ] All commands have been tested and work
- [ ] Template comments and instructions removed
- [ ] Sections not applicable to project removed
- [ ] Project-specific sections added where needed
- [ ] Both files use consistent terminology

## Advanced Features

### Skill Matrix
SKILLS.md includes a skill matrix table for quick reference of what skill to use for each task type.

### Quick Reference
Command quick reference sections for common operations without scrolling through procedures.

### Categorized Skills
Skills organized by domain (Database, API, UI, etc.) for easy navigation.

### Standard Procedures
Reusable procedures for common tasks:
- Adding new features
- Debugging problems
- Refactoring code

## Maintenance

Keep documentation updated when:
- Architecture changes
- New technologies are adopted
- Coding conventions evolve
- New common procedures are established
- Critical rules are added or modified

## Resources

This skill provides:
- `AGENTS_TEMPLATE.md` - Template for project context
- `SKILLS_TEMPLATE.md` - Template for agent capabilities
- Comprehensive examples for both frontend and backend
- SOLID principles guidance
- Clean Architecture patterns

## Output Format

Generated files use:
- ✅ Markdown with proper formatting
- ✅ Emojis for section headers (better visual scanning)
- ✅ Code blocks with syntax highlighting
- ✅ Tables for structured data
- ✅ Checklists for verification
- ✅ Cross-references as markdown links

## Tips for AI Agents

When using this skill:

1. **Read templates first** to understand the structure
2. **Analyze the project thoroughly** before filling templates
3. **Be specific**, not generic - use real project information
4. **Remove inapplicable sections** - not everything fits every project
5. **Add project-specific content** beyond the template
6. **Test commands** before documenting them
7. **Create cross-references** between related sections
8. **Use real code examples** from the project
9. **Follow the separation**: Context in AGENTS.md, Actions in SKILLS.md
10. **Update both files** when making changes to maintain consistency
