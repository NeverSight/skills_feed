---
name: transcript-to-workflow
description: Convierte transcripciones de reuniones en JSON estructurado para automatización de workflows. Extrae actores, triggers, datos y pasos del flujo desde lenguaje natural.
---

# Transcript to Workflow

Este skill transforma transcripciones de reuniones desordenadas en JSON técnico estructurado, listo para implementar automatizaciones.

## Cuándo Usar Este Skill

Usa este skill cuando el usuario:

- Comparte una transcripción o resumen de una reunión
- Describe un proceso que quiere automatizar en lenguaje natural
- Menciona necesidades como "cuando llegue un correo...", "si pasa X entonces...", "quiero que el sistema haga..."
- Quiere convertir requisitos verbales en estructura técnica

##Qué Hace Este Skill

### Entrada
Transcripción de reunión en lenguaje natural, por ejemplo:
> "Hola, mira, necesitamos que cuando llegue un correo con una factura, el sistema la lea y la guarde en Drive. Si no tiene PDF, que avise por Slack."

### Salida
JSON estructurado con:
- **summary**: Resumen técnico de 1 línea
- **entities**: Actores, sistemas involucrados, tipo de trigger
- **workflow_data**: Inputs, outputs, happy path steps, excepciones detectadas

## Ejemplo de Salida

```json
{
  "summary": "Automatización de lectura de facturas por email con almacenamiento en Drive y notificaciones Slack",
  "entities": {
    "actors": ["Sistema", "Usuario"],
    "systems_involved": ["Email", "Drive", "Slack"],
    "trigger_type": "INSTANT",
    "trigger_detail": "Webhook al recibir email con factura"
  },
  "workflow_data": {
    "inputs": ["Email entrante", "Archivo PDF adjunto"],
    "outputs": ["Archivo en Drive", "Notificación en Slack"],
    "happy_path_steps": [
      "Recibir email con adjunto",
      "Detectar si es factura (PDF)",
      "Leer contenido del PDF",
      "Guardar en carpeta de Drive",
      "Enviar confirmación por Slack"
    ],
    "detected_exceptions": [
      "Si no hay PDF -> Notificar por Slack que falta documento"
    ]
  }
}
```

## Cómo Usar

Simplemente comparte la transcripción o descripción del proceso que quieres automatizar. El skill la procesará y devolverá la estructura JSON lista para implementar en tu herramienta de automatización favorita (n8n, Zapier, Make, etc.).

## Integración

Este skill puede integrarse con:
- n8n
- Zapier
- Make (Integromat)
- Pipedream
- Cualquier herramienta que soporte webhooks y JSON

## Reglas de Diseño Espacial (Grid System)

Al extraer el flujo de la transcripción y estructurar el proceso BPMN, debes asignar coordenadas matemáticas lógicas para facilitar la visualización posterior:

### Carriles (Eje Y)
Asigna una coordenada Y fija para cada actor/rol:
- Comercial: Y = 100
- Operaciones: Y = 400
- Cliente: Y = 700

(Incrementos de 300 en 300 para cada nuevo rol/actor)

### Secuencia de Tiempo (Eje X)
Cada paso del proceso debe avanzar en el eje X en incrementos de 300 a 400 píxeles:
- Paso 1: X = 100
- Paso 2: X = 450
- Paso 3: X = 800

(Incrementos de 300-400 entre cada paso)

### Salida con Coordenadas

La estructura debe incluir la propuesta de coordenadas X e Y para cada nodo:

```json
{
  "summary": "Automatización de lectura de facturas...",
  "entities": { ... },
  "workflow_data": {
    "inputs": [...],
    "outputs": [...],
    "happy_path_steps": [
      {
        "step": "Recibir email con adjunto",
        "x": 100,
        "y": 400,
        "actor": "Sistema"
      },
      {
        "step": "Detectar si es factura (PDF)",
        "x": 450,
        "y": 400,
        "actor": "Sistema"
      },
      {
        "step": "Guardar en carpeta de Drive",
        "x": 800,
        "y": 400,
        "actor": "Sistema"
      },
      {
        "step": "Enviar confirmación por Slack",
        "x": 1150,
        "y": 700,
        "actor": "Cliente"
      }
    ],
    "detected_exceptions": [...]
  }
}
```

## Instalación

npx skills add JefferCB1/skill-orchestrador@transcript-to-workflow

O si ya tienes el repo clonado localmente:

npx skills add .agents/skills/transcript-to-workflow --global
