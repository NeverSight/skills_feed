---
name: pw-embedded-c-style
description: 嵌入式 C 代码风格助手, 基于 51 单片机教学项目的代码规范。默认使用蛇形命名 (snake_case), 可选驼峰命名。用于创建符合嵌入式开发规范的项目结构, 优化代码风格, 提供硬件驱动模板。适用于 51 单片机、STM32 等嵌入式 C 项目开发。
---

# pw-embedded-c-style

嵌入式 C 代码风格助手, 基于《手把手教你学51单片机》302 个 .c 文件和 66 个 .h 文件的代码风格分析。

**默认命名风格: 蛇形命名 (snake_case)**

## 使用场景

### 适用情况

- 创建新的嵌入式 C 项目 (51 单片机、STM32 等)
- 优化现有嵌入式代码的命名和结构
- 生成硬件驱动模块 (定时器、串口、LCD、按键等)
- 规范化项目文件组织和代码风格
- 学习嵌入式 C 编程的最佳实践

### 不适用情况

- 非嵌入式的通用 C/C++ 项目
- 需要 RTOS 或复杂架构的项目
- 纯算法实现 (无硬件交互)

## 使用方式

**默认命名风格: 蛇形命名 (snake_case)**

如需使用驼峰命名，请在指令中明确说明 "使用驼峰命名"。

### 创建项目

```bash
# 基础示例 (默认蛇形命名)
/pw-embedded-c-style 创建一个 LED 闪烁的项目

# 带外设的项目
/pw-embedded-c-style 创建一个带 LCD1602 显示和按键输入的项目

# 指定芯片
/pw-embedded-c-style 为 STM32F103 创建一个串口通信项目

# 明确指定使用驼峰命名
/pw-embedded-c-style 使用驼峰命名创建一个定时器项目
```

### 优化代码

```bash
# 优化代码风格 (默认蛇形命名)
/pw-embedded-c-style 帮我优化这段按键扫描代码

# 重构模块
/pw-embedded-c-style 将这段代码重构为独立的驱动模块

# 添加注释
/pw-embedded-c-style 为这段定时器配置代码添加规范注释

# 使用驼峰命名优化
/pw-embedded-c-style 使用驼峰命名优化这段代码
```

### 生成驱动模板

```bash
# 生成特定外设驱动
/pw-embedded-c-style 生成 DS1302 实时时钟驱动模板

# 生成通信协议
/pw-embedded-c-style 生成串口通信的收发缓冲区实现
```

---

## 核心规范

### 命名规范

**默认风格: 蛇形命名 (snake_case)**

```c
// 函数: 蛇形命名
void config_timer0(unsigned int ms);
void lcd_write_cmd(unsigned char cmd);
void init_ds1302(void);

// 变量: 蛇形命名
unsigned char flag_500ms = 0;
unsigned char cnt_rxd = 0;

// 宏/常量: 全大写下划线
#define SYS_MCLK    (11059200/12)
#define LCD1602_RS  P1^0

// sbit: 全大写或蛇形
sbit LED = P0^0;
sbit EN_LED = P1^4;
```

**备选风格: 驼峰命名 (camelCase/PascalCase)**

用户明确要求时使用此风格:

```c
// 函数: 大驼峰
void ConfigTimer0(unsigned int ms);
void LcdWriteCmd(unsigned char cmd);
void InitDS1302(void);

// 变量: 小驼峰
unsigned char flag500ms = 0;
unsigned char cntRxd = 0;

// 宏/常量: 全大写下划线 (相同)
#define SYS_MCLK    (11059200/12)
#define LCD1602_RS  P1^0

// sbit: 全大写或大驼峰
sbit LED = P0^0;
sbit ENLED = P1^4;
```

### 代码组织

**单文件项目**
```c
#include <reg52.h>

// 宏定义
// sbit 定义
// 全局变量
// 函数声明

void main() { }
// 函数实现
// 中断函数
```

**多文件项目**
```
config.h    - 全局配置 (类型定义、系统参数、IO 定义)
module.h    - 模块头文件 (结构体、extern 声明、函数声明)
module.c    - 模块实现 (#define _MODULE_C)
main.c      - 主程序
```

### 常用模式

**定时器配置**
```c
void config_timer0(unsigned int ms)
{
    unsigned long tmp;
    tmp = 11059200 / 12;
    tmp = (tmp * ms) / 1000;
    tmp = 65536 - tmp;
    tmp = tmp + 12;
    T0RH = (unsigned char)(tmp>>8);
    T0RL = (unsigned char)tmp;
    TMOD &= 0xF0;
    TMOD |= 0x01;
    TH0 = T0RH;
    TL0 = T0RL;
    ET0 = 1;
    TR0 = 1;
}
```

**中断服务函数**
```c
void interrupt_timer0() interrupt 1
{
    static unsigned char tmr_500ms = 0;
    TH0 = T0RH;
    TL0 = T0RL;
    if (++tmr_500ms >= 50)
    {
        tmr_500ms = 0;
        flag_500ms = 1;
    }
}
```

**标志位驱动**
```c
bit flag_500ms = 0;

// 中断中设置
flag_500ms = 1;

// 主循环检测
while (1)
{
    if (flag_500ms)
    {
        flag_500ms = 0;
        // 执行任务
    }
}
```

**按键消抖**
```c
void key_scan(void)
{
    static unsigned char keybuf[4] = {0xFF, 0xFF, 0xFF, 0xFF};
    keybuf[i] = (keybuf[i] << 1) | KEY_IN[i];
    if ((keybuf[i] & 0x0F) == 0x00)
        key_sta[i] = 0;  // 稳定按下
}
```

**查表法**
```c
unsigned char code led_char[] = {
    0xC0, 0xF9, 0xA4, 0xB0, 0x99, 0x92, 0x82, 0xF8,
    0x80, 0x90, 0x88, 0x83, 0xC6, 0xA1, 0x86, 0x8E
};
P0 = led_char[num];
```

### 注释风格

```c
/* 文件头注释 */
/*
*******************************************************************************
* 文件名称: main.c
* 描  述: 功能描述
* 版本号: v1.0.0
*******************************************************************************
*/

/* 函数注释 */
void lcd_show_str(unsigned char x, unsigned char y,
                  unsigned char *str, unsigned char len)

// 行内注释
EA = 1;                     // 使能总中断
config_timer0(10);          // 配置 T0 定时 10ms
```

---

## 代码风格特点

- 简洁直接, 避免过度抽象
- 直接操作硬件寄存器
- 使用 sbit 定义 IO 口
- 中断向量号直接指定 (interrupt 1)
- 存储区域修饰符 (code, pdata)
- 标志位驱动主循环
- 查表法处理数据映射

---

## 最佳实践

### 命名风格选择

**默认使用蛇形命名 (snake_case):**
- 符合 Linux 内核和大多数开源嵌入式项目的风格
- 单词分隔明显, 可读性好
- 适合生产项目和团队协作

**使用驼峰命名 (camelCase/PascalCase) 的场景:**
- 教学项目或参考教材使用驼峰命名
- 团队明确要求使用驼峰命名
- 需要与现有驼峰命名代码保持一致

**重要原则: 整个项目必须统一命名风格**

### 项目创建建议

1. 单文件项目: 适用于简单功能 (LED 闪烁、按键检测等)
2. 多文件项目: 适用于多外设协同 (LCD + 按键 + 串口等)
3. 模块化驱动: 每个外设独立为 .h/.c 文件对

### 代码优化建议

1. 命名规范: 默认使用蛇形命名 (函数/变量), 宏用全大写下划线
2. 中断精简: 中断函数只设置标志位, 主循环处理业务逻辑
3. 硬件抽象: 使用宏定义隔离硬件相关代码, 便于移植
4. 注释清晰: 关键寄存器配置必须添加行内注释

### 常见错误处理

**问题 1: 定时器不准确**
```c
// 错误: 未考虑指令周期补偿
tmp = 65536 - tmp;

// 正确: 加上补偿值
tmp = 65536 - tmp;
tmp = tmp + 12;  // 补偿中断响应延迟
```

**问题 2: 按键抖动**
```c
// 错误: 直接读取按键状态
if (KEY == 0) { /* 处理 */ }

// 正确: 使用移位寄存器消抖
keybuf = (keybuf << 1) | KEY;
if ((keybuf & 0x0F) == 0x00) { /* 稳定按下 */ }
```

**问题 3: 全局变量冲突**
```c
// 错误: 多个模块使用相同变量名
unsigned char flag;  // 在多个 .c 文件中定义

// 正确: 使用模块前缀或 static
static unsigned char uart_flag;  // 仅本文件可见
extern unsigned char g_system_flag;  // 全局共享
```

### 注意事项

- 中断函数必须尽快返回, 避免长时间占用
- 全局变量在中断和主循环共享时, 使用 volatile 修饰
- 大数组使用 code 修饰符存储在 ROM 中, 节省 RAM
- 延时函数不要在中断中调用
- 多文件项目必须使用 extern 正确声明全局变量

---

## 技术参数说明

### 支持的芯片平台

- 51 系列: AT89C51, STC89C52, STC15 等
- STM32 系列: F103, F407 等 (需调整寄存器定义)
- 其他 8051 兼容芯片

### 代码规范来源

基于《手把手教你学51单片机》实际教学项目:
- 302 个 .c 源文件
- 66 个 .h 头文件
- 涵盖 20+ 种常用外设驱动
- 默认采用蛇形命名, 更符合嵌入式 C 项目规范

### 输出格式

- 单文件项目: 生成 main.c
- 多文件项目: 生成 config.h, module.h, module.c, main.c
- 驱动模块: 生成 driver.h, driver.c

---

## 示例场景

### 场景 1: 快速原型验证

用户需求: "创建一个 LED 每秒闪烁的程序"

助手输出:
- 单个 main.c 文件
- 包含定时器配置和中断函数
- 使用标志位驱动 LED 翻转

### 场景 2: 模块化项目

用户需求: "创建一个带 LCD1602 显示温度和按键调节的项目"

助手输出:
- config.h (系统配置)
- lcd1602.h/c (LCD 驱动)
- key.h/c (按键驱动)
- ds18b20.h/c (温度传感器驱动)
- main.c (主程序)

### 场景 3: 代码优化

用户需求: "优化这段串口接收代码"

助手操作:
- 检查命名规范
- 优化缓冲区管理
- 添加溢出保护
- 补充注释说明

---

基于实际教学项目总结, 注重实用性和可读性。默认使用蛇形命名风格, 符合嵌入式 C 项目规范。
