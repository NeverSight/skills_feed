---
name: dev-rules
description: >
  Reglas de desarrollo globales para todos los proyectos. Activar siempre que Claude
  asista en tareas de programación, revisión de código, generación de código, commits,
  pull requests o cualquier tarea de ingeniería de software. Define idioma de comunicación,
  estilo de código, convenciones de git, principios de arquitectura, seguridad, rendimiento
  y manejo de errores. Aplica a cualquier lenguaje o framework.
---

# Dev Rules

## Invocación

Al invocar /dev-rules, mostrar el siguiente resumen al usuario:

Dev Rules v1.0.0

Comunicación   - Español, conciso, sin disculpas
Estilo         - Convenciones del proyecto, nombres descriptivos
Documentación  - Solo el "por qué", TODOs para incompletos
Git            - Conventional Commits, confirmar antes de commit/push
Código         - SOLID, composición sobre herencia, early returns, SRP
Arquitectura   - Capas separadas, DTOs, inyección de dependencias
Performance    - Caché, lazy loading, paginación
Errores        - Fail fast, logs por nivel, mensajes amigables
Seguridad      - Sin secrets en código/logs, queries parametrizadas
Testing        - Solo si se solicita
Deploy         - No modificar sin confirmación, respetar entornos
DB             - Sin queries destructivas sin confirmación

Reglas por tecnología:
  TS/Angular     - Sin any, inject(), async pipe, standalone + signals
  Java/Spring    - Constructor injection, Transactional, records, Jakarta
  Flutter/Dart   - const constructors, trailing commas, Bloc/Riverpod
  Kotlin/Compose - PascalCase Composable, Modifier en layout raíz

No agregar nada más. Solo mostrar el resumen.

## Idioma y Comunicación
- Responder siempre en español.
- Ser conciso pero completo.
- No disculparse por errores; corregirlos directamente.

## Formato y Estilo
- Seguir las convenciones del proyecto existente.
- Nombres descriptivos; el código debe hablar por sí mismo.
- Preferir código conciso sobre código documentado verbosamente.

## Documentación
- Documentar solo decisiones técnicas importantes o lógica no obvia.
- Comentarios solo para explicar el "por qué", nunca el "qué".
- Usar TODO para código incompleto.

## Git y Control de Versiones
- No hacer commit ni push sin confirmación explícita del usuario.
- Conventional Commits: feat, fix, docs, chore, refactor, test, ci.
- Ramas descriptivas: feature/, fix/, hotfix/, chore/.

## Código Limpio
- Principios SOLID.
- Composición sobre herencia.
- Sin comentarios decorativos ni separadores visuales excesivos.
- Early returns para condiciones de error (evitar nesting profundo).
- Métodos/funciones pequeños con una sola responsabilidad.
- DRY: extraer lógica duplicada solo cuando se repite 3+ veces.

## Arquitectura y Patrones
- Respetar la arquitectura existente del proyecto (microservicios, monolito, etc.).
- Separar claramente capas: controlador, servicio, repositorio/data.
- DTOs para transferencia entre capas; nunca exponer entidades directamente en APIs.
- Inyección de dependencias; evitar instanciación directa de servicios.

## TypeScript/Angular
- Evitar any; usar tipos específicos o unknown.
- inject() para inyección de servicios.
- async pipe para observables en templates.
- Preferir standalone components y signals.

## Java/Spring Boot
- Constructor Injection (sin Field Injection en producción).
- Transactional(readOnly = true) para lecturas, Transactional para escrituras.
- Java records para DTOs Request/Response.
- Validar inputs con Jakarta Validation.

## Flutter/Dart
- Constructores const para widgets inmutables.
- Evitar el operador bang (!) a menos que el valor esté garantizado no-nulo.
- Trailing commas para mejor formateo.
- State management (Bloc/Riverpod) para apps complejas.

## Kotlin/Compose
- Funciones Composable en PascalCase como sustantivos.
- Parámetros: obligatorios primero, luego Modifier, luego opcionales.
- Modifier se aplica solo al layout raíz.

## Performance
- Considerar el impacto en rendimiento de cada cambio.
- Usar caché cuando sea apropiado.
- Lazy loading y paginación; evitar cargar datos innecesarios.

## Manejo de Errores
- Fail fast: manejar errores al inicio de funciones.
- Logear con nivel apropiado: ERROR, WARN, INFO, DEBUG.
- Retornar mensajes amigables al usuario; detalles técnicos solo en logs.

## Seguridad
- Nunca exponer secrets, API keys o credenciales en código o logs.
- Nunca logear datos sensibles (passwords, tokens, datos personales).
- Parametrizar siempre queries SQL.
- Validar y sanitizar toda entrada externa.

## Testing
- No generar código de pruebas a menos que se solicite explícitamente.

## Docker y Despliegue
- No modificar Dockerfiles ni pipelines CI/CD sin confirmación explícita.
- Respetar la separación de entornos (dev, cert, prod).

## Base de Datos
- Nunca ejecutar queries destructivas (DROP, TRUNCATE, DELETE masivo) sin confirmación.
- Preferir migraciones versionadas sobre cambios manuales de esquema.
