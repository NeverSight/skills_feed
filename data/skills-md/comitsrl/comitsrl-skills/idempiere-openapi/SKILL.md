---
name: "idempiere-openapi"
description: "Definir y mantener contratos de API para iDempiere usando OpenAPI (3.1 preferido): paths, schemas, seguridad (OAuth2/JWT), ejemplos, versionado semver y artefactos derivados (stubs, Postman, contract tests). Usar para APIs POS, integraciones o portales."
---

# iDempiere OpenAPI Contract

## Objetivo

Producir una especificacion OpenAPI versionada y util como contrato entre:
- backend OSGi/Java,
- UI (ZK o frontend externo),
- clientes externos (POS, mobile, integraciones, middleware).

## Estructura sugerida (si el repo no tiene una)

- `openapi/` (specs versionadas)
- `postman/` (colecciones exportadas)
- `java/` (stubs/SDKs generados si aplica)
- `osgi/` (esqueleto de bundle/servicios)
- `db/migrations/` (migraciones necesarias)
- `tests/contract/` (contract tests)
- `docs/` (guia funcional/tecnica)

## Dominios comunes (baseline)

- `/auth/token`
- `/health`
- `/customers` (C_BPartner)
- `/products` (M_Product)
- `/inventory`
- `/sales/orders`
- `/shipments`
- `/invoices`
- `/payments`
- `/reports`
- `/webhooks`
- `/sync` (offline/batch)

## Workflow recomendado

1) Versionar el contrato
   - Usar semver estricto y un archivo por version.
2) Disenar schemas y mapping a iDempiere
   - Modelar IDs y referencias (AD_Client/AD_Org, C_BPartner, M_Product, etc).
   - Definir formato consistente de errores (4xx/5xx) y validaciones (422).
3) Disenar endpoints por dominio
   - Separar por bounded contexts (ventas, stock, finanzas, integraciones).
4) Seguridad
   - Documentar scopes/roles y aplicar `security` por operation.
   - No exponer datos sensibles (PCI/PII).
5) Validar y generar artefactos
   - Lint/validate de OpenAPI.
   - Generar stubs (Java) y coleccion Postman si el repo lo requiere.
   - Agregar contract tests contra mock o staging.
6) Integracion en OSGi
   - Definir servicios, transacciones y manejo de idempotencia.

## Checklist de salida

- [ ] Spec valida y versionada (semver).
- [ ] Ejemplos coherentes y errores documentados.
- [ ] Seguridad definida y aplicada.
- [ ] Artefactos derivados reproducibles (si aplican).

