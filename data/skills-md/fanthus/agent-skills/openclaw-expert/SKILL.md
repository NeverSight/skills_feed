---
name: openclaw-expert
description: OpenClaw learning expert that retrieves and synthesizes information from official documentation (https://docs.openclaw.ai) and GitHub repository (https://github.com/openclaw/openclaw). Use this skill whenever the user asks questions about OpenClaw, including installation, configuration, API usage, concepts, troubleshooting, best practices, or any OpenClaw-related inquiries. Triggers include OpenClaw questions about features, implementation, usage, setup, or any openclaw-related topics.
---

# OpenClaw Learning Expert

This skill helps answer questions about OpenClaw by retrieving information from official documentation and the GitHub repository, then providing comprehensive answers with source links.

## Workflow

When the user asks an OpenClaw-related question:

### Step 1: Identify the Question Type

Categorize the question to determine the best sources:

- **Getting Started/Installation** → Documentation: `/start/getting-started`
- **Concepts/Architecture** → Documentation: `/concepts/` sections
- **API Usage** → Documentation: `/api/` + GitHub examples
- **Configuration** → Documentation: `/guides/configuration`
- **Troubleshooting** → GitHub Issues + Documentation
- **Examples/Implementations** → GitHub `/examples` directory
- **Advanced/Source Code** → GitHub repository source code

### Step 2: Fetch Relevant Documentation

Use `web_fetch` tool to retrieve content from:

1. **Primary source**: Official documentation at https://docs.openclaw.ai/
   - Start with the most relevant documentation page based on the question type
   - Common pages: `/start/getting-started`, `/concepts/`, `/api/`, `/guides/`

2. **Secondary source**: GitHub repository at https://github.com/openclaw/openclaw
   - For code examples, implementation details, or when docs need clarification
   - Check README.md, examples directory, or source code as needed

**Important**: Always fetch the actual pages rather than guessing content, as OpenClaw is actively developed and documentation changes frequently.

### Step 3: Synthesize Information

After retrieving documentation:

1. **Extract relevant information** that answers the user's question
2. **Organize the answer** in a clear, logical structure:
   - Start with a direct answer to the question
   - Provide necessary context or explanation
   - Include code examples if relevant
   - Note any caveats or best practices
3. **Cite sources** by including the specific documentation URLs used

### Step 4: Present the Answer

Format the response as follows:

```markdown
[Direct answer to the question]

[Explanation and details]

[Code examples if applicable]

**Sources:**
- [Specific page title]: [Full URL to the documentation page]
- [Another source if used]: [Full URL]
```

**Example response structure:**

```markdown
OpenClaw uses a declarative configuration approach for defining workflows.

To configure a workflow, you create a YAML file that specifies...

Example:
```yaml
workflow:
  name: example
  steps:
    - action: process
```

**Sources:**
- Getting Started Guide: https://docs.openclaw.ai/start/getting-started
- Configuration Reference: https://docs.openclaw.ai/guides/configuration
```

## Best Practices

1. **Always fetch current documentation** - Don't rely on cached knowledge
2. **Provide specific URLs** - Include the exact page where information was found
3. **Include code examples** - When available in the documentation, include them
4. **Be comprehensive** - Cover edge cases and common pitfalls mentioned in docs
5. **Link to GitHub for implementation** - When users need to see source code or examples
6. **Check multiple sources** - If documentation is unclear, cross-reference with GitHub
7. **Note version information** - If the documentation mentions specific versions, include that context

## Handling Common Scenarios

### Question Not Directly Answered in Docs

1. Search GitHub Issues for similar questions
2. Check GitHub Discussions
3. Examine source code or examples for implementation patterns
4. Provide best available information with caveats

### Multiple Possible Answers

1. Present all relevant approaches found in documentation
2. Note recommended approach if docs specify one
3. Explain trade-offs when applicable

### Outdated or Conflicting Information

1. Prioritize official documentation over GitHub README
2. Note any conflicts found between sources
3. Suggest checking GitHub Issues for latest updates
4. Provide the most recent information available

## Reference Files

- **references/documentation_guide.md** - Overview of documentation structure and search strategies (consult when unsure where to find specific information)

## Tools to Use

- **web_fetch** - Primary tool for retrieving documentation pages
- **web_search** - For finding specific pages or GitHub issues when exact URL is unknown

## Notes

- OpenClaw is actively developed - always fetch fresh documentation
- User's questions may be in Chinese or English - respond in the same language
- Include both Chinese and English technical terms when appropriate
- Always verify URLs work before including in response
