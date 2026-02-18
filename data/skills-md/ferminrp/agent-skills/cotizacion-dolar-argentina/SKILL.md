---
name: cotizacion-dolar-argentina
description: >
  Consulta cotizaciones de dolar en Argentina usando DolarAPI.
  Usar cuando el usuario pida "dolar hoy", "dolar blue", "dolar oficial",
  "dolar bolsa", "MEP", "CCL", "dolar tarjeta", "dolar mayorista", "dolar cripto",
  o quiera comparar compra/venta y actualizacion de cotizaciones.
  Tambien usar cuando el usuario pida cotizacion de euro, real brasileno,
  peso chileno o peso uruguayo con endpoints de /v1/cotizaciones.
---

# Cotizacion Dolar Argentina

Consulta cotizaciones de dolar y monedas para Argentina con DolarAPI.

## API Overview

- **Base URL**: `https://dolarapi.com`
- **Auth**: None required
- **Response format**: JSON
- **Fuente**: DolarAPI endpoint publico
- **Timestamp**: `fechaActualizacion` viene en ISO UTC, por ejemplo `2026-02-17T13:59:00.000Z`

## Endpoints

### Dolares (lista y por tipo)

- `GET /v1/dolares`
- `GET /v1/dolares/{tipoCotizacion}`

Tipos admitidos para `{tipoCotizacion}`:

- `oficial`
- `blue`
- `bolsa`
- `contadoconliqui`
- `tarjeta`
- `mayorista`
- `cripto`

Ejemplos:

```bash
curl -s https://dolarapi.com/v1/dolares | jq '.'
curl -s https://dolarapi.com/v1/dolares/blue | jq '.'
```

### Otras monedas

- `GET /v1/cotizaciones`
- `GET /v1/cotizaciones/{codigoMoneda}`

Codigos admitidos para `{codigoMoneda}`:

- `eur`
- `brl`
- `clp`
- `uyu`

Ejemplos:

```bash
curl -s https://dolarapi.com/v1/cotizaciones | jq '.'
curl -s https://dolarapi.com/v1/cotizaciones/eur | jq '.'
```

## Valores admitidos

- `tipoCotizacion`: `oficial`, `blue`, `bolsa`, `contadoconliqui`, `tarjeta`, `mayorista`, `cripto`
- `codigoMoneda`: `eur`, `brl`, `clp`, `uyu`

Mapeos utiles para lenguaje del usuario:

- "MEP" -> `bolsa`
- "CCL" o "contado con liqui" -> `contadoconliqui`

## Campos clave

Campos base de respuesta:

- `moneda`
- `casa`
- `nombre`
- `compra`
- `venta`
- `fechaActualizacion`

Campo opcional observado:

- `variacion` (puede aparecer en algunos casos, por ejemplo `mayorista`)

## Workflow

1. Detectar intencion del usuario:
   - Dolar general o tipo especifico
   - Otra moneda (`eur`, `brl`, `clp`, `uyu`)
2. Elegir endpoint correcto segun la intencion.
3. Validar valor solicitado (`tipoCotizacion` o `codigoMoneda`).
4. Ejecutar request con `curl -s` y parsear con `jq`.
5. Mostrar resumen corto primero y detalle despues.
6. Incluir siempre `fechaActualizacion` en la respuesta.
7. Si hay multiples cotizaciones, presentar comparativa por `casa`.

## Error Handling

- **404 con body vacio**:
  - Ocurre cuando `tipoCotizacion` o `codigoMoneda` no existe.
  - Responder con mensaje claro: "tipo no soportado" o "moneda no soportada".
- **Falla de red/timeout**:
  - Reintentar hasta 2 veces con delay corto.
  - Si falla de nuevo, devolver endpoint consultado y error.
- **JSON inesperado**:
  - Mostrar minimo crudo util y aclarar inconsistencia del origen.

## Presenting Results

- Priorizar `compra`, `venta` y spread (`venta - compra`).
- Orden sugerido para dolares:
  - `oficial`, `blue`, `bolsa`, `contadoconliqui`, `mayorista`, `cripto`, `tarjeta`
- Aclarar timezone del timestamp (UTC en origen).
- No dar recomendaciones financieras; solo informar cotizaciones.

## Out of Scope

Esta skill **no** debe usar en v1:

- `/v1/ambito/dolares*`
- `/v1/estado`
- Endpoints de otros paises
