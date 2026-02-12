---
name: notion-mastery
description: Sistema completo de productividad y CRM en Notion con integracion n8n. Usar cuando el usuario necesite gestionar tareas, proyectos, metas, pipeline de ventas, CRM de clientes, prospeccion con Apollo.io, o automatizar workflows entre Notion y otras herramientas. Activa con palabras como Notion, tareas, proyectos, CRM, pipeline, leads, Apollo, prospeccion, follow-up, deals, clientes.
---

# Notion Mastery

Sistema integral para dominar la gestion de productividad y ventas en Notion.

## Capacidades

1. **Gestion de Tareas y Proyectos** - GTD, planificacion semanal, seguimiento de metas
2. **CRM Completo** - Empresas, contactos, deals, pipeline de ventas
3. **Prospeccion Apollo.io** - Workflow completo desde busqueda hasta cierre
4. **Automatizaciones n8n** - Workflows automatizados via MCP n8n-mcp

## Decision de Flujo

```
¿Que necesitas hacer?
│
├─► Gestionar tareas/proyectos → Ver references/tasks-projects.md
│
├─► Configurar CRM/Pipeline → Ver references/crm-pipeline.md
│
├─► Prospectar con Apollo → Ver references/apollo-workflow.md
│
└─► Automatizar con n8n → Ver references/n8n-workflows.md
```

## Quick Start por Caso de Uso

### Crear estructura de proyecto nuevo
1. Abrir base de datos Proyectos en Notion
2. Crear pagina con nombre del proyecto
3. Asignar estado, prioridad, fechas, owner
4. Crear tareas relacionadas
5. Ver `references/tasks-projects.md` para detalles

### Importar leads de Apollo a Notion
1. Buscar en Apollo con filtros de ICP
2. Exportar contactos verificados
3. Usar n8n workflow "Apollo → Notion" para importar
4. Ejecutar scoring automatico
5. Ver `references/apollo-workflow.md` para proceso completo

### Hacer follow-up a deals activos
1. Revisar vista "Seguimientos Pendientes" en Notion
2. Ver historial de actividades del contacto
3. Ejecutar siguiente touchpoint segun cadencia
4. Registrar actividad y actualizar siguiente accion
5. Ver `references/crm-pipeline.md` para cadencias

### Crear automatizacion n8n + Notion
1. Identificar trigger (nueva pagina, cambio de estado, schedule)
2. Usar MCP n8n-mcp para crear workflow
3. Configurar nodos Notion con queries correctos
4. Testear y activar
5. Ver `references/n8n-workflows.md` para templates

## Estructura de Bases de Datos

### Jerarquia Principal
```
Metas/OKRs
    └── Proyectos
            └── Tareas

Empresas (Accounts)
    └── Contactos
            └── Deals
                    └── Actividades
```

### Relaciones Clave
- Proyecto ↔ Tareas (1:N)
- Empresa ↔ Contactos (1:N)
- Empresa ↔ Deals (1:N)
- Contacto ↔ Deals (N:N)
- Deal ↔ Actividades (1:N)

## Pipeline de Ventas

```
PROSPECTING → QUALIFICATION → DISCOVERY → PROPOSAL → NEGOTIATION → CLOSED
    (0%)         (10%)          (25%)       (50%)       (75%)       (100%)
```

### Acciones por Etapa

| Etapa | Accion Principal | Siguiente Paso |
|-------|------------------|----------------|
| Prospecting | Validar ICP score | Primer contacto |
| Qualification | Primer email/LinkedIn | Agendar discovery |
| Discovery | Reunion inicial | Preparar propuesta |
| Proposal | Enviar propuesta | Follow-up revision |
| Negotiation | Resolver objeciones | Cerrar deal |

## Comandos MCP n8n

Usar el MCP `n8n-mcp` para automatizaciones:

```
# Ver workflows disponibles
Listar workflows de n8n

# Ejecutar sincronizacion
Ejecutar workflow de Apollo a Notion

# Crear recordatorio
Crear workflow de follow-up automatico
```

## Revision Diaria (5 min)

1. Revisar tareas con fecha = hoy
2. Verificar follow-ups pendientes
3. Actualizar deals con actividad reciente
4. Priorizar 3 tareas mas importantes

## Revision Semanal (30 min)

1. Procesar inbox de tareas
2. Revisar progreso de proyectos
3. Analizar metricas de pipeline
4. Planificar outreach de la semana
5. Actualizar forecast de ventas

## Referencias Detalladas

- **Tareas y Proyectos**: `references/tasks-projects.md` - Estructura GTD, vistas, formulas
- **CRM y Pipeline**: `references/crm-pipeline.md` - Scoring ICP, etapas, metricas
- **Apollo Workflow**: `references/apollo-workflow.md` - Prospeccion completa, cadencias, templates
- **n8n Workflows**: `references/n8n-workflows.md` - Automatizaciones, nodos, ejemplos
