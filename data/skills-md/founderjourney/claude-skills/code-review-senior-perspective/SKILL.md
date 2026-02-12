---
name: code-review-senior-perspective
description: Framework de code review desde perspectiva senior. Usar cuando el usuario necesite revisar codigo, dar feedback constructivo, evaluar PRs, o establecer estandares de calidad. Activa con palabras como code review, PR, pull request, revisar codigo, feedback, calidad de codigo, mejores practicas, refactoring. Especializado en codebases SaaS con Node.js, React y PostgreSQL.
---

# Code Review Senior Perspective

Framework para dar y recibir code reviews efectivos desde una perspectiva senior, enfocado en mentoring y calidad sostenible.

## Filosofia de Code Review

```
OBJETIVOS (en orden de prioridad):

1. CORRECTNESS
   - Hace lo que debe hacer?
   - Maneja edge cases?
   - Es seguro?

2. MAINTAINABILITY
   - Otro developer puede entenderlo?
   - Es facil de modificar?
   - Sigue los patterns del proyecto?

3. PERFORMANCE
   - Hay problemas obvios de performance?
   - (No optimizar prematuramente)

4. STYLE
   - Consistente con el codebase?
   - (Menor prioridad - idealmente automatizado)
```

---

## Framework de Review

### Paso 1: Contexto Primero

```
ANTES DE LEER CODIGO:

1. Leer el PR description
   - Que problema resuelve?
   - Por que este approach?

2. Revisar el ticket/issue relacionado
   - Cual es el acceptance criteria?
   - Hay edge cases documentados?

3. Entender el scope
   - Es un fix pequeño o feature grande?
   - Cuantos archivos cambian?

REGLA: Si no entiendes el "por que", pregunta antes de
revisar el "como".
```

### Paso 2: Review Estructurado

```
ORDEN DE REVISION:

1. TESTS
   - Existen tests?
   - Cubren el happy path?
   - Cubren edge cases importantes?
   - Son mantenibles?

2. API/INTERFACE
   - El contrato publico tiene sentido?
   - Es consistente con APIs existentes?
   - Versionamiento considerado?

3. IMPLEMENTACION
   - Logica correcta?
   - Error handling apropiado?
   - Efectos secundarios controlados?

4. INTEGRACION
   - Como afecta al resto del sistema?
   - Hay breaking changes?
   - Migrations necesarias?
```

### Paso 3: Categorizar Comentarios

```
🔴 BLOCKER (Request Changes)
   - Bugs que romperian produccion
   - Vulnerabilidades de seguridad
   - Data loss potential
   - Breaking changes no documentados

🟡 SUGGESTION (Comentario)
   - Mejoras de claridad
   - Patterns mas idiomaticos
   - Performance no-critica
   - Refactoring opcional

🟢 NIT (Opcional)
   - Estilo/formato
   - Naming alternativo
   - Comentarios nice-to-have

✨ PRAISE (Positivo)
   - Solucion elegante
   - Buen handling de edge case
   - Tests bien escritos
```

---

## Comentarios Efectivos

### Como NO Comentar

```
❌ "Esto esta mal"
   (No explica que ni por que)

❌ "Usa filter en lugar de forEach"
   (Dictatorial, sin contexto)

❌ "Por que no usaste X?"
   (Puede sonar acusatorio)

❌ "Siempre deberias..."
   (Absolutista, no considera contexto)
```

### Como SI Comentar

```
✅ Explicar el problema + sugerir solucion:
   "Este endpoint puede tener N+1 queries cuando hay muchas
   reservations. Considera usar eager loading:
   `db('reservations').whereIn('property_id', propIds)`"

✅ Preguntar antes de asumir:
   "Veo que usas forEach aqui - hay alguna razon para no
   usar filter/map? Si es intencional, un comentario
   ayudaria a futuros lectores."

✅ Ofrecer contexto:
   "En este codebase usamos el pattern X para este tipo
   de casos (ver example.js:45). No es blocker, pero
   mantendria consistencia."

✅ Reconocer tradeoffs:
   "Esto funciona, pero podria tener issues de performance
   con datasets grandes. Para el scope actual esta bien,
   solo lo menciono para tenerlo en cuenta."
```

---

## Patterns Problematicos (Red Flags)

### En Node.js/JavaScript

```javascript
// 🔴 N+1 Query
const properties = await db('properties').select('*');
for (const prop of properties) {
  prop.reservations = await db('reservations')
    .where({ property_id: prop.id }); // N queries!
}

// ✅ Sugerencia:
const properties = await db('properties').select('*');
const propIds = properties.map(p => p.id);
const reservations = await db('reservations')
  .whereIn('property_id', propIds);
// Agrupar en memoria por property_id


// 🔴 Promise sin await/catch
function processPayment(data) {
  stripe.paymentIntents.create(data); // Fire and forget!
}

// ✅ Sugerencia:
async function processPayment(data) {
  try {
    return await stripe.paymentIntents.create(data);
  } catch (error) {
    logger.error('Payment failed', { error, data });
    throw error;
  }
}


// 🔴 SQL Injection
const users = await db.raw(
  `SELECT * FROM users WHERE name = '${name}'` // Vulnerable!
);

// ✅ Sugerencia:
const users = await db('users').where({ name });
// o con raw: db.raw('SELECT * FROM users WHERE name = ?', [name])
```

### En React

```jsx
// 🔴 useEffect sin deps o con deps incorrectas
useEffect(() => {
  fetchData(userId);
}); // Corre en cada render!

// ✅ Sugerencia:
useEffect(() => {
  fetchData(userId);
}, [userId]);


// 🔴 Estado derivado innecesario
const [items, setItems] = useState([]);
const [filteredItems, setFilteredItems] = useState([]);

useEffect(() => {
  setFilteredItems(items.filter(i => i.active));
}, [items]);

// ✅ Sugerencia:
const [items, setItems] = useState([]);
const filteredItems = useMemo(
  () => items.filter(i => i.active),
  [items]
);


// 🔴 Props drilling excesivo
<Parent data={data}>
  <Child data={data}>
    <GrandChild data={data}>
      <GreatGrandChild data={data} />

// ✅ Sugerencia: Context o composicion
```

### En PostgreSQL/SQL

```sql
-- 🔴 SELECT * en tabla grande
SELECT * FROM audit_logs WHERE user_id = 123;

-- ✅ Sugerencia:
SELECT id, action, created_at FROM audit_logs
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 100;


-- 🔴 OFFSET para paginacion
SELECT * FROM orders
ORDER BY id
OFFSET 10000 LIMIT 20; -- Lento en offsets grandes

-- ✅ Sugerencia: Cursor-based pagination
SELECT * FROM orders
WHERE id > :last_seen_id
ORDER BY id
LIMIT 20;


-- 🔴 OR en columnas diferentes (no usa indices bien)
SELECT * FROM reservations
WHERE property_id = 123 OR guest_id = 456;

-- ✅ Sugerencia: UNION si performance es critica
SELECT * FROM reservations WHERE property_id = 123
UNION
SELECT * FROM reservations WHERE guest_id = 456;
```

---

## Seguridad: Checklist

```
EN CADA PR VERIFICAR:

AUTHENTICATION/AUTHORIZATION
[ ] Endpoints protegidos requieren auth
[ ] Permisos verificados (no solo auth)
[ ] Tenant isolation en multi-tenant

INPUT VALIDATION
[ ] Input sanitizado antes de usar
[ ] Queries parametrizadas (no concatenacion)
[ ] File uploads validados (tipo, tamaño)

DATA EXPOSURE
[ ] No logs de datos sensibles
[ ] Passwords hasheados (bcrypt, argon2)
[ ] Tokens/secrets en env vars, no en codigo

DEPENDENCIES
[ ] No dependencias con vulnerabilidades conocidas
[ ] Lockfile actualizado
```

---

## Multi-tenancy: Review Especial

```
EN CODEBASES MULTI-TENANT:

🔴 CRITICO - Query sin tenant_id:
// PELIGRO: Puede filtrar datos de otros tenants
const reservations = await db('reservations')
  .where({ status: 'confirmed' });

// ✅ SIEMPRE incluir tenant:
const reservations = await db('reservations')
  .where({ tenant_id: req.tenant.id, status: 'confirmed' });


🔴 CRITICO - Tenant de request vs recurso:
// PELIGRO: Usuario puede acceder a recurso de otro tenant
app.get('/api/reservations/:id', async (req, res) => {
  const reservation = await db('reservations')
    .where({ id: req.params.id })
    .first();
  res.json(reservation); // Sin verificar tenant!
});

// ✅ SIEMPRE verificar ownership:
app.get('/api/reservations/:id', async (req, res) => {
  const reservation = await db('reservations')
    .where({
      id: req.params.id,
      tenant_id: req.tenant.id  // Verificacion!
    })
    .first();

  if (!reservation) {
    return res.status(404).json({ error: 'Not found' });
  }
  res.json(reservation);
});
```

---

## Dar Feedback como Senior

### Enfoque Mentoría

```
EN LUGAR DE:
"Esto esta mal, deberia ser X"

HACER:
"Este approach puede tener [problema] cuando [condicion].
Una alternativa que hemos usado es [solucion] porque [razon].
Que opinas?"

---

EN LUGAR DE:
Solo señalar problemas

HACER:
Reconocer lo bueno:
"Me gusta como manejaste [caso X]. El error handling en
[linea Y] es muy robusto."

---

EN LUGAR DE:
Reescribir el codigo del PR

HACER:
Guiar hacia la solucion:
"El patron que usamos para esto esta en [file:line].
Te puede servir como referencia."
```

### Calibrar Feedback al Nivel

```
DEVELOPER JUNIOR:
- Mas explicaciones del "por que"
- Links a documentacion/ejemplos
- Ofrecer pair programming si es complejo
- Ser explicito sobre que es blocker vs nice-to-have

DEVELOPER SENIOR:
- Asumir que conocen los basics
- Enfocarse en edge cases y arquitectura
- Preguntar sobre decisiones de diseño
- Discutir tradeoffs como peers

DEVELOPER NUEVO EN EL PROYECTO:
- Señalar convenciones del proyecto
- Explicar contexto historico si es relevante
- Ser paciente con curva de aprendizaje
```

---

## Recibir Reviews como Senior

```
MINDSET CORRECTO:

1. El reviewer esta mejorando el codigo, no atacandote
2. Cada comentario es oportunidad de aprender
3. Esta bien defender tu decision CON argumentos
4. "No lo se" es respuesta valida

COMO RESPONDER:

✅ Si estas de acuerdo:
   "Buen catch, fixed!"

✅ Si quieres discutir:
   "Entiendo la sugerencia. Opte por X porque [razon].
   Pero estoy abierto a Z si crees que es mejor."

✅ Si no entiendes:
   "Puedes elaborar? No estoy seguro de entender
   el problema que señalas."

❌ Evitar:
   - Responder defensivamente
   - Ignorar comentarios sin responder
   - Cambiar sin entender por que
```

---

## Checklist de Code Review

```
ANTES DE APROBAR:

FUNCIONALIDAD
[ ] El codigo hace lo que dice el PR
[ ] Edge cases manejados
[ ] Error handling apropiado

SEGURIDAD
[ ] Sin vulnerabilidades obvias
[ ] Tenant isolation (si aplica)
[ ] Input validation

CALIDAD
[ ] Tests cubren funcionalidad nueva
[ ] Codigo legible y mantenible
[ ] Consistente con patterns del proyecto

OPERACIONES
[ ] Migrations incluidas (si aplica)
[ ] Logs/monitoring apropiados
[ ] No breaking changes sin documentar

MI REVIEW
[ ] Comentarios claros y constructivos
[ ] Distingo blockers de suggestions
[ ] Reconozco lo positivo
```
