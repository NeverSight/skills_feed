---
name: shadcn-create-project
description: Scaffold a NEW project with Shadcn UI pre-configured (Next.js, Vite, etc.) using `shadcn create`.
---

# Shadcn Create Project

Use this skill to create a **brand new** project with Shadcn UI initialized from the start.

## Documentation
- [Shadcn Installation](https://ui.shadcn.com/docs/installation)

## Workflow

1.  **Run Creation Command**:
    Execute the following command to start the interactive setup:
    ```bash
    pnpm dlx shadcn@latest create
    ```
    *(Or `pnpm create shadcn@latest` if supported)*

2.  **Configuration Prompts**:
    The CLI will prompt for the following choices. Choose based on user requirements or use defaults:
    -   **Project Name**: (User defined)
    -   **Framework**: Next.js, Laravel, Vite, Remix, or TanStack Start.
    -   **Style**: New York (Default) or Default.
    -   **Base Color**: Slate, Gray, Zinc, Neutral, Stone.
    -   **CSS Variables**: `yes` (Always prefer CSS variables).

3.  **Post-Scaffold Verification**:
    -   Verify the project directory was created.
    -   Verify `components.json` exists.
    -   Verify `tailwind.config.ts/js` (or CSS config) exists.
