---
name: "idempiere-db"
description: "Disenar y aplicar cambios de base de datos y Data Dictionary para iDempiere y plugins: tablas/columnas/indices, metadata AD_*, migraciones PostgreSQL, performance y rollback. Usar cuando un cambio requiera actualizar schema o diccionario."
---

# iDempiere DB (Diccionario + Migraciones)

## Objetivo

Entregar cambios de DB/diccionario que:
- sean repetibles (dev/stage/prod),
- respeten convenciones iDempiere (EntityType, AD_Client/AD_Org, auditoria),
- tengan verificacion clara y plan de rollback.

## Recordatorios iDempiere (para cambios estructurales)

- Objetos del plugin deben tener `EntityType` del plugin (no usar `D`/core).
- Tablas transaccionales suelen requerir columnas multi-tenant/auditoria: `AD_Client_ID`, `AD_Org_ID`, `IsActive`, `Created`, `CreatedBy`, `Updated`, `UpdatedBy`.
- Para cambios que impactan performance: definir indices y validar con `EXPLAIN` en consultas reales.

## Workflow recomendado

1) Identificar el tipo de cambio
   - DDL (tabla/columna/index), metadata AD_*, data fix, o combinacion.
2) Definir compatibilidad
   - Version destino, si hay datos existentes, y estrategia sin downtime (si aplica).
3) Preparar migracion
   - Escribir scripts idempotentes cuando sea posible.
   - Incluir defaults/backfill para columnas nuevas si corresponde.
4) Verificar en DB limpia + DB con datos
   - Aplicar sobre una DB nueva.
   - Aplicar sobre un dump/backup representativo.
5) Validar en iDempiere
   - Revisar que el diccionario refleja el cambio y que la UI/proceso funciona.

## Checklist de salida

- [ ] Scripts o mecanismo de migracion definidos y repetibles.
- [ ] EntityType correcto para objetos del plugin.
- [ ] Probado en PostgreSQL (y en la DB objetivo del cliente si difiere).
- [ ] Documentado: upgrade, rollback y riesgos.

