---
name: sonarqube-quality-gate-playbook
description: Playbook iterativo para llevar proyectos Node y TypeScript (NestJS + React en monorepo) a cumplir Quality Gates de SonarQube sin romper build ni pipelines. Usar cuando se necesite subir cobertura priorizando New Code, eliminar issues nuevos (Bugs, Vulnerabilities, Code Smells), revisar Security Hotspots y controlar duplicacion y deuda tecnica.
---

# SonarQube Quality Gate Playbook

Aplicar este flujo en iteraciones pequenas y verificables. Priorizar impacto real y bajo riesgo.

## Inputs requeridos

Definir estos inputs antes del primer ciclo:

- `SONAR_HOST_URL` (ejemplo: `http://127.0.0.1:9000`)
- `SONAR_TOKEN` con permisos de analisis
- `SONAR_PROJECT_KEY` y opcional `SONAR_PROJECT_NAME`
- `SONAR_NEW_CODE_REFERENCE_BRANCH` (default: `main`)
- Rutas del monorepo: `apps/backend`, `apps/frontend`, `packages/*`
- Comandos de test por app (backend/frontend) con coverage
- Rutas de reportes `lcov.info` por app
- Archivo Sonar (`sonar-project.properties`) o parametros equivalentes en CI
- Patron de exclusiones de coverage y de analisis
- Umbrales del Quality Gate (coverage, bugs, vulns, smells, duplicacion)
- Comando de build/pipeline que no se puede romper

## Estrategia de priorizacion

Seguir este orden de trabajo:

1. New Code primero
2. Nuevos Bugs y Vulnerabilities
3. Security Hotspots en estado `TO_REVIEW`
4. Coverage en modulos criticos y tocados por el PR
5. Nuevos Code Smells (priorizar severidad alta)
6. Duplicacion y deuda tecnica en zonas activas
7. Deuda historica (solo si no afecta el objetivo del sprint)

### Heuristica de impacto

Para cada issue o archivo, calcular prioridad de manera simple:

`priorityScore = (isNewCode*100) + (isBugOrVuln*80) + (isHotspotToReview*70) + severityWeight + (criticalPath*20) + (coverageGap*10) - (estimatedEffort*5)`

Donde `severityWeight` puede ser: blocker `40`, critical `30`, major `20`, minor `10`.

### Regla anti inflado de coverage

No aceptar tests que solo suben porcentaje sin validar comportamiento:

- Todo test nuevo debe cubrir caso feliz, caso negativo y borde
- Prohibido snapshot-only como unica asercion
- Evitar tests triviales de codigo sin logica
- Si el test no falla ante un bug real, no cuenta como cobertura de valor

## Pipeline del skill (paso a paso)

## Runbook de discrepancia de cobertura (caso reutilizable)

Usar este runbook cuando SonarQube muestre cobertura mucho menor a la local.

### Sintoma tipico

- Local (Jest/Vitest): cobertura alta (por ejemplo >90%)
- SonarQube: cobertura sensiblemente menor (por ejemplo 40-60%)

### Causas raiz frecuentes

1. Rutas `SF:` con backslashes (`\\`) en `lcov.info` generadas en Windows.
2. SonarQube ejecutando en Linux/containers sin poder mapear rutas con `\\`.
3. Packages compartidos con cobertura baja (ejemplo `packages/utils`) tirando abajo el global.

### Diagnostico rapido

1. Revisar primeras entradas `SF:` del `lcov.info` de cada app/package.
2. Verificar en logs de `sonar-scanner` si hay archivos de coverage no mapeados o ignorados.
3. Comparar cobertura por modulo (backend/frontend/packages) para detectar outliers.

Comandos sugeridos:

```powershell
Get-Content "apps\\backend\\coverage\\lcov.info" | Select-String "^SF:" | Select-Object -First 10
Get-Content "apps\\frontend\\coverage\\lcov.info" | Select-String "^SF:" | Select-Object -First 10
```

Si aparecen rutas como `SF:src\\app.ts`, normalizar antes del scan.

### Remediacion recomendada

1. Normalizar rutas a forward slash (`/`) en todos los `lcov.info` antes de `sonar-scanner`.
2. Re-ejecutar tests de coverage y scan.
3. Subir cobertura del paquete/modulo de menor porcentaje para no sesgar el global.

Ejemplo portable (`scripts/fix-lcov-paths.js`):

```js
const fs = require('node:fs');

const reports = [
  'apps/backend/coverage/lcov.info',
  'apps/frontend/coverage/lcov.info',
  'packages/utils/coverage/lcov.info'
];

for (const reportPath of reports) {
  if (!fs.existsSync(reportPath)) continue;
  const content = fs.readFileSync(reportPath, 'utf8');
  const normalized = content.replace(/\\\\/g, '/');
  fs.writeFileSync(reportPath, normalized);
}
```

Guardrail CI (fallar si quedan backslashes):

```bash
if grep -q 'SF:.*\\\\' apps/backend/coverage/lcov.info; then
  echo "ERROR: Backslashes encontrados en lcov.info"
  exit 1
fi
```

### Paso 1: Detectar gap actual

1. Ejecutar tests con coverage en backend/frontend/packages relevantes
2. Ejecutar analisis SonarQube
3. Levantar metricas e issues nuevos para priorizar

Comandos genericos:

```powershell
bun run --cwd apps/backend test -- --coverage
bun run --cwd apps/frontend test -- --coverage

sonar-scanner `
  -Dsonar.host.url=$env:SONAR_HOST_URL `
  -Dsonar.token=$env:SONAR_TOKEN `
  -Dsonar.projectKey=$env:SONAR_PROJECT_KEY `
  -Dsonar.qualitygate.wait=true

curl -4 -s "$env:SONAR_HOST_URL/api/measures/component?component=$env:SONAR_PROJECT_KEY&metricKeys=coverage,new_coverage,bugs,new_bugs,vulnerabilities,new_vulnerabilities,code_smells,new_code_smells,duplicated_lines_density,new_duplicated_lines_density" -u "$env:SONAR_TOKEN:"

curl -4 -s "$env:SONAR_HOST_URL/api/issues/search?componentKeys=$env:SONAR_PROJECT_KEY&resolved=false&inNewCodePeriod=true&types=BUG,VULNERABILITY,CODE_SMELL&ps=500" -u "$env:SONAR_TOKEN:"

curl -4 -s "$env:SONAR_HOST_URL/api/hotspots/search?projectKey=$env:SONAR_PROJECT_KEY&status=TO_REVIEW&ps=500" -u "$env:SONAR_TOKEN:"
```

### Paso 2: Generar o actualizar config Sonar

Crear o actualizar `sonar-project.properties` en raiz con rutas reales del monorepo.

### Paso 3: Asegurar lectura de coverage real

- Verificar existencia de `lcov.info`
- Configurar `sonar.javascript.lcov.reportPaths` con todas las rutas
- Validar en logs del scanner que no haya warnings de coverage faltante
- Verificar que lineas `SF:` usen `/` y no `\\`
- Si hay entorno mixto Windows/Linux, correr normalizacion de paths antes del scan
- Confirmar que packages compartidos relevantes tambien reporten coverage (no solo apps)

### Paso 4: Ejecutar tests de forma consistente

- Usar los mismos comandos y flags en local y CI
- Publicar artefactos de coverage
- No mezclar runners/flags entre entornos

### Paso 5: Iterar por lotes pequenos

- Lote A: Bugs/Vulns/Hotspots nuevos
- Lote B: Coverage en New Code
- Lote C: Code Smells nuevos
- Lote D: Duplicacion/deuda en areas tocadas

## Generacion de tests guiada (backend y frontend)

## 1) Identificar archivos sin cobertura

- Fuente principal: SonarQube (archivos con uncovered lines en New Code)
- Fuente secundaria: `lcov.info` + archivos modificados del PR

```powershell
git diff --name-only origin/main...HEAD | Where-Object { $_ -match '\.(ts|tsx)$' }
```

## 2) Elegir tipo de test correcto

- Unit: logica pura y funciones con pocas dependencias
- Integration (backend): controladores + servicios + repositorios mockeados
- Component (frontend): interacciones, estados y accesibilidad
- E2E: solo flujos criticos, no como reemplazo de unit/component

## 3) Mocking strategy

- DB: fake repo o base de test aislada
- HTTP externo: mocks deterministas (sin pegar a servicios reales)
- Tiempo/random: controlar reloj y valores aleatorios
- Evitar mocks excesivos que oculten defectos reales

## 4) Criterios minimos de calidad del test

- Estructura Arrange/Act/Assert clara
- Aserciones semanticas del comportamiento esperado
- Caso feliz + negativo + borde obligatorios
- Test estable y sin flakiness
- Nombre orientado a comportamiento

## 5) Naming y estructura

- Backend: `*.spec.ts`
- Frontend: `*.test.tsx`
- Patron recomendado:
  - `should <resultado> when <condicion>`
  - `returns <error> when <input invalido>`

## Remediacion de Code Smells, Bugs y Security

Aplicar fixes quirurgicos, sin cambios de estilo masivos.

Checklist por categoria:

- Complejidad: extraer funciones, usar early return, bajar anidacion
- Duplicacion: consolidar utilidades y evitar copy-paste
- Nullability: guards explicitos y defaults seguros
- Manejo de errores: evitar `catch` vacio, propagar con contexto
- Leaks/resources: cerrar timers, subscripciones, conexiones
- Regex/DoS: evitar patrones catastróficos y limitar input
- Dependencias inseguras: actualizar librerias vulnerables
- Sanitizacion: validar y sanitizar input, evitar XSS/inyeccion
- Security Hotspots: revisar y documentar resolucion por cada item

## Reglas de exclusion y trade-offs

Exclusiones aceptables (con justificativo):

- `**/index.ts` sin logica
- DTOs o types simples sin ramas
- codigo generado (`**/generated/**`)
- bootstrap minimo sin logica de negocio

Exclusiones no aceptables:

- servicios/casos de uso/controladores con logica
- hooks y validadores con ramas
- codigo de autenticacion/autorizacion
- excluir para pasar el porcentaje sin mejorar calidad

Regla: cada exclusion debe registrar el motivo tecnico.

## Definicion de Done y metricas

Declarar ciclo completado solo con evidencia:

- Quality Gate en estado `PASSED`
- `new_coverage >= 80`
- `new_bugs = 0`
- `new_vulnerabilities = 0`
- `new_code_smells = 0`
- `new_security_hotspots_reviewed = 100%`
- Duplicacion y deuda dentro de umbral del gate
- Build y pipelines verdes

Evidencia minima a adjuntar:

1. salida de `sonar-scanner` con `sonar.qualitygate.wait=true`
2. salida de APIs de metricas/issues/hotspots
3. cobertura por carpeta (backend/frontend/packages)
4. resumen de issues resueltos (antes/despues)

## Snippets de configuracion

### sonar-project.properties

```properties
sonar.projectKey=my-org_my-monorepo
sonar.projectName=my-monorepo
sonar.sourceEncoding=UTF-8

sonar.sources=apps/backend/src,apps/frontend/src,packages
sonar.tests=apps/backend,apps/frontend,packages
sonar.test.inclusions=**/*.spec.ts,**/*.test.ts,**/*.test.tsx,**/*.spec.tsx

sonar.javascript.lcov.reportPaths=apps/backend/coverage/lcov.info,apps/frontend/coverage/lcov.info
sonar.newCode.referenceBranch=main

sonar.exclusions=**/dist/**,**/build/**,**/node_modules/**,**/*.d.ts
sonar.coverage.exclusions=**/index.ts,**/*.dto.ts,**/generated/**,**/*.stories.tsx
```

### Jest backend (ejemplo)

```ts
import type { Config } from 'jest';

const config: Config = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.dto.ts',
    '!src/**/index.ts',
    '!src/**/generated/**'
  ]
};

export default config;
```

### Vitest frontend (ejemplo)

```ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'html'],
      reportsDirectory: './coverage',
      include: ['src/**/*.{ts,tsx}'],
      exclude: ['src/**/*.stories.tsx', 'src/**/index.ts']
    }
  }
});
```

### GitHub Actions (ejemplo)

```yaml
name: quality-gate

on:
  pull_request:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: oven-sh/setup-bun@v2
      - run: bun install --frozen-lockfile

      - name: Backend tests with coverage
        run: bun run --cwd apps/backend test -- --coverage

      - name: Frontend tests with coverage
        run: bun run --cwd apps/frontend test -- --coverage

      - name: Normalize lcov paths (Windows/Linux safe)
        run: node scripts/fix-lcov-paths.js

      - name: Validate lcov path format
        run: |
          if grep -q 'SF:.*\\\\' apps/backend/coverage/lcov.info; then
            echo "ERROR: Backslashes encontrados en backend lcov.info"
            exit 1
          fi

      - name: Build
        run: bun run build

      - name: SonarQube Scan
        env:
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: |
          sonar-scanner \
            -Dsonar.host.url=$SONAR_HOST_URL \
            -Dsonar.token=$SONAR_TOKEN \
            -Dsonar.qualitygate.wait=true
```

### GitLab CI (ejemplo)

```yaml
stages:
  - test
  - quality

variables:
  GIT_DEPTH: "0"

test_and_build:
  stage: test
  image: oven/bun:1
  script:
    - bun install --frozen-lockfile
    - bun run --cwd apps/backend test -- --coverage
    - bun run --cwd apps/frontend test -- --coverage
    - node scripts/fix-lcov-paths.js
    - bun run build
  artifacts:
    when: always
    paths:
      - apps/backend/coverage/
      - apps/frontend/coverage/

sonarqube:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  dependencies:
    - test_and_build
  script:
    - sonar-scanner -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.token=$SONAR_TOKEN -Dsonar.qualitygate.wait=true
  allow_failure: false
```

## README del skill

Usar este resumen rapido en ejecucion:

1. correr tests con coverage
2. correr sonar-scanner con wait del gate
3. priorizar New Code -> Bugs/Vulns -> Hotspots -> Coverage -> Smells
4. iterar en lotes pequenos y adjuntar evidencia

Comandos base:

- `bun run --cwd apps/backend test -- --coverage`
- `bun run --cwd apps/frontend test -- --coverage`
- `sonar-scanner -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.token=$SONAR_TOKEN -Dsonar.qualitygate.wait=true`

## Checklist de PR

- [ ] No hay nuevos Bugs ni Vulnerabilities
- [ ] No hay nuevos Code Smells
- [ ] New Coverage >= 80%
- [ ] Hotspots nuevos revisados
- [ ] Sin exclusiones injustificadas
- [ ] Tests con caso feliz, negativo y borde
- [ ] Build y CI en verde
- [ ] Evidencia de Sonar adjunta
- [ ] `lcov.info` sin backslashes en lineas `SF:`
- [ ] Packages compartidos sin brecha fuerte de coverage

## Plantillas de comandos listas para pegar

```powershell
$env:SONAR_HOST_URL="http://127.0.0.1:9000"
$env:SONAR_TOKEN="<token>"
$env:SONAR_PROJECT_KEY="<project-key>"

bun run --cwd apps/backend test -- --coverage
bun run --cwd apps/frontend test -- --coverage
bun run build

sonar-scanner `
  -Dsonar.host.url=$env:SONAR_HOST_URL `
  -Dsonar.token=$env:SONAR_TOKEN `
  -Dsonar.projectKey=$env:SONAR_PROJECT_KEY `
  -Dsonar.qualitygate.wait=true

curl -4 -s "$env:SONAR_HOST_URL/api/measures/component?component=$env:SONAR_PROJECT_KEY&metricKeys=new_coverage,new_bugs,new_vulnerabilities,new_code_smells,new_duplicated_lines_density" -u "$env:SONAR_TOKEN:"
```

## Defaults a ajustar si hay incertidumbre

- branch de New Code: `main`
- umbral New Coverage: `80`
- duplicacion maxima new code: `3%`
- coverage exclusions: solo archivos sin logica
- estrategia de lotes: 1 PR por categoria critica
