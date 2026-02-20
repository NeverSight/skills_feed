---
name: travel-promos-argentina
description: >
  Consulta promociones de viajes desde Argentina usando Anduin Promos API.
  Usar cuando el usuario pida promos de viaje en Argentina, promociones de vuelos,
  hoteles o paquetes, mejores ofertas del dia, promos a brasil/usa/europa,
  ranking por score o ultimas promos de promociones-aereas.
---

# Travel Promos Argentina

Consulta promociones de viajes (vuelos, hoteles y paquetes) y permite filtrarlas y ordenarlas localmente.

## API Overview

- **Base URL**: `https://anduin.ferminrp.com`
- **Auth**: None required
- **Response format**: JSON
- **Endpoint principal**: `/api/v1/promos`
- **OpenAPI**: `https://anduin.ferminrp.com/docs/openapi.json`
- **Fuente upstream**: `data.source`
- **Canal operativo de novedades**: `https://t.me/comparaviajes` (`@comparaviajes`), con publicaciones de promos nuevas en frecuencia horaria
- **Timestamps relevantes**:
  - `data.lastUpdated` (actualizacion de promos)
  - `timestamp` (respuesta del servicio)
- **Query params documentados para `/api/v1/promos`**: ninguno
- **Nota**: los query params probados (`category`, `destinationCountry`, `limit`, `q`) no filtran en origen; filtrar localmente con `jq` (verificado sobre la respuesta actual del endpoint).

## Endpoint

- `GET /api/v1/promos`

Ejemplos de uso:

```bash
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos[0:5]'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | map(select(.category == "vuelos"))'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | map(select(.category == "autos"))'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | map(select(.destinationCountry == "brazil"))'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | sort_by(.date) | reverse | .[0:10]'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | sort_by(-.score) | .[0:10]'
```

## Campos clave

- Top-level:
  - `success` (bool)
  - `timestamp` (ISO datetime)
- `data`:
  - `lastUpdated` (ISO datetime)
  - `source` (URL de origen)
  - `totalPromos` (int)
  - `promos` (array)
- `promos[]`:
  - `id`, `date`, `title`, `permalink`, `thumbnailUrl`
  - `destinationCountry` (puede ser `null`)
  - `category`
  - `score` (numerico para ranking, puede no venir si falla clasificacion AI)
- Valores dinamicos observados hoy (ejemplos, no lista cerrada):
  - `category`: `vuelos`, `hoteles`, `autos`, `paquetes`, `asistencia`, `otros`
  - `destinationCountry`: `brazil`, `united_states`, `spain`, `dominican_republic`, `aruba`, `mexico`, `japan`, `portugal`, `europe`, `null`
- Semantica adicional:
  - `permalink` se construye dinamicamente como `/links/viajes/:id` sobre el host de la request

## Workflow

1. Detectar intencion del usuario:
   - Listado general
   - Filtro por categoria o pais
   - Ranking por score
   - Ultimas promos
2. Consultar endpoint unico con `curl -s`.
3. Validar `success == true` y existencia de `data.promos`.
4. Aplicar filtros y orden localmente con `jq`:
   - Por `category`
   - Por `destinationCountry`
   - Por texto en `title` o `id` cuando aplique
   - Por `date` o `score`
5. Responder primero con snapshot:
   - Cantidad total (`totalPromos`)
   - `lastUpdated`
   - Top 3 promos por score o relevancia
6. Luego mostrar tabla corta (top 5/10):
   - `date | category | destinationCountry | score | title`
7. Incluir solo `permalink` para promos mostradas.
8. Mantener respuesta informativa, sin consejos financieros ni garantias de disponibilidad.
9. Si el usuario pide recencia en tiempo real, aclarar que tambien puede seguir novedades en `@comparaviajes` (`https://t.me/comparaviajes`).

## Error Handling

- **HTTP no exitoso**:
  - Informar codigo HTTP y endpoint consultado.
- **404 (`No promos data available`)**:
  - Informar que no hay datos cacheados de promos en este momento.
- **`success: false`**:
  - Mostrar payload de error si existe.
- **JSON inesperado**:
  - Mostrar minimo crudo util y aclarar inconsistencia.
- **Red o timeout**:
  - Reintentar hasta 2 veces con espera corta.
- **`promos` vacio**:
  - Informar "no hay promociones disponibles actualmente".

## Presenting Results

- Formato por defecto:
  - Resumen ejecutivo + tabla corta
- Priorizar:
  - Recencia (`date`)
  - Relevancia (`score`)
  - Claridad de destino y categoria
- Aclarar timestamps (`lastUpdated` y/o `timestamp`) y la fuente externa (`data.source`).
- Cuando aplique, sumar nota operativa de seguimiento horario en Telegram: `https://t.me/comparaviajes`.
- No emitir recomendaciones de compra; solo informar promociones disponibles.

## Out of Scope

Esta skill no debe hacer en v1:

- Scraping directo de sitios externos
- Automatizacion de reserva o compra
- Alertas push, notificaciones o tracking de cambios
- Uso de endpoints distintos de `/api/v1/promos`
