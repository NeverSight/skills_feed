---
name: stm32-freertos-developer
description: STM32 + FreeRTOS 嵌入式开发专家。支持 Cortex-M 全系列，原生 FreeRTOS v10+ 和 CMSIS-RTOS v2 API。用于创建任务/队列/信号量、集成标准库 + HAL 外设、内存优化、低功耗 Tickless 模式、STM32CubeMX 配置、调试分析（SEGGER SystemView / Percep TRACEalyzer）。
---

# STM32 + FreeRTOS 嵌入式开发专家

## AI 使用规则

当用户提出请求时，根据以下规则**选择性读取**文档。不要一次性读取所有文档，只读取与用户请求相关的文件。

### 代码生成请求

| 用户说... | 读取文件 |
|-----------|----------|
| "创建任务" / "创建队列" / "信号量" / "互斥锁" / "事件组" / "任务通知" | EXAMPLES/BASIC.md |
| "UART 驱动" / "ADC 驱动" / "I2C 驱动" / "TIM 驱动" | REFERENCE/HAL_DRIVERS.md + EXAMPLES/DRIVERS.md |
| "printf 重定向" / "printf 输出" / "ITM" | REFERENCE/STD_LIBS.md |
| "DMA 接收" / "不定长数据" | REFERENCE/HAL_DRIVERS.md + EXAMPLES/DRIVERS.md |

### 代码审查/问题排查请求

| 用户说... | 读取文件 |
|-----------|----------|
| "中断" / "FromISR" / "portYIELD_FROM_ISR" / "优先级配置" | PATTERNS/INTERRUPT.md |
| "死锁" / "优先级反转" / "堆栈溢出" / "资源泄漏" | PATTERNS/TRAPS.md |
| "生产者-消费者" / "状态机" / "资源池" / "发布-订阅" | PATTERNS/DESIGN.md |

### 调试请求

| 用户说... | 读取文件 |
|-----------|----------|
| "SystemView" / "TRACEalyzer" / "trace 分析" | REFERENCE/DEBUG_TOOLS.md |
| "任务统计" / "堆栈监控" / "CPU 使用率" | REFERENCE/DEBUG_TOOLS.md |

### 高级应用请求

| 用户说... | 读取文件 |
|-----------|----------|
| "低功耗" / "Tickless" / "STOP 模式" | EXAMPLES/ADVANCED.md |
| "CubeMX 配置" / "STM32CubeMX" | EXAMPLES/ADVANCED.md |
| "传感器融合" / "多任务" | EXAMPLES/ADVANCED.md |

### API 查询请求

| 用户说... | 读取文件 |
|-----------|----------|
| "xTaskCreate 参数" / "API 语法" / "函数说明" | REFERENCE/FREERTOS_API.md |

### 使用方法

如果用户请求不够明确，无法判断读取哪个文件：
1. 先读取 SKILL.md 和 REFERENCE/FREERTOS_API.md
2. 询问用户具体需求
3. 根据回答读取正确的文件

**不要一次性读取所有文件！只读取与用户请求相关的文件。**

---

## 技能简介

本技能专为在 **STM32 微控制器** 上使用 **FreeRTOS 实时操作系统** 进行嵌入式开发而设计。AI 将作为"嵌入式系统架构师"，帮助你编写安全、高效、可维护的 C 代码。

**适用场景：**
- 使用 STM32CubeMX 生成的工程
- ARM Cortex-M 全系列（F0/F1/F3/F4/F7/H7/G0/L0/L4/L5 等）
- FreeRTOS v10+ 版本
- 原生 FreeRTOS API 或 CMSIS-RTOS v2 API

---

## 使用场景

### 代码生成
- 创建任务、队列、信号量、互斥锁
- 编写外设驱动模板（UART DMA、ADC DMA、I2C 等）
- 配置低功耗 Tickless 模式
- 实现 printf 重定向（ITM_SendChar / UART）

### 代码审查
- 分析任务优先级配置是否合理
- 检查中断与任务交互的正确性
- 排查死锁、优先级反转、资源泄漏
- 验证 FreeRTOSConfig.h 配置

### 教学辅导
- 解释 FreeRTOS 核心概念（任务调度、上下文切换）
- 演示生产者-消费者、发布-订阅等设计模式
- 指导调试工具使用（SEGGER SystemView、TRACEalyzer）

---

## 核心能力模块

### 任务管理
- 创建静态/动态任务（`xTaskCreate`, `xTaskCreateStatic`）
- 设置优先级、堆栈大小、任务名
- 任务状态监控（`uxTaskGetStackHighWaterMark`）

### 任务间通信
- **队列（Queue）**：生产者-消费者模型
- **信号量（Semaphore）**：二值/计数型
- **互斥锁（Mutex）**：避免竞态条件，含优先级继承
- **事件组（Event Groups）**：多条件等待
- **任务通知（Task Notifications）**：轻量级替代方案

### 中断与任务交互
- 在 HAL 回调中使用 `xQueueSendFromISR` / `vTaskNotifyGiveFromISR`
- ISR 中不阻塞，仅发送通知
- `portYIELD_FROM_ISR(xHigherPriorityTaskWoken)` 用法

### 外设集成
- **UART DMA + 队列**：不定长数据接收（IDLE 中断）
- **ADC DMA + 任务通知**：连续采样
- **I2C 主/从模式**：传感器通信
- **TIM 定时器/PWM**：周期任务

### 内存与性能优化
- 推荐静态分配（避免 heap 碎片）
- 合理估算堆栈大小
- 开启 `configASSERT()` 和 `configCHECK_FOR_STACK_OVERFLOW`
- 使用 `configUSE_PREEMPTION = 1` 提升实时性

### 调试与诊断
- 生成任务列表打印代码（`vTaskList`）
- SEGGER SystemView（Keil/IAR 环境）
- Percep TRACEalyzer（FreeRTOS 环境）
- ITM/SWO 配置与 printf 调试

---

## 文件索引

| 类型 | 文件 | 说明 |
|------|------|------|
| 主文件 | SKILL.md | AI 唯一自动读取的文件 |
| 用户指南 | USER_GUIDE.md | 仅用户阅读，不读取 |
| API 参考 | REFERENCE/FREERTOS_API.md | FreeRTOS API 语法 |
| API 参考 | REFERENCE/STD_LIBS.md | 标准库集成 |
| API 参考 | REFERENCE/HAL_DRIVERS.md | HAL 外设驱动 |
| API 参考 | REFERENCE/DEBUG_TOOLS.md | 调试工具配置 |
| 代码示例 | EXAMPLES/BASIC.md | 基础组件示例 |
| 代码示例 | EXAMPLES/DRIVERS.md | 外设驱动模板 |
| 代码示例 | EXAMPLES/ADVANCED.md | 高级应用 |
| 设计模式 | PATTERNS/DESIGN.md | 设计模式 |
| 设计模式 | PATTERNS/INTERRUPT.md | 中断最佳实践 |
| 设计模式 | PATTERNS/TRAPS.md | 常见陷阱 |

---

## 脚本工具

### freertos_config_check.py

验证 FreeRTOSConfig.h 关键配置：

```bash
python scripts/freertos_config_check.py FreeRTOSConfig.h
```

输出 JSON 格式，便于 CI 集成。
