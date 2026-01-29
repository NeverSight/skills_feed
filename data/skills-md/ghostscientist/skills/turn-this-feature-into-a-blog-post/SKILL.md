---
name: turn-this-feature-into-a-blog-post
description: Generates a technical blog post from code implementation. Use when asked to write a blog post about a feature, explain an implementation for a blog, document code as a blog article, or create technical content from source code. Triggers on phrases like "write a blog post about", "turn this into a blog", "create a technical article", or "explain this for a blog".
---

# Turn This Feature Into a Blog Post

Generate a Markdown blog post that explains a code implementation in an engaging, educational way.

## Process

1. **Analyze the implementation** - Read and understand all relevant code files, tracing the feature from entry point to completion
2. **Identify the narrative** - Find the core problem being solved and why it matters
3. **Structure the post** - Organize as What → Why → How (from first principles)
4. **Write accessibly** - Use friendly, conversational language while maintaining technical authority
5. **Output Markdown** - Create a complete `.md` file ready for publishing

## Blog Post Structure

### Title
- Clear, specific, and searchable
- Format: "How We Built [Feature]" or "Building [Feature]: A Deep Dive"

### Introduction (2-3 paragraphs)
- Hook the reader with the problem or outcome
- Briefly explain what the feature does
- Preview what readers will learn

### The What (1-2 sections)
- Describe the feature from the user's perspective
- Include screenshots or diagrams if applicable
- Keep technical jargon minimal

### The Why (1-2 sections)
- Explain the problem this solves
- Discuss alternatives considered and why this approach won
- Connect to broader engineering principles

### The How (2-4 sections)
- Walk through the implementation from first principles
- Include relevant code snippets with explanations
- Explain non-obvious decisions
- Build up complexity gradually

### Conclusion
- Summarize key takeaways
- Mention potential future improvements
- Invite engagement (questions, feedback)

## Writing Style

- **Friendly but authoritative** - Write like a knowledgeable colleague explaining over coffee
- **First-person plural** - Use "we" to create shared ownership
- **Active voice** - "We built" not "It was built"
- **Show, don't just tell** - Use code examples liberally
- **Explain the "why"** - Every code block should have context
- **Avoid jargon walls** - Define terms on first use

## Code Snippets

- Include only relevant portions, not entire files
- Add comments for non-obvious lines
- Use syntax highlighting with language tags
- Provide context before each snippet

## Output

Save the blog post as a Markdown file with:
- Kebab-case filename matching the title
- Frontmatter with title, date, author, and tags (if appropriate for the target platform)
- Properly formatted headers, code blocks, and lists
