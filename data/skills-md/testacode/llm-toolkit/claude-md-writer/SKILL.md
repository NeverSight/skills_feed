---
name: claude-md-writer
description: Escribe y mejora CLAUDE.md siguiendo best practices. Usa cuando el usuario diga "crear CLAUDE.md", "mejorar CLAUDE.md", "actualizar CLAUDE.md", "revisar CLAUDE.md", "escribir instrucciones del proyecto", "agregar reglas al proyecto", "actualizar documentación", "optimizar documentación para Claude", o configure un nuevo repo.
allowed-tools: Read, Glob, Grep, Write, Edit
---

# CLAUDE.md Writer

A skill for creating and optimizing CLAUDE.md files following official Anthropic best practices (2026-01).

## When to Use This Skill

- Creating a new CLAUDE.md for a project
- Reviewing/auditing an existing CLAUDE.md
- Optimizing documentation for better Claude Code performance
- User asks about CLAUDE.md best practices

## Golden Rule

Para cada línea, preguntá: *"¿Eliminar esto causaría que Claude cometa errores?"*
Si no, eliminalo. CLAUDE.md inflados causan que Claude ignore instrucciones.

> "Think of CLAUDE.md as the 'unwritten knowledge' in your codebase"

## Quick Tools

- `/init` - Genera CLAUDE.md inicial basado en la estructura del proyecto
- `#` key - Agregar instrucciones dinámicamente durante la sesión

## @import Syntax

CLAUDE.md puede importar otros archivos:
```markdown
See @README.md for overview and @package.json for commands.
Git workflow: @docs/git-instructions.md
```

## Reference Documentation

For detailed best practices, read: `docs/claude-md-best-practices.md`

## What to Include vs Exclude

| ✅ Include | ❌ Exclude |
|-----------|-----------|
| Bash commands Claude can't guess | Anything Claude can figure out by reading code |
| Code style rules that differ from defaults | Standard language conventions |
| Testing instructions and preferred test runners | Detailed API docs (link instead) |
| Repository etiquette (branch naming, PR) | Information that changes frequently |
| Architectural decisions specific to project | Long explanations or tutorials |
| Developer environment quirks (env vars) | File-by-file descriptions |
| Common gotchas or non-obvious behaviors | Self-evident practices |

## CLAUDE.md vs Skills

| CLAUDE.md | Skills |
|-----------|--------|
| Reglas amplias que aplican siempre | Conocimiento de dominio solo relevante a veces |
| Code style y workflow | Workflows especializados reutilizables |
| Convenciones del repo | Info que cambia por contexto |
| Se carga en cada sesión | Se cargan on-demand |

## Usage Modes

El skill acepta argumentos para diferentes flujos:

| Invocación | Comportamiento |
|------------|----------------|
| `/claude-md-writer` | Proceso completo: analizar proyecto → escribir/mejorar CLAUDE.md |
| `/claude-md-writer actualiza con la sesión` | Extraer info relevante de la sesión actual y agregar a CLAUDE.md |
| `/claude-md-writer agrega regla: [descripción]` | Agregar una regla específica con el formato correcto |
| `/claude-md-writer revisa y optimiza` | Auditar CLAUDE.md existente, eliminar redundancias, mejorar énfasis |
| `/claude-md-writer convierte a skill` | Identificar contenido que debería ser skill y extraerlo |

## Content Triage

Antes de agregar contenido a CLAUDE.md, evaluar:

| Si el contenido es... | Entonces... |
|-----------------------|-------------|
| Regla que aplica a TODAS las tareas | ✅ Agregar a CLAUDE.md |
| Domain knowledge específico | 🔄 Sugerir crear skill con `/skill-creator` |
| Workflow que solo aplica a veces | 🔄 Sugerir crear skill |
| Info que cambia frecuentemente | ❌ No agregar, linkear a docs |

### Detectar candidatos a Skill

Si el usuario quiere agregar info que cumple estos criterios, sugerir skill:
- "Cuando trabajes con X..." (condicional)
- "Para tareas de tipo Y..." (específico)
- "Si estás haciendo Z..." (situacional)
- Workflows con muchos pasos
- Conocimiento de dominio especializado

**Respuesta sugerida:**
> Esta información parece ser domain knowledge/workflow específico que no aplica
> a todas las tareas. Te sugiero crear un skill separado usando `/skill-creator`
> o `document-skills:skill-creator`. Así se carga on-demand sin inflar cada sesión.

## Process

### Step 1: Analyze the Project

Before writing, gather information:

```bash
# Check project type and structure
ls -la
cat package.json 2>/dev/null || cat pom.xml 2>/dev/null || cat Cargo.toml 2>/dev/null

# Find existing documentation
ls -la docs/ 2>/dev/null
ls -la README.md 2>/dev/null
```

Identify:
- Tech stack (language, framework, build tools)
- Project structure (monorepo, single app, library)
- Existing documentation to reference

### Step 2: Apply the Three Dimensions

Every CLAUDE.md must address:

| Dimension | Question to Answer |
|-----------|-------------------|
| **WHAT** | What is this project? Tech stack? Structure? |
| **WHY** | Why does it exist? What problem does it solve? |
| **HOW** | How do I work on it? Commands? Workflows? |

#### Triage Check

Para cada pieza de información, preguntar:
1. ¿Aplica a TODAS las tareas en este repo? → CLAUDE.md
2. ¿Solo aplica a ciertos tipos de tareas? → Skill
3. ¿Cambia frecuentemente? → Link externo

### Step 3: Write Following Best Practices

**Length**: Keep under 200 lines (ideal ~100 lines)

**Structure** (in order):
1. Repository Overview (1 paragraph)
2. Why This Exists (purpose, users)
3. Quick Start & Commands (bash with descriptions)
4. Architecture Overview (key patterns)
5. Key Development Rules (with emphasis)
6. References (links to detailed docs)

**Emphasis for Critical Rules**:
```markdown
- **CRITICAL**: [Never violate this]
- **IMPORTANT**: [Always do this]
- **YOU MUST**: [Mandatory action]
```

**Progressive Disclosure**:
- Use file references instead of code snippets
- Link to external docs for detailed topics
- Keep CLAUDE.md focused on universal instructions

### Step 4: Verify with Checklist

Before finalizing, verify:

- [ ] Under 200 lines?
- [ ] Passes Golden Rule? (each line prevents mistakes)
- [ ] Has WHAT, WHY, HOW sections?
- [ ] Critical rules have emphasis (CRITICAL/IMPORTANT)?
- [ ] Code snippets replaced with file references?
- [ ] Bash commands have descriptions?
- [ ] References external docs for detailed topics?
- [ ] No styling rules that should be in linters?
- [ ] Domain-specific content moved to skills?

## Template

```markdown
# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

[One paragraph: what this project is, tech stack, main purpose]

## Why This Exists

[What problem it solves, who uses it, business context]

## Quick Start & Commands

\`\`\`bash
npm ci        # Install dependencies
npm start     # Start dev server
npm test      # Run tests
npm run build # Production build
\`\`\`

> **Note**: [Any important setup notes, env files, postinstall behavior]

## Architecture Overview

[Key patterns, folder structure, main concepts - keep brief]

## Key Development Rules

- **CRITICAL**: [Most important rule that must never be violated]
- **IMPORTANT**: [Second most important rule]
- [Other rules...]

## References

- `/docs/` - Detailed documentation
- `README.md` - Project readme
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| Code snippets | Become stale, waste tokens | Use `file:line` references |
| Styling rules | LLM is slow for deterministic tasks | Configure linters |
| Kitchen sink | Dilutes instruction effectiveness | Keep < 200 lines |
| No emphasis | Critical rules same weight as minor | Use CRITICAL/IMPORTANT |
| Auto-generated | Misses project nuances | Manually craft |
| Domain knowledge | Inflates every session | Move to skills |
