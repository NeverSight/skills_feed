---
name: prospero-types-skill
description: Provides comprehensive knowledge about the Prospero project, using the `src` directory as a source of truth for terms, types, and their descriptions. Use this skill when you need to understand any Prospero-specific types, data structures, or concepts.
---

# Prospero Types Knowledge Base

## Overview

This skill provides detailed information and definitions for types and concepts used across the Prospero project. It leverages the local `src` directory as its primary source of truth, offering clear explanations of data structures and their relationships.

## How to Use This Skill

When asked about a Prospero-specific term, type, or data structure, you should:

1.  **Identify the relevant type name or concept.**
2.  **Search the `src/` directory** for files containing the definition of this type. You can use the `search_file_content` tool with a pattern like `export (type|interface) <TypeName>`.
3.  **Read the content of the identified file(s)** using the `read_file` tool.
4.  **Extract the type definition**: Analyze the TypeScript syntax to understand the properties, their types, and any associated comments.
5.  **Provide a clear, concise explanation** of the type, including its purpose, key properties, and any relationships to other types. If the type is complex, break down its components.
6.  **For complex types or inter-dependencies**: If a type references other types (e.g., `Assignment` referencing `MediaImage`), recursively investigate those types as well to provide a complete understanding.
7.  **For a high-level understanding of Prospero components and their relationships, refer to `prospero-overview.md` if available, or ask the user for more context.**

## References

This skill is powered by the following type definitions:

### `prospero-types` (local `src` directory)
The type definitions from the local project's `src` directory. These files contain the authoritative definitions for various entities and data structures within the Prospero ecosystem.

You can browse the raw type definitions in these files for detailed information:
- `src/assignments.ts`
- `src/basket.ts`
- `src/bundles.ts`
- `src/common.ts`
- `src/dashboard.ts`
- `src/discord.ts`
- `src/email.ts`
- `src/groups.ts`
- `src/index.ts`
- `src/library.ts`
- `src/media.ts`
- `src/permissions.ts`
- `src/producers.ts`
- `src/sessions.ts`
- `src/smartscripts.ts`
- `src/stripe.ts`
- `src/subscriptions.ts`
- `src/users.ts`
- `src/functions/api.ts`
- `src/functions/assignments.ts`
- `src/functions/discord.ts`
- `src/functions/groups.ts`
- `src/functions/index.ts`
- `src/functions/media.ts`
- `src/functions/producers.ts`
- `src/functions/sessions.ts`
- `src/functions/smartscripts.ts`
- `src/functions/stripe.ts`
- `src/functions/subscriptions.ts`
- `src/functions/tokens.ts`
- `src/functions/transfers.ts`
- `src/functions/users.ts`
- `src/genres/index.ts`
- `src/genres/lighting.ts`
- `src/genres/mPaper.ts`
- `src/genres/pose.ts`
- `src/genres/questionnaire.ts`
- `src/genres/scriptWriter.ts`
- `src/genres/wordPairs.ts`
- `src/render/actions.ts`
- `src/render/actors.ts`
- `src/render/characters.ts`
- `src/render/index.ts`
- `src/render/nodes.ts`
- `src/render/scenes.ts`
- `src/render/triggers.ts`
- `src/render/variables.ts`
- `src/research/evidence.ts`
- `src/research/index.ts`
- `src/research/reports.ts`
- `src/research/zod.ts`