---
name: react-triage
description: Maintain and extend the React Triage Bun CLI that scans React/Next.js projects with Oxlint, custom checks, Vercel best-practice rules, and security auditing. Use this skill when modifying scan logic, adding diagnostics, adjusting scoring, updating CLI/report output, or debugging Bun-based project analysis behavior.
---

# React Triage

Maintain and operate React Triage to scan React/Next.js projects, export actionable diagnostics, and manage report files.

## Installation

```bash
bun add -g react-triage
```

or with npm:

```bash
npm install -g react-triage
```

## Usage

```bash
react-triage .
```

or 

```bash
bunx react-triage .
```

## Workflow

1. Run the `react-triage .` command at the project root.
2. Export results to Markdown.
3. Read the report and act on diagnostics.
4. Remove the report file after use.

## Markdown Report Lifecycle

Use these commands to run the tool, export a Markdown report, read it, and remove it.

1. Export results to Markdown:
   - `react-triage . --to-markdown=triage-report.md`
2. Read the exported report:
   - `cat triage-report.md`
3. Remove the exported report when no longer needed:
   - `rm triage-report.md`

## Rules
- **Oxlint Checks**: Run Oxlint for code quality and best practices.
- **Accessibility Checks**: WCAG 2.1 violations via the jsx-a11y plugin (missing alt text, invalid ARIA roles, keyboard accessibility, empty headings, unlabelled form controls).
- **Custom Checks**: Implement custom logic for React/Next.js patterns.
- **Vercel Best Practices**: Enforce Vercel deployment guidelines.
- **Security Auditing**: Identify potential security issues in the codebase.
- **Unused Packages**: Detect and report unused dependencies in package.json.
