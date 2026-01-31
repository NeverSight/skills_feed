---
name: awesome-ai-security-overview
description: Guide for understanding and contributing to the awesome-ai-security curated resource list. Use this skill when adding resources, organizing categories, or maintaining README.md consistency (no duplicates).
---

# Awesome AI Security - Project Overview

## Purpose

This is a curated collection of AI/ML security materials and resources for pentesters, red teamers, and security researchers. The goal is to keep the list **AI-focused**, **high-signal**, **well-categorized**, and **non-duplicated**.

## Project Structure

```
awesome-ai-security/
├── README.md                # Main resource list (curated)
├── LICENSE                  # License
├── .claude/
│   └── skills/              # Claude skills (this directory)
└── ref/                     # Reference notes (not curated)
    ├── my_collect.md        # Personal collection
    ├── Awesome-AI-Security-1/
    ├── awesome-ai-security-2/
    ├── 模型安全/             # Model security notes
    ├── 渗透测试相关/          # Pentesting notes
    └── 网络安全相关/          # Network security notes
```

## README.md Format Convention

### Heading Structure

- Top-level categories use `##`.
- Subcategories use `###` (e.g., inside `AI Security & Attacks`).
- Starter Pack uses bold bullets for sub-sections (e.g., `- **CTFs / Practice**`).

### Link Format

- Use full URLs, one per bullet line.
- Add a short description in square brackets: `- https://... [Short description]`
- Keep descriptions concise.
- Do not add the same URL in multiple places.

### Example Entry

```markdown
### Prompt Injection
- https://github.com/example/tool [Prompt injection detector]
```

## Categorization Rules (How to Place a New Link)

- **AI Security Starter Pack**: CTFs, courses, blogs, newsletters, beginner resources.
- **AI/LLM Guide**: LLM fundamentals, tutorials, awesome lists.
- **AI Security & Attacks**: Prompt injection, adversarial attacks, poisoning, privacy, model security.
- **AI Pentesting & Red Teaming**: AI-powered pentesting tools, red teaming, MCP security tools.
- **AI Security Tools & Frameworks**: AI vulnerability detection, CVE analysis, OSINT, security libraries.
- **AI Agents & Frameworks**: Agent frameworks, RAG, browser automation, MCP servers.
- **AI Development & Training**: Training frameworks, local models, uncensored models, prompts.
- **AI Applications**: Chat assistants, deep research, search engines, code analysis, web scraping.
- **AI Image & Video**: Image generation, video generation, TTS, face recognition.
- **Benchmarks & Standards**: AI safety benchmarks, threat frameworks, standards.

## AI-Relevance Filter

**Only include AI/ML-related resources.** Do not add:

- Traditional security tools (unless AI-powered)
- Web3/blockchain tools (unless AI-related)
- General pentesting tools without AI integration
- Browser vulnerabilities, phishing tools, CVE collections (unless AI-analyzed)

## Duplicate Policy

**No duplicate URLs in README.md.** If a link fits multiple categories, pick the primary one.

## Contribution Checklist

1. Check for duplicates in `README.md` before adding.
2. Verify the resource is AI/ML-related.
3. Verify the link points to the canonical source (avoid low-value forks).
4. Keep the description concise and useful.
5. Put it into the most appropriate category.
6. Prefer minimal changes over reformatting large sections.

## Data Source

For detailed and up-to-date resources, fetch the complete list from:

```
https://raw.githubusercontent.com/gmh5225/awesome-ai-security/refs/heads/main/README.md
```

Use this URL to get the latest curated links when you need specific tools, papers, or resources.
