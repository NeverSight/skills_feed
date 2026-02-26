---
name: "commiter"
description: "Guía para generar mensajes de commit en español siguiendo Conventional Commits estrictos con Emojis. Usa esta skill siempre que el usuario pida hacer un commit, generar un mensaje de commit, commitear cambios, o cuando se complete un cambio de código y sea momento de registrarlo en git. También se activa con 'commit', 'commitear', 'guardar cambios', 'registrar cambios' o cualquier intención de crear un punto en el historial de git."
metadata:
  version: "1.0"
  type: "project"
  triggers:
    - "commit"
    - "commitear"
    - "guardar cambios"
    - "registrar cambios"
    - "hacer commit"
    - "git commit"
---

# Generador de Commits

Cuando se te pida realizar un commit o generar un mensaje de commit, DEBES seguir estrictamente este formato.

## Estándar: Conventional Commits con Emojis

Utilizamos **Conventional Commits** enriquecidos con **Gitmoji** como base. Todo el contenido debe estar en **ESPAÑOL**.

## Formato

```text
<emoji> <tipo>(<alcance>): <descripción corta>

<cuerpo detallado y extenso>

<footer>
```

## Reglas Obligatorias

1. **Emoji**: El mensaje DEBE comenzar con el emoji correspondiente al tipo de cambio.
2. **Idioma**: Todo el contenido del commit (descripción y cuerpo) debe estar en **ESPAÑOL**.
3. **Límite del Título**: La primera línea (asunto) **NO debe exceder los 50 caracteres** (sin contar el emoji). Sé conciso.
4. **Descripción Extensa**: El cuerpo del mensaje es **OBLIGATORIO**. Debes explicar detalladamente:
   - **Qué** se ha cambiado.
   - **Por qué** se ha hecho el cambio.
   - Detalles técnicos relevantes de la implementación.
5. **Tiempos Verbales**: Usa el modo imperativo en el asunto (ej: "agrega", "corrige", "cambia"), no en pasado.

## Tipos Permitidos y Emojis

| Emoji | Tipo | Descripción |
| :---: | :--- | :--- |
| ✨ | `feat` | Nueva característica (correlaciona con MINOR en SemVer). |
| 🐛 | `fix` | Corrección de un bug (correlaciona con PATCH en SemVer). |
| 📚 | `docs` | Cambios en la documentación. |
| 💄 | `style` | Cambios que no afectan el significado del código (espacios, formato, etc). |
| ♻️ | `refactor` | Cambio de código que no corrige bugs ni añade funcionalidades. |
| ⚡ | `perf` | Cambio de código que mejora el rendimiento. |
| ✅ | `test` | Añadir tests faltantes o corregir existentes. |
| 📦 | `build` | Cambios que afectan el sistema de construcción o dependencias externas. |
| 👷 | `ci` | Cambios en archivos de configuración y scripts de CI. |
| 🔧 | `chore` | Otros cambios que no modifican src o test files (ej. config de herramientas). |
| ⏪ | `revert` | Reversión de un commit anterior. |

## Procedimiento

Cuando el usuario pida hacer commit:

1. **Analiza los cambios**: Revisa qué archivos se modificaron y qué tipo de cambio representan.
2. **Selecciona el tipo**: Elige el tipo de commit más apropiado de la tabla.
3. **Define el alcance**: Identifica el módulo o componente afectado (opcional pero recomendado).
4. **Redacta el asunto**: Máximo 50 caracteres, imperativo, en español.
5. **Redacta el cuerpo**: Explica qué, por qué y detalles técnicos. Es obligatorio.
6. **Ejecuta el commit**: Usa `git commit -m` con el formato completo.

## Ejemplo Correcto

```text
✨ feat(auth): integra login social con Google

Se ha implementado la autenticación mediante OAuth2 con Google para facilitar
el acceso a nuevos usuarios.

Cambios principales:
- Agrega configuración de estrategia de Passport.js para Google.
- Crea nuevas rutas de callback en el controlador de autenticación.
- Actualiza el modelo de Usuario para almacenar el providerId.
- Ajusta la interfaz de login para incluir el botón de "Entrar con Google".

Motivación:
Reducir la fricción en el registro de usuarios y aumentar la conversión.
```

## Errores Comunes a Evitar

- `fix: error login` → Falta emoji, título vago, sin cuerpo.
- `🐛 Fix: arregla login` → Tipo en mayúscula, lo correcto es minúscula `fix`.
- `✨ feat(user): Update user logic` → En inglés, debe ser en español.
- Título que excede 50 caracteres → Acorta y mueve el detalle al cuerpo.

## Integración con el Workflow

Después de ejecutar un commit exitoso, el router debe activar la skill `changelog-updater` para registrar el cambio automáticamente en `CHANGELOG.md`.
