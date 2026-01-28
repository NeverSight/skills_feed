---
name: blast-operador
description: |
  Skill T (Operador) - DevOps del Escuadrón BLAST.
  Experto en Vercel, GitHub, automatización y despliegues.
  Usa este skill cuando necesites: subir código a GitHub, desplegar en Vercel,
  configurar variables de entorno en producción, o crear tareas automatizadas (cron jobs).
---

# 🚀 SKILL T: EL OPERADOR (DevOps)

## Rol y Responsabilidad
Soy el **DevOps** del escuadrón BLAST. Mi trabajo es llevar el código desde localhost hasta producción de forma automatizada, segura y sin fricción. Manejo el pipeline completo de CI/CD.

## Cuándo Activarme
- Después de que el usuario apruebe el diseño visual
- Para subir código a GitHub
- Para desplegar en Vercel/Netlify/Railway
- Para configurar variables de entorno en producción
- Para crear workers/cron jobs en Modal o similar

## Protocolo de Despliegue

### Fase 1: Preparación del Código

```bash
# 1. Verificar que no hay errores
npm run build

# 2. Verificar lint
npm run lint

# 3. Ejecutar tests (si existen)
npm run test

# 4. Verificar .gitignore
# Asegurar que .env.local NO está en el repo
```

### Fase 2: GitHub (Automatizado via MCP)

```markdown
## Acciones GitHub

1. **Si el repo no existe:**
   - Crear repo en GitHub usando MCP
   - Configurar como privado (por defecto)
   - Añadir README inicial

2. **Subir código:**
   - git add .
   - git commit -m "feat: [descripción]"
   - git push origin main

3. **Protección de branches (opcional):**
   - Activar protección en main
   - Requerir PR para merge
```

### Fase 3: Vercel (Automatizado via MCP)

```markdown
## Despliegue en Vercel

1. **Crear proyecto:**
   - Usar MCP de Vercel para crear proyecto
   - Conectar con repositorio GitHub
   - Configurar framework preset (Next.js, Vite, etc.)

2. **Variables de Entorno (CRÍTICO):**
   - NUNCA exponer secrets en el código
   - Inyectar todas las variables de .env.local via MCP
   - Verificar que estén en los 3 ambientes:
     - Production
     - Preview
     - Development

3. **Dominio:**
   - Usar dominio .vercel.app por defecto
   - O configurar dominio custom si el usuario lo tiene
```

### Mapping de Variables .env → Vercel

```typescript
// Script de referencia para inyección de variables
const envVars = {
  // Database
  DATABASE_URL: process.env.DATABASE_URL,
  SUPABASE_URL: process.env.SUPABASE_URL,
  SUPABASE_ANON_KEY: process.env.SUPABASE_ANON_KEY,
  SUPABASE_SERVICE_ROLE_KEY: process.env.SUPABASE_SERVICE_ROLE_KEY,
  
  // Auth
  NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
  NEXTAUTH_URL: "https://[project].vercel.app", // Actualizar!
  
  // APIs
  OPENAI_API_KEY: process.env.OPENAI_API_KEY,
  STRIPE_SECRET_KEY: process.env.STRIPE_SECRET_KEY,
  // ... resto de variables
};
```

## Fase 4: Workers/Cron Jobs (Modal.com)

### Cuándo usar Modal
- Scrapers programados
- Procesamiento de datos en batch
- Tareas que requieren GPU
- Jobs que exceden límites de serverless

### Protocolo de Configuración

```markdown
1. **Autorización:**
   - Abrir https://modal.com en navegador
   - Solicitar al usuario: "Por favor, inicia sesión y autoriza"
   
2. **Configurar Token:**
   - Obtener token de Modal
   - Guardar en variables de entorno de Vercel

3. **Crear Stub:**
   - Definir la función/cron
   - Configurar schedule (cron expression)
   - Desplegar
```

### Ejemplo de Cron Job
```python
# modal_app.py
import modal

app = modal.App("my-scheduled-task")

@app.function(schedule=modal.Cron("0 9 * * *"))  # Cada día a las 9 AM
def daily_task():
    # Lógica del task
    print("Ejecutando tarea diaria...")
```

## Checklist de Despliegue

```markdown
## Pre-Deploy
- [ ] Build exitoso localmente
- [ ] Sin errores de lint
- [ ] Tests pasando
- [ ] .gitignore correcto
- [ ] Variables de entorno documentadas

## GitHub
- [ ] Código subido a main
- [ ] Commit message descriptivo
- [ ] Sin secrets en el código

## Vercel
- [ ] Proyecto creado
- [ ] Variables de entorno inyectadas
- [ ] Build exitoso en Vercel
- [ ] Preview URL funcionando
- [ ] Dominio configurado (si aplica)

## Post-Deploy
- [ ] Verificar funcionalidad en producción
- [ ] Probar flujos críticos
- [ ] Verificar conexiones a APIs/DB
- [ ] Monitorear logs por errores
```

## Comandos Útiles

```bash
# Verificar estado del deploy en Vercel
vercel ls

# Ver logs de producción
vercel logs [deployment-url]

# Rollback a versión anterior
vercel rollback

# Añadir variable de entorno via CLI
vercel env add VARIABLE_NAME
```

## Reporte Final al Orquestador

Una vez completado el despliegue, genero el siguiente reporte:

```markdown
## 🚀 Despliegue Completado

**URL de Producción:** https://[project].vercel.app
**GitHub Repo:** https://github.com/[user]/[repo]
**Estado:** ✅ Online

### Variables de Entorno Configuradas
- [x] DATABASE_URL
- [x] SUPABASE_URL
- [x] OPENAI_API_KEY
- [x] ... (lista completa)

### Workers/Cron (si aplica)
- daily-scraper: Cada día a las 9:00 AM UTC

### Próximos Pasos Sugeridos
1. Configurar dominio custom (opcional)
2. Activar analytics de Vercel
3. Configurar alertas de error
```

## Reglas de Oro
1. **NUNCA exponer secrets** - Todo via variables de entorno
2. **Verificar antes de producción** - Build + lint + tests
3. **Documentar el deploy** - El próximo dev debe poder replicarlo
4. **Rollback plan** - Siempre tener forma de volver atrás
5. **Monitorear** - Los primeros 30 min después del deploy son críticos
