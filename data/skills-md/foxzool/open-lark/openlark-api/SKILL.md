---
name: openlark-api
description: OpenLark 项目 API 接口实现规范（速查）。用于添加/重构飞书开放平台 API：确定落盘路径、实现 Body/Response + Builder(Request)、对齐 endpoints 常量/enum、补齐 mod.rs 导出，并明确"调用服务端 API"的方法签名/RequestOption 传递约定。触发关键词：API 接口、API 文件、飞书 API、添加 API、调用服务端 API
allowed-tools: Bash, Read, Grep, Glob, Edit
---

# OpenLark API 接口实现规范（速查）

## 🧭 技能路由指南

**本技能适用场景：**
- 添加/重构单个飞书开放平台 API
- 需要确定 API 落盘路径（bizTag → crate → 文件路径）
- 需要参考代码模板（Body/Response + Builder）
- 需要了解端点规范、RequestOption 约定、Service 链式调用

**其他技能：**
- 审查整体设计规范 → `Skill(openlark-design-review)`
- 统一 `validate()` 写法 → `Skill(openlark-validation-style)`

---

本文件只保留"可执行的最小流程"，标准示例与 docPath 抓取能力见 `references/` 与 `scripts/`。

## 0. 快速工作流（新增一个 API）

1) **定位 API**：在 `./api_list_export.csv` 拿到 `bizTag`、`meta.Project`、`meta.Version`、`meta.Resource`、`meta.Name`
   - 若有 `docPath`，用脚本抓取请求/响应体定义（见 §4）
2) **选 crate**：根据 bizTag 选择 feature crate（见 §1）
3) **定路径**：`crates/{crate}/src/{bizTag}/{project}/{version}/{resource...}/{name}.rs`
4) **写代码**：`Body/Response` + Builder（`execute/send`）+ 端点常量/enum
   - **必须支持 RequestOption**：用于 `user_access_token` / `tenant_key` / 自定义 header
5) **补导出**：在 `mod.rs` 中 `pub mod ...` / `pub use ...`
6) **补链路**：在约定入口补齐链式调用（默认 `service.rs`，但 `openlark-docs` 例外，见 §2）
7) **验证**：`just fmt && just lint && just test`

## 1. Feature Crate ↔ bizTag

仓库以 `tools/api_coverage.toml` 作为 **crate→bizTag** 的唯一来源。

```bash
# 查看所有映射
python3 tools/validate_apis.py --list-crates

# 验证特定 crate 的覆盖率
python3 tools/validate_apis.py --crate openlark-docs
```

**反查技巧**：落盘路径以"目标 crate 现有结构"为准，参考 `references/file-layout.md`

## 2. Service 链式调用（实现 + 调用约定）

> 本节提供"如何实现"的技术规范。若需要审查"是否应该统一范式"（Request 自持 Config vs Builder → Service），见 `Skill(openlark-design-review) §1`。

### 2.1 实现侧：service.rs

目标：让 `openlark-client` 能走 `client.<biz>.service().<project>().<version>()...<api>()`

- 若 crate 已有 `src/service.rs`：在顶层 service 新增 `pub fn {bizTag}(&self) -> ...`
- 若没有：创建 `src/service.rs` 并在 `lib.rs` 中 `pub mod service;`
- `openlark-docs` 特例：为避免 strict API 校验脚本把"链式入口"计为 API 实现文件，链式入口放在 `crates/openlark-docs/src/common/chain.rs`，只做模块级入口与 Config 透传，不为 200+ API 手写方法。

#### ⚠️ Service 层标准模式

**正确示例**（参考 `openlark-docs/src/common/chain.rs`）：

```rust
use std::sync::Arc;
use openlark_core::config::Config;

/// DocClient 只持有 Arc<Config>
#[derive(Debug, Clone)]
pub struct DocClient {
    config: Arc<Config>,
}

impl DocClient {
    pub fn new(config: Config) -> Self {
        Self { config: Arc::new(config) }
    }

    /// 子 Service 只透传 Arc<Config>
    pub fn drive(&self) -> DriveService {
        DriveService::new(self.config.clone())
    }
}

/// Service 层只持有 Arc<Config>，不持有独立 HTTP client
#[derive(Debug, Clone)]
pub struct DriveService {
    config: Arc<Config>,
}

impl DriveService {
    pub fn new(config: Arc<Config>) -> Self {
        Self { config }
    }

    pub fn v1(&self) -> DriveV1 {
        DriveV1::new(self.config.clone())
    }
}
```

**❌ 禁止模式**：
- ❌ Service 持有独立的 HTTP client 字段
- ❌ 使用 `LarkClient` 作为具体类型（它是 trait）
- ❌ 在测试中使用 `.unwrap()` 调用 `Config::build()`（build() 直接返回 Config）

**✅ 正确模式**：
- ✅ Service 只持有 `Arc<Config>`
- ✅ `Config::build()` 直接返回 `Config`，不需要 `.unwrap()`
- ✅ HTTP 传输由 `openlark_core::Transport` 处理

### 2.2 调用侧：RequestOption 约定

**必须提供** `execute_with_options(..., RequestOption)` 或等价签名，并将 option 透传到 `Transport::request(..., Some(option))`

**使用场景**：
- 用户态 API → `user_access_token`
- 商店应用 → `tenant_key` / `app_ticket`
- 链路追踪 → `request_id` / 自定义 header

> ⚠️ 不要只调用 `ApiRequest::request_option(...)`，它仅合并 header，token 推断需要走 Transport

详细示例见 `references/standard-example.md`

## 3. API 模板（以仓库现有风格为准）

> 以下提供两种仓库中真实存在的风格。**实现时优先模仿目标 crate 的现有文件风格**，避免在同一 project/version 内混用多种范式。
>
> 范式一致性审查见 `Skill(openlark-design-review) §1`。

### 3.1 Request / Response

```rust
use openlark_core::{api::ApiRequest, config::Config, http::Transport, SDKResult};
use openlark_core::req_option::RequestOption;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct {Name}Body {
    // 字段按官方文档，用 serde rename 对齐
    // 可选：Option<T> + #[serde(skip_serializing_if = "Option::is_none")]
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct {Name}Response {
    // 字段按官方文档
}
```

### 3.2 Builder + execute/send

```rust
use std::sync::Arc;

pub struct {Name}Request {
    config: Arc<Config>,
    // 路径/查询参数（按需）
}

impl {Name}Request {
    pub fn new(config: Arc<Config>) -> Self { /* ... */ }

    pub async fn execute(self, body: {Name}Body) -> SDKResult<{Name}Response> {
        self.execute_with_options(body, RequestOption::default()).await
    }

    pub async fn execute_with_options(
        self,
        body: {Name}Body,
        option: RequestOption,
    ) -> SDKResult<{Name}Response> {
        // 端点必须复用 crate 的 endpoints 常量或 enum（禁止手写 "/open-apis/..."）
        let req: ApiRequest<{Name}Response> = ApiRequest::post({ENDPOINT_CONST_OR_ENUM});
        let resp = Transport::request(req, &self.config, Some(option)).await?;
        resp.data.ok_or_else(|| openlark_core::error::validation_error("响应数据为空", "服务器没有返回有效的数据"))
    }
}
```

## 4. 提交前检查清单

- [ ] 落盘路径正确（与同模块现有结构一致）
- [ ] Request/Response 字段对齐官方文档（含 `serde(rename)`）
- [ ] HTTP 方法与 `url` 一致；端点使用常量或 enum
- [ ] `mod.rs` 已导出
- [ ] `service.rs` 已提供链式访问
- [ ] 已提供 `execute_with_options(..., RequestOption)` 并透传到 Transport
- [ ] `just fmt && just lint && just test` 通过

## 5. docPath 网页读取

```bash
python3 .claude/skills/openlark-api/scripts/fetch_docpath.py "<docPath>" --format md --out /tmp/doc.md
```

## 6. References

- 目录规范与反查：`references/file-layout.md`
- CSV 映射规则：`references/csv-mapping.md`
- 标准示例（照抄结构）：`references/standard-example.md`
