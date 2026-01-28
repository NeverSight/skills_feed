---
name: documentation-guidelines
description: Write or update backend feature documentation that follows a repo's DOCUMENTATION_GUIDELINES.md (or equivalent) across any project. Use when asked to create/update module docs, API contracts, or backend documentation that must include architecture, endpoints, payloads, Mermaid diagrams, and seeding instructions.
author: Official
---

# Documentation Guidelines

## Overview
Produce a single, canonical module doc that matches the repository's documentation rules and keeps backend/API contracts consistent and skimmable.

## Workflow
1. Locate the repo's documentation rules (prefer `docs/memories/DOCUMENTATION_GUIDELINES.md`). If missing, load `references/documentation-guidelines.md`.
2. Determine the correct documentation path for the current project. Use the repo's conventions; if no zones exist, default to `docs/features/<module>.md` (or the project's documented location).
3. Create or update the module doc before changing logic. Remove outdated content instead of appending.
4. Follow the required section order from the guidelines and keep the doc in English.

## Required Content Checklist
- Add the metadata header (Version, Last Updated, Maintained By).
- Include Mermaid ERD and Mermaid flowchart.
- Document controllers/routes, requests, resources, models, services, jobs, and providers.
- Provide endpoint table, headers, payloads, response examples, and error dictionary.
- State permissions, feature flags, and client consumption rules.
- Add local development + seeding commands and troubleshooting/log hints.

## Style Rules
- Describe contracts and behavior, not UI.
- Use tables for endpoints and business rules.
- Keep Mermaid labels short and safe; wrap special characters in quotes if needed.
- Delete obsolete text to keep the doc clean and non-duplicative.

## Frontend API Documentation
If the user explicitly asks for frontend-facing API docs, load the repo's frontend guideline file (typically `docs/memories/FRONTEND_API_DOCUMENTATION_GUIDELINES.md`) and follow it.

## Resources
- `references/documentation-guidelines.md`: Canonical structure and ordering for backend feature documentation.
