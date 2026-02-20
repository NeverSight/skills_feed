---
name: cafci-fondos-comunes-argentina
description: >
  Consulta fondos comunes de inversion de Argentina (CAFCI) usando endpoints de lectura de Anduin.
  Usar cuando el usuario pida fondos por categoria, historico de un fondo, rendimiento por periodo,
  comparacion entre fondos, rankings de rendimiento, categorias, stats agregadas,
  fechas disponibles o ficha/detalle de un fondo.
---

# CAFCI Fondos Comunes Argentina

Consulta datos de Fondos Comunes de Inversion (FCI) para usuarios finales con endpoints read-only de Anduin.

## API Overview

- **Base URL**: `https://anduin.ferminrp.com`
- **Auth**: None required
- **Response format**: JSON
- **Docs source**: `https://anduin.ferminrp.com/docs`


## Endpoints de Lectura

### 1) Fondos (listado)

- `GET /api/v1/fci`
- Filtros:
  - `fecha` (`YYYY-MM-DD`)
  - `categoria_id` (2-11)
  - `horizonte` (`COR`, `MED`, `LAR`, `FLEX`)
  - `search`
  - `patrimonio_min`
  - `limit`, `offset`
  - `order_by` (`nombre`, `vcp`, `patrimonio`, `fecha`)
  - `order` (`asc`, `desc`)

Ejemplos:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci?limit=20&order_by=patrimonio&order=desc" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/fci?categoria_id=3&horizonte=MED&limit=10" | jq '.data.fondos'
```

### 2) Fondo puntual

- `GET /api/v1/fci/{nombre}`
- Query opcional: `fecha`

Ejemplo:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/1810%20Ahorro" | jq '.'
```

### 3) Historico de fondo

- `GET /api/v1/fci/{nombre}/historico`
- Query opcionales: `desde`, `hasta`, `intervalo` (`diario`, `semanal`, `mensual`), `limit`

Ejemplo:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/1810%20Ahorro/historico?intervalo=mensual&limit=12" | jq '.'
```

### 4) Rendimiento de fondo

- `GET /api/v1/fci/{nombre}/rendimiento`
- Query opcionales: `periodo` (`1d`, `7d`, `30d`, `90d`, `ytd`, `1y`), `fecha_base`

Ejemplo:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/1810%20Ahorro/rendimiento?periodo=30d" | jq '.'
```

### 5) Comparar fondos

- `GET /api/v1/fci/comparar`
- Query:
  - `fondos` (requerido, coma-separado, max 10)
  - `desde`, `hasta`
  - `metrica` (`vcp`, `patrimonio`, `rendimiento`)

Ejemplo:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/comparar?fondos=1810%20Ahorro,Adcap%20Balanceado&metrica=rendimiento" | jq '.'
```

### 6) Rankings

- `GET /api/v1/fci/rankings`
- Query tipicos: `periodo`, `categoria_id`, `orden`, `limit`

Ejemplo:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/rankings?periodo=30d&limit=10" | jq '.'
```

### 7) Categorias

- `GET /api/v1/fci/categorias`
- `GET /api/v1/fci/categorias/{id}`

Ejemplos:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/categorias" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/fci/categorias/3" | jq '.'
```

### 8) Estadisticas y fechas

- `GET /api/v1/fci/stats`
- `GET /api/v1/fci/fechas`

Ejemplos:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/stats" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/fci/fechas" | jq '.'
```

### 9) Ficha / detalle de fondo

- `GET /api/v1/fci/detalle/{identifier}`
- `identifier` admite `claseId` numerico o nombre de fondo URL-encoded.

Ejemplos:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/fci/detalle/4538" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/fci/detalle/1810%20Ahorro" | jq '.'
```

## Campos clave

- Estructura general de respuesta:
  - `success`
  - `data`
  - `timestamp`
- Campos frecuentes de fondos:
  - `fondoNombre`, `slug`, `categoriaId`, `categoriaNombre`, `horizonte`, `vcp`, `patrimonio`, `fecha`
- Historico:
  - `registros[]` con `fecha`, `vcp`, `ccp`, `patrimonio`
- Rendimiento:
  - `variacionPorcentual`, `variacionAbsoluta`, `vcpInicial`, `vcpFinal`, `fechaInicial`, `fechaFinal`
- Rankings:
  - `posicion`, `fondoNombre`, `categoriaNombre`, `rendimiento`
- Ficha/detalle:
  - clases, honorarios, cartera y rendimientos segun disponibilidad de origen

## Workflow

1. Detectar intencion del usuario:
   - Listado
   - Detalle
   - Historico
   - Rendimiento
   - Comparacion
   - Ranking
   - Ficha
2. Validar inputs minimos (`nombre`, `fondos`, fechas, periodo).
3. Ejecutar request con `curl -s` y parsear con `jq`.
4. Entregar primero snapshot breve y luego tabla comparativa.
5. En comparaciones/rankings, priorizar orden por rendimiento y contexto de fechas.
6. Si el nombre del fondo tiene espacios, usar URL-encoding (por ejemplo `1810%20Ahorro`).

## Error Handling

- **HTTP no exitoso**:
  - Informar codigo y endpoint consultado.
- **`success: false`**:
  - Propagar `error.message` si existe.
- **404 o fondo no encontrado**:
  - Dar mensaje claro y sugerir busqueda previa con `GET /api/v1/fci`.
- **JSON inesperado**:
  - Mostrar minimo crudo util y advertir inconsistencia.
- **Red/timeout**:
  - Reintentar hasta 2 veces con espera corta.

## Presenting Results

- Formato recomendado:
  - Resumen ejecutivo primero (quien rindio mejor/peor en el periodo)
  - Tabla breve luego con columnas relevantes
- Incluir siempre marco temporal (`fecha`, `desde/hasta`, `fechaFinal`).
- No emitir asesoramiento financiero; solo informar datos.

## Out of Scope

- Endpoints operativos de sync/status:
  - `/api/v1/fci/sync/status`
  - `/api/v1/fci/sync/categories`
  - `POST /api/v1/fci/sync*`
  - `POST /api/v1/fci/detalle/sync`
- Escritura o refresh de datos
- Recomendaciones de inversion

## OpenAPI Spec

Ver snapshot local en [references/openapi-spec.json](references/openapi-spec.json).
