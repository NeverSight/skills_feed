---
name: quadrats-module
description: |
  Quadrats CMS NestJS module (Quadrats 富文本 CMS NestJS 模組). Use when working with rich text content management, article versioning (文章版本控制), multi-language content (多語言內容), category management (分類管理), or image uploads (圖片上傳). Covers QuadratsArticleService, CategoryService, TagService, ImageService. Keywords: Quadrats, CMS, 富文本, 文章管理, 多語言, NestJS, rich text, article, versioning
---

# Quadrats CMS NestJS Module (Quadrats 富文本 CMS 模組)

## Overview

`@rytass/quadrats-nestjs` 提供 Quadrats CMS 的 NestJS 整合模組，支援富文本內容管理、文章版本控制、多語言內容和圖片上傳。

## Quick Start

### 安裝

```bash
npm install @rytass/quadrats-nestjs @quadrats/core
```

### 基本設定

```typescript
import { QuadratsModule } from '@rytass/quadrats-nestjs';

@Module({
  imports: [
    QuadratsModule.forRoot({
      accessKey: 'your-access-key',
      secret: 'your-secret',
      // host: 'https://api.quadrats.io',  // 預設值
    }),
  ],
})
export class AppModule {}
```

### 非同步設定

```typescript
import { QuadratsModule } from '@rytass/quadrats-nestjs';
import { ConfigService } from '@nestjs/config';

@Module({
  imports: [
    QuadratsModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        accessKey: config.get('QUADRATS_ACCESS_KEY'),
        secret: config.get('QUADRATS_SECRET'),
      }),
    }),
  ],
})
export class AppModule {}
```

## Services

### QuadratsArticleService

文章 CRUD 與版本管理：

```typescript
import { QuadratsArticleService, Language } from '@rytass/quadrats-nestjs';
import { Paragraph } from '@quadrats/core';

@Injectable()
export class ContentService {
  constructor(private readonly articleService: QuadratsArticleService) {}

  // 建立文章
  async createArticle() {
    return this.articleService.create({
      title: '文章標題',
      categoryIds: ['category-id'],
      tags: ['tag1', 'tag2'],
      contents: [
        Paragraph.create({ children: [{ text: '文章內容' }] }),
      ],
      language: Language.ZH_TW,
      releasedAt: new Date(),
    });
  }

  // 多語言文章
  async createMultiLangArticle() {
    return this.articleService.create({
      title: '多語言文章',
      categoryIds: ['category-id'],
      tags: ['multilang'],
      languageContents: [
        {
          language: Language.ZH_TW,
          elements: [Paragraph.create({ children: [{ text: '繁體中文內容' }] })],
        },
        {
          language: Language.EN,
          elements: [Paragraph.create({ children: [{ text: 'English content' }] })],
        },
      ],
    });
  }

  // 取得文章
  async getArticle(id: string, versionId?: string) {
    return this.articleService.get(id, versionId);
  }

  // 取得文章 ID 列表
  async getArticleIds() {
    return this.articleService.getIds({
      limit: 10,
      offset: 0,
      categoryIds: ['category-id'],
      tags: ['featured'],
    });
  }

  // 新增版本
  async addVersion(id: string) {
    return this.articleService.addVersion({
      id,
      title: '更新標題',
      categoryIds: ['category-id'],
      tags: ['updated'],
      contents: [
        Paragraph.create({ children: [{ text: '新版本內容' }] }),
      ],
    });
  }

  // 刪除文章
  async removeArticle(id: string) {
    return this.articleService.remove(id);
  }
}
```

### QuadratsArticleCategoryService

分類管理：

```typescript
import { QuadratsArticleCategoryService } from '@rytass/quadrats-nestjs';

@Injectable()
export class CategoryManagementService {
  constructor(private readonly categoryService: QuadratsArticleCategoryService) {}

  // 取得所有分類
  async getAllCategories() {
    return this.categoryService.getAll();
  }

  // 取得單一分類
  async getCategory(id: string) {
    return this.categoryService.get(id);
  }

  // 建立分類
  async createCategory(name: string, parentId?: string) {
    return this.categoryService.create(name, parentId);
  }

  // 重新命名分類
  async renameCategory(id: string, newName: string) {
    return this.categoryService.rename(id, newName);
  }
}
```

### QuadratsArticleTagService

標籤查詢：

```typescript
import { QuadratsArticleTagService } from '@rytass/quadrats-nestjs';

@Injectable()
export class TagService {
  constructor(private readonly tagService: QuadratsArticleTagService) {}

  // 取得所有標籤
  async getAllTags() {
    return this.tagService.getAll({
      limit: 50,
      offset: 0,
      searchTerm: 'tech',  // 可選搜尋詞
    });
  }
}
```

### QuadratsArticleImageService

圖片上傳：

```typescript
import { QuadratsArticleImageService, ImageDetailURL } from '@rytass/quadrats-nestjs';
import { Readable } from 'stream';

@Injectable()
export class ImageUploadService {
  constructor(private readonly imageService: QuadratsArticleImageService) {}

  // 上傳圖片 (urlMode = false 或省略，回傳詳細 URL 資訊)
  async uploadImageWithDetails(buffer: Buffer): Promise<ImageDetailURL> {
    return this.imageService.uploadImage(buffer, false);
    // 回傳: ImageDetailURL { id, preload, thumbnails, public, full }
  }

  // 上傳圖片 (不帶 urlMode 時預設為 false，回傳詳細 URL 資訊)
  async uploadImageDefault(buffer: Buffer): Promise<ImageDetailURL> {
    return this.imageService.uploadImage(buffer);
    // 回傳: ImageDetailURL { id, preload, thumbnails, public, full }
  }

  // 上傳圖片 (urlMode = true，回傳簡單 URL 字串)
  async uploadImageUrl(buffer: Buffer): Promise<string> {
    return this.imageService.uploadImage(buffer, true);
    // 回傳: string (URL)
  }

  // 支援 Stream 上傳
  async uploadFromStream(stream: Readable): Promise<ImageDetailURL> {
    return this.imageService.uploadImage(stream);
  }
}

### ImageDetailURL

```typescript
interface ImageDetailURL {
  id: string;         // 檔案 ID
  preload: string;    // 模糊預載 URL
  thumbnails: string; // 小尺寸 URL
  public: string;     // 標準尺寸 URL
  full: string;       // 大尺寸 URL
}
```

## Language Enum

支援的語言（含別名）：

```typescript
import { Language } from '@rytass/quadrats-nestjs';

enum Language {
  DEFAULT = 'DEFAULT',
  ZH = 'TRADITIONAL_CHINESE',       // 繁體中文（別名）
  ZH_TW = 'TRADITIONAL_CHINESE',    // 繁體中文
  ZH_CN = 'SIMPLIFIED_CHINESE',     // 簡體中文
  EN_US = 'ENGLISH_UNITED_STATES',  // 美式英文（別名）
  EN = 'ENGLISH_UNITED_STATES',     // 美式英文
  EN_GB = 'ENGLISH_UNITED_KINGDOM', // 英式英文
  JA_JP = 'JAPANESE',               // 日文
  JP = 'JAPANESE',                  // 日文（別名）
  KO_KR = 'KOREAN',                 // 韓文
  KR = 'KOREAN',                    // 韓文（別名）
  ES = 'SPANISH_SPAIN',             // 西班牙文
  PT = 'PORTUGUESE_PORTUGAL',       // 葡萄牙文
  DE = 'GERMANY_GERMAN',            // 德文
  IT = 'ITALIAN_ITALY',             // 義大利文
  FR = 'FRENCH_FRANCE',             // 法文
}
```

> **提示:** `ZH`/`ZH_TW`、`EN`/`EN_US`、`JP`/`JA_JP`、`KR`/`KO_KR` 為相同值的別名，可依習慣選用。

## Data Types

### QuadratsArticle

```typescript
interface QuadratsArticle {
  id: string;
  versionId: string;
  title: string;
  categories: QuadratsArticleCategory[];
  tags: string[];
  releasedAt: Date | null;
  contents: QuadratsArticleContentItem[];
}
```

### QuadratsArticleCategory

```typescript
interface QuadratsArticleCategory {
  id: string;
  name: string;
}
```

### QuadratsArticleContentItem

```typescript
import type { QuadratsElement } from '@quadrats/core';

interface QuadratsArticleContentItem {
  language: string;
  elements: QuadratsElement[];
}
```

## Complete Example

```typescript
import { Module, Injectable } from '@nestjs/common';
import {
  QuadratsModule,
  QuadratsArticleService,
  QuadratsArticleCategoryService,
  QuadratsArticleImageService,
  Language,
} from '@rytass/quadrats-nestjs';
import { Paragraph, createEditor } from '@quadrats/core';

// Module 設定
@Module({
  imports: [
    QuadratsModule.forRoot({
      accessKey: process.env.QUADRATS_ACCESS_KEY!,
      secret: process.env.QUADRATS_SECRET!,
    }),
  ],
  providers: [BlogService],
})
export class BlogModule {}

// 部落格服務
@Injectable()
export class BlogService {
  constructor(
    private readonly articleService: QuadratsArticleService,
    private readonly categoryService: QuadratsArticleCategoryService,
    private readonly imageService: QuadratsArticleImageService,
  ) {}

  // 發佈文章（含圖片）
  async publishPost(data: {
    title: string;
    content: string;
    categoryId: string;
    tags: string[];
    coverImage?: Buffer;
  }) {
    // 上傳封面圖（不帶 urlMode 或 urlMode=false 時回傳 ImageDetailURL）
    let coverUrl: string | undefined;
    if (data.coverImage) {
      const imageResult = await this.imageService.uploadImage(data.coverImage);
      coverUrl = imageResult.public;
    }

    // 建立文章內容
    const elements = [
      Paragraph.create({ children: [{ text: data.content }] }),
    ];

    // 建立文章
    return this.articleService.create({
      title: data.title,
      categoryIds: [data.categoryId],
      tags: data.tags,
      contents: elements,
      language: Language.ZH_TW,
      releasedAt: new Date(),
    });
  }

  // 取得文章列表
  async getPosts(categoryId?: string, page = 1, pageSize = 10) {
    const ids = await this.articleService.getIds({
      categoryIds: categoryId ? [categoryId] : undefined,
      limit: pageSize,
      offset: (page - 1) * pageSize,
    });

    return Promise.all(ids.map(id => this.articleService.get(id)));
  }

  // 更新文章（建立新版本）
  async updatePost(id: string, updates: { title: string; content: string }) {
    return this.articleService.addVersion({
      id,
      title: updates.title,
      categoryIds: [],
      tags: [],
      contents: [
        Paragraph.create({ children: [{ text: updates.content }] }),
      ],
    });
  }

  // 分類管理
  async setupCategories() {
    const tech = await this.categoryService.create('技術');
    const frontend = await this.categoryService.create('前端', tech.id);
    const backend = await this.categoryService.create('後端', tech.id);

    return { tech, frontend, backend };
  }
}
```

## Configuration Options

```typescript
interface QuadratsModuleOptions {
  accessKey: string;   // Quadrats API Access Key
  secret: string;      // Quadrats API Secret
  host?: string;       // API Host (預設: https://api.quadrats.io)
}

interface QuadratsModuleAsyncOptions extends Pick<ModuleMetadata, 'imports'> {
  name?: string;
  useFactory: (...args: any[]) => Promise<QuadratsModuleOptions> | QuadratsModuleOptions;
  inject?: (InjectionToken | OptionalFactoryDependency)[];
}
```

## Dependencies

**Required:**
- `@quadrats/core` ^1.1.5 (富文本元素定義)

**Peer Dependencies:**
- `@nestjs/common` ^9.4.2

## Troubleshooting

### 文章建立失敗

確保 `contents` 或 `languageContents` 其中之一有設定：

```typescript
// 正確: 使用 contents
await articleService.create({
  title: '標題',
  categoryIds: [],
  tags: [],
  contents: [Paragraph.create({ children: [{ text: '內容' }] })],
});

// 正確: 使用 languageContents
await articleService.create({
  title: '標題',
  categoryIds: [],
  tags: [],
  languageContents: [
    { language: Language.ZH_TW, elements: [...] },
  ],
});

// 錯誤: 兩者都沒設定
await articleService.create({
  title: '標題',
  categoryIds: [],
  tags: [],
  // 會拋出錯誤: `contents` or `languageContents` should be set
});
```

### 圖片上傳失敗

確認圖片格式和大小符合要求，並使用正確的 Buffer 或 Stream：

```typescript
import * as fs from 'fs';

// 從檔案讀取
const buffer = fs.readFileSync('image.jpg');
await imageService.uploadImage(buffer);

// 從 Stream 讀取
const stream = fs.createReadStream('image.jpg');
await imageService.uploadImage(stream);
```
