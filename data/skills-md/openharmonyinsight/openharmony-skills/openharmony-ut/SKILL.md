---
name: openharmony-ut
description: |
  Automate OpenHarmony unit test and fuzz test workflows including
  test generation, compilation, deployment to devices, and execution.
  Use when writing, building, or running UT/FuzzTest for OpenHarmony projects.
allowed-tools: Bash, Read, Edit, Write
---

# OpenHarmony UT 自动化

## 初始化配置

**重要：在执行任何操作前，必须先收集用户配置信息。**

首次使用此 skill 时，请按以下顺序询问用户配置：

### 1. 项目根目录路径
```
请输入 OpenHarmony 项目根目录路径
默认：/root/OpenHarmony
```

### 2. 编译产物路径
```
请输入编译产物输出路径
默认：${项目根目录}/out/rk3568/tests
```

### 3. 编译命令
```
请输入编译命令
模板（使用 ${OH_ROOT} 和 ${TARGET} 变量）
默认：cd ${OH_ROOT} && ./build.sh --product-name=rk3568 --build-target  ${TARGET}
```

### 4. Windows IP 地址
```
请输入 Windows 机器的 IP 地址（用于 hdc 连接）
格式：x.x.x.x
端口固定使用 8710
```

**自动获取选项**：如果当前环境是 WSL，可以先尝试自动获取：
```bash
WIN_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
echo $WIN_IP
```
询问用户是否使用自动获取之后的 IP，或手动输入。

### 5. 连接验证（⚠️ 必须执行）

配置完 IP 后，**必须**依次执行以下验证步骤，确保设备可用：

#### 5.1 验证 IP 地址可达性

```bash
ping -c 3 ${WINDOWS_IP}
```

**判断标准**：
- 成功：收到 3 个 reply，无 100% packet loss
- 失败：请求超时或 unreachable

**失败处理**：
```
❌ 无法 ping 通 ${WINDOWS_IP}
请检查：
1. Windows 机器是否开机
2. 网络连接是否正常
3. IP 地址是否正确
4. Windows 防火墙是否允许 ping（ICMP）
```

#### 5.2 验证 HDC 端口可连接

```bash
nc -zv -w 3 ${WINDOWS_IP} 8710
```

**判断标准**：
- 成功：显示 `succeeded!` 或 `Connection to xxx 8710 port [tcp/*] succeeded!`
- 失败：显示 `timed out` 或 `Connection refused`

**失败处理**：
```
❌ 无法连接到 ${WINDOWS_IP}:8710
请检查：
1. HDC 服务是否在 Windows 上启动
2. 端口 8710 是否被防火墙阻止
3. hdc_std.exe 是否在 Windows 上运行

启动 HDC 服务方法（Windows 管理员权限 PowerShell）：
hdc_std start -l
```

#### 5.3 验证设备列表

```bash
hdc -s ${WINDOWS_IP}:8710 list targets
```

**判断标准**：
- 成功：返回设备序列号，如 `xxxxx`
- 失败：返回 `[Empty]` 或报错

**失败处理**：
```
❌ 未检测到可用设备
请检查：
1. OpenHarmony 设备是否开机
2. 设备是否通过 USB 连接到 Windows 机器
3. hdc_std 是否正确识别设备

手动查看设备（Windows 上执行）：
hdc_std list targets
```

#### 5.4 验证 Shell 连接

```bash
hdc -s ${WINDOWS_IP}:8710 shell "echo 'connection OK'"
```

**判断标准**：
- 成功：返回 `connection OK`
- 失败：显示错误或无响应

**失败处理**：
```
❌ Shell 连接失败
请检查 hdc 版本兼容性
```

### 6. 配置变量说明
收集到的配置将存储为以下变量，后续命令中使用：
1. `OH_ROOT` - 项目根目录
2. `OH_OUTPUT` - 编译产物路径
3. `BUILD_CMD` - 编译命令模板
4. `WINDOWS_IP` - Windows IP，端口固定为 8710

## 快速命令

### 编译测试

```bash
cd ${OH_ROOT}/ && ${BUILD_CMD} <TARGET_NAME>
```

### 部署到设备

```bash
hdc -s ${WINDOWS_IP}:8710 shell "mkdir -p /data/test/"
hdc -s ${WINDOWS_IP}:8710 file send <TARGET_PATH> /data/test
```

### 运行测试

```bash
hdc shell -s ${WINDOWS_IP}:8710 "chmod +x /data/test/<TARGET_NAME> && /data/test/<TARGET_NAME>"
```

## 自动化流程

### 完整流程（编写 + 运行）

当用户请求"编写并运行"或类似明确包含编写意图时，按以下顺序执行：

1. **编写** - 生成测试代码，命名必须与 build target 一致
2. **编译** - 执行构建命令
3. **部署** - 上传到设备 `/data/test/`
4. **运行** - 执行测试并返回结果
5. **修复** - 如失败则修复错误直到通过

### 仅运行流程（⚠️ 优先使用）

**当用户仅说"运行用例"、"跑一下这个用例"等，没有明确提及编写或修改代码时：**

1. **先查找编译产物** - 检查是否已有编译好的文件：

   ```bash
   cd ${OH_OUTPUT}/ && find . -name <TARGET_NAME>
   ```

2. **如果找到** - 直接跳到部署步骤
3. **如果找不到** - 再执行编译，然后继续部署运行

**判断依据：用户请求是否包含"编写"、"写"、"生成"、"创建"等动词**

## 关键规则

1. **命名**: 测试名必须与 BUILD.gn target 一致（如 `LnnNetBuilderFuzzTest`）
2. **位置**: 放在对应模块的 tests 目录下
3. **风格**: 遵循 OpenHarmony HWTEST_F 规范，不使用 GoogleTest main
4. **禁魔数**: 所有常量必须有命名

## 详细文档

1. [environment.md](references/environment.md) - 构建环境架构和路径说明
2. [test-generation.md](references/test-generation.md) - 测试编写规范
3. [build-guide.md](references/build-guide.md) - 编译命令和产物说明
4. [deployment.md](references/deployment.md) - 部署步骤详解
5. [execution.md](references/execution.md) - 测试执行和故障排除
