---
name: doc-organizer
description: Organiza y categoriza documentos en docs/. Usa cuando el usuario diga "organizar docs", "ordenar documentación", "mover documentos a carpetas", "categorizar archivos", o tenga archivos .md sueltos en docs/.
allowed-tools: Read, Bash, Glob, LS
---

# Doc Organizer

Skill para organizar y categorizar documentos tecnicos existentes en la estructura correcta del proyecto.

## Cuando usar esta Skill

- Usuario pide "organizar", "reorganizar", "categorizar" documentos
- Usuario pide "ordenar docs" o "mover documentos a carpetas"
- Se detectan archivos `.md` sueltos directamente en `docs/` sin subcarpeta

## Proceso de Organizacion

### Paso 1: Inspeccionar estado actual

```bash
# Archivos sueltos en docs/ (sin subcarpeta)
ls docs/*.md 2>/dev/null

# Carpetas existentes y su contenido
ls -la docs/*/ 2>/dev/null

# Listar todos los archivos md
find docs -name "*.md" -type f 2>/dev/null
```

### Paso 2: Preguntar por categorias

Presentar al usuario las opciones disponibles:

1. **Categorias existentes** detectadas en el proyecto
2. **Categorias sugeridas** si no existen:

| Categoria | Uso |
|-----------|-----|
| `specs/` | Especificaciones de features/sistemas |
| `plans/` | Planes de implementacion |
| `architecture/` | ADRs, decisiones arquitectonicas |
| `reference/` | Documentacion tecnica de referencia |

Formato de pregunta:
```
Categorias disponibles:
- specs/ - Especificaciones de features/sistemas
- plans/ - Planes de implementacion
- architecture/ - ADRs, decisiones arquitectonicas
- reference/ - Documentacion tecnica de referencia
- [Crear nueva categoria]

Cuales quieres usar para organizar?
```

### Paso 3: Analizar documentos y sugerir categorizacion

Para cada documento encontrado:

1. Leer contenido (primeras ~50 lineas)
2. Detectar tipo por keywords:

| Keywords detectados | Categoria sugerida |
|---------------------|-------------------|
| "ADR", "Decision", "Status: Accepted/Proposed", "Context", "Consequences" | `architecture/` |
| "Specification", "Requirements", "Spec", "Technical Approach" | `specs/` |
| "Plan", "Implementation", "Steps", "Timeline", "Goal" | `plans/` |
| "Reference", "Guide", "How to", "Examples", "Usage" | `reference/` |

3. Presentar sugerencias al usuario:

```
Analisis de documentos:

authentication-notes.md
   Detectado: Menciona "requirements" y "technical approach"
   Sugerencia: specs/
   Mover a specs/? [Y/n/otra categoria]

db-migration-decision.md
   Detectado: Contiene "Status: Accepted", "Context", "Decision"
   Sugerencia: architecture/ (es un ADR)
   Mover a architecture/? [Y/n/otra categoria]
```

### Paso 4: Ejecutar reorganizacion

Para cada documento confirmado:

1. Crear carpeta destino si no existe:
```bash
mkdir -p docs/<categoria>/
```

2. Mover archivo preservando historial git:
```bash
git mv docs/<archivo>.md docs/<categoria>/<archivo>.md
```

3. Renombrar al formato estandar si no lo tiene:
   - Formato: `YYYY-MM-DD-HH-MM-<name>.md`
   - Ejemplo: `2025-12-25-15-30-authentication-notes.md`

### Paso 5: Resumen final

Mostrar resultado de la organizacion:

```
Organizacion completada:
- 3 archivos movidos a specs/
- 2 archivos movidos a architecture/
- 1 archivo movido a plans/
- 0 archivos sin categorizar

Archivos reorganizados:
- docs/specs/2025-12-25-15-30-authentication-notes.md
- docs/architecture/2025-12-25-15-31-db-migration-decision.md
- ...
```

---

## Ejemplo de uso

Usuario: "Organiza los documentos en docs/"

1. Inspeccionar: Encuentra 3 archivos .md sueltos en docs/
2. Preguntar categorias: Usuario selecciona specs/, plans/, architecture/
3. Analizar cada archivo y sugerir categoria
4. Usuario confirma movimientos
5. Ejecutar: `git mv` para cada archivo
6. Mostrar resumen: "3 archivos reorganizados"
