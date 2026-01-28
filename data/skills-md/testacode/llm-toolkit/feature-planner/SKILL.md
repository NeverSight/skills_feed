---
name: feature-planner
description: Planifica features con entrevista estructurada y crea tareas. Usa cuando el usuario diga "quiero agregar", "planificar feature", "nueva funcionalidad", "implementar esto", "crear plan", "planificar antes de codear", "diseñar feature", o quiera pensar antes de escribir código.
allowed-tools: Read, Write, Edit, Glob, Bash, AskUserQuestion, TodoWrite
---

# Feature Planner

Skill para planificar nuevas funcionalidades mediante un proceso estructurado de entrevista y documentación.

## Cuándo Usar Este Skill

- Usuario quiere agregar una nueva funcionalidad
- Planificar un feature antes de implementarlo
- Crear un plan de implementación detallado
- Diseñar una característica con especificaciones claras

## Workflow

### Paso 1: Entender el Feature

Cuando el usuario describe una funcionalidad (ej: "quiero agregar dark mode"):

1. **Crear borrador inicial** en `/docs/wip/<feature-name>-plan.md`
2. **Capturar la idea principal** del usuario en el documento
3. **Identificar información faltante** para la implementación

```markdown
# <Feature Name> - Plan de Implementación

## Estado: BORRADOR

## Idea Original
<Lo que el usuario describió inicialmente>

## Preguntas Pendientes
- [ ] <pregunta 1>
- [ ] <pregunta 2>
```

### Paso 2: Entrevistar al Usuario

Invocar el proceso de entrevista siguiendo el patrón de `/interview`:

**Objetivo**: Obtener todos los detalles necesarios para una especificación completa.

**Áreas a cubrir**:

| Área | Preguntas Clave |
|------|-----------------|
| **Funcionalidad** | ¿Qué debe hacer exactamente? ¿Qué no debe hacer? |
| **UI/UX** | ¿Cómo interactúa el usuario? ¿Qué ve? |
| **Datos** | ¿Qué datos se necesitan? ¿Dónde se guardan? |
| **Integraciones** | ¿Qué APIs o servicios externos? |
| **Edge cases** | ¿Qué pasa si...? Escenarios límite |
| **Restricciones** | Performance, seguridad, compatibilidad |
| **Prioridad** | MVP vs nice-to-have |

**Técnicas de entrevista**:

- Usar `AskUserQuestion` para cada pregunta
- No hacer preguntas obvias o que se puedan inferir del código
- Profundizar en respuestas vagas ("¿podrías elaborar?")
- Confirmar entendimiento antes de avanzar
- Continuar hasta que el spec esté completo

**Referencia**: Ver `commands/dev/interview.md` para el patrón de entrevista completo.

### Paso 3: Documentar el Spec

Una vez completada la entrevista, actualizar el documento usando la plantilla:

```bash
# Ubicación del documento
/docs/wip/<feature-name>-plan.md
```

**Usar la plantilla de referencia**: `references/plan-template.md`

Cambiar el estado de BORRADOR a ESPECIFICADO cuando esté completo.

### Paso 4: Crear Tareas

Después de documentar, crear items con `TodoWrite`:

1. **Analizar el spec** y dividir en tareas atómicas
2. **Ordenar por dependencia** (qué debe hacerse primero)
3. **Estimar complejidad** (pequeña, mediana, grande)

```
Ejemplo de tareas para "dark mode":
1. Crear context de tema (ThemeContext)
2. Agregar toggle en settings
3. Definir variables CSS para dark mode
4. Aplicar estilos condicionales a componentes
5. Persistir preferencia en localStorage
6. Detectar preferencia del sistema
7. Escribir tests
```

**Criterios para buenas tareas**:
- Cada tarea es independiente o tiene dependencias claras
- Se puede completar en una sesión
- Tiene criterio de aceptación implícito
- Sigue el orden lógico de implementación

### Paso 5: Validar Estado Actual (Opcional)

Si el proyecto tiene scripts de validación:

```bash
# Verificar si existe npm run check o similar
cat package.json | grep -E '"check"|"lint"|"test"|"typecheck"'
```

Si existe:

1. **Preguntar al usuario** si desea ejecutar validación
2. **Ejecutar** `npm run check` (o equivalente)
3. **Reportar issues** encontrados antes de implementar
4. **Documentar** en el plan cualquier deuda técnica relevante

## Flujo Completo

```
Usuario: "Quiero agregar dark mode"
                ↓
    [Crear /docs/wip/dark-mode-plan.md]
                ↓
    [Entrevistar con AskUserQuestion]
    - ¿Solo toggle o detectar sistema?
    - ¿Qué componentes afecta?
    - ¿Persiste la preferencia?
    - ¿Transición animada?
                ↓
    [Actualizar documento con spec]
                ↓
    [Crear TodoWrite items]
                ↓
    [Ofrecer validar estado actual]
                ↓
    "Plan completo. ¿Empezamos?"
```

## Notas Importantes

- **No implementar** durante la planificación
- **Ser exhaustivo** en la entrevista, no asumir
- **Documentar decisiones** y su justificación
- **Mantener el documento** actualizado durante la implementación
- El documento queda en `/docs/wip/` hasta que el feature esté completo
