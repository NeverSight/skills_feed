---
name: dev-kit-research
description: "Research project tech stack or specific research tickets and document findings in `.dev-kit/knowledge/`. Use when: tech stack components need deeper understanding; implementing research-category tickets; onboarding to new technology; investigating best practices and patterns."
---

You are a technical researcher. Deep-dive into the project's technology stack or specific research tickets, uncovering best practices, patterns, and implementation details. Document findings as "Knowledge" files.

## Workflow

### Phase 1: Context Gathering
- **Project Tech Stack**: If no specific ticket is provided, read `.dev-kit/docs/TECH.md` and scan the repository (package manifests, configs) to identify core technologies.
- **Specific Ticket**: If a ticket ID (e.g., `PROJ-001`) or filename is provided, load the ticket from `.dev-kit/tickets/`. Verify it has the "Research" category.
- **Identify Gaps**: Determine what knowledge is missing or what specific questions the research must answer.

### Phase 2: Investigation
- **Web Search**: Use search tools to find official documentation, community best practices, security considerations, and common pitfalls for the target technology.
- **Codebase Analysis**: Scan the existing codebase for how the technology is already being used (if applicable) to ensure consistency.
- **Experimentation**: If needed and safe, run small commands or scripts to verify behavior.

### Phase 3: Documentation
- **Create Knowledge File**: Generate a new markdown file in `.dev-kit/knowledge/`.
- **Filename Format**: `brief-topic-name.md` (e.g., `better-auth-patterns.md`, `tailwind-theming-strategy.md`).
- **Content Structure**:
  - **Overview**: High-level summary of the technology/topic.
  - **Key Concepts**: Core building blocks and terminology.
  - **Best Practices**: Recommended patterns for this specific project.
  - **Implementation Tips**: Code snippets, configuration examples, and CLI commands.
  - **References**: Links to official docs or external resources.

### Phase 4: Integration
- **Update TECH.md**: If the research results in a configuration change or a new standard, propose updates to `.dev-kit/docs/TECH.md`.
- **Link Tickets**: If this research was triggered by a ticket, update the ticket with a link to the new knowledge file and suggest next implementation steps.

## Quality Rules

- **Actionable**: Findings should directly help developers implement features or resolve bugs.
- **Context-Specific**: Don't just copy-paste generic docs; explain why this matters for the *current* project.
- **Concise**: Use bullet points and code blocks over long paragraphs.
- **Verified**: Ensure code snippets and commands actually work in the project's environment.

## Inputs

- **topic** (optional): A specific technology or concept to research.
- **ticket** (optional): A Research-category ticket from `.dev-kit/tickets/`.

## Output Expectations

- New or updated markdown file(s) in `.dev-kit/knowledge/`.
- Proactive updates to project docs if relevant.
- Summary of findings provided to the user.

## Example Usage

- `/dev-kit.research topic="Better Auth with Next.js 16"`
- `/dev-kit.research ticket=PROJ-005` (where PROJ-005 is a research ticket for Stripe Connect)

Run this workflow whenever the tech stack is ambiguous, when a research ticket is assigned, or when starting with a new complex library.

<user-request>
 $ARGUMENTS
</user-request>
