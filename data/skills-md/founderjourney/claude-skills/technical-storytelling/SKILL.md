---
name: technical-storytelling
description: Sistema para convertir logros tecnicos en narrativas que comunican senioridad e impacto. Usar cuando el usuario necesite escribir sobre sus proyectos, preparar presentaciones tecnicas, documentar decisiones de arquitectura, o comunicar complejidad a audiencias no-tecnicas. Activa con palabras como explicar proyecto, presentacion, documentar, caso de estudio, blog tecnico, conferencia. Especializado en developers senior que necesitan comunicar impacto business.
---

# Technical Storytelling

Sistema para convertir complejidad tecnica en narrativas que comunican senioridad, impacto y expertise.

## El Framework IMPACT

```
I - Issue (El problema de negocio)
M - Metrics (Numeros del problema)
P - Process (Tu approach tecnico)
A - Action (Lo que implementaste)
C - Consequences (Resultados medibles)
T - Takeaways (Lecciones aprendidas)
```

---

## Transformando Proyectos en Historias

### Tu Proyecto: HostelOS

#### Version Junior (NO hacer)

```
"Hice un sistema de reservas para hostels con React y Node.js.
Tiene un calendario y se conecta con Booking.com."
```

#### Version Senior (HACER)

```
"HostelOS resuelve el problema de fragmentacion de canales
en la industria hostelera. Los hostels manejan reservas de
5-10 fuentes diferentes - Booking, Expedia, directas, walk-ins -
y el overbooking les cuesta en promedio $2,000/mes por
reservas perdidas y compensaciones.

Disene una arquitectura multi-tenant donde cada hostel tiene
su instancia aislada pero comparte infraestructura. El challenge
principal fue sincronizar disponibilidad en tiempo real con
APIs de terceros que tienen diferentes modelos de datos y
tasas de fallo.

Implemente un Channel Manager con reconciliacion eventual,
usando webhooks cuando estan disponibles y polling inteligente
como fallback. Para iCal (que es inherentemente poll-based),
desarrolle un sistema de diff que detecta cambios reales vs
actualizaciones cosmeticas.

El resultado: +1000 usuarios activos, 99.2% uptime, y reduccion
de overbooking en 87% para los hostels que lo usan correctamente."
```

### Tu Proyecto: Digitaliza

#### Version Junior

```
"Plataforma de facturacion electronica con integracion bancaria."
```

#### Version Senior

```
"Digitaliza ataca un problema de compliance en LATAM: las
empresas necesitan emitir facturas electronicas certificadas
por el gobierno, pero las soluciones existentes son legacy,
caras, y no se integran bien con sistemas modernos.

El challenge tecnico principal fue la integracion bancaria.
Los bancos colombianos tienen APIs legacy, con disponibilidad
intermitente y documentacion inconsistente. Un fallo en el
procesamiento de pago puede significar una factura duplicada
o perdida de dinero.

Implemente un sistema de reconciliacion con tres niveles:
1. Webhook para notificaciones real-time cuando funciona
2. Polling con backoff exponencial como fallback
3. Reconciliacion batch nocturna para catch-all

Agregue idempotency keys en todas las transacciones y un
dead letter queue para casos edge que requieren intervencion
manual.

Resultado: 400+ clientes activos, cero transacciones perdidas
en 18 meses, tiempo de reconciliacion reducido de 2 dias a
15 minutos."
```

---

## Templates por Contexto

### Para Entrevistas Tecnicas

```
ESTRUCTURA (2-3 minutos):

"En [Proyecto], enfrentamos [problema de negocio] que
afectaba [metrica especifica].

Evalué [2-3 opciones] y elegí [solucion] porque [razones
tecnicas especificas].

La implementacion involucró [tecnologias/patterns principales].
El challenge más interesante fue [problema especifico] - lo
resolví con [approach].

El resultado fue [metricas de impacto]. Lo que aprendí es
[insight aplicable]."

EJEMPLO:
"En HostelOS, enfrentamos el problema de sincronización de
disponibilidad entre múltiples canales. Un hostel típico
perdía $2K/mes por overbooking.

Evalué event sourcing completo vs eventual consistency con
reconciliación. Elegí el segundo porque los canales externos
no soportan eventos - trabajan con snapshots de estado.

Implementé un Channel Manager con webhooks como primary y
polling inteligente como fallback. Para iCal, desarrollé un
sistema de diff que evita actualizaciones innecesarias.

Resultado: 87% reducción en overbooking, 99.2% uptime."
```

### Para Documentacion Tecnica (ADR)

```
# ADR-001: Estrategia de Multi-Tenancy

## Status
Accepted

## Context
HostelOS necesita servir múltiples hostels con datos aislados
pero infraestructura compartida para mantener costos bajos.

## Decision
Implementar modelo "Pool" con tenant_id en cada tabla y
Row Level Security (RLS) en PostgreSQL.

## Alternatives Considered

### Option A: Database per tenant (Silo)
- Pros: Aislamiento perfecto, facil backup per-tenant
- Cons: Costo O(n), complejidad operacional, migrations dolorosas
- Rejected: No escala economicamente para SMB market

### Option B: Schema per tenant
- Pros: Buen aislamiento, queries simples
- Cons: Connection pooling limitado, migrations complejas
- Rejected: Complejidad operacional alta

### Option C: Shared tables with tenant_id (Pool) ✓
- Pros: Costo constante, simple ops, migrations faciles
- Cons: Requiere disciplina en queries, riesgo de data leaks
- Accepted: Con RLS para seguridad adicional

## Consequences
- Todas las queries deben incluir tenant_id
- RLS policies enforced a nivel DB como safety net
- Monitoring de queries sin tenant_id filter
- Backups son de toda la DB, restore granular requiere tooling
```

### Para Blog/Conferencias

```
ESTRUCTURA:

1. HOOK (problema relatable)
   "Has tenido ese momento donde el deploy de Friday arruina
   tu weekend? En HostelOS, un bug de sincronización nos
   costó 47 reservas duplicadas en un fin de semana."

2. CONTEXTO (por qué importa)
   "Los Channel Managers manejan la disponibilidad de hoteles
   en múltiples plataformas. Cuando fallan, los hostels hacen
   overbooking y pierden dinero y reputación."

3. JOURNEY (tu proceso)
   "Nuestra primera versión era naive: sync cada 5 minutos.
   Funcionaba hasta que no funcionaba..."

4. SOLUCION (tecnica pero accesible)
   "Implementamos tres capas de defensa:
   - Webhooks cuando están disponibles
   - Polling con backoff inteligente
   - Reconciliación eventual como safety net"

5. RESULTADOS (numeros)
   "De 47 overbookings/mes a 2. De 94% uptime a 99.2%."

6. TAKEAWAY (accionable)
   "La lección: en integraciones externas, diseña para el
   failure mode, no para el happy path."
```

---

## Comunicando a Audiencias No-Tecnicas

### Traduccion de Conceptos

```
TECNICO                  | PARA STAKEHOLDERS
-------------------------|----------------------------------
Multi-tenant             | Multiples clientes en una plataforma
                         | compartiendo costos
                         |
API rate limiting        | El proveedor solo permite X
                         | llamadas por minuto
                         |
Eventual consistency     | Los datos se sincronizan en segundos,
                         | no instantaneamente
                         |
Idempotency              | Si algo falla y se reintenta, no
                         | se duplica la accion
                         |
Technical debt           | Atajos que tomamos para entregar
                         | rapido, pero que cuestan despues
                         |
Horizontal scaling       | Agregar mas servidores cuando
                         | hay mas usuarios
```

### Script para Updates de Proyecto

```
PARA PRODUCT/BUSINESS:

"Esta semana completamos [feature] que permite [beneficio
para usuarios].

El challenge principal fue [problema en terminos simples].
Lo resolvimos [approach simplificado].

Esto nos da [beneficio tangible: velocidad, costo, capacidad].

La proxima semana nos enfocamos en [siguiente prioridad]."

EJEMPLO:
"Esta semana completamos la integracion con Banco X que
permite pagos automaticos para facturas.

El challenge principal fue que el banco tiene sistemas
antiguos con disponibilidad intermitente. Implementamos
un sistema que reintenta automaticamente y reconcilia
todas las noches.

Esto nos da cero pagos perdidos y reduce trabajo manual
de 2 horas/dia a 15 minutos.

La proxima semana nos enfocamos en el dashboard de reportes."
```

---

## Metricas que Importan

### Framework para Cuantificar Impacto

```
BUSCAR NUMEROS EN:

1. ESCALA
   - Usuarios activos
   - Transacciones/dia
   - Datos procesados

2. MEJORA
   - % reduccion de errores
   - % mejora en velocidad
   - % ahorro de costos

3. RELIABILITY
   - Uptime %
   - Tiempo de respuesta p99
   - Incidentes/mes

4. BUSINESS
   - Revenue impactado
   - Clientes ganados/retenidos
   - Tiempo ahorrado

SI NO TIENES NUMEROS EXACTOS:
- Estimar orden de magnitud
- Usar comparativos ("redujo a la mitad")
- Describir el before/after cualitativo
```

### Ejemplos de Metricas Bien Presentadas

```
DEBIL:
"Mejore la performance del sistema"

FUERTE:
"Reduje el tiempo de respuesta del endpoint de busqueda
de 800ms a 50ms (94% mejora) agregando un indice compuesto
en PostgreSQL"

DEBIL:
"Implemente integraciones con varios servicios"

FUERTE:
"Integre 6 canales de distribucion (Booking, Expedia, Airbnb,
Hostelworld + 2 locales), procesando 2,000+ actualizaciones
de disponibilidad diarias con 99.8% de exito"

DEBIL:
"El sistema es escalable"

FUERTE:
"La arquitectura soporta 10x crecimiento sin cambios:
actualmente 1,000 usuarios, probado con 10,000 en staging"
```

---

## Tus Historias Listas

### Historia 1: El Overbooking que Cambio Todo

```
"Un hostel en Cartagena perdio $3,000 en un fin de semana
por overbooking. Tenian reservas en Booking, Expedia, y
directas - ninguna se sincronizaba bien.

Ese fue el momento que definio la arquitectura de HostelOS.
En lugar de un sync simple, disene un Channel Manager con
tres niveles de confiabilidad...

[continua con detalles tecnicos y resultado]"
```

### Historia 2: La Integracion Bancaria Imposible

```
"El banco dijo que su API 'funcionaba'. Lo que no dijeron
es que caia 3 veces por semana, no tenia documentacion
actualizada, y los errores venian en espanol coloquial.

Digitaliza necesitaba esta integracion para funcionar.
Asi que construi un sistema que asumia que todo iba a fallar...

[continua con solucion y metricas]"
```

### Historia 3: De 800ms a 50ms

```
"El endpoint de busqueda de reservas tardaba 800ms. Para
un calendario que hace 10+ llamadas para renderizar, eso
era inaceptable.

EXPLAIN ANALYZE revelo un Seq Scan en 50,000 filas.
La solucion parecia obvia - agregar un indice. Pero el
indice simple no funcionaba porque...

[continua con detalle tecnico de indice compuesto]"
```

---

## Checklist de Storytelling

```
ANTES DE PRESENTAR/ESCRIBIR:
[ ] Tengo el problema de NEGOCIO claro (no solo tecnico)
[ ] Tengo al menos 2 metricas concretas
[ ] Puedo explicar por que MI solucion vs alternativas
[ ] Tengo un takeaway accionable
[ ] Ajuste el nivel tecnico a mi audiencia

ESTRUCTURA:
[ ] Hook que engancha (problema relatable)
[ ] Contexto suficiente (pero no excesivo)
[ ] Journey con obstaculos (muestra expertise)
[ ] Solucion con razonamiento (no solo que, sino por que)
[ ] Resultados medibles
[ ] Leccion aplicable

REVISION:
[ ] Elimine jargon innecesario
[ ] Cada oracion agrega valor
[ ] Fluye como historia, no como lista
[ ] Suena como YO, no como template generico
```
