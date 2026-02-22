---
name: postgresql-performance-expert
description: Optimizacion de PostgreSQL para Senior Full-Stack Developer. Usar cuando el usuario necesite diagnosticar queries lentos, optimizar performance de base de datos, disenar indices, resolver N+1 queries, o defender experiencia en optimizacion. Activa con palabras como PostgreSQL, query lento, performance, EXPLAIN, indice, N+1, optimizar base de datos, latencia. Especializado en aplicaciones SaaS con Node.js.
---

# PostgreSQL Performance Expert

Sistema para diagnosticar y resolver problemas de performance en PostgreSQL.

## Workflow de Diagnostico

### 1. Identificar el problema

```
SINTOMAS:
- Endpoint lento (>500ms)
- Timeouts en queries
- CPU/memoria alta en DB
- Conexiones agotadas

HERRAMIENTAS:
- EXPLAIN ANALYZE
- pg_stat_statements
- slow query log
- connection pool metrics
```

### 2. Proceso de optimizacion

```
1. MEDIR     → EXPLAIN ANALYZE con query real
2. IDENTIFICAR → Seq Scan? Nested Loop? Alto cost?
3. HIPOTESIS  → Falta indice? N+1? Over-fetching?
4. APLICAR    → Crear indice / reescribir query
5. VERIFICAR  → Re-ejecutar EXPLAIN, comparar
6. MONITOREAR → Observar en produccion
```

---

## EXPLAIN ANALYZE: Como Leerlo

### Ejecutar correctamente

```sql
-- Siempre con ANALYZE para tiempos reales
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM reservations
WHERE property_id = 123
  AND check_in >= '2024-01-01';
```

### Que buscar

```
MALO - Seq Scan en tabla grande:
Seq Scan on reservations  (cost=0.00..15432.00 rows=50000)
  Filter: (property_id = 123)
  Rows Removed by Filter: 49000
→ Solucion: agregar indice en property_id

MALO - Nested Loop con muchas filas:
Nested Loop  (cost=0.00..125000.00 rows=1000)
  -> Seq Scan on properties
  -> Index Scan on reservations (1000 loops)
→ Solucion: cambiar a Hash Join o agregar indice

BUENO - Index Scan:
Index Scan using idx_reservations_property
  Index Cond: (property_id = 123)
→ Usando indice correctamente
```

---

## Problemas Comunes + Soluciones

### N+1 Queries

```javascript
// MALO: N+1
const properties = await db('properties').select('*');
for (const prop of properties) {
  prop.reservations = await db('reservations')
    .where({ property_id: prop.id }); // N queries!
}

// BUENO: Eager loading
const properties = await db('properties')
  .select('properties.*')
  .leftJoin('reservations', 'properties.id', 'reservations.property_id');

// O con subquery
const properties = await db('properties').select('*');
const propIds = properties.map(p => p.id);
const reservations = await db('reservations')
  .whereIn('property_id', propIds);
// Agrupar en memoria
```

### Missing Index

```sql
-- Query lento
SELECT * FROM orders
WHERE user_id = 123 AND status = 'pending'
ORDER BY created_at DESC;

-- Agregar indice compuesto
CREATE INDEX idx_orders_user_status_created
ON orders (user_id, status, created_at DESC);

-- Verificar uso
EXPLAIN ANALYZE SELECT ...
-- Deberia mostrar Index Scan
```

### Over-fetching

```javascript
// MALO: traer todo
const users = await db('users').select('*');

// BUENO: solo lo necesario
const users = await db('users').select('id', 'name', 'email');

// MALO: sin limite
const logs = await db('audit_logs').where({ user_id: 123 });

// BUENO: con limite
const logs = await db('audit_logs')
  .where({ user_id: 123 })
  .orderBy('created_at', 'desc')
  .limit(100);
```

---

## Indices: Guia Rapida

### Tipos

```
B-tree (default): =, <, >, BETWEEN, ORDER BY
  CREATE INDEX idx_name ON table (column);

GIN: arrays, JSONB, full-text search
  CREATE INDEX idx_tags ON posts USING GIN (tags);

Partial: solo subset de filas
  CREATE INDEX idx_active ON users (email) WHERE active = true;

Covering: incluir columnas extra
  CREATE INDEX idx_orders ON orders (user_id) INCLUDE (total, status);
```

### Indice Compuesto: Orden Importa

```sql
-- Indice en (A, B, C)
CREATE INDEX idx ON table (a, b, c);

-- Funciona para:
WHERE a = 1
WHERE a = 1 AND b = 2
WHERE a = 1 AND b = 2 AND c = 3
WHERE a = 1 ORDER BY b

-- NO funciona para:
WHERE b = 2  -- Necesita A primero
WHERE c = 3  -- Necesita A y B primero
```

---

## Connection Pooling

```javascript
// Sin pooling: nueva conexion por query (lento, inseguro)
// Con pooling: reusar conexiones

// Knex.js config
const db = knex({
  client: 'pg',
  connection: {
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    // ...
  },
  pool: {
    min: 2,        // Conexiones minimas
    max: 10,       // Conexiones maximas
    acquireTimeoutMillis: 30000,
    idleTimeoutMillis: 30000
  }
});

// Monitorear pool
setInterval(() => {
  const pool = db.client.pool;
  console.log({
    used: pool.numUsed(),
    free: pool.numFree(),
    pending: pool.numPendingAcquires()
  });
}, 60000);
```

---

## Tu Experiencia: Script de Respuesta

```
"En HostelOS tuve un endpoint que tardaba 800ms. Esto es lo que hice:

1. MEDIR
   EXPLAIN ANALYZE mostro Seq Scan en tabla de 50K reservas

2. IDENTIFICAR
   Query filtraba por property_id y rango de fechas, pero
   no habia indice para esa combinacion

3. APLICAR
   CREATE INDEX idx_reservations_property_dates
   ON reservations (property_id, check_in, check_out);

4. RESULTADO
   Bajo a 50ms (94% mejora)

5. SIGUIENTE PROBLEMA
   Con mas datos, subio a 120ms. Agregue partial index:
   CREATE INDEX idx_active_reservations
   ON reservations (property_id, check_in)
   WHERE status = 'confirmed';

   Bajo a 35ms."
```

---

## Checklist de Performance

```
INDICES
[ ] Queries frecuentes tienen indices apropiados
[ ] Indices compuestos en orden correcto
[ ] Partial indices para subsets comunes
[ ] No hay indices duplicados o sin usar

QUERIES
[ ] Sin N+1 (usar eager loading)
[ ] SELECT solo columnas necesarias
[ ] LIMIT en queries grandes
[ ] Paginacion con cursor, no OFFSET

CONFIGURACION
[ ] Connection pooling configurado
[ ] shared_buffers apropiado (~25% RAM)
[ ] work_mem para queries complejas
[ ] Statement timeout configurado

MONITOREO
[ ] slow_query_log habilitado
[ ] pg_stat_statements instalado
[ ] Alertas para queries >1s
[ ] Dashboard de metricas DB
```
