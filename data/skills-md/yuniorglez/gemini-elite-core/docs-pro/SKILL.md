---
name: docs-pro
id: docs-pro
version: 1.1.0
description: "Senior Technical Writer & Docs Architect. Expert in AI-driven documentation synchronization, style guide enforcement, and 2026 Markdown standards."
---

# 📚 Skill: docs-pro (v1.1.0)

## Executive Summary
`docs-pro` is a comprehensive skill for managing the lifecycle of technical documentation. It bridges the gap between raw implementation and user-facing clarity. In 2026, we treat **Documentation as Code (DaC)**, using AI to ensure that every new feature, configuration, and API change is accurately reflected in our docs within minutes of a commit.

---

## 📋 Table of Contents
1. [Core Capabilities](#core-capabilities)
2. [The "Do Not" List (Anti-Patterns)](#the-do-not-list-anti-patterns)
3. [Quick Start: The Sync Audit](#quick-start-the-sync-audit)
4. [Standard Production Patterns](#standard-production-patterns)
5. [Documentation Quality Standards](#documentation-quality-standards)
6. [AI-Driven Documentation Workflow](#ai-driven-documentation-workflow)
7. [Reference Library](#reference-library)

---

## 🚀 Core Capabilities
- **Automated Sync Audit**: Scanning codebases for undocumented exports, settings, and flags.
- **Style Enforcement**: Ensuring all documentation follows the 2026 Squaads AI Style Guide.
- **Modular Content Architecture**: Managing reusable snippets and modular pages for scalability.
- **Multimodal Documentation**: Integrating diagrams (Mermaid), code examples, and interactive elements.

---

## 🚫 The "Do Not" List (Anti-Patterns)

| Anti-Pattern | Why it fails in 2026 | Modern Alternative |
| :--- | :--- | :--- |
| **"Click Here" Links** | Bad for accessibility and AI context. | Use **Descriptive Anchor Text**. |
| **Outdated Defaults** | Leads to user frustration and support tickets. | Use **Docs Sync Audit** to verify defaults. |
| **Manual Reference Docs** | Impossible to maintain at scale. | Generate API refs from **Code Docstrings**. |
| **Wall of Text** | Low information retention. | Use **Bullet Points, Tables, and Diagrams**. |
| **Mixing Languages** | Makes maintenance and translation hard. | Keep English as the **Source of Truth** in `docs/`. |

---

## ⚡ Quick Start: The Sync Audit

Perform a basic check to see what's missing in your documentation:

```bash
# 1. Analyze changes in current branch vs main
git diff main...HEAD -- src/

# 2. Search for common undocumented patterns
rg "export (const|function|class)" src/ --type ts

# 3. Compare findings with docs/ structure
ls -R docs/
```

---

## 🛠 Standard Production Patterns

### Pattern A: The Feature Release Doc
When implementing a new feature, follow this checklist:
1.  **Overview**: What does it do?
2.  **Configuration**: List all environment variables and settings.
3.  **Examples**: Provide "Quick Start" and "Advanced" code blocks.
4.  **Troubleshooting**: Common errors and their fixes.

### Pattern B: The API Reference Update
Instead of editing `docs/ref/*.md` directly:
1.  Update the JSDoc/TSDoc comments in the source code.
2.  Run the doc generator (e.g., `make build-docs`).
3.  Verify the output matches the **Markdown Standard**.

---

## 📏 Documentation Quality Standards

We adhere to strict standards to ensure high utility for both humans and AI agents.

- **Clarity**: Active voice, present tense, and direct address.
- **Accuracy**: Code examples must be tested and valid.
- **Discoverability**: Every page must be listed in `mkdocs.yml` with a descriptive title.

*See [References: Style Guide](./references/style-guide.md) for more.*

---

## 🤖 AI-Driven Documentation Workflow

1.  **Inventory**: AI scans the codebase to build a feature list.
2.  **Gap Analysis**: AI compares the inventory to existing `.md` files.
3.  **Drafting**: AI proposes new content based on implementation logic.
4.  **Review**: Human-in-the-loop verification of tone and accuracy.

*See [References: AI Collaboration](./references/ai-collaboration.md) for more.*

---

## 📖 Reference Library

Detailed deep-dives into documentation excellence:

- [**2026 Style Guide**](./references/style-guide.md): Voice, tone, and structural rules.
- [**Markdown Standards**](./references/markdown-standard.md): Frontmatter, code blocks, and AI-friendly syntax.
- [**AI Collaboration Guide**](./references/ai-collaboration.md): How agents and humans work together on docs.
- [**Coverage Checklist**](./references/doc-coverage-checklist.md): The master list for doc audits.

---

*Updated: January 22, 2026 - 17:05*
