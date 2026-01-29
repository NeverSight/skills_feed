---
name: changelog
description: Write changelog entries for Hugging Face Hub features. Use when asked to write a changelog, create a changelog entry, or document a new feature/PR for hf.co/changelog. Triggers on "write changelog", "changelog entry", "document this PR/feature for changelog".
---

# Changelog

Write changelog entries for hf.co/changelog that match the existing style.

## Workflow

1. **Identify the change**: Get the PR/branch name or ask the user
2. **Gather context**: Read the PR description and changed files to understand the feature
3. **Write the entry**: Follow the format and patterns below

## Format

```markdown
**[Date in "Mon D, YY" format]**

## [Short Title]

[1-2 paragraphs]
```

## Title Patterns

Keep titles short (2-5 words). Common patterns:
- Noun phrase: "Trending Papers", "GGUF Metadata Editor", "Cleaner Collection URLs"
- Feature location: "JSON Support in the Dataset Viewer", "HuggingChat for Papers"
- Action: "Sort Models by Parameter Count", "Set Default Sorting in the Community Tab"

## Opening Sentence Patterns

Choose based on the type of change:

| Type | Pattern | Example |
|------|---------|---------|
| New user feature | "You can now..." | "You can now sort models by their number of parameters..." |
| Platform addition | "All Hugging Face [X] now include/feature..." | "All Hugging Face Papers now include a built-in assistant..." |
| Specific users | "[Users/Authors/Owners] can now..." | "Repository owners can now set the default sorting..." |
| Page improvement | "[Feature] pages now have..." | "Collection pages now have shorter, cleaner links..." |
| Existing feature | "The [feature] now includes..." | "The Daily Papers page now includes Trending Papers..." |
| Breaking change | "We've renamed/overhauled..." | "We've renamed `huggingface-cli` to `hf`..." |

## Style Rules

- Date: `Mon D, YY` (e.g., "Jan 9, 26")
- 1-2 short paragraphs max
- Link to relevant HF pages: `[Models](https://huggingface.co/models)`
- Use backticks for code/commands: `hf download`
- Mention where feature is available (page, profiles, settings)
- Second paragraph (optional): who it helps, examples, or migration notes
- Stay neutral - no marketing fluff
- Include screenshot recommendation when visual

## Examples

**New feature:**
```markdown
**Jan 22, 26**

## Sort Models by Parameter Size

You can now sort models by their number of parameters on the [Models](https://huggingface.co/models) page and on user and organization profiles. Two new sorting options are available: "Most parameters" and "Least parameters."
```

**Platform-wide addition:**
```markdown
**Jan 7, 26**

## HuggingChat for Papers

All Hugging Face [Papers](https://huggingface.co/papers) now include a built-in assistant, powered by [HuggingChat](https://huggingface.co/chat) and the [Hugging Face MCP server](https://huggingface.co/docs/huggingface_hub/main/en/package_reference/mcp). It helps you quickly understand papers by answering questions, summarizing key ideas, and providing context as you browse the latest research.
```

**Breaking change with migration:**
```markdown
**Jul 25, 25**

## Introducing a better Hugging Face CLI

We've renamed `huggingface-cli` to `hf` and overhauled the command structure for speed and clarity. The new CLI now uses the format `hf <resource> <action>`, so commands like `hf auth login`, `hf repo create`, or `hf download Qwen/Qwen3-0.6B` are now consistent and intuitive.

Migration is easy, the old CLI still works and will gently point you to the new commands.
```

**Improvement with examples:**
```markdown
**Oct 9, 25**

## Organization tagging for Papers

Authors can now tag an Organization when submitting a paper. Each Organization has a dedicated Papers page that automatically lists its tagged publications. See examples: https://huggingface.co/nvidia/papers and https://huggingface.co/google/papers.

This makes it easier for teams to showcase their research and for readers to discover work by lab, company, or community.
```
