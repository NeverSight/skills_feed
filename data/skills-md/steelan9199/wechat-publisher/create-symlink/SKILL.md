---
name: create-symlink
description: 创建软链接（符号链接）支持 Windows、macOS 和 Linux 系统。根据当前操作系统自动选择正确的命令创建目录或文件的软链接。当用户需要创建软链接、符号链接或需要在不同位置共享文件/目录时使用此技能。
---

# 创建软链接 (Create Symlink)

## 指令

当用户需要创建软链接时，首先检测操作系统类型，然后使用对应的命令：

### 1. 检测操作系统

AI 通过以下方式判断当前系统：

1. **查看环境变量中的系统信息**：如 `process.platform`（在 Node.js 环境中）
2. **分析用户提供的路径格式**：
   - Windows 路径：`C:\Users\...` 或 `D:\...`
   - macOS 路径：`/Users/username/...` 或 `~/...`
   - Linux 路径：`/home/username/...` 或 `~/...`
3. **直接询问用户**：当无法确定时，询问用户当前使用的操作系统

**系统标识**：
- Windows: `win32`
- macOS: `darwin`
- Linux: `linux`

### 2. 创建目录软链接

**Windows (PowerShell):**
```powershell
New-Item -ItemType SymbolicLink -Path "目标路径" -Target "源路径"
```

**Windows (CMD):**
```cmd
mklink /D "目标路径" "源路径"
```

**macOS / Linux:**
```bash
ln -s "源路径" "目标路径"
```

### 3. 创建文件软链接

**Windows (PowerShell):**
```powershell
New-Item -ItemType SymbolicLink -Path "目标文件路径" -Target "源文件路径"
```

**Windows (CMD):**
```cmd
mklink "目标文件路径" "源文件路径"
```

**macOS / Linux:**
```bash
ln -s "源文件路径" "目标文件路径"
```

### 4. 创建硬链接（文件）

**Windows (CMD):**
```cmd
mklink /H "目标文件路径" "源文件路径"
```

**macOS / Linux:**
```bash
ln "源文件路径" "目标文件路径"
```

## 使用场景

使用此技能当用户：

- 需要在不同位置共享同一个目录或文件
- 想要创建快捷方式但保持原始路径引用
- 需要跨目录访问文件而不想复制
- 想要统一管理配置文件或资源
- 在开发环境中链接依赖目录
- 需要迁移大文件夹但保持原路径可用

## 注意事项

### 权限要求
- **Windows**: 创建软链接通常需要管理员权限（开发者模式可免除）
- **macOS / Linux**: 普通用户可以创建软链接，但可能需要权限才能链接到某些系统目录

### 路径格式
- **Windows**: 使用完整路径，如 `C:\Users\name\folder` 或 `"C:\Users\name\folder"`
- **macOS / Linux**: 使用完整路径，如 `/home/user/folder` 或 `~/folder`
- 避免使用相对路径，特别是在脚本中

### 目标存在
- 源路径必须存在才能创建软链接
- 目标路径不能已存在（文件或目录）

### 跨文件系统
- 软链接可以跨文件系统创建
- 硬链接不能跨文件系统创建

## 各平台示例

### Windows 示例

#### 创建目录软链接
```powershell
New-Item -ItemType SymbolicLink -Path "D:\shared\tools" -Target "C:\tools"
```

#### 创建文件软链接
```powershell
New-Item -ItemType SymbolicLink -Path "C:\Users\Public\Desktop\config.json" -Target "D:\MyConfigs\main-config.json"
```

### macOS 示例

#### 创建目录软链接
```bash
ln -s /Users/username/Documents/work /Users/username/Desktop/work-link
```

#### 创建文件软链接
```bash
ln -s ~/.config/app/settings.json ~/Desktop/settings-link.json
```

### Linux 示例

#### 创建目录软链接
```bash
ln -s /home/user/projects/myapp /var/www/myapp
```

#### 创建文件软链接
```bash
ln -s /etc/nginx/sites-available/my-site /etc/nginx/sites-enabled/my-site
```

## 验证链接

### Windows
```powershell
# 查看链接详情
Get-ChildItem "链接路径"

# 查看是否为符号链接
(Get-Item "链接路径").Attributes
```

### macOS / Linux
```bash
# 查看链接详情
ls -la "链接路径"

# 验证链接指向
readlink "链接路径"

# 查看链接和源文件
ls -la "链接路径" "源路径"
```

## 删除软链接

### Windows
```powershell
# 删除软链接（不要加 -Recurse，否则会删除源文件）
Remove-Item "链接路径"
```

### macOS / Linux
```bash
# 删除软链接（不要加 -r，否则会删除源文件）
rm "链接路径"

# 或
unlink "链接路径"
```

## 使用指南

### 快速开始

查看 [QUICK-REF.md](QUICK-REF.md) 获取快速参考卡片

### 详细指南

详细的使用说明请参考 [USAGE.md](USAGE.md) 文件，其中包含了：

- 各种触发关键词
- 完整的对话示例
- 常见使用场景
- 注意事项提醒
