---
name: cms-modules
description: |
  CMS NestJS module integration (內容管理系統 NestJS 模組). Use when working with article management (文章管理), category systems (分類系統), approval workflows (審核流程), multi-language content (多語言內容), or GraphQL CMS integration. Covers DataLoader patterns, TypeORM integration, and permission control. Keywords: CMS, 內容管理, 文章管理, 分類, 審核, GraphQL, NestJS, DataLoader, TypeORM, 多語言
---

# CMS NestJS Modules (內容管理系統模組)

## Overview

`@rytass/cms-base-nestjs-module` 系列提供完整的 NestJS CMS 解決方案，支援文章管理、分類系統、審核流程和多語言內容。

### 套件清單

| 套件 | 說明 |
|------|------|
| `@rytass/cms-base-nestjs-module` | 核心 CMS 模組（服務層、實體、DataLoader） |
| `@rytass/cms-base-nestjs-graphql-module` | GraphQL 整合層（Resolvers、Queries、Mutations） |

## Quick Start

### 安裝

```bash
# 核心模組
npm install @rytass/cms-base-nestjs-module

# GraphQL 整合（可選）
npm install @rytass/cms-base-nestjs-graphql-module
```

### 基本設定

```typescript
import { CMSBaseModule } from '@rytass/cms-base-nestjs-module';

@Module({
  imports: [
    TypeOrmModule.forRoot({ /* 資料庫配置 */ }),
    CMSBaseModule.forRoot({
      multipleLanguageMode: true,
      enableDraftMode: true,
      signatureLevels: ['編輯', '主編'],
    }),
  ],
})
export class AppModule {}
```

### GraphQL 整合

```typescript
import { CMSBaseGraphQLModule } from '@rytass/cms-base-nestjs-graphql-module';

@Module({
  imports: [
    GraphQLModule.forRoot({ /* Apollo 配置 */ }),
    CMSBaseGraphQLModule.forRoot({
      multipleLanguageMode: true,
      enableDraftMode: true,
      signatureLevels: ['編輯', '主編'],
    }),
  ],
})
export class AppModule {}
```

## Core Concepts

### 文章生命週期 (Article Stages)

```
DRAFT → REVIEWING → VERIFIED → SCHEDULED/RELEASED
                  ↓
               DELETED
```

| 階段 | 說明 | 觸發操作 |
|------|------|---------|
| `DRAFT` | 草稿 | 建立/退回 |
| `REVIEWING` | 審核中 | submit() |
| `VERIFIED` | 已核准 | approve() |
| `SCHEDULED` | 預約發布 | release(futureDate) |
| `RELEASED` | 已發布 | release() |
| `DELETED` | 已刪除 | archive() |
| `UNKNOWN` | 未知狀態 | 例外狀態 |

### Symbol-Based 注入

```typescript
import {
  RESOLVED_ARTICLE_REPO,
  ArticleBaseService,
} from '@rytass/cms-base-nestjs-module';

@Injectable()
export class ArticleResolver {
  constructor(
    @Inject(RESOLVED_ARTICLE_REPO)
    private readonly articleRepo: Repository<BaseArticleEntity>,

    // ArticleBaseService 直接使用類別注入
    private readonly articleService: ArticleBaseService,
  ) {}
}
```

### DataLoader 模式

防止 N+1 查詢問題：

```typescript
import { ArticleDataLoader } from '@rytass/cms-base-nestjs-module';

@Injectable()
export class ArticleResolver {
  constructor(private readonly articleDataLoader: ArticleDataLoader) {}

  @ResolveField()
  async categories(@Parent() article: Article) {
    return this.articleDataLoader.categoriesLoader.load(article.id);
  }
}
```

**可用的 DataLoaders：**

| DataLoader                   | 提供的 Loaders                               |
|-----------------------------|----------------------------------------------|
| `ArticleDataLoader`          | `stageLoader`, `categoriesLoader`            |
| `ArticleVersionDataLoader`   | `stageVersionsLoader`, `versionsLoader`      |
| `ArticleSignatureDataLoader` | `versionSignaturesLoader`                    |
| `CategoryDataLoader`         | `withParentsLoader`                          |

## Common Patterns

### 自訂實體擴展

```typescript
import { BaseArticleEntity } from '@rytass/cms-base-nestjs-module';

@Entity('articles')
@ChildEntity()
export class CustomArticle extends BaseArticleEntity {
  @Column({ nullable: true })
  featuredImage?: string;

  @Column({ type: 'jsonb', nullable: true })
  seoMetadata?: Record<string, any>;
}

// 模組配置
CMSBaseModule.forRoot({
  articleEntity: CustomArticle,
  articleVersionEntity: CustomArticleVersion,       // 可選
  articleVersionContentEntity: CustomContent,       // 可選
  categoryEntity: CustomCategory,                   // 可選
})
```

### 文章版本管理

```typescript
// 新增版本
await articleService.addVersion(articleId, {
  title: '更新標題',
  content: [...],
  categoryIds: ['cat-1'],
  userId: 'user-1',
  submitted: true,  // 直接提交審核
});

// 刪除特定版本
await articleService.deleteVersion(articleId, 2);

// 封存文章（軟刪除）
await articleService.archive(articleId);
```

### 多語言內容

```typescript
// 建立多語言文章
await articleService.create({
  multiLanguageContents: {
    'zh-TW': { title: '標題', content: '內容' },
    'en-US': { title: 'Title', content: 'Content' },
  },
  categoryIds: ['cat-1'],
});
```

### 審核流程

```typescript
// 1. 提交審核
await articleService.submit(articleId, { userId: 'user-1' });

// 2. 核准
await articleService.approveVersion(
  { id: articleId, version: 1 },
  { signatureLevel: '主編', signerId: 'user-1' },
);

// 3. 發布
await articleService.release(articleId, {
  releasedAt: new Date(),
  version: 1,  // 可選，指定版本
  userId: 'user-1',
});

// 4. 退回（重新編輯）
await articleService.putBack(articleId);

// 5. 拒絕審核
await articleService.rejectVersion(
  { id: articleId },
  { signatureLevel: '主編', signerId: 'user-1', reason: '內容不完整' },
);

// 6. 撤回已發布文章
await articleService.withdraw(articleId, 1);  // id, version
```

### GraphQL 查詢範例

```graphql
# 公開文章列表
query Articles($page: Int, $limit: Int) {
  articles(page: $page, limit: $limit) {
    items {
      articleId
      title
      categories { id, name }
      releasedBy { username }
    }
    meta { totalCount, hasNextPage }
  }
}

# 後台文章（含所有階段）
query BackstageArticles($stage: ArticleStage) {
  backstageArticles(stage: $stage) {
    items {
      articleId
      stage
      signatures { approved, level }
    }
  }
}
```

### 權限控制整合

> **注意：** `BaseResource` 和 `BaseAction` 枚舉定義在 `@rytass/cms-base-nestjs-graphql-module` 的 `src/constants/enum/` 目錄下，但目前未從 index.ts 導出。如需使用，請直接引用字串或在專案中自行定義。

```typescript
import { AllowActions } from '@rytass/member-base-nestjs-module';

@Mutation()
@AllowActions([['article', 'create']])  // 使用字串代替枚舉
async createArticle() { }
```

## Module Options

| 選項 | 預設 | 說明 |
|------|------|------|
| `multipleLanguageMode` | false | 啟用多語言內容 |
| `allowMultipleParentCategories` | false | 分類允許多個父分類 |
| `allowCircularCategories` | false | 分類允許循環參照 |
| `fullTextSearchMode` | false | 啟用全文搜尋 |
| `enableDraftMode` | false | 啟用草稿模式 |
| `signatureLevels` | [] | 審核層級定義 |
| `autoReleaseWhenLatestSignatureApproved` | false | 最終核准後自動發布 |
| `articleEntity` | BaseArticleEntity | 自訂文章實體類別 |
| `articleVersionEntity` | BaseArticleVersionEntity | 自訂文章版本實體類別 |
| `articleVersionContentEntity` | BaseArticleVersionContentEntity | 自訂文章內容實體類別 |
| `categoryEntity` | BaseCategoryEntity | 自訂分類實體類別 |
| `categoryMultiLanguageNameEntity` | BaseCategoryMultiLanguageNameEntity | 自訂多語言分類名稱實體類別 |
| `signatureLevelEntity` | BaseSignatureLevelEntity | 自訂審核層級實體類別 |

## Additional Types

### Enums

```typescript
// 文章階段
enum ArticleStage {
  DRAFT = 'DRAFT',
  REVIEWING = 'REVIEWING',
  VERIFIED = 'VERIFIED',
  SCHEDULED = 'SCHEDULED',
  RELEASED = 'RELEASED',
  DELETED = 'DELETED',
  UNKNOWN = 'UNKNOWN',
}

// 文章排序
enum ArticleSorter {
  CREATED_AT_DESC = 'CREATED_AT_DESC',
  CREATED_AT_ASC = 'CREATED_AT_ASC',
  UPDATED_AT_DESC = 'UPDATED_AT_DESC',
  UPDATED_AT_ASC = 'UPDATED_AT_ASC',
  SUBMITTED_AT_DESC = 'SUBMITTED_AT_DESC',
  SUBMITTED_AT_ASC = 'SUBMITTED_AT_ASC',
  RELEASED_AT_DESC = 'RELEASED_AT_DESC',
  RELEASED_AT_ASC = 'RELEASED_AT_ASC',
}

// 文章搜尋模式
enum ArticleSearchMode {
  FULL_TEXT = 'full_text',
  TITLE = 'title',
  TITLE_AND_TAG = 'title-and-tag',
}

// 審核結果
enum ArticleSignatureResult {
  APPROVED = 'APPROVED',
  REJECTED = 'REJECTED',
}
```

### Error Classes

```typescript
// 基礎錯誤
class MultipleLanguageModeIsDisabledError extends Error {}

// 文章相關錯誤
class ArticleNotFoundError extends Error {}
class ArticleVersionNotFoundError extends Error {}

// 分類相關錯誤
class CategoryNotFoundError extends Error {}
class CircularCategoryNotAllowedError extends Error {}
class MultipleParentCategoryNotAllowedError extends Error {}
class ParentCategoryNotFoundError extends Error {}
```

### Symbol Tokens

**Repository Tokens（可用於依賴注入）：**
- `RESOLVED_ARTICLE_REPO`
- `RESOLVED_ARTICLE_VERSION_REPO`
- `RESOLVED_ARTICLE_VERSION_CONTENT_REPO`
- `RESOLVED_CATEGORY_REPO`
- `RESOLVED_CATEGORY_MULTI_LANGUAGE_NAME_REPO`
- `RESOLVED_SIGNATURE_LEVEL_REPO`

**Mode Tokens（模組配置狀態）：**
- `MULTIPLE_LANGUAGE_MODE`
- `DRAFT_MODE`
- `MULTIPLE_CATEGORY_PARENT_MODE`
- `CIRCULAR_CATEGORY_MODE`
- `FULL_TEXT_SEARCH_MODE`
- `SIGNATURE_LEVELS`
- `AUTO_RELEASE_AFTER_APPROVED`

## API Reference

詳細 API 文件請參閱 [reference.md](reference.md)。

## Troubleshooting

### 循環依賴錯誤

使用 Symbol Token 注入而非直接類別注入：
```typescript
// 正確
@Inject(RESOLVED_ARTICLE_REPO) repo: Repository<Article>

// 避免
constructor(private readonly repo: ArticleRepository)
```

### DataLoader 快取問題

ArticleDataLoader 提供的 loaders：
- `stageLoader` - 帶 LRU 快取
- `categoriesLoader` - 帶 LRU 快取

如需無快取版本，請在自訂 DataLoader 時設定：
```typescript
// DataLoader 本身支援 cache: false 選項
const uncachedLoader = new DataLoader(
  (keys) => this.batchLoad(keys),
  { cache: false }
);
```

### 多語言模式未啟用

確認模組配置 `multipleLanguageMode: true`，否則只能存取第一個語言內容。
