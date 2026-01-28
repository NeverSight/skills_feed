---
name: git-reconciler
description: Sincroniza branch con main/master detectando conflictos antes de mergear. Usa cuando el usuario diga "sync con main", "actualizar branch", "traer cambios de main", "reconciliar", "merge main", "hay conflictos?", o tenga branch desactualizado.
allowed-tools: Bash, Read
---

# Git Reconciler

Skill para sincronizar tu branch de trabajo con main/master de forma segura, detectando conflictos antes de mergear.

## Cuando usar esta Skill

- Usuario pide "actualizar branch", "sync con main", "traer cambios de main"
- Usuario pide "reconciliar", "merge main", "rebase"
- Usuario pregunta si hay conflictos con main
- Branch esta desactualizado respecto a origin/main
- Antes de crear un PR para asegurar que no hay conflictos

## Proceso

### Paso 1: Verificar estado actual

```bash
# Estado del repo y branch actual
git status

# Identificar branch actual
git branch --show-current

# Verificar si hay cambios sin commitear
git status --porcelain
```

**IMPORTANTE**: Si hay cambios sin commitear, preguntar al usuario:
- Queres hacer commit primero?
- Queres hacer stash?
- Queres descartar cambios?

### Paso 2: Identificar branch principal

```bash
# Detectar si es main o master
git remote show origin | grep "HEAD branch" | cut -d: -f2 | tr -d ' '
```

Si falla, probar:
```bash
# Verificar cual existe
git branch -r | grep -E "origin/(main|master)$" | head -1 | sed 's/.*origin\///'
```

### Paso 3: Fetch de cambios remotos

```bash
# Traer cambios sin aplicar
git fetch origin main  # o master segun detectado
```

### Paso 4: Analizar divergencia

```bash
# Commits en main que no estan en tu branch
git log HEAD..origin/main --oneline

# Commits en tu branch que no estan en main
git log origin/main..HEAD --oneline

# Ver cuanto divergieron
git rev-list --left-right --count origin/main...HEAD
```

El output de `rev-list` es: `<commits_en_main> <commits_en_branch>`

Interpretar:
- `0 0` = Sincronizados, no hay nada que hacer
- `5 0` = Main tiene 5 commits nuevos, tu branch esta atras
- `0 3` = Tu branch tiene 3 commits, main no tiene nuevos (solo push needed)
- `5 3` = Divergencia: main tiene 5 nuevos, tu branch tiene 3

### Paso 5: Detectar conflictos potenciales

```bash
# Ver archivos modificados en main desde que divergieron
git diff --name-only HEAD...origin/main

# Ver archivos modificados en tu branch
git diff --name-only origin/main...HEAD
```

Comparar las listas. Si hay archivos en comun, hay riesgo de conflicto.

Para verificar conflictos sin mergear:
```bash
# Simulacion de merge (no aplica cambios)
git merge-tree $(git merge-base HEAD origin/main) HEAD origin/main
```

Si el output contiene `<<<<<<` o `>>>>>>`, habra conflictos.

### Paso 6: Sugerir estrategia

Presentar al usuario:

**Opcion A: Merge (recomendado para branches compartidos)**
```
git merge origin/main
```
- Preserva historial completo
- Crea commit de merge
- Mas seguro para branches con colaboradores

**Opcion B: Rebase (recomendado para branches personales)**
```
git rebase origin/main
```
- Historial lineal
- Reescribe commits (requiere force push si ya pusheaste)
- Mejor para branches limpios antes de PR

Pregunta:
```
Estrategia recomendada: [merge/rebase] porque [razon].
Cual preferis? [merge/rebase]
```

### Paso 7: Ejecutar sincronizacion

**Si eligio MERGE:**
```bash
git merge origin/main
```

**Si eligio REBASE:**
```bash
git rebase origin/main
```

### Paso 8: Manejar conflictos (si ocurren)

Si hay conflictos, listarlos:
```bash
# Listar archivos con conflictos
git diff --name-only --diff-filter=U
```

Mostrar al usuario:
```
Hay conflictos en los siguientes archivos:
- src/components/Auth.tsx
- src/utils/helpers.ts

Opciones:
1. Resolver conflictos manualmente (te guio archivo por archivo)
2. Abortar merge: git merge --abort
3. Abortar rebase: git rebase --abort
```

Para cada archivo con conflicto:
```bash
# Mostrar las secciones en conflicto
git diff <archivo>
```

### Paso 9: Verificar resultado

```bash
# Confirmar estado limpio
git status

# Verificar que estas sincronizado
git log --oneline -5
```

---

## Soporte para Worktrees

Si el usuario trabaja con worktrees (patron `.worktrees/`):

### Detectar si estamos en worktree
```bash
# Verificar si estamos en un worktree
git rev-parse --is-inside-work-tree
git worktree list
```

### Consideraciones especiales para worktrees

1. **El main/master suele estar en el repo principal**, no en el worktree
2. **Fetch desde el worktree** funciona igual
3. **Rebase puede ser problematico** si el worktree comparte objetos

Flujo para worktree:
```bash
# Desde el worktree
pwd  # Verificar que estamos en .worktrees/<branch>

# Fetch funciona normal
git fetch origin main

# Merge/rebase normal
git merge origin/main
```

---

## Ejemplos

### Ejemplo 1: Sincronizar branch de feature

Usuario: "Necesito actualizar mi branch con main"

```bash
$ git status
On branch feature/auth
Your branch is up to date with 'origin/feature/auth'.

$ git fetch origin main
$ git rev-list --left-right --count origin/main...HEAD
3       5

# Interpretacion: main tiene 3 commits nuevos, tu branch tiene 5 commits propios

$ git diff --name-only HEAD...origin/main
src/config.ts
README.md

$ git diff --name-only origin/main...HEAD
src/components/Auth.tsx
src/hooks/useAuth.ts
tests/auth.test.ts
```

Respuesta:
```
Tu branch `feature/auth` tiene 5 commits propios y main tiene 3 commits nuevos.

Archivos modificados en main: src/config.ts, README.md
Archivos modificados en tu branch: 3 archivos en src/components, src/hooks, tests/

No hay archivos en comun, bajo riesgo de conflictos.

Estrategia recomendada: MERGE (tu branch ya fue pusheado)
Confirmas que haga merge de origin/main? [y/n]
```

### Ejemplo 2: Detectar conflictos antes de mergear

Usuario: "Hay conflictos con main?"

```bash
$ git fetch origin main
$ git diff --name-only HEAD...origin/main
src/utils/api.ts
src/components/Header.tsx

$ git diff --name-only origin/main...HEAD
src/utils/api.ts
src/components/Auth.tsx
```

Respuesta:
```
Hay riesgo de conflicto en:
- src/utils/api.ts (modificado en ambos branches)

Archivos solo en main: src/components/Header.tsx
Archivos solo en tu branch: src/components/Auth.tsx

Te recomiendo hacer merge ahora para resolver el conflicto de api.ts antes de que crezca.
Queres que haga el merge? [y/n]
```

### Ejemplo 3: Branch en worktree

Usuario: "Actualizar este worktree con main"

```bash
$ pwd
/Users/user/project/.worktrees/feature-login

$ git worktree list
/Users/user/project              abc1234 [main]
/Users/user/project/.worktrees/feature-login  def5678 [feature-login]

$ git fetch origin main
$ git merge origin/main
Already up to date.
```

Respuesta:
```
Estas trabajando en el worktree `feature-login`.
El worktree esta sincronizado con origin/main, no hay cambios nuevos que mergear.
```

### Ejemplo 4: Resolver conflictos

Despues de merge con conflictos:

```bash
$ git merge origin/main
Auto-merging src/utils/api.ts
CONFLICT (content): Merge conflict in src/utils/api.ts
Automatic merge failed; fix conflicts and then commit the result.

$ git diff --name-only --diff-filter=U
src/utils/api.ts
```

Respuesta:
```
Hay conflicto en src/utils/api.ts.

Opciones:
1. Te muestro el conflicto para que lo resuelvas
2. Abortar merge (git merge --abort)

Que preferis? [1/2]
```

Si elige 1:
```bash
$ git diff src/utils/api.ts
```

Mostrar el diff y guiar la resolucion.

---

## Comandos de referencia rapida

| Accion | Comando |
|--------|---------|
| Ver estado | `git status` |
| Fetch sin merge | `git fetch origin main` |
| Ver divergencia | `git rev-list --left-right --count origin/main...HEAD` |
| Commits pendientes de main | `git log HEAD..origin/main --oneline` |
| Merge main | `git merge origin/main` |
| Rebase sobre main | `git rebase origin/main` |
| Abortar merge | `git merge --abort` |
| Abortar rebase | `git rebase --abort` |
| Listar conflictos | `git diff --name-only --diff-filter=U` |
| Ver worktrees | `git worktree list` |
