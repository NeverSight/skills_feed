---
name: worktree-manager
description: Gestiona git worktrees en .worktrees/. Usa cuando el usuario diga "crear worktree", "nuevo branch en paralelo", "trabajar en otra feature", "limpiar worktrees", "listar worktrees", o quiera desarrollo paralelo sin cambiar de branch.
allowed-tools: Bash, Read, Write
---

# Worktree Manager

Skill para gestionar git worktrees siguiendo la estrategia de carpeta `.worktrees/` dentro del repositorio.

## Cuando usar esta Skill

- Usuario pide crear un nuevo worktree o branch de trabajo
- Usuario pide listar worktrees activos
- Usuario pide limpiar worktrees despues de merge
- Usuario menciona "worktree", "nuevo branch", "feature branch"
- Usuario pide podar referencias huerfanas

## Estructura de Worktrees

```
~/Projects/<github|gitlab>/<project>/
├── .worktrees/                     # ignorado por .gitignore
│   ├── feature-x/                  # worktree para branch feature-x
│   └── bugfix-123/                 # worktree para branch bugfix-123
├── src/                            # archivos del repo (master/main)
└── .gitignore                      # debe incluir .worktrees/
```

## Proceso

### Paso 0: Verificar contexto

Antes de cualquier operacion, verificar que estamos en un repositorio git:

```bash
# Verificar que es un repo git
git rev-parse --is-inside-work-tree

# Verificar rama actual (debe ser main o master para operaciones desde root)
git branch --show-current
```

---

## Comandos Disponibles

### 1. Setup Inicial

Ejecutar una vez por proyecto para habilitar worktrees:

```bash
# Verificar si .worktrees/ esta en .gitignore
grep -q "^\.worktrees/$" .gitignore 2>/dev/null || echo ".worktrees/" >> .gitignore

# Crear carpeta .worktrees si no existe
mkdir -p .worktrees

# Verificar estado
cat .gitignore | grep worktrees
```

Si `.worktrees/` no estaba en `.gitignore`, hacer commit:

```bash
git add .gitignore
git commit -m "chore: ignore worktrees folder"
```

### 2. Crear Worktree

Para crear un nuevo worktree con branch nuevo:

```bash
# Sintaxis: git worktree add .worktrees/<nombre-branch> -b <nombre-branch>
git worktree add .worktrees/feature-nueva-funcionalidad -b feature-nueva-funcionalidad
```

El branch debe seguir convenciones:
- `feature/<descripcion>` o `feature-<descripcion>` para nuevas features
- `bugfix/<descripcion>` o `bugfix-<descripcion>` para correcciones
- `hotfix/<descripcion>` para arreglos urgentes
- `chore/<descripcion>` para tareas de mantenimiento

### 3. Listar Worktrees

Ver todos los worktrees activos:

```bash
git worktree list
```

Output esperado:
```
/Users/user/Projects/github/mi-proyecto        abc1234 [main]
/Users/user/Projects/github/mi-proyecto/.worktrees/feature-x  def5678 [feature-x]
```

### 4. Trabajar en Worktree

Despues de crear, navegar al worktree:

```bash
cd .worktrees/<nombre-branch>

# Trabajar normalmente...
# hacer cambios...

# Commit y push
git add .
git commit -m "feat: descripcion del cambio"
git push -u origin <nombre-branch>
```

### 5. Cleanup despues de Merge

Una vez que el PR fue mergeado, limpiar:

```bash
# Desde el directorio raiz del proyecto (no desde el worktree)

# Paso 1: Remover worktree
git worktree remove .worktrees/<nombre-branch>

# Paso 2: Eliminar branch remoto (si no se elimino con el PR)
git push origin --delete <nombre-branch>

# Paso 3: Eliminar branch local si existe
git branch -d <nombre-branch>
```

### 6. Podar Referencias Huerfanas

Limpiar referencias a worktrees que fueron eliminados manualmente:

```bash
git worktree prune
```

---

## Flujo Completo de Trabajo

### Ejemplo: Nueva Feature

```bash
# 1. Asegurar que estamos en main/master actualizado
git checkout main
git pull origin main

# 2. Verificar setup (primera vez)
grep -q "^\.worktrees/$" .gitignore || echo ".worktrees/" >> .gitignore

# 3. Crear worktree para la feature
git worktree add .worktrees/feature-auth -b feature-auth

# 4. Ir al worktree
cd .worktrees/feature-auth

# 5. Desarrollar, commit, push
# ... hacer cambios ...
git add .
git commit -m "feat: add authentication module"
git push -u origin feature-auth

# 6. Crear PR (desde GitHub CLI o web)
gh pr create --title "feat: add authentication module" --body "..."

# 7. Despues del merge, volver al root y limpiar
cd ../..  # volver a raiz del proyecto
git worktree remove .worktrees/feature-auth
git push origin --delete feature-auth
```

### Ejemplo: Bugfix Rapido

```bash
# Desde main actualizado
git pull origin main

# Crear worktree para el fix
git worktree add .worktrees/bugfix-login-error -b bugfix-login-error

# Trabajar en el fix
cd .worktrees/bugfix-login-error
# ... fix ...
git add . && git commit -m "fix: resolve login error on mobile"
git push -u origin bugfix-login-error

# Crear PR
gh pr create --title "fix: resolve login error" --body "..."

# Despues del merge
cd ../..
git worktree remove .worktrees/bugfix-login-error
```

---

## Principios Clave

| Principio | Descripcion |
|-----------|-------------|
| Worktrees son temporales | No son casas permanentes, se eliminan despues del merge |
| Main siempre limpio | El repo principal siempre esta en main/master |
| Nombres descriptivos | Carpeta del worktree = nombre del branch |
| Cleanup obligatorio | Siempre limpiar despues del merge del PR |

---

## Troubleshooting

### Error: "worktree already exists"

El worktree ya existe. Listar y verificar:

```bash
git worktree list
ls -la .worktrees/
```

### Error: "branch already exists"

El branch ya existe. Opciones:

```bash
# Opcion 1: Usar branch existente (sin -b)
git worktree add .worktrees/feature-x feature-x

# Opcion 2: Eliminar branch viejo primero
git branch -D feature-x
git worktree add .worktrees/feature-x -b feature-x
```

### Error: "is already checked out"

El branch esta checked out en otro lugar:

```bash
# Ver donde esta el branch
git worktree list

# Remover el worktree anterior primero
git worktree remove .worktrees/<branch-name>
```

### Limpiar worktrees huerfanos

Si se eliminaron carpetas manualmente sin `git worktree remove`:

```bash
git worktree prune
git worktree list  # verificar que se limpio
```

---

## Preguntas al Usuario

Antes de crear un worktree, preguntar:

1. **Nombre del branch**: "Como quieres llamar al branch?" (sugerir formato `feature-*` o `bugfix-*`)
2. **Confirmar estructura**: Si es primera vez, confirmar que se agregara `.worktrees/` a `.gitignore`

Antes de cleanup, confirmar:

1. **PR mergeado?**: "El PR ya fue mergeado? Confirmar antes de eliminar el worktree."
2. **Branch remoto**: "Eliminar tambien el branch remoto?"
