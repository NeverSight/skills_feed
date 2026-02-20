---
name: riesgo-pais-argentina
description: >
  Consulta riesgo pais de Argentina con serie historica desde Anduin API.
  Usar cuando el usuario pida "riesgo pais argentina", "ultimo riesgo pais",
  "serie historica de riesgo pais", "riesgo pais por fecha o periodo",
  o "evolucion del riesgo pais".
---

# Riesgo Pais Argentina

Consulta la serie historica y el ultimo dato de riesgo pais de Argentina.

## API Overview

- **Base URL**: `https://anduin.ferminrp.com`
- **Auth**: None required
- **Response format**: JSON
- **Endpoint principal**: `/api/v1/indices/riesgo-pais`
- **Timestamp de respuesta**: `timestamp`
- **Metadatos utiles**: `data.cached`, `data.fetchedAt`, `data.totalRegistros`

## Endpoint

- `GET /api/v1/indices/riesgo-pais`

Ejemplos:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/indices/riesgo-pais" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/indices/riesgo-pais" | jq '.data.datos[-1]'
curl -s "https://anduin.ferminrp.com/api/v1/indices/riesgo-pais" | jq '.data.datos | map(select(.fecha >= "2025-01-01" and .fecha <= "2025-12-31"))'
```

## Campos clave

- Top-level:
  - `success` (bool)
  - `timestamp` (ISO datetime)
- `data`:
  - `slug` (esperado: `riesgo-pais`)
  - `datos` (array de `{ fecha, valor }`)
  - `totalRegistros` (int)
  - `fetchedAt` (ISO datetime)
  - `cached` (bool)

## Workflow

1. Detectar intencion del usuario (ultimo dato, rango, serie completa o comparacion simple).
2. Llamar endpoint con `curl -s`.
3. Validar `success == true` y existencia de `data.datos`.
4. Si pide periodo, filtrar localmente con `jq` por `fecha`.
5. Responder primero con snapshot:
   - Ultimo `valor`
   - `fecha` del ultimo registro
   - `timestamp` o `fetchedAt`
6. Luego mostrar detalle breve en tabla (`fecha | valor`) segun pedido.
7. Mantener respuesta descriptiva, sin recomendaciones financieras.

## Error Handling

- **HTTP no exitoso**:
  - Reportar codigo HTTP y endpoint consultado.
- **`success: false`**:
  - Mostrar `error.message` si existe.
- **JSON invalido o inesperado**:
  - Mostrar salida minima cruda y advertir inconsistencia.
- **Red o timeout**:
  - Reintentar hasta 2 veces con espera corta.
- **Serie vacia**:
  - Informar "sin datos disponibles actualmente".

## Presenting Results

- Priorizar:
  - Ultimo dato de riesgo pais
  - Fecha del dato
  - Cantidad de registros usados
- Para multiples filas:
  - Tabla corta `fecha | valor`
- Aclarar fuente y tiempo de actualizacion (`timestamp` o `fetchedAt`).
- No emitir asesoramiento financiero o economico; solo informar datos.

## Out of Scope

Esta skill no debe usar en v1:

- `/api/v1/indices` (listado general)
- `/api/v1/indices/inflacion-mensual`
- `/api/v1/indices/icl`
- `/api/v1/indices/uva`
- Cualquier endpoint fuera de `riesgo-pais`
