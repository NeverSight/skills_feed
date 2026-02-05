---
name: nextjs-16-specialist
description: This skill should be used when developing Next.js 16 applications with React, TypeScript, Material-UI V7, and Firebase. Provides comprehensive guidance on setup, best practices, error handling, and advanced patterns for production-ready applications.
---

# Next.js 16 Specialist

## Overview

Este skill transforma você em um especialista em **Next.js 16 com React 19.2, TypeScript, Material-UI V7 e Firebase**. Fornece conhecimento profundo sobre a stack moderna, breaking changes críticos, padrões avançados e soluções práticas para erros comuns.

## Quando Usar Este Skill

Use este skill quando:

- Criar **novo projeto Next.js 16** com stack completa (React + TypeScript + MUI + Firebase)
- Migrar de **Next.js 15 para 16** (breaking changes obrigatórios)
- Implementar **autenticação com Firebase** em aplicações Next.js
- Trabalhar com **Material-UI V7** integrado ao Next.js App Router
- Resolver erros específicos de **async/await, Firebase, MUI ou caching**
- Otimizar performance com **Turbopack, Cache Components e File System Caching**
- Implementar **TypedRoutes** para type safety em navegação
- Usar **Next.js DevTools MCP** para debugging assistido por IA
- Otimizar **routing e navigation** com Layout Deduplication
- Implementar **View Transitions** e **useEffectEvent** do React 19.2
- Implementar **padrões avançados** como Error Boundaries e Protected Routes

## Stack Completo

| Componente | Versão | Propósito |
|-----------|--------|----------|
| **Next.js** | 16+ | Framework full-stack com Server Components |
| **React** | 19.2+ | UI library com React Compiler |
| **TypeScript** | 5.1+ | Type safety completo |
| **Material-UI** | V7 | Component library profissional |
| **Firebase** | Latest | Auth, Firestore, Storage |
| **Turbopack** | Stable | Bundler padrão (2-5x mais rápido) |

## Estrutura do Conhecimento

Este skill está organizado em 4 áreas principais:

### 1. Setup & Quickstart
- Criação de projeto do zero
- Instalação e configuração de dependências
- Primeiros passos com Firebase
- Checklist pré-produção

### 2. Breaking Changes Críticos
- APIs assíncronas obrigatórias (`params`, `searchParams`)
- Mudança de `middleware.ts` → `proxy.ts`
- Novos defaults de imagem
- Migrações de Route Segment Configs

### 3. Recursos Referenciais
Este skill inclui arquivos de referência detalhada que devem ser consultados conforme necessário:

- `setup-guide-detailed.md` - Setup completo passo-a-passo
- `breaking-changes-reference.md` - Todas as mudanças do Next.js 16
- `common-errors-solutions.md` - 40+ erros e soluções
- `advanced-patterns.md` - Padrões profissionais (Auth, Upload, Testing)

Use a seção **References** deste skill para localizar informações específicas.

### 4. Padrões Avançados
- Autenticação com persistência de sessão
- Error Boundaries com Material-UI
- Validação com Zod
- Upload de arquivos com Storage
- Testes com Vitest e Testing Library
- Deployment em Vercel/Firebase Hosting

## Como Usar Este Skill

### Para um Novo Projeto

1. **Consulte**: `setup-guide-detailed.md` → Seção "Criando o Projeto do Zero"
2. **Execute**: Comandos de criação do projeto com `create-next-app`
3. **Configure**: Firebase, Material-UI seguindo os passos
4. **Valide**: Checklist pré-produção em `setup-guide-detailed.md`

### Para Migrar do Next.js 15

1. **Leia**: `breaking-changes-reference.md` - Seção "Guia de Atualização"
2. **Execute**: Codemod automático: `npx @next/codemod@canary upgrade latest`
3. **Verifique**: Todos os `params`/`searchParams` agora precisam de `await`
4. **Teste**: Seu código TypeScript com `npx tsc --noEmit`

### Para Resolver Erros

1. **Procure**: O erro em `common-errors-solutions.md`
2. **Estude**: Seção "❌ Sintoma" para identificar causa
3. **Aplique**: Solução em "✅ CORRETO"
4. **Teste**: Mudanças localmente antes de commit

### Para Implementar Recursos Avançados

1. **Procure**: O padrão em `advanced-patterns.md`
2. **Copie**: Código de exemplo (Auth Context, Error Boundary, etc.)
3. **Adapte**: Para seu projeto específico
4. **Teste**: Especialmente autenticação com ProtectedRoute

## Dicas Rápidas

### ⚡ Turbopack (Default + File System Cache)
```bash
npm run dev  # Usa Turbopack automaticamente
npm run build  # 2-5x mais rápido que Webpack

# Habilitar File System Caching (Beta)
# next.config.ts
experimental: { turbopackFileSystemCacheForDev: true }
# Restarts 3-5x mais rápidos! ✅
```

### 📦 Cache Components (refresh, updateTag, revalidateTag)
```typescript
'use cache';  # Marcar componente como cacheado
cacheTag('products');  # Identificar cache
revalidateTag('products', 'max');  # Invalidar com SWR
updateTag('products');  # Read-your-writes (imediato)
refresh();  # Atualizar dados não-cacheados apenas
```

### 🚀 Enhanced Routing (Automático)
```typescript
# Layout Deduplication - Zero config
# Layouts compartilhados baixados 1x só
# Economia: 50-80% de prefetch size ✅

# Incremental Prefetching
# Só prefetcha o que NÃO está em cache
# Viewport-aware: cancela quando sai da tela
```

### 🔐 Firebase + Auth (Seguro)
```typescript
const app = getApps().length === 0 ? initializeApp(config) : getApps()[0];
# ✅ Nunca reinicializa Firebase
```

### ⌛ Params Agora são Async (Obrigatório!)
```typescript
# ❌ ERRADO - Não compila no Next.js 16
export default function Page({ params }) { }

# ✅ CORRETO - OBRIGATÓRIO
export default async function Page({ params }) {
  const { slug } = await params;
}
```

### 🔗 TypedRoutes (Type Safety para Links)
```typescript
# Habilitar em next.config.ts
const nextConfig: NextConfig = {
  typedRoutes: true,  // ✅ Detecta links inválidos no build
};

# Uso
<Link href="/about" />  // ✅ Validado
<Link href="/aboot" />  // ❌ Type error detectado
router.push(`/blog/${slug}`);  // ✅ Template literals validados
```

### 🤖 Next.js DevTools MCP (IA Integrada)
```json
// .mcp.json na raiz do projeto
{
  "mcpServers": {
    "next-devtools": {
      "command": "npx",
      "args": ["-y", "next-devtools-mcp@latest"]
    }
  }
}

# Claude Code agora vê:
# - Erros em tempo real
# - Estrutura do projeto
# - Logs do dev server
# - Metadados de páginas
```

### ✨ React 19.2 (View Transitions + useEffectEvent)
```typescript
# View Transitions (animações suaves)
<ViewTransition name="product-1">
  <ProductCard />
</ViewTransition>

# useEffectEvent (lógica não-reativa)
const logView = useEffectEvent(() => {
  analytics.track('view', { userId }); // Sempre atualizado
});
useEffect(() => logView(), [productId]); // Só re-executa com productId
```

### 🎨 Material-UI V7 (Sempre AppRouterCacheProvider)
```typescript
<AppRouterCacheProvider>  {# OBRIGATÓRIO primeiro #}
  <ThemeProvider theme={theme}>
    {children}
  </ThemeProvider>
</AppRouterCacheProvider>
```

## Tecnologias & Versões

- **Node.js**: 20.9.0+ (18 não é mais suportado)
- **npm**: 9.x+ recomendado
- **TypeScript**: 5.1.0+ (aumentado de 4.9)
- **React**: 19.2+ (com React Compiler estável)
- **Next.js**: 16.0.0+
- **Material-UI**: 7.x

## Checklist de Início

- [ ] Node.js 20.9+ instalado
- [ ] Ler `breaking-changes-reference.md` se migrando de Next.js 15
- [ ] Seguir `setup-guide-detailed.md` para novo projeto
- [ ] Configurar `.env.local` com variáveis Firebase
- [ ] Testar autenticação localmente
- [ ] Verificar `common-errors-solutions.md` ao encontrar erros
- [ ] Ativar `strict: true` em `tsconfig.json`
- [ ] Rodar `npx next typegen` para tipos automáticos

## Próximos Passos

### 📚 Guias Essenciais
1. **Para novo projeto**: Veja `references/setup-guide-detailed.md`
2. **Para migração**: Veja `references/breaking-changes-reference.md`
3. **Para erros**: Veja `references/common-errors-solutions.md`
4. **Para avançado**: Veja `references/advanced-patterns.md`

### 🚀 Features do Next.js 16
5. **Cache Components (use cache, refresh, updateTag)**: Veja `features/cache-components-deep-dive.md`
6. **Turbopack + File System Caching**: Veja `features/turbopack-masterclass.md`
7. **Enhanced Routing & Navigation**: Veja `features/enhanced-routing-navigation.md` (NOVO!)
8. **TypedRoutes (Type Safety)**: Veja `features/typed-routes-complete-guide.md` (NOVO!)
9. **Next.js DevTools MCP (IA Integration)**: Veja `features/nextjs-devtools-mcp-guide.md` (NOVO!)

### ⚛️ React 19.2 Features
10. **View Transitions, useEffectEvent, Activity**: Veja `features/react-19-2-new-features.md`

---

**Última Atualização**: Novembro 2025 (Next.js 16.0.0 - Cobertura 100% Completa)
**Compatibilidade**: Next.js 16+ com React 19.2+
**Status**: Estável para produção

## 🎉 Novidades Recentes (Novembro 2025)

- ✅ **TypedRoutes Guide** - Type safety completo para navegação
- ✅ **Next.js DevTools MCP** - Debugging assistido por IA com Claude Code
- ✅ **Enhanced Routing & Navigation** - Layout Deduplication + Incremental Prefetching
- ✅ **refresh() API** - Nova API de cache para dados não-cacheados
- ✅ **View Transitions** - Animações declarativas do React 19.2
- ✅ **useEffectEvent** - Hook para lógica não-reativa em Effects
- ✅ **Turbopack File System Caching** - Restarts 3-5x mais rápidos

**Total**: 3 novos guias + 4 guias atualizados + cobertura 100% do Next.js 16! 🚀
