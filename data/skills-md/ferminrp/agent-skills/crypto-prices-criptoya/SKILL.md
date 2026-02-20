---
name: crypto-prices-criptoya
description: >
  Consulta cotizaciones de criptomonedas con CriptoYa por exchange y en forma agregada.
  Usar cuando el usuario pida "precio BTC en ARS", "cotizacion USDT", "precio ETH en USD",
  "mejor precio por exchange", "comparar exchanges", "precio en belo/ripio/lemon/binance/bybit",
  o cuando pida comisiones de retiro y fees por red.
---

# Crypto Prices CriptoYa

Consulta cotizaciones cripto de CriptoYa por exchange, cotizacion general y comisiones de retiro.

## API Overview

- **Base URL**: `https://criptoya.com`
- **Auth**: None required
- **Response format**: JSON en respuestas validas
- **Nota operativa**: para pares o valores invalidos la API puede devolver texto plano `"Invalid pair"` con HTTP `200`
- **Timestamp**: campo `time` en unix epoch

## Endpoints

- `GET /api/{exchange}/{coin}/{fiat}/{volumen}`
- `GET /api/{coin}/{fiat}/{volumen}`
- `GET /api/fees`

Ejemplos:

```bash
curl -s "https://criptoya.com/api/BTC/ARS/0.1" | jq '.'
curl -s "https://criptoya.com/api/belo/BTC/ARS/0.1" | jq '.'
curl -s "https://criptoya.com/api/fees" | jq '.'
```

## Valores admitidos

### `coin`

`BTC, ETH, USDT, USDC, DAI, UXD, USDP, WLD, BNB, SOL, XRP, ADA, AVAX, DOGE, TRX, LINK, DOT, MATIC, SHIB, LTC, BCH, EOS, XLM, FTM, AAVE, UNI, ALGO, BAT, PAXG, CAKE, AXS, SLP, MANA, SAND, CHZ`

### `fiat`

`ARS, BRL, CLP, COP, MXN, PEN, VES, BOB, UYU, DOP, PYG, USD, EUR`

### `exchange`

`cryptomkt, letsbit, belo, bitsoalpha, bybit, ripio, lemoncash, fiwind, tiendacrypto, eluter, universalcoins, buenbit, binance, huobip2p, bitso, eldoradop2p, lemoncashp2p, kucoinp2p, decrypto, mexcp2p, pluscrypto, cocoscrypto, bitgetp2p, cryptomktpro, satoshitango, coinexp2p, paydecep2p, binancep2p, bingxp2p, ripioexchange, astropay, dolarapp, vibrant, wallbit, vitawallet, weexp2p, trubit, okexp2p, bybitp2p, saldo, p2pme, airtm`

### `volumen`

Numero decimal usando punto: `0.1`, `1`, `250.5`.

## Campos clave

- Cotizacion por exchange:
  - `ask`, `totalAsk`, `bid`, `totalBid`, `time`
- Cotizacion general:
  - Objeto por exchange con los mismos campos (`ask`, `totalAsk`, `bid`, `totalBid`, `time`)
- Fees:
  - Estructura anidada `exchange -> coin -> red -> fee`

## Workflow

1. Detectar intencion:
   - Cotizacion general
   - Cotizacion por exchange
   - Fees de retiro
2. Validar inputs requeridos:
   - `coin`, `fiat`, `volumen`
   - `exchange` cuando aplique
3. Ejecutar `curl -s` y parsear con `jq`.
4. Si la respuesta es `"Invalid pair"` o no es JSON esperado, informar parametros invalidos.
5. Presentar primero resumen accionable:
   - Mejor `bid`
   - Mejor `ask`
   - Spread relevante
6. Presentar detalle:
   - Top exchanges y `time` por cotizacion

## Error Handling

- **Parametro invalido / par no soportado**:
  - Detectar texto `"Invalid pair"` aunque HTTP sea `200`.
  - Informar claramente que la combinacion solicitada no esta soportada.
- **Red/timeout**:
  - Reintentar hasta 2 veces con espera corta.
  - Si falla, devolver mensaje claro con endpoint consultado.
- **JSON inesperado**:
  - Mostrar minimo crudo util y aclarar inconsistencia del origen.

## Presenting Results

- Priorizar:
  - Mejor precio de compra (`ask`)
  - Mejor precio de venta (`bid`)
  - Spread (`ask - bid`) por exchange
- En comparativas:
  - Tabla corta por exchange con `ask`, `bid`, `totalAsk`, `totalBid`, `time`
- Aclarar:
  - Datos informativos y sin recomendacion financiera

## Out of Scope

Esta skill no debe usar en v1:

- `/api/dolar`
- `/api/cer`
- `/api/uva`
- `/api/bancostodos`
