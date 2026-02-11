---
name: saury-revit
description: 基于 Saury.Revit.Template 创建 Revit 插件项目。当用户要求创建 Revit 插件、新建 Revit 项目、初始化 Revit 开发环境、使用 saury-revit 模板时触发。覆盖场景：(1) 创建新 Revit 插件项目 (2) 安装/更新 saury-revit dotnet 模板 (3) 在已创建的项目中添加新功能（Command/View/ViewModel/Service）。关键词：Revit、插件、plugin、saury-revit、dotnet new。
license: MIT
metadata:
  author: hopesy
  version: "1.0.3"
---

# Saury Revit 项目创建器

基于 `Saury.Revit.Template` dotnet 模板，通过交互式流程创建完整配置的 Revit 2026 插件项目（MVVM + DI 架构）。

## 工作流程

按顺序执行以下步骤，每步完成后再进入下一步。

### 第 1 步：交互式确认项目配置

执行任何命令前，必须向用户确认以下信息：

**必问：**
1. **项目名称** — 必须是合法 C# 命名空间名（如 `Acme.WallTools`、`JD.RevitHelper`），默认 `RevitDemo` 或 `RevitTest`。该名称将用于解决方案、项目文件夹、命名空间、程序集、addin 文件、Ribbon 选项卡。
2. **项目创建目录** — 默认当前工作目录。

**可选（有默认值，仅需确认）：**
3. **Revit 版本** — 默认 `2026`，通过 `--RevitVersion` 参数指定。

用户确认后，汇总配置让用户做最终确认再执行。

### 第 2 步：检查并安装 .NET 环境

**检测流程（按顺序执行）：**

1. **检测 dotnet CLI 是否存在**：

```bash
where dotnet
```

2. **若命令存在**，检测 SDK 版本：

```bash
dotnet --list-sdks
```

检查输出中是否包含 `8.0` 或更高版本的 SDK。

3. **判断结果**：
   - dotnet CLI 存在 且 SDK 8.0+ 已安装 → 跳过，进入下一步
   - dotnet CLI 存在 但 无 SDK 或版本不足 → 需要安装 SDK
   - dotnet CLI 不存在 → 需要完整安装

**安装方式（按优先级尝试）：**

```bash
winget install Microsoft.DotNet.SDK.8
```

- 安装完成后重新验证：`where dotnet && dotnet --list-sdks`
- 若 `winget` 不可用，改用官方脚本安装：

```powershell
Invoke-WebRequest -Uri https://dot.net/v1/dotnet-install.ps1 -OutFile dotnet-install.ps1
./dotnet-install.ps1 -Channel 8.0
```

- 若以上方式均失败，告知用户手动下载 [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)

### 第 3 步：安装模板

```bash
# 检查是否已安装
dotnet new list saury-revit
```

- 若已安装 → 跳过，告知用户当前已安装
- 若未安装 → 执行安装：

```bash
dotnet new install Saury.Revit.Template
```

- 若需更新 → `dotnet new install Saury.Revit.Template --force`

### 第 4 步：创建项目

```bash
dotnet new saury-revit -n <项目名称> -o <输出目录>
```

| 参数 | 说明 | 示例 |
|---|---|---|
| `-n` | 项目名称（替换所有 `Saury.Revit.Template`） | `Acme.WallTools` |
| `-o` | 输出目录 | `./Acme.WallTools` |
| `--RevitVersion` | Revit 版本（默认 2026） | `2026` |

**模板自动完成：**
- 全局替换 `Saury.Revit.Template` → 用户项目名
- 自动生成唯一 GUID 替换 `ADDIN-GUID-PLACEHOLDER`
- 排除 `.template.config/`、`bin/`、`obj/`、`.vs/`、`Logs/`、`*.user`

### 第 5 步：验证项目结构

创建后，列出目录确认结构完整：

```
<项目名称>/
├── <项目名称>.slnx
└── <项目名称>/
    ├── Commands/AboutCommand.cs
    ├── Extensions/DataContextExtension.cs
    ├── Models/AboutInfo.cs
    ├── ViewModels/AboutViewModel.cs
    ├── Views/AboutView.xaml(.cs)
    ├── Resources/Icons/about.png
    ├── Resources/Styles/ButtonStyles.xaml
    ├── Services/Interfaces/
    ├── Application.cs
    ├── Host.cs
    ├── appsettings.json
    ├── <项目名称>.addin
    └── <项目名称>.csproj
```

### 第 6 步：构建验证

```bash
cd <输出目录>
dotnet restore
dotnet build --configuration Debug_R26
```

**关键**：本项目使用 `Debug_R26` / `Release_R26`，**禁止**使用标准 `Debug` / `Release`，否则构建失败。

构建成功后，编译产物自动复制到 `C:\ProgramData\Autodesk\Revit\Addins\2026\`。

### 第 7 步：告知用户如何使用

构建成功后，向用户展示以下使用说明：

#### 调试启动配置

1. **修改 Revit 路径** — 打开 `<项目名称>.csproj`，找到 `StartProgram` 属性，确认路径指向本机 Revit 安装位置：

```xml
<StartProgram>C:\Program Files\Autodesk\Revit 2026\Revit.exe</StartProgram>
```

> 若 Revit 安装在非默认路径，需修改为实际路径。

2. **用 Visual Studio 或 Rider 打开** `<项目名称>.slnx`
3. **选择构建配置** `Debug_R26`（工具栏下拉框，**不要选** `Debug`）
4. **点击启动/F5** — 自动编译 → 产物复制到 Addins 目录 → 启动 Revit → 附加调试器
5. **Revit 启动后** — 在 Ribbon 选项卡中找到插件按钮，点击即可触发断点调试

#### 后续定制

1. **厂商信息**（`<项目名称>.addin`）— VendorId、VendorDescription、VendorEmail
2. **关于页信息**（`Models/AboutInfo.cs`）— GiteeUrl、Description
3. **添加新功能** — 参见 [architecture.md](references/architecture.md)

## 添加新功能

当用户要求在已创建的项目中添加新功能时，阅读 [references/architecture.md](references/architecture.md) 获取完整的代码模板和规则约束，严格按照 A→F 六步流程执行：

1. **Model** → `Models/` 目录
2. **ViewModel** → `ViewModels/` 目录（`partial class`，继承 `ObservableObject`）
3. **View** → `Views/` 目录（构造函数注入 ViewModel）
4. **Command** → `Commands/` 目录（`[Transaction(TransactionMode.Manual)]`）
5. **DI 注册** → `Host.cs`（`AddTransient`）
6. **Ribbon 按钮** → `Application.cs` 的 `CreateRibbon` 方法

## 禁止事项

- 禁止使用 `Debug` / `Release` 配置，只能用 `Debug_R26` / `Release_R26`
- 禁止手动 `new` View 或 ViewModel，必须通过 `Host.GetService<T>()` 获取
- 禁止在 View code-behind 中编写业务逻辑
- 禁止在 ViewModel 中直接调用 `MessageBox` 或操作 `Window`
- 禁止硬编码配置值，使用 `appsettings.json` + `IOptions<T>`
- 除非用户明确要求，不要删除示例 About 功能
