---
name: visualize-with-libraries
description: Renderiza diagramas BPMN usando iconos de carpetas locales ('icons' o 'librerias'). Detecta automáticamente carpetas de iconos en el proyecto. Genera JSON Excalidraw minimalista con coordenadas X/Y.
allowed-tools:
  - "Read"
  - "Write"
  - "Bash"
  - "glob"
  - "grep"
---

# Visualizer with Local Libraries

Esta skill renderiza diagramas BPMN utilizando iconos de carpetas locales encontradas en el proyecto del usuario.

## Características

- Detección automática de carpetas de iconos locales
- Soporte para extensiones: `.svg`, `.png`, `.jpg`, `.jpeg`
- Prioridad de búsqueda: `icons/` > `librerias/` > `libraries/`
- Fallback a emojis técnicos si no se encuentran iconos
- Estilo visual 60-30-10 para colores

## REGLAS ESTRICTAS DE GENERACIÓN EXCALIDRAW (CRÍTICO)

### Minimalismo JSON
- **PROHIBIDO** usar el tipo `freedraw`
- Usa únicamente tipos primitivos: `rectangle`, `diamond`, `text`, `arrow`
- Omite metadatos redundantes para que el archivo pese menos de 500 líneas

### Motor de Conexiones
- Toda línea (`type: "arrow"`) **DEBE** estar conectada lógicamente
- Usa **obligatoriamente** `startBinding` y `endBinding` apuntando a los IDs de origen y destino
- Ejemplo obligatorio de flecha:
```json
{
  "type": "arrow",
  "id": "arr_1",
  "startBinding": {"elementId": "origen_1", "focus": 0, "gap": 5},
  "endBinding": {"elementId": "destino_1", "focus": 0, "gap": 5},
  "roundness": {"type": 2}
}
```

### Anclaje Bidireccional (Contenedores de Texto)

Tienes estrictamente prohibido intentar calcular manualmente las coordenadas x e y para centrar los textos dentro de las figuras. Debes utilizar el sistema nativo de Contenedores de Excalidraw para garantizar que el texto quede perfectamente centrado y no se desborde.

**En la figura contenedora (rectangle, diamond, ellipse, etc.):**
Añade la propiedad `boundElements` con un array que contenga el ID del texto:

```json
{
  "id": "caja_paso_1",
  "type": "rectangle",
  "boundElements": [{ "type": "text", "id": "texto_paso_1" }]
}
```

**En el elemento de texto:**
Añade la propiedad `containerId` apuntando al ID de la figura:

```json
{
  "id": "texto_paso_1",
  "type": "text",
  "containerId": "caja_paso_1"
}
```

### Auto-Alineación del Texto

Todo elemento de texto dentro de un contenedor DEBE incluir:

```json
{
  "textAlign": "center",
  "verticalAlign": "middle"
}
```

### Visibilidad y Estilo de las Formas

Las figuras base no pueden ser transparentes ni tener bordes invisibles:

```json
{
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid"
}
```

### Estructura JSON Completa con Contenedor

```json
[
  {
    "id": "caja_paso_1",
    "type": "rectangle",
    "x": 100,
    "y": 100,
    "width": 150,
    "height": 80,
    "strokeColor": "#1e1e1e",
    "backgroundColor": "transparent",
    "fillStyle": "solid",
    "boundElements": [{ "type": "text", "id": "texto_paso_1" }]
  },
  {
    "id": "texto_paso_1",
    "type": "text",
    "text": "Registrar Lead",
    "x": 100,
    "y": 100,
    "width": 150,
    "height": 80,
    "fontSize": 18,
    "fontFamily": 5,
    "textAlign": "center",
    "verticalAlign": "middle",
    "containerId": "caja_paso_1"
  }
]
```

**IMPORTANTE**: 
- El texto debe tener las mismas coordenadas y dimensiones que su contenedor
- NO uses la fórmula manual de centrado (`estimatedWidth = text.length * fontSize * 0.5`)
- USA SIEMPRE el sistema de contenedores con `boundElements` + `containerId`

### Estructura JSON de Salida

```json
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {
      "id": "task_1",
      "type": "rectangle",
      "x": 100,
      "y": 100,
      "width": 120,
      "height": 60,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "boundElements": [{ "type": "text", "id": "text_1" }]
    },
    {
      "id": "text_1",
      "type": "text",
      "text": "Recibir Email",
      "x": 100,
      "y": 100,
      "width": 120,
      "height": 60,
      "fontSize": 16,
      "fontFamily": 5,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "task_1"
    },
    {
      "id": "arr_1",
      "type": "arrow",
      "startBinding": {"elementId": "task_1", "focus": 0, "gap": 5},
      "endBinding": {"elementId": "task_2", "focus": 0, "gap": 5},
      "roundness": {"type": 2}
    }
  ]
}
```

## Uso

Cuando el usuario quiera renderizar un diagrama BPMN y desee usar iconos locales:

1. La skill escanea el proyecto buscando carpetas `icons/`, `librerias/` o `libraries/`
2. Busca iconos que coincidan con los tipos de tareas BPMN
3. Genera el diagrama usando los iconos encontrados

### Estructura de carpetas de iconos

```
tu-proyecto/
├── icons/           # Prioridad 1
│   ├── db.svg
│   ├── user.png
│   └── api.jpg
├── librerias/        # Prioridad 2
│   └── ...
└── libraries/        # Prioridad 3
    └── ...
```

### Nombres de archivos de iconos

| Tipo de tarea | Archivo esperado |
|---------------|------------------|
| Service Task  | `service.svg`, `service.png` |
| User Task     | `user.svg`, `user.png` |
| Script Task  | `script.svg`, `script.png` |
| Manual Task  | `manual.svg`, `manual.png` |
| Send Task    | `send.svg`, `send.png` |
| Receive Task | `receive.svg`, `receive.png` |

## Instalación

npx skills add JefferCB1/skill-visualizer-direct
