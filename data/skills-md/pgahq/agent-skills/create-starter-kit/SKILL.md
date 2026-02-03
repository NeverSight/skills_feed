---
name: create-starter-kit
description: Creates a new Next.js starter kit repository with PRD documentation structure. Sets up a minimal Next.js app with shadcn/ui and Tailwind CSS, then scaffolds a docs directory with PRD templates. Use when the user wants to create a new starter kit repository for documenting a new product or system.
---

# Create Starter Kit Repository

This skill creates a new Next.js starter kit repository with a structured PRD documentation system. Starter kits are minimal app scaffolds with comprehensive documentation that serve as input for AI coding agents or developers.

## Prerequisites

**REQUIRED**: Before proceeding, the user must provide:
- A brief description of what the starter kit will be about (domain, purpose, scope)
- The desired repository name

The agent must prompt for this information if not provided and cannot proceed without it.

## Project Location

Ask the user where they want to create the project, or use the current working directory if appropriate. The project will be created at the specified path.

If the chosen directory already exists, use a variant of the name (e.g., `project-name-v2`).

## Setup Process

Follow these steps in order:

### 1. Gather Requirements

**MANDATORY**: Ask the user to describe what the starter kit will be about. Use this information to:
- Generate a basic PRD overview
- Determine appropriate repository name
- Create relevant PRD sections

Example prompt: "What is this starter kit for? Please provide a brief description of the domain, purpose, and scope (e.g., 'A ticketing platform for events', 'A credentialing system for staff access', etc.)"

### 2. Create Next.js Project

```bash
bun create next-app {project-full-path} --yes --ts --eslint --tailwind --app --src-dir --import-alias "@/*"
```

**Important**: Do NOT install Vercel AI SDK or any AI-related packages. This starter kit is documentation-focused and does not include AI functionality.

### 3. Initialize shadcn/ui

```bash
cd {project-full-path}
bunx shadcn@latest init --base-color neutral
```

### 4. Install Dependencies

```bash
bun install
```

### 5. Add Simple API Route

Create `src/app/api/hello/route.ts`:
```typescript
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ message: "Hello World from the API" });
}
```

### 6. Update Main Page

Replace `src/app/page.tsx` with a placeholder page that provides instructions:

```typescript
export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 max-w-3xl mx-auto">
      <h1 className="text-5xl font-bold mb-8 text-center">Starter Kit</h1>
      
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 w-full">
        <h2 className="text-2xl font-semibold mb-6 text-center">Next Steps</h2>
        
        <ol className="space-y-4 list-decimal list-inside">
          <li className="text-lg">
            <strong>Complete the PRD docs</strong> in <code className="bg-white px-2 py-1 rounded text-blue-600 font-mono">docs/prd/</code>
            <p className="text-gray-600 mt-2 ml-6 text-sm">Add as many markdown files as you want to <code className="bg-white px-2 py-1 rounded text-blue-600 font-mono">docs/</code> to document your project.</p>
          </li>
          <li className="text-lg">
            <strong>Implement the application</strong> with: <code className="bg-white px-2 py-1 rounded text-blue-600 font-mono">implement and run @/prd</code>
          </li>
        </ol>
      </div>
    </div>
  );
}
```

### 7. Create Documentation Structure

Create the following directory structure:

```
docs/
└── prd/
    ├── dev-plan.md
    └── overview.md
```

### 8. Create prd/dev-plan.md

Create `docs/prd/dev-plan.md` with this template:

```markdown
# Development Plan: {Project Name}

## Goal
{Add goal statement based on user's description}

## Guiding principles
- {Add principles relevant to the project}
- {Add principles relevant to the project}

## Sequencing overview
{Add high-level development phases}

## Phase-by-phase plan

### Phase 1: Foundation
**Goals**
- {Add goals}

**Deliverables**
- {Add deliverables}

**Checklist**
- [ ] {Add checklist items}

{Add additional phases as needed}

## Quality gates
- {Add quality gates}

## Definition of Done
- {Add definition of done criteria}
```

### 9. Create PRD Overview

Create `docs/prd/overview.md` with this template, customizing based on the user's description:

```markdown
# PRD: {Project Name} Overview

> Start here: see `dev-plan.md` for sequencing and quality gates.

> **Note for AI Agents**: When instructed to "build" or "implement" this application, this means to create/write the code based on the PRD documentation, not to create a production build. Use `implement and run @/prd` to begin implementation.

## Purpose & Vision

{Write 2-3 paragraphs describing the purpose and vision based on user's description}

## Users & Personas

| Persona | Primary Needs | Systems Used |
|---------|---------------|--------------|
| {Persona 1} | {Needs} | {Systems} |
| {Persona 2} | {Needs} | {Systems} |

{Add personas relevant to the project}

## System Architecture

{Add architecture diagram or description if applicable}

## Key Features & Capabilities

### {Feature Category 1}
- {Feature 1}
- {Feature 2}

### {Feature Category 2}
- {Feature 1}
- {Feature 2}

{Add features based on user's description}

## Document Map

This PRD suite consists of interconnected documents covering all aspects of the platform:

### Planning & Overview
- **[dev-plan.md](dev-plan.md)**: Development sequence, checklists, and quality gates
- **[overview.md](overview.md)**: System overview (this document)

{Additional PRDs will be added as the project evolves}

## Success Metrics

- {Add success metrics}

## Implementation Notes

- {Add implementation notes}
```

### 10. Create AGENTS.md

Create `AGENTS.md` in the project root:

```markdown
# Agent Development Guidelines

This document provides guidance for AI agents working on this application.

## Development Standards

- Always use TypeScript
- Follow Next.js App Router conventions
- Use Tailwind CSS for styling (shadcn/ui components available)
- Implement proper error handling
- Test integrations thoroughly before committing
```

### 11. Initialize Git Repository

```bash
cd {project-full-path}
git init
git add .
git commit -m "Initial starter kit with PRD documentation structure"
```

### 12. Open in IDE

Check for Cursor first, then fall back to VS Code or other modern IDEs:

```bash
cd {project-full-path}
if command -v cursor &> /dev/null && cursor --version &> /dev/null; then
  cursor .
elif command -v code &> /dev/null; then
  code .
elif command -v codium &> /dev/null; then
  codium .
else
  echo "Please open the project in your preferred IDE"
fi
```

## Documentation Structure Guidelines

### Directory Organization

The `/docs` directory follows this structure:

```
docs/
└── prd/                   # Product Requirements Documents
    ├── dev-plan.md        # Development sequence and quality gates
    ├── overview.md        # System overview and architecture
    └── *.md               # Additional PRDs as needed
```

**Note**: Users can add as many markdown files as they want to the `docs/` directory (or any subdirectories) to document their project. The structure is flexible and can be organized however makes sense for the project.

### Documentation Principles

1. **Progressive disclosure**: Start with overview, add detail in additional PRDs
2. **Cross-references**: Link between related documents
3. **Consistent structure**: Use similar sections across PRDs
4. **Living documents**: PRDs evolve as requirements clarify

## Checklist

Use this checklist to track progress:

- [ ] Gather project description from user
- [ ] Determine project location and name
- [ ] Check if directory already exists
- [ ] Create Next.js project (without AI SDK)
- [ ] Initialize shadcn/ui with neutral base color
- [ ] Install dependencies
- [ ] Create API route returning "Hello World from the API"
- [ ] Update page.tsx with placeholder UI and instructions
- [ ] Create docs directory structure
- [ ] Create prd/dev-plan.md with project-specific content
- [ ] Create prd/overview.md with project-specific content
- [ ] Create AGENTS.md with development guidelines
- [ ] Initialize git repository and commit
- [ ] Open project in IDE (checking for Cursor first, then VS Code)

## Notes

- Starter kits are intentionally minimal - they focus on documentation over implementation
- The app scaffold is a placeholder UI with instructions, not a working application
- PRDs should be written first, then implementation follows
- Do NOT include AI SDK or AI-related functionality in starter kits
- Do NOT build the actual application - leave it as a placeholder with instructions
