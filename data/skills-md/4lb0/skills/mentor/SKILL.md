---
name: mentor
description: Genera un documento estructurado de objetivos para sesiones de mentoría tech a partir del CV y metas del mentee.
---

# Definición de Objetivos de Mentoría

## Propósito

Analizar el perfil de un mentee y sus objetivos para generar un documento
estructurado que sirva como base para sesiones de mentoría tech. Usa el
framework GROW (Goal, Reality, Options).

## Cuándo usar este skill

Cuando un mentee quiere prepararse para una mentoría y necesita clarificar qué
quiere lograr.

## Inputs requeridos

El mentee debe proporcionar todo junto:

1. **CV** (archivo o texto)
2. **¿Qué rol querés alcanzar y en qué plazo?**
3. **¿Qué te falta hoy para llegar ahí?**
4. **¿Qué caminos consideraste?** (crecer internamente, cambiar empresa,
   estudiar, etc.)

Si falta algún input, solicitar todo lo que falte antes de procesar.

## Proceso

### Paso 1: Analizar CV

Extraer del CV:

- Nombre
- Rol actual
- Años de experiencia total
- Stack tecnológico principal
- Progresión de carrera (roles anteriores)
- Experiencia de liderazgo (si existe)

### Paso 2: Analizar objetivos

Evaluar las respuestas del mentee identificando:

- Claridad del objetivo
- Gaps entre situación actual y objetivo
- Viabilidad de los caminos propuestos

### Paso 3: Validar

Incluir en el documento observaciones sobre:

- **Objetivo vago:** Si no es específico, señalarlo (ej: "crecer
  profesionalmente" no es un objetivo concreto)
- **Plazo poco realista:** Si el salto es muy grande para el tiempo propuesto
- **Coherencia CV-Objetivo:** Gaps importantes entre experiencia actual y meta
- **Caminos incompletos:** Si no consideró opciones relevantes

Ejemplos:

- "Objetivo de Tech Lead en 6 meses sin experiencia previa liderando equipos.
  Plazo agresivo."
- "Objetivo CTO con 2 años de experiencia. Considerar roles intermedios."
- "No menciona capacitación formal como opción, podría ser relevante."

## Output

Generar un archivo Markdown:

```markdown
# Objetivos de Mentoría

**Fecha:** [fecha actual] **Mentee:** [nombre]

---

## Perfil actual

- **Rol:** [rol actual]
- **Experiencia:** [X años]
- **Stack principal:** [tecnologías]
- **Liderazgo previo:** [sí/no, detalles si aplica]

## Objetivo

**Meta:** [objetivo concreto] **Plazo:** [timeframe]

## Análisis de situación

[Resumen de dónde está hoy respecto al objetivo. Gaps identificados entre perfil
actual y meta.]

## Caminos considerados

- [Opción 1]
- [Opción 2]
- [etc.]

## Observaciones

[Validaciones sobre realismo, coherencia, puntos a profundizar en la sesión. Ser
directo pero constructivo.]

---

_Documento generado para sesión de mentoría en mentor.dev.ar_
```

## Tono

- Directo y profesional
- Validar sin desmotivar
- Señalar problemas con claridad pero de forma constructiva

## Ejemplo

### Input del mentee

> **CV:** Soy desarrollador backend con 4 años de experiencia. Trabajé 2 años en
> una software factory haciendo APIs en Node.js y los últimos 2 años estoy en
> una fintech como dev semi-senior, principalmente con Python y PostgreSQL. No
> tengo gente a cargo pero a veces ayudo a los juniors cuando se traban.
>
> **¿Qué rol querés alcanzar y en qué plazo?** Quiero ser Senior en 1 año y
> después ver si puedo pasar a Tech Lead.
>
> **¿Qué te falta hoy para llegar ahí?** No sé bien qué diferencia a un
> semi-senior de un senior. Siento que técnicamente estoy bien pero no sé si me
> falta algo más. Tampoco sé si en mi empresa actual tengo espacio para crecer.
>
> **¿Qué caminos consideraste?** Pensé en buscar en otro lado donde paguen mejor
> y tenga más visibilidad. También me dijeron que haga cursos de arquitectura
> pero no sé si sirve.

### Output generado

```markdown
# Objetivos de Mentoría

**Fecha:** 29 de enero de 2026 **Mentee:** [Nombre]

---

## Perfil actual

- **Rol:** Desarrollador Backend Semi-Senior
- **Experiencia:** 4 años
- **Stack principal:** Python, Node.js, PostgreSQL
- **Liderazgo previo:** No formal, pero asiste a juniors ocasionalmente

## Objetivo

**Meta:** Pasar a Senior, luego evaluar Tech Lead **Plazo:** 1 año para Senior

## Análisis de situación

Perfil técnico sólido con experiencia en dos entornos distintos (software
factory y fintech). Tiene exposición a mentoreo informal de juniors, lo cual es
un buen indicador para crecimiento.

Gaps identificados:

- No tiene claridad sobre qué lo separa del nivel Senior
- Duda sobre oportunidades de crecimiento en su empresa actual
- Considera capacitación pero sin dirección clara

## Caminos considerados

- Buscar en otra empresa con mejor sueldo y visibilidad
- Hacer cursos de arquitectura

## Observaciones

- El objetivo de Senior en 1 año es realista dado su experiencia
- La duda sobre diferencia semi-senior/senior es el punto central a trabajar
- El interés en cursos de arquitectura puede ser prematuro si no resuelve
  primero el salto a Senior

---

_Documento generado para sesión de mentoría en mentor.dev.ar_
```

### Feedback del mentor (ejemplo de sesión)

**Diferencia Semi-Senior vs Senior:**

La diferencia principal no es técnica. Un semi-senior técnicamente suele estar
bien. Lo que cambia es el foco:

- **Semi-Senior:** Recibe una tarea, la cumple, listo.
- **Senior:** Se preocupa por las tareas del equipo entero, no solo las suyas.
  Entiende que el resultado del equipo importa más que su aporte individual.

**Sobre la sobreingeniería:**

Un patrón común del semi-senior es aplicar conocimientos nuevos donde no
corresponde. Por ejemplo, aprende patrones de diseño y quiere usarlos en todos
lados. Todavía no tiene el criterio para saber cuándo aplicarlos y cuándo
mantenerlo simple.

**Puntos a trabajar:**

1. Ampliar el foco: de "mis tareas" a "las tareas del equipo"
2. Desarrollar criterio para elegir cuándo complejizar y cuándo no
3. Evaluar si la empresa actual da espacio para ejercer este rol ampliado

**Sobre buscar afuera vs crecer internamente:**

Siempre agotar primero la opción interna. Dentro de la misma empresa puede ser
otro equipo, pero primero asegurarse en el mismo equipo. La mayoría de las veces
hay espacio para crecer.

Señales de que sí hay que buscar afuera:

- No hay interés en nuevas tecnologías
- No hay interés en capacitación
- No hay nuevas posiciones disponibles
- Hay muchos seniors de los que aprender pero no hay juniors a quienes coachear
  (necesitás ambos para crecer)

**Acción concreta:** Hablar con compañeros, líder técnico, líder no técnico,
jefe de proyecto. Pedir feedback para saber cómo lo están percibiendo. Muchas
veces uno cree que está haciendo bien el trabajo pero hay un gap de
comunicación: te pidieron A, entendiste B, entregaste B, y no están contentos.
No es que seas malo, es un problema de comunicación.

---

### Ejemplo 2: Senior a Tech Lead

### Input del mentee

> **CV:** Tengo 7 años de experiencia como desarrollador full-stack. Empecé en
> una consultora chica, después pasé a una empresa de producto donde estuve 4
> años y crecí a Senior. Hace 1 año me cambié a una startup de logística como
> Senior Developer. Stack principal: React, Node.js, TypeScript, AWS. Tengo
> experiencia haciendo code reviews, definiendo arquitectura de microservicios y
> onboardeando gente nueva al equipo.
>
> **¿Qué rol querés alcanzar y en qué plazo?** Quiero ser Tech Lead en los
> próximos 6-12 meses. En mi empresa actual no hay ese rol definido, somos un
> equipo chico y el CTO hace todo.
>
> **¿Qué te falta hoy para llegar ahí?** Técnicamente me siento preparado. Lo
> que no sé es cómo manejar conflictos en el equipo o tener conversaciones
> difíciles. Tampoco sé bien cómo hablar con gente de negocio, siempre me costó
> traducir lo técnico a algo que entienda el producto o el CEO.
>
> **¿Qué caminos consideraste?** Buscar una empresa más grande donde haya una
> posición de Tech Lead abierta. También pensé en hablar con el CTO para ver si
> podemos crear el rol, pero no sé cómo plantearlo.

### Output generado

```markdown
# Objetivos de Mentoría

**Fecha:** 29 de enero de 2026 **Mentee:** [Nombre]

---

## Perfil actual

- **Rol:** Senior Developer Full-Stack
- **Experiencia:** 7 años
- **Stack principal:** React, Node.js, TypeScript, AWS
- **Liderazgo previo:** Code reviews, definición de arquitectura, onboarding de
  nuevos integrantes

## Objetivo

**Meta:** Tech Lead **Plazo:** 6-12 meses

## Análisis de situación

Perfil técnico sólido con experiencia en arquitectura y tareas de liderazgo
informal. Ya hace varias funciones de Tech Lead sin el título. El contexto
(startup chica, CTO hace todo) es tanto un obstáculo como una oportunidad.

Gaps identificados:

- Soft skills: manejo de conflictos, conversaciones difíciles
- Comunicación con negocio: traducir lo técnico para stakeholders no técnicos
- El rol no existe formalmente en su empresa actual

## Caminos considerados

- Buscar empresa más grande con posición de Tech Lead
- Hablar con el CTO para crear el rol

## Observaciones

- El plazo de 6-12 meses es realista dado su experiencia
- Ya tiene las bases técnicas, el foco debería estar en soft skills y
  comunicación
- La opción de hablar con el CTO es la correcta pero no sabe cómo plantearla
- Buscar afuera debería ser plan B, no plan A

---

_Documento generado para sesión de mentoría en mentor.dev.ar_
```

### Feedback del mentor (ejemplo de sesión)

**Sobre crear el rol internamente:**

De nuevo, fundamental tratar de quedarse en la misma empresa y ver si se puede
crecer ahí. Puede haber un espacio nuevo: un proyecto chico, un producto
interno, o una parte específica del producto donde puedas encargarte de la
arquitectura y también de hablar con stakeholders (clientes internos o
externos).

**Cómo plantearlo con el CTO:**

1. Pedí una reunión para hablar sobre "crecimiento de la empresa" (no sobre tu
   crecimiento, para no asustarlo ni que piense que vas a renunciar)
2. Planteale cosas concretas, sacate el miedo
3. Una charla proactiva siempre es valorable. Que alguien del equipo quiera
   crecer es positivo para cualquier CTO.

**Qué pedir concretamente:**

El CTO probablemente está haciendo todo lo que vos querés hacer. Pedile que te
delegue parte de eso. No todo de golpe, sino empezar con una parte chica:

- Una funcionalidad específica del producto (si es un e-commerce: el checkout, o
  el buscador)
- Un producto interno chico
- Un proyecto nuevo que esté arrancando

La idea es concentrarte en algo acotado donde puedas ejercer el rol completo:
arquitectura + comunicación con stakeholders.

**Sobre hablar con otras áreas (producto/negocio):**

Si bien no es parte del rol técnico en sí, hablar con otras áreas es
fundamental. A veces es más del lado de producto, pero está bueno acompañarlos
porque desde lo técnico podemos dar una visión y alternativas que ellos no
tienen.

Ejemplo concreto: producto quiere una funcionalidad de una manera, pero vos
sabés que técnicamente va a costar mucho tiempo. Podés proponer una alternativa
más corta a nivel desarrollo que permita validar más temprano. Eso es oro para
la gente de producto.

**El diferencial del Tech Lead:**

Entender cuánto se tarda realmente en hacer algo. No necesitás conocer todo el
código, pero sí podés:

- Ir a hablar con el dev que conoce mejor esa parte
- Preguntarle si se le ocurre una alternativa
- Motivarlo para que proponga soluciones

No es pisar el rol de producto, es trabajar codo a codo. Un buen Tech Lead y un
buen Product Manager laburando juntos hacen la diferencia.

---

### Ejemplo 3: Tech Lead a CTO / VP of Engineering

### Input del mentee

> **CV:** 10 años de experiencia en desarrollo. Los últimos 3 años soy Tech Lead
> en una empresa de software para salud. Lidero un equipo de 6 personas (4 devs,
> 1 QA, 1 DevOps). Stack: Java, Spring Boot, PostgreSQL, AWS. Me encargo de
> arquitectura, code reviews, planificación de sprints, 1:1s con el equipo y
> coordino con producto. Antes fui Senior Developer en la misma empresa.
>
> **¿Qué rol querés alcanzar y en qué plazo?** Quiero ser CTO o VP of
> Engineering en 2-3 años. No sé bien cuál de los dos, creo que son parecidos
> pero no idénticos.
>
> **¿Qué te falta hoy para llegar ahí?** Siento que estoy muy metido en el día a
> día del equipo. No tengo visión de negocio ni manejo presupuesto. Tampoco sé
> cómo es contratar gente, siempre lo hizo RRHH y yo solo hacía la entrevista
> técnica. Me cuesta delegar, termino resolviendo yo los problemas técnicos
> difíciles.
>
> **¿Qué caminos consideraste?** Quedarme acá y esperar que crezca la empresa.
> También pensé en buscar una startup más chica donde pueda tener más
> responsabilidades, o hacer un MBA pero me parece mucho tiempo y plata.

### Output generado

```markdown
# Objetivos de Mentoría

**Fecha:** 29 de enero de 2026 **Mentee:** [Nombre]

---

## Perfil actual

- **Rol:** Tech Lead
- **Experiencia:** 10 años (3 como Tech Lead)
- **Stack principal:** Java, Spring Boot, PostgreSQL, AWS
- **Liderazgo previo:** Equipo de 6 personas, arquitectura, 1:1s, coordinación
  con producto

## Objetivo

**Meta:** CTO o VP of Engineering **Plazo:** 2-3 años

## Análisis de situación

Experiencia sólida como Tech Lead con responsabilidades amplias. Tiene las bases
de liderazgo técnico pero identifica correctamente los gaps para el siguiente
nivel.

Gaps identificados:

- Muy metido en el día a día, cuesta delegar
- Sin visión de negocio ni manejo de presupuesto
- Sin experiencia en hiring (solo entrevista técnica)
- No tiene clara la diferencia entre CTO y VP of Engineering

## Caminos considerados

- Quedarse y esperar que crezca la empresa
- Buscar startup más chica con más responsabilidades
- Hacer un MBA

## Observaciones

- El plazo de 2-3 años es razonable para el salto
- Necesita clarificar CTO vs VP of Engineering (son roles distintos)
- El problema de delegación es crítico: si no lo resuelve, no escala
- "Esperar que crezca la empresa" es pasivo, debería buscar activamente las
  oportunidades

---

_Documento generado para sesión de mentoría en mentor.dev.ar_
```

### Feedback del mentor (ejemplo de sesión)

**Sobre el MBA:**

Si te parece que la educación es buena y podés hacerlo con menos recursos
(tiempo y plata), la educación siempre suele ser buena. Especialmente si es un
instituto conocido, de importancia. No quiere decir que todos los cursos sean
malos, pero una institución reconocida suma. Además, no es solo por lo que
aprendés, sino por los contactos que generás.

**Sobre ir a una empresa más chica:**

Suele ser mejor porque tenés más margen para aprender. Pero primero plantear
internamente si hay espacio para crecer.
