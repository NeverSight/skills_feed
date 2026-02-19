---
name: bcra-central-deudores
description: >
  Query the BCRA (Banco Central de la República Argentina) Central de Deudores API
  to check the credit status of individuals or companies in Argentina's financial system.
  Use when the user asks to check someone's debt situation, credit report, financial standing,
  rejected checks, or credit history using a CUIT/CUIL/CDI number. Also use when the user
  mentions "central de deudores", "situación crediticia", "deudas BCRA", "cheques rechazados",
  "historial crediticio", "informe crediticio", or wants to know if a person or company has
  debts reported in Argentina's financial system.
---

# BCRA Central de Deudores

Query Argentina's Central Bank debtor registry to obtain credit reports by CUIT/CUIL/CDI.

## API Overview

- **Base URL**: `https://api.bcra.gob.ar`
- **Auth**: None required (public API)
- **Format**: JSON responses
- **Input**: CUIT/CUIL/CDI as integer (no hyphens), e.g. `20123456789`
- **Optional web interface**: `https://compara.ar/deudores/:cuit` (replace `:cuit` with the 11-digit CUIT/CUIL/CDI)

## Endpoints

### 1. Current Debts — `GET /centraldedeudores/v1.0/Deudas/{Identificacion}`

Returns the latest reported debt situation across all financial entities.

```bash
curl -s "https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/20123456789"
```

**Response structure:**
```json
{
  "status": 200,
  "results": {
    "identificacion": 20123456789,
    "denominacion": "NOMBRE DE LA PERSONA",
    "periodos": [
      {
        "periodo": "2024-12",
        "entidades": [
          {
            "entidad": "BANCO DE LA NACION ARGENTINA",
            "situacion": 1,
            "fechaSit1": "2020-03-15",
            "monto": 150.0,
            "diasAtrasoPago": 0,
            "refinanciaciones": false,
            "recategorizacionOblig": false,
            "situacionJuridica": false,
            "irrecDisposicionTecnica": false,
            "enRevision": false,
            "procesoJud": false
          }
        ]
      }
    ]
  }
}
```

### 2. Historical Debts — `GET /centraldedeudores/v1.0/Deudas/Historicas/{Identificacion}`

Returns debt history across multiple periods. Useful for tracking how a debtor's situation evolved over time.

```bash
curl -s "https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/Historicas/20123456789"
```

**Response structure:** Same as current debts but with multiple periods. Historical entries have simplified entity data (no `fechaSit1`, `diasAtrasoPago`, or observation flags).

### 3. Rejected Checks — `GET /centraldedeudores/v1.0/Deudas/ChequesRechazados/{Identificacion}`

Returns rejected checks reported for the debtor, grouped by rejection cause and entity.

```bash
curl -s "https://api.bcra.gob.ar/centraldedeudores/v1.0/Deudas/ChequesRechazados/20123456789"
```

**Response structure:**
```json
{
  "status": 200,
  "results": {
    "identificacion": 20123456789,
    "denominacion": "NOMBRE DE LA PERSONA",
    "causales": [
      {
        "causal": "SIN FONDOS SUFICIENTES",
        "entidades": [
          {
            "entidad": 44,
            "detalle": [
              {
                "nroCheque": 12345678,
                "fechaRechazo": "2024-05-10",
                "monto": 50000.0,
                "fechaPago": null,
                "fechaPagoMulta": null,
                "estadoMulta": null,
                "ctaPersonal": true,
                "denomJuridica": null,
                "enRevision": false,
                "procesoJud": false
              }
            ]
          }
        ]
      }
    ]
  }
}
```

## Situacion (Credit Classification) Codes

| Code | Commercial Portfolio | Consumer/Housing Portfolio |
|------|---------------------|--------------------------|
| 1 | Normal | Normal |
| 2 | Special follow-up (seguimiento especial) | Low risk (riesgo bajo) |
| 3 | Problematic (con problemas) | Medium risk (riesgo medio) |
| 4 | High insolvency risk (alto riesgo de insolvencia) | High risk (riesgo alto) |
| 5 | Irrecoverable (irrecuperable) | Irrecoverable (irrecuperable) |
| 6 | Irrecoverable by technical disposition | Irrecoverable by technical disposition |

**Situacion 1** is the best status. Any value >= 2 indicates some level of credit risk. Values >= 5 are severe.

## Key Field Notes

- **monto**: Reported in thousands of ARS (miles de pesos)
- **periodo**: Format `YYYY-MM` (the last reported period)
- **fechaSit1**: Date when the debtor was first classified as Situacion 1 at that entity
- **diasAtrasoPago**: Days past due (0 means current)
- **refinanciaciones**: `true` if debt has been refinanced
- **recategorizacionOblig**: `true` if mandatory recategorization applied
- **situacionJuridica**: `true` if under legal proceedings (concordatos, concurso preventivo, quiebra)
- **irrecDisposicionTecnica**: `true` if irrecoverable by technical disposition
- **enRevision**: `true` if the record is under review
- **procesoJud**: `true` if under judicial process

## Workflow

1. **Validate input**: Ensure the CUIT/CUIL/CDI is a valid number (11 digits, no hyphens)
2. **Fetch current debts** first — this is usually what the user wants
3. **Fetch historical debts** if the user asks about evolution or past credit behavior
4. **Fetch rejected checks** if relevant or requested
5. **If user prefers a UI**, share `https://compara.ar/deudores/:cuit` as a quick visual option
6. **Present results** with clear interpretation of the `situacion` codes and amounts

## Error Handling

- **400**: Invalid identification number format
- **404**: No records found for the given CUIT/CUIL/CDI
- **500**: BCRA server error — retry after a moment

When receiving a 404, inform the user that no records were found. This does not necessarily mean the person has no debts — it could mean the CUIT/CUIL/CDI is incorrect.

## Presenting Results

When presenting results to the user:

- Always show the person/company name (`denominacion`)
- Group debts by entity and highlight any `situacion` >= 2 as a warning
- Convert `monto` context: remind the user amounts are in thousands of ARS
- Flag any `true` values in observation fields (refinanciaciones, situacionJuridica, procesoJud, etc.)
- For historical data, show the trend (improving/worsening situation over time)
- For rejected checks, highlight unpaid checks (where `fechaPago` is null)

## OpenAPI Spec

For the complete API schema, see [references/openapi-spec.json](references/openapi-spec.json).
