---
name: inflacion-argentina-ipc
description: >
  Consulta IPC de Argentina con la serie de inflacion mensual desde Anduin API.
  Usar cuando el usuario pida "inflacion argentina", "ipc argentina", "inflacion mensual",
  "ultimo dato de inflacion", "serie historica de inflacion", "inflacion por fecha",
  "inflacion por periodo" o "variacion mensual ipc".
---

# Inflacion Argentina IPC

Consulta la serie historica y el ultimo dato de inflacion mensual (IPC) en Argentina.

## API Overview

- **Base URL**: `https://anduin.ferminrp.com`
- **Auth**: None required
- **Response format**: JSON
- **Endpoint principal**: `/api/v1/indices/inflacion-mensual`
- **Timestamp de respuesta**: `timestamp`
- **Metadatos utiles**: `data.cached`, `data.fetchedAt`, `data.totalRegistros`

## Endpoint

- `GET /api/v1/indices/inflacion-mensual`

Ejemplos:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/indices/inflacion-mensual" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/indices/inflacion-mensual" | jq '.data.datos[-1]'
curl -s "https://anduin.ferminrp.com/api/v1/indices/inflacion-mensual" | jq '.data.datos | map(select(.fecha >= "2025-01-01" and .fecha <= "2025-12-31"))'
```

## Campos clave

- Top-level:
  - `success` (bool)
  - `timestamp` (ISO datetime)
- `data`:
  - `slug` (esperado: `inflacion-mensual`)
  - `datos` (array de `{ fecha, valor }`)
  - `totalRegistros` (int)
  - `fetchedAt` (ISO datetime)
  - `cached` (bool)

## Workflow

1. Detectar intencion del usuario (ultimo dato, rango, serie completa o comparacion simple).
2. Llamar el endpoint con `curl -s`.
3. Validar `success == true` y existencia de `data.datos`.
4. Si el usuario pide periodo, filtrar localmente con `jq` por `fecha`.
5. Responder primero con snapshot:
   - Ultimo `valor`
   - `fecha` del ultimo registro
   - `timestamp` o `fetchedAt`
6. Luego mostrar detalle tabular corto (`fecha`, `valor`) segun el pedido.
7. Mantener respuesta descriptiva, sin recomendaciones financieras.

## Error Handling

- **HTTP no exitoso**:
  - Informar codigo HTTP y endpoint consultado.
- **`success: false`**:
  - Mostrar `error.message` si existe.
- **JSON invalido o inesperado**:
  - Mostrar salida minima cruda y aclarar inconsistencia.
- **Red o timeout**:
  - Reintentar hasta 2 veces con espera corta.
- **Serie vacia**:
  - Informar "sin datos disponibles actualmente".

## Presenting Results

- Priorizar:
  - Ultimo dato de IPC mensual
  - Fecha del dato
  - Cantidad de registros considerados
- Si hay multiples filas, usar tabla breve:
  - `fecha | valor`
- Aclarar fuente y tiempo de actualizacion (`timestamp` o `fetchedAt`).
- No emitir asesoramiento financiero o economico; solo informar datos.

## Out of Scope

Esta skill no debe usar en v1:

- `/api/v1/indices` (listado general)
- `/api/v1/indices/riesgo-pais`
- `/api/v1/indices/icl`
- `/api/v1/indices/uva`
- Cualquier endpoint fuera de `inflacion-mensual`
