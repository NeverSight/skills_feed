---
name: doc-writer
description: Crea documentos técnicos organizados en /docs (specs, planes, ADRs, referencias). Usa cuando el usuario diga "crear documento", "escribir spec", "documentar esto", "creame una spec", "escribime documentación", "hacer documentación", o quiera agregar documentación al proyecto.
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, LS
---

# Doc Writer

Skill para crear documentos tecnicos en la estructura correcta del proyecto.

## Cuando usar esta Skill

- Usuario pide escribir una spec o especificacion
- Usuario pide crear un plan de implementacion
- Usuario pide documentar una decision arquitectonica (ADR)
- Usuario pide crear documentacion de referencia
- Cualquier documento que deba ir en `docs/`

## Proceso de Creación

### Paso 1: Buscar estructura de docs existente

```bash
# Buscar carpeta docs
ls -la docs/ 2>/dev/null

# Listar subcarpetas existentes
ls -d docs/*/ 2>/dev/null
```

### Paso 2: Preguntar categoria al usuario

**Si existen subcarpetas en docs/**: Ofrecerlas como opciones.

**Si no existen subcarpetas**, preguntar al usuario qué categorías quiere usar:

| Categoria | Uso |
|-----------|-----|
| `specs/` | Especificaciones de features/sistemas |
| `plans/` | Planes de implementacion |
| `architecture/` | ADRs, decisiones arquitectonicas |
| `reference/` | Documentacion tecnica de referencia |
| `backlog/` | Features pendientes, ideas futuras |
| `work-in-progress/` | Documentacion de trabajo activo |

Formato de pregunta:
```
¿En qué categoría va este documento?
☐ specs/ - Especificaciones
☐ plans/ - Planes de implementación
☐ architecture/ - ADRs, decisiones
☐ reference/ - Documentación de referencia
☐ [Otra categoría]
```

### Paso 3: Generar nombre de archivo

Formato: `YYYY-MM-DD-HH-MM-<feature-name>.md`

- Usar fecha y hora actual
- `<feature-name>` en kebab-case, descriptivo, sin espacios

Ejemplo: `2025-12-25-14-30-user-authentication.md`

### Paso 4: Crear el documento

1. Crear subcarpeta si no existe
2. Aplicar template segun tipo de documento
3. Escribir archivo en la ubicacion correcta

## Templates

### Spec Template

Usar cuando el usuario pide una especificacion o spec de feature:

```markdown
# [Feature Name] - Specification

## Overview
Brief description of what this feature does.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Technical Approach
How this will be implemented.

## Dependencies
- Dependency 1

## Open Questions
- Question 1?
```

### Plan Template

Usar cuando el usuario pide un plan de implementacion:

```markdown
# [Feature Name] - Implementation Plan

## Goal
What we're trying to achieve.

## Steps
1. Step 1
2. Step 2

## Considerations
- Risk/consideration 1

## Success Criteria
- [ ] Criteria 1
```

### Architecture Template (ADR)

Usar cuando el usuario pide documentar una decision arquitectonica:

```markdown
# ADR: [Decision Title]

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult because of this change?
```

### Reference Template

Usar cuando el usuario pide documentacion de referencia:

```markdown
# [Topic] Reference

## Overview
What this document covers.

## Details
Technical details and usage.

## Examples
Code or usage examples.

## Related
- Link to related docs
```

---

## Ejemplos de uso

Usuario: "Escribime una spec para el sistema de autenticacion"

1. Buscar docs/: Existe, tiene subcarpetas `specs/`, `plans/`
2. Preguntar categoría: "¿En qué categoría va?" → Usuario elige `specs/`
3. Nombre: `2025-12-25-15-30-authentication-system.md`
4. Crear: `docs/specs/2025-12-25-15-30-authentication-system.md` con Spec Template
