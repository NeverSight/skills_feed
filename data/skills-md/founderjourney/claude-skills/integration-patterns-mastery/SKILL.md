---
name: integration-patterns-mastery
description: Patrones de integracion robustas para Senior Full-Stack Developer. Usar cuando el usuario necesite disenar o explicar integraciones con APIs externas, webhooks, sincronizacion de datos, retry patterns, manejo de errores en integraciones, o defender experiencia con Stripe, OTAs, WhatsApp API. Activa con palabras como webhook, integracion, API externa, sync, retry, idempotencia, Stripe, iCal, OTA, dead letter queue, reconciliacion. Especializado en sistemas de produccion robustos.
---

# Integration Patterns Mastery

Sistema para disenar y explicar integraciones robustas en produccion.

## Workflow Principal

### 1. Identificar necesidad

| Usuario dice... | Accion |
|-----------------|--------|
| "Disenar integracion" | Ir a Decision Framework (abajo) |
| "Webhooks seguros" | Ver [webhook-security.md](references/webhook-security.md) |
| "Retry patterns" | Ver [retry-patterns.md](references/retry-patterns.md) |
| "Sincronizar datos" | Ver [sync-strategies.md](references/sync-strategies.md) |
| "Integrar Stripe/pagos" | Ver [payment-edge-cases.md](references/payment-edge-cases.md) |
| "Explicar mi integracion" | Usar ejemplos de tu experiencia |

---

### 2. Decision Framework: Disenar Integracion

**Paso 1: Clasificar tipo de integracion**
```
PUSH (webhooks, eventos)
→ API externa notifica a tu sistema
→ Necesitas: endpoint seguro, idempotencia, retry handling

PULL (polling, fetch)
→ Tu sistema consulta API externa
→ Necesitas: scheduler, rate limiting, cache

BIDIRECCIONAL (sync)
→ Datos fluyen en ambas direcciones
→ Necesitas: conflict resolution, reconciliacion
```

**Paso 2: Definir garantias necesarias**
```
At-least-once: mensaje llega 1+ veces (tolera duplicados)
→ Implementar: idempotencia en handler

At-most-once: mensaje llega 0 o 1 vez (puede perder)
→ Implementar: solo si perdida es aceptable

Exactly-once: mensaje llega exactamente 1 vez
→ Implementar: transacciones + deduplicacion (complejo)
```

**Paso 3: Error handling strategy**
```
TRANSIENT ERRORS (timeout, 503)
→ Retry con exponential backoff

PERMANENT ERRORS (400, 401)
→ No retry, log + alerta

PARTIAL FAILURES
→ Dead letter queue para revision manual
```

---

### 3. Patrones Core

#### Webhook Handler Seguro

```javascript
app.post('/webhooks/stripe', async (req, res) => {
  // 1. VERIFICAR FIRMA (siempre primero)
  const sig = req.headers['stripe-signature'];
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.rawBody, sig, SECRET);
  } catch (err) {
    return res.status(400).send('Invalid signature');
  }

  // 2. IDEMPOTENCIA (evitar procesar dos veces)
  const processed = await db('webhook_events')
    .where({ event_id: event.id }).first();
  if (processed) {
    return res.json({ status: 'already_processed' });
  }

  // 3. PROCESAR
  try {
    await handleEvent(event);
    await db('webhook_events').insert({ event_id: event.id });
    res.json({ received: true });
  } catch (err) {
    // 4. RETRY LOGIC (devolver 500 para que reintenten)
    console.error('Webhook processing failed', err);
    res.status(500).send('Processing failed');
  }
});
```

#### Retry con Exponential Backoff

```javascript
const retryWithBackoff = async (fn, options = {}) => {
  const { maxRetries = 5, baseDelay = 1000 } = options;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (!isRetryable(error) || attempt === maxRetries - 1) {
        throw error;
      }
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
      await sleep(delay);
    }
  }
};

const isRetryable = (error) => {
  // Retry: timeouts, 5xx, network errors
  // No retry: 4xx (except 429)
  if (error.code === 'ETIMEDOUT') return true;
  if (error.status >= 500) return true;
  if (error.status === 429) return true;
  return false;
};
```

#### Dead Letter Queue

```javascript
// Cuando algo falla permanentemente
const handleFailedJob = async (job, error) => {
  await db('dead_letter_queue').insert({
    job_type: job.type,
    payload: JSON.stringify(job.data),
    error: error.message,
    failed_at: new Date(),
    retry_count: job.attemptsMade
  });

  // Notificar para revision manual
  await sendAlert({
    channel: 'integrations',
    message: `Job ${job.id} failed permanently: ${error.message}`
  });
};
```

---

### 4. Tu Experiencia: Scripts de Respuesta

**iCal Sync con OTAs:**
```
"El challenge principal fue que iCal es un protocolo muy basico - solo
tiene bloques de tiempo sin estados ni IDs unicos.

Mi solucion tiene 4 componentes:

1. SYNC ENGINE: Polling cada 5 minutos, parsea iCal
2. RECONCILIADOR: Compara con estado interno, genera diff
3. CONFLICT RESOLVER: Aplica reglas de prioridad
4. RETRY HANDLER: Exponential backoff para failures

El resultado: 99% de syncs automaticos, cero overbookings en 18 meses."
```

**Stripe Integration:**
```
"Implemente integracion completa con Stripe incluyendo:

- Customer creation y management
- PaymentIntents para one-time payments
- Subscriptions con lifecycle completo
- Webhook handlers para todos los eventos criticos

Los edge cases mas importantes que manejo:
- Pagos fallidos con dunning flow
- Disputes y chargebacks
- Currency handling para Colombia (COP sin centavos)
- Idempotencia para evitar cobros duplicados"
```

---

### 5. Checklist de Integracion Robusta

```
SEGURIDAD
[ ] Verificacion de firmas en webhooks
[ ] Secrets en variables de entorno
[ ] HTTPS para todos los endpoints
[ ] Rate limiting en endpoints publicos

RELIABILITY
[ ] Retry con exponential backoff
[ ] Dead letter queue para failures
[ ] Timeouts configurados
[ ] Circuit breaker si aplica

IDEMPOTENCIA
[ ] Unique key para cada operacion
[ ] Check antes de procesar
[ ] Respuesta consistente para duplicados

OBSERVABILIDAD
[ ] Logs estructurados
[ ] Metricas de latencia y errores
[ ] Alertas para failures
[ ] Dashboard de health
```

---

## Referencias

| Archivo | Contenido | Cuando usar |
|---------|-----------|-------------|
| [webhook-security.md](references/webhook-security.md) | Firmas, replay attacks, idempotencia | Implementar webhooks |
| [retry-patterns.md](references/retry-patterns.md) | Backoff, jitter, circuit breaker | Manejar failures |
| [sync-strategies.md](references/sync-strategies.md) | Push, pull, bidireccional, reconciliacion | Sincronizar datos |
| [payment-edge-cases.md](references/payment-edge-cases.md) | Stripe, disputes, refunds, currencies | Integrar pagos |
