---
name: engineering-terminology
description: Expert knowledge in engineering, technical, and scientific terminology across English, Japanese, and Chinese (Traditional). Use when translating technical documents, engineering specifications, API documentation, or scientific papers. Provides accurate technical term translations and domain-specific vocabulary.
---

# Engineering Terminology Expertise

## Overview

This skill provides comprehensive engineering and technical terminology knowledge for trilingual translation work (English, Japanese, Chinese Traditional). Use this when working with technical documents, software engineering materials, hardware specifications, or scientific content.

The terminology is organized into domain-specific glossaries with progressive disclosure, allowing you to access detailed terminology only when needed.

## How to Use Glossaries

### Available Glossaries

All glossaries are located in the `glossaries/` subdirectory:

1. **[software-engineering.md](./glossaries/software-engineering.md)** - Core software engineering concepts, design patterns, testing, version control
2. **[web-development.md](./glossaries/web-development.md)** - Frontend/backend frameworks, web technologies, API design
3. **[devops-cloud.md](./glossaries/devops-cloud.md)** - DevOps practices, cloud computing, containerization, infrastructure
4. **[data-engineering.md](./glossaries/data-engineering.md)** - Data processing, databases, analytics, data pipelines
5. **[ai-ml.md](./glossaries/ai-ml.md)** - Artificial intelligence, machine learning, deep learning, LLMs
6. **[hardware-electronics.md](./glossaries/hardware-electronics.md)** - Hardware design, electronics, embedded systems

### Searching Across Glossaries

When translating a technical document:

1. **Identify the domain** - Determine which glossary(ies) are most relevant
2. **Read the glossary** - Use the Read tool to access the specific glossary file
3. **Search for terms** - Use Grep tool if you need to search across multiple glossaries
4. **Maintain consistency** - Create a project-specific term list for recurring translations

Example workflow:

```
User: "Translate this API documentation"
→ Read web-development.md (for REST, GraphQL, endpoint)
→ Read software-engineering.md (for architecture, testing)
```

### Transliteration vs Translation

**Keep English (or transliterate)**:

- Widely adopted acronyms: API, SDK, GUI, REST, JSON, XML
- Product/brand names: React, Docker, Kubernetes, AWS
- Programming languages: Python, JavaScript, TypeScript
- When the English term is standard in the target language

**Translate**:

- Conceptual terms with established translations
- General engineering concepts
- User-facing content and documentation
- When clarity for non-technical users is important

### Regional Variations

**Taiwan vs Hong Kong Chinese**:

- This skill uses Taiwan (台灣) conventions as the default
- Hong Kong (香港) may use different terms, especially for computing
- Examples:
  - Software: 軟體 (TW) vs 軟件 (HK)
  - Network: 網路 (TW) vs 網絡 (HK)
  - Information: 資訊 (TW) vs 信息 (HK)

**Japanese Variations**:

- Technical documents mix kanji, katakana, and English
- Katakana for foreign technical terms (サーバー for "server")
- Formal documents use more kanji, casual content more katakana

## Core Translation Principles

### Principle 1: Consistency

Technical terms should remain consistent throughout a document. Create a terminology glossary for each translation project to ensure uniformity.

### Principle 2: Context Matters

The same English term may have different translations depending on context:

- "Function" in programming → JA: 関数 / ZH-TW: 函式
- "Function" in general usage → JA: 機能 / ZH-TW: 功能
- "Type" in programming → JA: 型 / ZH-TW: 型別
- "Type" as category → JA: タイプ / ZH-TW: 類型

### Principle 3: Audience Awareness

Technical depth varies by audience:

- **Engineers**: Can use more technical jargon, keep English acronyms
- **Technical managers**: Balance technical terms with clarity
- **End users**: Prefer natural language translations, explain acronyms

### Principle 4: Official Standards

For major products and standards, check official localizations:

- Microsoft terminology database
- Apple Human Interface Guidelines (localized)
- Google Developer documentation (localized)
- IEEE, ISO international standards

## Quick Reference: Most Common Terms

| English      | Japanese          | Chinese (Traditional) | Notes                                                 |
| ------------ | ----------------- | --------------------- | ----------------------------------------------------- |
| API          | API, エーピーアイ | API, 應用程式介面     | Keep acronym usually                                  |
| Framework    | フレームワーク    | 框架                  | -                                                     |
| Database     | データベース      | 資料庫                | Often shortened to DB                                 |
| Algorithm    | アルゴリズム      | 演算法                | -                                                     |
| Architecture | アーキテクチャ    | 架構                  | System architecture: システムアーキテクチャ, 系統架構 |
| Backend      | バックエンド      | 後端                  | -                                                     |
| Frontend     | フロントエンド    | 前端                  | -                                                     |
| Deploy       | デプロイ          | 部署                  | Deployment: デプロイメント, 部署作業                  |
| Debug        | デバッグ          | 除錯                  | -                                                     |
| Compile      | コンパイル        | 編譯                  | Compiler: コンパイラ, 編譯器                          |
| Runtime      | ランタイム        | 執行時期              | Runtime environment: 実行環境, 執行環境               |
| Library      | ライブラリ        | 函式庫                | -                                                     |
| Module       | モジュール        | 模組                  | -                                                     |
| Container    | コンテナ          | 容器                  | Docker container, etc.                                |
| Pipeline     | パイプライン      | 流水線                | CI/CD pipeline                                        |
| Repository   | リポジトリ        | 儲存庫                | Code repository                                       |
| Branch       | ブランチ          | 分支                  | Git branch                                            |
| Commit       | コミット          | 提交                  | Git commit                                            |
| Merge        | マージ            | 合併                  | Git merge                                             |
| Cloud        | クラウド          | 雲端                  | Cloud computing: クラウドコンピューティング, 雲端運算 |
| Server       | サーバー          | 伺服器                | -                                                     |
| Client       | クライアント      | 客戶端                | -                                                     |
| Request      | リクエスト        | 請求                  | HTTP request                                          |
| Response     | レスポンス        | 回應                  | HTTP response                                         |
| Query        | クエリ            | 查詢                  | Database query                                        |
| Schema       | スキーマ          | 綱要                  | Database schema                                       |
| Model        | モデル            | 模型                  | Data model, ML model                                  |
| Interface    | インターフェース  | 介面                  | User interface: ユーザーインターフェース, 使用者介面  |
| Component    | コンポーネント    | 元件                  | Software component                                    |
| Service      | サービス          | 服務                  | Microservice, web service                             |

## Best Practices

### 1. Create Project Glossaries

For each translation project, maintain a consistent terminology list. Document decisions about:

- Which acronyms to keep in English
- Which terms to translate vs transliterate
- Domain-specific terminology choices
- Client or project-specific preferences

### 2. Verify Technical Accuracy

Always verify that technical translations maintain the correct meaning:

- Consult domain experts when uncertain
- Test translations with native speakers in the field
- Check that code examples remain executable
- Ensure technical procedures are still accurate

### 3. Handle Code and Technical Elements

When translating documents with code:

- **Keep code unchanged** unless explicitly localizing
- **Keep variable names** in English (standard practice)
- **Translate comments** in code blocks
- **Translate string literals** for user-facing text
- **Keep API endpoints** and technical identifiers unchanged

### 4. Units and Measurements

Be careful with units and measurements:

- Keep SI units (meters, kilograms) as-is
- Note regional differences (e.g., 公尺 vs 米 for meter)
- Convert units only when the target audience expects different units
- Always double-check numerical values and formulas

### 5. Cross-References and Citations

Maintain proper references:

- Keep citation numbers and reference IDs unchanged
- Translate citation text (author names may stay in original)
- Update hyperlinks if localized versions exist
- Maintain bibliography formatting standards

## Quality Checklist

When translating engineering content:

- [ ] Technical terms are accurately translated
- [ ] Terminology is consistent throughout the document
- [ ] Acronyms are handled appropriately (keep or translate)
- [ ] Code samples remain syntactically correct
- [ ] Comments in code are translated
- [ ] Variable names and identifiers are preserved
- [ ] Mathematical formulas and symbols are unchanged
- [ ] Units and measurements are correctly handled
- [ ] Cross-references and citations are properly maintained
- [ ] Hyperlinks are updated to localized versions if available
- [ ] Technical accuracy is verified (ideally by domain expert)
- [ ] Target language feels natural to native speakers
- [ ] Formatting (markdown, LaTeX, etc.) is preserved
- [ ] Images, diagrams, and figures are referenced correctly

## Additional Resources

For terms not found in the glossaries:

1. **Microsoft Language Portal** - Extensive terminology database
2. **Google Developer Documentation** - Check localized versions
3. **IEEE Standards** - For electrical and electronic engineering
4. **ISO Standards** - For international technical standards
5. **Academic Papers** - Check translations in published papers in the field
6. **Product Documentation** - Official translations from major tech companies

## Contributing to Glossaries

When you encounter important terms not in the glossaries, note them for future additions. Prioritize:

- Frequently used terms in your domain
- Terms with ambiguous or multiple translations
- Newly emerging technical concepts
- Terms where regional variations are significant
