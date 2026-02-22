---
name: docs
description: >
  Agent-first project documentation. Scaffolds and maintains a documentation
  architecture designed for AI agents — ROADMAP, design-docs, logs, and more.
  Use when the user says "/docs", asks to set up project documentation, wants
  to update docs, or when starting a new project that lacks documentation
  structure. Also use when the user asks to plan a feature (creates a design
  doc) or review what's been done (updates logs/roadmap).
---

# /docs — Project Documentation

You are managing an agent-first documentation architecture. Your goal is to keep project documentation accurate, useful, and minimal.

## Determine mode

1. If the user explicitly says "init" or "setup", use **Init mode**.
2. If the project is missing core doc files (no ROADMAP.md, no design-docs/), suggest Init mode.
3. Otherwise, use **Update mode**.

---

## Init mode

Scaffold the documentation structure for this project. Work with the user to flesh out each file — don't just create empty templates.

### Steps

1. **Assess what exists.** Check for existing README.md, CLAUDE.md, ARCHITECTURE.md, etc. Don't overwrite existing content — integrate with it using these rules:
   - **README.md**: Preserve existing content. Reorganize into template sections if the structure is loose, but keep the substance.
   - **CLAUDE.md**: Never modify existing instructions. If there's no existing documentation section, append one using the template. If there's already a documentation section (or similar conventions like "work log" or "commit" instructions), show the user both the existing rules and the template rules, and ask which to keep or how to merge them. Existing project conventions take precedence over template defaults.
   - **ARCHITECTURE.md**: If one exists, adopt its structure and fill gaps from the template. If not, create from template.
   - **Other files** (ROADMAP, IDEAS, MARKETING): Create fresh from templates — these are unlikely to exist already.

2. **Discuss scope with the user.** Not every project needs every file. At minimum, most projects benefit from:
   - README.md (what is this project?)
   - ROADMAP.md (what needs to happen?)
   - CLAUDE.md additions (agent maintenance instructions)

   Larger projects may also want:
   - ARCHITECTURE.md (system design)
   - IDEAS.md (brainstorming backlog)
   - MARKETING.md (go-to-market notes)
   - design-docs/ and logs/ directories

3. **Create files using the templates** in `references/` as starting points. Each template is a separate file:
   - `references/roadmap.md` — ROADMAP.md template
   - `references/ideas.md` — IDEAS.md template
   - `references/architecture.md` — ARCHITECTURE.md template
   - `references/marketing.md` — MARKETING.md template
   - `references/design-doc.md` — design doc template
   - `references/log.md` — daily log template
   - `references/claude-md.md` — CLAUDE.md documentation section

   Read only the templates you need. Adapt them to the project — don't use verbatim. Work with the user to fill in real content rather than leaving placeholders.

4. **Add maintenance instructions to CLAUDE.md.** Create CLAUDE.md if it doesn't exist. Use `references/claude-md.md` as the base. Adapt to what files were actually created (e.g., omit the IDEAS.md instruction if that file wasn't created).

5. **Create initial log entry** in `logs/` for today, noting the documentation setup.

---

## Update mode

Review recent work and bring documentation up to date.

### Steps

1. **Scan recent activity.** Check:
   - `git log` for recent commits since the last log entry. Find the newest file in `logs/` to determine the cutoff date. If no prior log exists, scan the last ~20 commits for context.
   - Current state of ROADMAP.md — are items stale? Anything done but not checked off?
   - Existing design-docs — any need status updates?
   - If `logs/` doesn't exist yet, create it and start the first entry.

2. **Update ROADMAP.md.** Check off completed items with dates and commit hashes. Add any new work that's emerged. Move items between sections as needed.

3. **Update or create today's log entry** in `logs/`. Summarize what was done, link to relevant design-docs or commits. Focus on narrative — surprises, debugging insights, decisions made. Don't duplicate information that's already in design-docs.

4. **Update design-docs** if any active ones need status changes or new decisions recorded.

5. **Surface gaps.** Let the user know if you notice:
   - Work that doesn't have a corresponding ROADMAP entry
   - Decisions that aren't documented anywhere
   - Stale items that might need to be moved to wontdo

Keep updates concise. The goal is accurate docs, not comprehensive prose.

---

## File reference

When creating or updating these files, read the corresponding template from `references/` for the expected structure.

| File | Template | Purpose | When to update |
|------|----------|---------|----------------|
| `README.md` | — | Project goal, what this is | When the project scope changes |
| `ARCHITECTURE.md` | `references/architecture.md` | System design, components | When architecture changes |
| `ROADMAP.md` | `references/roadmap.md` | Status, active work, done, wontdo | After completing or starting work |
| `IDEAS.md` | `references/ideas.md` | Brainstorming, not-yet-ready | When ideas come up |
| `MARKETING.md` | `references/marketing.md` | Positioning, distribution, content | When marketing strategy evolves |
| `design-docs/YYYY-MM-DD-*.md` | `references/design-doc.md` | Feature specs and plans | When planning or after key decisions |
| `logs/YYYY-MM-DD.md` | `references/log.md` | Daily narrative | After each work session |
| `CLAUDE.md` (docs section) | `references/claude-md.md` | Agent maintenance instructions | During init |
