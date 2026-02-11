---
name: substack-blog
description: Crea artículos de blog personal para Substack. Usa cuando el usuario dice "escribir post", "blog personal", "artículo para substack", o quiere crear contenido técnico/reflexivo personal.
---

# Substack Blog

Crea artículos de blog personal para Substack con tono técnico-conversacional.

## Configuración requerida

### Archivo de configuración

Verifica que existe `.blog-config.json` en la carpeta de esta skill. Si no existe, pregunta:

1. "¿Cuál es la ruta de tu vault de Obsidian?"
2. "¿Cuál es la URL de tu publicación en Substack? (ej: https://tunombre.substack.com)"
3. "¿Cuál es tu user_id de Substack?"

Crea el archivo:

```json
{
  "obsidian_vault_path": "{ruta al vault}",
  "substack_publication_url": "{url de la publicación}",
  "user_id": "{tu user_id}"
}
```

### Autenticación (automática)

Las cookies se extraen **automáticamente** de Safari, Chrome o Firefox usando `@steipete/sweet-cookie`.

Solo necesitas estar logueado en substack.com en tu navegador.

**Fallback manual:** Si la extracción automática falla, crea `.env` en la carpeta de la skill:

```
SID=tu_cookie_sid
SUBSTACK_SID=tu_cookie_substack_sid
SUBSTACK_LLI=tu_cookie_substack_lli
```

### Style guide

Verifica que existe `Areas/Writing/style-guide.md` en el vault de Obsidian. Si no existe, créalo con el contenido base (ver sección Referencias).

## Paso 1: Origen de la idea

Pregunta:

```
¿De dónde viene la idea?

1. Buscar en Inbox/ - Seleccionar idea guardada
2. Tema nuevo - Describir directamente
```

### Si elige Inbox/

1. Lista archivos en:
   - `{vault}/Inbox/ideas/`
   - `{vault}/Inbox/bookmarks/`
   - `{vault}/Inbox/trending/`

2. Muestra lista numerada con título de cada archivo
3. Usuario selecciona uno
4. Lee el contenido como contexto para el artículo

### Si elige tema nuevo

Pregunta: "¿De qué quieres escribir?"

## Paso 2: Discusión interactiva

Haz estas preguntas UNA A UNA:

1. "¿Qué quieres que el lector se lleve de este artículo?"
2. "¿Hay código o ejemplos concretos que mostrar?"
3. "¿Qué aprendiste tú en el proceso?"
4. "¿Hubo algún error, problema interesante o decisión difícil?"
5. "¿Algo más que quieras incluir?"

## Paso 3: Generar outline

Presenta estructura propuesta:

```markdown
## Outline propuesto

1. **Gancho** - {descripción}
2. **Contexto/Problema** - {descripción}
3. **Desarrollo**
   - {sección 1}
   - {sección 2}
   - ...
4. **Reflexión** - {descripción}
5. **Cierre** - {descripción}

¿Ajustamos algo?
```

Itera hasta que el usuario apruebe.

## Paso 4: Escribir artículo

1. Lee `{vault}/Areas/Writing/style-guide.md`
2. Genera artículo completo en Markdown
3. Incluye frontmatter:

```yaml
---
title: "{título}"
date: {fecha actual YYYY-MM-DD}
tags: [{tags relevantes}]
excerpt: "{resumen de 1-2 frases}"
status: draft
---
```

4. Muestra el artículo completo
5. Pregunta: "¿Ajustamos algo?"

## Paso 5: Revisar (opcional)

Pregunta: "¿Quieres que revise claridad y estilo?"

Si responde sí:
- Invoca `marketing-skills:copy-editing`
- Instrucciones especiales:
  - Revisar claridad de frases
  - Eliminar redundancias
  - NO añadir CTAs ni tono de venta
  - Mantener voz personal en primera persona

## Paso 6: Guardar en Obsidian

Genera el slug del título (lowercase, guiones, sin caracteres especiales).

Crea carpeta y archivos:

```
{vault}/Areas/Writing/{slug}/
├── article.md          # Artículo final con frontmatter
└── source-idea.md      # Solo si vino de Inbox/
```

Si la idea vino de Inbox/:
1. Copia el archivo original a `source-idea.md`
2. Mueve el archivo original a `{vault}/Processed/{subcarpeta original}/`

## Paso 7: Crear draft en Substack

Ejecuta:

```bash
npx bun {skill_path}/scripts/substack.ts create --title "{título}" --subtitle "{excerpt}" --file "{vault}/Areas/Writing/{slug}/article.md"
```

Muestra resultado:
- Si éxito: "Draft creado. Abre Substack para revisar y publicar: {url}"
- Si error: Muestra el error y sugiere verificar cookies

## Referencias

### Style guide base

Si no existe `Areas/Writing/style-guide.md`, créalo con:

```markdown
# Style Guide - Blog Personal

## Voz y Tono

- **Perspectiva:** Primera persona ("descubrí", "decidí", "me funcionó")
- **Tono:** Conversacional, como hablar con un colega
- **Honestidad:** Admitir limitaciones ("esto no es perfecto", "hay casos donde no aplica")
- **Opiniones:** Claras y fundamentadas ("prefiero X porque...")

## Principios de Escritura

### 1. Muestra el proceso, no solo el resultado
- Qué problema tenías
- Qué intentaste
- Qué falló y por qué
- Qué funcionó finalmente

### 2. Código con contexto
- No code dumps sin explicación
- Explica el "por qué", no solo el "qué"
- Muestra errores reales que cometiste

### 3. Reflexiones genuinas
- Qué aprendiste
- Qué harías diferente
- Qué sigue sin estar claro

### 4. Estructura clara pero no rígida
- Headers que guían la lectura
- Párrafos cortos (2-3 líneas máximo)
- Listas cuando ayudan, no por defecto

## Qué Evitar

- Tono de tutorial genérico ("en este post vamos a ver...")
- Exceso de disclaimers
- Falsa modestia
- Jerga innecesaria sin explicar
- CTAs o tono de venta
- Frases vacías ("es importante mencionar que...")

## Estructura Típica

1. **Gancho** - Problema o situación interesante
2. **Contexto** - Por qué importa, qué intentabas
3. **Desarrollo** - El journey, con código si aplica
4. **Reflexión** - Qué aprendiste, qué cambiarías
5. **Cierre** - Próximos pasos, preguntas abiertas (opcional)

## Formato

### Títulos
- Descriptivos y específicos
- Pueden ser preguntas
- Evitar clickbait

### Código
- Bloques con lenguaje especificado
- Comentarios donde ayuden
- Mostrar output cuando sea relevante

### Links
- Solo si aportan valor real
- Describir a dónde llevan
```

### Rutas del proyecto

Leer de `.blog-config.json`:
- **Vault Obsidian**: `obsidian_vault_path`
- **Substack URL**: `substack_publication_url`
- **User ID**: `user_id`

## Script de Substack

La skill incluye un script CLI para interactuar con Substack:

```bash
# Crear draft desde archivo markdown
npx bun scripts/substack.ts create --title "Título" --file path/to/article.md

# Crear draft con subtítulo
npx bun scripts/substack.ts create --title "Título" --subtitle "Subtítulo" --file article.md

# Listar drafts existentes
npx bun scripts/substack.ts drafts
```

El script lee automáticamente `.blog-config.json` y `.env` de la carpeta de la skill.
