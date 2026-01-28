---
name: github-to-skill
description: "Search GitHub repositories and generate Claude Skills from them. Use this skill when users want to create a new skill based on an existing GitHub repository, need to find high-quality libraries for skill development, or want to transform a GitHub project into a reusable Claude capability. Supports repository search, quality filtering, and skill template generation."
---

# GitHub to Skill Creator

Automatically discover GitHub repositories and convert them into Claude Skills.

## Overview

Transforms any GitHub repository into a reusable Claude Skill by:
1. **Searching** GitHub for high-quality, active repositories
2. **Analyzing** repository structure and documentation
3. **Generating** skill templates with proper structure
4. **Packaging** ready-to-use skills

## Workflow Decision Tree

```
User Request
    ↓
Does user have a specific repo in mind?
    ├─ YES → Generate skill template directly
    │         (use generate_skill_template.py)
    │
    └─ NO → Search GitHub first
             1. Ask clarifying questions
             2. Run repository search
             3. Present TOP 5-10 options
             4. User selects repo
             5. Generate skill template
```

## Phase 1: Repository Search & Recommendation

### Step 1: Understand Requirements

Ask the user:
- What functionality do you need?
- Any preferred programming language?
- Specific requirements (license, activity level)?

### Step 2: Search GitHub

Use the search script with appropriate filters:

```bash
# Basic search
python3 scripts/search_github_repos.py "PDF processing"

# With language filter
python3 scripts/search_github_repos.py "image manipulation" --language python

# High quality, recently updated
python3 scripts/search_github_repos.py "REST API" --min-stars 500 --sort updated

# Save results for analysis
python3 scripts/search_github_repos.py "data processing" --output results.json
```

### Step 3: Present Results

Display results in a clear table format:

| # | Repository | Stars | Updated | Language | Description | Recommendation |
|---|-----------|-------|---------|----------|-------------|----------------|
| 1 | [owner/repo](url) | 2500 | 2024-01 | Python | Brief desc | ⭐ High quality, active |

### Quality Criteria

When recommending repositories, ensure:
- ✅ **Active maintenance**: Updated within 6 months
- ✅ **Quality indicators**: 100+ stars, good documentation
- ✅ **Clear API**: Well-defined interfaces and examples
- ✅ **License**: Permissive license (MIT, Apache, BSD)

## Phase 2: Skill Template Generation

### Step 1: Analyze Repository

After user selects a repository:

```bash
# Generate skill template
python3 scripts/generate_skill_template.py owner/repository

# Custom output directory
python3 scripts/generate_skill_template.py owner/repository --output ./skills
```

### Step 2: Review Generated Structure

The generator creates:

```
skill-name/
├── SKILL.md              # Ready to customize
├── scripts/
│   └── example.py        # Starter code
└── references/           # For additional docs
```

### Step 3: Customize the Skill

**Update SKILL.md:**
- Edit frontmatter description (be specific about when to use)
- Replace [TODO] items with actual content
- Add clear usage examples
- Document configuration options

**Implement Core Logic:**
- Write wrapper scripts in `scripts/`
- Handle errors gracefully
- Add logging and user feedback

**Add References:**
- API documentation
- Configuration examples
- Troubleshooting guides

### Step 4: Test & Package

```bash
# Test the skill
# [Manual testing steps]

# Package the skill
cd ../skill-creator
python3 scripts/package_skill.py ../skill-name
```

## Usage Examples

### Example 1: User Knows What They Want

**User:** "Create a skill from pdfplumber repository"

**Action:**
```bash
python3 scripts/generate_skill_template.py jsvine/pdfplumber
```

### Example 2: User Needs Guidance

**User:** "I want to add PDF processing capabilities"

**Action:**
1. Ask: "What type of PDF processing? (extraction, manipulation, form filling)"
2. Search: `python3 scripts/search_github_repos.py "PDF extraction" --language python`
3. Present TOP 5 options with pros/cons
4. Guide selection and generate template

### Example 3: No Suitable Repository Found

**User:** "I need quantum computing simulation"

**Action:**
1. Search reveals limited/old repositories
2. Suggest alternatives:
   - Combine multiple smaller libraries
   - Create from scratch with skill-creator
   - Use web APIs instead

## Best Practices

### Search Strategy

- **Start broad**: Use general terms ("PDF processing")
- **Narrow down**: Add filters (--language, --min-stars)
- **Try variations**: "PDF extract", "PDF parse", "document processing"

### Repository Evaluation

Check these before recommending:
1. **Last commit**: Within 6 months
2. **Issues ratio**: Low open/closed ratio indicates good maintenance
3. **Documentation**: README, examples, API docs
4. **License**: Prefer MIT/Apache for permissive use

### Skill Design Principles

- **Keep it focused**: One primary purpose per skill
- **Minimal dependencies**: Prefer widely-used libraries
- **Clear error messages**: Help users troubleshoot
- **Test thoroughly**: Verify before packaging

## Troubleshooting

**No repositories found**
- Broaden search terms
- Reduce minimum stars threshold
- Try different programming languages

**GitHub API rate limit**
- Create GitHub token: https://github.com/settings/tokens
- Set `GITHUB_TOKEN` environment variable
- Or use `--token` parameter

**Generated skill doesn't work**
- Verify repository has clear API/usage patterns
- Check dependencies are installable
- Review error messages in scripts

## Dependencies

```bash
pip install requests
```

Optional (for GitHub API rate limits):
- GitHub personal access token

## Related Skills

- **skill-creator**: Create skills from scratch
- **pdf-to-ppt**: Example of a generated skill

## Resources

- GitHub Search: https://github.com/search
- GitHub API Docs: https://docs.github.com/en/rest
- Skill Creation Guide: Available in skill-creator references/
