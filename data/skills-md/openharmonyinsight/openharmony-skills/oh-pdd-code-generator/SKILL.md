---
name: oh-pdd-code-generator
description: 基于设计文档自动生成鸿蒙系统代码框架，包括 IDL 接口定义、目录结构、头文件、源文件模板、构建配置等。生成前会分析 OpenHarmony 存量代码，学习现有代码风格和架构规范。适用于用户请求：(1) 生成代码框架, (2) 创建 IDL 接口, (3) 生成 BUILD.gn 配置, (4) 创建服务代码, (5) 初始化项目结构, (6) 参考现有代码风格。关键词：code generation, IDL, BUILD.gn, bundle.json, SA profile, OpenHarmony code style, 代码生成, 接口定义, 构建配置, OH代码风格
---

# 代码生成器

基于设计文档自动生成 OpenHarmony 系统代码框架，包括目录结构、IDL 接口、头文件、源文件、构建配置等。

## 快速开始

提供设计文档路径：

```
基于 {功能设计文档} 生成代码框架
```

指定模块名称：

```
为 {模块名} 生成完整代码，基于 {功能设计文档}
```

## OpenHarmony 代码分析

在生成代码前，需要分析 OpenHarmony 存量代码，确保生成的代码符合现有代码风格和架构规范。

### 分析步骤

#### 1. 发现目录结构

使用 Glob 工具发现现有模块的组织结构：

```bash
# 查找相似模块的目录结构
foundation/{subsystem}/*/services/
foundation/{subsystem}/*/interfaces/
foundation/{subsystem}/*/tests/
```

#### 2. 搜索代码模式

使用 Grep 工具搜索代码模式：

| 搜索目标 | 搜索关键字 | 提取信息 |
|----------|------------|----------|
| 类命名 | `class.*Service` | 服务类命名 |
| 命名空间 | `namespace.*` | 命名空间组织 |
| 日志标签 | `HiLogLabel` | 日志使用方式 |
| 错误码 | `ERROR_.*=.*[0-9]` | 错误码分配 |
| 宏定义 | `#define.*_ENABLE` | 条件编译开关 |
| 初始化函数 | `bool Init\(\)` | 初始化模式 |
| 清理函数 | `void.*Release\(\)` | 资源清理模式 |

#### 3. 读取参考实现

使用 Read 工具读取相似模块的实现：

- 服务实现: `*_service.cpp`
- Provider 实现: `*_provider.cpp`
- IDL 定义: `I*.idl`
- 构建配置: `BUILD.gn`

#### 4. 智能探索

使用 Task 工具启动 Explore 代理：

- 查找参考实现的最佳实践
- 提取通用代码模板
- 发现依赖的公共库和工具类

### 参考目录模式

OpenHarmony 标准目录结构：

```
foundation/{subsystem}/{part}/
├── bundle.json              # 部件配置
├── BUILD.gn                  # 主构建文件
├── {part}.gni                # 模块配置
├── services/
│   └── native/
│       ├── {sa_id}.json      # SA 配置
│       ├── include/          # 对外头文件
│       └── src/              # 实现文件
├── interfaces/
│   ├── idl/                  # IDL 接口
│   ├── innerkits/            # 内部 Kit
│   └── kits/                 # 对外 Kit
└── tests/                    # 测试代码
```

### 代码风格参考

| 代码元素 | 风格规则 | 示例 |
|----------|----------|------|
| 类名 | 大驼峰 + 后缀 | `DiskInfoService` |
| 方法名 | 大驼峰 | `GetDiskList()` |
| 成员变量 | 小驼峰 + 下划线后缀 | `mutex_`, `inited_` |
| 命名空间 | 小写双冒号分隔 | `OHOS::DiskManagement` |
| 文件名 | 小写下划线 | `disk_info_service.cpp` |
| 宏定义 | 大写下划线 | `DISK_MANAGEMENT_FORMAT_ENABLE` |

### 常用依赖库

| 依赖 | external_deps 格式 | 用途 |
|------|-------------------|------|
| HiLog | `hilog:libhilog` | 日志输出 |
| c_utils | `c_utils:utils` | C 工具函数 |
| ipc_core | `ipc_core:ipc_core` | IPC 通信 |
| AccessToken | `access_token:libaccesstoken` | 权限管理 |
| HiSysEvent | `hisysevent:libhisysevent` | 事件上报 |
| HiTrace | `hitrace_native:hitrace_meter` | 链路追踪 |

## 生成内容

### 1. 目录结构

自动创建符合 OpenHarmony 规范的目录结构：

```
disk_management/
├── bundle.json              # 部件配置
├── BUILD.gn                  # 主构建配置
├── disk_management.gni       # 模块配置
├── services/
│   ├── native/
│   │   ├── 5001.json         # SA 配置文件
│   │   ├── disk_management.cfg  # Init 配置文件
│   │   ├── include/          # 头文件目录
│   │   └── src/              # 源文件目录
│   └── disk_info_service/    # 各服务目录
│       ├── include/
│       └── src/
├── interfaces/
│   ├── idl/OHOS/DiskManagement/    # IDL 接口定义
│   ├── innerkits/native/           # Native Kit
│   └── kits/js/                    # JS Kit
└── tests/                          # 测试目录
```

### 2. IDL 接口文件

生成 IDL 接口定义文件，格式：

```idl
/* Copyright (c) 2026 Huawei Device Co., Ltd. */

package OHOS.DiskManagement;

import "DiskInfoTypes.idl";

interface IDiskInfoService {
    /// 获取系统所有磁盘列表
    GetDiskList(): DiskInfo[];

    /// 获取指定磁盘的详细信息
    GetDiskInfo([in] string diskId): DiskInfo;

    /// 注册磁盘变化监听器
    RegisterChangeListener([in] IDiskChangeListener listener): void;
};
```

### 3. 头文件模板

生成符合 OpenHarmony 编码规范的头文件：

```cpp
/* Copyright (c) 2026 Huawei Device Co., Ltd. */
#ifndef DISK_INFO_SERVICE_H
#define DISK_INFO_SERVICE_H

#include <string>
#include <vector>
#include <mutex>

namespace OHOS {
namespace DiskManagement {

class DiskInfoService {
public:
    DiskInfoService();
    ~DiskInfoService();

    bool Init();
    void Release();

    std::vector<DiskInfo> GetDiskList();
    DiskInfo GetDiskInfo(const std::string& diskId);

private:
    std::mutex mutex_;
    bool inited_;
};

} // namespace DiskManagement
} // namespace OHOS

#endif // DISK_INFO_SERVICE_H
```

### 4. 源文件模板

生成基础实现框架：

```cpp
/* Copyright (c) 2026 Huawei Device Co., Ltd. */

#include "disk_info_service.h"
#include "hilog/log.h"

namespace OHOS {
namespace DiskManagement {

static constexpr HiLogLabel LABEL = { LOG_CORE, 0xD00430D, "DiskInfoService" };

DiskInfoService::DiskInfoService() : inited_(false)
{
    HiLog::Info(LABEL, "DiskInfoService constructed");
}

DiskInfoService::~DiskInfoService()
{
    Release();
}

bool DiskInfoService::Init()
{
    std::lock_guard<std::mutex> lock(mutex_);
    if (inited_) {
        HiLog::Warn(LABEL, "Already initialized");
        return true;
    }
    // TODO: 初始化逻辑
    inited_ = true;
    return true;
}

void DiskInfoService::Release()
{
    std::lock_guard<std::mutex> lock(mutex_);
    if (!inited_) {
        return;
    }
    // TODO: 清理资源
    inited_ = false;
}

} // namespace DiskManagement
} // namespace OHOS
```

### 5. BUILD.gn 配置

生成构建配置文件：

```gni
import("//build/ohos.gni")
import("//build/test.gni")
import("//foundation/filemanagement/disk_management/disk_management.gni")

ohos_shared_library("disk_management_sa") {
  subsystem_name = "filemanagement"
  part_name = "disk_management"

  sources = [
    "src/disk_management_service.cpp",
    "src/main.cpp",
  ]

  include_dirs = [
    "include",
    "${disk_management_path}/include",
    "//utils/native/base/include",
  ]

  deps = [
    ":disk_management_idl",
    "//foundation/hiviewdfx/hilog/native/framework:libhilog",
  ]

  external_deps = [
    "c_utils:c_utils",
  ]

  branch_protector_ret = "pac_ret"
  sanitize = {
    integer_overflow = true
    cfi = true
    debug = false
  }
}

ohos_unittest("disk_management_unittest") {
  subsystem_name = "filemanagement"
  part_name = "disk_management"
  test_type = "unittest"
  test_time_out = 300

  sources = [
    "test/disk_management_test.cpp",
  ]

  deps = [
    ":disk_management_sa",
  ]

  external_deps = [
    "googletest:gmock_main",
    "googletest:gtest_main",
  ]

  cflags_cc = [ "--coverage" ]
  ldflags = [ "--coverage" ]
}
```

### 6. SA 配置文件 (5001.json)

```json
{
  "sa-id": 5001,
  "sa-name": "disk_management",
  "run-on-create": true,
  "auto-start": true,
  "start-mode": "boot",
  "process": "disk_management_service",
  "dump-level": "control",
  "critical": [1, 4, 240],
  "libpath": "libdisk_management_sa.z.so"
}
```

### 7. bundle.json

```json
{
  "name": "disk_management",
  "description": "HM Desktop Disk Management Service",
  "version": "1.0.0",
  "component": {
    "name": "disk_management",
    "subsystem": "filemanagement",
    "syscap": [
      "SystemCapability.DiskManagement.DiskInfo",
      "SystemCapability.DiskManagement.Format"
    ]
  }
}
```

## 参考文档

- **IDL 编写指南**: [references/idl_guide.md](references/idl_guide.md)
- **BUILD.gn 规范**: [references/build_gn_guide.md](references/build_gn_guide.md)
- **SA 配置规范**: [references/sa_profile_guide.md](references/sa_profile_guide.md)
- **编码规范**: [references/coding_style.md](references/coding_style.md)

## 命名规范映射

| 设计文档术语 | 代码术语 | 规则 |
|--------------|----------|------|
| 服务名称 | 类名 | 大驼峰 + Service 后缀 |
| 模块名称 | 命名空间 | 小写下划线分隔 |
| 接口名称 | IDL 接口 | I + 大驼峰 |
| 数据结构 | struct | 大驼峰 |
| 方法名 | 函数名 | 大驼峰 |
| 成员变量 | 成员变量 | 小驼峰 + 下划线后缀 |

## 模块类型与生成策略

### 信息服务 (InfoService)

生成内容：
- GetList() 方法
- Get() 方法
- RegisterListener() 方法

示例：DiskInfoService

### 管理服务 (ManagerService)

生成内容：
- Execute() 方法
- Cancel() 方法
- RegisterProgressListener() 方法

示例：FormatManagerService, RepairManagerService

### 监听器 (Listener)

生成内容：
- OnChanged() 回调方法
- OnCompleted() 回调方法

示例：DiskChangeListener, FormatProgressListener

## 使用示例

**生成完整代码框架**：
```
基于 {功能设计文档} 为 {模块名} 模块生成完整代码
```

**仅生成 IDL 接口**：
```
只生成 IDL 接口文件，基于 {功能设计文档}
```

**指定 SA ID**：
```
生成代码，SA ID 使用 {SA_ID}，基于 {功能设计文档}
```

**预览模式**：
```
预览将要生成的文件，不实际创建，基于 {功能设计文档}
```

**指定输出目录**：
```
生成代码到 ./code_output 目录，基于 {功能设计文档}
```

## 条件编译支持

生成的代码支持功能条件编译：

```gni
# 在 .gni 文件中定义
declare_args() {
  disk_management_enable_format = true
  disk_management_enable_repair = true
}

# 在 BUILD.gn 中使用
if (disk_management_enable_format) {
  sources += [ "src/format_service.cpp" ]
  defines += [ "DISK_MANAGEMENT_FORMAT_ENABLE" ]
}
```

## 测试代码生成

同时生成单元测试框架：

```cpp
/* Copyright (c) 2026 Huawei Device Co., Ltd. */

#include <gtest/gtest.h>
#include "disk_info_service.h"

namespace OHOS {
namespace DiskManagement {

class DiskInfoServiceTest : public testing::Test {
protected:
    void SetUp() override {
        service_ = std::make_unique<DiskInfoService>();
        ASSERT_TRUE(service_->Init());
    }

    void TearDown() override {
        service_->Release();
    }

    std::unique_ptr<DiskInfoService> service_;
};

TEST_F(DiskInfoServiceTest, GetDiskList) {
    auto disks = service_->GetDiskList();
    EXPECT_GE(disks.size(), 0u);
}

} // namespace DiskManagement
} // namespace OHOS
```

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 设计文档格式错误 | 提示具体缺失章节 |
| IDL 语法错误 | 标记错误行号，提供正确格式 |
| 目录创建失败 | 检查权限，提示用户手动创建 |
| 文件已存在 | 使用 --force 覆盖或跳过 |

## 生成的文件清单

生成完成后，输出文件列表：

```
[INFO] 代码框架生成完成!
[INFO]
[INFO] 生成的文件：
[INFO]   目录: disk_management/
[INFO]   配置: bundle.json, BUILD.gn, disk_management.gni
[INFO]   SA配置: services/native/5001.json, disk_management.cfg
[INFO]   IDL: interfaces/idl/OHOS/DiskManagement/*.idl
[INFO]   头文件: services/native/include/*.h
[INFO]   源文件: services/native/src/*.cpp
[INFO]   测试: test/unittest/*_test.cpp
[INFO]
[INFO] 总计: 15 个文件, 5 个目录
```
