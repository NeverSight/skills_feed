---
name: pr-reviewer
description: Revisa PRs aplicando KISS, DRY, SOLID. Usa cuando el usuario diga "revisar PR", "code review", "analizar cambios del PR", "responder comentarios del PR", o comparta URL/número de PR.
allowed-tools: Read, Glob, Grep, Bash
---

# PR Reviewer

Skill para revisar Pull Requests de forma exhaustiva, aplicando principios de ingenieria de software y respondiendo a comentarios en español.

## Cuando usar esta Skill

- Usuario pide "revisar PR", "review PR", "code review"
- Usuario pide "analizar cambios" de un PR
- Usuario pide "responder comentarios" de un PR
- Usuario comparte URL de PR o numero de PR
- Usuario pide "PR feedback" o "revisar mis cambios"

## Proceso

### Paso 1: Detectar PR

Intentar detectar el PR automaticamente o solicitar al usuario:

```bash
# Opcion 1: Detectar PR del branch actual
gh pr view --json number,title,url,state,headRefName,baseRefName 2>/dev/null

# Si falla, preguntar al usuario por URL o numero
```

Si el usuario proporciona:
- **URL completa**: Extraer owner/repo y numero
- **Solo numero**: Usar repo actual
- **Nada**: Intentar detectar del branch actual

### Paso 2: Obtener informacion del PR

```bash
# Metadata del PR
gh pr view {numero} --json number,title,body,author,state,headRefName,baseRefName,additions,deletions,changedFiles

# Diff completo
gh pr diff {numero}

# Comentarios existentes
gh api repos/{owner}/{repo}/pulls/{numero}/comments --jq '.[] | {id, path, line, body, user: .user.login, created_at}'

# Review comments (si hay reviews)
gh api repos/{owner}/{repo}/pulls/{numero}/reviews --jq '.[] | {id, state, body, user: .user.login}'
```

### Paso 3: Analizar el diff

Para cada archivo modificado, revisar:

#### 3.1 Seguridad
- Credenciales hardcodeadas
- SQL injection
- XSS vulnerabilities
- Secrets expuestos (.env, API keys)
- Permisos incorrectos
- Input validation faltante

#### 3.2 Calidad de codigo (KISS, DRY, SOLID)
- **KISS**: Codigo innecesariamente complejo
- **DRY**: Logica duplicada que deberia extraerse
- **Single Responsibility**: Funciones/clases haciendo demasiado
- **Open/Closed**: Violaciones de extensibilidad
- **Dependency Inversion**: Dependencias concretas donde deberian ser abstracciones

#### 3.3 Bugs y edge cases
- Null/undefined sin manejar
- Race conditions
- Memory leaks
- Error handling faltante
- Off-by-one errors
- Boundary conditions

#### 3.4 Testing
- Tests faltantes para nuevo codigo
- Tests que no cubren edge cases
- Mocks incorrectos
- Assertions debiles

#### 3.5 Estilo y mantenibilidad
- Nombres poco descriptivos
- Comentarios faltantes o excesivos
- Funciones muy largas (>50 lineas)
- Archivos muy grandes (>200 lineas)
- Magic numbers sin constantes

### Paso 4: Responder a comentarios existentes

Para CADA comentario en el PR, generar una respuesta:

```bash
# Formato de respuesta individual
gh pr comment {numero} --body "**Re: @{autor} en \`{archivo}:{linea}\`**

{respuesta en español}

---
_Respuesta generada por PR Reviewer_"
```

**Reglas para respuestas:**
- Siempre en ESPAÑOL
- Ser constructivo, no destructivo
- Si el comentario es valido: "Buen punto, se deberia..."
- Si el comentario es incorrecto: "En realidad, este patron es correcto porque..."
- Si requiere cambio: Sugerir codigo concreto
- Si es pregunta: Responder con explicacion clara

### Paso 5: Generar reporte de review

Presentar al usuario un resumen estructurado:

```markdown
## Review del PR #{numero}: {titulo}

### Resumen
- **Archivos modificados**: X
- **Lineas agregadas**: +X
- **Lineas eliminadas**: -X
- **Comentarios respondidos**: X

### Hallazgos por severidad

#### Criticos (bloquean merge)
- [ ] {hallazgo 1}

#### Importantes (deberian arreglarse)
- [ ] {hallazgo 2}

#### Sugerencias (nice to have)
- [ ] {hallazgo 3}

### Archivos revisados

| Archivo | Estado | Notas |
|---------|--------|-------|
| src/foo.ts | Requiere cambios | Falta validacion |
| src/bar.ts | OK | - |

### Comentarios respondidos

1. @usuario en `archivo.ts:42`: "{comentario original}"
   - Respuesta: "{mi respuesta}"
```

### Paso 6: Confirmar antes de comentar

**IMPORTANTE**: Antes de publicar comentarios, mostrar al usuario:

```
Voy a publicar las siguientes respuestas:

1. En archivo.ts:42 - "Buen punto, se deberia..."
2. En otro.ts:15 - "Este patron es correcto porque..."

¿Confirmas que publique estos comentarios? [S/n]
```

Solo publicar despues de confirmacion explicita.

## Ejemplos de uso

### Ejemplo 1: Review automatico

```
Usuario: "Revisame el PR"

1. Detectar: gh pr view → PR #123 "Add user authentication"
2. Obtener diff y comentarios
3. Analizar aplicando checklist
4. Generar respuestas para 3 comentarios existentes
5. Mostrar reporte y pedir confirmacion
6. Publicar comentarios tras confirmacion
```

### Ejemplo 2: PR especifico

```
Usuario: "Revisa https://github.com/org/repo/pull/456"

1. Parsear URL → owner=org, repo=repo, numero=456
2. Cambiar contexto al repo si es necesario
3. Ejecutar proceso completo de review
```

### Ejemplo 3: Solo responder comentarios

```
Usuario: "Responde los comentarios del PR 789"

1. Obtener PR #789
2. Listar comentarios existentes
3. Generar respuestas sin hacer review completo
4. Confirmar y publicar
```

## Comandos gh utiles

```bash
# Ver PR actual
gh pr view

# Ver diff
gh pr diff {numero}

# Listar comentarios
gh api repos/{owner}/{repo}/pulls/{numero}/comments

# Agregar comentario general
gh pr comment {numero} --body "texto"

# Agregar comentario en linea especifica
gh api repos/{owner}/{repo}/pulls/{numero}/comments \
  -f body="comentario" \
  -f path="archivo.ts" \
  -f line=42 \
  -f side="RIGHT"

# Aprobar PR
gh pr review {numero} --approve --body "LGTM"

# Pedir cambios
gh pr review {numero} --request-changes --body "Ver comentarios"
```

## Principios de review

### Tono constructivo
- Sugerir, no ordenar
- Explicar el "por que" detras de cada sugerencia
- Reconocer lo bueno antes de criticar
- Ofrecer alternativas concretas

### Priorizar hallazgos
1. Seguridad (critico)
2. Bugs (critico)
3. Performance (importante)
4. Mantenibilidad (importante)
5. Estilo (sugerencia)

### Evitar
- Comentarios vagos ("esto no me gusta")
- Bikeshedding sobre preferencias
- Ignorar el contexto del cambio
- Ser condescendiente
