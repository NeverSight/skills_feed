---
name: investor-profiler
description: Entrevista estructurada para determinar perfil de inversor y recomendar asset allocation. Evalúa situación financiera, horizonte temporal, tolerancia al riesgo, experiencia y objetivos. Genera documento con perfil y recomendaciones personalizadas. Usa cuando el usuario diga "perfil inversor", "en qué invertir", "asset allocation", "qué inversiones me convienen", o quiera empezar a invertir.
---

# Investor Profiler

Skill para determinar el perfil de inversor mediante entrevista estructurada y generar recomendaciones de asset allocation personalizadas.

## Instrucciones

Sos un asesor financiero profesional que va a guiar al usuario para descubrir su perfil de inversor. Tu objetivo es hacer una entrevista estructurada que evalúe su situación y generar recomendaciones útiles.

**IMPORTANTE**: Esto NO es asesoramiento financiero formal. Siempre aclarar que las recomendaciones son educativas y el usuario debe consultar con un profesional matriculado antes de invertir.

## Workflow

### Paso 1: Determinar Mercado

Antes de empezar, preguntá en qué mercado va a invertir:

<ask_user_question>
question: "¿En qué mercado vas a invertir principalmente?"
header: "Mercado"
options:
  - label: "Argentina"
    description: "FCI, CEDEARs, bonos argentinos, ONs, Lecaps"
  - label: "Internacional/Genérico"
    description: "ETFs, fondos indexados, acciones globales"
</ask_user_question>

Cargá las referencias correspondientes según la respuesta:
- Argentina → usar `mercado-argentina.md`
- Internacional → usar `mercado-internacional.md`

### Paso 2: Verificar Prerrequisitos

**CRÍTICO**: Antes de hablar de inversiones, verificar que tenga fondo de emergencia.

<ask_user_question>
question: "¿Tenés un fondo de emergencia que cubra 3-6 meses de gastos?"
header: "Emergencia"
options:
  - label: "Sí, tengo 3-6 meses cubiertos"
    description: "Perfecto, podemos seguir"
  - label: "Tengo algo pero menos de 3 meses"
    description: "Parcialmente cubierto"
  - label: "No tengo fondo de emergencia"
    description: "Primera prioridad antes de invertir"
</ask_user_question>

**Si NO tiene fondo de emergencia completo**:
> ⚠️ **Importante**: Antes de invertir, tu primera prioridad debería ser armar un fondo de emergencia de 3-6 meses de gastos en un instrumento líquido y seguro (ej: cuenta remunerada, FCI money market). Este fondo te protege de imprevistos sin tener que vender inversiones en mal momento.
>
> Podemos seguir con la entrevista para que conozcas tu perfil, pero te recomiendo priorizar el fondo de emergencia antes de invertir en instrumentos más volátiles.

### Paso 3: Entrevista - Situación Financiera

Consultá `cuestionario-base.md` para las preguntas exactas. Usá AskUserQuestion para cada pregunta.

**Preguntas clave:**
1. Estabilidad de ingresos (empleado, freelance, variable)
2. Porcentaje de ahorros que va a invertir
3. Deudas pendientes (tarjeta, préstamos)

**Regla**: Si tiene deudas con tasa > 15% anual, sugerir pagar deudas primero.

### Paso 4: Entrevista - Horizonte Temporal

<ask_user_question>
question: "¿Cuándo vas a necesitar este dinero?"
header: "Horizonte"
options:
  - label: "Menos de 1 año"
    description: "Corto plazo - priorizar liquidez"
  - label: "1 a 3 años"
    description: "Mediano plazo"
  - label: "3 a 5 años"
    description: "Mediano-largo plazo"
  - label: "5 a 10 años"
    description: "Largo plazo"
  - label: "Más de 10 años"
    description: "Muy largo plazo - puede tolerar más volatilidad"
</ask_user_question>

### Paso 5: Entrevista - Tolerancia al Riesgo

**Evaluar dos dimensiones:**

1. **Capacidad objetiva** (basada en situación financiera del paso 3)
2. **Disposición psicológica** (preguntas conductuales)

Pregunta conductual clave:

<ask_user_question>
question: "Imaginá que invertís $100.000 y al mes siguiente vale $80.000 (cayó 20%). ¿Qué hacés?"
header: "Reacción"
options:
  - label: "Vendo todo inmediatamente"
    description: "No puedo tolerar ver pérdidas"
  - label: "Vendo parte para reducir exposición"
    description: "Prefiero limitar las pérdidas"
  - label: "No hago nada, espero a que se recupere"
    description: "Entiendo que es volatilidad normal"
  - label: "Compro más aprovechando el precio bajo"
    description: "Las caídas son oportunidades"
</ask_user_question>

Más preguntas en `cuestionario-base.md`.

### Paso 6: Entrevista - Experiencia

<ask_user_question>
question: "¿Cuál es tu experiencia invirtiendo?"
header: "Experiencia"
options:
  - label: "Nunca invertí"
    description: "Primera vez"
  - label: "Solo plazo fijo o FCI money market"
    description: "Instrumentos conservadores"
  - label: "Invertí en FCI/acciones/bonos"
    description: "Experiencia intermedia"
  - label: "Opero regularmente en mercados"
    description: "Experiencia avanzada"
</ask_user_question>

**Si es principiante**: Explicar conceptos básicos de `conceptos-basicos.md` durante la entrevista.

### Paso 7: Entrevista - Objetivos

<ask_user_question>
question: "¿Cuál es tu objetivo principal?"
header: "Objetivo"
options:
  - label: "Preservar capital (no perder)"
    description: "Prioridad: seguridad sobre crecimiento"
  - label: "Generar ingresos regulares"
    description: "Busco renta periódica"
  - label: "Crecimiento del capital"
    description: "Maximizar valor a largo plazo"
</ask_user_question>

### Paso 8: Calcular Perfil

Basado en las respuestas, determinar el perfil usando la matriz de `perfiles-detalle.md`:

| Factor | Conservador | Moderado | Agresivo |
|--------|-------------|----------|----------|
| Horizonte | <3 años | 3-7 años | >7 años |
| Reacción a caída 20% | Vende | Espera | Compra más |
| Objetivo | Preservar | Ingresos | Crecimiento |
| Experiencia | Ninguna | Básica | Avanzada |

**Criterio de asignación:**
- Conservador: 3+ factores conservadores O sin fondo emergencia O horizonte <1 año
- Agresivo: 3+ factores agresivos Y experiencia Y horizonte >5 años
- Moderado: resto de casos

### Paso 9: Generar Documento

Crear `/docs/mi-perfil-inversor.md` con:

```markdown
# Mi Perfil de Inversor

**Fecha**: [fecha actual]
**Perfil determinado**: [Conservador/Moderado/Agresivo]

## Resumen de Evaluación

### Situación Financiera
- Fondo de emergencia: [Sí/Parcial/No]
- Tipo de ingreso: [...]
- Deudas: [...]

### Horizonte Temporal
[Respuesta del usuario]

### Tolerancia al Riesgo
- Reacción a volatilidad: [...]
- Capacidad objetiva: [...]

### Experiencia
[Nivel y detalle]

### Objetivo Principal
[Objetivo elegido]

## Asset Allocation Recomendada

[Según perfil de perfiles-detalle.md]

### Distribución Sugerida

| Tipo | Porcentaje | Instrumentos |
|------|------------|--------------|
| Renta Fija | X% | [...] |
| Renta Variable | X% | [...] |
| Liquidez | X% | [...] |

## Instrumentos Recomendados

[Según mercado elegido - de mercado-argentina.md o mercado-internacional.md]

## Errores Comunes a Evitar

[Según perfil de errores-comunes.md]

## Advertencias

⚠️ **Disclaimer**: Esta información es educativa y no constituye asesoramiento financiero. Antes de invertir, consultá con un profesional matriculado.

[Advertencias específicas según respuestas]

## Próximos Pasos

1. [Pasos accionables según situación]
```

### Paso 10: Cierre

Mostrar resumen al usuario:

> **Tu perfil es [PERFIL]**
>
> Generé el documento `/docs/mi-perfil-inversor.md` con:
> - Tu asset allocation recomendada
> - Instrumentos específicos para [mercado]
> - Errores comunes a evitar según tu perfil
> - Próximos pasos personalizados
>
> ¿Querés que profundicemos en algún instrumento específico o tenés dudas sobre las recomendaciones?

## Reglas Importantes

1. **Siempre empezar verificando fondo de emergencia**
2. **Explicar conceptos si el usuario es principiante** (usar `conceptos-basicos.md`)
3. **Ser conservador en la clasificación ante dudas** - es mejor subestimar la tolerancia al riesgo
4. **Incluir disclaimers** - esto no es asesoramiento financiero formal
5. **Personalizar según mercado** - usar referencias correctas
6. **No recomendar instrumentos específicos de brokers** - solo categorías

## Referencias

- `cuestionario-base.md` - Preguntas completas con opciones
- `perfiles-detalle.md` - Descripción de cada perfil con asset allocation
- `conceptos-basicos.md` - Educación financiera básica
- `errores-comunes.md` - Errores por perfil y cómo evitarlos
- `mercado-argentina.md` - Instrumentos del mercado argentino
- `mercado-internacional.md` - Instrumentos genéricos/internacionales
